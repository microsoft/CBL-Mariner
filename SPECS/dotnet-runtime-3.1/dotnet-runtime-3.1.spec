Summary:        Microsoft .NET Core Runtime
Name:           dotnet-runtime-3.1
Version:        3.1.15
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/dotnet/core
Source0:        https://download.visualstudio.microsoft.com/download/pr/692284f9-e1e7-4b31-9191-cd8043441024/ac45c17d4327b1f992b7fe3956a99129/dotnet-runtime-3.1.15-linux-x64.tar.gz
Requires:       glibc
Requires:       icu
Requires:       krb5
Requires:       libgcc
Requires:       libstdc++
Requires:       libunwind
Requires:       lttng-ust
Requires:       openssl
Requires:       zlib
ExclusiveArch:  x86_64

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%setup -qc -T -a 0 dotnet-runtime-%{version}

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet

cp -r * %{buildroot}%{_libdir}/dotnet
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libdir}/dotnet/dotnet %{buildroot}%{_bindir}/dotnet

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.txt ThirdPartyNotices.txt
%defattr(-,root,root,0755)
%exclude %{_libdir}/dotnet/LICENSE.txt
%exclude %{_libdir}/dotnet/ThirdPartyNotices.txt
%exclude %{_libdir}/debug
%{_bindir}/dotnet
%{_libdir}/*

%changelog
*   Wed May 12 2021 Andrew Phelps <anphel@microsoft.com> 3.1.15-1
-   Update version to 3.1.15

*   Fri May 7 2021 Nicolas Guibourge <nicolasg@microsoft.com> 3.1.14-1
-   Update version to 3.1.14

*   Thu Nov 12 2020 Henry Beberman <henry.beberman@microsoft.com> 3.1.5-2
-   Fix scriptlets and move licenses to the correct folder

*   Fri Jun 19 2020 Andrew Phelps <anphel@microsoft.com> 3.1.5-1
-   Update version to 3.1.5. Fix runtime requirements.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.1.3-4
-   Added %%license line automatically

*   Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> 3.1.3-3
-   Renaming dotnet-runtime to dotnet-runtime-3.1

*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 3.1.3-2
-   Replace BuildArch with ExclusiveArch

*   Mon Mar 30 2020 Andrew Phelps <anphel@microsoft.com> 3.1.3-1
-   Update to dotnet 3.1.3. License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.2.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 2.2.0-1
-   upgraded to version 2.2.0

*   Thu Sep 27 2018 Ajay Kaher <akaher@vmware.com> 2.1.4-1
-   upgraded to version 2.1.4
-   add aarch64 support

*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.5-1
-   Initial build for photon
