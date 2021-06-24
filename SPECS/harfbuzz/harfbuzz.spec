Summary:        opentype text shaping engine
Name:           harfbuzz
Version:        2.6.4
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://harfbuzz.github.io/
Source0:        https://www.freedesktop.org/software/harfbuzz/release/%{name}-%{version}.tar.xz
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(icu-uc)
Requires:       glib
%if %{with_check}
BuildRequires:  python3-devel
%endif

%description
HarfBuzz is an implementation of the OpenType Layout engine.

%package	    devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig(glib-2.0)
Provides:       %{name}-icu = %{version}-%{release}

%description	devel
It contains the libraries and header files to create applications

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
# Remove all instances of "/usr/bin/env python" shabangs from test code
find . -type f -name "*.py" -exec sed -i'' -e '1 s|^#!\s*/usr/bin/env\s\+python\d\?|#! %{python3}|' {} +
%make_build -k check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so*
%{_bindir}/*

%files devel
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/harfbuzz/harfbuzz-config.cmake

%changelog
* Tue Jun 22 2021 Thomas Crain <thcrain@microsoft.com> - 2.6.4-3
- Fix pkgconfig(freetype) dependency

* Mon Jun 21 2021 Thomas Crain <thcrain@microsoft.com> - 2.6.4-2
- Build harfbuzz with icu libraries, fontconfig libraries
- Use pkgconfig(*)-style dependencies
- Provide harbuzz-icu from devel subpackage
- Use macros throughout the spec
- Fix package tests by fixing Python shabangs
- Update URL

* Fri Apr 16 2021 Henry Li <lihl@microsoft.com> - 2.6.4-1
- Upgrade to version 2.6.4
- Remove freetype from build requirement

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.9.0-4
- Added %%license line automatically

* Mon Apr 20 2020 Nicolas Ontiveros <niontive@microsoft.com> - 1.9.0-3
- Rename "freetype2" to "freetype". 
- Remove sha1 macro.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.9.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> - 1.9.0-1
- Update to version 1.9.0

* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> - 1.4.5-2
- Add glib requirement

* Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.4.5-1
- Initial version
