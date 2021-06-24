Summary:        Trusted pre-kernel module and tools.
Name:           tboot
Version:        1.9.12
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://sourceforge.net/projects/tboot/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  trousers-devel
Requires:       libtspi
ExclusiveArch:  x86_64

%description
Trusted Boot (tboot) is an open source, pre- kernel/VMM module that uses
Intel(R) Trusted Execution Technology (Intel(R) TXT) to perform a measured
and verified launch of an OS kernel/VMM.

%prep
%setup -q

%build
CFLAGS="%{optflags} -Wno-error=implicit-fallthrough= "
export CFLAGS
make debug=y %{?_smp_mflags}

%install
make debug=y DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%license COPYING
/boot/%{name}.gz
/boot/%{name}-syms
%{_prefix}/sbin
%{_mandir}
%exclude %{_sysconfdir}

%changelog
*   Tue May 11 2021 Andrew Phelps <anphel@microsoft.com> 1.9.12-1
-   Update to version 1.9.12 for binutils 2.36.1 compatibility
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.9.7-7
-   Added %%license line automatically
*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 1.9.7-6
-   Replace BuildArch with ExclusiveArch
*   Tue Mar 24 2020 Henry Beberman <henry.beberman@microsoft.com> 1.9.7-5
-   Add patch to fix compat with GCC9. Source0 URL updated. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.9.7-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Dec 14 2018 Ankit Jain <ankitja@vmware.com> 1.9.7-3
-   Resolved conflict while installing the package
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.9.7-2
-   Adding BuildArch
*   Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 1.9.7-1
-   Update to version 1.9.7.
*   Tue Aug 07 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.9.6-1
-   Update to version 1.9.6 to get it to build with gcc 7.3
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.5-2
-   Ensure non empty debuginfo
*   Thu Mar 2 2017 Alexey Makhalov <amakhalov@vmware.com> 1.9.5-1
-   Initial build. First version
