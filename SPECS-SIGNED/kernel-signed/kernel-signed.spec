%global debug_package %{nil}
%global sha512hmac bash %{_sourcedir}/sha512hmac-openssl.sh
%ifarch x86_64
%global buildarch x86_64
%endif
%ifarch aarch64
%global buildarch aarch64
%endif
%define uname_r %{version}-%{release}
Summary:        Signed Linux Kernel for %{buildarch} systems
Name:           kernel-signed-%{buildarch}
Version:        5.10.52.1
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
# This spec purpose is to take an input kernel rpm and input secure-boot-signed
# kernel binary from the same build and generate a new "kernel" rpm with the
# signed kernel binary + all of the other original kernel files, triggers,
# scriptlets, requires, provides, etc.
#
# We need to ensure the kernel modules and kernel binary used are from the exact
# same build because at build time the kernel modules are signed with an
# ephemeral key that the kernel enrolls in its keyring. We enforce kernel
# module signature checking when we enable security features like kernel
# lockdown so our kernel can only load those specific kernel modules at runtime.
#
# Additionally, to complete the UEFI Secure Boot chain, we must PE-sign the
# kernel binary. Ideally we would enable secure-boot signing tools like pesign
# or sbsign to be callable from inside the rpmbuild environment, that way we can
# secure-boot sign the kernel binary during the kernel's rpmbuild. It is best
# practice to sign as soon as possible. However there are issues getting that
# secure boot signing infrastructure in place today. Hence we sign the
# resulting kernel binary and "repackage" the kernel RPM (something rpm itself
# actively tries to make sure you never do...generally for good reasons).
#
# To achive this repackaging, this spec creates a new subpackage named
# "kernel". To retain all of the initial kernel package behaviors, we make sure
# the subpackage has the same requires, provides, triggers, post steps, and
# files as the original kernel package.
#
# This specific repackaging implementation leaves room for us to enable the
# more ideal secure-boot signing flow in the future without introducing any
# sort of breaking change or new packaging. Users still install a "kernel"
# package like they normally would.
#
# Maintenance Notes:
# - This spec's "version" and "release" must reflect the unsigned version that
# was signed. An important consequence is that when making a change to this
# spec or the normal kernel spec, the other spec's version version/release must
# be increased to keep the two versions consistent.
#
# - Make sure the kernel subpackage's Requires, Provides, triggers, post/postun
# scriptlets, and files match the normal kernel spec's. The kernel subpackage
# should contain the same content as the input kernel package but replace the
# kernel binary with our signed kernel binary. Since all the requires, provides,
# etc are the same, this new kernel package can be a direct replacement for the
# normal kernel package and RPM will resolve packages with kernel dependencies
# correctly.
#
# To populate the input sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec
Source0:        kernel-%{version}-%{release}.%{buildarch}.rpm
Source1:        vmlinuz-%{uname_r}
Source2:        sha512hmac-openssl.sh
BuildRequires:  cpio
BuildRequires:  openssl
BuildRequires:  sed

%description
This package contains the Linux kernel package with kernel signed with the production key

%package -n     kernel
Summary:        Linux Kernel
Group:          System Environment/Kernel
Requires:       filesystem
Requires:       kmod
Requires(post): coreutils
Requires(postun): coreutils

%description -n kernel
The kernel package contains the signed Linux kernel.

%prep

%build
# This spec's whole purpose is to inject the signed kernel binary
rpm2cpio %{SOURCE0} | cpio -idmv
cp %{SOURCE1} ./boot/vmlinuz-%{uname_r}

%install
# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

# Recalculate sha512hmac for FIPS
%{sha512hmac} %{buildroot}/boot/vmlinuz-%{uname_r} | sed -e "s,$RPM_BUILD_ROOT,," > %{buildroot}/boot/.vmlinuz-%{uname_r}.hmac
cp %{buildroot}/boot/.vmlinuz-%{uname_r}.hmac %{buildroot}/lib/modules/%{uname_r}/.vmlinuz.hmac

