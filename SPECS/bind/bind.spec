%global        bind_dir          %{_var}/named
%global        chroot_prefix     %{bind_dir}/chroot
%global        chroot_create_directories /dev /run/named %{_localstatedir}/{log,named,tmp} \\\
                                         %{_sysconfdir}/crypto-policies/back-ends %{_sysconfdir}/pki/dnssec-keys %{_sysconfdir}/named \\\
                                         %{_libdir}/bind %{_libdir}/named %{_datadir}/GeoIP
## The order of libs is important. See lib/Makefile.in for details
%define bind_export_libs isc dns isccfg irs
%{!?_export_dir:%global _export_dir /bind9-export/}
Summary:        Domain Name System software
Name:           bind
Version:        9.16.15
Release:        1%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://www.isc.org/downloads/bind/
Source0:        https://ftp.isc.org/isc/bind9/%{version}/%{name}-%{version}.tar.xz
Source1:        named.sysconfig
Source2:        named.logrotate
Source3:        named.root
Source4:        named.localhost
Source5:        named.loopback
Source6:        named.empty
Source7:        named.rfc1912.zones
Source8:        named.conf.sample
Source9:        named.root.key
Source10:       trusted-key.key
Source11:       setup-named-chroot.sh
Source12:       generate-rndc-key.sh
Source13:       named.rwtab
Source14:       setup-named-softhsm.sh
Source15:       named-chroot.files
# CVE-2019-6470 is fixed by updating the dhcp package to 4.4.1 or greater
Patch0:         CVE-2019-6470.nopatch
# CVE-2020-8623 only impacts package built with "--enable-native-pkcs11"
Patch1:         CVE-2020-8623.nopatch
Patch2:         bind-9.14-config-pkcs11.patch
Patch3:         bind-9.10-dist-native-pkcs11.patch
BuildRequires:  gcc
BuildRequires:  json-c-devel
BuildRequires:  krb5-devel
BuildRequires:  libcap-devel
BuildRequires:  libtool
BuildRequires:  libuv-devel
BuildRequires:  lmdb-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  python3
BuildRequires:  python3-ply
Requires:       libuv
Requires:       openssl
Requires(postun): %{_sbindir}/groupdel
Requires(postun): %{_sbindir}/userdel
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd
# Enforce fix for CVE-2019-6470
Conflicts:      dhcp < 4.4.1
# libisc-nosym requires to be linked with unresolved symbols
# When libisc-nosym linking is fixed, it can be defined to 1
# Visit https://bugzilla.redhat.com/show_bug.cgi?id=1540300
%undefine _strict_symbol_defs_build

%description
BIND is open source software that implements the Domain Name System (DNS) protocols
for the Internet. It is a reference implementation of those protocols, but it is
also production-grade software, suitable for use in high-volume and high-reliability applications.

%package pkcs11
Summary:        Bind with native PKCS#11 functionality for crypto
Requires:       bind%{?_isa} = %{version}-%{release}
Requires:       bind-libs%{?_isa} = %{version}-%{release}
Requires:       bind-pkcs11-libs%{?_isa} = %{version}-%{release}
Requires:       systemd
Recommends:     softhsm

%description pkcs11
This is a version of BIND server built with native PKCS#11 functionality.
It is important to have SoftHSM v2+ installed and some token initialized.
For other supported HSM modules please check the BIND documentation.

%package pkcs11-utils
Summary:        Bind tools with native PKCS#11 for using DNSSEC
Requires:       bind-dnssec-doc = %{version}-%{release}
Requires:       bind-pkcs11-libs%{?_isa} = %{version}-%{release}
Obsoletes:      bind-pkcs11 < 9.9.4-16.P2

%description pkcs11-utils
This is a set of PKCS#11 utilities that when used together create rsa
keys in a PKCS11 keystore. Also utilities for working with DNSSEC
compiled with native PKCS#11 functionality are included.

%package pkcs11-libs
Summary:        Bind libraries compiled with native PKCS#11
Requires:       bind-libs%{?_isa} = %{version}-%{release}
Requires:       bind-license = %{version}-%{release}

%description pkcs11-libs
This is a set of BIND libraries (dns, isc) compiled with native PKCS#11
functionality.

