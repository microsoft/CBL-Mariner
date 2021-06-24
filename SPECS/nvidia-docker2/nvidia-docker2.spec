%global debug_package %{nil}
Summary:        nvidia-docker CLI wrapper
Name:           nvidia-docker2
Version:        2.6.0
Release:        2%{?dist}
License:        ASL2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development Tools
URL:            https://github.com/NVIDIA/nvidia-docker
#Source0:       https://github.com/NVIDIA/nvidia-docker/archive/v%%{version}.tar.gz
Source0:        nvidia-docker-%{version}.tar.gz
Requires:       nvidia-container-runtime >= 3.4.2
Conflicts:      nvidia-docker < 2.0.0
BuildArch:      noarch

%description
Replaces nvidia-docker with a new implementation based on nvidia-container-runtime

%prep
%autosetup -n nvidia-docker-%{version}
cp nvidia-docker daemon.json LICENSE ..

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 -t %{buildroot}%{_bindir} nvidia-docker
mkdir -p %{buildroot}%{_sysconfdir}/docker
install -m 644 -t %{buildroot}%{_sysconfdir}/docker daemon.json

%files
%license LICENSE
%{_bindir}/nvidia-docker
%config %{_sysconfdir}/docker/daemon.json

%changelog
* Wed May 19 2021 Joseph Knierman <joknierm@nvidia.com> - 2.6.0-2
- License verified
- Initial CBL-Mariner import from NVIDIA (license: ASL 2.0).

* Thu Apr 29 2021 NVIDIA CORPORATION <cudatools@nvidia.com> 2.6.0-1
- Add dependence on nvidia-container-runtime >= 3.5.0
- Add Jenkinsfile for building packages

* Wed Sep 16 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 2.5.0-1
- Bump version to v2.5.0
- Add dependence on nvidia-container-runtime >= 3.4.0
- Update readme to point to the official documentatio
- Add %config directive to daemon.json for RPM installations

* Wed Jul 08 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 2.4.0-1
- 09a01276 Update package license to match source license
- b9c70155 Update dependence on nvidia-container-runtime to 3.3.0

* Fri May 15 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 2.3.0-1
- 0d3b049a Update build system to support multi-arch builds
- 8557216d Require new MIG changes
