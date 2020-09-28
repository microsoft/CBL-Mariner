Summary:	Mariner specific rpm macro files
Name:		mariner-rpm-macros
Version:	1.0
Release:	6%{?dist}
License:	GPL+
Group:		Development/System
Vendor:		Microsoft Corporation
Distribution:	Mariner
Source0: macros
Source1: rpmrc
Source2: default-hardened-cc1
Source3: default-hardened-ld
Source4: default-annobin-cc1
Source5: macros.check
Source6: macros.python
Source7: macros.python2
Source8: macros.python3
Source9: macros.python-srpm
Source10: macros.openblas-srpm
Source11: macros.nodejs-srpm
Source12: macros.mono-srpm
Source13: macros.ocaml-srpm
Source14: macros.perl-srpm
Provides: redhat-rpm-config
Provides: openblas-srpm-macros
Provides: ocaml-srpm-macros
Provides: perl-srpm-macros
BuildArch: noarch


%global rcdir /usr/lib/rpm/mariner

%description
Mariner specific rpm macro files.

%package -n mariner-check-macros
Summary:        Mariner specific rpm macros to override default %%check behavior
License:        GPL+
Group:          Development/System

%description -n mariner-check-macros
Mariner specific rpm macros to override default %%check behavior

%package -n mariner-python-macros
Summary:        Mariner python macros
License:        GPL+
Group:          Development/System
Provides:       python-srpm-macros
Provides:       python-rpm-macros
Provides:       python2-rpm-macros
Provides:       python3-rpm-macros

%description -n mariner-python-macros
Mariner python macros

%prep
%setup -c -T
cp -p %{sources} .

%install
mkdir -p %{buildroot}%{rcdir}
install -p -m 644 -t %{buildroot}%{rcdir} macros rpmrc
install -p -m 444 -t %{buildroot}%{rcdir} default-hardened-*
install -p -m 444 -t %{buildroot}%{rcdir} default-annobin-*

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/macros.d macros.*

%files
%defattr(-,root,root)
%{rcdir}/macros
%{rcdir}/rpmrc
%{rcdir}/default-hardened-*
%{rcdir}/default-annobin-*
%{_rpmconfigdir}/macros.d/macros.openblas-srpm
%{_rpmconfigdir}/macros.d/macros.nodejs-srpm
%{_rpmconfigdir}/macros.d/macros.mono-srpm
%{_rpmconfigdir}/macros.d/macros.ocaml-srpm
%{_rpmconfigdir}/macros.d/macros.perl-srpm

%files -n mariner-check-macros
%{_rpmconfigdir}/macros.d/macros.check

%files -n mariner-python-macros
%{_rpmconfigdir}/macros.d/macros.python*

%changelog
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