%package pkcs11-devel
Summary:        Development files for Bind libraries compiled with native PKCS#11
Requires:       bind-devel%{?_isa} = %{version}-%{release}
Requires:       bind-pkcs11-libs%{?_isa} = %{version}-%{release}

%description pkcs11-devel
This a set of development files for BIND libraries (dns, isc) compiled
with native PKCS#11 functionality.

%package libs
Summary:        Libraries used by the BIND DNS packages
Requires:       bind-license = %{version}-%{release}
Provides:       bind-libs-lite = %{version}-%{release}
Obsoletes:      bind-libs-lite < 9.16.13

%description libs
Contains heavyweight version of BIND suite libraries used by both named DNS
server and utilities in bind-utils package.

%package license
Summary:        License of the BIND DNS suite
BuildArch:      noarch

%description license
Contains license of the BIND DNS suite.

%package devel
Summary:        Header files and libraries needed for bind-dyndb-ldap
Requires:       bind-libs%{?_isa} = %{version}-%{release}
Requires:       json-c-devel%{?_isa}
Requires:       krb5-devel%{?_isa}
Requires:       libcap-devel%{?_isa}
Requires:       libxml2-devel%{?_isa}
Requires:       lmdb-devel%{?_isa}
Requires:       openssl-devel%{?_isa}
Provides:       bind-lite-devel = %{version}-%{release}
Obsoletes:      bind-lite-devel < 9.16.6-3

%description devel
The bind-devel package contains full version of the header files and libraries
required for building bind-dyndb-ldap. Upstream no longer supports nor recommends
bind libraries for third party applications.

%package chroot
Summary:        A chroot runtime environment for the ISC BIND DNS server, named(8)
Requires:       bind%{?_isa} = %{version}-%{release}
# grep is required due to setup-named-chroot.sh script
Requires:       grep

%description chroot
This package contains a tree of files which can be used as a
chroot(2) jail for the named(8) program from the BIND package.
Based on the code from Jan "Yenya" Kasprzak <kas@fi.muni.cz>

%package dnssec-utils
Summary:        DNSSEC keys and zones management utilities
Requires:       bind-dnssec-doc = %{version}-%{release}
Requires:       bind-libs%{?_isa} = %{version}-%{release}
Requires:       python3-bind = %{version}-%{release}
Recommends:     bind-utils

%description dnssec-utils
Bind-dnssec-utils contains a collection of utilities for editing
DNSSEC keys and BIND zone files. These tools provide generation,
revocation and verification of keys and DNSSEC signatures in zone files.

You should install bind-dnssec-utils if you need to sign a DNS zone
or maintain keys for it.

%package dnssec-doc
Summary:        Manual pages of DNSSEC utilities
Requires:       bind-license = %{version}-%{release}
BuildArch:      noarch

%description dnssec-doc
Bind-dnssec-doc contains manual pages for bind-dnssec-utils.

%package -n python3-bind
Summary:        A module allowing rndc commands to be sent from Python programs
Requires:       bind-license = %{version}-%{release}
Requires:       python3
Requires:       python3-ply
BuildArch:      noarch

%description -n python3-bind
This package provides a module which allows commands to be sent to rndc directly from Python programs.

%package utils
Summary:        BIND utilities

%description utils
%{summary}.

%prep
%setup -q

%patch2 -p1 -b .config-pkcs11
cp -r bin/named{,-pkcs11}
cp -r bin/dnssec{,-pkcs11}
cp -r lib/dns{,-pkcs11}
cp -r lib/ns{,-pkcs11}
%patch3 -p1 -b .dist_pkcs11

libtoolize -c -f; aclocal -I libtool.m4 --force; autoconf -f

%build
./configure \
    --prefix=%{_prefix} \
    --with-python=python3 \
    --with-libtool \
    --localstatedir=%{_var} \
    --disable-static \
    --includedir=%{_includedir}/bind9 \
    --enable-native-pkcs11 \
    --with-lmdb=yes \
    --without-libjson --with-json-c \
    --enable-fixed-rrset \
    --with-docbook-xsl=%{_datadir}/sgml/docbook/xsl-ns-stylesheets \
    --enable-full-report \

