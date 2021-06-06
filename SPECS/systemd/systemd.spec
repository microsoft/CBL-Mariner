Summary:        Systemd-239
Name:           systemd
Version:        239
Release:        37%{?dist}
License:        LGPLv2+ AND GPLv2+ AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.freedesktop.org/wiki/Software/systemd/
#Source0:       https://github.com/systemd/systemd-stable/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        50-security-hardening.conf
Source2:        systemd.cfg
Source3:        99-dhcp-en.network
Patch0:         01-enoX-uses-instance-number-for-vmware-hv.patch
Patch1:         02-install-general-aliases.patch
Patch2:         systemd-239-default-dns-from-env.patch
Patch3:         systemd-macros.patch
Patch4:         systemd-239-query-duid.patch
# Fix glibc-2.28 build issue. Checked in upstream after v239
Patch5:         systemd-239-glibc-build-fix.patch
Patch6:         systemd-239-revert-mtu.patch
Patch7:         systemd-239-CVE-2018-15688.patch
Patch8:         systemd-239-CVE-2018-15686.patch
Patch9:         systemd-239-CVE-2018-15687.patch
Patch10:        systemd-239-CVE-2018-16864.patch
Patch11:        systemd-239-CVE-2018-16865.patch
Patch12:        systemd-239-CVE-2018-16866.patch
Patch13:        Backport-FOREACH_STRING-fix-for-gcc9.patch
Patch14:        Disable-argument-to-mount_cgroup_controllers.patch
# This commit from upstream fixes an issue caused by using a later version of meson.
Patch15:        https://github.com/systemd/systemd/commit/8f6b442a78d0b485f044742ad90b2e8271b4e68e.patch
Patch16:        CVE-2019-3842.patch
Patch17:        CVE-2019-3843.patch
Patch18:        CVE-2019-3844.patch
Patch19:        CVE-2019-6454.patch
Patch20:        CVE-2019-20386.patch
Patch21:        CVE-2020-1712.patch
Patch22:        CVE-2020-13776.patch
# This vulnerability is in the strict DNS-over-TLS (DoT) mechanism of systemd-resolve.
# DoT is only enabled when systemd is build against gnutls.
# Furthermore, strict mode DoT is not supported before v243.
Patch23:        CVE-2018-21029.nopatch
#Portablectl patches for --now --enable and --no-block flags support
Patch100:       100-portabled-allow-to-detach-an-image-with-a-unit-in-li.patch
Patch101:       101-Portabled-fix-inspect-on-image-attached-as-directory.patch
Patch102:       102-portablectl-add-now-and-enable-to-attach-detach.patch
Patch103:       103-core-allow-portablectl-to-load-new-services-without-.patch
Patch104:       104-portablectl-block-when-stopping-a-unit-on-detach-now.patch
Patch105:       105-portablectl-use-replace-unload-when-stopping-a-servi.patch
Patch106:       106-portabled-implement-container-host-os-release-interf.patch
Patch1000:      0001-udevd-drop-redundant-logic-of-receiving-uevent.patch
BuildRequires:  cryptsetup-devel
BuildRequires:  docbook-dtd-xml
BuildRequires:  docbook-style-xsl
BuildRequires:  gettext
BuildRequires:  glib-devel
BuildRequires:  gperf
BuildRequires:  intltool
BuildRequires:  kbd
BuildRequires:  kmod-devel
BuildRequires:  libcap-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libxslt
BuildRequires:  lz4-devel
BuildRequires:  meson
BuildRequires:  pam-devel
BuildRequires:  perl-XML-Parser
BuildRequires:  shadow-utils
BuildRequires:  util-linux-devel >= 2.30
BuildRequires:  xz-devel
Requires:       filesystem >= 1.1
Requires:       glib
Requires:       kmod
Requires:       libcap
Requires:       libgcrypt
Requires:       lz4
Requires:       pam
Requires:       xz
Obsoletes:      systemd-bootstrap

%description
Systemd is an init replacement with better process control and security

%package devel
Summary:        Development headers for systemd
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel

%description devel
Development headers for developing applications linking to libsystemd

%package lang
Summary:        Language pack for systemd
Requires:       %{name} = %{version}-%{release}

%description lang
Language pack for systemd

%prep
%autosetup -p1
cat > config.cache << "EOF"
KILL=/bin/kill
HAVE_BLKID=1
BLKID_LIBS="-lblkid"
BLKID_CFLAGS="-I/usr/include/blkid"
cc_cv_CFLAGS__flto=no
EOF

sed -i "s#\#DefaultTasksMax=512#DefaultTasksMax=infinity#g" src/core/system.conf.in

%build
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
CFLAGS="%{build_cflags} -Wno-error=format-overflow="                        \
meson  --prefix %{_prefix}                                            \
       --sysconfdir %{_sysconfdir}                                    \
       --localstatedir %{_var}                                        \
       -Dblkid=true                                                   \
       -Dbuildtype=release                                            \
       -Ddefault-dnssec=no                                            \
       -Dfirstboot=false                                              \
       -Dinstall-tests=false                                          \
       -Dldconfig=false                                               \
       -Drootprefix=                                                  \
       -Drootlibdir=/lib                                              \
       -Dsplit-usr=true                                               \
       -Dsysusers=false                                               \
       -Dpam=true                                                     \
       -Dlibcurl=false                                                \
       -Dpolkit=true                                                  \
       -Dlibcryptsetup=true                                           \
       -Dgcrypt=true                                                  \
       -Dlz4=true                                                     \
       -Ddbuspolicydir=%{_sysconfdir}/dbus-1/system.d                 \
       -Ddbussessionservicedir=%{_datadir}/dbus-1/services            \
       -Ddbussystemservicedir=%{_datadir}/dbus-1/system-services      \
       -Dsysvinit-path=%{_sysconfdir}/rc.d/init.d                     \
       -Drc-local=%{_sysconfdir}/rc.d/rc.local                        \
       $PWD build &&
       cd build &&
       %ninja_build

%install
cd build && %ninja_install

install -vdm 755 %{buildroot}/sbin
for tool in runlevel reboot shutdown poweroff halt telinit; do
     ln -sfv ../bin/systemctl %{buildroot}/sbin/${tool}
done
ln -sfv ../lib/systemd/systemd %{buildroot}/sbin/init
sed -i '/srv/d' %{buildroot}%{_lib}/tmpfiles.d/home.conf
sed -i "s:0775 root lock:0755 root root:g" %{buildroot}%{_lib}/tmpfiles.d/legacy.conf
sed -i "s:NamePolicy=kernel database onboard slot path:NamePolicy=kernel database:g" %{buildroot}/lib/systemd/network/99-default.link
sed -i "s:#LLMNR=yes:LLMNR=false:g" %{buildroot}%{_sysconfdir}/systemd/resolved.conf
sed -i "s:#NTP=:NTP=time.windows.com:g" %{buildroot}%{_sysconfdir}/systemd/timesyncd.conf
rm -f %{buildroot}%{_var}/log/README
mkdir -p %{buildroot}%{_localstatedir}/opt/journal/log
mkdir -p %{buildroot}%{_localstatedir}/log
ln -sfv %{_localstatedir}/opt/journal/log %{buildroot}%{_localstatedir}/log/journal

