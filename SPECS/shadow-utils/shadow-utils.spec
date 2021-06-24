Summary:        Programs for handling passwords in a secure way
Name:           shadow-utils
Version:        4.6
Release:        12%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/shadow-maint/shadow/
Source0:        https://github.com/shadow-maint/shadow/releases/download/4.6/shadow-%{version}.tar.xz
Source1:        chage
Source2:        chpasswd
Source3:        login
Source4:        other
Source5:        passwd
Source6:        sshd
Source7:        su
Source8:        system-account
Source9:        system-auth
Source10:       system-password
Source11:       system-session
Patch1:         chkname-allowcase.patch
BuildRequires:  cracklib
BuildRequires:  cracklib-devel
BuildRequires:  pam-devel
Requires:       cracklib
Requires:       pam
Provides:       /sbin/nologin
Provides:       passwd = %{version}-%{release}

%description
The Shadow package contains programs for handling passwords
in a secure way.

%prep
%setup -q -n shadow-%{version}
%patch1 -p1
sed -i 's/groups$(EXEEXT) //' src/Makefile.in
find man -name Makefile.in -exec sed -i 's/groups\.1 / /' {} \;
sed -i -e 's@#ENCRYPT_METHOD DES@ENCRYPT_METHOD SHA512@' \
    -e 's@%{_var}/spool/mail@%{_var}/mail@' etc/login.defs

sed -i 's@DICTPATH.*@DICTPATH\t/usr/share/cracklib/pw_dict@' \
    etc/login.defs

%build
%configure --sysconfdir=%{_sysconfdir} --with-libpam \
           --with-libcrack --with-group-name-max-length=32
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/passwd %{buildroot}/bin
sed -i 's/yes/no/' %{buildroot}%{_sysconfdir}/default/useradd
ln -s useradd %{buildroot}%{_sbindir}/adduser
# Use group id 100(users) by default
sed -i 's/GROUP.*/GROUP=100/' %{buildroot}%{_sysconfdir}/default/useradd
# Enable usergroups. Each user will get their own primary group with a name matching their login name
sed -i 's/USERGROUPS_ENAB.*/USERGROUPS_ENAB yes/' %{buildroot}%{_sysconfdir}/login.defs
cp etc/{limits,login.access} %{buildroot}%{_sysconfdir}
for FUNCTION in FAIL_DELAY               \
                FAILLOG_ENAB             \
                LASTLOG_ENAB             \
                MAIL_CHECK_ENAB          \
                OBSCURE_CHECKS_ENAB      \
                PORTTIME_CHECKS_ENAB     \
                QUOTAS_ENAB              \
                CONSOLE MOTD_FILE        \
                FTMP_FILE NOLOGINS_FILE  \
                ENV_HZ PASS_MIN_LEN      \
                SU_WHEEL_ONLY            \
                CRACKLIB_DICTPATH        \
                PASS_CHANGE_TRIES        \
                PASS_ALWAYS_WARN         \
                CHFN_AUTH ENCRYPT_METHOD \
                ENVIRON_FILE
do
    sed -i "s/^${FUNCTION}/# &/" %{buildroot}%{_sysconfdir}/login.defs
done

install -vm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE5} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE6} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE7} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE8} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE9} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE11} %{buildroot}%{_sysconfdir}/pam.d/

for PROGRAM in chfn chgpasswd chsh groupadd groupdel \
               groupmems groupmod newusers useradd userdel usermod
do
    install -v -m644 %{buildroot}%{_sysconfdir}/pam.d/chage %{buildroot}%{_sysconfdir}/pam.d/${PROGRAM}
    sed -i "s/chage/$PROGRAM/" %{buildroot}%{_sysconfdir}/pam.d/${PROGRAM}
done

%find_lang shadow

%check
make %{?_smp_mflags} check

%post
%{_sbindir}/pwconv
%{_sbindir}/grpconv

