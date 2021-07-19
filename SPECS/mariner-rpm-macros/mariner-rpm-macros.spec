Summary:	Mariner specific rpm macro files
Name:		mariner-rpm-macros
Version:	1.0
Release:	4%{?dist}
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

%files -n mariner-check-macros
%{_rpmconfigdir}/macros.d/macros.check

%changelog
* Wed Jun 30 2021 Andrew Phelps <anphel@microsoft.com> - 1.0-4
- Remove calls to brp-strip-debug-symbols and brp-strip-unneeded from macros
* Tue Jun 23 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0-3
- Add macros.check to support non-fatal check section runs for log collection.
* Mon Jun 08 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0-2
- Add vendor folder. Add optflags related macros and rpmrc derived from Fedora 32.
* Fri May 22 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0-1
- Original version for CBL-Mariner
