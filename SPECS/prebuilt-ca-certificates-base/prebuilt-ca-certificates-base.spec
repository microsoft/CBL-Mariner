# When updating, "Version" AND "Release" tags must be updated in the "ca-certificates" package as well.
Summary:        Prebuilt version of ca-certificates-base package.
Name:           prebuilt-ca-certificates-base
Version:        20200720
Release:        14%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://hg.mozilla.org
BuildArch:      noarch

%description
Prebuilt version of the ca-certificates-base package with no runtime dependencies.

BuildRequires:  ca-certificates-base

Conflicts:      ca-certificates
Conflicts:      ca-certificates-base
Conflicts:      ca-certificates-microsoft

%prep -q

%build

%install

mkdir -p %{buildroot}%{_datadir}/pki/ca-trust-legacy/
mkdir -p %{buildroot}%{_sysconfdir}/pki/

install -p -m 644 %{_datadir}/pki/ca-trust-legacy/* %{buildroot}%{_datadir}/pki/ca-trust-legacy/
cp -r %{_sysconfdir}/pki/* %{buildroot}%{_sysconfdir}/pki/

find %{buildroot} -name README -delete

rm %{buildroot}%{_sysconfdir}/pki/ca-trust/ca-legacy.conf
rm %{buildroot}%{_sysconfdir}/pki/ca-trust/source/ca-bundle.legacy.crt
rm %{buildroot}%{_sysconfdir}/pki/tls/*.cnf
rm %{buildroot}%{_sysconfdir}/pki/rpm-gpg/*

%files
# Base certs bundle file with trust
%{_sysconfdir}/pki/tls/cert.pem
%{_sysconfdir}/pki/tls/certs/*
%{_sysconfdir}/pki/ca-trust/extracted/*
%{_sysconfdir}/pki/java/cacerts
%{_datadir}/pki/ca-trust-legacy/*

%changelog
* Thu Jun 03 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 20200720-14
- Making 'Release' match with 'ca-certificates'.

* Fri Mar 12 2021 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20200720-13
- Making 'Release' match with 'ca-certificates'.

* Sat Mar 06 2021 CBL-Mariner Servicing Account <clbmargh@microsoft.com> - 20200720-12
- Making 'Release' match with 'ca-certificates'.

* Mon Feb 08 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-11
- Making 'Release' match with 'ca-certificates'.

* Tue Jan 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-10
- Making 'Release' match with 'ca-certificates'.

* Wed Dec 2 2020 Mateusz Malisz <mamalisz@microsoft.com> - 20200720-1
- Original version for CBL-Mariner
