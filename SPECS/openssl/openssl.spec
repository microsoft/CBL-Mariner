# Don't depend on bash by default
%define __requires_exclude ^/(bin|usr/bin).*$
%define soversion 1.1
Summary:        Utilities from the general purpose cryptography library with TLS implementation
Name:           openssl
Version:        1.1.1k
Release:        3%{?dist}
License:        OpenSSL
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.openssl.org/
# We have to remove certain patented algorithms from the openssl source
# tarball with the hobble-openssl script which is included below.
# The original openssl upstream tarball cannot be shipped in the .src.rpm.
Source0:        %{name}-%{version}-hobbled.tar.xz
Source1:        hobble-openssl
Source2:        ec_curve.c
Source3:        ectest.c
Source4:        ideatest.c
Patch0:         openssl-1.1.1-no-html.patch
# CVE only applies when Apache HTTP Server version 2.4.37 or less.
Patch1:         CVE-2019-0190.nopatch
Patch2:         0001-Replacing-deprecated-functions-with-NULL-or-highest.patch
Patch3:         openssl-1.1.1-ec-curves.patch
Patch4:         openssl-1.1.1-no-brainpool.patch
Patch5:         openssl-1.1.1-fips.patch
Patch6:         openssl-1.1.1-version-override.patch
Patch7:         openssl-1.1.1-seclevel.patch
Patch8:         openssl-1.1.1-fips-post-rand.patch
Patch9:         openssl-1.1.1-evp-kdf.patch
Patch10:        openssl-1.1.1-ssh-kdf.patch
Patch11:        openssl-1.1.1-krb5-kdf.patch
Patch12:        openssl-1.1.1-edk2-build.patch
Patch13:        openssl-1.1.1-fips-crng-test.patch
Patch14:        openssl-1.1.1-fips-drbg-selftest.patch
Patch15:        openssl-1.1.1-fips-dh.patch
Patch16:        openssl-1.1.1-s390x-ecc.patch
Patch17:        openssl-1.1.1-kdf-selftest.patch
Patch18:        openssl-1.1.1-fips-curves.patch
Patch19:        openssl-1.1.1-sp80056arev3.patch
Patch20:        openssl-1.1.1-jitterentropy.patch
BuildRequires:  perl-Test-Warnings
BuildRequires:  perl-Text-Template
Requires:       %{name}-libs = %{version}-%{release}
Requires:       glibc
Requires:       libgcc
Conflicts:      httpd <= 2.4.37

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package libs
Summary:        A general purpose cryptography library with TLS implementation
Group:          System Environment/Libraries

%description libs
OpenSSL is a toolkit for supporting cryptography. The openssl-libs
package contains the libraries that are used by various applications which
support cryptographic algorithms and protocols.

%package devel
Summary:        Development Libraries for openssl
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       openssl = %{version}-%{release}

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%package static
Summary:        Libraries for static linking of applications which will use OpenSSL
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description static
OpenSSL is a toolkit for supporting cryptography. The openssl-static
package contains static libraries needed for static linking of
applications which support various cryptographic algorithms and
protocols.

%package perl
Summary:        Perl scripts provided with OpenSSL
Group:          Applications/Internet
Requires:       openssl = %{version}-%{release}
Requires:       perl-interpreter

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%prep
%setup -q

# The hobble_openssl is called here redundantly, just to be sure.
# The tarball has already the sources removed.
%{SOURCE1} > /dev/null

cp %{SOURCE2} crypto/ec/
cp %{SOURCE3} test/
cp %{SOURCE4} test/

%patch0  -p1
%patch2  -p1
%patch3  -p1
%patch4  -p1
%patch5  -p1
%patch6  -p1
%patch7  -p1
%patch8  -p1
%patch9  -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1

%build
# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
# Also add -O0 to enable optimization, which is needed for jitterentropy
NEW_RPM_OPT_FLAGS="%{optflags} -Wa,--noexecstack -Wa,--generate-missing-build-notes=yes -DPURIFY $RPM_LD_FLAGS -O0"

export HASHBANGPERL=%{_bindir}/perl

# The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.

# See https://wiki.openssl.org/index.php/Compilation_and_Installation for configure options

# NOTE: the 'no-<prot>-method' switches are not used by design. The changes inside 'Patch2'
#       make sure that protocols disabled through 'no-<prot>' will still be unaccessible.
#       This is a workaround until OpenSSL issue #7048 is officially resolved.
#       Issue link: https://github.com/openssl/openssl/issues/7048.
#       For more details please read the comment inside the patch.
./config \
    --prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls --libdir=lib \
    shared \
    no-aria \
    enable-bf \
    no-blake2 \
    enable-camellia \
    no-capieng \
    enable-cast \
    no-chacha \
    enable-cms \
    no-comp \
    enable-ct \
    enable-deprecated \
    enable-des \
    enable-dh \
    enable-dsa \
    no-dtls1 \
    no-ec2m \
    enable-ec_nistp_64_gcc_128 \
    enable-ecdh \
    enable-ecdsa \
    no-gost \
    no-idea \
    no-mdc2 \
    no-md2 \
    enable-md4 \
    no-poly1305 \
    enable-rc2 \
    enable-rc4 \
    enable-rc5 \
    no-rfc3779 \
    enable-rmd160 \
    no-sctp \
    no-seed \
    no-siphash \
    no-sm2 \
    no-sm3 \
    no-sm4 \
    no-ssl \
    no-ssl3 \
    no-tls1 \
    no-tls1_1 \
    no-weak-ssl-ciphers \
    no-whirlpool \
    no-zlib \
    no-zlib-dynamic \
    $NEW_RPM_OPT_FLAGS \
    '-DDEVRANDOM="\"/dev/urandom\""'

perl ./configdata.pm -d

make all

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done

# Add generation of HMAC checksum of the final stripped library
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %__os_install_post \
    crypto/fips/fips_standalone_hmac %{buildroot}%{_libdir}/libcrypto.so.%{version} >%{buildroot}%{_libdir}/.libcrypto.so.%{version}.hmac \
    ln -sf .libcrypto.so.%{version}.hmac %{buildroot}%{_libdir}/.libcrypto.so.%{soversion}.hmac \
    crypto/fips/fips_standalone_hmac %{buildroot}%{_libdir}/libssl.so.%{version} >%{buildroot}%{_libdir}/.libssl.so.%{version}.hmac \
    ln -sf .libssl.so.%{version}.hmac %{buildroot}%{_libdir}/.libssl.so.%{soversion}.hmac \
%{nil}

%check
make test

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
install -d %{buildroot}{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl,%{_pkgdocdir}}
make DESTDIR=%{buildroot} MANDIR=%{_mandir} MANSUFFIX=ssl install
rename so.%{soversion} so.%{version} %{buildroot}%{_libdir}/*.so.%{soversion}
for lib in %{buildroot}%{_libdir}/*.so.%{version} ; do
	chmod 755 ${lib}
	ln -s -f `basename ${lib}` %{buildroot}%{_libdir}/`basename ${lib} .%{version}`
	ln -s -f `basename ${lib}` %{buildroot}%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
done
mkdir -p %{buildroot}%{_sysconfdir}/pki/tls/certs

# Move runable perl scripts to bindir
mv %{buildroot}%{_sysconfdir}/pki/tls/misc/*.pl %{buildroot}%{_bindir}
mv %{buildroot}%{_sysconfdir}/pki/tls/misc/tsget %{buildroot}%{_bindir}

# Rename man pages so that they don't conflict with other system man pages.
pushd %{buildroot}%{_mandir}
ln -s -f config.5 man5/openssl.cnf.5
for manpage in man*/* ; do
	if [ -L ${manpage} ]; then
		TARGET=`ls -l ${manpage} | awk '{ print $NF }'`
		ln -snf ${TARGET}ssl ${manpage}ssl
		rm -f ${manpage}
	else
		mv ${manpage} ${manpage}ssl
	fi
done
for conflict in passwd rand ; do
	rename ${conflict} ssl${conflict} man*/${conflict}*
# Fix dangling symlinks
	manpage=man1/openssl-${conflict}.*
	if [ -L ${manpage} ] ; then
		ln -snf ssl${conflict}.1ssl ${manpage}
	fi
done
popd

mkdir -m755 %{buildroot}%{_sysconfdir}/pki/CA
mkdir -m700 %{buildroot}%{_sysconfdir}/pki/CA/private
mkdir -m755 %{buildroot}%{_sysconfdir}/pki/CA/certs
mkdir -m755 %{buildroot}%{_sysconfdir}/pki/CA/crl
mkdir -m755 %{buildroot}%{_sysconfdir}/pki/CA/newcerts

