%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Package manager
Name:           rpm
Version:        4.14.2
Release:        11%{?dist}
License:        GPLv2+ and LGPLv2+ and BSD
URL:            https://rpm.org
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/rpm-software-management/rpm/archive/%{name}-%{version}-release.tar.gz
Source1:        brp-strip-debug-symbols
Source2:        brp-strip-unneeded
Patch0:         find-debuginfo-do-not-generate-dir-entries.patch
Requires:       bash
Requires:       libdb
Requires:       rpm-libs = %{version}-%{release}
Requires:       libarchive
Requires:       lua
BuildRequires:  libarchive-devel
BuildRequires:  libdb-devel
BuildRequires:  popt-devel
BuildRequires:  nss-devel
BuildRequires:  elfutils-devel
BuildRequires:  libcap-devel
BuildRequires:  xz-devel
BuildRequires:  zstd-devel
BuildRequires:  file-devel
BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  lua-devel

%description
RPM package manager

%package devel
Summary:        Libraries and header files for rpm
Provides:       pkgconfig(rpm)
Requires:       %{name} = %{version}-%{release}
%description devel
Static libraries and header files for the support library for rpm

%package libs
Summary:        Libraries for rpm
Requires:       nss-libs
Requires:       popt
Requires:       libgcc
Requires:       libcap
Requires:       zlib
Requires:       bzip2-libs
Requires:       elfutils-libelf
Requires:       xz-libs
Requires:       zstd-libs
Requires:       mariner-rpm-macros
%description    libs
Shared libraries librpm and librpmio

%package build-libs
Summary: Librpmbuild.so.* libraries needed to build rpms.
%description build-libs
%{summary}

%package build
Requires:       %{name}-build-libs
Requires:       %{name}-devel = %{version}-%{release}
Requires:       elfutils-libelf
Requires:       elfutils-devel
Requires:       unzip
Requires:       tar
Requires:       xz
Requires:       bzip2
Requires:       gzip
Requires:       cpio
Summary: Binaries, scripts and libraries needed to build rpms.
%description build
%{summary}

%package lang
Summary:        Additional language files for rpm
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
%description lang
These are the additional language files of rpm.

%package -n     python-rpm
Summary:        Python 2 bindings for rpm.
Group:          Development/Libraries
Requires:       python2
%description -n python-rpm

%package -n     python3-rpm
Summary:        Python 3 bindings for rpm.
Group:          Development/Libraries
Requires:       %{name}-build-libs
Requires:       python3

%description -n python3-rpm
Python3 rpm.

%prep
%setup -n rpm-%{name}-%{version}-release
%patch0 -p1

%build
sed -i '/define _GNU_SOURCE/a #include "../config.h"' tools/sepdebugcrcfix.c
# pass -L opts to gcc as well to prioritize it over standard libs
sed -i 's/-Wl,-L//g' python/setup.py.in
sed -i '/library_dirs/d' python/setup.py.in
sed -i 's/extra_link_args/library_dirs/g' python/setup.py.in

./autogen.sh --noconfigure
%configure \
    CPPFLAGS='-I/usr/include/nspr -I/usr/include/nss -DLUA_COMPAT_APIINTCASTS' \
        --program-prefix= \
        --disable-dependency-tracking \
        --disable-static \
        --with-vendor=mariner \
        --enable-python \
        --with-cap \
        --with-lua \
        --disable-silent-rules \
        --with-external-db
make %{?_smp_mflags}

pushd python
python2 setup.py build
python3 setup.py build
popd

%check
make check

%install
make DESTDIR=%{buildroot} install

find %{buildroot} -name '*.la' -delete
find %{buildroot} -name 'perl*' -delete

%find_lang %{name}
# System macros and prefix
install -dm 755 %{buildroot}%{_sysconfdir}/rpm
install -vm755 %{SOURCE1} %{buildroot}%{_libdir}/rpm/
install -vm755 %{SOURCE2} %{buildroot}%{_libdir}/rpm/

pushd python
python2 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
popd

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post   build-libs -p /sbin/ldconfig
%postun build-libs -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/rpm
%{_bindir}/gendiff
%{_bindir}/rpm2archive
%{_bindir}/rpm2cpio
%{_bindir}/rpmdb
%{_bindir}/rpmgraph
%{_bindir}/rpmkeys
%{_bindir}/rpmquery
%{_bindir}/rpmverify

