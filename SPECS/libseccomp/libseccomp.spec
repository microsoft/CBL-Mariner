Summary:       Enhanced seccomp library
Name:          libseccomp
Version:       2.4.1
Release:       2%{?dist}
License:       LGPLv2
Group:         System Environment/Libraries
Url:           https://github.com/seccomp/libseccomp/wiki
Source0:       https://github.com/seccomp/libseccomp/releases/download/v%{version}/%{name}-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
%if %{with_check}
BuildRequires: which
%endif

%description
The libseccomp library provides an easy to use, platform independent, interface
to the Linux Kernel syscall filtering mechanism: seccomp. The libseccomp API
is designed to abstract away the underlying BPF based syscall filter language
and present a more conventional function-call based filtering interface that
should be familiar to, and easily adopted by application developers.

%package devel
Summary:  Development files used to build applications with libseccomp support
Group:    Development/Libraries
Provides: pkgconfig(libseccomp)

%description devel
The libseccomp-devel package contains the libraries and header files
needed for developing secure applications.

%prep
%setup -q

%build
%configure
make V=1 %{?_smp_mflags}

%install
rm -rf "%{buildroot}"
make V=1 DESTDIR="%{buildroot}" install

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc LICENSE
%doc CREDITS
%doc README.md
%{_libdir}/libseccomp.so.*

%files devel
%{_includedir}/seccomp.h
%{_libdir}/libseccomp.so
%{_libdir}/libseccomp.a
%{_libdir}/libseccomp.la
%{_libdir}/pkgconfig/libseccomp.pc
%{_bindir}/scmp_sys_resolver
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 2.4.1-1
-   Update to 2.4.1. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.3.3-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*  Wed Jan 9 2019 Michelle Wang <michellew@vmware.com> 2.3.3-2
-  Fix make check for libseccomp.
*  Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 2.3.3-1
-  Updated to version 2.3.3.
*  Tue Apr 11 2017 Harish Udaiya KUmar <hudaiyakumar@vmware.com> 2.3.2-1
-  Updated to version 2.3.2.
*  Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.3-2
-  GA - Bump release of all rpms.
*  Sat Jan 16 2016 Fabio Rapposelli <fabio@vmware.com> - 2.2.3-1
-  First release of the package.