%make_build

%install
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_libdir}/{bind,named}
mkdir -p %{buildroot}%{_localstatedir}/named/{slaves,data,dynamic}
mkdir -p %{buildroot}%{_mandir}/{man1,man5,man8}
mkdir -p %{buildroot}/run/named

#chroot
for D in %{chroot_create_directories}
do
  mkdir -p %{buildroot}/%{chroot_prefix}${D}
done

# create symlink as it is on real filesystem
pushd %{buildroot}/%{chroot_prefix}%{_var}
ln -s ../run run
popd

# these are required to prevent them being erased during upgrade of previous
touch %{buildroot}/%{chroot_prefix}%{_sysconfdir}/named.conf
#end chroot

%make_install

mkdir -p  %{buildroot}%{_libexecdir}
install -m 755 %{SOURCE11} %{buildroot}%{_libexecdir}/setup-named-chroot.sh
install -m 755 %{SOURCE12} %{buildroot}%{_libexecdir}/generate-rndc-key.sh

install -m 755 %{SOURCE14} %{buildroot}%{_libexecdir}/setup-named-softhsm.sh

install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/named
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/named
install -m 644 %{SOURCE15} %{buildroot}%{_sysconfdir}/named-chroot.files

# Install isc/errno2result.h header
install -m 644 lib/isc/unix/errno2result.h %{buildroot}%{_includedir}/bind9/isc

# Files required to run test-suite outside of build tree:
cp -fp config.h %{buildroot}%{_includedir}/bind9

# Remove libtool .la files:
find %{buildroot} -type f -name "*.la" -delete -print

# PKCS11 versions manpages
pushd %{buildroot}%{_mandir}/man8
ln -s named.8.gz named-pkcs11.8.gz
ln -s dnssec-checkds.8.gz dnssec-checkds-pkcs11.8.gz
ln -s dnssec-dsfromkey.8.gz dnssec-dsfromkey-pkcs11.8.gz
ln -s dnssec-importkey.8.gz dnssec-importkey-pkcs11.8.gz
ln -s dnssec-keyfromlabel.8.gz dnssec-keyfromlabel-pkcs11.8.gz
ln -s dnssec-keygen.8.gz dnssec-keygen-pkcs11.8.gz
ln -s dnssec-revoke.8.gz dnssec-revoke-pkcs11.8.gz
ln -s dnssec-settime.8.gz dnssec-settime-pkcs11.8.gz
ln -s dnssec-signzone.8.gz dnssec-signzone-pkcs11.8.gz
ln -s dnssec-verify.8.gz dnssec-verify-pkcs11.8.gz
popd

# configuration files:
touch %{buildroot}%{_sysconfdir}/rndc.{key,conf}
install -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/named.root.key
install -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/trusted-key.key
mkdir -p %{buildroot}%{_sysconfdir}/named

# data files:
mkdir -p %{buildroot}%{_localstatedir}/named
install -m 640 %{SOURCE3} %{buildroot}%{_localstatedir}/named/named.ca
install -m 640 %{SOURCE4} %{buildroot}%{_localstatedir}/named/named.localhost
install -m 640 %{SOURCE5} %{buildroot}%{_localstatedir}/named/named.loopback
install -m 640 %{SOURCE6} %{buildroot}%{_localstatedir}/named/named.empty
install -m 640 %{SOURCE7} %{buildroot}%{_sysconfdir}/named.rfc1912.zones

mkdir -p %{buildroot}/%{_tmpfilesdir}
cat << EOF >> %{buildroot}/%{_sysconfdir}/named.conf
zone "." in {
    type master;
    allow-update {none;}; // no DDNS by default
};
EOF
echo "d /run/named 0755 named named - -" > %{buildroot}/%{_tmpfilesdir}/named.conf

# sample bind configuration files for %%doc:
mkdir -p sample/etc sample/var/named/{data,slaves}
install -m 644 %{SOURCE8} sample/etc/named.conf
# Copy default configuration to %%doc to make it usable from system-config-bind
cp %{buildroot}/%{_tmpfilesdir}/named.conf named.conf.default
install -m 644 %{SOURCE7} sample/etc/named.rfc1912.zones
install -m 644 %{SOURCE4} %{SOURCE5} %{SOURCE6}  sample/var/named
install -m 644 %{SOURCE3} sample/var/named/named.ca
for f in my.internal.zone.db slaves/my.slave.internal.zone.db slaves/my.ddns.internal.zone.db my.external.zone.db; do
  echo '@ in soa localhost. root 1 3H 15M 1W 1D
  ns localhost.' > sample/var/named/$f;
