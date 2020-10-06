// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A worker for building packages locally

package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"gopkg.in/alecthomas/kingpin.v2"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/file"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/packagerepo/repomanager/rpmrepomanager"
	"microsoft.com/pkggen/internal/rpm"
	"microsoft.com/pkggen/internal/safechroot"
	"microsoft.com/pkggen/internal/shell"
	"microsoft.com/pkggen/internal/sliceutils"
)

const (
	chrootRpmBuildRoot      = "/usr/src/mariner"
	chrootLocalRpmsDir      = "/localrpms"
	chrootLocalRpmsCacheDir = "/upstream-cached-rpms"
)

var (
	app                  = kingpin.New("pkgworker", "A worker for building packages locally")
	srpmFile             = exe.InputFlag(app, "Full path to the SRPM to build")
	workDir              = app.Flag("work-dir", "The directory to create the build folder").Required().String()
	workerTar            = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	repoFile             = app.Flag("repo-file", "Full path to local.repo").Required().ExistingFile()
	rpmsDirPath          = app.Flag("rpm-dir", "The directory to use as the local repo and to submit RPM packages to").Required().ExistingDir()
	srpmsDirPath         = app.Flag("srpm-dir", "The output directory for source RPM packages").Required().String()
	cacheDir             = app.Flag("cache-dir", "The cache directory containing downloaded dependency RPMS from Mariner Base").Required().ExistingDir()
	noCleanup            = app.Flag("no-cleanup", "Whether or not to delete the choot folder after the build is done").Bool()
	distTag              = app.Flag("dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	distroReleaseVersion = app.Flag("distro-release-version", "The distro release version that the SRPM will be built with").Required().String()
	distroBuildNumber    = app.Flag("distro-build-number", "The distro build number that the SRPM will be built with").Required().String()
	rpmmacrosFile        = app.Flag("rpmmacros-file", "Optional file path to an rpmmacros file for rpmbuild to use").ExistingFile()
	runCheck             = app.Flag("run-check", "Run the check during package build").Bool()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

var (
	greaterThanOrEqualRegex = regexp.MustCompile(` '?>='? [^ ]*`)
	equalToRegex            = regexp.MustCompile(` '?='? `)
	lessThanOrEqualToRegex  = regexp.MustCompile(` '?<='? `)

	packageUnavailableRegex = regexp.MustCompile(`^No package \\x1b\[1m\\x1b\[30m(.+) \\x1b\[0mavailable`)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	rpmsDirAbsPath, err := filepath.Abs(*rpmsDirPath)
	logger.PanicOnError(err, "Unable to find absolute path for RPMs directory '%s'", *rpmsDirPath)

	srpmsDirAbsPath, err := filepath.Abs(*srpmsDirPath)
	logger.PanicOnError(err, "Unable to find absolute path for SRPMs directory '%s'", *srpmsDirPath)

	srpmName := strings.TrimSuffix(filepath.Base(*srpmFile), ".src.rpm")
	chrootDir := filepath.Join(*workDir, srpmName)

	defines := rpm.DefaultDefines()
	defines[rpm.DistTagDefine] = *distTag
	defines[rpm.DistroReleaseVersionDefine] = *distroReleaseVersion
	defines[rpm.DistroBuildNumberDefine] = *distroBuildNumber

	builtRPMs, err := buildSRPMInChroot(chrootDir, rpmsDirAbsPath, *workerTar, *srpmFile, *repoFile, *rpmmacrosFile, defines, *noCleanup, *runCheck)
	logger.PanicOnError(err, "Failed to build SRPM '%s'. For details see log file: %s .", *srpmFile, *logFile)

	err = copySRPMToOutput(*srpmFile, srpmsDirAbsPath)
	logger.PanicOnError(err, "Failed to copy SRPM '%s' to output directory '%s'.", *srpmFile, rpmsDirAbsPath)

	// On success write a comma-seperated list of RPMs built to stdout that can be parsed by the invoker.
	// Any output from logger will be on stderr so stdout will only contain this output.
	fmt.Printf(strings.Join(builtRPMs, ","))
}

func copySRPMToOutput(srpmFilePath, srpmOutputDirPath string) (err error) {
	const srpmsDirName = "SRPMS"

	srpmFileName := filepath.Base(srpmFilePath)
	srpmOutputFilePath := filepath.Join(srpmOutputDirPath, srpmFileName)

	err = file.Copy(srpmFilePath, srpmOutputFilePath)

	return
}

func buildSRPMInChroot(chrootDir, rpmDirPath, workerTar, srpmFile, repoFile, rpmmacrosFile string, defines map[string]string, noCleanup bool, runCheck bool) (builtRPMs []string, err error) {
	const (
		existingChrootDir = false
		squashErrors      = false

		overlaySource  = ""
		overlayWorkDir = "/overlaywork"
		rpmDirName     = "RPMS"
	)

	srpmBaseName := filepath.Base(srpmFile)
	logger.Log.Infof("Building (%s)", srpmBaseName)

	// Create the chroot used to build the SRPM
	chroot := safechroot.NewChroot(chrootDir, existingChrootDir)

	overlayMount, overlayExtraDirs := safechroot.NewOverlayMountPoint(chroot.RootDir(), overlaySource, chrootLocalRpmsDir, rpmDirPath, chrootLocalRpmsDir, overlayWorkDir)
	rpmCacheMount := safechroot.NewMountPoint(*cacheDir, chrootLocalRpmsCacheDir, "", safechroot.BindMountPointFlags, "")
	mountPoints := []*safechroot.MountPoint{overlayMount, rpmCacheMount}
	extraDirs := append(overlayExtraDirs, chrootLocalRpmsCacheDir)

	err = chroot.Initialize(workerTar, extraDirs, mountPoints)
	if err != nil {
		return
	}
	defer chroot.Close(noCleanup)

	// Place extra files that will be needed to build into the chroot
	srpmFileInChroot, err := copyFilesIntoChroot(chroot, srpmFile, repoFile, rpmmacrosFile)
	if err != nil {
		return
	}

	err = chroot.Run(func() (err error) {
		return buildRPMFromSRPMInChroot(srpmFileInChroot, runCheck, defines)
	})

	if err != nil {
		return
	}

	rpmBuildOutputDir := filepath.Join(chroot.RootDir(), chrootRpmBuildRoot, rpmDirName)
	builtRPMs, err = moveBuiltRPMs(rpmBuildOutputDir, rpmDirPath)
	if err != nil {
		return
	}

	logger.Log.Infof("Built (%s) -> %v", srpmBaseName, builtRPMs)

	return
}

func buildRPMFromSRPMInChroot(srpmFile string, runCheck bool, defines map[string]string) (err error) {
	// Convert /localrpms into a repository that a package manager can use
	err = rpmrepomanager.CreateRepo(chrootLocalRpmsDir)
	if err != nil {
		return
	}

	// Install the SRPM like a regular RPM to expand it
	err = rpm.InstallRPM(srpmFile)
	if err != nil {
		return
	}

	// Query and install the build requirements for this SRPM
	err = installBuildRequires(defines)
	if err != nil {
		return
	}

	// Remove all libarchive files on the system before issuing a build.
	// If the build environment has libtool archive files present, gnu configure
	// could detect it and create more libtool archive files which can cause
	// build failures.
	err = removeLibArchivesFromSystem()
	if err != nil {
		return
	}

	// Build the SRPM
	if runCheck {
		err = rpm.BuildRPMFromSRPM(srpmFile, defines)
	} else {
		err = rpm.BuildRPMFromSRPM(srpmFile, defines, "--nocheck")
	}

	return
}

func moveBuiltRPMs(rpmOutDir, dstDir string) (builtRPMs []string, err error) {
	const rpmExtension = ".rpm"
	err = filepath.Walk(rpmOutDir, func(path string, info os.FileInfo, fileErr error) (err error) {
		if fileErr != nil {
			return fileErr
		}

		// Only copy regular files (not unix sockets, directories, links, ...)
		if !info.Mode().IsRegular() {
			return
		}

		if !strings.HasSuffix(path, rpmExtension) {
			return
		}

		// Get the relative path of the RPM, this will include the architecture directory it lives in.
		// Then join the relative path to the destination directory, this will ensure the RPM gets placed
		// in its correct architecture directory.
		relPath, err := filepath.Rel(rpmOutDir, path)
		if err != nil {
			return
		}

		dstFile := filepath.Join(dstDir, relPath)
		err = file.Move(path, dstFile)
		if err != nil {
			return
		}

		builtRPMs = append(builtRPMs, dstFile)
		return
	})

	return
}

func installBuildRequires(defines map[string]string) (err error) {
	const (
		emptyQueryFormat = ""
	)
	// Find the SPEC file extracted from the SRPM
	specDir := filepath.Join(chrootRpmBuildRoot, "SPECS")
	allSpecFiles, err := ioutil.ReadDir(specDir)
	if err != nil {
		return
	}

	if len(allSpecFiles) != 1 {
		return fmt.Errorf("unexpected number of SPEC files extracted, wanted (1) and found (%d)", len(allSpecFiles))
	}

	specFile := filepath.Join(specDir, allSpecFiles[0].Name())
	logger.Log.Debugf("Querying SPEC (%s)", specFile)
	sourceDir := filepath.Join(chrootRpmBuildRoot, "SOURCES")
	buildRequires, err := rpm.QuerySPEC(specFile, sourceDir, emptyQueryFormat, defines, rpm.BuildRequiresArgument)
	if err != nil {
		return
	}

	if len(buildRequires) == 0 {
		return
	}

	packagesToInstall := make([]string, 0, len(buildRequires))
	for _, pkg := range buildRequires {
		// Replace version conditionals with tdnf friendly version:
		// - replace >= with "latest" (no version)
		// - replace = and <= with the exact version
		buildReq := greaterThanOrEqualRegex.ReplaceAllString(pkg, "")
		buildReq = equalToRegex.ReplaceAllString(buildReq, "-")
		buildReq = lessThanOrEqualToRegex.ReplaceAllString(buildReq, "-")

		// Add each package to the installArgs
		packagesToInstall = append(packagesToInstall, strings.TrimSpace(buildReq))
	}

	// Try matching dependencies from locally build RPMs first. If some are not available,
	// then consider the package cache. This will ensure that local packages are preferred over remote ones.
	allowCache := true
	failedToInstall, err := tdnfInstall(packagesToInstall, allowCache)
	if len(failedToInstall) != 0 {
		allowCache = false
		failedToInstall, err = tdnfInstall(failedToInstall, allowCache)
	}

	if len(failedToInstall) != 0 {
		logger.Log.Errorf("Failed to install the following packages: %v", failedToInstall)
	}

	return
}

func tdnfInstall(packages []string, allowCached bool) (failedToInstall []string, err error) {
	const (
		alreadyInstalledPostfix = "is already installed."
		noMatchingPackagesErr   = "Error(1011) : No matching packages"
		builtPackagesRepo       = "local-repo"
		cachedPackagesRepo      = "upstream-cache-repo"
		packageMatchGroup       = 1
	)

	installArgs := []string{"install", "-y", "--disablerepo=*", fmt.Sprintf("--enablerepo=%s", builtPackagesRepo)}
	if allowCached {
		installArgs = append(installArgs, fmt.Sprintf("--enablerepo=%s", cachedPackagesRepo))
	}

	installArgs = append(installArgs, packages...)
	stdout, stderr, err := shell.Execute("tdnf", installArgs...)
	foundNoMatchingPackages := false

	if err != nil {
		logger.Log.Warnf("Failed to install build requirements. stderr: %s\nstdout: %s", stderr, stdout)
		// TDNF will output an error if all packages are already installed.
		// Ignore it iff there is no other error present in stderr.
		splitStderr := strings.Split(stderr, "\n")
		for _, line := range splitStderr {
			trimmedLine := strings.TrimSpace(line)
			if trimmedLine == "" {
				continue
			}

			if strings.Contains(trimmedLine, noMatchingPackagesErr) {
				foundNoMatchingPackages = true
			}

			if !strings.HasSuffix(trimmedLine, alreadyInstalledPostfix) && trimmedLine != noMatchingPackagesErr {
				err = fmt.Errorf(trimmedLine)
				return
			}
		}
	}

	// TDNF will ignore unavailable packages that have been requested to be installed without reporting an error code.
	// Search the stdout of TDNF for such a failure and warn the user.
	// This may happen if a SPEC requires the the path to a tool (e.g. /bin/cp), so mark it as a warning for now.
	splitStdout := strings.Split(stdout, "\n")
	for _, line := range splitStdout {
		trimmedLine := strings.TrimSpace(line)
		matches := packageUnavailableRegex.FindStringSubmatch(trimmedLine)
		if len(matches) == 0 {
			continue
		}

		failedToInstall = append(failedToInstall, matches[packageMatchGroup])
	}

	// TDNF will output the error "Error(1011) : No matching packages" if all packages could not be found.
	// In this case it will not print any of the individual packages that failed.
	if foundNoMatchingPackages && len(failedToInstall) == 0 {
		failedToInstall = packages
	}

	if len(failedToInstall) != 0 {
		err = fmt.Errorf("unable to install the following packages: %v", failedToInstall)
	}

	return
}

// removeLibArchivesFromSystem removes all libarchive files on the system. If
// the build environment has libtool archive files present, gnu configure could
// detect it and create more libtool archive files which can cause build failures.
func removeLibArchivesFromSystem() (err error) {
	dirsToExclude := []string{"/proc", "/dev", "/sys", "/run"}

	err = filepath.Walk("/", func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// Skip directories that are meant for device files and kernel virtual filesystems.
		// These will not contain .la files and are mounted into the safechroot from the host.
		if info.IsDir() && sliceutils.Find(dirsToExclude, path) != -1 {
			return filepath.SkipDir
		}

		if strings.HasSuffix(info.Name(), ".la") {
			return os.Remove(path)
		}

		return nil
	})

	if err != nil {
		logger.Log.Warnf("Unable to remove lib archive file: %s", err)
	}

	return
}

// copyFilesIntoChroot copies several required build specific files into the chroot.
func copyFilesIntoChroot(chroot *safechroot.Chroot, srpmFile, repoFile, rpmmacrosFile string) (srpmFileInChroot string, err error) {
	const (
		chrootRepoDestDir = "/etc/yum.repos.d"
		chrootSrpmDestDir = "/root/SRPMS"
		rpmmacrosDest     = "/usr/lib/rpm/macros.d/macros.override"
	)

	repoFileInChroot := filepath.Join(chrootRepoDestDir, filepath.Base(repoFile))
	srpmFileInChroot = filepath.Join(chrootSrpmDestDir, filepath.Base(srpmFile))

	filesToCopy := []safechroot.FileToCopy{
		safechroot.FileToCopy{
			Src:  repoFile,
			Dest: repoFileInChroot,
		},
		safechroot.FileToCopy{
			Src:  srpmFile,
			Dest: srpmFileInChroot,
		},
	}

	if rpmmacrosFile != "" {
		rpmmacrosCopy := safechroot.FileToCopy{
			Src:  rpmmacrosFile,
			Dest: rpmmacrosDest,
		}
		filesToCopy = append(filesToCopy, rpmmacrosCopy)
	}

	err = chroot.AddFiles(filesToCopy...)
	return
}
