Name:           fuse-zip
Version:        0.7.2
Release:        2%{?dist}
Summary:        Filesystem to navigate, extract, create and modify ZIP archives
Vendor:         Microsoft Corporation
Distribution:   Mariner
License:        GPLv3+
URL:            https://bitbucket.org/agalanin/fuse-zip/
Source0:        https://bitbucket.org/agalanin/fuse-zip/downloads/%{name}-%{version}.tar.gz

BuildRequires:  libstdc++
BuildRequires:  libstdc++-devel
BuildRequires:  libzip-devel
BuildRequires:  fuse-devel
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  make
Requires:       fuse

%description
fuse-zip is a FUSE file system to navigate, extract, create and modify
ZIP archives based in libzip implemented in C++.

With fuse-zip you really can work with ZIP archives as real directories.
Unlike KIO or Gnome VFS, it can be used in any application without
modifications.

Unlike other FUSE filesystems, only fuse-zip provides write support
to ZIP archives. Also, fuse-zip is faster that all known implementations
on large archives with many files.

%prep
%autosetup -p1

sed -i '/CXXFLAGS=.*/d' lib/Makefile
sed -i '/CXXFLAGS=.*/d' Makefile
sed -i "s|prefix=/usr/local|prefix=%{_prefix}|" Makefile

%build
%set_build_flags
%make_build

%install
%make_install

%files
%doc README.md changelog
%license LICENSE
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_docdir}/fuse-zip

%changelog
* Mon May 17 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.7.2-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Mon Feb 22 2021 Vasiliy Glazov <vascom2@gmail.com> - 0.7.2-1
- Update to 0.7.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 21 2020 Vasiliy Glazov <vascom2@gmail.com> - 0.7.1-1
- Update to 0.7.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 25 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 0.7.0-1
- Update to 0.7.0

* Tue Aug 06 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 0.6.2-1
- Update to 0.6.2

* Mon Jul 29 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 0.6.1-1
- Update to 0.6.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 20 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 0.6.0-1
- Update to 0.6.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 25 2018 Vasiliy N. Glazov <vascom2@gmail.com> - 0.5.0-1
- Update to 0.5.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Vasiliy N. Glazov <vascom2@gmail.com> - 0.4.5-1
- Update to 0.4.5

* Thu Dec 07 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 0.4.4-1
- Update to 0.4.4

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 28 2017 Remi Collet <remi@fedoraproject.org> - 0.4.2-3
- rebuild for new libzip

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Mar 15 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 0.4.2-1
- Update to 0.4.2

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 29 2015 Vasiliy N. Glazov <vascom2@gmail.com> - 0.4.1-1
- Update to 0.4.1
- Update makefile patch

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 06 2015 Remi Collet <remi@fedoraproject.org> - 0.4.0-4
- rebuild for new libzip
- honour fedora build flags and fix FTBFS

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Vasiliy N. Glazov <vascom2@gmail.com> - 0.4.0-1
- Update to 0.4.0
- Drop fuse-zip-libzip010.patch

* Wed Aug 21 2013 Remi Collet <rcollet@redhat.com> - 0.2.12-9
- rebuild for new libzip

* Thu Aug 08 2013 Vasiliy N. Glazov <vascom2@gmail.com> - 0.2.12-8
- Clean spec
- Correct build flags
- Added russian description

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Feb 04 2012 Remi Collet <remi@fedoraproject.org> - 0.2.12-4
- rebuild for new libzip
- add patch for new callback prototype (fix #787370)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May 04 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 0.2.12-1
- Updated to 0.2.12

* Sat Jan 30 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 0.2.11-1
- Updated to 0.2.11

* Fri Dec 04 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 0.2.8-1
- Updated to 0.2.8

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> - 0.2.7-4
- Rebuilt with new fuse

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.2.7-1
- Upgraded to 0.2.7

* Mon Dec 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.2.6-6
- fixed man page spelling mistake

* Sun Dec 07 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.2.6-5
- fixed debug info package

* Sat Nov 08 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.2.6-4
- removed INSTALL file from package - not useful

* Fri Nov 07 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.2.6-3
- fix flag, save timestamp and clean %%install

* Tue Nov 04 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.2.6-2
- Makefile patch by Debarshi Ray <rishi@fedoraproject.org>, fix debuginfo

* Tue Nov 04 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.2.6-1
- initial package