rm -f %{buildroot}%{_sysconfdir}/pki/tls/openssl.cnf.dist
rm -f %{buildroot}%{_sysconfdir}/pki/tls/ct_log_list.cnf.dist

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc FAQ NEWS README README.FIPS
%{_bindir}/openssl
%{_mandir}/man1*/*
%{_mandir}/man5*/*
%{_mandir}/man7*/*
%exclude %{_mandir}/man1*/*.pl*
%exclude %{_mandir}/man1*/tsget*
%exclude %{_mandir}/man1*/openssl-tsget*

%files libs
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%dir %{_sysconfdir}/pki/tls/misc
%dir %{_sysconfdir}/pki/tls/private
%config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf
%config(noreplace) %{_sysconfdir}/pki/tls/ct_log_list.cnf
%attr(0755,root,root) %{_libdir}/*.so*
%attr(0755,root,root) %{_libdir}/engines-%{soversion}
%attr(0644,root,root) %{_libdir}/.libcrypto.so.*.hmac
%attr(0644,root,root) %{_libdir}/.libssl.so.*.hmac

%files devel
%doc CHANGES doc/dir-locals.example.el doc/openssl-c-indent.el
%{_includedir}/openssl
%{_mandir}/man3*/*
%{_libdir}/pkgconfig/*.pc

%files static
%{_libdir}/*.a

%files perl
%{_bindir}/c_rehash
%{_bindir}/*.pl
%{_bindir}/tsget
%{_mandir}/man1*/*.pl*
%{_mandir}/man1*/tsget*
%{_mandir}/man1*/openssl-tsget*
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/CA/certs
%dir %{_sysconfdir}/pki/CA/crl
%dir %{_sysconfdir}/pki/CA/newcerts

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%clean
rm -rf %{buildroot}


%changelog
* Mon Jun 21 2021 Thomas Crain <thcrain@microsoft.com> - 1.1.1k-3
- Merge the following releases from 1.0 to the dev spec:
- niontive@microsoft.com, 1.1.1k-2: Remove FIPS DRBG rewire patch
- niontive@microsoft.com, 1.1.1k-3: In FIPS mode, use only jitterentropy

* Fri Apr 02 2021 Thomas Crain <thcrain@microsoft.com> - 1.1.1k-2
- Merge the following releases from dev to 1.0 spec
- joschmit@microsoft.com, 1.1.1g-7: Use new perl package names.

* Mon Mar 29 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.1.1k-1
- Update to version 1.1.1k

* Tue Mar 23 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.1.1g-15
- Patch CVE-2021-3449 and CVE-2021-3450

* Wed Mar 17 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.1.1g-14
- Fix bugs in SP800-56a Rev.3 patch, including oridinal test

* Thu Mar 11 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.1.1g-13
- Add changes for SP800-56a rev. 3 compliance

* Wed Feb 03 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.1.1g-12
- Apply FIPS patches from CentOS 8.

* Wed Jan 13 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.1.1g-11
- Add ec-curves and no-brainpool patches from Fedora to fix ecdsa and ssl_new tests.

* Fri Jan 08 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.1.1g-10
- Remove source code and support for EC2M.
- Remove source code for IDEA.
- Use "hobbled" tarball

* Thu Dec 10 2020 Mateusz Malisz <mamalisz@microsoft.com> - 1.1.1g-9
- Remove binaries (such as bash) from requires list

* Wed Dec 09 2020 Joe Schmitt <joschmit@microsoft.com> - 1.1.1g-8
- Patch CVE-2020-1971.

* Tue Nov 10 2020 Johnson George <johgeorg@microsoft.com> - 1.1.1g-7
- Updated the config option to enable package test

* Tue Jul 28 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.1g-6
- Replacing removal of functions through the 'no-<prot>-method' option
  with returning a method negotiating the highest supported protocol
  version for TLS and NULL for SSLv3 in order to prevent
  link-time breaks from dependent binaries.

* Thu Jun 11 2020 Joe Schmitt <joschmit@microsoft.com> - 1.1.1g-5
- Enable RC2 ciphers in config settings.

* Wed Apr 29 2020 Paul Monson <paulmon@microsoft.com> - 1.1.1g-4
- Update config settings.

* Tue Apr 21 2020 Paul Monson <paulmon@microsoft.com> - 1.1.1g-3
- Update to OpenSSL 1.1.1g.
- Accidently skipped releases 1 and 2.

* Mon Apr 06 2020 Andrew Phelps <anphel@microsoft.com> - 1.1.1d-3
- Fix Source0 URL

* Sun Apr 05 2020 Paul Monson <paulmon@microsoft.com> - 1.1.1d-2
- Removing ca-certificates to break a circular dependency

* Tue Mar 03 2020 Paul Monson <paulmon@microsoft.com> - 1.1.1d-1
- Initial CBL-Mariner import from Fedora 27 (license: MIT).
- License verified.

* Thu Oct  3 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1d-2
- re-enable the stitched AES-CBC-SHA implementations
- make AES-GCM work in FIPS mode again
- enable TLS-1.2 AES-CCM ciphers in FIPS mode
- fix openssl speed errors in FIPS mode

* Fri Sep 13 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1d-1
- update to the 1.1.1d release

