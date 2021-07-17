%global debug_package %{nil}
%ifarch x86_64
%global buildarch x86_64
%global grubefiname grubx64.efi
%endif
%ifarch aarch64
%global buildarch aarch64
%global grubefiname grubaa64.efi
%endif
Summary:        Signed GRand Unified Bootloader for %{buildarch} systems
Name:           grub2-efi-binary-signed-%{buildarch}
Version:        2.06~rc1
Release:        5%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.gnu.org/software/grub
# This package's "version" and "release" must reflect the unsigned version that
# was signed.
# An important consequence is that when making a change to this package, the
# unsigned version/release must be increased to keep the two versions consistent.
# Ideally though, this spec will not change much or at all, so the version will
# just track the unsigned package's version/release.
#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec
Source0:        grub2-efi-binary-%{version}-%{release}.%{buildarch}.rpm
Source1:        %{grubefiname}

%description
This package contains the GRUB EFI image signed for secure boot. The package is
specifically created for installing on %{buildarch} systems

%package -n     grub2-efi-binary
Summary:        GRand Unified Bootloader
Group:          Applications/System

%description -n grub2-efi-binary
This package contains the GRUB EFI image signed for secure boot. The package is
specifically created for installing on %{buildarch} systems

%prep

%build

%install
mkdir -p %{buildroot}/boot/efi/EFI/BOOT
cp %{SOURCE1} %{buildroot}/boot/efi/EFI/BOOT/%{grubefiname}

%files -n grub2-efi-binary
/boot/efi/EFI/BOOT/%{grubefiname}

%changelog
* Thu Jun 03 2021 Henry Li <lihl@microsoft.com> - 2.06~rc1-5
- Update release to be aligned with unsigned version

* Fri Apr 16 2021 Chris Co <chrco@microsoft.com> - 2.06~rc1-4
- Commonize to one spec instead of having a spec per arch
- Define a new grub2-efi-binary subpackage which contains the signed collateral

* Fri Apr 02 2021 Rachel Menge <rachelmenge@microsoft.com> - 2.06~rc1-3
- Update release to be aligned with unsigned version

* Fri Mar 26 2021 Chris Co <chrco@microsoft.com> - 2.06~rc1-2
- Update release to be aligned with unsigned version

* Wed Mar 10 2021 Chris Co <chrco@microsoft.com> - 2.06~rc1-1
- Update to 2.06-rc1
- Incorporate SBAT data

* Wed Dec 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.02-26
- Updating release to be aligned with the unsigned bits.

* Tue Nov 03 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.02-25
- Updating release to be aligned with the unsigned bits.

* Thu Aug 13 2020 Chris Co <chrco@microsoft.com> 2.02-24
- Original version for CBL-Mariner.