%triggerin -n kernel -- initramfs
mkdir -p %{_localstatedir}/lib/rpm-state/initramfs/pending
touch %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
echo "initrd generation of kernel %{uname_r} will be triggered later" >&2

%triggerun -n kernel -- initramfs
rm -rf %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
rm -rf /boot/initrd.img-%{uname_r}
echo "initrd of kernel %{uname_r} removed" >&2

%postun -n kernel
if [ ! -e /boot/mariner.cfg ]
then
     ls /boot/linux-*.cfg 1> /dev/null 2>&1
     if [ $? -eq 0 ]
     then
          list=`ls -tu /boot/linux-*.cfg | head -n1`
          test -n "$list" && ln -sf "$list" /boot/mariner.cfg
     fi
fi

%post -n kernel
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/mariner.cfg

%files -n kernel
%defattr(-,root,root)
%license COPYING
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
/boot/.vmlinuz-%{uname_r}.hmac
%config(noreplace) /boot/linux-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
/lib/modules/%{uname_r}/.vmlinuz.hmac
%exclude /lib/modules/%{uname_r}/build
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound
%ifarch x86_64
%exclude /lib/modules/%{uname_r}/kernel/arch/x86/oprofile/
%endif

%changelog
* Tue Jul 20 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.52.1-1
- Update source to 5.10.52.1

* Mon Jul 19 2021 Chris Co <chrco@microsoft.com> - 5.10.47.1-2
- Bump release number to match kernel release

* Tue Jul 06 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.47.1-1
- Update source to 5.10.47.1

* Wed Jun 30 2021 Chris Co <chrco@microsoft.com> - 5.10.42.1-4
- Bump release number to match kernel release

* Tue Jun 22 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.10.42.1-3
- Bump release number to match kernel release

* Wed Jun 16 2021 Chris Co <chrco@microsoft.com> - 5.10.42.1-2
- Bump release number to match kernel release

* Tue Jun 08 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.42.1-1
- Update source to 5.10.42.1

* Thu Jun 03 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.37.1-2
- Bump release number to match kernel release

* Fri May 28 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.37.1-1
- Update source to 5.10.37.1

* Thu May 27 2021 Chris Co <chrco@microsoft.com> - 5.10.32.1-7
- Bump release number to match kernel release

* Wed May 26 2021 Chris Co <chrco@microsoft.com> - 5.10.32.1-6
- Bump release number to match kernel release

* Tue May 25 2021 Daniel Mihai <dmihai@microsoft.com> - 5.10.32.1-5
- Bump release number to match kernel release

* Thu May 20 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.10.32.1-4
- Recalculate sha512hmac on signed kernel binary

* Tue May 17 2021 Andrew Phelps <anphel@microsoft.com> - 5.10.32.1-3
- Update to kernel release 5.10.32.1-3

* Thu May 13 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.32.1-2
- Bump release number to match kernel release

* Mon May 03 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.32.1-1
- Update source to 5.10.32.1

* Thu Apr 22 2021 Chris Co <chrco@microsoft.com> - 5.10.28.1-4
- Bump release number to match kernel release

* Mon Apr 19 2021 Chris Co <chrco@microsoft.com> - 5.10.28.1-3
- Define a new kernel subpackage

* Thu Apr 15 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.28.1-2
- Update to kernel release 5.10.28.1-2

* Thu Apr 08 2021 Chris Co <chrco@microsoft.com> - 5.10.28.1-1
- Update source to 5.10.28.1
- Update uname_r define to match the new value derived from the source

* Fri Mar 26 2021 Daniel Mihai <dmihai@microsoft.com> - 5.10.21.1-4
- Update to kernel release 5.10.21.1-4

* Thu Mar 18 2021 Chris Co <chrco@microsoft.com> - 5.10.21.1-3
- Fix file copy

