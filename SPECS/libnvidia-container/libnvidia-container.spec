%define modprobe_version 450.57
%define _major 1
%define mod_probe_dir deps/src/nvidia-modprobe-%{modprobe_version}
Summary:        NVIDIA container runtime library
Name:           libnvidia-container
Version:        1.3.3
Release:        3%{?dist}
License:        BSD AND ASL2.0 AND GPLv3+ AND LGPLv3+ AND MIT AND GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/NVIDIA/libnvidia-container
#Source0:       https://github.com/NVIDIA/%%{name}/archive/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
#Source1:       https://github.com/NVIDIA/nvidia-modprobe/archive/%%{modprobe_version}.tar.gz
Source1:        nvidia-modprobe-%{modprobe_version}.tar.gz
Patch0:         common.mk.patch
Patch1:         libtirpc.patch
Patch2:         nvidia-modprobe.patch
BuildRequires:  libseccomp-devel
BuildRequires:  libtirpc-devel
BuildRequires:  make
BuildRequires:  rpcsvc-proto
BuildRequires:  which

%description
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

mkdir -p %{mod_probe_dir}
tar -C %{mod_probe_dir} --strip-components=1 -xzf %{SOURCE1}
%patch2 -p1 -d %{mod_probe_dir}
touch %{mod_probe_dir}/.download_stamp

%build
%make_build WITH_LIBELF=yes

%install
DESTDIR=%{buildroot} make install prefix=%{_prefix} \
	exec_prefix=%{_prefix} \
	bindir=%{_bindir} \
	libdir=%{_libdir} \
	includedir=%{_includedir}\
	docdir=%{_licensedir} \
	WITH_LIBELF=yes

%package -n %{name}%{_major}
Summary:        NVIDIA container runtime library

%description -n %{name}%{_major}
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

This package requires the NVIDIA driver (>= 340.29) to be installed separately.

%package devel
Summary:        NVIDIA container runtime library (development files)
Requires:       %{name}%{_major}%{?_isa} = %{version}-%{release}

%description devel
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

This package contains the files required to compile programs with the library.

%package static
Summary:        NVIDIA container runtime library (static library)
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

This package requires the NVIDIA driver (>= 340.29) to be installed separately.

%define debug_package %{nil}

%package -n %{name}%{_major}-debuginfo
Summary:        NVIDIA container runtime library (debugging symbols)
Requires:       %{name}%{_major}%{?_isa} = %{version}-%{release}

%description -n %{name}%{_major}-debuginfo
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

This package contains the debugging symbols for the library.

%package tools
Summary:        NVIDIA container runtime library (command-line tools)
Requires:       %{name}%{_major}%{?_isa} = %{version}-%{release}

%description tools
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

This package contains command-line tools that facilitate using the library.

%post -n %{name}%{_major} -p /sbin/ldconfig
%postun -n %{name}%{_major} -p /sbin/ldconfig

