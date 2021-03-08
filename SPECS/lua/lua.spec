%define LICENSE_PATH LICENSE.PTR
%define majmin %(echo %{version} | cut -d. -f1-2)
Summary:        Lua programming language
Name:           lua
Version:        5.4.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://www.lua.org
Source0:        https://www.lua.org/ftp/%{name}-%{version}.tar.gz
Source1:        %{LICENSE_PATH}
Patch0:         lua-5.4.2-shared_library-1.patch
BuildRequires:  readline-devel
Requires:       readline

%description
Lua is a powerful, light-weight programming language designed for extending
applications. Lua is also frequently used as a general-purpose, stand-alone
language. Lua is free software.

%package devel
Summary:        Libraries and header files for lua
Requires:       %{name} = %{version}

%description devel
Static libraries and header files for the support library for lua

%prep
%autosetup -p1
sed -i '/#define LUA_ROOT/s:%{_prefix}/local/:%{_prefix}/:' src/luaconf.h
sed -i 's/CFLAGS= -O2 /CFLAGS+= -fPIC -O2 -DLUA_COMPAT_MODULE /' src/Makefile
cp %{SOURCE1} ./

%build
make V=%{majmin} R=%{version} VERBOSE=1 %{?_smp_mflags} linux

%install
make %{?_smp_mflags} \
    V=%{majmin} \
    R=%{version} \
    INSTALL_TOP=%{buildroot}%{_prefix} TO_LIB="liblua.so \
    liblua.so.%{majmin} liblua.so.%{version}" \
    INSTALL_DATA="cp -d" \
    INSTALL_MAN=%{buildroot}%{_mandir}/man1 \
    install
install -vdm 755 %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/lua.pc <<- "EOF"
    V=%{majmin}
    R=%{version}

    prefix=%{_prefix}
    INSTALL_BIN=${prefix}/bin
    INSTALL_INC=${prefix}/include
    INSTALL_LIB=${prefix}/lib
    INSTALL_MAN=${prefix}/man/man1
    exec_prefix=${prefix}
    libdir=${exec_prefix}/lib
    includedir=${prefix}/include

    Name: Lua
    Description: An Extensible Extension Language
    Version: ${R}
    Requires:
    Libs: -L${libdir} -llua -lm -ldl
    Cflags: -I${includedir}
EOF
rmdir %{buildroot}%{_libdir}/lua/%{majmin}
rmdir %{buildroot}%{_libdir}/lua

%check
make test

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%license %{LICENSE_PATH}
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/liblua.so.*
%{_mandir}/*/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/lua.pc
%{_libdir}/liblua.so

%changelog
* Thu Feb 11 2021 Thomas Crain <thcrain@microsoft.com> - 5.4.2-1
- Upgrade to 5.4.2 to fix CVE-2020-15945
- Lint spec to Mariner standards
- Remove patches for CVEs filed against older versions
- Update shared lib patch for current version

* Thu Oct 01 2020 Daniel McIlvaney <damcilva@microsoft.com> - 5.3.5-8
- Nopatch CVE-2020-24342
- Apply patch for CVE-2019-6706 from Lua mailing list
- Apply patch for CVE-2020-15888 from Open Embedded

* Mon Sep 28 2020 Daniel McIlvaney <damcilva@microsoft.com> - 5.3.5-7
- Nopatch CVE-2020-15889 since it only affects 5.4.0

* Tue Aug 11 2020 Mateusz Malisz <mamalisz@microsoft.com> - 5.3.5-6
- Append -fPIC and -O2 to CFLAGS to fix build issues.

* Fri Jul 31 2020 Leandro Pereira <leperei@microsoft.com> - 5.3.5-5
- Don't stomp on CFLAGS.

* Thu Jun 06 2020 Joe Schmitt <joschmit@microsoft.com> - 5.3.5-4
- Added %%license macro.

* Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> - 5.3.5-3
- Verified License. Fixed Source0 download URL. Fixed URL.  Fixed Formatting.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 5.3.5-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 5.3.5-1
- Update to version 5.3.5

* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> - 5.3.4-1
- Update package version

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 5.3.2-2
- GA - Bump release of all rpms

* Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> - 5.3.2-1
- Update to version 5.3.2.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 5.2.3-1
- Initial build.	First version