find %{buildroot} -type f -name "*.la" -delete -print
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysctl.d
install -dm 0700 %{buildroot}/boot/
install -m 0600 %{SOURCE2} %{buildroot}/boot/
rm %{buildroot}/lib/systemd/system/default.target
ln -sfv multi-user.target %{buildroot}/lib/systemd/system/default.target
install -dm 0755 %{buildroot}/%{_sysconfdir}/systemd/network
install -m 0644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/systemd/network
%find_lang %{name} ../%{name}.lang

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE.GPL2
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/user
%dir %{_sysconfdir}/systemd/network
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/binfmt.d
%{_sysconfdir}/X11/xinit/xinitrc.d/50-systemd-user.sh
%{_sysconfdir}/sysctl.d/50-security-hardening.conf
%{_sysconfdir}/xdg/systemd
%{_sysconfdir}/rc.d/init.d/README
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.login1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.locale1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.timedate1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.resolve1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.network1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.machine1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.portable1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.timesync1.conf
%config(noreplace) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %{_sysconfdir}/systemd/user.conf
%config(noreplace) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %{_sysconfdir}/systemd/resolved.conf
%config(noreplace) %{_sysconfdir}/systemd/coredump.conf
%config(noreplace) %{_sysconfdir}/systemd/timesyncd.conf
%config(noreplace) %{_sysconfdir}/pam.d/systemd-user
%config(noreplace) %{_sysconfdir}/systemd/network/99-dhcp-en.network

