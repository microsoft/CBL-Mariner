%define sha1    nginx-njs=fd8c3f2d219f175be958796e3beaa17f3b465126
Summary:        High-performance HTTP server and reverse proxy
Name:           nginx
Version:        1.20.1
Release:        1%{?dist}
License:        BSD 2-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://nginx.org/
Source0:        https://nginx.org/download/%{name}-%{version}.tar.gz
Source1:        nginx.service
Source2:        nginx-njs-0.2.1.tar.gz
Patch0:         CVE-2009-4487.nopatch
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  which
Provides:       %{name}-filesystem = %{version}-%{release}

%description
NGINX is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server.

%prep
%autosetup -p1
pushd ../
mkdir nginx-njs
tar -C nginx-njs -xf %{SOURCE2}
popd

%build
sh configure \
    --prefix=%{_sysconfdir}//nginx              \
    --sbin-path=%{_sbindir}/nginx                 \
    --conf-path=%{_sysconfdir}/nginx/nginx.conf           \
    --pid-path=%{_var}/run/nginx.pid               \
    --lock-path=%{_var}/run/nginx.lock             \
    --error-log-path=%{_var}/log/nginx/error.log   \
    --http-log-path=%{_var}/log/nginx/access.log   \
    --add-module=../nginx-njs/njs-0.2.1/nginx   \
    --with-http_ssl_module \
    --with-pcre \
    --with-ipv6 \
    --with-stream \
    --with-http_auth_request_module \
    --with-http_sub_module \
    --with-http_stub_status_module

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm755 %{buildroot}%{_libdir}/systemd/system
install -vdm755 %{buildroot}%{_var}/log
install -vdm755 %{buildroot}%{_var}/opt/nginx/log
ln -sfv %{_var}/opt/nginx/log %{buildroot}%{_var}/log/nginx
install -p -m 0644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system/nginx.service

%files
%defattr(-,root,root)
%license LICENSE
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi.conf
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi.conf.default
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi_params
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi_params.default
%config(noreplace) %{_sysconfdir}/%{name}/koi-utf
%config(noreplace) %{_sysconfdir}/%{name}/koi-win
%config(noreplace) %{_sysconfdir}/%{name}/mime.types
%config(noreplace) %{_sysconfdir}/%{name}/mime.types.default
%config(noreplace) %{_sysconfdir}/%{name}/nginx.conf
%config(noreplace) %{_sysconfdir}/%{name}/nginx.conf.default
%config(noreplace) %{_sysconfdir}/%{name}/scgi_params
%config(noreplace) %{_sysconfdir}/%{name}/scgi_params.default
%config(noreplace) %{_sysconfdir}/%{name}/uwsgi_params
%config(noreplace) %{_sysconfdir}/%{name}/uwsgi_params.default
%{_sysconfdir}/%{name}/win-utf
%{_sysconfdir}/%{name}/html/*
%{_sbindir}/*
%{_libdir}/systemd/system/nginx.service
%dir %{_var}/opt/nginx/log
%{_var}/log/nginx

%changelog
* Mon Jun 21 2021 Thomas Crain <thcrain@microsoft.com> - 1.20.1-1
- Merge the following releases from 1.0 to dev branch
- henry.beberman@microsoft.com, 1.20.1-1: Update to version 1.20.1 to resolve CVE-2021-23017

* Fri Apr 02 2021 Thomas Crain <thcrain@microsoft.com> - 1.16.1-4
- Merge the following releases from 1.0 to dev branch
- lihl@microsoft.com, 1.16.1-3: Used autosetup, Added patch to resolve CVE-2019-20372
- nicolasg@microsoft.com, 1.16.1-4: nopatch for CVE-2009-4487

* Wed Feb 10 2021 Henry Li <lihl@microsoft.com> - 1.16.1-3
- Add Provides for nginx-filesystem from nginx

* Sat May 09 00:21:09 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.16.1-2
- Added %%license line automatically

* Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> - 1.16.1-1
- Update to version 1.16.1. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.15.3-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Mar 15 2019 Keerthana K <keerthanak@vmware.com> - 1.15.3-4
- Enable http_stub_status_module.

* Wed Nov 07 2018 Ajay Kaher <akaher@vmware.com> - 1.15.3-3
- mark config files as non replaceable on upgrade.

* Mon Sep 17 2018 Keerthana K <keerthanak@vmware.com> - 1.15.3-2
- Adding http_auth_request_module and http_sub_module.

* Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 1.15.3-1
- Upgrade to version 1.15.3

* Fri Jul 20 2018 Keerthana K <keerthanak@vmware.com> - 1.13.8-3
- Restarting nginx on failure.

* Fri Jun 08 2018 Dheeraj Shetty <dheerajs@vmware.com> - 1.13.8-2
- adding module njs.

* Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 1.13.8-1
- Update to version 1.13.8 to support nginx-ingress

* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com> - 1.13.5-2
- Fixed the log file directory structure

* Wed Oct 04 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.13.5-1
- Update to version 1.13.5

* Mon May 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.11.13-2
- adding module stream to nginx.

* Wed Apr 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.11.13-1
- update to 1.11.13

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com> - 1.10.0-5
- Add patch for CVE-2016-4450

* Wed Jul 27 2016 Divya Thaluru<dthaluru@vmware.com> - 1.10.0-4
- Removed packaging of debug files

* Fri Jul 8 2016 Divya Thaluru<dthaluru@vmware.com> - 1.10.0-3
- Modified default pid filepath and fixed nginx systemd service

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.10.0-2
- GA - Bump release of all rpms

* Mon May 16 2016 Xiaolin Li <xiaolinl@vmware.com> - 1.10.0-1
- Initial build. First version
