Summary:        Container Network Interface (CNI) plugins
Name:           cni
Version:        0.7.5
Release:        6%{?dist}
License:        ASL 2.0
# cni moved to https://github.com/containernetworking/cni/issues/667#issuecomment-491693752
URL:            https://github.com/containernetworking/plugins
#Source0:       https://github.com/containernetworking/plugins/archive/v0.7.5.tar.gz
Source0:        %{name}-v%{version}.tar.gz
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  golang >= 1.5
%define _default_cni_plugins_dir /opt/cni/bin

%description
The CNI (Container Network Interface) project consists of a specification and libraries for writing plugins to configure network interfaces in Linux containers, along with a number of supported plugins.

%prep
%setup -n plugins-%{version}

%build
./build.sh

%install
install -vdm 755 %{buildroot}%{_default_cni_plugins_dir}
install -vpm 0755 -t %{buildroot}%{_default_cni_plugins_dir} bin/*

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post

%postun

%files
%defattr(-,root,root)
%license LICENSE
%{_default_cni_plugins_dir}/*

%changelog
*   Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 0.7.5-6
-   Increment release to force republishing using golang 1.15.11.
*   Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 0.7.5-5
-   Increment release to force republishing using golang 1.15.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.7.5-4
-   Added %%license line automatically
*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 0.7.5-3
-   Renaming go to golang
*   Tue Mar 07 2020 Paul Monson <paulmon@microsoft.com> 0.7.5-3
-   Fix Source0. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.7.5-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Apr 02 2019 Ashwin H <ashwinh@vmware.com> 0.7.5-1
-   Update cni to v0.7.5
*   Tue Dec 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.6.0-1
-   cni v0.6.0.
*   Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 0.5.1-1
-   Version update
*   Thu Feb 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.4.0-1
-   Add CNI plugins package to PhotonOS.
