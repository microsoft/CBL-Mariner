Summary:        A high performance C-based HTTP client library built upon the Apache Portable Runtime (APR) library
Name:           libserf
Version:        1.3.9
Release:        6%{?dist}
License:        ASL 2.0
URL:            https://serf.apache.org/
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://www.apache.org/dist/serf/serf-%{version}.tar.bz2
Requires:       openldap
BuildRequires:  apr-devel
BuildRequires:  apr-util-devel
BuildRequires:  scons
BuildRequires:  openssl-devel
BuildRequires:  openldap

%description
The Apache Serf library is a C-based HTTP client library built upon the Apache
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations are
kept to a minimum to provide high performance operation.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}
%description    devel
It contains the libraries and header files to create serf applications.

%prep
%setup -q -n serf-%{version}

%build
scons PREFIX=%{_prefix}

%install
scons PREFIX=%{buildroot}%{_prefix} install

%check
# The source tarball contains an expired cert, leading to 14 test failures. Skip these tests.
sed -i '/SUITE_ADD_TEST(suite, test_ssl_trust_rootca);/d' ./test/test_context.c
sed -i '/SUITE_ADD_TEST(suite, test_ssl_certificate_chain_with_anchor);/d' ./test/test_context.c
sed -i '/SUITE_ADD_TEST(suite, test_ssl_certificate_chain_all_from_server);/d' ./test/test_context.c
sed -i '/SUITE_ADD_TEST(suite, test_ssl_no_servercert_callback_allok);/d' ./test/test_context.c
sed -i '/SUITE_ADD_TEST(suite, test_ssl_large_response);/d' ./test/test_context.c
sed -i '/SUITE_ADD_TEST(suite, test_ssl_large_request);/d' ./test/test_context.c
sed -i '/SUITE_ADD_TEST(suite, test_ssl_client_certificate);/d' ./test/test_context.c
sed -i '/SUITE_ADD_TEST(suite, test_ssl_future_server_cert);/d' ./test/test_context.c
sed -i '/SUITE_ADD_TEST(suite, test_setup_ssltunnel);/d' ./test/test_context.c
sed -i '/SUITE_ADD_TEST(suite, test_ssltunnel_basic_auth);/d' ./test/test_context.c
sed -i '/SUITE_ADD_TEST(suite, test_ssltunnel_basic_auth_server_has_keepalive_off);/d' ./test/test_context.c
sed -i '/SUITE_ADD_TEST(suite, test_ssltunnel_basic_auth_proxy_has_keepalive_off);/d' ./test/test_context.c
sed -i '/SUITE_ADD_TEST(suite, test_ssltunnel_basic_auth_proxy_close_conn_on_200resp);/d' ./test/test_context.c
sed -i '/SUITE_ADD_TEST(suite, test_ssltunnel_digest_auth);/d' ./test/test_context.c

# OpenSSL 1.1.1i+ breaks test_ssl_handshake, so disable test_ssl_handshake
sed -i '/SUITE_ADD_TEST(suite, test_ssl_handshake);/d' ./test/test_context.c
scons check

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/libserf-1.so.*

%files devel
%{_includedir}/*
%{_libdir}/libserf-1.so
%{_libdir}/libserf-1.a
%{_libdir}/pkgconfig/*


%changelog
*   Tue May 04 2021 Nicolas Ontiveros <niontive@microsoft.com> 1.3.9-6
-   Disable test_ssl_handshake

*   Mon Dec 07 2020 Andrew Phelps <anphel@microsoft.com> 1.3.9-5
-   Fix check tests.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.3.9-4
-   Added %%license line automatically
*   Mon Apr 13 2020 Emre Girgin <mrgirgin@microsoft.com? 1.3.9-3
-   Rename the package to libserf.
-   Update license. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.3.9-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Jan 22 2018 Xiaolin Li <xiaolinl@vmware.com> 1.3.9-1
-   Initial build. First version
