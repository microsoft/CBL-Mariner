Summary:        An URL retrieval utility and library
Name:           curl
Version:        7.76.0
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/NetworkingLibraries
URL:            https://curl.haxx.se
Source0:        https://curl.haxx.se/download/%{name}-%{version}.tar.gz
Patch0:         CVE-2021-22898.patch
Patch1:         CVE-2021-22901.patch
BuildRequires:  krb5-devel
BuildRequires:  libssh2-devel
BuildRequires:  openssl-devel
Requires:       curl-libs = %{version}-%{release}
Requires:       krb5
Requires:       libssh2
Requires:       openssl
%if %{with_check}
BuildRequires:  python3
BuildRequires:  shadow-utils
BuildRequires:  sudo
%endif

%description
The cURL package contains an utility and a library used for
transferring files with URL syntax to any of the following
protocols: FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET,
DICT, LDAP, LDAPS and FILE. Its ability to both download and
upload files can be incorporated into other programs to support
functions like streaming media.

%package devel
Summary:        Libraries and header files for curl
Requires:       %{name} = %{version}-%{release}
Provides:       libcurl-devel = %{version}-%{release}

%description devel
Static libraries and header files for the support library for curl

%package libs
Summary:        Libraries for curl
Group:          System Environment/Libraries
Provides:   libcurl = %{version}-%{release}

%description libs
This package contains minimal set of shared curl libraries.

%prep
%autosetup -p1

%build
%configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --disable-static \
    --enable-threaded-resolver \
    --with-ssl \
    --with-gssapi \
    --with-libssh2 \
    --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.trust.crt \
    --with-ca-path=%{_sysconfdir}/ssl/certs
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -v -d -m755 %{buildroot}/%{_docdir}/%{name}-%{version}
find %{buildroot} -type f -name "*.la" -delete -print
%{_fixperms} %{buildroot}/*

%check
chmod g+w . -R
useradd test -G root -m

sudo -u test make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*


%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man3/*
%{_datarootdir}/aclocal/libcurl.m4
%{_docdir}/%{name}-%{version}

%files libs
%{_libdir}/libcurl.so.*

%changelog
* Mon Jun 21 2021 Thomas Crain <thcrain@microsoft.com> - 7.76.0-3
- Merge the following releases from 1.0 to the dev spec:
- joslobo@microsoft.com, 7.76.0-2: Patch 7.76.0 to fix CVE-2021-22898 and CVE-2021-22901.

* Fri Apr 02 2021 Thomas Crain <thcrain@microsoft.com> - 7.76.0-2
- Merge the following releases from dev to 1.0 spec
- v-ruyche@microsoft.com, 7.68.0-2: Add explicit provides for libcurl and libcurl-devel

* Wed Mar 31 2021 Nicolas Ontiveros <niontive@microsoft.com> - 7.76.0-1
- Upgrade to version 7.76.0 to fix CVE-2021-22876 and CVE-2021-22890.

* Tue Dec 22 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.74.0-1
- Updating to 7.74.0 to fix CVE-2020-8169 and incorporate fixes for other CVEs as well.
- Updating source URL to an HTTPS address.
- Enabling more tests to run by running them as non-root and extending 'BuildRequires'.
- License verified.

* Fri Dec 18 2020 Ruying Chen <v-ruyche@microsoft.com> - 7.68.0-5
- Patch CVE-2020-8231

* Tue Dec 15 2020 Ruying Chen <v-ruyche@microsoft.com> - 7.68.0-4
- Patch CVE-2020-8177

* Wed Dec 09 2020 Nicolas Ontiveros <niontive@microsoft.com> - 7.68.0-3
- Patch CVE-2020-8284
- Patch CVE-2020-8285
- Patch CVE-2020-8286

* Wed Oct 07 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.68.0-2
- Updating certificate bundle path to include full set of trust information.

* Tue Aug 11 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.68.0-1
- Upgrading to 7.68.0 to enable verification against a partial cert chain.

* Thu May 14 2020 Nicolas Ontiveros <niontive@microsoft.com> - 7.66.0-1
- Upgrade to version 7.66.0, which fixes CVE-2018-16890 and CVE-2019-3822/3833.

* Sat May 09 00:21:39 PST 2020 Nick Samson <nisamson@microsoft.com> - 7.61.1-6
- Added %%license line automatically

* Wed May 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.61.1-5
- Removing *Requires for "ca-certificates".
- Adding a certs directory through "--with-ca-path" at compile time.

* Mon Apr 20 2020 Nicolas Ontiveros <niontive@microsoft.com> - 7.61.1-4
- Fix CVE-2019-5481.
- Fix CVE-2019-5482.
- Remove sha1 macro.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 7.61.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jan 08 2019 Dweep Advani <dadvani@vmware.com> - 7.61.1-2
- Fix of CVE-2018-16839, CVE-2018-16840 and CVE-2018-16842

* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> - 7.61.1-1
- Upgraded to version 7.61.1

* Wed Apr 04 2018 Dheeraj Shetty <dheerajs@vmware.com> - 7.59.0-1
- Update to version 7.59.0

* Thu Feb 08 2018 Xiaolin Li <xiaolinl@vmware.com> - 7.58.0-1
- Fix CVE-2017-8817.

* Thu Dec 21 2017 Xiaolin Li <xiaolinl@vmware.com> - 7.56.1-2
- Fix CVE-2017-8818.

* Wed Dec 13 2017 Xiaolin Li <xiaolinl@vmware.com> - 7.56.1-1
- Update to version 7.56.1

* Mon Nov 27 2017 Xiaolin Li <xiaolinl@vmware.com> - 7.54.1-4
- Fix CVE-2017-1000257

* Mon Nov 06 2017 Xiaolin Li <xiaolinl@vmware.com> - 7.54.1-3
- Fix CVE-2017-1000254

* Thu Nov 02 2017 Xiaolin Li <xiaolinl@vmware.com> - 7.54.1-2
- Fix CVE-2017-1000099, CVE-2017-1000100, CVE-2017-1000101

* Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> - 7.54.1-1
- Update to 7.54.1

* Mon Apr 24 2017 Bo Gan <ganb@vmware.com> - 7.54.0-1
- Update to 7.54.0

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 7.51.0-5
- Added -libs subpackage

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> - 7.51.0-4
- Added -devel subpackage.

* Wed Nov 30 2016 Xiaolin Li <xiaolinl@vmware.com> - 7.51.0-3
- Enable sftp support.

* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> - 7.51.0-2
- Required krb5-devel.

* Wed Nov 02 2016 Anish Swaminathan <anishs@vmware.com> - 7.51.0-1
- Upgrade curl to 7.51.0

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> - 7.50.3-2
- Modified %check

* Thu Sep 15 2016 Xiaolin Li <xiaolinl@vmware.com> - 7.50.3-1
- Update curl to version 7.50.3.

* Tue Aug 23 2016 Xiaolin Li <xiaolinl@vmware.com> - 7.47.1-3
- Enable gssapi in curl.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 7.47.1-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> - 7.47.1-1
- Updated to version 7.47.1

* Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> - 7.46.0-1
- Updated to version 7.46.0

* Thu Aug 13 2015 Divya Thaluru <dthaluru@vmware.com> - 7.43.0-1
- Update to version 7.43.0.

* Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 7.41.0-1
- Update to version 7.41.0.
