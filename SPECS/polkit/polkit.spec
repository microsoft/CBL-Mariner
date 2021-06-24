Summary:       A toolkit for defining and handling authorizations.
Name:          polkit
Version:       0.116
Release:       4%{?dist}
Group:         Applications/System
Vendor:        Microsoft Corporation
License:       LGPLv2+
URL:           https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html
Source0:       https://www.freedesktop.org/software/polkit/releases/%{name}-%{version}.tar.gz
Patch0:        CVE-2021-3560.patch
Distribution:  Mariner
BuildRequires: autoconf
BuildRequires: expat-devel
BuildRequires: glib-devel
BuildRequires: gobject-introspection
BuildRequires: intltool >= 0.40.0
BuildRequires: mozjs60-devel
BuildRequires: pam-devel
BuildRequires: systemd-devel
Requires:      expat
Requires:      glib
Requires:      mozjs60
Requires:      pam
Requires:      systemd
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):  /usr/sbin/userdel /usr/sbin/groupdel

%description
polkit provides an authorization API intended to be used by privileged programs
(“MECHANISMS”) offering service to unprivileged programs (“SUBJECTS”) often
through some form of inter-process communication mechanism

%package devel
Summary: polkit development headers and libraries
Group: Development/Libraries
Requires: polkit = %{version}-%{release}

%description devel
header files and libraries for polkit

%prep
%autosetup -p1

%build
%configure \
    --datadir=%{_datarootdir} \
    --enable-libsystemd-login=yes \
    --with-systemdsystemunitdir=%{_libdir}/systemd/system
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
install -vdm 755 %{buildroot}/etc/pam.d
cat > %{buildroot}/etc/pam.d/polkit-1 << "EOF"
# Begin /etc/pam.d/polkit-1

auth     include        system-auth
account  include        system-account
password include        system-password
session  include        system-session

# End /etc/pam.d/polkit-1
EOF

%check
# Disable check. It requires dbus - not available in chroot/container.

%pre
getent group polkitd > /dev/null || groupadd -fg 27 polkitd &&
getent passwd polkitd > /dev/null || \
    useradd -c "PolicyKit Daemon Owner" -d /etc/polkit-1 -u 27 \
        -g polkitd -s /bin/false polkitd

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    systemctl stop polkit
    if getent passwd polkitd >/dev/null; then
        userdel polkitd
    fi
    if getent group polkitd >/dev/null; then
        groupdel polkitd
    fi
fi

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/pk*
%{_libdir}/lib%{name}-*.so.*
%{_libdir}/polkit-1/polkit-agent-helper-1
%{_libdir}/polkit-1/polkitd
%{_libdir}/systemd/system/polkit.service
%{_datarootdir}/dbus-1/system-services/org.freedesktop.PolicyKit1.service
%{_datarootdir}/locale/*
%{_datarootdir}/polkit-1/actions/*.policy
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%{_sysconfdir}/pam.d/polkit-1
%{_sysconfdir}/polkit-1/rules.d/50-default.rules

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}-1/
%{_libdir}/lib%{name}-*.a
%{_libdir}/lib%{name}-*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gettext/its/polkit.its
%{_datadir}/gettext/its/polkit.loc

%changelog
*   Thu Jun 03 2021 Jon Slobodzian <josloboe@microsoft.com> - 0.116-4
-   Patch for CVE 2021-3560.  Fix changelog formatting.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.116-3
-   Added %%license line automatically

*   Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 0.116-2
-   Renaming Linux-PAM to pam

*   Thu Apr 16 2020 Nicolas Ontiveros <niontive@microsoft.com> 0.116-1
-   Update to version 0.116.
-   License verified.
-   Use mozjs60 instead of js for requires and BR.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.113-5
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Thu Jan 10 2019 Dweep Advani <dadvani@vmware.com> 0.113-4
-   Fix for CVE-2018-19788

*   Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 0.113-3
-   Added pre and postun requires for shadow tools

*   Thu Oct 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.113-2
-   Enable PAM and systemd.

*   Wed Oct 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.113-1
-   Upgrade to 0.113-1

*   Fri May 22 2015 Alexey Makhalov <amakhalov@vmware.com> 0.112-1
-   initial version
