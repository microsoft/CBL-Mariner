%define         debug_package %{nil}
Summary:        Microsoft aspnetcore runtime
Name:           aspnetcore-runtime-3.1
Version:        3.1.15
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/dotnet/aspnetcore
Source0:        https://download.visualstudio.microsoft.com/download/pr/8aaf94dc-ce57-4d00-9d2d-70e8b760619e/2979ffe47a37c1aa5d931ee1953613f3/aspnetcore-runtime-3.1.15-linux-x64.tar.gz
Requires:       dotnet-runtime-3.1
ExclusiveArch:  x86_64

%description
ASP.NET Core is an open-source and cross-platform framework for building
modern cloud based internet connected applications, such as web apps,
IoT apps and mobile backends

%prep
%setup -qc -T -a 0 aspnetcore-runtime-%{version}

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet/shared
cp -r shared/Microsoft.AspNetCore.App %{buildroot}%{_libdir}/dotnet/shared

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.txt ThirdPartyNotices.txt
%defattr(-,root,root,0755)
%{_libdir}/dotnet/shared/Microsoft.AspNetCore.App

%changelog
* Wed May 12 2021 Andrew Phelps <anphel@microosft.com> - 3.1.15-1
- Update version to 3.1.15

* Fri May 7 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 3.1.14-1
- Update version to 3.1.14

* Thu Nov 12 2020 Henry Beberman <henry.beberman@microsoft.com> - 3.1.5-1
- Add aspnetcore-runtime spec.
- License verified
- Original version for CBL-Mariner
