Summary:        A library that implements the client-side of the ACVP protocol
Name:           libacvp
Version:        1.3.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://github.com/cisco/libacvp
# Source0:      https://github.com/cisco/%%{name}/archive/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:         app_fips_lcl.patch
Patch1:         dsa.patch
Patch2:         aes.patch
Patch3:         ecdsa.patch
Patch4:         kas.patch
Patch5:         rsa.patch
Patch6:         app_main.patch
Patch7:         app_fips_init_lcl.patch
Patch8:         drbg.patch
Patch9:         acvp_dsa.patch
Patch10:        app_aes.patch
Patch11:        acvp.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  make

%description
A library that implements the client-side of the ACVP protocol.

%package app
Summary:        Libacvp application for OpenSSL
Group:          Applications/System
BuildRequires:  openssl-devel
Requires:       openssl-libs

%description app
This app provides the glue between the OpenSSL module under test
and the library itself.

%prep
%autosetup -p1

%build
./configure \
    --prefix=%{_prefix} \
    --enable-offline \
    CFLAGS="-pthread -DACVP_NO_RUNTIME -DOPENSSL_KWP -O0 -g" \
    LIBS="-ldl"
make clean
make CC=gcc

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" -delete -print

%clean
rm -rf %{buildroot}/*


%files
%license LICENSE
%{_datadir}/README.md
%{_libdir}/libacvp.a
%{_includedir}/acvp/*

%files app
%{_bindir}/acvp_app

%changelog
* Wed Mar 17 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.3.0-1
- Update to version 1.3.0
- Patch aes_app, dsa_app, ecdsa_app, kas_app, drbg_app and rsa_app.

* Mon Feb 08 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.2.0-1
- Original version for CBL-Mariner. License verified.