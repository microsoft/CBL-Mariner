Summary:        Compact text-to-speech synthesizer
Name:           espeak-ng
Version:        1.50
Release:        3%{?dist}
# Apache2 license applies only to Android APK code- does not apply here
# BSD license applies only to Windows code- does not apply here
License:        GPLv3 AND Unicode
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/espeak-ng/espeak-ng
Source0:        https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}.tgz
Patch0:         tests-fix-greek-letter-variants.patch
Patch1:         tests-newline-fixes.patch
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pcaudiolib-devel
BuildRequires:  pkg-config
BuildRequires:  which
Requires:       pcaudiolib

%description
The eSpeak NG is a compact open source software text-to-speech synthesizer for Linux.

%package devel
Summary:        Libraries and header files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Libraries and header files for %{name}

%prep
%autosetup -n %{name} -p1

%build
./autogen.sh
%configure --without-sonic
# Don't use -j here: messes with data compilation
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print
ln -s libespeak-ng.so %{buildroot}%{_libdir}/libespeak.so
rm %{buildroot}%{_libdir}/libespeak.la

# Rename problematic file with space in name
# This file does not work well with our GNU Make build system when placed in the ISO initrd
# GNU Make hacks to allow spaces in filenames are hacky and likely to make things worse
# Sample error: "make[1]: *** No rule to make target 'serious', needed by 'image'. Stop."
mv "%{buildroot}%{_datadir}/espeak-ng-data/voices/!v/Mr serious" "%{buildroot}%{_datadir}/espeak-ng-data/voices/!v/Mr_serious"

%check
make check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS CHANGELOG.md README.md
%{_bindir}/*
%{_datadir}/espeak-ng-data
%{_datadir}/vim/addons/ftdetect/espeakfiletype.vim
%{_datadir}/vim/addons/syntax/espeaklist.vim
%{_datadir}/vim/addons/syntax/espeakrules.vim
%{_datadir}/vim/registry/espeak.yaml
%{_libdir}/libespeak-ng.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/espeak
%{_includedir}/espeak-ng
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
* Wed May 05 2021 Thomas Crain <thcrain@microsoft.com> - 1.50-3
- Rename 'Mr serious' voice file to 'Mr_serious' to avoid spaces in filenames

* Fri Mar 05 2021 Thomas Crain <thcrain@microsoft.com> - 1.50-2
- Add tests-fix-greek-letter-variants.patch to address failing test
- Adjust tests-newline-fixes.patch to account for new patch

* Fri Feb 05 2021 Thomas Crain <thcrain@microsoft.com> - 1.50-1
- Original version for CBL-Mariner (license: MIT)
- License verified
