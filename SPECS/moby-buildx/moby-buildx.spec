Summary: A Docker CLI plugin for extended build capabilities with BuildKit
Name: moby-buildx
Version: 0.4.1+azure
Release: 4%{?dist}
License: ASL 2.0
Group: Tools/Container

# Git clone is a standard practice of producing source files for moby.
# Please look at ./generate-sources.sh for generating source tar ball.
# buildx sources are git cloned to tag 0.4.1
# BUILDX_REPO=https://github.com/docker/buildx.git
%define BUILDX_GITCOMMIT bda4882a65349ca359216b135896bddc1d92461c
%define vernum %(echo "%{version}" | cut -d+ -f1)
#Source0: https://github.com/docker/buildx/archive/v%{vernum}.tar.gz
Source0: moby-buildx-%{version}.tar.gz
Patch0: CVE-2019-5736_0a8e41.patch
Patch1: CVE-2019-5736_6635b4.patch
Source1: LICENSE
Source2: NOTICE
URL: https://www.github.com/docker/buildx
Vendor: Microsoft Corporation
Distribution: Mariner

BuildRequires: bash
BuildRequires: golang
# Removed requirement for go-md2man since this is not available in non-adm64 repos
# Maybe we can just build our own packages... for now this gets built/installed  before running rpmbuild

# required packages on install
Requires: /bin/sh

# conflicting packages
Conflicts: docker-ce
Conflicts: docker-ee

%description
A Docker CLI plugin for extended build capabilities with BuildKit

%define OUR_GOPATH %{_topdir}/.gopath

%prep
%autosetup -n %{name}-%{version} -c
mkdir -p %{OUR_GOPATH}/src/github.com/docker
ln -sfT %{_topdir}/BUILD/%{name}-%{version} %{OUR_GOPATH}/src/github.com/docker/buildx

%build
export GOPATH=%{OUR_GOPATH}
export GOCACHE=%{OUR_GOPATH}/.cache
export GOPROXY=direct
export GO111MODULE=on
export CGO_ENABLED=0
# GOFLAGS for go1.13 only
#export GOFLAGS='-trimpath -gcflags=all="-trimpath=%{OUR_GOPATH}/src" -asmflags=all="-trimpath=%{OUR_GOPATH}/src"'
export GOGC=off

cd %{OUR_GOPATH}/src/github.com/docker/buildx
go build -mod=vendor \
    -ldflags "-X github.com/docker/buildx/version.Version=%{version} -X github.com/docker/buildx/version.Revision=%{BUILDX_GITCOMMIT} -X github.com/docker/buildx/version.Package=github.com/docker/buildx" \
    -o buildx \
    ./cmd/buildx

%install
# install binary
mkdir -p "%{buildroot}/%{_libexecdir}/docker/cli-plugins"
cp -aT buildx "%{buildroot}/%{_libexecdir}/docker/cli-plugins/docker-buildx"

# copy legal files
mkdir -p %{buildroot}/usr/share/doc/%{name}-%{version}
cp %{SOURCE1} %{buildroot}/usr/share/doc/%{name}-%{version}/LICENSE
cp %{SOURCE2} %{buildroot}/usr/share/doc/%{name}-%{version}/NOTICE

%post

%preun

%postun

%files
%license LICENSE
/usr/share/doc/%{name}-%{version}/*
%{_libexecdir}/docker/cli-plugins/docker-buildx

%changelog
*   Fri Jul 16 2021 Mariner Autopatcher <cblmargh@microsoft.com> 0.4.1+azure-4
-   Added patch file(s) CVE-2019-5736_0a8e41.patch,
-   CVE-2019-5736_6635b4.patch
* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 0.4.1+azure-3
- Increment release to force republishing using golang 1.15.13.
* Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 0.4.1+azure-2
- Increment release to force republishing using golang 1.15.
* Thu Jun 11 2020 Andrew Phelps <anphel@microsoft.com> 0.4.1+azure-1
- Update to version 0.4.1+azure
* Wed May 20 2020 Joe Schmitt <joschmit@microsoft.com> 0.3.1+azure-5
- Remove reliance on existing GOPATH environment variable.
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.3.1+azure-4
- Added %%license line automatically
* Mon May 04 2020 Eric Li <eli@microsoft.com> 0.3.1+azure-3
- Add #Source0: and license verified
* Fri May 01 2020 Emre Girgin <mrgirgin@microsoft.com> 0.3.1+azure-2
- Renaming go to golang
* Fri Apr 03 2020 Mohan Datla <mdatla@microsoft.com> 0.3.1+azure-1
- Initial CBL-Mariner import from Azure.
* Tue Mar 24 2020 Brian Goff <brgoff@microsoft.com>
- Initial version
