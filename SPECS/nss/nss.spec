%global unsupported_tools_directory %{_libdir}/nss/unsupported-tools
# Produce .chk files for the final stripped binaries
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %__os_install_post \
    %{buildroot}%{unsupported_tools_directory}/shlibsign -i %{buildroot}%{_libdir}/libsoftokn3.so \
    %{buildroot}%{unsupported_tools_directory}/shlibsign -i %{buildroot}%{_libdir}/libfreeblpriv3.so \
    %{buildroot}%{unsupported_tools_directory}/shlibsign -i %{buildroot}%{_libdir}/libfreebl3.so \
    %{buildroot}%{unsupported_tools_directory}/shlibsign -i %{buildroot}%{_libdir}/libnssdbm3.so \
%{nil}
Summary:        Security client
Name:           nss
Version:        3.44
Release:        5%{?dist}
License:        MPLv2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS
Source0:        https://archive.mozilla.org/pub/security/nss/releases/NSS_3_44_RTM/src/%{name}-%{version}.tar.gz
Patch0:         nss-3.44-standalone-1.patch
Patch1:         CVE-2020-12403.patch
BuildRequires:  nspr-devel
BuildRequires:  sqlite-devel
Provides:       %{name}-tools = %{version}-%{release}
Provides:       %{name}-softokn = %{version}-%{release}
Requires:       nspr
Requires:       nss-libs = %{version}-%{release}

%description
 The Network Security Services (NSS) package is a set of libraries
 designed to support cross-platform development of security-enabled
 client and server applications. Applications built with NSS can
 support SSL v2 and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12,
 S/MIME, X.509 v3 certificates, and other security standards.
 This is useful for implementing SSL and S/MIME or other Internet
 security standards into an application.

%package devel
Summary:        Development Libraries for Network Security Services
Group:          Development/Libraries
Provides:       %{name}-static = %{version}-%{release}
Provides:       %{name}-softokn-devel = %{version}-%{release}
Provides:       %{name}-pkcs11-devel = %{version}-%{release}
Provides:       %{name}-pkcs11-devel-static = %{version}-%{release}
Requires:       nspr-devel
Requires:       nss = %{version}-%{release}

%description devel
Header files for doing development with Network Security Services.

%package libs
Summary:        Libraries for Network Security Services
Group:          System Environment/Libraries
Provides:       %{name}-util = %{version}-%{release}
Requires:       sqlite-libs
Requires:       nspr

%description libs
This package contains minimal set of shared nss libraries.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
export NSS_FORCE_FIPS=1
export NSS_DISABLE_GTESTS=1
cd nss
# -j is not supported by nss
make VERBOSE=1 BUILD_OPT=1 \
    NSPR_INCLUDE_DIR=%{_includedir}/nspr \
    USE_SYSTEM_ZLIB=1 \
    ZLIB_LIBS=-lz \
    USE_64=1 \
    $([ -f %{_includedir}/sqlite3.h ] && echo NSS_USE_SYSTEM_SQLITE=1)

%install
cd nss
cd ../dist
mkdir -p %{buildroot}%{unsupported_tools_directory}
install -vdm 755 %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_includedir}/nss
install -vdm 755 %{buildroot}%{_libdir}
install -v -m755 Linux*/lib/*.so %{buildroot}%{_libdir}
install -v -m644 Linux*/lib/libcrmf.a %{buildroot}%{_libdir}
cp -v -RL {public,private}/nss/* %{buildroot}%{_includedir}/nss
chmod 644 %{buildroot}%{_includedir}/nss/*
install -v -m755 Linux*/bin/{certutil,nss-config,pk12util} %{buildroot}%{_bindir}
install -v -m755 Linux*/bin/shlibsign %{buildroot}%{unsupported_tools_directory}
install -vdm 755 %{buildroot}%{_libdir}/pkgconfig
install -vm 644 Linux*/lib/pkgconfig/nss.pc %{buildroot}%{_libdir}/pkgconfig

%check
pushd nss/tests
export USE_64=1
HOST=localhost DOMSUF=localdomain BUILD_OPT=1 NSS_CYCLES=standard ./all.sh
popd

%post   -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license nss/COPYING
%{_bindir}/*
%{_libdir}/*.chk
%{_libdir}/*.so
%exclude %{_libdir}/libfreeblpriv3.so
%exclude %{_libdir}/libnss3.so
%exclude %{_libdir}/libnssutil3.so
%exclude %{_libdir}/libsoftokn3.so

%files devel
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

%files libs
%{_libdir}/libfreeblpriv3.so
%{_libdir}/libnss3.so
%{_libdir}/libnssutil3.so
%{_libdir}/libsoftokn3.so
%{unsupported_tools_directory}/shlibsign

%changelog
* Mon Jun 21 2021 Thomas Crain <thcrain@microsoft.com> - 3.44-5
- Merge the following releases from 1.0 to dev branch
- anphel@microsoft.com, 3.44-5: Set NSS_DISABLE_GTESTS=1 to speed up build, Run fast tests using NSS_CYCLES=standard
- henry.beberman@microsoft.com, 3.44-6: Patch CVE-2020-12403

* Fri Mar 26 2021 Thomas Crain <thcrain@microsoft.com> - 3.44-4
- Merge the following releases from 1.0 to dev branch
- anphel@microsoft.com, 3.44-3: Fix check tests
- niontive@microsoft.com, 3.44-4: Enable FIPS mode

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.44-3
- Provide nss-tools, -util, -static, -softokn, -softokn-devel
- Provide nss-pkcs11-devel, -pkcs11-devel-static

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.44-2
- Added %%license line automatically

* Tue Mar 17 2020 Andrew Phelps <anphel@microsoft.com> - 3.44-1
- Update version to 3.44. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.39-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 3.39-1
- Upgrade to 3.39.

* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> - 3.31-5
- Add static libcrmf.a library to devel package

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 3.31-4
- Aarch64 support

* Fri Jul 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 3.31-3
- Fix buildrequires.

* Thu Jun 29 2017 Xiaolin Li <xiaolinl@vmware.com> - 3.31-2
- Fix check.

* Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> - 3.31-1
- Upgrade to 3.31.

* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 3.30.1-1
- Update to 3.30.1

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 3.25-4
- Added libs subpackage to reduce tdnf dependent tree

* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> - 3.25-3
- Use sqlite-libs as runtime dependency

* Mon Oct 04 2016 ChangLee <changLee@vmware.com> - 3.25-2
- Modified %check

* Tue Jul 05 2016 Anish Swaminathan <anishs@vmware.com> - 3.25-1
- Upgrade to 3.25

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 3.21-2
- GA - Bump release of all rpms

* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> - 3.21
- Updated to version 3.21

* Tue Aug 04 2015 Kumar Kaushik <kaushikk@vmware.com> - 3.19-2
- Version update. Firefox requirement.

* Fri May 29 2015 Alexey Makhalov <amakhalov@vmware.com> - 3.19-1
- Version update. Firefox requirement.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 3.15.4-1
- Initial build. First version