%files -n %{name}%{_major}
%license %{_licensedir}/*
%{_libdir}/lib*.so.*

%files devel
%license %{_licensedir}/*
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files static
%license %{_licensedir}/*
%{_libdir}/lib*.a

%files -n %{name}%{_major}-debuginfo
%license %{_licensedir}/*
%{_libdir}/debug%{_libdir}/lib*.so.*

%files tools
%license %{_licensedir}/*
%{_bindir}/*

%changelog
* Tue Jun 22 2021 Thomas Crain <thcrain@microsoft.com. - 1.3.3-3
- Fix improper usage of %%{_lib} macro

* Fri Apr 23 2021 joseph knierman <joknierm@microsoft.com> - 1.3.3-2
- License verified
- Initial CBL-Mariner import from NVIDIA (license: ASL 2.0).

* Fri Feb 05 2021 NVIDIA CORPORATION <cudatools@nvidia.com> 1.3.3-1
- Promote 1.3.3-0.1.rc.2 to 1.3.3-1

* Wed Feb 03 2021 NVIDIA CORPORATION <cudatools@nvidia.com> 1.3.3-0.1.rc.2
- Remove path_join() with already chrooted directory

* Wed Feb 03 2021 NVIDIA CORPORATION <cudatools@nvidia.com> 1.3.3-0.1.rc.1
- Pre-create MIG related nvcaps at startup
- Add more logging around device node creation with --load-kmods

* Mon Jan 25 2021 NVIDIA CORPORATION <cudatools@nvidia.com> 1.3.2-1
- Fix handling of /proc/PID/cgroups entries with colons in paths
- Add pread64 as allowed syscall for ldconfig

* Mon Dec 07 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.3.1-1
- Honor OPT_NO_CGROUPS in nvc_device_mig_caps_mount
- Fix bug in resolving absolute symlinks in find_library_paths()

* Wed Sep 16 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.3.0-1
- Promote 1.3.0-0.1.rc.1 to 1.3.0-1

* Fri Aug 21 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.3.0-0.1.rc.1
- 2bda067f Add support to "list" command to print /dev based capabilities
- 3c2ad6aa Add logic to conditionally mount /dev based nvidia-capabilities
- 4d432175 Change default "list" command to set mig-config / mig-monitor = NULL
- 3ec7f3ba Fix minor bug that would not unmount paths on failure
- b5c0a394 Update nvidia-modprobe dependency to 450.57

* Wed Jul 08 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.2.0-1
- Promote 1.2.0-0.1.rc.3 to 1.2.0-1

* Wed Jul 01 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.2.0-0.1.rc.3
- 7deea6b8 WSL2 Support - Remove unnecessary umount and free
- 53739009 WSL2 Support - Fix error path when mounting the driver
- 38198a81 WSL2 Support - Fix error path in dxcore
- 31f5ea35 Changed email for travis.ci to kklues@nvidia.com
- abdd5175 Update license and copyright in packages
- 65827fe7 Update license clause to reflect actual licensing
- 77499d88 Transition Travis CI build to Ubuntu 18.04

* Thu Jun 18 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.2.0-0.1.rc.2
- 4ea9b59f Update debian based dockerfiles to set distribution in changelog
- a57fcea5 Add 'ngx' as a new capability for a container
- 6f16ccd3 Allow --mig-monitor and --mig-config on machines without MIG capable GPUs

* Thu Jun 11 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.2.0-0.1.rc.1
- 4263e684 Add support for Windows Subsystem for Linux (WSL2)
- e768f8bc Fix ability to build RC packages via TAG=rc.<num>

* Tue May 19 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.1.1-1
- deeb499 Fixup deb packaging files to remove warnings
- 6003504 nvmlSystemGetCudaDriverVersion_v2 to nvmlSystemGetCudaDriverVersion
- 1ee8b60 Update centos8/rhel8 to conditionally set appropriate CFLAGS and LDLIBS
- d746370 Add smoke test to verify functioning build for all OSs on amd64/x86_64

* Fri May 15 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.1.0-1
- b217c6ad Update build system to support multi-arch builds
- 1ddcdfc1 Add support for MIG (Milti-Instance-GPUs)
- ddae363a Add libnvidia-allocator.so as a compute-lib
- 6ed0f129 Add option to not use pivot_root
- e18e9b7a Allow devices to be identified by PCI bus ID

* Mon Nov 11 2019 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.7-1
- 8d90918a Add Raytracing library

* Fri Sep 013 2019 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.6-1
- b6aff41 Update error messages for CUDA version requirements

* Wed Sep 04 2019 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.5-1
- 688495e Add Opensuse15.1 support

* Wed Aug 21 2019 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.4-1
- 61bfaf38 Update DSL to output the first element instead of the last in case of failure
- 5ce32c6c Add initial support for Optix
- acc38a22 Fix execveat typo
- b5e491b1 arm64: Add support for AARCH64 architecture

* Thu Jul 18 2019 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.3-1
- b9545d7 Add support for Vulkan

* Tue Feb 05 2019 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.2-1
- 4045013 Adds support for libnvidia-opticalflow

* Mon Jan 14 2019 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.1-1
- deccb28 Allow yet more syscalls in ldconfig

* Thu Sep 20 2018 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.0-1
- 35a9f27 Add support for CUDA forward compatibility
- ebed710 Add device brand to the device informations and requirements
- a141a7a Handle 32-bit PCI domains in procfs
- 391c4b6 Preload glibc libraries before switching root
- bcf69c6 Bump libtirpc to 1.1.4
- 30aec17 Bump nvidia-modprobe-utils to 396.51
- d05745f Bump the address space limits for ldconfig

* Mon Jun 11 2018 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.0-0.1.rc.2
- 7ea554a Rework capabilities to support more unprivileged use-cases
- f06cbbb Fix driver process DEATHSIG teardown
- 931bd4f Allow more syscalls in ldconfig
- a0644ea Fix off-by-one error

* Thu Apr 26 2018 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.0-0.1.rc.1
- 4d43665 Bump nvidia-modprobe-utils to 396.18
- d8338a6 Bump libtirpc to 1.0.3
- cef6c8f Add execveat to the list of allowed syscalls

* Mon Mar 05 2018 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.0-0.1.beta.1
- 6822b13 Bump nvidia-modprobe-utils to 390.25
- 8245f6c Slightly improve RPC error messages
- 9398d41 Add support for display capability
- 57a0dd5 Increase driver service timeout from 1s to 10s
- e48a0d4 Add device minor to the CLI info command
- 019fdc1 Add support for custom driver root directory
- b78a28c Add ppc64le support
- 41656bf Add --ldcache option to the CLI

* Wed Jan 10 2018 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.0-0.1.alpha.3
- d268f8f Improve error message if driver installed in the container
- 3fdac29 Add optional support for libelf from the elfutils project
- 584bca5 Remove top directory bind mounts to prevent EXDEV errors
- c6dc820 Add info command to nvidia-container-cli
- 44b74ee Add device model to the device informations
- cbdd58f Strip RPC prefix from error messages
- d4ee216 Rework the CLI list command
- b0c4865 Improve the --userspec CLI option and rename it to --user
- e6fa331 Refactor the CLI and split it into multiple files
- fa9853b Bump nvidia-modprobe-utils to 387.34
- 7888296 Move the driver capabilities to the container options
- ea2f780 Add support for EGL device isolation
- b5bffa3 Fix driver procfs remount to work with unpatched kernels 

* Mon Oct 30 2017 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.0-0.1.alpha.2
- b80e4b6 Relax some requirement constraints
- 3cd1bb6 Handle 32-bit PCI domains
- 6c67a19 Add support for device architecture requirement
- 7584e96 Filter NVRM proc filesystem based on visible devices
- 93c46e1 Prevent the driver process from triggering MPS
- fe4925e Reject invalid device identifier "GPU-"
- dabef1c Do not change bind mount attributes on top-level directories

* Tue Sep 05 2017 NVIDIA CORPORATION <cudatools@nvidia.com> 1.0.0-0.1.alpha.1
- Initial release
