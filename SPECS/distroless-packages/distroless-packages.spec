Summary:        Metapackage with core sets of packages for distroless containers
Name:           distroless-packages
Version:        0.1
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://aka.ms/cbl-mariner

%description
Metapackage holding sets of core packages for different applications.

%package minimal
Summary:        The smallest useful package list.
Requires:       ca-certificates-prebuilt
Requires:       filesystem
Requires:       mariner-release

%package base
Summary:        Metapackage defining the basic set of packages (no kernel) used to create a "distroless" container.
Requires:       ca-certificates-prebuilt
Requires:       filesystem
Requires:       glibc-iconv
Requires:       iana-etc
Requires:       mariner-release
Requires:       openssl
Requires:       openssl-libs
Requires:       tzdata

%description base
%{summary}

%package debug
Summary:        Debug packages for distroless
Requires:       %{name}-base = %{version}-%{release}
Requires:       busybox

%description debug
%{summary}

%prep

%build

%files minimal

%files base

%files debug

%changelog
* Thu Oct 15 2020 Mateusz Malisz <mamalisz@microsoft.com> - 0.1-2
- Extend the set of requirements for the base image
- Add debug package with busybox

* Tue Sep 01 2020 Jon Slobodzian <joslobo@microsoft.com> - 0.1-1
- Initial Mariner Version
