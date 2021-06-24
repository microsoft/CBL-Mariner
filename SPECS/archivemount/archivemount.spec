Name:          archivemount
Version:       0.9.1
Release:       4%{?dist}
Summary:       FUSE based filesystem for mounting compressed archives
Vendor:        Microsoft Corporation
Distribution:  Mariner
License:       LGPLv2+
URL:           https://www.cybernoia.de/software/archivemount.html
Source0:       https://www.cybernoia.de/software/archivemount/%{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: fuse-devel
BuildRequires: libarchive-devel
BuildRequires: automake
BuildRequires: make
Requires:      fuse

%description
Archivemount is a piece of glue code between libarchive and FUSE. It can be
used to mount a (possibly compressed) archive (as in .tar.gz or .tar.bz2)
and use it like an ordinary filesystem.

%prep
%autosetup -p1

%build
%configure --enable-debug
%make_build

%install
rm -rf $RPM_BUILD_ROOT
rm -f archivemount.1
%make_install

%files
%doc CHANGELOG README
%license COPYING
%{_mandir}/*/*
%{_bindir}/archivemount

%changelog
* Mon May 17 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.9.1-4
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Niels de Vos <devos@fedoraproject.org> - 0.9.1-1
- Update to version 0.9.1

* Mon Apr 20 2020 Niels de Vos <devos@fedoraproject.org> - 0.9.0-1
- Update to version 0.9.0 (#1825602)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Vasiliy N. Glazov <vascom2@gmail.com> - 0.8.12-2
- Clean spec to match packaging guidelines

* Sun Apr 1 2018 Niels de Vos <devos@fedoraproject.org> - 0.8.12-1
- Update to version 0.8.12 (#1560985)

* Tue Mar 27 2018 Niels de Vos <devos@fedoraproject.org> - 0.8.11-1
- Update to version 0.8.11 (#1560985)

* Fri Mar 16 2018 Niels de Vos <devos@fedoraproject.org> - 0.8.10-1
- Update to version 0.8.10 (#1557308)

* Tue Mar 6 2018 Niels de Vos <devos@fedoraproject.org> - 0.8.9-1
- Update to version 0.8.9 (#1547963)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 24 2015 Niels de Vos <devos@fedoraproject.org> - 0.8.7-1
- Update to version 0.8.7 (#1284705)

* Mon Nov 23 2015 Niels de Vos <devos@fedoraproject.org> - 0.8.6-1
- Update to version 0.8.6 (#1197053)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 24 2013 Niels de Vos <devos@fedoraproject.org> - 0.8.3-1
- Update to version 0.8.3 (#1022856)
- Drop upstreamed patches

* Wed Oct 23 2013 Niels de Vos <devos@fedoraproject.org> - 0.8.2-1
- Update to version 0.8.2 (#1021347)

* Sun Oct 13 2013 Niels de Vos <devos@fedoraproject.org> - 0.8.1-2
- Do not call fuse_main() to prevent a confusing error message (#1018587)

* Mon Aug 19 2013 Niels de Vos <devos@fedoraproject.org> - 0.8.1-1
- Update to version 0.8.1 (#997779)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Tomas Bzatek <tbzatek@redhat.com> - 0.6.1-10
- Rebuilt for new libarchive

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 26 2012 Tomas Bzatek <tbzatek@redhat.com> - 0.6.1-8
- Rebuilt for new libarchive

* Sat Jan 07 2012 Niels de Vos <devos@fedoraproject.org> - 0.6.1-7
- Rebuild for new gcc-4.7

* Tue Nov 15 2011 Niels de Vos <devos@fedoraproject.org> - 0.6.1-6
- Rebuild for new libarchive

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Niels de Vos <ndevos@redhat.com> 0.6.1-4
- fix the -debuginfo package as suggested by Tomas Mraz (BZ#598688 comment #12)

* Fri Jan 14 2011 Niels de Vos <ndevos@redhat.com> 0.6.1-3
- fix the -debuginfo package (BZ#598688 comment #10)

* Mon Jan 10 2011 Niels de Vos <niels@nixpanic.net> 0.6.1-2
- force running in single threaded mode (much more stable)
- fix some points from BZ #598688 comment #7

* Thu Jun 24 2010 Niels de Vos <ndevos@redhat.com> 0.6.1-1
- upstream fixed licensing in the source to LGPL (v2 or newer)
- new source does not contain autom4te.cache anymore, no need to 'rm -rf' it

* Tue Jun 15 2010 Niels de Vos <ndevos@redhat.com> 0.6.0-2
- fix license to GNU Library General Public v2 or newer
- remove packaged autoconf/automake cache files

* Tue Jun 01 2010 Niels de Vos <ndevos@redhat.com> 0.6.0-1
- Initial package
