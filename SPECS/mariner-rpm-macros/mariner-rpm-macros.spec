%global rcdir %{_libdir}/rpm/mariner
%global rcluadir %{_libdir}/rpm/lua/mariner
# Turn off auto byte compilation since when building this spec in the toolchain the needed scripts are not installed yet.
# __brp_python_bytecompile
%global __brp_python_bytecompile %{nil}
Summary:        Mariner specific rpm macro files
Name:           mariner-rpm-macros
Version:        2.0
Release:        1%{?dist}
License:        GPL+ AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/System
Source0:        macros
Source1:        rpmrc
Source2:        default-hardened-cc1
Source3:        default-hardened-ld
Source4:        default-annobin-cc1
Source5:        macros.check
Source6:        macros.python
Source7:        macros.python2
Source8:        macros.python3
Source9:        macros.python-srpm
Source10:       macros.openblas-srpm
Source11:       macros.nodejs-srpm
Source12:       macros.mono-srpm
Source13:       macros.ocaml-srpm
Source14:       macros.perl-srpm
Source15:       gpgverify
Source16:       pythondist.attr
Source17:       brp-python-bytecompile
Source18:       macros.pybytecompile
# Use an enhanced copy of Python's compileall module for Python >= 3.4
Source19:       https://github.com/fedora-python/compileall2/raw/v0.7.1/compileall2.py
Source20:       macros.forge
Source21:       common.lua
Source22:       forge.lua
# macros.rust-srpm is taken from https://pagure.io/fedora-rust/rust2rpm
Source23:       macros.rust-srpm
# macros.fonts is taken from the "fontpackages-devel" package.
Source24:       macros.fonts
Provides:       redhat-rpm-config
Provides:       openblas-srpm-macros
Provides:       ocaml-srpm-macros
Provides:       perl-srpm-macros
Provides:       python-srpm-macros
Provides:       python-rpm-macros
Provides:       python2-rpm-macros
Provides:       python3-rpm-macros
Provides:       rust-srpm-macros
BuildArch:      noarch

%description
Mariner specific rpm macro files.

%package -n mariner-check-macros
Summary:        Mariner specific rpm macros to override default %%check behavior
Group:          Development/System

%description -n mariner-check-macros
Mariner specific rpm macros to override default %%check behavior

%prep
%setup -q -c -T
cp -p %{sources} .

%install
mkdir -p %{buildroot}%{rcdir}
install -p -m 644 -t %{buildroot}%{rcdir} macros rpmrc
install -p -m 444 -t %{buildroot}%{rcdir} default-hardened-*
install -p -m 444 -t %{buildroot}%{rcdir} default-annobin-*
install -p -m 755 -t %{buildroot}%{rcdir} gpgverify
install -p -m 755 -t %{buildroot}%{rcdir} compileall2.py
install -p -m 755 -t %{buildroot}%{rcdir} brp-*

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/macros.d macros.*
mkdir -p %{buildroot}%{_fileattrsdir}
install -p -m 644 -t %{buildroot}%{_fileattrsdir} pythondist.attr

mkdir -p %{buildroot}%{rcluadir}/{rpm,srpm}
install -p -m 644 -t %{buildroot}%{rcluadir} common.lua
install -p -m 644 -t %{buildroot}%{rcluadir}/srpm forge.lua

%files
%defattr(-,root,root)
%{rcdir}/macros
%{rcdir}/rpmrc
%{rcdir}/default-hardened-*
%{rcdir}/default-annobin-*
%{rcdir}/gpgverify
%{rcdir}/brp-*
%{rcdir}/compileall2.py
%{_rpmconfigdir}/macros.d/macros.openblas-srpm
%{_rpmconfigdir}/macros.d/macros.nodejs-srpm
%{_rpmconfigdir}/macros.d/macros.mono-srpm
%{_rpmconfigdir}/macros.d/macros.ocaml-srpm
%{_rpmconfigdir}/macros.d/macros.perl-srpm
%{_rpmconfigdir}/macros.d/macros.rust-srpm
%{_rpmconfigdir}/macros.d/macros.fonts
%{_rpmconfigdir}/macros.d/macros.forge
%dir %{rcluadir}
%dir %{rcluadir}/srpm
%dir %{rcluadir}/rpm
%{rcluadir}/*.lua
%{rcluadir}/srpm/*.lua
%{_rpmconfigdir}/macros.d/macros.pybytecompile
%{_rpmconfigdir}/macros.d/macros.python*
%{_fileattrsdir}/pythondist.attr

%files -n mariner-check-macros
%{_rpmconfigdir}/macros.d/macros.check

%changelog
* Thu Jul 08 2021 Jon Slobodzian <joslobo@microsoft.com> - 2.0-1
- Version update for 2.0.

* Tue Jun 01 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-17
- Adding font macros from the "fontpackages-devel" package.

* Mon May 17 2021 Thomas Crain <thcrain@microsoft.com> - 1.0-16
- Add Rust SRPM macros from rust2rpm (license: MIT)
- Add rust-srpm-macros Provides

* Thu Feb 25 2021 Henry Li <lihl@microsoft.com> - 1.0-15
- Add _smp_build_cpus and relevant macros.

* Thu Feb 25 2021 Joe Schmitt <joschmit@microsoft.com> - 1.0-14
- Add forge macros and scripts.

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.0-13
- Import brp-python-bytecompile, compileall2.py, macros.pybytecompile, and python byte compilation in macros from Fedora 32 (license: MIT).
- Fix %%{_lib} and %%{_lib64} macros to reference the folder names instead of paths.
- Combine mariner-python-macros into the main package for byte compilation support.
- Make python3 the default python interpreter for byte compilation.

* Tue Jan 19 2021 Joe Schmitt <joschmit@microsoft.com> - 1.0-12
- Disable python requirement generator.

* Thu Jan 14 2021 Ruying Chen <v-ruyche@microsoft.com> - 1.0-11
- Remove pythondistdeps.py.

* Mon Jan 04 2021 Ruying Chen <v-ruyche@microsoft.com> - 1.0-10
- Enable python dependency generator for dist provides.

* Wed Nov 04 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0-9
- Define meson macros.

* Mon Nov 02 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0-8
- Define gpgverify macro.

* Thu Oct 22 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0-7
- Define __make macro.

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0-6
- Add backwards compatibility macros for compiling and linking.
- Define _fmoddir macro.
- Turn on perl_bootstrap by default.
- Add perl-srpm macros.

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0-5
- Add srpm macros.
- Add python related macros derived from Fedora 32 python-rpm-macros.

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0-4
- Add ldconfig_scriptlets related macros derived from Fedora 32 redhat-rpm-config.

* Tue Jun 23 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0-3
- Add macros.check to support non-fatal check section runs for log collection.

* Mon Jun 08 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0-2
- Add vendor folder. Add optflags related macros and rpmrc derived from Fedora 32.

* Fri May 22 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0-1
- Original version for CBL-Mariner
