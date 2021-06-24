%global uclibc_name uClibc-ng
# This package only contains a static library
%global debug_package %{nil}
Summary:        C library for embedded Linux
Name:           uclibc-ng
Version:        1.0.37
Release:        1%{?dist}
License:        LGPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.uclibc.org/
Source0:        https://downloads.uclibc-ng.org/releases/%{version}/%{uclibc_name}-%{version}.tar.xz
Source1:        uClibc.config
BuildRequires:  gcc

%description
uClibc-ng is a C library for developing embedded Linux systems.
It is much smaller than the GNU C Library, but nearly all applications
supported by glibc also work perfectly with uClibc.

%package devel
Summary:        Header files and libraries for uClibc library
Provides:       uclibc-static = %{version}-%{release}
Provides:       uclibc-devel = %{version}-%{release}

%description devel
uClibc is a C library for developing embedded Linux systems.
It is much smaller than the GNU C Library, but nearly all applications
supported by glibc also work perfectly with uClibc.
This package contains the header files and libraries
needed for uClibc package.

%prep
%setup -q -n %{uclibc_name}-%{version}

cat %{SOURCE1} >.config1
iconv -f windows-1252 -t utf-8 README >README.pom
mv README.pom README

%build
mkdir kernel-include
cp -a %{_includedir}/asm kernel-include
cp -a %{_includedir}/asm-generic kernel-include
cp -a %{_includedir}/linux kernel-include

arch=`uname -m | sed -e 's/i.86/i386/' -e 's/ppc/powerpc/' -e 's/armv7l/arm/' -e 's/armv5tel/arm/'`
echo "TARGET_$arch=y" >.config
echo "TARGET_ARCH=\"$arch\"" >>.config
%ifarch %{arm}
echo "CONFIG_ARM_EABI=y" >>.config
echo "ARCH_ANY_ENDIAN=n" >>.config
echo "ARCH_LITTLE_ENDIAN=y" >>.config
echo "ARCH_WANTS_LITTLE_ENDIAN=y" >>.config
%endif
cat .config1 >>.config

yes "" | make oldconfig %{?_smp_mflags}
make V=1 %{?_smp_mflags}

%install
mkdir -p %{buildroot}/lib
make install PREFIX="%{buildroot}/"
make install_headers PREFIX="%{buildroot}/" DEVEL_PREFIX=""
cp -a kernel-include/* %{buildroot}/include/

# move libraries to proper subdirectory
mkdir -p %{buildroot}/%{_libdir}/uClibc
mv  %{buildroot}/lib/*  %{buildroot}/%{_libdir}/uClibc/
rm -rf  %{buildroot}/lib/

# move the header files to /usr subdirectory
mkdir -p %{buildroot}/%{_includedir}/uClibc
mv  %{buildroot}/include/*  %{buildroot}/%{_includedir}/uClibc
rm -rf  %{buildroot}/include/

%files devel
%doc docs/Glibc_vs_uClibc_Differences.txt docs/uClibc_vs_SuSv3.txt docs/porting.txt
%license COPYING.LIB
%doc README MAINTAINERS
%{_includedir}/uClibc
%{_libdir}/uClibc

%changelog
* Wed May 05 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.37-1
- Updating to version 1.0.37 to fix CVE-2021-27419.

* Thu Oct 15 2020 Mateusz Malisz <mamalisz@microsoft.com> - 1.0.36-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- License Verified
- Changed uclibc to uclibc-ng
- Changed version from 0.9.33.2 to 1.0.36

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Nikola Forró <nforro@redhat.com> - 0.9.33.2-17
- add missing gcc build dependency

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 20 2016 Dan Horák <dan[at]danny.cz> - 0.9.33.2-12
- switch to ExclusiveArch

* Mon Aug 15 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.33.2-11
- Update Power64 macro

* Mon Jul 11 2016 Nikola Forró <nforro@redhat.com> - 0.9.33.2-10
- fix CVE-2016-6264
  resolves #1352460

* Thu Feb 18 2016 Nikola Forró <nforro@redhat.com> - 0.9.33.2-9
- add support for MIPS
  resolves #1305957

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.33.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.33.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.33.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.33.2-5
- No aarch64 support

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.33.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May  6 2013 Denys Vlasenko <dvlasenko@redhat.com> - 0.9.32-3
- Enable UCLIBC_HAS_RESOLVER_SUPPORT, UCLIBC_LINUX_MODULE_26,
  UCLIBC_HAS_SHA256/512_CRYPT_IMPL, UCLIBC_HAS_FOPEN_CLOSEEXEC_MODE
  config options.
- fix __kernel_long_t problem.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.33.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Peter Schiffer <pschiffe@redhat.com> - 0.9.33.2-1
- resolves: #771041
  update to 0.9.33.2

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 18 2011 Peter Schiffer <pschiffe@redhat.com> - 0.9.32-2
- fixed compile error on i686

* Tue Aug 16 2011 Peter Schiffer <pschiffe@redhat.com> - 0.9.32-1
- resolves: #712040
  resolves: #716134
  update to 0.9.32 final

* Mon Jun 13 2011 Peter Robinson <pbrobinson@gmail.com> - 0.9.32-0.5.rc2
- And set the ARM build to little endian

* Sat Jun 11 2011 Peter Robinson <pbrobinson@gmail.com> - 0.9.32-0.4.rc2
- It seems we need to set the ARM ABI to EABI too

* Sat Jun 11 2011 Peter Robinson <pbrobinson@gmail.com> - 0.9.32-0.3.rc2
- Add support for ARM

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.32-0.2.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Tom Callaway <spot@fedoraproject.org> - 0.9.32-0.1.rc2
- update config for 0.9.32-rc2, busybox
- patch getutent

* Tue Nov  9 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.9.31-2
- update to 0.9.31

* Fri Jun  5 2009 Ivana Varekova <varekova@redhat.com> - 0.9.30.1-2
- initial build for Red Hat