* Wed Mar 17 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.10.21.1-2
- Update to kernel release 5.10.21.1-2

* Thu Mar 11 2021 Chris Co <chrco@microsoft.com> - 5.10.21.1-1
- Update source to 5.10.21.1

* Fri Mar 05 2021 Chris Co <chrco@microsoft.com> - 5.10.13.1-4
- Update release number to match kernel spec
- Use uname_r macro instead of version-release for kernel version

* Thu Mar 04 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.10.13.1-3
- Update to kernel release 5.10.13.1-3

* Mon Feb 22 2021 Thomas Crain <thcrain@microsoft.com> - 5.10.13.1-2
- Update to kernel release 5.10.13.1-2

* Thu Feb 18 2021 Chris Co <chrco@microsoft.com> - 5.10.13.1-1
- Update source to 5.10.13.1

* Tue Feb 16 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.91-5
- Update to kernel release 5.4.91-5.

* Tue Feb 09 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.91-4
- Update to kernel release 5.4.91-4

* Thu Jan 28 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.91-3
- Add hmac files for FIPS

* Wed Jan 27 2021 Daniel McIlvaney <damcilva@microsoft.com> - 5.4.91-2
- Update release number to match kernel spec

* Wed Jan 20 2021 Chris Co <chrco@microsoft.com> - 5.4.91-1
- Update source to 5.4.91

* Tue Jan 12 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.4.83-4
- Update release number to match kernel spec

* Sat Jan 09 2021 Andrew Phelps <anphel@microsoft.com> - 5.4.83-3
- Update to kernel release 5.4.83-3

* Mon Dec 28 2020 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.83-2
- Update to kernel release 5.4.83-2

* Tue Dec 15 2020 Henry Beberman <henry.beberman@microsoft.com> - 5.4.83-1
- Update source to 5.4.83

* Fri Dec 04 2020 Chris Co <chrco@microsoft.com> - 5.4.81-1
- Update source to 5.4.81

* Wed Nov 25 2020 Chris Co <chrco@microsoft.com> - 5.4.72-5
- Update release number to match kernel spec

* Mon Nov 23 2020 Chris Co <chrco@microsoft.com> - 5.4.72-4
- Update release number to match kernel spec

* Mon Nov 16 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.4.72-3
- Update release number

* Tue Nov 10 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.4.72-2
- Update release number

* Mon Oct 26 2020 Chris Co <chrco@microsoft.com> - 5.4.72-1
- Update source to 5.4.72
- Lint spec

* Fri Oct 16 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.4.51-11
- Update release number

* Fri Oct 02 2020 Chris Co <chrco@microsoft.com> - 5.4.51-10
- Update release number to match kernel spec

* Fri Oct 02 2020 Chris Co <chrco@microsoft.com> - 5.4.51-9
- Update release number

* Wed Sep 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 5.4.51-8
- Update postun script to deal with removal in case of another installed kernel.

* Fri Sep 25 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.4.51-7
- Update release number

* Wed Sep 23 2020 Daniel McIlvaney <damcilva@microsoft.com> - 5.4.51-6
- Update release number

* Thu Sep 03 2020 Daniel McIlvaney <damcilva@microsoft.com> - 5.4.51-5
- Update release number

* Thu Sep 03 2020 Chris Co <chrco@microsoft.com> - 5.4.51-4
- Update release number

* Thu Sep 03 2020 Chris Co <chrco@microsoft.com> - 5.4.51-3
- Add missing requires

* Tue Sep 01 2020 Chris Co <chrco@microsoft.com> - 5.4.51-2
- Update release number

* Wed Aug 19 2020 Chris Co <chrco@microsoft.com> - 5.4.51-1
- Update source to 5.4.51

* Wed Aug 19 2020 Chris Co <chrco@microsoft.com> - 5.4.42-12
- Update release number

* Tue Aug 18 2020 Chris Co <chrco@microsoft.com> - 5.4.42-11
- Original version for CBL-Mariner.
