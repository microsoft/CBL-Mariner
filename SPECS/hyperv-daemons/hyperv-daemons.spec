# Hyper-V KVP daemon binary name
%global hv_kvp_daemon hypervkvpd
# Hyper-V VSS daemon binary name
%global hv_vss_daemon hypervvssd
# Hyper-V FCOPY daemon binary name
%global hv_fcopy_daemon hypervfcopyd
# udev rules prefix
%global udev_prefix 70
Summary:        Hyper-V daemons suite
Name:           hyperv-daemons
Version:        5.10.52.1
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
#Source0:        https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner/%{version}.tar.gz
Source0:        kernel-%{version}.tar.gz
# HYPERV KVP DAEMON
Source1:        hypervkvpd.service
Source2:        hypervkvp.rules
Source3:        hv_set_ifconfig
# HYPERV VSS DAEMON
Source101:      hypervvssd.service
Source102:      hypervvss.rules
# HYPERV FCOPY DAEMON
Source201:      hypervfcopyd.service
Source202:      hypervfcopy.rules
BuildRequires:  gcc
Requires:       hypervfcopyd = %{version}-%{release}
Requires:       hypervkvpd = %{version}-%{release}
Requires:       hypervvssd = %{version}-%{release}
# Hyper-V is available only on x86 architectures
# The base empty (a.k.a. virtual) package can not be noarch
# due to http://www.rpm.org/ticket/78

%description
Suite of daemons that are needed when Linux guest
is running on Windows Host with Hyper-V.

%package -n hypervkvpd
Summary:        Hyper-V key value pair (KVP) daemon
BuildRequires:  kernel-headers
BuildRequires:  systemd
Requires:       %{name}-license = %{version}-%{release}
Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd

%description -n hypervkvpd
Hypervkvpd is an implementation of Hyper-V key value pair (KVP)
functionality for Linux. The daemon first registers with the
kernel driver. After this is done it collects information
requested by Windows Host about the Linux Guest. It also supports
IP injection functionality on the Guest.

%package -n hypervvssd
Summary:        Hyper-V VSS daemon
BuildRequires:  kernel-headers
BuildRequires:  systemd
Requires:       %{name}-license = %{version}-%{release}
Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd

%description -n hypervvssd
Hypervvssd is an implementation of Hyper-V VSS functionality
for Linux. The daemon is used for host initiated guest snapshot
on Hyper-V hypervisor. The daemon first registers with the
kernel driver. After this is done it waits for instructions
from Windows Host if to "freeze" or "thaw" the filesystem
on the Linux Guest.

%package -n hypervfcopyd
Summary:        Hyper-V FCOPY daemon
BuildRequires:  kernel-headers
BuildRequires:  systemd
Requires:       %{name}-license = %{version}-%{release}
Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd

%description -n hypervfcopyd
Hypervfcopyd is an implementation of file copy service functionality
for Linux Guest running on Hyper-V. The daemon enables host to copy
a file (over VMBUS) into the Linux Guest. The daemon first registers
with the kernel driver. After this is done it waits for instructions
from Windows Host.

%package license
Summary:        License of the Hyper-V daemons suite
BuildArch:      noarch

%description license
Contains license of the Hyper-V daemons suite.

%package -n hyperv-tools
Summary:        Tools for Hyper-V guests
BuildArch:      noarch

%description -n hyperv-tools
Contains tools and scripts useful for Hyper-V guests.

%prep
%setup -q -n CBL-Mariner-Linux-Kernel-rolling-lts-mariner-%{version}

%build
pushd tools/hv

# HYPERV KVP DAEMON
%{__cc} %{optflags} -c hv_kvp_daemon.c
%{__cc} $RPM_LD_FLAGS  hv_kvp_daemon.o -o %{hv_kvp_daemon}

# HYPERV VSS DAEMON
%{__cc} %{optflags} -c hv_vss_daemon.c
%{__cc} $RPM_LD_FLAGS hv_vss_daemon.o -o %{hv_vss_daemon}

# HYPERV FCOPY DAEMON
%{__cc} %{optflags} -c hv_fcopy_daemon.c
%{__cc} $RPM_LD_FLAGS hv_fcopy_daemon.o -o %{hv_fcopy_daemon}

popd

%install