%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d
%dir %{_sysconfdir}/udev/hwdb.d
%config(noreplace) %{_sysconfdir}/udev/udev.conf
%config(noreplace) /boot/systemd.cfg
%{_sysconfdir}/systemd/system/*
/lib/udev/*
/lib/systemd/systemd*
/lib/systemd/system-*
/lib/systemd/system/*
/lib/systemd/network/80-container*
/lib/systemd/*.so
/lib/systemd/resolv.conf
/lib/systemd/portablectl
%config(noreplace) /lib/systemd/network/99-default.link
%config(noreplace) /lib/systemd/portable/profile/default/service.conf
%config(noreplace) /lib/systemd/portable/profile/nonetwork/service.conf
%config(noreplace) /lib/systemd/portable/profile/strict/service.conf
%config(noreplace) /lib/systemd/portable/profile/trusted/service.conf
%{_libdir}/environment.d/99-environment.conf
%exclude %{_libdir}/debug
%exclude %{_datadir}/locale
%{_libdir}/binfmt.d
%{_libdir}/kernel
%{_libdir}/modules-load.d
%{_libdir}/rpm
/lib/security
%{_libdir}/sysctl.d
%{_libdir}/systemd
%{_libdir}/tmpfiles.d
/lib/*.so*
/lib/modprobe.d/systemd.conf
%{_bindir}/*
/bin/*
/sbin/*
%{_datadir}/bash-completion/*
%{_datadir}/factory/*
%{_datadir}/dbus-1
%{_docdir}/*
%{_mandir}/man[1578]/*
%{_datadir}/polkit-1
%{_datadir}/systemd
%{_datadir}/zsh/*
%dir %{_localstatedir}/opt/journal/log
%{_localstatedir}/log/journal

%files devel
%dir %{_includedir}/systemd
/lib/libudev.so
/lib/libsystemd.so
%{_includedir}/systemd/*.h
%{_includedir}/libudev.h
%{_libdir}/pkgconfig/libudev.pc
%{_libdir}/pkgconfig/libsystemd.pc
%{_datadir}/pkgconfig/systemd.pc
%{_datadir}/pkgconfig/udev.pc
%{_mandir}/man3/*

%files lang -f %{name}.lang

%changelog
* Thu Jun 03 2021 Chris Co <chrco@microsoft.com> - 239-37
- Add patch to remove redundant on_uevent call from on_inotify.

* Thu Mar 11 2021 Chris Co <chrco@microsoft.com> - 239-36
- Disallow unprivileged BPF scripts by default. Additional mitigation for CVE-2021-20194

* Fri Feb 12 2021 Henry Beberman <henry.beberman@microsoft.com> - 239-35
- Enable LZ4 so journalctl can read logs from the container host.

* Fri Nov 13 2020 Nicolas Ontiveros <niontive@microsoft.com> - 239-34
- Fix CVE-2019-6454 patch. Add upstream patch info.
- Fix CVE-2020-1712 patch. Add upstream patch info.

* Thu Oct 22 2020 Nicolas Ontiveros <niontive@microsoft.com> - 239-33
- Use autosetup
- Fix CVE-2019-3842
- Fix CVE-2019-3843
- Fix CVE-2019-3844
- Fix CVE-2019-6454
- Fix CVE-2019-20386
- Fix CVE-2020-1712
- Fix CVE-2020-13776

*  Wed Sep 23 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 239-32
-  Portablectl patches for --now --enable and --no-block flags support

*  Mon Aug 24 2020 Leandro Pereira <leperei@microsoft.com> 239-31
-  Use time.windows.com as the default NTP server in timesyncd.

*  Tue Aug 11 2020 Mateusz Malisz <mamalisz@microsoft.com> 239-30
-  Reduce kptr_restrict to 1

*  Fri May 29 2020 Nicolas Ontiveros <niontive@microsoft.com> 239-29
-  Include cryptsetup to build cryptsetup generator.

*  Wed May 27 2020 Chris Co <chrco@microsoft.com> 239-28
-  Disable IPv6 router advertisements by default

*  Wed May 20 2020 Emre Girgin <mrgirgin@microsoft.com> 239-27
-  Change /boot directory permissions to 600.

*  Wed May 20 2020 Joe Schmitt <joschmit@microsoft.com> 239-26
-  Remove 99-vmware-hotplug.rules.

*  Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 239-25
-  Added %%license line automatically

*  Wed May 06 2020 Emre Girgin <mrgirgin@microsoft.com> 239-24
-  Renaming docbook-xsl to docbook-style-xsl

*  Wed May 06 2020 Emre Girgin <mrgirgin@microsoft.com> 239-23
-  Renaming docbook-xml to docbook-dtd-xml

*  Wed May 06 2020 Emre Girgin <mrgirgin@microsoft.com> 239-22
-  Renaming Linux-PAM to pam

*  Wed May 06 2020 Emre Girgin <mrgirgin@microsoft.com> 239-21
-  Renaming XML-Parser to perl-XML-Parser

*  Tue May 05 2020 Joe Schmitt <joschmit@microsoft.com> 239-20
-  Remove unused rdrand-rng after kernel update.

*  Thu Apr 23 2020 Emre Girgin <mrgirgin@microsoft.com> 239-19
-  Ignore CVE-2018-21029.

*  Fri Apr 17 2020 Emre Girgin <mrgirgin@microsoft.com> 239-18
-  Rename shadow to shadow-utils.

*  Thu Apr 16 2020 Emre Girgin <mrgirgin@microsoft.com> 239-17
-  Resolve build issues arising from upgrading meson to 0.49.2.

*  Thu Apr 09 2020 Henry Beberman <henry.beberman@microsoft.com> 239-16
-  Add patch to disable arguments to mount_cgroup_controllers as in upstream latest.

*  Tue Apr 07 2020 Paul Monson <paulmon@microsoft.com> 239-15
-  Update Source0 link.  License verified.

*  Tue Mar 31 2020 Henry Beberman <henry.beberman@microsoft.com> 239-14
-  Backport upstream fix for FOREACH_STRING macro.

*  Tue Mar 24 2020 Henry Beberman <henry.beberman@microsoft.com> 239-13
-  Add -Wno-error=format-overflow= to fix gcc9 build.

*  Thu Feb 27 2020 Henry Beberman <hebeberm@microsoft.com> 239-12
-  Disable libcurl auto-configure

*  Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 239-11
-  Initial CBL-Mariner import from Photon (license: Apache2).

*  Thu Jan 10 2019 Anish Swaminathan <anishs@vmware.com>  239-10
-  Fix CVE-2018-16864, CVE-2018-16865, CVE-2018-16866

*  Wed Jan 09 2019 Keerthana K <keerthanak@vmware.com> 239-9
-  Seting default values for tcp_timestamps, tcp_challenge_ack_limit and ip_forward.

*  Wed Jan 02 2019 Anish Swaminathan <anishs@vmware.com>  239-8
-  Fix CVE-2018-15686, CVE-2018-15687

*  Sun Nov 11 2018 Tapas Kundu <tkundu@vmware.com> 239-7
-  Fix CVE-2018-15688

*  Fri Oct 26 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 239-6
-  Auto-load rdrand-rng kernel module only on x86.

*  Fri Oct 26 2018 Anish Swaminathan <anishs@vmware.com>  239-5
-  Revert the commit that causes GCE networkd timeout
-  https://github.com/systemd/systemd/commit/44b598a1c9d11c23420a5ef45ff11bcb0ed195eb

*  Mon Oct 08 2018 Srinidhi Rao <srinidhir@vmware.com> 239-4
-  Add glib-devel as a Requirement to systemd-devel

*  Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 239-3
-  Fix compilation issue against glibc-2.28

*  Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 239-2
-  Automatically load rdrand-rng kernel module on every boot.

*  Tue Aug 28 2018 Anish Swaminathan <anishs@vmware.com>  239-1
-  Update systemd to 239

*  Wed Apr 11 2018 Xiaolin Li <xiaolinl@vmware.com>  236-3
-  Build systemd with util-linux 2.32.

*  Wed Jan 17 2018 Divya Thaluru <dthaluru@vmware.com>  236-2
-  Fixed the log file directory structure

*  Fri Dec 29 2017 Anish Swaminathan <anishs@vmware.com>  236-1
-  Update systemd to 236

*  Thu Nov 09 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-11
-  Fix CVE-2017-15908 dns packet loop fix.

*  Tue Nov 07 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-10
-  Fix nullptr access during link disable.

*  Mon Sep 18 2017 Anish Swaminathan <anishs@vmware.com>  233-9
-  Backport router solicitation backoff from systemd 234

*  Fri Sep 15 2017 Anish Swaminathan <anishs@vmware.com>  233-8
-  Move network file to systemd package

*  Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> 233-7
-  Fix compilation issue for glibc-2.26

*  Fri Jul 21 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-6
-  Fix for CVE-2017-1000082.

*  Fri Jul 07 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-5
-  Fix default-dns-from-env patch.

*  Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 233-4
-  Add kmod-devel to BuildRequires

*  Thu Jun 29 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-3
-  Fix for CVE-2017-9445.

*  Tue Jun 20 2017 Anish Swaminathan <anishs@vmware.com>  233-2
-  Fix for CVE-2017-9217

*  Mon Mar 06 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-1
-  Update systemd to 233

*  Tue Jan 3 2017 Alexey Makhalov <amakhalov@vmware.com>  232-5
-  Added /boot/systemd.cfg

*  Tue Dec 20 2016 Alexey Makhalov <amakhalov@vmware.com>  232-4
-  Fix initrd-switch-root issue

*  Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 232-3
-  BuildRequires Linux-PAM-devel

*  Thu Dec 01 2016 Xiaolin Li <xiaolinl@vmware.com> 232-2
-  disable-elfutils.

*  Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  232-1
-  Update systemd to 232

*  Thu Nov 3 2016 Divya Thaluru <dthaluru@vmware.com>  228-32
-  Added logic to reload services incase of rpm upgrade

*  Thu Sep 29 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-31
-  Fix a CVE in systemd-notify socket.

*  Mon Aug 29 2016 Alexey Makhalov <amakhalov@vmware.com>  228-30
-  02-install-general-aliases.patch to create absolute symlinks

*  Fri Aug 26 2016 Anish Swaminathan <anishs@vmware.com>  228-29
-  Change config file properties for 99-default.link

*  Tue Aug 16 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-28
-  systemd-resolved: Fix DNS_TRANSACTION_PENDING assert.

*  Mon Aug 1 2016 Divya Thaluru <dthaluru@vmware.com> 228-27
-  Removed packaging of symlinks and will be created during installation

*  Tue Jul 12 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-26
-  systemd-resolved: Fix DNS domains resolv.conf search issue for static DNS.

*  Mon Jul 11 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-25
-  systemd-networkd: Update DUID/IAID config interface to systemd v230 spec.

*  Tue Jun 21 2016 Anish Swaminathan <anishs@vmware.com>  228-24
-  Change config file properties

*  Fri Jun 17 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-23
-  systemd-resolved: Configure initial DNS servers from environment var.

*  Mon Jun 06 2016 Alexey Makhalov <amakhalov@vmware.com>  228-22
-  systemd-resolved: disable LLMNR

*  Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 228-21
-  GA - Bump release of all rpms

*  Tue May 17 2016 Anish Swaminathan <anishs@vmware.com>  228-20
-  Added patch for letting kernel handle ndisc

*  Tue May 17 2016 Divya Thaluru <dthaluru@vmware.com> 228-19
-  Updated systemd-user PAM configuration

*  Mon May 16 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 228-18
-  Updated the MaxTasks to infinity in system.conf file

*  Thu Apr 21 2016 Mahmoud Bassiouny <mbassiouny@vmware.com>  228-17
-  Set the default.target to the multi-user.target

*  Tue Apr 12 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-16
-  Disable network interface renaming.

*  Thu Mar 31 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-15
-  Patch to query DHCP DUID, IAID.f

*  Wed Mar 30 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-14
-  Update DHCP DUID, IAID configuration patch.

*  Wed Mar 30 2016 Kumar Kaushik <kaushikk@vmware.com>  228-13
-  Install the security hardening script as part of systemd.

*  Tue Mar 29 2016 Kumar Kaushik <kaushikk@vmware.com>  228-12
-  Added patch for timedatectl /etc/adjtime PR2749.

*  Fri Mar 11 2016 Anish Swaminathan <anishs@vmware.com>  228-11
-  Added patch for dhcp preservation via duid iaid configurability

*  Fri Mar 11 2016 Anish Swaminathan <anishs@vmware.com>  228-10
-  Added patch for swap disconnect order

*  Thu Mar 10 2016 XIaolin Li <xiaolinl@vmware.com> 228-9
-  Enable manpages.

*  Fri Feb 19 2016 Anish Swaminathan <anishs@vmware.com>  228-8
-  Added patch to get around systemd-networkd wait online timeout

*  Sat Feb 06 2016 Alexey Makhalov <amakhalov@vmware.com>  228-7
-  Added patch: fix-reading-routes.

*  Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  228-6
-  Add hotplug udev rules.

*  Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  228-5
-  Change config file attributes.

*  Wed Jan 06 2016 Anish Swaminathan <anishs@vmware.com> 228-4
-  Patches for minor network fixes.

*  Wed Dec 16 2015 Anish Swaminathan <anishs@vmware.com> 228-3
-  Patch for ostree.

*  Wed Dec 16 2015 Anish Swaminathan <anishs@vmware.com> 228-2
-  Patch for loopback address.

*  Fri Dec 11 2015 Anish Swaminathan <anishs@vmware.com> 228-1
-  Upgrade systemd version.

*  Mon Nov 30 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 216-13
-  Removing the reference of lock user

*  Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 216-12
-  Removing la files from packages.

*  Fri Sep 18 2015 Divya Thaluru <dthaluru@vmware.com> 216-11
-  Packaging journal log directory

*  Thu Sep 10 2015 Alexey Makhalov <amakhalov@vmware.com> 216-10
-  Improve enoX renaming in VMware HV case. Patch is added.

*  Tue Aug 25 2015 Alexey Makhalov <amakhalov@vmware.com> 216-9
-  Reduce systemd-networkd boot time (exclude if-rename patch).

*  Mon Jul 20 2015 Divya Thaluru <dthaluru@vmware.com> 216-8
-  Adding sysvinit support

*  Mon Jul 06 2015 Kumar Kaushik <kaushikk@vmware.com> 216-7
-  Fixing networkd/udev race condition for renaming interface.

*  Thu Jun 25 2015 Sharath George <sharathg@vmware.com> 216-6
-  Remove debug files.

*  Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 216-5
-  Building compat libs

*  Mon Jun 1 2015 Alexey Makhalov <amakhalov@vmware.com> 216-4
-  gudev support

*  Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 216-3
-  Removing packing of PAM configuration files

*  Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 216-2
-  Update according to UsrMove.

*  Mon Oct 27 2014 Sharath George <sharathg@vmware.com> 216-1
-  Initial build. First version
