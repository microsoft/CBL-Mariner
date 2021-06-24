Summary:        Azure IoT Edge Security Daemon
Name:           azure-iotedge
Version:        1.1.2
Release:        1%{?dist}

# A buildable azure-iotedge environments needs functioning submodules that do not work from the archive download
# To recreate the tar.gz run the following
#  sudo git clone https://github.com/Azure/iotedge.git -b %{version}
#  pushd iotedge
#  sudo git submodule update --init --recursive
#  popd
#  sudo mv iotedge azure-iotedge-%{version}
#  sudo tar -cvf azure-iotedge-%{version}.tar.gz azure-iotedge-%{version}/

#Source0:       https://github.com/Azure/iotedge/archive/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-cargo.tar.gz
License:        MIT
Group:          Applications/File
URL:            https://github.com/azure/iotedge
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  rust = 1.47.0
BuildRequires:  cmake
BuildRequires:  curl
BuildRequires:  git
BuildRequires:  shadow-utils
BuildRequires:  systemd
Requires:       libiothsm-std
Requires:       openssl
Requires:       moby-engine
Requires:       moby-cli

Patch0:         0001-set-mgmt-socket-to-var-lib.patch

%description
Azure IoT Edge Security Daemon
Azure IoT Edge is a fully managed service that delivers cloud intelligence
locally by deploying and running artificial intelligence (AI), Azure services,
and custom logic directly on cross-platform IoT devices. Run your IoT solution
securely and at scale whether in the cloud or offline.

This package contains the IoT Edge daemon and CLI tool

%define iotedge_user iotedge
%define iotedge_group %{iotedge_user}
%define iotedge_home %{_localstatedir}/lib/iotedge
%define iotedge_logdir %{_localstatedir}/log/iotedge
%define iotedge_confdir %{_sysconfdir}/iotedge
%define iotedge_datadir %{_datadir}/iotedge

%global debug_package %{nil}

%prep
# Setup .cargo directory
mkdir -p $HOME
pushd $HOME
tar xf %{SOURCE1} --no-same-owner
popd
%setup -q -n %{_topdir}/BUILD/azure-iotedge-%{version}/edgelet
%patch0 -p1

%build
cd %{_topdir}/BUILD/azure-iotedge-%{version}/edgelet

# Remove FORTIFY_SOURCE from CFLAGS to fix compilation error
CFLAGS="`echo " %{build_cflags} " | sed 's/ -Wp,-D_FORTIFY_SOURCE=2//'`"
export CFLAGS

make %{?_smp_mflags} release

%install
export PATH=$PATH:/root/.cargo/bin/
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT unitdir=%{_unitdir} docdir=%{_docdir}/iotedge-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Check for container runtime
if ! /usr/bin/getent group docker >/dev/null; then
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo ""
    echo " ERROR: No container runtime detected."
    echo ""
    echo " Please install a container runtime and run this install again."
    echo ""
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

    exit 1
fi

# Create iotedge group
if ! /usr/bin/getent group iotedge >/dev/null; then
    %{_sbindir}/groupadd -r %{iotedge_group}
fi

# Create iotedge user
if ! /usr/bin/getent passwd iotedge >/dev/null; then
    %{_sbindir}/useradd -r -g %{iotedge_group} -c "iotedge user" -s /bin/nologin -d %{iotedge_home} %{iotedge_user}
fi

if /usr/bin/getent group docker >/dev/null; then
    %{_sbindir}/usermod -a -G docker %{iotedge_user}
fi
exit 0

%post
sed -i "s/hostname: \"<ADD HOSTNAME HERE>\"/hostname: \"$(hostname)\"/g" /etc/iotedge/config.yaml
echo "==============================================================================="
echo ""
echo "                              Azure IoT Edge"
echo ""
echo "  IMPORTANT: Please update the configuration file located at:"
echo ""
echo "    /etc/iotedge/config.yaml"
echo ""
echo "  with your device's provisioning information. You will need to restart the"
echo "  'iotedge' service for these changes to take effect."
echo ""
echo "  To restart the 'iotedge' service, use:"
echo ""
echo "    'systemctl restart iotedge'"
echo ""
echo "  This command may need to be run with sudo depending on your environment."
echo ""
echo "==============================================================================="
%systemd_post iotedge.service

%preun
%systemd_preun iotedge.service

%postun
%systemd_postun_with_restart iotedge.service

%files
%defattr(-, root, root, -)
%license ../LICENSE

# bins
%{_bindir}/iotedge
%{_bindir}/iotedged

# config
%attr(400, %{iotedge_user}, %{iotedge_group}) %config(noreplace) %{iotedge_confdir}/config.yaml
%config(noreplace) %{_sysconfdir}/logrotate.d/iotedge

# man
%{_mandir}/man1/iotedge.1.gz
%{_mandir}/man8/iotedged.8.gz

# systemd
%{_unitdir}/iotedge.service

# sockets
%attr(660, %{iotedge_user}, %{iotedge_group}) %{iotedge_home}/mgmt.sock
%attr(666, %{iotedge_user}, %{iotedge_group}) %{iotedge_home}/workload.sock

# dirs
%attr(-, %{iotedge_user}, %{iotedge_group}) %dir %{iotedge_home}
%attr(-, %{iotedge_user}, %{iotedge_group}) %dir %{iotedge_logdir}

%doc %{_docdir}/iotedge-%{version}/LICENSE.gz
%doc %{_docdir}/iotedge-%{version}/ThirdPartyNotices.gz
%doc %{_docdir}/iotedge-%{version}/trademark

%changelog
* Fri May 14 2021 Andrew Phelps <anphel@microsoft.com> - 1.1.2-1
- Update to version 1.1.2

* Mon Apr 26 2021 Thomas Crain <thcrain@microsoft.com> - 1.1.0-4
- Bump release to rebuild with rust 1.47.0-3 (security update)

* Tue Apr 20 2021 Thomas Crain <thcrain@microsoft.com> - 1.1.0-3
- Bump release to rebuild with rust 1.47.0-2 (security update)

* Fri Apr 09 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.0-2
- Fixing a 'BuildRequires' typo from "==" to "=".

* Tue Feb 23 2021 Andrew Phelps <anphel@microsoft.com> - 1.1.0-1
- Update to version 1.1.0

* Sun May 31 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0.9.1-2
- Disable FORTIFY_SOURCE=2 to fix compilation error with hardened defaults.

* Wed May 27 2020 Andrew Phelps <anphel@microsoft.com> - 1.0.9.1-1
- Update to version 1.0.9.1. Fix tarball build notes.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0.9-8
- Added %%license line automatically

* Thu May 07 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 1.0.9-7
- Fix docker based build issue.

* Wed May 06 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.0.9-6
- Rename shadow to shadow-utils.

* Tue May 05 2020 Mohan Datla <mdatla@microsoft.com> - 1.0.9-5
- Add moby-engine and moby-cli dependencies

* Wed Apr 29 2020 Mohan Datla <mdatla@microsoft.com> - 1.0.9-4
- Removed dependency on docker.

* Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.9-3
- Fixed 'Source0' tag.

* Mon Apr 20 2020 Andrew Phelps <anphel@microsoft.com> - 1.0.9-2
- Support building offline with prepopulated .cargo directory.

* Thu Mar 19 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0.9-1
- Update to 1.0.9. License verified.

* Tue Dec 3 2019 Henry Beberman <hebeberm@microsoft.com> - 1.0.8.4-1
- Original version for CBL-Mariner.
