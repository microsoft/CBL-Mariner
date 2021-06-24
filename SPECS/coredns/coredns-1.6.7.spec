%global debug_package %{nil}

Summary:        Fast and flexible DNS server
Name:           coredns
Version:        1.6.7
Release:        2%{?dist}
License:        Apache License 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/coredns/coredns
#Source0:       https://github.com/coredns/coredns/archive/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/coredns/coredns/archive/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
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
Patch0:         makefile-buildoption-commitnb.patch

BuildRequires:  golang >= 1.12

%description
CoreDNS is a fast and flexible DNS server.

%prep
%autosetup -p1

%build
# create vendor folder from the vendor tarball and set vendor mode
tar -xf %{SOURCE1} --no-same-owner
export BUILDOPTS="-mod=vendor -v"
# set commit number that correspond to the github tag for that version
export GITCOMMIT="da7f65b"
make

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} %{name}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}

%changelog
* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.6.7-2
- Increment release to force republishing using golang 1.15.11.
* Wed Jan 20 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.6.7-1
- Original version for CBL-Mariner.