done
:;

mkdir -p %{buildroot}%{_sysconfdir}/rwtab.d
install -m 644 %{SOURCE13} %{buildroot}%{_sysconfdir}/rwtab.d/named

# Remove unwanted files
rm -f %{buildroot}%{_prefix}%{_sysconfdir}/bind.keys

%pre
if ! getent group named >/dev/null; then
    groupadd -r named
fi
if ! getent passwd named >/dev/null; then
    useradd -g named -d %{_sharedstatedir}/bind\
        -s /bin/false -M -r named
fi

%post -p /sbin/ldconfig
%postun
/sbin/ldconfig
if getent passwd named >/dev/null; then
    userdel named
fi
if getent group named >/dev/null; then
    groupdel named
fi

# Fix permissions on existing device files on upgrade
%define chroot_fix_devices() \
if [ $1 -gt 1 ]; then \
  for DEV in "%{1}/dev"/{null,random,zero}; do \
    if [ -e "$DEV" -a "$(/bin/stat --printf="%{G} %{a}" "$DEV")" = "root 644" ]; \
    then \
      /bin/chmod 0664 "$DEV" \
      /bin/chgrp named "$DEV" \
    fi \
  done \
fi
Vendor:         Microsoft Corporation
Distribution:   Mariner
%ldconfig_scriptlets libs
%ldconfig_scriptlets pkcs11-libs

%post chroot
%chroot_fix_devices %{chroot_prefix}

