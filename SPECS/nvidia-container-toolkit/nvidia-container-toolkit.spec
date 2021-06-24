%global debug_package %{nil}
Summary:        NVIDIA container runtime hook
Name:           nvidia-container-toolkit
Version:        1.4.2
Release:        2%{?dist}
License:        ALS2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/NVIDIA/nvidia-container-runtime
#Source0:       https://github.com/NVIDIA/%%{name}/archive/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/NVIDIA/%%{name}/archive/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         nvidia-container-toolkit-1.4.2.patch
BuildRequires:  golang
Provides:       nvidia-container-runtime-hook

%description
Provides a OCI hook to enable GPU support in containers.

%prep
%autosetup -p1
tar -xvf %{SOURCE1}

%build
go build -ldflags "-s -w " -o "nvidia-container-toolkit" ./pkg

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 -t %{buildroot}%{_bindir} nvidia-container-toolkit

cp config/config.toml.centos config.toml
mkdir -p %{buildroot}%{_sysconfdir}/nvidia-container-runtime
install -m 644 -t %{buildroot}%{_sysconfdir}/nvidia-container-runtime config.toml

mkdir -p %{buildroot}%{_libexecdir}/oci/hooks.d
install -m 755 -t %{buildroot}%{_libexecdir}/oci/hooks.d oci-nvidia-hook

mkdir -p %{buildroot}%{_datadir}/containers/oci/hooks.d
install -m 644 -t %{buildroot}%{_datadir}/containers/oci/hooks.d oci-nvidia-hook.json

%posttrans
ln -sf %{_bindir}/nvidia-container-toolkit %{_bindir}/nvidia-container-runtime-hook

%postun
rm -f %{_bindir}/nvidia-container-runtime-hook

%files
%license LICENSE
%{_bindir}/nvidia-container-toolkit
%config %{_sysconfdir}/nvidia-container-runtime/config.toml
%{_libexecdir}/oci/hooks.d/oci-nvidia-hook
%{_datadir}/containers/oci/hooks.d/oci-nvidia-hook.json

%changelog
* Mon Apr 26 2021 Joseph Knierman <joknierm@microsoft.com> - 1.4.2-2
- License verified
- Initial CBL-Mariner import from NVIDIA (license: ASL 2.0).

* Fri Feb 05 2021 NVIDIA CORPORATION <cudatools@nvidia.com> 1.4.2-1
- Add dependence on libnvidia-container-tools >= 1.3.3

* Mon Jan 25 2021 NVIDIA CORPORATION <cudatools@nvidia.com> 1.4.1-1
- Ignore NVIDIA_VISIBLE_DEVICES for containers with insufficent privileges
- Add dependence on libnvidia-container-tools >= 1.3.2

* Fri Dec 11 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.4.0-1
- Add 'compute' capability to list of defaults
- Add dependence on libnvidia-container-tools >= 1.3.1

* Wed Sep 16 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.3.0-1
- Promote 1.3.0-0.1.rc.2 to 1.3.0-1
- Add dependence on libnvidia-container-tools >= 1.3.0

* Mon Aug 10 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.3.0-0.1.rc.2
- 2c180947 Add more tests for new semantics with device list from volume mounts
- 7c003857 Refactor accepting device lists from volume mounts as a boolean

* Fri Jul 24 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.3.0-0.1.rc.1
- b50d86c1 Update build system to accept a TAG variable for things like rc.x
- fe65573b Add common CI tests for things like golint, gofmt, unit tests, etc.
- da6fbb34 Revert "Add ability to merge envars of the form NVIDIA_VISIBLE_DEVICES_*"
- a7fb3330 Flip build-all targets to run automatically on merge requests
- 8b248b66 Rename github.com/NVIDIA/container-toolkit to nvidia-container-toolkit
- da36874e Add new config options to pull device list from mounted files instead of ENVVAR

* Wed Jul 22 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.2.1-1
- 4e6e0ed4 Add 'ngx' to list of *all* driver capabilities
- 2f4af743 List config.toml as a config file in the RPM SPEC

* Wed Jul 08 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.2.0-1
- 8e0aab46 Fix repo listed in changelog for debian distributions
- 320bb6e4 Update dependence on libnvidia-container to 1.2.0
- 6cfc8097 Update package license to match source license
- e7dc3cbb Fix debian copyright file
- d3aee3e0 Add the 'ngx' driver capability

* Wed Jun 03 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.1.2-1
- c32237f3 Add support for parsing Linux Capabilities for older OCI specs

* Tue May 19 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.1.1-1
- d202aded Update dependence to libnvidia-container 1.1.1

* Fri May 15 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.1.0-1
- 4e4de762 Update build system to support multi-arch builds
- fcc1d116 Add support for MIG (Multi-Instance GPUs)
- d4ff0416 Add ability to merge envars of the form NVIDIA_VISIBLE_DEVICES_* 
- 60f165ad Add no-pivot option to toolkit
