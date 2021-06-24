Summary:        agent for collecting, processing, aggregating, and writing metrics.
Name:           telegraf
Version:        1.14.5
Release:        6%{?dist}
License:        MIT
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/influxdata/telegraf

#Source0:       %{url}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz

Patch0:         add-extra-metrics.patch

BuildRequires:  golang
BuildRequires:  systemd-devel

Requires:           systemd
Requires:           logrotate
Requires:           procps-ng
Requires:           shadow-utils
Requires(pre):      /usr/sbin/useradd
Requires(pre):      /usr/sbin/groupadd
Requires(postun):   /usr/sbin/userdel
Requires(postun):   /usr/sbin/groupdel

%description
Telegraf is an agent written in Go for collecting, processing, aggregating, and writing metrics.

Design goals are to have a minimal memory footprint with a plugin system so that developers in
the community can easily add support for collecting metrics from well known services (like Hadoop,
Postgres, or Redis) and third party APIs (like Mailchimp, AWS CloudWatch, or Google Analytics).

%prep
%autosetup -p1
tar -xf %{SOURCE1}

%build
go build -mod=vendor ./cmd/telegraf

%install
mkdir -pv %{buildroot}%{_sysconfdir}/%{name}/%{name}.d
install -m 755 -D %{name} %{buildroot}%{_bindir}/%{name}
install -m 755 -D scripts/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -m 755 -D etc/logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m 755 -D etc/telegraf.conf %{buildroot}%{_sysconfdir}/%{name}/telegraf.conf

%clean
rm -rf %{buildroot}/*

%pre
getent group telegraf >/dev/null || groupadd -r telegraf
getent passwd telegraf >/dev/null || useradd -c "Telegraf" -d %{_localstatedir}/lib/%{name} -g %{name} \
        -s /sbin/nologin -M -r %{name}

%post
chown -R telegraf:telegraf /etc/telegraf
%systemd_post %{name}.service
systemctl daemon-reload

%preun
%systemd_preun %{name}.service

%postun
if [ $1 -eq 0 ] ; then
    getent passwd telegraf >/dev/null && userdel telegraf
    getent group telegraf >/dev/null && groupdel telegraf
fi
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/telegraf.conf
%license LICENSE
%{_bindir}/telegraf
%{_unitdir}/telegraf.service
%{_sysconfdir}/logrotate.d/%{name}
%dir %{_sysconfdir}/%{name}/telegraf.d

%changelog
*   Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.14.5-6
-   Increment release to force republishing using golang 1.15.11.
*   Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 1.14.5-5
-   Increment release to force republishing using golang 1.15.
*   Thu Oct 15 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.14.5-4
-   License verified.
-   Added %%license macro.
-   Fixed source URL.
-   Switched to %%autosetup.
*   Fri Aug 21 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 1.14.5-3
-   Add runtime required procps-ng and shadow-utils
*   Tue Jul 14 2020 Jonathan Chiu <jochi@microsoft.com> 1.14.5-1
-   Update to version 1.14.5
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.7.4-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 1.7.4-1
-   Update version to 1.7.4 and its plugin version to 1.4.0.
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
-   Remove shadow from requires and use explicit tools for post actions
*   Tue Jul 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.4-1
-   first version