%posttrans chroot
if [ -x %{_sbindir}/selinuxenabled ] && %{_sbindir}/selinuxenabled; then
  [ -x /sbin/restorecon ] && /sbin/restorecon %{chroot_prefix}/dev/* > /dev/null 2>&1;
fi;

%files
%dir %{_libdir}/bind
%dir %{_libdir}/named
%{_libdir}/named/*.so
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/named
%config(noreplace) %{_sysconfdir}/logrotate.d/named
%{_sbindir}/named-journalprint
%{_sbindir}/named-checkconf
%{_bindir}/named-rrchecker
%{_bindir}/mdig
%{_sbindir}/named
%{_sbindir}/rndc*
%{_libexecdir}/generate-rndc-key.sh
%{_mandir}/man1/mdig.1*
%{_mandir}/man1/named-rrchecker.1*
%{_mandir}/man5/named.conf.5*
%{_mandir}/man5/rndc.conf.5*
%{_mandir}/man8/rndc.8*
%{_mandir}/man8/named.8*
%{_mandir}/man8/named-checkconf.8*
%{_mandir}/man8/rndc-confgen.8*
%{_mandir}/man8/named-journalprint.8*
%{_mandir}/man8/filter-aaaa.8.gz
%doc CHANGES README named.conf.default
%doc sample/

%defattr(0660,root,named,01770)
%dir %{_localstatedir}/named
%defattr(0660,named,named,0770)
%dir %{_localstatedir}/named/slaves
%dir %{_localstatedir}/named/data
%dir %{_localstatedir}/named/dynamic
%ghost %{_localstatedir}/log/named.log
%defattr(0640,root,named,0750)
%config %verify(not link) %{_localstatedir}/named/named.ca
%config %verify(not link) %{_localstatedir}/named/named.localhost
%config %verify(not link) %{_localstatedir}/named/named.loopback
%config %verify(not link) %{_localstatedir}/named/named.empty
%ghost %config(noreplace) %{_sysconfdir}/rndc.key
# ^- rndc.key now created on first install only if it does not exist
%ghost %config(noreplace) %{_sysconfdir}/rndc.conf
# ^- The default rndc.conf which uses rndc.key is in named's default internal config -
# so rndc.conf is not necessary.
%defattr(-,named,named,-)
%dir /run/named

%files libs
%{_libdir}/*-%{version}*.so
%exclude %{_libdir}/libdns-pkcs11*
%exclude %{_libdir}/libns-pkcs11*

%files license
%license LICENSE
%license COPYRIGHT

%files devel
%{_libdir}/libbind9.so
%{_libdir}/libisccc.so
%{_libdir}/libns.so
%{_libdir}/libdns.so
%{_libdir}/libirs.so
%{_libdir}/libisc.so
%{_libdir}/libisccfg.so
%dir %{_includedir}/bind9
%{_includedir}/bind9/config.h
%{_includedir}/bind9/bind9
%{_includedir}/bind9/isccc
%{_includedir}/bind9/ns
%{_includedir}/bind9/dns
%{_includedir}/bind9/dst
%{_includedir}/bind9/irs
%{_includedir}/bind9/isc
%dir %{_includedir}/bind9/pk11
%{_includedir}/bind9/pk11/site.h
%{_includedir}/bind9/isccfg

%files pkcs11
%{_sbindir}/named-pkcs11
%{_mandir}/man8/named-pkcs11.8*
%{_libexecdir}/setup-named-softhsm.sh

%files pkcs11-utils
%{_sbindir}/dnssec*pkcs11
%{_sbindir}/pkcs11-destroy
%{_sbindir}/pkcs11-keygen
%{_sbindir}/pkcs11-list
%{_sbindir}/pkcs11-tokens
%{_mandir}/man8/pkcs11*.8*
%{_mandir}/man8/dnssec*-pkcs11.8*

%files pkcs11-libs
%{_libdir}/libdns-pkcs11*
%{_libdir}/libns-pkcs11*

%files pkcs11-devel
%{_includedir}/bind9/pk11/*.h
%exclude %{_includedir}/bind9/pk11/site.h
%{_includedir}/bind9/pkcs11
%{_libdir}/libdns-pkcs11.so
%{_libdir}/libns-pkcs11.so

%files dnssec-utils
%{_sbindir}/dnssec*
%exclude %{_sbindir}/dnssec*pkcs11

%files dnssec-doc
%{_mandir}/man8/dnssec*.8*
%exclude %{_mandir}/man8/dnssec*-pkcs11.8*

%files -n python3-bind
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/isc/

%files chroot
%config(noreplace) %{_sysconfdir}/named-chroot.files
%{_libexecdir}/setup-named-chroot.sh
%defattr(0664,root,named,-)
%ghost %dev(c,1,3) %verify(not mtime) %{chroot_prefix}/dev/null
%ghost %dev(c,1,8) %verify(not mtime) %{chroot_prefix}/dev/random
%ghost %dev(c,1,9) %verify(not mtime) %{chroot_prefix}/dev/urandom
%ghost %dev(c,1,5) %verify(not mtime) %{chroot_prefix}/dev/zero
%defattr(0640,root,named,0750)
%dir %{chroot_prefix}
%dir %{chroot_prefix}/dev
%dir %{chroot_prefix}%{_sysconfdir}
%dir %{chroot_prefix}%{_sysconfdir}/named
%dir %{chroot_prefix}%{_sysconfdir}/pki
%dir %{chroot_prefix}%{_sysconfdir}/pki/dnssec-keys
%dir %{chroot_prefix}%{_sysconfdir}/crypto-policies
%dir %{chroot_prefix}%{_sysconfdir}/crypto-policies/back-ends
%dir %{chroot_prefix}%{_localstatedir}
%dir %{chroot_prefix}/run
%ghost %config(noreplace) %{chroot_prefix}%{_sysconfdir}/named.conf
%defattr(-,root,root,-)
%dir %{chroot_prefix}%{_prefix}
%dir %{chroot_prefix}/%{_libdir}
%dir %{chroot_prefix}/%{_libdir}/bind
%dir %{chroot_prefix}/%{_datadir}/GeoIP
%defattr(0660,root,named,01770)
%dir %{chroot_prefix}%{_localstatedir}/named
%defattr(0660,named,named,0770)
%dir %{chroot_prefix}%{_localstatedir}/tmp
%dir %{chroot_prefix}%{_localstatedir}/log
%defattr(-,named,named,-)
%dir %{chroot_prefix}/run/named
%{chroot_prefix}%{_localstatedir}/run

%files utils
%defattr(-,root,root)
%{_sbindir}/ddns-confgen
%{_sbindir}/tsig-keygen
%{_sbindir}/nsec3hash
%{_sbindir}/named-checkzone
%{_sbindir}/named-compilezone
%{_sbindir}/named-nzd2nzf
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/ddns-confgen.8*
%{_mandir}/man8/tsig-keygen.8*
%{_mandir}/man8/nsec3hash.8*
%{_mandir}/man8/named-checkzone.8*
%{_mandir}/man8/named-compilezone.8*
%{_mandir}/man8/named-nzd2nzf.8*
%{_sysconfdir}/*
%{_tmpfilesdir}/named.conf

%changelog
* Mon Jun 21 2021 Thomas Crain <thcrain@microsoft.com> - 9.16.15-1
- Update patches for a new version
- Remove unprovided soname version of libraries
- Include versioned library names in libs subpackage
- Merge the following releases from 1.0 to dev branch
- anphel@microsoft.com, 9.16.15-1: Update version to 9.16.15 to fix CVE-2021-25215

* Fri May 14 2021 Thomas Crain <thcrain@microsoft.com> - 9.16.3-5
- Merge the following releases from 1.0 to dev branch
- nicolasg@microsoft.com, 9.16.3-3: Fixes CVE-2020-8625

* Thu May 13 2021 Henry Li <lihl@microsoft.com> - 9.16.3-4
- Fix file path error caused by linting
- Remove duplicate %files section for bind-license
- Remove named.conf from main package, which is already provided by bind-utils

* Mon May 03 2021 Henry Li <lihl@microsoft.com> - 9.16.3-3
- Add bind, bind-devel, bind-libs, bind-license, bind-pkcs11, bind-pkcs11-libs,
  bind-pkcs11-utils, bind-pkcs11-devel, bind-dnssec-utils, bind-dnssec-doc,
  bind-python3-bind and bind-chroot packages

* Fri Sep 11 2020 Ruying Chen <v-ruyche@microsoft.com> - 9.16.3-2
- Fixes CVE-2020-8618, CVE-2020-8619, CVE-2020-8620,
- CVE-2020-8621, CVE-2020-8622, CVE-2020-8623, CVE-2020-8624

* Wed May 27 2020 Daniel McIlvaney <damcilva@microsoft.com> - 9.16.3-1
- Update to version 9.16.3, fixes CVE-2018-5743, CVE-2018-5744, CVE-2019-6465, CVE-2019-6467, CVE-2019-6471, CVE-2020-8616, CVE-2020-8617

* Sat May 09 00:21:20 PST 2020 Nick Samson <nisamson@microsoft.com> - 9.13.3-4
- Added %%license line automatically

* Fri May  1 2020 Emre Girgin <mrgirgin@microsoft.com> - 9.13.3-3
- Renaming bindutils to bind.
- Add bind-utils subpackage.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 9.13.3-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 23 2018 Sujay G <gsujay@vmware.com> - 9.13.3-1
- Bump bindutils version to 9.13.3

* Mon Feb 12 2018 Xiaolin Li <xiaolinl@vmware.com> - 9.10.6-1
- Upgrading version to 9.10.6-P1, fix CVE-2017-3145

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> - 9.10.4-4
- Remove shadow from requires and use explicit tools for post actions

* Fri Apr 14 2017 Kumar Kaushik <kaushikk@vmware.com> - 9.10.4-3
- Upgrading version to 9.10.4-P8

* Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 9.10.4-2
- add shadow to requires

* Mon Jun 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 9.10.4-1
- Upgraded the version to 9.10.4

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 9.10.3-3
- GA - Bump release of all rpms

* Fri Apr 29 2016 Xiaolin Li <xiaolinl@vmware.com> - 9.10.3-2
- Add group named and user named

* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> - 9.10.3-1
- Updated to version 9.10.3

* Tue Aug 11 2015 Divya Thaluru <dthaluru@vmware.com> - 9.10.1-1
- Fixing release

* Tue Jan 20 2015 Divya Thaluru <dthaluru@vmware.com> - 9.10.1-P1
- Initial build. First version
