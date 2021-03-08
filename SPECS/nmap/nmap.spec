Summary:        Nmap Network Mapper
Name:           nmap
Version:        7.90
Release:        2%{?dist}
License:        Nmap
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://nmap.org/
Source0:        https://nmap.org/dist/%{name}-%{version}.tar.bz2
BuildRequires:  binutils
BuildRequires:  gcc
BuildRequires:  kernel-headers
BuildRequires:  libpcap-devel
BuildRequires:  libssh2-devel
BuildRequires:  lua-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

%description
Nmap ("Network Mapper") is a free and open source utility for network discovery and security auditing.

%package ncat
Summary:        Nmap replacement for ncat
Provides:       nc

%description ncat
Nmap implementation of the ncat tool

%prep
%autosetup -p1

# Remove bundled copies of several libraries. Leave pcre since we dont have a static version.
rm -rf libpcap macosx mswin32 libssh2 libz

%build
%configure
%make_build

%install
%make_install

rm -rf %{buildroot}%{_datadir}/ncat
ln -s ncat %{buildroot}%{_bindir}/nc

%files
%license LICENSE
%exclude %{_mandir}
%{_bindir}/nmap
%{_bindir}/nping
%{_datadir}/nmap

%files ncat
%license LICENSE
%{_bindir}/ncat
%{_bindir}/nc

%changelog
* Thu Feb 11 2021 Thomas Crain <thcrain@microsoft.com> - 7.90-2
- Bump release version alongside upgrade to lua 5.4.2

* Tue Feb 02 2021 Henry Beberman <henry.beberman@microsoft.com> - 7.90-1
- Add nmap spec
- License verified
- Original version for CBL-Mariner
