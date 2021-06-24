Summary:        library for fast, message-based applications
Name:           zeromq
Version:        4.3.4
Release:        1%{?dist}
License:        LGPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://www.zeromq.org
Source0:        https://github.com/zeromq/libzmq/releases/download/v%{version}/zeromq-%{version}.tar.gz
Requires:       libstdc++

%description
The 0MQ lightweight messaging kernel is a library which extends the standard
socket interfaces with features traditionally provided by specialised messaging
middleware products. 0MQ sockets provide an abstraction of asynchronous message
queues, multiple messaging patterns, message filtering (subscriptions), seamless
access to multiple transport protocols and more.

%package    devel
Summary:        Header and development files for zeromq
Requires:       %{name} = %{version}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -n zeromq-%{version} -p1

%build
./autogen.sh
./configure \
    --prefix=%{_prefix} \
    --with-libsodium=no \
    --without-docs \
    --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%check
make check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/
%{_libdir}/libzmq.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
%{_includedir}/

%changelog
* Thu Jun 03 2021 Nick Samson <nisamson@microsoft.com> - 4.3.4-1
- Upgraded to 4.3.4 to address CVE-2021-20236, updated URL

* Sat May 09 00:20:47 PST 2020 Nick Samson <nisamson@microsoft.com> - 4.3.2-2
- Added %%license line automatically

*   Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 4.3.2-1
-   Update to 4.3.2. Source0 URL fixed. License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.2.3-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 4.2.3-1
-   Updated to latest version

*   Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 4.1.4-3
-   Remove devpts mount

*   Mon Aug 07 2017 Chang Lee <changlee@vmware.com> 4.1.4-2
-   Fixed %check

*   Thu Apr 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.1.4-1
-   Initial build. First version
