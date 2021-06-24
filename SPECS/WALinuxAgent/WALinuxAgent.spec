Summary:        The Windows Azure Linux Agent
Name:           WALinuxAgent
Version:        2.2.54.2
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Daemons
URL:            https://github.com/Azure/WALinuxAgent
#Source0:       https://github.com/Azure/WALinuxAgent/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  python3-distro
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  systemd
Requires:       /bin/grep
Requires:       /bin/sed
Requires:       iptables
Requires:       openssh
Requires:       openssl
Requires:       python3-pyasn1
Requires:       python3-xml
Requires:       python3
Requires:       python3-libs
Requires:       sudo
Requires:       systemd
Requires:       util-linux
BuildArch:      noarch

%description
The Windows Azure Linux Agent supports the provisioning and running of Linux
VMs in the Windows Azure cloud. This package should be installed on Linux disk
images that are built to run in the Windows Azure environment.

%prep
%setup -q -n %{name}-%{version}

%pre -p /bin/sh

%build
python3 setup.py build -b py3

%install
python3 -tt setup.py build -b py3 install --prefix=%{_prefix} --lnx-distro='mariner' --root=%{buildroot} --force
mkdir -p  %{buildroot}/%{_localstatedir}/log
mkdir -p -m 0700 %{buildroot}/%{_sharedstatedir}/waagent
mkdir -p %{buildroot}/%{_localstatedir}/log
touch %{buildroot}/%{_localstatedir}/log/waagent.log
# python refers to python2 version on CBL-Mariner hence update to use python3
sed -i 's,#!/usr/bin/env python,#!/usr/bin/python3,' %{buildroot}%{_bindir}/waagent
sed -i 's,#!/usr/bin/env python,#!/usr/bin/python3,' %{buildroot}%{_bindir}/waagent2.0
sed -i 's,/usr/bin/python ,/usr/bin/python3 ,' %{buildroot}%{_libdir}/systemd/system/waagent.service

%check
python3 setup.py check && python3 setup.py test

%post
%systemd_post waagent.service

%preun
%systemd_preun waagent.service

%postun
%systemd_postun_with_restart waagent.service

%files
%{_libdir}/systemd/system/*
%defattr(0644,root,root,0755)
%license LICENSE.txt
%attr(0755,root,root) %{_bindir}/waagent
%attr(0755,root,root) %{_bindir}/waagent2.0
%config %{_sysconfdir}/waagent.conf
%ghost %{_localstatedir}/log/waagent.log
%dir %attr(0700, root, root) %{_sharedstatedir}/waagent
%{python3_sitelib}/*

%changelog
* Mon Jun 21 2021 Thomas Crain <thcrain@microsoft.com> - 2.2.54.2-1
- Fix incorrect %%{_lib} macro usage
- Use python3 macros
- Merge the following releases from 1.0 to the dev spec:
- schalam@microsoft.com, 2.2.54.2-1: Upgrade to version 2.2.54.2 which has Mariner distro support.

* Mon Apr 26 2021 Thomas Crain <thcrain@microsoft.com> - 2.2.52-3
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Mon Jan 25 2021 Henry Beberman <henry.beberman@microsoft.com> - 2.2.52-2
- Remove log symlink and use /var/log/waagent.log directly

* Tue Dec 08 2020 Henry Li <lihl@microsoft.com> - 2.2.52-1
- Upgrade to version 2.2.52
- Update add-distro.patch

* Tue Dec 01 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.2.38-4
- Move "waagent" and "waagent2.0" from bindir to sbindir

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.2.38-3
- Added %%license line automatically

* Thu Apr 09 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.2.38-2
- Remove toybox and only use util-linux for requires.

* Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> - 2.2.38-1
- Update to version 2.2.38. Source0 URL fixed. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.2.35-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Feb 12 2019 Tapas Kundu <tkundu@vmware.com> - 2.2.35-1
- Update to 2.2.35

* Tue Oct 23 2018 Anish Swaminathan <anishs@vmware.com> - 2.2.22-1
- Update to 2.2.22

* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com> - 2.2.14-3
- Fixed the log file directory structure

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.2.14-2
- Requires /bin/grep, /bin/sed and util-linux or toybox

* Thu Jul 13 2017 Anish Swaminathan <anishs@vmware.com> - 2.2.14-1
- Update to 2.2.14

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.0.18-4
- Use python2 explicitly to build

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.0.18-3
- GA - Bump release of all rpms

* Tue May 10 2016 Anish Swaminathan <anishs@vmware.com> - 2.0.18-2
- Edit post scripts

* Thu Apr 28 2016 Anish Swaminathan <anishs@vmware.com> - 2.0.18-1
- Update to 2.0.18

* Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> - 2.0.14-3
- Removed redundant requires

* Thu Aug 6 2015 Anish Swaminathan <anishs@vmware.com>
- Added sha1sum

* Fri Mar 13 2015 - mbassiouny@vmware.com
- Initial packaging
