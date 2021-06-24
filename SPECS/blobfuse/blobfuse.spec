Summary:        FUSE adapter - Azure Storage Blobs
Name:           blobfuse
Version:        1.3.6
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/Azure/azure-storage-fuse/
Source0:        https://github.com/Azure/azure-storage-fuse/archive/%{name}-%{version}.tar.gz
BuildRequires:  boost
BuildRequires:  boost-devel
BuildRequires:  boost-static
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  curl-libs
BuildRequires:  fuse-devel
BuildRequires:  gnutls
BuildRequires:  gnutls-devel
BuildRequires:  golang
BuildRequires:  libgcrypt-devel
BuildRequires:  pkg-config
BuildRequires:  util-linux-devel
BuildRequires:  util-linux-libs
Requires:       fuse

%description
FUSE adapter - Azure Storage Blobs

%prep
%autosetup -n azure-storage-fuse-blobfuse-%{version}

%build
./build.sh

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 build/blobfuse %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/blobfuse

%changelog
* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.3.6-2
- Increment release to force republishing using golang 1.15.11.
* Tue Feb 02 2021 Henry Beberman <henry.beberman@microsoft.com> 1.3.6-1
- Add blobfuse spec
- License verified
- Original version for CBL-Mariner
