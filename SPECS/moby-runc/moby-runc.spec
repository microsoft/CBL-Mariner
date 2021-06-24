Summary:        CLI tool for spawning and running containers per OCI spec.
Name:           moby-runc
Version:        1.0.0~rc95+azure
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://runc.io/

# See generate-sources.sh for creating runc source tarball
#Source0:       https://github.com/opencontainers/runc/releases/download/v1.0.0-rc95/runc.tar.xz
Source0:        runc-v1.0.0-rc95.tar.gz
#Source1:       https://github.com/sirupsen/logrus/archive/v1.8.1.tar.gz
Source1:        logrus-v1.8.1.tar.gz
#Source2:       https://github.com/opencontainers/runtime-spec/archive/v1.0.2.tar.gz
Source2:        runtime-spec-v1.0.2.tar.gz
#Source3:       https://github.com/urfave/cli/archive/v2.3.0.tar.gz
Source3:        urfave-cli-v2.3.0.tar.gz
# golang sys and crypto sources are git cloned to latest commit.
# Please look for ./getgosources.sh for more details.
Source4:        https://github.com/golang/sys/archive/golang-sys-b0526f3d87448f0401ea3f7f3a81aa9e6ab4804d.tar.gz
Source5:        https://github.com/golang/crypto/archive/golang-crypto-c07d793c2f9aacf728fe68cbd7acd73adbd04159.tar.gz
Source6:        NOTICE
Source7:        LICENSE

Group:          Virtualization/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  curl
BuildRequires:  gawk
BuildRequires:  golang
BuildRequires:  iptables-devel
BuildRequires:  pkg-config
BuildRequires:  libaio-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-c-devel
BuildRequires:  python2-devel
BuildRequires:  unzip
BuildRequires:  go-md2man
Buildrequires:  which
Buildrequires:  git

Requires:       glibc
Requires:       libgcc
Requires:       libseccomp

# conflicting packages
Conflicts: runc
Conflicts: runc-io

Obsoletes: runc
Obsoletes: runc-io

%description
runC is a CLI tool for spawning and running containers according to the OCI specification. Containers are started as a child process of runC and can be embedded into various other systems without having to run a daemon.

%define OUR_GOPATH %{_topdir}/.gopath

%prep
%setup -q -n %{name}-%{version} -c
mkdir -p %{OUR_GOPATH}/src/github.com/opencontainers
ln -svfT %{_topdir}/BUILD/%{name}-%{version}/runc %{OUR_GOPATH}/src/github.com/opencontainers/runc

pushd ..

tar -xvf %{SOURCE1}
tar -xvf %{SOURCE2}
tar -xvf %{SOURCE3}
tar -xzvf %{SOURCE4}
tar -xzvf %{SOURCE5}

mkdir -p %{OUR_GOPATH}/src/github.com/opencontainers/
mkdir -p %{OUR_GOPATH}/src/github.com/sirupsen/
mkdir -p %{OUR_GOPATH}/src/github.com/urfave/
mkdir -p %{OUR_GOPATH}/src/golang.org/x/

ln -sfT %{_topdir}/BUILD/%{name}-%{version}/runtime-spec-1.0.2 %{OUR_GOPATH}/src/github.com/opencontainers/runtime-spec
ln -sfT %{_topdir}/BUILD/%{name}-%{version}/logrus-1.8.1 %{OUR_GOPATH}/src/github.com/sirupsen/logrus
ln -sfT %{_topdir}/BUILD/%{name}-%{version}/cli-2.3.0 %{OUR_GOPATH}/src/github.com/urfave/cli
ln -sfT %{_topdir}/BUILD/%{name}-%{version}/sys-master %{OUR_GOPATH}/src/golang.org/x/sys
ln -sfT %{_topdir}/BUILD/%{name}-%{version}/crypto-master %{OUR_GOPATH}/src/golang.org/x/crypto

popd

%build
export GOPATH=%{OUR_GOPATH}
export GOCACHE=%{OUR_GOPATH}/.cache
export GOPROXY=off
export GO111MODULE=off
# export GOFLAGS="-trimpath -gcflags=all=\"-trimpath=%{OUR_GOPATH}/src\" -asmflags=all=\"-trimpath=%{OUR_GOPATH}/src\""
export GOGC=off
export CGO_ENABLED=1
cd %{OUR_GOPATH}/src/github.com/opencontainers/runc
make %{?_smp_mflags} BUILDTAGS='seccomp apparmor' man runc

%install
cd %{OUR_GOPATH}/src/github.com/opencontainers/runc
make install BINDIR=%{buildroot}%{_bindir}
mkdir -p "%{buildroot}/%{_mandir}/man8"
for i in man/man8/*; do
    install -T -p -m 644 "${i}" "%{buildroot}%{_mandir}/man8/$(basename $i)"
done

mkdir -p %{buildroot}/usr/share/doc/%{name}-%{version}
cp %{SOURCE6} %{buildroot}/usr/share/doc/%{name}-%{version}/NOTICE
cp %{SOURCE7} %{buildroot}/usr/share/doc/%{name}-%{version}/LICENSE

%files
%license /usr/share/doc/%{name}-%{version}/LICENSE
%{_bindir}/runc
/usr/share/doc/%{name}-%{version}/*
%{_mandir}/*/*

%changelog
* Wed May 19 2021 Andrew Phelps <anphel@microsoft.com> 1.0.0~rc95+azure-1
- Update to version 1.0.0~rc95+azure to fix CVE-2021-30465
* Thu May 13 2021 Andrew Phelps <anphel@microsoft.com> 1.0.0~rc94+azure-1
- Update to version 1.0.0~rc94+azure
* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.0.0~rc10+azure-6
- Increment release to force republishing using golang 1.15.11.
* Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 1.0.0~rc10+azure-5
- Increment release to force republishing using golang 1.15.
* Wed May 20 2020 Joe Schmitt <joschmit@microsoft.com> 1.0.0~rc10+azure-4
- Remove reliance on existing GOPATH environment variable.
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.0.0~rc10+azure-3
- Added %%license line automatically
* Fri May 01 2020 Emre Girgin <mrgirgin@microsoft.com> 1.0.0~rc10+azure-2
- Renaming go to golang
* Fri Apr 03 2020 Mohan Datla <mdatla@microsoft.com> 1.0.0~rc10+azure-1
- Initial CBL-Mariner import from Azure.
* Thu Jan 23 2020 Brian Goff <brgoff@microsoft.com>
- Initial version