mkdir -p %{buildroot}%{_sbindir}
install -p -m 0755 tools/hv/%{hv_kvp_daemon} %{buildroot}%{_sbindir}
install -p -m 0755 tools/hv/%{hv_vss_daemon} %{buildroot}%{_sbindir}
install -p -m 0755 tools/hv/%{hv_fcopy_daemon} %{buildroot}%{_sbindir}
# Systemd unit file
mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE101} %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE201} %{buildroot}%{_unitdir}
# Udev rules
mkdir -p %{buildroot}%{_udevrulesdir}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_udevrulesdir}/%{udev_prefix}-hypervkvp.rules
install -p -m 0644 %{SOURCE102} %{buildroot}%{_udevrulesdir}/%{udev_prefix}-hypervvss.rules
install -p -m 0644 %{SOURCE202} %{buildroot}%{_udevrulesdir}/%{udev_prefix}-hypervfcopy.rules
# Shell scripts for the KVP daemon
mkdir -p %{buildroot}%{_libexecdir}/%{hv_kvp_daemon}
install -p -m 0755 tools/hv/hv_get_dhcp_info.sh %{buildroot}%{_libexecdir}/%{hv_kvp_daemon}/hv_get_dhcp_info
install -p -m 0755 tools/hv/hv_get_dns_info.sh %{buildroot}%{_libexecdir}/%{hv_kvp_daemon}/hv_get_dns_info
install -p -m 0755 %{SOURCE3} %{buildroot}%{_libexecdir}/%{hv_kvp_daemon}/hv_set_ifconfig
# Directory for pool files
mkdir -p %{buildroot}%{_sharedstatedir}/hyperv

# Tools
install -p -m 0755 tools/hv/lsvmbus %{buildroot}%{_sbindir}/
sed -i 's,#!/usr/bin/env python,#!/usr/bin/python3,' %{buildroot}%{_sbindir}/lsvmbus

%post -n hypervkvpd
if [ $1 -gt 1 ] ; then
	# Upgrade
	systemctl --no-reload disable hypervkvpd.service >/dev/null 2>&1 || :
fi

%preun -n hypervkvpd
%systemd_preun hypervkvpd.service

%postun -n hypervkvpd
# hypervkvpd daemon does NOT support restarting (driver, neither)
%systemd_postun hypervkvpd.service
# If removing the package, delete %%{_sharedstatedir}/hyperv directory
if [ "$1" -eq "0" ] ; then
    rm -rf %{_sharedstatedir}/hyperv || :
fi

%post -n hypervvssd
if [ $1 -gt 1 ] ; then
	# Upgrade
	systemctl --no-reload disable hypervvssd.service >/dev/null 2>&1 || :
fi

%postun -n hypervvssd
%systemd_postun hypervvssd.service

%preun -n hypervvssd
%systemd_preun hypervvssd.service

%post -n hypervfcopyd
if [ $1 -gt 1 ] ; then
	# Upgrade
	systemctl --no-reload disable hypervfcopyd.service >/dev/null 2>&1 || :
fi

%postun -n hypervfcopyd
%systemd_postun hypervfcopyd.service

%preun -n hypervfcopyd
%systemd_preun hypervfcopyd.service

%files
# the base package does not contain any files.

