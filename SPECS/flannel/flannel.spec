%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath
%define gopath_flannel_folder %{our_gopath}/src/github.com/coreos/flannel

Summary:        Simple and easy way to configure a layer 3 network fabric designed for Kubernetes
Name:           flannel
Version:        0.12.0
Release:        2%{?dist}
License:        Apache License 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/coreos/flannel
#Source0:       https://github.com/coreos/flannel/archive/v0.12.0.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:         buid-no-static-glibc.patch

BuildRequires:  golang >= 1.10.3

%description
Flannel is a simple and easy way to configure a layer 3 network fabric designed for Kubernetes.

%prep
%autosetup -p1

%build
# move sources where make expect them to be (see flannel building.md)
export GOPATH=%{our_gopath}
mkdir -p "%{gopath_flannel_folder}"
mv %{_builddir}/%{name}-%{version}/* %{gopath_flannel_folder}
# but keep license file where it was to make %license macro happy
cp %{gopath_flannel_folder}/LICENSE %{_builddir}/%{name}-%{version}

# build flannel
export TAG=v%{version}
%ifarch x86_64
export ARCH=amd64
%endif
%ifarch aarch64
export ARCH=arm64
%endif

pushd %{gopath_flannel_folder}
make dist/flanneld
popd

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} %{gopath_flannel_folder}/dist/flanneld

%clean
rm -rf %{buildroot}/*
rm -rf %{gopath_flannel_folder}/*

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/flanneld

%changelog
* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 0.12.0-2
- Increment release to force republishing using golang 1.15.11.
* Wed Jan 20 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 0.12.0-1
- Original version for CBL-Mariner.
