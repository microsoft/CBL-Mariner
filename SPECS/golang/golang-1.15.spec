%global goroot          /usr/lib/golang
%global gopath          %{_datadir}/gocode
%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif
%define debug_package %{nil}
%define __strip /bin/true
# rpmbuild magic to keep from having meta dependency on libc.so.6
%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
Summary:        Go
Name:           golang
Version:        1.15.11
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://golang.org
Source0:        https://dl.google.com/go/go%{version}.src.tar.gz
Source1:        https://dl.google.com/go/go1.4-bootstrap-20171003.tar.gz
Patch0:         go14_bootstrap_aarch64.patch
Obsoletes:      %{name} < %{version}
Provides:       %{name} = %{version}

%description
Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.

%prep
# Setup go 1.4 bootstrap source
tar xf %{SOURCE1} --no-same-owner
patch -Np1 --ignore-whitespace < /usr/src/mariner/SOURCES/go14_bootstrap_aarch64.patch
mv -v go go-bootstrap

%setup -q -n go

%build
# Build go 1.4 bootstrap
pushd /usr/src/mariner/BUILD/go-bootstrap/src
CGO_ENABLED=0 ./make.bash
popd
mv -v /usr/src/mariner/BUILD/go-bootstrap /usr/lib/golang
export GOROOT=/usr/lib/golang

# Build current go version
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOROOT_BOOTSTRAP=%{goroot}

export GOROOT="`pwd`"
export GOPATH=%{gopath}
export GOROOT_FINAL=%{_bindir}/go
rm -f  %{gopath}/src/runtime/*.c
pushd src
./make.bash --no-clean
popd

%install

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{goroot}

cp -R api bin doc favicon.ico lib pkg robots.txt src misc VERSION %{buildroot}%{goroot}

# remove the unnecessary zoneinfo file (Go will always use the system one first)
rm -rfv %{buildroot}%{goroot}/lib/time

# remove the doc Makefile
rm -rfv %{buildroot}%{goroot}/doc/Makefile

# put binaries to bindir, linked to the arch we're building,
# leave the arch independent pieces in %{goroot}
mkdir -p %{buildroot}%{goroot}/bin/linux_%{gohostarch}
ln -sfv ../go %{buildroot}%{goroot}/bin/linux_%{gohostarch}/go
ln -sfv ../gofmt %{buildroot}%{goroot}/bin/linux_%{gohostarch}/gofmt
ln -sfv %{goroot}/bin/gofmt %{buildroot}%{_bindir}/gofmt
ln -sfv %{goroot}/bin/go %{buildroot}%{_bindir}/go

# ensure these exist and are owned
mkdir -p %{buildroot}%{gopath}/src/github.com/
mkdir -p %{buildroot}%{gopath}/src/bitbucket.org/
mkdir -p %{buildroot}%{gopath}/src/code.google.com/p/

install -vdm755 %{buildroot}%{_sysconfdir}/profile.d
cat >> %{buildroot}%{_sysconfdir}/profile.d/go-exports.sh <<- "EOF"
export GOROOT=%{goroot}
export GOPATH=%{_datadir}/gocode
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOOS=linux
EOF

%post -p /sbin/ldconfig
%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  #This is uninstall
  rm %{_sysconfdir}/profile.d/go-exports.sh
  rm -rf /opt/go
  exit 0
fi

%files
%defattr(-,root,root)
%license LICENSE
%exclude %{goroot}/src/*.rc
%exclude %{goroot}/include/plan9
%{_sysconfdir}/profile.d/go-exports.sh
%{goroot}/*
%{gopath}/src
%exclude %{goroot}/src/pkg/debug/dwarf/testdata
%exclude %{goroot}/src/pkg/debug/elf/testdata
%{_bindir}/*

%changelog
* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.15.11-1
- Updated to version 1.15.11 to fix CVE-2021-27918

* Wed Feb 03 2021 Andrew Phelps <anphel@microsoft.com> - 1.15.7-1
- Updated to version 1.15.7 to fix CVE-2021-3114

* Mon Nov 23 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.15.5-1
- Updated to version 1.15.5

* Fri Oct 30 2020 Thomas Crain <thcrain@microsoft.com> - 1.13.15-2
- Patch CVE-2020-24553

* Tue Sep 08 2020 Nicolas Ontiveros <niontive@microsoft.com> - 1.13.15-1
- Updated to version 1.13.15, which fixes CVE-2020-14039 and CVE-2020-16845.

* Sun May 24 2020 Mateusz Malisz <mamalisz@microsoft.com> - 1.13.11-1
- Updated to version 1.13.11

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.12.5-7
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.12.5-6
- Renaming go to golang

* Thu Apr 23 2020 Nicolas Ontiveros <niontive@microsoft.com> - 1.12.5-5
- Fix CVE-2019-14809.

* Fri Mar 27 2020 Andrew Phelps <anphel@microsoft.com> - 1.12.5-4
- Support building standalone by adding go 1.4 bootstrap.

* Thu Feb 27 2020 Henry Beberman <hebeberm@microsoft.com> - 1.12.5-3
- Remove meta dependency on libc.so.6

* Thu Feb 6 2020 Andrew Phelps <anphel@microsoft.com> - 1.12.5-2
- Remove ExtraBuildRequires

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.12.5-1
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Jan 21 2019 Bo Gan <ganb@vmware.com> - 1.9.7-1
- Update to 1.9.7

* Wed Oct 24 2018 Alexey Makhalov <amakhalov@vmware.com> - 1.9.4-3
- Use extra build requires

* Mon Apr 02 2018 Dheeraj Shetty <dheerajs@vmware.com> - 1.9.4-2
- Fix for CVE-2018-7187

* Thu Mar 15 2018 Xiaolin Li <xiaolinl@vmware.com> - 1.9.4-1
- Update to golang release v1.9.4

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 1.9.1-2
- Aarch64 support

* Wed Nov 01 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 1.9.1-1
- Update to golang release v1.9.1

* Wed May 31 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.8.1-2
- Remove mercurial from buildrequires and requires.

* Tue Apr 11 2017 Danut Moraru <dmoraru@vmware.com> - 1.8.1-1
- Update Golang to version 1.8.1, updated patch0

* Wed Dec 28 2016 Xiaolin Li <xiaolinl@vmware.com> - 1.7.4-1
- Updated Golang to 1.7.4.

* Thu Oct 06 2016 ChangLee <changlee@vmware.com> - 1.6.3-2
- Modified %check

* Wed Jul 27 2016 Anish Swaminathan <anishs@vmware.com> - 1.6.3-1
- Update Golang to version 1.6.3 - fixes CVE 2016-5386

* Fri Jul 8 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 1.6.2-1
- Updated the Golang to version 1.6.2

* Thu Jun 2 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.4.2-5
- Fix script syntax

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.4.2-4
- GA - Bump release of all rpms

* Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> - 1.4.2-3
- Handling upgrade scenario pre/post/un scripts.

* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> - 1.4.2-2
- Edit post script.

* Mon Aug 03 2015 Vinay Kulkarni <kulkarniv@vmware.com> - 1.4.2-1
- Update to golang release version 1.4.2

* Fri Oct 17 2014 Divya Thaluru <dthaluru@vmware.com> - 1.3.3-1
- Initial build.  First version