%files -n hypervkvpd
%{_sbindir}/%{hv_kvp_daemon}
%{_unitdir}/hypervkvpd.service
%{_udevrulesdir}/%{udev_prefix}-hypervkvp.rules
%dir %{_libexecdir}/%{hv_kvp_daemon}
%{_libexecdir}/%{hv_kvp_daemon}/*
%dir %{_sharedstatedir}/hyperv

%files -n hypervvssd
%{_sbindir}/%{hv_vss_daemon}
%{_unitdir}/hypervvssd.service
%{_udevrulesdir}/%{udev_prefix}-hypervvss.rules

%files -n hypervfcopyd
%{_sbindir}/%{hv_fcopy_daemon}
%{_unitdir}/hypervfcopyd.service
%{_udevrulesdir}/%{udev_prefix}-hypervfcopy.rules

%files license
%license COPYING

%files -n hyperv-tools
%{_sbindir}/lsvmbus

%changelog
* Tue Jul 20 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.52.1-1
- Update source to 5.10.52.1

* Tue Jul 06 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.47.1-1
- Update source to 5.10.47.1

* Tue Jun 08 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.42.1-1
- Update source to 5.10.42.1

* Fri May 28 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.37.1-1
- Update source to 5.10.37.1

* Mon May 03 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.32.1-1
- Update source to 5.10.32.1

* Thu Apr 15 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.28.1-2
- Update to kernel release 5.10.28.1-2

* Thu Apr 08 2021 Chris Co <chrco@microsoft.com> - 5.10.28.1-1
- Update source to 5.10.28.1

* Thu Mar 11 2021 Chris Co <chrco@microsoft.com> - 5.10.21.1-1
- Update source to 5.10.21.1

* Thu Feb 18 2021 Chris Co <chrco@microsoft.com> - 5.10.13.1-1
- Update source to 5.10.13.1

* Wed Jan 20 2021 Chris Co <chrco@microsoft.com> - 5.4.91-1
- Update source to 5.4.91

* Mon Dec 28 2020 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.83-2
- Update to kernel release 5.4.83-2

* Tue Dec 15 2020 Henry Beberman <henry.beberman@microsoft.com> - 5.4.83-1
- Update source to 5.4.83

* Fri Dec 04 2020 Chris Co <chrco@microsoft.com> - 5.4.81-1
- Update source to 5.4.81

* Fri Nov 20 2020 Johnson George <johgeorg@microsoft.com> - 5.4.72-3
- Added network configure script to support ip injection

* Wed Nov 11 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.4.72-2
- Enable Hyper-V daemons package building for Arm64 arch

* Mon Oct 26 2020 Chris Co <chrco@microsoft.com> - 5.4.72-1
- Update source to 5.4.72
- Lint spec

* Tue Sep 01 2020 Chris Co <chrco@microsoft.com> - 5.4.51-2
- Update source hash

* Wed Aug 19 2020 Chris Co <chrco@microsoft.com> - 5.4.51-1
- Update source to 5.4.51

* Tue Jun 16 2020 Paul Monson <paulmon@microsoft.com> - 5.4.42-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- Update to match version 5.4.42 of the kernel.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.32.20190303git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Tom Stellard <tstellar@redhat.com> - 0-0.31.20190303git
- Use __cc macro instead of hard-coding gcc

* Fri Nov 08 2019 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.30.20190303git
- Rebase to 5.4-rc6
- Add IgnoreOnIsolate to systemd units

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.29.20190303git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 15 2019 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.28.20190303git
- Rebase to 5.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.27.20180415git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.26.20180415git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 11 2018 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.25.20180415git
- Switch lsvmbus to Python3

* Thu Apr 26 2018 Tomas Hozza <thozza@redhat.com> - 0-0.24.20180415git
- Added gcc as an explicit BuildRequires

* Thu Apr 19 2018 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.23.20180415git
- Rebase to 4.17-rc1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.22.20170105git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.21.20170105git
- Rebase to 4.15-rc2, drop fedora patches as changes are upstream
- Start kvpd after network.target

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.20.20170105git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.19.20170105git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.18.20170105git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.17.20160728git
- Use '-gt' instead of '>' to do the right comparison (#1412033)

* Thu Jan 05 2017 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.16.20160728git
- Rebase to 4.9
- hyperv-tools subpackage added

* Thu Jul 28 2016 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.15.20160728git
- Rebase to 4.8-rc0 (20160728 git snapshot)
- Disable services and remove ConditionVirtualization, multi-user.target
  dependencies switching to udev-only activation (#1331577)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.14.20150702git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.13.20150702git
- Add udev rules to properly restart services (#1195029)
- Spec cleanup

* Thu Jul 02 2015 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.12.20150702git
- Rebase to 4.2-rc0 (20150702 git snapshot)
- Switch to new chardev-based communication layer (#1195029)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.11.20150108git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 08 2015 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.10.20150108git
- Rebase to 3.19-rc3 (20150108 git snapshot)
- Drop 'nodaemon' patches, use newly introduced '-n' option

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.9.20140714git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 14 2014 Tomas Hozza <thozza@redhat.com> - 0-0.8.20140714git
- Update the File copy daemon to the latest git snapshot
- Fix hyperfcopyd.service to check for /dev/vmbus/hv_fcopy

* Wed Jun 11 2014 Tomas Hozza <thozza@redhat.com> - 0-0.7.20140611git
- Fix FTBFS (#1106781)
- Use kernel-headers instead of kernel-devel for building
- package new Hyper-V fcopy daemon as hypervfcopyd sub-package

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.6.20140219git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 19 2014 Tomas Hozza <thozza@redhat.com> - 0-0.5.20140219git
- rebase to the latest git snapshot next-20140219
  - KVP, VSS: removed inclusion of linux/types.h
  - VSS: Ignore VFAT mounts during freeze operation

* Fri Jan 10 2014 Tomas Hozza <thozza@redhat.com> - 0-0.4.20131022git
- provide 'hyperv-daemons' package for convenient installation of all daemons

* Tue Oct 22 2013 Tomas Hozza <thozza@redhat.com> - 0-0.3.20131022git
- rebase to the latest git snapshot next-20130927 (obtained 2013-10-22)
  - KVP, VSS: daemon use single buffer for send/recv
  - KVP: FQDN is obtained on start and cached

* Fri Sep 20 2013 Tomas Hozza <thozza@redhat.com> - 0-0.2.20130826git
- Use 'hypervkvpd' directory in libexec for KVP daemon scripts (#1010268)
- daemons are now WantedBy multi-user.target instead of basic.target (#1010260)

* Mon Aug 26 2013 Tomas Hozza <thozza@redhat.com> - 0-0.1.20130826git
- Initial package