* Fri Sep  6 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1c-6
- upstream fix for status request extension non-compliance (#1737471)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1c-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1c-4
- do not try to use EC groups disallowed in FIPS mode
  in TLS
- fix Valgrind regression with constant-time code

* Mon Jun  3 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1c-3
- add upstream patch to defer sending KeyUpdate after
  pending writes are complete

* Thu May 30 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1c-2
- fix use of uninitialized memory

* Wed May 29 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1c-1
- update to the 1.1.1c release

* Fri May 10 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1b-10
- Another attempt at the AES-CCM regression fix

* Fri May 10 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1b-9
- Fix two small regressions
- Change the ts application default hash to SHA256

* Tue May  7 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1b-8
- FIPS compliance fixes

* Mon May  6 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1b-7
- add S390x chacha20-poly1305 assembler support from master branch

* Fri May  3 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1b-6
- apply new bugfixes from upstream 1.1.1 branch

* Tue Apr 16 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1b-5
- fix for BIO_get_mem_ptr() regression in 1.1.1b (#1691853)

* Wed Mar 27 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1b-4
- drop unused BuildRequires and Requires in the -devel subpackage

* Fri Mar 15 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1b-3
- fix regression in EVP_PBE_scrypt() (#1688284)
- fix incorrect help message in ca app (#1553206)

* Fri Mar  1 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1b-2
- use .include = syntax in the config file to allow it
  to be parsed by 1.0.2 version (#1668916)

* Thu Feb 28 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1b-1
- update to the 1.1.1b release
- EVP_KDF API backport from master
- SSH KDF implementation for EVP_KDF API backport from master

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Tomáš Mráz <tmraz@redhat.com> - 1.1.1a-1
- update to the 1.1.1a release

* Fri Nov  9 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-7
- use /dev/urandom for seeding the RNG in FIPS POST

* Fri Oct 12 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-6
- fix SECLEVEL 3 support
- fix some issues found in Coverity scan

* Thu Sep 27 2018 Charalampos Stratakis <cstratak@redhat.com> - 1:1.1.1-5
- Correctly invoke sed for defining OPENSSL_NO_SSL3

* Thu Sep 27 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-4
- define OPENSSL_NO_SSL3 so the newly built dependencies do not
  have access to SSL3 API calls anymore

* Mon Sep 17 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-3
- reinstate accidentally dropped patch for weak ciphersuites

* Fri Sep 14 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-2
- for consistent support of security policies we build
  RC4 support in TLS (not default) and allow SHA1 in SECLEVEL 2

* Thu Sep 13 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-1
- update to the final 1.1.1 version

* Thu Sep  6 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-0.pre9.3
- do not try to initialize RNG in cleanup if it was not initialized
  before (#1624554)
- use only /dev/urandom if getrandom() is not available
- disable SM4

* Wed Aug 29 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-0.pre9.2
- fix dangling symlinks to manual pages
- make SSLv3_method work

* Wed Aug 22 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-0.pre9.1
- update to the latest 1.1.1 beta version

* Mon Aug 13 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-0.pre8.4
- bidirectional shutdown fixes from upstream

* Mon Aug 13 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-0.pre8.3
- do not put error on stack when using fixed protocol version
  with the default config (#1615098)

* Fri Jul 27 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-0.pre8.2
- load crypto policy config file from the default config

* Wed Jul 25 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-0.pre8
- update to the latest 1.1.1 beta version

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.0h-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.0h-5
- fix FIPS RSA key generation failure

* Mon Jun  4 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.0h-4
- ppc64le is not multilib arch (#1584994)

* Tue Apr  3 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.0h-3
- fix regression of c_rehash (#1562953)

* Thu Mar 29 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.0h-2
- fix FIPS symbol versions

* Thu Mar 29 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.0h-1
- update to upstream version 1.1.0h
- add Recommends for openssl-pkcs11

* Fri Feb 23 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.0g-6
- one more try to apply RPM_LD_FLAGS properly (#1541033)
- dropped unneeded starttls xmpp patch (#1417017)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.0g-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb  1 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.0g-4
- apply RPM_LD_FLAGS properly (#1541033)

* Thu Jan 11 2018 Tomáš Mráz <tmraz@redhat.com> - 1.1.0g-3
- silence the .rnd write failure as that is auxiliary functionality (#1524833)

* Thu Dec 14 2017 Tomáš Mráz <tmraz@redhat.com> - 1.1.0g-2
- put the Makefile.certificate in pkgdocdir and drop the requirement on make

* Fri Nov  3 2017 Tomáš Mráz <tmraz@redhat.com> - 1.1.0g-1
- update to upstream version 1.1.0g

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.0f-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.0f-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Tomáš Mráz <tmraz@redhat.com> - 1:1.1.0f-7
- make s_client and s_server work with -ssl3 option (#1471783)

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 1:1.1.0f-6
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Mon Jun 26 2017 Tomáš Mráz <tmraz@redhat.com> - 1.1.0f-5
- disable verification of all insecure hashes

* Fri Jun 23 2017 Tomáš Mráz <tmraz@redhat.com> - 1.1.0f-4
- make DTLS work (#1462541)

* Thu Jun 15 2017 Tomáš Mráz <tmraz@redhat.com> - 1.1.0f-3
- enable 3DES SSL ciphersuites, RC4 is kept disabled (#1453066)

* Mon Jun  5 2017 Tomáš Mráz <tmraz@redhat.com> - 1.1.0f-2
- only release thread-local key if we created it (from upstream) (#1458775)

* Fri Jun  2 2017 Tomáš Mráz <tmraz@redhat.com> - 1.1.0f-1
- update to upstream version 1.1.0f
- SRP and GOST is now allowed, note that GOST support requires
  adding GOST engine which is not part of openssl anymore

* Thu Feb 16 2017 Tomáš Mráz <tmraz@redhat.com> - 1.1.0e-1
- update to upstream version 1.1.0e
- add documentation of the PROFILE=SYSTEM special cipher string (#1420232)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.0d-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb  1 2017 Tomáš Mráz <tmraz@redhat.com> - 1.1.0d-2
- applied upstream fixes (fix regression in X509_CRL_digest)

* Thu Jan 26 2017 Tomáš Mráz <tmraz@redhat.com> - 1.1.0d-1
- update to upstream version 1.1.0d

* Thu Dec 22 2016 Tomáš Mráz <tmraz@redhat.com> - 1.1.0c-5
- preserve new line in fd BIO BIO_gets() as other BIOs do

* Fri Dec  2 2016 Tomáš Mráz <tmraz@redhat.com> - 1.1.0c-4
- FIPS mode fixes for TLS

* Wed Nov 30 2016 Tomáš Mráz <tmraz@redhat.com> - 1.1.0c-3
- revert SSL_read() behavior change - patch from upstream (#1394677)
- fix behavior on client certificate request in renegotiation (#1393579)

* Tue Nov 22 2016 Tomáš Mráz <tmraz@redhat.com> - 1.1.0c-2
- EC curve NIST P-224 is now allowed, still kept disabled in TLS due
  to less than optimal security

* Fri Nov 11 2016 Tomáš Mráz <tmraz@redhat.com> - 1.1.0c-1
- update to upstream version 1.1.0c

* Fri Nov  4 2016 Tomáš Mráz <tmraz@redhat.com> - 1.1.0b-4
- use a random seed if the supplied one did not generate valid
  parameters in dsa_builtin_paramgen2()

* Wed Oct 12 2016 Tomáš Mráz <tmraz@redhat.com> - 1.1.0b-3
- do not break contract on return value when using dsa_builtin_paramgen2()

* Wed Oct 12 2016 Tomáš Mráz <tmraz@redhat.com> - 1.1.0b-2
- fix afalg failure on big endian

* Tue Oct 11 2016 Tomáš Mráz <tmraz@redhat.com> - 1.1.0b-1
- update to upstream version 1.1.0b

* Fri Oct 07 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.2j-2
- Add flags for riscv64.

* Mon Sep 26 2016 Tomáš Mráz <tmraz@redhat.com> - 1.0.2j-1
- minor upstream release 1.0.2j fixing regression from previous release

* Sat Sep 24 2016 David Woodhouse <dwmw2@infradead.org> - 1.0.2i-2
- Fix enginesdir in libcrypto.c (#1375361)

* Thu Sep 22 2016 Tomáš Mráz <tmraz@redhat.com> - 1.0.2i-1
- minor upstream release 1.0.2i fixing security issues
- move man pages for perl based scripts to perl subpackage (#1377617)

* Wed Aug 10 2016 Tomáš Mráz <tmraz@redhat.com> - 1.0.2h-3
- fix regression in Cisco AnyConnect VPN support (#1354588)

* Mon Jun 27 2016 Tomáš Mráz <tmraz@redhat.com> - 1.0.2h-2
- require libcrypto in libssl.pc (#1301301)

* Tue May  3 2016 Tomáš Mráz <tmraz@redhat.com> - 1.0.2h-1
- minor upstream release 1.0.2h fixing security issues

* Tue Mar 29 2016 Tomáš Mráz <tmraz@redhat.com> - 1.0.2g-4
- disable SSLv2 support altogether (without ABI break)

* Mon Mar  7 2016 Tom Callaway <spot@fedoraproject.org> - 1.0.2g-3
- enable RC5

* Wed Mar  2 2016 Tomáš Mráz <tmraz@redhat.com> - 1.0.2g-2
- reenable SSL2 in the build to avoid ABI break (it does not
  make the openssl vulnerable to DROWN attack)

* Tue Mar  1 2016 Tomáš Mráz <tmraz@redhat.com> - 1.0.2g-1
- minor upstream release 1.0.2g fixing security issues

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.2f-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Tomáš Mráz <tmraz@redhat.com> - 1.0.2f-1
- minor upstream release 1.0.2f fixing security issues
- add support for MIPS secondary architecture

* Fri Jan 15 2016 Tomáš Mráz <tmraz@redhat.com> - 1.0.2e-5
- document some options of openssl speed command

* Fri Dec 18 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.2e-4
- enable sctp support in DTLS

* Tue Dec  8 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.2e-3
- remove unimplemented EC method from header (#1289599)

* Mon Dec  7 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.2e-2
- the fast nistp implementation works only on little endian architectures

* Fri Dec  4 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.2e-1
- minor upstream release 1.0.2e fixing moderate severity security issues
- enable fast assembler implementation for NIST P-256 and P-521
  elliptic curves (#1164210)
- filter out unwanted link options from the .pc files (#1257836)
- do not set serial to 0 in Makefile.certificate (#1135719)

* Mon Nov 16 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.2d-3
- fix sigill on some AMD CPUs (#1278194)

* Wed Aug 12 2015 Tom Callaway <spot@fedoraproject.org> - 1.0.2d-2
- re-enable secp256k1 (bz1021898)

* Thu Jul  9 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.2d-1
- minor upstream release 1.0.2d fixing a high severity security issue

* Tue Jul  7 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.2c-3
- fix the aarch64 build

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.2c-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.2c-1
- minor upstream release 1.0.2c fixing multiple security issues

* Thu May  7 2015 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.2a-4
- Add aarch64 sslarch details

* Thu May  7 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.2a-3
- fix some 64 bit build targets

* Tue Apr 28 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.2a-2
- add alternative certificate chain discovery support from upstream

* Thu Apr 23 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.2a-1
- rebase to 1.0.2 branch

* Thu Apr  9 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.1k-7
- drop the AES-GCM restriction of 2^32 operations because the IV is
  always 96 bits (32 bit fixed field + 64 bit invocation field)

* Thu Mar 19 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.1k-6
- fix CVE-2015-0209 - potential use after free in d2i_ECPrivateKey()
- fix CVE-2015-0286 - improper handling of ASN.1 boolean comparison
- fix CVE-2015-0287 - ASN.1 structure reuse decoding memory corruption
- fix CVE-2015-0289 - NULL dereference decoding invalid PKCS#7 data
- fix CVE-2015-0293 - triggerable assert in SSLv2 server

* Mon Mar 16 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.1k-5
- fix bug in the CRYPTO_128_unwrap()

* Fri Feb 27 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.1k-4
- fix bug in the RFC 5649 support (#1185878)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1:1.0.1k-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Jan 15 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.1k-2
- test in the non-FIPS RSA keygen for minimal distance of p and q
  similarly to the FIPS RSA keygen

* Fri Jan  9 2015 Tomáš Mráz <tmraz@redhat.com> - 1.0.1k-1
- new upstream release fixing multiple security issues

* Thu Nov 20 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1j-3
- disable SSLv3 by default again (mail servers and possibly
  LDAP servers should probably allow it explicitly for legacy
  clients)

* Tue Oct 21 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1j-2
- update the FIPS RSA keygen to be FIPS 186-4 compliant

* Thu Oct 16 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1j-1
- new upstream release fixing multiple security issues

* Fri Oct 10 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1i-5
- copy negotiated digests when switching certs by SNI (#1150032)

* Mon Sep  8 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1i-4
- add support for RFC 5649

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.1i-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1i-2
- drop RSA X9.31 from RSA FIPS selftests
- add Power 8 optimalizations

* Thu Aug  7 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1i-1
- new upstream release fixing multiple moderate security issues
- for now disable only SSLv2 by default

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 1.0.1h-6
- fix license handling

* Mon Jun 30 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1h-5
- disable SSLv2 and SSLv3 protocols by default (can be enabled
  via appropriate SSL_CTX_clear_options() call)

* Wed Jun 11 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1h-4
- use system profile for default cipher list

* Tue Jun 10 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1h-3
- make FIPS mode keygen bit length restriction enforced only when
  OPENSSL_ENFORCE_MODULUS_BITS is set
- fix CVE-2014-0224 fix that broke EAP-FAST session resumption support

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.1h-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun  5 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1h-1
- new upstream release 1.0.1h

* Sat May 31 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.1g-2
- Drop obsolete and irrelevant docs
- Move devel docs to appropriate package

* Wed May  7 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1g-1
- new upstream release 1.0.1g
- do not include ECC ciphersuites in SSLv2 client hello (#1090952)
- fail on hmac integrity check if the .hmac file is empty

* Mon Apr 07 2014 Dennis Gilmore <dennis@ausil.us> - 1.0.1e-44
- pull in upstream patch for CVE-2014-0160
- removed CHANGES file portion from patch for expediency

* Thu Apr  3 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-43
- add support for ppc64le architecture (#1072633)

* Mon Mar 17 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-42
- properly detect encryption failure in BIO
- use 2048 bit RSA key in FIPS selftests

* Fri Feb 14 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-41
- use the key length from configuration file if req -newkey rsa is invoked

* Thu Feb 13 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-40
- print ephemeral key size negotiated in TLS handshake (#1057715)
- add DH_compute_key_padded needed for FIPS CAVS testing

* Thu Feb  6 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-39
- make expiration and key length changeable by DAYS and KEYLEN
  variables in the certificate Makefile (#1058108)
- change default hash to sha256 (#1062325)

* Wed Jan 22 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-38
- make 3des strength to be 128 bits instead of 168 (#1056616)

* Tue Jan  7 2014 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-37
- fix CVE-2013-4353 - Invalid TLS handshake crash
- fix CVE-2013-6450 - possible MiTM attack on DTLS1

* Fri Dec 20 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-36
- fix CVE-2013-6449 - crash when version in SSL structure is incorrect
- more FIPS validation requirement changes

* Wed Dec 18 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-35
- drop weak ciphers from the default TLS ciphersuite list
- add back some symbols that were dropped with update to 1.0.1 branch
- more FIPS validation requirement changes

* Tue Nov 19 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-34
- fix locking and reseeding problems with FIPS drbg

* Fri Nov 15 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-33
- additional changes required for FIPS validation

* Wed Nov 13 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-32
- disable verification of certificate, CRL, and OCSP signatures
  using MD5 if OPENSSL_ENABLE_MD5_VERIFY environment variable
  is not set

* Fri Nov  8 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-31
- add back support for secp521r1 EC curve
- add aarch64 to Configure (#969692)

* Tue Oct 29 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-30
- fix misdetection of RDRAND support on Cyrix CPUS (from upstream) (#1022346)

* Thu Oct 24 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-29
- do not advertise ECC curves we do not support (#1022493)

* Wed Oct 16 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-28
- only ECC NIST Suite B curves support
- drop -fips subpackage

* Mon Oct 14 2013 Tom Callaway <spot@fedoraproject.org> - 1.0.1e-27
- resolve bugzilla 319901 (phew! only took 6 years & 9 days)

* Fri Sep 27 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-26
- make DTLS1 work in FIPS mode
- avoid RSA and DSA 512 bits and Whirlpool in 'openssl speed' in FIPS mode

* Mon Sep 23 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-25
- avoid dlopening libssl.so from libcrypto (#1010357)

* Fri Sep 20 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-24
- fix small memory leak in FIPS aes selftest

* Thu Sep 19 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-23
- fix segfault in openssl speed hmac in the FIPS mode

* Thu Sep 12 2013 Tomáš Mráz <tmraz@redhat.com> - 1.0.1e-22
- document the nextprotoneg option in manual pages
  original patch by Hubert Kario

* Tue Sep 10 2013 Kyle McMartin <kyle@redhat.com> - 1.0.1e-21
- [arm] use elf auxv to figure out armcap.c instead of playing silly
  games with SIGILL handlers. (#1006474)

* Wed Sep  4 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-20
- try to avoid some races when updating the -fips subpackage

* Mon Sep  2 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-19
- use version-release in .hmac suffix to avoid overwrite
  during upgrade

* Thu Aug 29 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-18
- allow deinitialization of the FIPS mode

* Thu Aug 29 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-17
- always perform the FIPS selftests in library constructor
  if FIPS module is installed

* Tue Aug 27 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-16
- add -fips subpackage that contains the FIPS module files

* Fri Aug 16 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-15
- fix use of rdrand if available
- more commits cherry picked from upstream
- documentation fixes

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1:1.0.1e-14
- Perl 5.18 rebuild

* Fri Jul 26 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-13
- additional manual page fix
- use symbol versioning also for the textual version

* Thu Jul 25 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-12
- additional manual page fixes

* Fri Jul 19 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-11
- use _prefix macro

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:1.0.1e-10
- Perl 5.18 rebuild

* Thu Jul 11 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-9
- add openssl.cnf.5 manpage symlink to config.5

* Wed Jul 10 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-8
- add relro linking flag

* Wed Jul 10 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-7
- add support for the -trusted_first option for certificate chain verification

* Fri May  3 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-6
- fix build of manual pages with current pod2man (#959439)

* Sun Apr 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.1e-5
- Enable ARM optimised build

* Mon Mar 18 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-4
- fix random bad record mac errors (#918981)

* Tue Feb 19 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-3
- fix up the SHLIB_VERSION_NUMBER

* Tue Feb 19 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-2
- disable ZLIB loading by default (due to CRIME attack)

* Tue Feb 19 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1e-1
- new upstream version

* Wed Jan 30 2013 Tomas Mraz <tmraz@redhat.com> - 1.0.1c-12
- more fixes from upstream
- fix errors in manual causing build failure (#904777)

* Fri Dec 21 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1c-11
- add script for renewal of a self-signed cert by Philip Prindeville (#871566)
- allow X509_issuer_and_serial_hash() produce correct result in
  the FIPS mode (#881336)

* Thu Dec  6 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1c-10
- do not load default verify paths if CApath or CAfile specified (#884305)

* Tue Nov 20 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1c-9
- more fixes from upstream CVS
- fix DSA key pairwise check (#878597)

* Thu Nov 15 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1c-8
- use 1024 bit DH parameters in s_server as 512 bit is not allowed
  in FIPS mode and it is quite weak anyway

* Mon Sep 10 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1c-7
- add missing initialization of str in aes_ccm_init_key (#853963)
- add important patches from upstream CVS
- use the secure_getenv() with new glibc

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.1c-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1c-5
- use __getenv_secure() instead of __libc_enable_secure

* Fri Jul 13 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1c-4
- do not move libcrypto to /lib
- do not use environment variables if __libc_enable_secure is on
- fix strict aliasing problems in modes

* Thu Jul 12 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1c-3
- fix DSA key generation in FIPS mode (#833866)
- allow duplicate FIPS_mode_set(1)
- enable build on ppc64 subarch (#834652)

* Wed Jul 11 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1c-2
- fix s_server with new glibc when no global IPv6 address (#839031)
- make it build with new Perl

* Tue May 15 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1c-1
- new upstream version

* Thu Apr 26 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1b-1
- new upstream version

* Fri Apr 20 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1a-1
- new upstream version fixing CVE-2012-2110

* Wed Apr 11 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1-3
- add Kerberos 5 libraries to pkgconfig for static linking (#807050)

* Thu Apr  5 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1-2
- backports from upstream CVS
- fix segfault when /dev/urandom is not available (#809586)

* Wed Mar 14 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1-1
- new upstream release

* Mon Mar  5 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1-0.3.beta3
- add obsoletes to assist multilib updates (#799636)

* Wed Feb 29 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1-0.2.beta3
- epoch bumped to 1 due to revert to 1.0.0g on Fedora 17
- new upstream release from the 1.0.1 branch
- fix s390x build (#798411)
- versioning for the SSLeay symbol (#794950)
- add -DPURIFY to build flags (#797323)
- filter engine provides
- split the libraries to a separate -libs package
- add make to requires on the base package (#783446)

* Tue Feb  7 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.1-0.1.beta2
- new upstream release from the 1.0.1 branch, ABI compatible
- add documentation for the -no_ign_eof option

* Thu Jan 19 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.0g-1
- new upstream release fixing CVE-2012-0050 - DoS regression in
  DTLS support introduced by the previous release (#782795)

* Thu Jan  5 2012 Tomas Mraz <tmraz@redhat.com> - 1.0.0f-1
- new upstream release fixing multiple CVEs

* Tue Nov 22 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0e-4
- move the libraries needed for static linking to Libs.private

* Thu Nov  3 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0e-3
- do not use AVX instructions when osxsave bit not set
- add direct known answer tests for SHA2 algorithms

* Wed Sep 21 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0e-2
- fix missing initialization of variable in CHIL engine

* Wed Sep  7 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0e-1
- new upstream release fixing CVE-2011-3207 (#736088)

* Wed Aug 24 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0d-8
- drop the separate engine for Intel acceleration improvements
  and merge in the AES-NI, SHA1, and RC4 optimizations
- add support for OPENSSL_DISABLE_AES_NI environment variable
  that disables the AES-NI support

* Tue Jul 26 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0d-7
- correct openssl cms help output (#636266)
- more tolerant starttls detection in XMPP protocol (#608239)

* Wed Jul 20 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0d-6
- add support for newest Intel acceleration improvements backported
  from upstream by Intel in form of a separate engine

* Thu Jun  9 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0d-5
- allow the AES-NI engine in the FIPS mode

* Tue May 24 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0d-4
- add API necessary for CAVS testing of the new DSA parameter generation

* Thu Apr 28 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0d-3
- add support for VIA Padlock on 64bit arch from upstream (#617539)
- do not return bogus values from load_certs (#652286)

* Tue Apr  5 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0d-2
- clarify apps help texts for available digest algorithms (#693858)

* Thu Feb 10 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0d-1
- new upstream release fixing CVE-2011-0014 (OCSP stapling vulnerability)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0c-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0c-3
- add -x931 parameter to openssl genrsa command to use the ANSI X9.31
  key generation method
- use FIPS-186-3 method for DSA parameter generation
- add OPENSSL_FIPS_NON_APPROVED_MD5_ALLOW environment variable
  to allow using MD5 when the system is in the maintenance state
  even if the /proc fips flag is on
- make openssl pkcs12 command work by default in the FIPS mode

* Mon Jan 24 2011 Tomas Mraz <tmraz@redhat.com> - 1.0.0c-2
- listen on ipv6 wildcard in s_server so we accept connections
  from both ipv4 and ipv6 (#601612)
- fix openssl speed command so it can be used in the FIPS mode
  with FIPS allowed ciphers

* Fri Dec  3 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0c-1
- new upstream version fixing CVE-2010-4180

* Tue Nov 23 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0b-3
- replace the revert for the s390x bignum asm routines with
  fix from upstream

* Mon Nov 22 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0b-2
- revert upstream change in s390x bignum asm routines

* Tue Nov 16 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0b-1
- new upstream version fixing CVE-2010-3864 (#649304)

* Tue Sep  7 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0a-3
- make SHLIB_VERSION reflect the library suffix

* Wed Jun 30 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0a-2
- openssl man page fix (#609484)

* Fri Jun  4 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0a-1
- new upstream patch release, fixes CVE-2010-0742 (#598738)
  and CVE-2010-1633 (#598732)

* Wed May 19 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0-5
- pkgconfig files now contain the correct libdir (#593723)

* Tue May 18 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0-4
- make CA dir readable - the private keys are in private subdir (#584810)

* Fri Apr  9 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0-3
- a few fixes from upstream CVS
- move libcrypto to /lib (#559953)

* Tue Apr  6 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0-2
- set UTC timezone on pod2man run (#578842)
- make X509_NAME_hash_old work in FIPS mode

* Tue Mar 30 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0-1
- update to final 1.0.0 upstream release

* Tue Feb 16 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.22.beta5
- make TLS work in the FIPS mode

* Fri Feb 12 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.21.beta5
- gracefully handle zero length in assembler implementations of
  OPENSSL_cleanse (#564029)
- do not fail in s_server if client hostname not resolvable (#561260)

* Wed Jan 20 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.20.beta5
- new upstream release

* Thu Jan 14 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.19.beta4
- fix CVE-2009-4355 - leak in applications incorrectly calling
  CRYPTO_free_all_ex_data() before application exit (#546707)
- upstream fix for future TLS protocol version handling

* Wed Jan 13 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.18.beta4
- add support for Intel AES-NI

* Thu Jan  7 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.17.beta4
- upstream fix compression handling on session resumption
- various null checks and other small fixes from upstream
- upstream changes for the renegotiation info according to the latest draft

* Mon Nov 23 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.16.beta4
- fix non-fips mingw build (patch by Kalev Lember)
- add IPV6 fix for DTLS

* Fri Nov 20 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.15.beta4
- add better error reporting for the unsafe renegotiation

* Fri Nov 20 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.14.beta4
- fix build on s390x

* Wed Nov 18 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.13.beta4
- disable enforcement of the renegotiation extension on the client (#537962)
- add fixes from the current upstream snapshot

* Fri Nov 13 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.12.beta4
- keep the beta status in version number at 3 so we do not have to rebuild
  openssh and possibly other dependencies with too strict version check

* Thu Nov 12 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.11.beta4
- update to new upstream version, no soname bump needed
- fix CVE-2009-3555 - note that the fix is bypassed if SSL_OP_ALL is used
  so the compatibility with unfixed clients is not broken. The
  protocol extension is also not final.

* Fri Oct 16 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.10.beta3
- fix use of freed memory if SSL_CTX_free() is called before
  SSL_free() (#521342)

* Thu Oct  8 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.9.beta3
- fix typo in DTLS1 code (#527015)
- fix leak in error handling of d2i_SSL_SESSION()

* Wed Sep 30 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.8.beta3
- fix RSA and DSA FIPS selftests
- reenable fixed x86_64 camellia assembler code (#521127)

* Fri Sep  4 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.7.beta3
- temporarily disable x86_64 camellia assembler code (#521127)

* Mon Aug 31 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.6.beta3
- fix openssl dgst -dss1 (#520152)

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.5.beta3
- drop the compat symlink hacks

* Sat Aug 22 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.4.beta3
- constify SSL_CIPHER_description()

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.3.beta3
- fix WWW:Curl:Easy reference in tsget

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.2.beta3
- enable MD-2

* Thu Aug 20 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.0-0.1.beta3
- update to new major upstream release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8k-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Bill Nottingham <notting@redhat.com>
- do not build special 'optimized' versions for i686, as that's the base
  arch in Fedora now

* Tue Jun 30 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8k-6
- abort if selftests failed and random number generator is polled
- mention EVP_aes and EVP_sha2xx routines in the manpages
- add README.FIPS
- make CA dir absolute path (#445344)
- change default length for RSA key generation to 2048 (#484101)

* Thu May 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8k-5
- fix CVE-2009-1377 CVE-2009-1378 CVE-2009-1379
  (DTLS DoS problems) (#501253, #501254, #501572)

* Tue Apr 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8k-4
- support compatibility DTLS mode for CISCO AnyConnect (#464629)

* Fri Apr 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8k-3
- correct the SHLIB_VERSION define

* Wed Apr 15 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8k-2
- add support for multiple CRLs with same subject
- load only dynamic engine support in FIPS mode

* Wed Mar 25 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8k-1
- update to new upstream release (minor bug fixes, security
  fixes and machine code optimizations only)

* Thu Mar 19 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8j-10
- move libraries to /usr/lib (#239375)

* Fri Mar 13 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8j-9
- add a static subpackage

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8j-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8j-7
- must also verify checksum of libssl.so in the FIPS mode
- obtain the seed for FIPS rng directly from the kernel device
- drop the temporary symlinks

* Mon Jan 26 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8j-6
- drop the temporary triggerpostun and symlinking in post
- fix the pkgconfig files and drop the unnecessary buildrequires
  on pkgconfig as it is a rpmbuild dependency (#481419)

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8j-5
- add temporary triggerpostun to reinstate the symlinks

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8j-4
- no pairwise key tests in non-fips mode (#479817)

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8j-3
- even more robust test for the temporary symlinks

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8j-2
- try to ensure the temporary symlinks exist

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.8j-1
- new upstream version with necessary soname bump (#455753)
- temporarily provide symlink to old soname to make it possible to rebuild
  the dependent packages in rawhide
- add eap-fast support (#428181)
- add possibility to disable zlib by setting
- add fips mode support for testing purposes
- do not null dereference on some invalid smime files
- add buildrequires pkgconfig (#479493)

* Sun Aug 10 2008 Tomas Mraz <tmraz@redhat.com> - 0.9.8g-11
- do not add tls extensions to server hello for SSLv3 either

* Mon Jun  2 2008 Joe Orton <jorton@redhat.com> - 0.9.8g-10
- move root CA bundle to ca-certificates package

* Wed May 28 2008 Tomas Mraz <tmraz@redhat.com> - 0.9.8g-9
- fix CVE-2008-0891 - server name extension crash (#448492)
- fix CVE-2008-1672 - server key exchange message omit crash (#448495)

* Tue May 27 2008 Tomas Mraz <tmraz@redhat.com> - 0.9.8g-8
- super-H arch support
- drop workaround for bug 199604 as it should be fixed in gcc-4.3

* Mon May 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.9.8g-7
- sparc handling

* Mon Mar 10 2008 Joe Orton <jorton@redhat.com> - 0.9.8g-6
- update to new root CA bundle from mozilla.org (r1.45)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.8g-5
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Tomas Mraz <tmraz@redhat.com> - 0.9.8g-4
- merge review fixes (#226220)
- adjust the SHLIB_VERSION_NUMBER to reflect library name (#429846)

* Thu Dec 13 2007 Tomas Mraz <tmraz@redhat.com> - 0.9.8g-3
- set default paths when no explicit paths are set (#418771)
- do not add tls extensions to client hello for SSLv3 (#422081)

* Tue Dec  4 2007 Tomas Mraz <tmraz@redhat.com> - 0.9.8g-2
- enable some new crypto algorithms and features
- add some more important bug fixes from openssl CVS

* Mon Dec  3 2007 Tomas Mraz <tmraz@redhat.com> - 0.9.8g-1
- update to latest upstream release, SONAME bumped to 7

* Mon Oct 15 2007 Joe Orton <jorton@redhat.com> - 0.9.8b-17
- update to new CA bundle from mozilla.org

* Fri Oct 12 2007 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-16
- fix CVE-2007-5135 - off-by-one in SSL_get_shared_ciphers (#309801)
- fix CVE-2007-4995 - out of order DTLS fragments buffer overflow (#321191)
- add alpha sub-archs (#296031)

* Tue Aug 21 2007 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-15
- rebuild

* Fri Aug  3 2007 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-14
- use localhost in testsuite, hopefully fixes slow build in koji
- CVE-2007-3108 - fix side channel attack on private keys (#250577)
- make ssl session cache id matching strict (#233599)

* Wed Jul 25 2007 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-13
- allow building on ARM architectures (#245417)
- use reference timestamps to prevent multilib conflicts (#218064)
- -devel package must require pkgconfig (#241031)

* Mon Dec 11 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-12
- detect duplicates in add_dir properly (#206346)

* Thu Nov 30 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-11
- the previous change still didn't make X509_NAME_cmp transitive

* Thu Nov 23 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-10
- make X509_NAME_cmp transitive otherwise certificate lookup
  is broken (#216050)

* Thu Nov  2 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-9
- aliasing bug in engine loading, patch by IBM (#213216)

* Mon Oct  2 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-8
- CVE-2006-2940 fix was incorrect (#208744)

* Mon Sep 25 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-7
- fix CVE-2006-2937 - mishandled error on ASN.1 parsing (#207276)
- fix CVE-2006-2940 - parasitic public keys DoS (#207274)
- fix CVE-2006-3738 - buffer overflow in SSL_get_shared_ciphers (#206940)
- fix CVE-2006-4343 - sslv2 client DoS (#206940)

* Tue Sep  5 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-6
- fix CVE-2006-4339 - prevent attack on PKCS#1 v1.5 signatures (#205180)

* Wed Aug  2 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-5
- set buffering to none on stdio/stdout FILE when bufsize is set (#200580)
  patch by IBM

* Fri Jul 28 2006 Alexandre Oliva <aoliva@redhat.com> - 0.9.8b-4.1
- rebuild with new binutils (#200330)

* Fri Jul 21 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-4
- add a temporary workaround for sha512 test failure on s390 (#199604)

* Thu Jul 20 2006 Tomas Mraz <tmraz@redhat.com>
- add ipv6 support to s_client and s_server (by Jan Pazdziora) (#198737)
- add patches for BN threadsafety, AES cache collision attack hazard fix and
  pkcs7 code memleak fix from upstream CVS

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.9.8b-3.1
- rebuild

* Wed Jun 21 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-3
- dropped libica and ica engine from build

* Wed Jun 21 2006 Joe Orton <jorton@redhat.com>
- update to new CA bundle from mozilla.org; adds CA certificates
  from netlock.hu and startcom.org

* Mon Jun  5 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-2
- fixed a few rpmlint warnings
- better fix for #173399 from upstream
- upstream fix for pkcs12

* Thu May 11 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-1
- upgrade to new version, stays ABI compatible
- there is no more linux/config.h (it was empty anyway)

* Tue Apr  4 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8a-6
- fix stale open handles in libica (#177155)
- fix build if 'rand' or 'passwd' in buildroot path (#178782)
- initialize VIA Padlock engine (#186857)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.9.8a-5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.9.8a-5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Dec 15 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.8a-5
- don't include SSL_OP_NETSCAPE_REUSE_CIPHER_CHANGE_BUG
  in SSL_OP_ALL (#175779)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 29 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.8a-4
- fix build (-lcrypto was erroneusly dropped) of the updated libica
- updated ICA engine to 1.3.6-rc3

* Tue Nov 22 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.8a-3
- disable builtin compression methods for now until they work
  properly (#173399)

* Wed Nov 16 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.8a-2
- don't set -rpath for openssl binary

* Tue Nov  8 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.8a-1
- new upstream version
- patches partially renumbered

* Fri Oct 21 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.7f-11
- updated IBM ICA engine library and patch to latest upstream version

* Wed Oct 12 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.7f-10
- fix CAN-2005-2969 - remove SSL_OP_MSIE_SSLV2_RSA_PADDING which
  disables the countermeasure against man in the middle attack in SSLv2
  (#169863)
- use sha1 as default for CA and cert requests - CAN-2005-2946 (#169803)

* Tue Aug 23 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.7f-9
- add *.so.soversion as symlinks in /lib (#165264)
- remove unpackaged symlinks (#159595)
- fixes from upstream (constant time fixes for DSA,
  bn assembler div on ppc arch, initialize memory on realloc)

* Thu Aug 11 2005 Phil Knirsch <pknirsch@redhat.com> - 0.9.7f-8
- Updated ICA engine IBM patch to latest upstream version.

* Thu May 19 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.7f-7
- fix CAN-2005-0109 - use constant time/memory access mod_exp
  so bits of private key aren't leaked by cache eviction (#157631)
- a few more fixes from upstream 0.9.7g

* Wed Apr 27 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.7f-6
- use poll instead of select in rand (#128285)
- fix Makefile.certificate to point to /etc/pki/tls
- change the default string mask in ASN1 to PrintableString+UTF8String

* Mon Apr 25 2005 Joe Orton <jorton@redhat.com> - 0.9.7f-5
- update to revision 1.37 of Mozilla CA bundle

* Thu Apr 21 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.7f-4
- move certificates to _sysconfdir/pki/tls (#143392)
- move CA directories to _sysconfdir/pki/CA
- patch the CA script and the default config so it points to the
  CA directories

* Fri Apr  1 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.7f-3
- uninitialized variable mustn't be used as input in inline
  assembly
- reenable the x86_64 assembly again

* Thu Mar 31 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.7f-2
- add back RC4_CHAR on ia64 and x86_64 so the ABI isn't broken
- disable broken bignum assembly on x86_64

* Wed Mar 30 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.7f-1
- reenable optimizations on ppc64 and assembly code on ia64
- upgrade to new upstream version (no soname bump needed)
- disable thread test - it was testing the backport of the
  RSA blinding - no longer needed
- added support for changing serial number to
  Makefile.certificate (#151188)
- make ca-bundle.crt a config file (#118903)

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.7e-3
- libcrypto shouldn't depend on libkrb5 (#135961)

* Mon Feb 28 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.7e-2
- rebuild

* Mon Feb 28 2005 Tomas Mraz <tmraz@redhat.com> - 0.9.7e-1
- new upstream source, updated patches
- added patch so we are hopefully ABI compatible with upcoming
  0.9.7f

* Thu Feb 10 2005 Tomas Mraz <tmraz@redhat.com>
- Support UTF-8 charset in the Makefile.certificate (#134944)
- Added cmp to BuildPrereq

* Thu Jan 27 2005 Joe Orton <jorton@redhat.com> - 0.9.7a-46
- generate new ca-bundle.crt from Mozilla certdata.txt (revision 1.32)

* Thu Dec 23 2004 Phil Knirsch <pknirsch@redhat.com> - 0.9.7a-45
- Fixed and updated libica-1.3.4-urandom.patch patch (#122967)

* Fri Nov 19 2004 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-44
- rebuild

* Fri Nov 19 2004 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-43
- rebuild

* Fri Nov 19 2004 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-42
- rebuild

* Fri Nov 19 2004 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-41
- remove der_chop, as upstream cvs has done (CAN-2004-0975, #140040)

* Tue Oct 05 2004 Phil Knirsch <pknirsch@redhat.com> - 0.9.7a-40
- Include latest libica version with important bugfixes

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 14 2004 Phil Knirsch <pknirsch@redhat.com> - 0.9.7a-38
- Updated ICA engine IBM patch to latest upstream version.

* Mon Jun  7 2004 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-37
- build for linux-alpha-gcc instead of alpha-gcc on alpha (Jeff Garzik)

* Tue May 25 2004 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-36
- handle %%{_arch}=i486/i586/i686/athlon cases in the intermediate
  header (#124303)

* Thu Mar 25 2004 Joe Orton <jorton@redhat.com> - 0.9.7a-35
- add security fixes for CAN-2004-0079, CAN-2004-0112

* Tue Mar 16 2004 Phil Knirsch <pknirsch@redhat.com>
- Fixed libica filespec.

* Thu Mar 11 2004 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-34
- ppc/ppc64 define __powerpc__/__powerpc64__, not __ppc__/__ppc64__, fix
  the intermediate header

* Wed Mar 10 2004 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-33
- add an intermediate <openssl/opensslconf.h> which points to the right
  arch-specific opensslconf.h on multilib arches

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Phil Knirsch <pknirsch@redhat.com> - 0.9.7a-32
- Updated libica to latest upstream version 1.3.5.

* Tue Feb 17 2004 Phil Knirsch <pknirsch@redhat.com> - 0.9.7a-31
- Update ICA crypto engine patch from IBM to latest version.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Phil Knirsch <pknirsch@redhat.com> - 0.9.7a-29
- rebuilt

* Wed Feb 11 2004 Phil Knirsch <pknirsch@redhat.com> - 0.9.7a-28
- Fixed libica build.

* Wed Feb  4 2004 Nalin Dahyabhai <nalin@redhat.com>
- add "-ldl" to link flags added for Linux-on-ARM (#99313)

* Wed Feb  4 2004 Joe Orton <jorton@redhat.com> - 0.9.7a-27
- updated ca-bundle.crt: removed expired GeoTrust roots, added
  freessl.com root, removed trustcenter.de Class 0 root

* Sun Nov 30 2003 Tim Waugh <twaugh@redhat.com> - 0.9.7a-26
- Fix link line for libssl (bug #111154).

* Fri Oct 24 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-25
- add dependency on zlib-devel for the -devel package, which depends on zlib
  symbols because we enable zlib for libssl (#102962)

* Fri Oct 24 2003 Phil Knirsch <pknirsch@redhat.com> - 0.9.7a-24
- Use /dev/urandom instead of PRNG for libica.
- Apply libica-1.3.5 fix for /dev/urandom in icalinux.c
- Use latest ICA engine patch from IBM.

* Sat Oct  4 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-22.1
- rebuild

* Wed Oct  1 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-22
- rebuild (22 wasn't actually built, fun eh?)

* Tue Sep 30 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-23
- re-disable optimizations on ppc64

* Tue Sep 30 2003 Joe Orton <jorton@redhat.com>
- add a_mbstr.c fix for 64-bit platforms from CVS

* Tue Sep 30 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-22
- add -Wa,--noexecstack to RPM_OPT_FLAGS so that assembled modules get tagged
  as not needing executable stacks

* Mon Sep 29 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-21
- rebuild

* Thu Sep 25 2003 Nalin Dahyabhai <nalin@redhat.com>
- re-enable optimizations on ppc64

* Thu Sep 25 2003 Nalin Dahyabhai <nalin@redhat.com>
- remove exclusivearch

* Wed Sep 24 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-20
- only parse a client cert if one was requested
- temporarily exclusivearch for %%{ix86}

* Tue Sep 23 2003 Nalin Dahyabhai <nalin@redhat.com>
- add security fixes for protocol parsing bugs (CAN-2003-0543, CAN-2003-0544)
  and heap corruption (CAN-2003-0545)
- update RHNS-CA-CERT files
- ease back on the number of threads used in the threading test

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> - 0.9.7a-19
- rebuild to fix gzipped file md5sums (#91211)

* Mon Aug 25 2003 Phil Knirsch <pknirsch@redhat.com> - 0.9.7a-18
- Updated libica to version 1.3.4.

* Thu Jul 17 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-17
- rebuild

* Tue Jul 15 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-10.9
- free the kssl_ctx structure when we free an SSL structure (#99066)

* Fri Jul 11 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-16
- rebuild

* Thu Jul 10 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-15
- lower thread test count on s390x

* Tue Jul  8 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-14
- rebuild

* Thu Jun 26 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-13
- disable assembly on arches where it seems to conflict with threading

* Thu Jun 26 2003 Phil Knirsch <pknirsch@redhat.com> - 0.9.7a-12
- Updated libica to latest upstream version 1.3.0

* Wed Jun 11 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-9.9
- rebuild

* Wed Jun 11 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-11
- rebuild

* Tue Jun 10 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-10
- ubsec: don't stomp on output data which might also be input data

* Tue Jun 10 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-9
- temporarily disable optimizations on ppc64

* Mon Jun  9 2003 Nalin Dahyabhai <nalin@redhat.com>
- backport fix for engine-used-for-everything from 0.9.7b
- backport fix for prng not being seeded causing problems, also from 0.9.7b
- add a check at build-time to ensure that RSA is thread-safe
- keep perlpath from stomping on the libica configure scripts

* Fri Jun  6 2003 Nalin Dahyabhai <nalin@redhat.com>
- thread-safety fix for RSA blinding

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> - 0.9.7a-8
- rebuilt

* Fri May 30 2003 Phil Knirsch <pknirsch@redhat.com> - 0.9.7a-7
- Added libica-1.2 to openssl (featurerequest).

* Wed Apr 16 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-6
- fix building with incorrect flags on ppc64

* Wed Mar 19 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-5
- add patch to harden against Klima-Pokorny-Rosa extension of Bleichenbacher's
  attack (CAN-2003-0131)

* Mon Mar 17 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-4
- add patch to enable RSA blinding by default, closing a timing attack
  (CAN-2003-0147)

* Wed Mar  5 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-3
- disable use of BN assembly module on x86_64, but continue to allow inline
  assembly (#83403)

* Thu Feb 27 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-2
- disable EC algorithms

* Wed Feb 19 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7a-1
- update to 0.9.7a

* Wed Feb 19 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7-8
- add fix to guard against attempts to allocate negative amounts of memory
- add patch for CAN-2003-0078, fixing a timing attack

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> - 0.9.7-7
- Add openssl-ppc64.patch

* Mon Feb 10 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7-6
- EVP_DecryptInit should call EVP_CipherInit() instead of EVP_CipherInit_ex(),
  to get the right behavior when passed uninitialized context structures
  (#83766)
- build with -mcpu=ev5 on alpha family (#83828)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jan 17 2003 Phil Knirsch <pknirsch@redhat.com> - 0.9.7-4
- Added IBM hw crypto support patch.

* Wed Jan 15 2003 Nalin Dahyabhai <nalin@redhat.com>
- add missing builddep on sed

* Thu Jan  9 2003 Bill Nottingham <notting@redhat.com> - 0.9.7-3
- debloat
- fix broken manpage symlinks

* Wed Jan  8 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7-2
- fix double-free in 'openssl ca'

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7-1
- update to 0.9.7 final

* Tue Dec 17 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.7-0
- update to 0.9.7 beta6 (DO NOT USE UNTIL UPDATED TO FINAL 0.9.7)

* Wed Dec 11 2002 Nalin Dahyabhai <nalin@redhat.com>
- update to 0.9.7 beta5 (DO NOT USE UNTIL UPDATED TO FINAL 0.9.7)

* Tue Oct 22 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-30
- add configuration stanza for x86_64 and use it on x86_64
- build for linux-ppc on ppc
- start running the self-tests again

* Wed Oct 02 2002 Elliot Lee <sopwith@redhat.com> - 0.9.6b-29hammer.3
- Merge fixes from previous hammer packages, including general x86-64 and
  multilib

* Tue Aug  6 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-29
- rebuild

* Thu Aug  1 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-28
- update asn patch to fix accidental reversal of a logic check

* Wed Jul 31 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-27
- update asn patch to reduce chance that compiler optimization will remove
  one of the added tests

* Wed Jul 31 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-26
- rebuild

* Mon Jul 29 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-25
- add patch to fix ASN.1 vulnerabilities

* Thu Jul 25 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-24
- add backport of Ben Laurie's patches for OpenSSL 0.9.6d

* Wed Jul 17 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-23
- own {_datadir}/ssl/misc

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-20
- free ride through the build system (whee!)

* Thu May 16 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-19
- rebuild in new environment

* Thu Apr  4 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-17, 0.9.6b-18
- merge RHL-specific bits into stronghold package, rename

* Tue Apr 02 2002 Gary Benson <gbenson@redhat.com> stronghold-0.9.6c-2
- add support for Chrysalis Luna token

* Tue Mar 26 2002 Gary Benson <gbenson@redhat.com>
- disable AEP random number generation, other AEP fixes

* Fri Mar 15 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-15
- only build subpackages on primary arches

* Thu Mar 14 2002 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-13
- on ia32, only disable use of assembler on i386
- enable assembly on ia64

* Mon Jan  7 2002 Florian La Roche <Florian.LaRoche@redhat.de> - 0.9.6b-11
- fix sparcv9 entry

* Mon Jan  7 2002 Gary Benson <gbenson@redhat.com> stronghold-0.9.6c-1
- upgrade to 0.9.6c
- bump BuildArch to i686 and enable assembler on all platforms
- synchronise with shrimpy and rawhide
- bump soversion to 3

* Wed Oct 10 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- delete BN_LLONG for s390x, patch from Oliver Paukstadt

* Mon Sep 17 2001 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-9
- update AEP driver patch

* Mon Sep 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- adjust RNG disabling patch to match version of patch from Broadcom

* Fri Sep  7 2001 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-8
- disable the RNG in the ubsec engine driver

* Tue Aug 28 2001 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-7
- tweaks to the ubsec engine driver

* Fri Aug 24 2001 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-6
- tweaks to the ubsec engine driver

* Thu Aug 23 2001 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-5
- update ubsec engine driver from Broadcom

* Fri Aug 10 2001 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-4
- move man pages back to %%{_mandir}/man?/foo.?ssl from
  %%{_mandir}/man?ssl/foo.?
- add an [ engine ] section to the default configuration file

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- add a patch for selecting a default engine in SSL_library_init()

* Mon Jul 23 2001 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-3
- add patches for AEP hardware support
- add patch to keep trying when we fail to load a cert from a file and
  there are more in the file
- add missing prototype for ENGINE_ubsec() in engine_int.h

* Wed Jul 18 2001 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-2
- actually add hw_ubsec to the engine list

* Tue Jul 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- add in the hw_ubsec driver from CVS

* Wed Jul 11 2001 Nalin Dahyabhai <nalin@redhat.com> - 0.9.6b-1
- update to 0.9.6b

* Thu Jul  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- move .so symlinks back to %%{_libdir}

* Tue Jul  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- move shared libraries to /lib (#38410)

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- switch to engine code base

* Mon Jun 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- add a script for creating dummy certificates
- move man pages from %%{_mandir}/man?/foo.?ssl to %%{_mandir}/man?ssl/foo.?

* Thu Jun 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add s390x support

* Fri Jun  1 2001 Nalin Dahyabhai <nalin@redhat.com>
- change two memcpy() calls to memmove()
- don't define L_ENDIAN on alpha

* Wed May 23 2001 Joe Orton <jorton@redhat.com> stronghold-0.9.6a-1
- Add 'stronghold-' prefix to package names.
- Obsolete standard openssl packages.

* Wed May 16 2001 Joe Orton <jorton@redhat.com>
- Add BuildArch: i586 as per Nalin's advice.

* Tue May 15 2001 Joe Orton <jorton@redhat.com>
- Enable assembler on ix86 (using new .tar.bz2 which does
  include the asm directories).

* Tue May 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- make subpackages depend on the main package

* Tue May  1 2001 Nalin Dahyabhai <nalin@redhat.com>
- adjust the hobble script to not disturb symlinks in include/ (fix from
  Joe Orton)

* Fri Apr 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- drop the m2crypo patch we weren't using

* Tue Apr 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- configure using "shared" as well

* Sun Apr  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 0.9.6a
- use the build-shared target to build shared libraries
- bump the soversion to 2 because we're no longer compatible with
  our 0.9.5a packages or our 0.9.6 packages
- drop the patch for making rsatest a no-op when rsa null support is used
- put all man pages into <section>ssl instead of <section>
- break the m2crypto modules into a separate package

* Tue Mar 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- use BN_LLONG on s390

* Mon Mar 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix the s390 changes for 0.9.6 (isn't supposed to be marked as 64-bit)

* Sat Mar  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- move c_rehash to the perl subpackage, because it's a perl script now

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 0.9.6
- enable MD2
- use the libcrypto.so and libssl.so targets to build shared libs with
- bump the soversion to 1 because we're no longer compatible with any of
  the various 0.9.5a packages circulating around, which provide lib*.so.0

* Wed Feb 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change hobble-openssl for disabling MD2 again

* Tue Feb 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- re-disable MD2 -- the EVP_MD_CTX structure would grow from 100 to 152
  bytes or so, causing EVP_DigestInit() to zero out stack variables in
  apps built against a version of the library without it

* Mon Feb 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- disable some inline assembly, which on x86 is Pentium-specific
- re-enable MD2 (see http://www.ietf.org/ietf/IPR/RSA-MD-all)

* Thu Feb 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix s390 patch

* Fri Dec 8 2000 Than Ngo <than@redhat.com>
- added support s390

* Mon Nov 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove -Wa,* and -m* compiler flags from the default Configure file (#20656)
- add the CA.pl man page to the perl subpackage

* Thu Nov  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- always build with -mcpu=ev5 on alpha

* Tue Oct 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- add a symlink from cert.pem to ca-bundle.crt

* Wed Oct 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- add a ca-bundle file for packages like Samba to reference for CA certificates

* Tue Oct 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove libcrypto's crypt(), which doesn't handle md5crypt (#19295)

* Mon Oct  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- add unzip as a buildprereq (#17662)
- update m2crypto to 0.05-snap4

* Tue Sep 26 2000 Bill Nottingham <notting@redhat.com>
- fix some issues in building when it's not installed

* Wed Sep  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- make sure the headers we include are the ones we built with (aaaaarrgh!)

* Fri Sep  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- add Richard Henderson's patch for BN on ia64
- clean up the changelog

* Tue Aug 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix the building of python modules without openssl-devel already installed

* Wed Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- byte-compile python extensions without the build-root
- adjust the makefile to not remove temporary files (like .key files when
  building .csr files) by marking them as .PRECIOUS

* Sat Aug 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- break out python extensions into a subpackage

* Mon Jul 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak the makefile some more

* Tue Jul 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable MD2 support

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable MDC2 support

* Sun Jul  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak the disabling of RC5, IDEA support
- tweak the makefile

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- strip binaries and libraries
- rework certificate makefile to have the right parts for Apache

* Wed Jun 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- use %%{_perl} instead of /usr/bin/perl
- disable alpha until it passes its own test suite

* Fri Jun  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- move the passwd.1 man page out of the passwd package's way

* Fri Jun  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 0.9.5a, modified for U.S.
- add perl as a build-time requirement
- move certificate makefile to another package
- disable RC5, IDEA, RSA support
- remove optimizations for now

* Wed Mar  1 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- Bero told me to move the Makefile into this package

* Wed Mar  1 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- add lib*.so symlinks to link dynamically against shared libs

* Tue Feb 29 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 0.9.5
- run ldconfig directly in post/postun
- add FAQ

* Sat Dec 18 1999 Bernhard Rosenkrdnzer <bero@redhat.de>
- Fix build on non-x86 platforms

* Fri Nov 12 1999 Bernhard Rosenkrdnzer <bero@redhat.de>
- move /usr/share/ssl/* from -devel to main package

* Tue Oct 26 1999 Bernhard Rosenkrdnzer <bero@redhat.de>
- inital packaging
- changes from base:
  - Move /usr/local/ssl to /usr/share/ssl for FHS compliance
  - handle RPM_OPT_FLAGS