%{_libdir}/rpm/rpmpopt-*
%{_libdir}/rpm/rpmdb_*
%{_libdir}/rpm/rpm.daily
%{_libdir}/rpm/rpm.log
%{_libdir}/rpm/rpm.supp
%{_libdir}/rpm/rpm2cpio.sh
%{_libdir}/rpm/tgpg
%{_libdir}/rpm/platform
%{_libdir}/rpm-plugins/*
%{_libdir}/rpm/python-macro-helper
%{_libdir}/rpm/pythondistdeps.py
%{_mandir}/man8/rpm.8.gz
%{_mandir}/man8/rpm2cpio.8.gz
%{_mandir}/man8/rpmdb.8.gz
%{_mandir}/man8/rpmgraph.8.gz
%{_mandir}/man8/rpmkeys.8.gz
%{_mandir}/man8/rpm-misc.8.gz
%{_mandir}/man8/rpm-plugin-systemd-inhibit.8.gz
%exclude %{_mandir}/fr/man8/*.gz
%exclude %{_mandir}/ja/man8/*.gz
%exclude %{_mandir}/ko/man8/*.gz
%exclude %{_mandir}/pl/man1/*.gz
%exclude %{_mandir}/pl/man8/*.gz
%exclude %{_mandir}/ru/man8/*.gz
%exclude %{_mandir}/sk/man8/*.gz

%files libs
%defattr(-,root,root)
%{_libdir}/librpmio.so.*
%{_libdir}/librpm.so.*
%{_libdir}/rpm/macros
%{_libdir}/rpm/rpmrc
%{_libdir}/rpm/platform/*

%files build-libs
%{_libdir}/librpmbuild.so*

%files build
%{_bindir}/rpmbuild
%{_bindir}/rpmsign
%{_bindir}/rpmspec
%{_libdir}/rpm/macros.*
%{_libdir}/rpm/find-debuginfo.sh
%{_libdir}/rpm/find-lang.sh
%{_libdir}/rpm/find-provides
%{_libdir}/rpm/find-requires
%{_libdir}/rpm/brp-*
%{_libdir}/rpm/mono-find-provides
%{_libdir}/rpm/mono-find-requires
%{_libdir}/rpm/ocaml-find-provides.sh
%{_libdir}/rpm/ocaml-find-requires.sh
%{_libdir}/rpm/fileattrs/*
%{_libdir}/rpm/script.req
%{_libdir}/rpm/check-buildroot
%{_libdir}/rpm/check-files
%{_libdir}/rpm/check-prereqs
%{_libdir}/rpm/check-rpaths
%{_libdir}/rpm/check-rpaths-worker
%{_libdir}/rpm/config.guess
%{_libdir}/rpm/config.sub
%{_libdir}/rpm/debugedit
%{_libdir}/rpm/elfdeps
%{_libdir}/rpm/libtooldeps.sh
%{_libdir}/rpm/mkinstalldirs
%{_libdir}/rpm/pkgconfigdeps.sh
%{_libdir}/rpm/*.prov
%{_libdir}/rpm/sepdebugcrcfix

%{_libdir}/rpm/pythondeps.sh
%{_libdir}/rpm/rpmdeps

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmspec.8*
%{_mandir}/man8/rpmsign.8.gz

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/rpm.pc
%{_libdir}/librpmio.so
%{_libdir}/librpm.so
%{_libdir}/librpmsign.so
%{_libdir}/librpmsign.so.*

%files lang -f %{name}.lang
%defattr(-,root,root)

%files -n python-rpm
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-rpm
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Thu Feb 11 2021 Thomas Crain <thcrain@microsoft.com> - 4.14.2-11
- Bump release version alongside upgrade to lua 5.4.2

* Thu Jun 11 2020 Henry Beberman <henry.beberman@microsoft.com> - 4.14.2-10
- Add a vendor definition so rpm will search /usr/lib/rpm/<vendor> for macros.

* Tue Jun 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.14.2-9
- Removed 'rpm-build' dependency on 'perl'.
- Defined an 'rpm-build-libs' subpackage to prevent 'python3-rpm'
- from pulling in 'perl'.
- Made 'python3-rpm' dependency on 'rpm-build-libs' explicit.

* Thu May 28 2020 Ruying Chen <v-ruyche@microsoft.com> - 4.14.2-8
- Move macros to mariner-rpm-macros

* Wed May 20 2020 Henry Beberman <henry.beberman@microsoft.com> - 4.14.2-7
- Add BuildRequires and Requires for zstd support.

* Sat May 09 00:20:45 PST 2020 Nick Samson <nisamson@microsoft.com> - 4.14.2-6
- Added %%license line automatically

* Wed May 06 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.14.2-5
- Enable built-in lua support.
- Update URL.
- License verified.

* Wed Apr 29 2020 Mateusz Malisz <mamalisz@microsoft.com> - 4.14.2-4
- Add packaging tools as runtime requirements for rpm-build

* Fri Apr 03 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.14.2-3
- Remove rpm-build from requires.

* Wed Sep 11 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.14.2-2
- Fix Dependency and include build in base package.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.14.2-1
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Oct 03 2018 Alexey Makhalov <amakhalov@vmware.com> - 4.14.2-4
- Clean up the file in accordance to spec file checker

* Mon Oct 01 2018 Alexey Makhalov <amakhalov@vmware.com> - 4.14.2-3
- Fix python libs dependencies to use current libs version (regression)

* Fri Sep 28 2018 Alexey Makhalov <amakhalov@vmware.com> - 4.14.2-2
- macros: set _build_id_links to alldebug

* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> - 4.14.2-1
- Update to version 4.14.2

* Thu Dec 21 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.13.0.1-7
- Fix CVE-2017-7501

* Wed Oct 04 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.13.0.1-6
- make python{,3}-rpm depend on current version of librpm

* Wed Jun 28 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.13.0.1-5
- Add file-devel to BuildRequires

* Mon Jun 26 2017 Chang Lee <changlee@vmware.com> - 4.13.0.1-4
- Updated %check

* Mon Jun 05 2017 Bo Gan <ganb@vmware.com> - 4.13.0.1-3
- Fix Dependency

* Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.13.0.1-2
- Remove python2 from requires of rpm-devel subpackages.

* Wed May 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.13.0.1-1
- Update to 4.13.0.1

* Fri Apr 21 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.13.0-1
- Update to 4.13.0

* Wed Apr 19 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-22
- Do not allow -debuginfo to own directories to avoid conflicts with
    filesystem package and between each other. Patch applied

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-21
- rpm-libs requires nss-libs, xz-libs and bzip2-libs.

* Tue Mar 21 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.11.2-20
- Added python3 packages and moved python2 site packages from devel to python-rpm.

* Tue Jan 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.11.2-19
- added buildrequires for xz-devel for PayloadIsLzma cap

* Thu Dec 15 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.11.2-18
- Moved some files from rpm to rpm-build.

* Tue Dec 06 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.11.2-17
- Added -lang subpackage.

* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-16
- Move rpmrc and macros into -libs subpackage
- Move zlib and elfutils-libelf dependency from rpm to rpm-libs
- Add bzip2 dependency to rpm-libs

* Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-15
- Added -libs subpackage

* Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-14
- Disable lua support

* Tue Oct 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.11.2-13
- Apply patch for CVE-2014-8118

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> - 4.11.2-12
- Modified %check

* Fri Aug 26 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-11
- find-debuginfo...patch: exclude non existing .build-id from packaging
- Move all files from rpm-system-configuring-scripts tarball to here

* Wed May 25 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.11.2-10
- Exclude .build-id/.1 and .build-id/.1.debug from debuginfo pkg

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.11.2-9
- GA - Bump release of all rpms

* Thu May 05 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.11.2-8
- Update rpm version in lock-step with lua update to 5.3.2

* Fri Apr 08 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> - 4.11.2-7
- Build rpm with capabilities.

* Wed Aug 05 2015 Sharath George <sharathg@vmware.com> - 4.11.2-6
- Moving build utils to a different package.

* Sat Jun 27 2015 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-5
- Update rpm-system-configuring-scripts. Use tar --no-same-owner for rpmbuild.

* Thu Jun 18 2015 Anish Swaminathan <anishs@vmware.com> - 4.11.2-4
- Add pkgconfig Provides directive

* Thu Jun 18 2015 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-3
- Do no strip debug info from .debug files

* Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> - 4.11.2-2
- Removing perl-module-scandeps package from run time required packages

* Tue Jan 13 2015 Divya Thaluru <dthaluru@vmware.com> - 4.11.2-1
- Initial build. First version