%files -f shadow.lang
%defattr(-,root,root)
%license COPYING
%config(noreplace) %{_sysconfdir}/login.defs
%config(noreplace) %{_sysconfdir}/login.access
%config(noreplace) %{_sysconfdir}/default/useradd
%config(noreplace) %{_sysconfdir}/limits
%{_bindir}/*
%{_sbindir}/*
/bin/passwd
%{_mandir}/man1
%{_mandir}/man5
%{_mandir}/man8
%exclude %{_mandir}/cs
%exclude %{_mandir}/da
%exclude %{_mandir}/de
%exclude %{_mandir}/fi
%exclude %{_mandir}/fr
%exclude %{_mandir}/hu
%exclude %{_mandir}/id
%exclude %{_mandir}/it
%exclude %{_mandir}/ja
%exclude %{_mandir}/ko
%exclude %{_mandir}/man3
%exclude %{_mandir}/pl
%exclude %{_mandir}/pt_BR
%exclude %{_mandir}/ru
%exclude %{_mandir}/sv
%exclude %{_mandir}/tr
%exclude %{_mandir}/zh_CN
%exclude %{_mandir}/zh_TW
%config(noreplace) %{_sysconfdir}/pam.d/*

%changelog
* Mon Jun 21 2021 Thomas Crain <thcrain@microsoft.com> - 4.6-12
- Enable usergroups for useradd

* Fri Mar 26 2021 Thomas Crain <thcrain@microsoft.com> - 4.6-11
- Merge the following releases from 1.0 to dev branch
- schalam@microsoft.com, 4.6-9: Remove PASS_MAX_DAYS customized value 90 to set default value
- lihl@microsoft.com, 4.6-10: Add sym link to adduser from useradd and create the file for adduser

* Fri Dec 11 2020 Joe Schmitt <joschmit@microsoft.com> - 4.6-10
- Provide passwd.

* Tue Nov 03 2020 Joe Schmitt <joschmit@microsoft.com> - 4.6-9
- Provide /sbin/nologin.

* Sat May 09 00:20:53 PST 2020 Nick Samson <nisamson@microsoft.com> - 4.6-8
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.6-7
- Renaming Linux-PAM to pam

* Mon Apr 14 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.6-6
- Consolidate all subpackages as one and rename it to shadow-utils.
- Update the URL.

* Thu Apr 09 2020 Nicolas Ontiveros <niontive@microsoft.com> - 4.6-5
- Remove toybox and only use shadow-tools for requires.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.6-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Oct 24 2018 Michelle Wang <michellew@vmware.com> - 4.6-3
- Add su and login into shadow-tool.

* Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> - 4.6-2
- Add conflict toybox for shadow-tools.

* Wed Sep 19 2018 Srinidhi Rao <srinidhir@vmware.com> - 4.6-1
- Upgrading the version to 4.6.

* Mon Jul 30 2018 Tapas Kundu <tkundu@vmware.com> - 4.2.1-16
- Added fix for CVE-2018-7169.

* Fri Apr 20 2018 Alexey Makhalov <amakhalov@vmware.com> - 4.2.1-15
- Move pam.d config file to here for better tracking.
- Add pam_loginuid module as optional in a session.

* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.2.1-14
- Added -tools subpackage.
- Main package requires -tools or toybox.

* Tue Aug 15 2017 Anish Swaminathan <anishs@vmware.com> - 4.2.1-13
- Added fix for CVE-2017-12424, CVE-2016-6252.

* Thu Apr 27 2017 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-12
- Allow '.' in username.

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.2.1-11
- BuildRequires Linux-PAM-devel.

* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.2.1-10
- Added -lang subpackage.

* Tue Oct 04 2016 ChangLee <changlee@vmware.com> - 4.2.1-9
- Modified %check.

* Tue Jun 21 2016 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-8
- Added logic to not replace pam.d conf files in upgrade scenario.

* Fri May 27 2016 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-7
- Adding pam_cracklib module as requisite to pam password configuration.

* Wed May 25 2016 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-6
- Modifying pam_systemd module as optional in a session.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.2.1-5
- GA Bump release of all rpms.

* Mon May 2 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.2.1-4
- Enabling pam_systemd module in a session.

* Fri Apr 29 2016 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-3
- Setting password aging limits to 90 days.

* Wed Apr 27 2016 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-3
- Setting password aging limits to 365 days.

* Wed Mar 23 2016 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-2
- Enabling pam_limits module in a session.

* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> - 4.2.1-1
- Update version.

* Wed Dec 2 2015 Divya Thaluru <dthaluru@vmware.com> - 4.1.5.1-6
- Fixed PAM Configuration file for passwd.

* Mon Oct 26 2015 Sharath George <sharathg@vmware.com> - 4.1.5.1-5
- Allow mixed case in username.

* Mon Jun 29 2015 Divya Thaluru <dthaluru@vmware.com> - 4.1.5.1-4
- Fixed PAM Configuration file for chpasswd.

* Tue Jun 16 2015 Alexey Makhalov <amakhalov@vmware.com> - 4.1.5.1-3
- Use group id 100(users) by default.

* Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> - 4.1.5.1-2
- Adding PAM support.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 4.1.5.1-1
- Initial build First version.
