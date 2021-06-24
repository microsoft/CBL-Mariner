%define debug_package %{nil}

Summary:        CRI tools
Name:           cri-tools
Version:        1.11.1
Release:        7%{?dist}
License:        ASL 2.0
URL:            https://github.com/kubernetes-sigs/cri-tools
#Source0:       https://github.com/kubernetes-sigs/cri-tools/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  golang

%description
cri-tools aims to provide a series of debugging and validation tools for Kubelet CRI, which includes:
crictl: CLI for kubelet CRI.
critest: validation test suites for kubelet CRI.

%prep
%setup -qn %{name}-%{version}

%build
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/lib/.build-id
mkdir -p %{buildroot}/usr/share/doc/cri-tools
mkdir -p %{buildroot}/usr/share/licenses/cri-tools
mkdir -p %{buildroot}/man/man1

make install DESTDIR=%{buildroot}
cp /usr/local/bin/crictl %{buildroot}/usr/bin
cp /usr/local/bin/critest %{buildroot}/usr/bin
cp CHANGELOG.md %{buildroot}/usr/share/doc/cri-tools
cp LICENSE %{buildroot}/usr/share/licenses/cri-tools
cp CHANGELOG.md %{buildroot}/usr/share/doc/cri-tools
cp CONTRIBUTING.md %{buildroot}/usr/share/doc/cri-tools
cp OWNERS %{buildroot}/usr/share/doc/cri-tools
cp README.md %{buildroot}/usr/share/doc/cri-tools
cp code-of-conduct.md %{buildroot}/usr/share/doc/cri-tools
cp docs/validation.md %{buildroot}/usr/share/doc/cri-tools
cp docs/roadmap.md %{buildroot}/usr/share/doc/cri-tools

%files
%defattr(-,root,root)
%license LICENSE
%{_datadir}/%{name}
/usr/bin
/usr/share/doc/*
/usr/share/licenses/*
/man/man1/

%clean
rm -rf %{buildroot}/*

%changelog
*   Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.11.1-7
-   Increment release to force republishing using golang 1.15.11.
*   Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 1.11.1-6
-   Increment release to force republishing using golang 1.15.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.11.1-5
-   Added %%license line automatically
*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.11.1-4
-   Renaming go to golang
*   Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.11.1-3
-   Fixed "Source0" and "URL" tags.
-   License verified.
-   Removed "%%define sha1".
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.11.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Jul 26 2018 Tapas Kundu <tkundu@vmware.com> 1.11.1-1
-   Initial build added for Photon.
