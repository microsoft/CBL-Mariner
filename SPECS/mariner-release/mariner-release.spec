Summary:       CBL-Mariner release files
Name:          mariner-release
Version:       1.0
Release:       18%{?dist}
License:       MIT
Group:         System Environment/Base
URL:           https://aka.ms/cbl-mariner
Vendor:        Microsoft Corporation
Distribution:  Mariner
BuildArch:     noarch

# Allows package management tools to find and set the default value
# for the "releasever" variable from the RPM database.
Provides: system-release(releasever)

%description
Azure CBL-Mariner release files such as yum configs and other /etc/ release related files

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
install -d $RPM_BUILD_ROOT/usr/lib

echo "CBL-Mariner %{mariner_release_version}" > %{buildroot}/etc/mariner-release
echo "MARINER_BUILD_NUMBER=%{mariner_build_number}" >> %{buildroot}/etc/mariner-release

cat > %{buildroot}/etc/lsb-release <<- "EOF"
DISTRIB_ID="Mariner"
DISTRIB_RELEASE="%{mariner_release_version}"
DISTRIB_CODENAME=Mariner
DISTRIB_DESCRIPTION="CBL-Mariner %{mariner_release_version}"
EOF

version_id=`echo %{mariner_release_version} | grep -o -E '[0-9]+.[0-9]+' | head -1`
cat > %{buildroot}/usr/lib/os-release << EOF
NAME="Common Base Linux Mariner"
VERSION="%{mariner_release_version}"
ID=mariner
VERSION_ID=$version_id
PRETTY_NAME="CBL-Mariner/Linux"
ANSI_COLOR="1;34"
HOME_URL="%{url}"
BUG_REPORT_URL="%{url}"
SUPPORT_URL="%{url}"
EOF

ln -sv ../usr/lib/os-release %{buildroot}/etc/os-release

cat > %{buildroot}/etc/issue <<- EOF
Welcome to CBL-Mariner %{mariner_release_version} (%{_arch}) - Kernel \r (\l)
EOF

cat > %{buildroot}/etc/issue.net <<- EOF
Welcome to CBL-Mariner %{mariner_release_version} (%{_arch}) - Kernel %r (%t)
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/mariner-release
%config(noreplace) /etc/lsb-release
%config(noreplace) /usr/lib/os-release
%config(noreplace) /etc/os-release
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net

%changelog
*   Thu Jun 15 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-18
-   Updating version for Mid-May update to fix ISO boot issue.
*   Thu Jun 3 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-17
-   Updating version for May update
*   Wed Apr 27 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-16
-   Updating version for April update
*   Tue Mar 30 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-15
-   Updating version for March update
*   Mon Feb 22 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-14
-   Updating version for February update
*   Sun Jan 24 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-13
-   Updating version for January update
*   Mon Dec 21 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-12
-   Updating version for December update.
*   Fri Nov 20 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 1.0-11
-   Updating version for November update
*   Sat Oct 24 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.0-10
-   Updating version for October update
*   Fri Sep 04 2020 Mateusz Malisz <mamalisz@microsoft.com> - 1.0-9
-   Remove empty %%post section, dropping dependency on /bin/sh
*   Tue Aug 24 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.0-8
-   Changing CBL-Mariner ID from "Mariner" to "mariner" to conform to standard.  Also updated Distrib-Description and Name per internal review.
*   Tue Aug 18 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.0-7
-   Restoring correct Name, Distribution Name, CodeName and ID.
*   Fri Jul 31 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-6
-   Updating distribution name.
*   Wed Jul 29 2020 Nick Samson <nisamson@microsoft.com> - 1.0-5
-   Updated os-release file and URL to reflect project naming
*   Wed Jun 24 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.0-4
-   Updated license for 1.0 release.
*   Mon May 04 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-3
-   Providing "system-release(releasever)" for the sake of DNF
-   and other package management tools.
*   Thu Jan 30 2020 Jon Slobodzian <joslobo@microsoft.com> 1.0-2
-   Remove Microsoft name from distro version.
*   Wed Sep 04 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0-1
-   Original version for CBL-Mariner.
