%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        A set of tools to gather troubleshooting information from a system
Name:           sos
Version:        4.1
Release:        3%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/sosreport/sos
#Source0:       https://github.com/sosreport/sos/archive/%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  gettext
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       bzip2
Requires:       python3
Requires:       python3-libxml2
Requires:       python3-pexpect
Requires:       python3-rpm
Requires:       tar
Requires:       xz
BuildArch:      noarch

%description
Sos is a set of tools that gathers information about system
hardware and configuration. The information can then be used for
diagnostic purposes and debugging. Sos is commonly used to help
support technicians and developers.

%prep
%autosetup -n %{name}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot} --install-scripts=%{_sbindir}

# Remove doubly-packaged documentation files
rm -rf %{buildroot}%{_datadir}/licenses/sos
rm -rf %{buildroot}%{_datadir}/doc/sos

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 700 %{buildroot}%{_sysconfdir}/%{name}/cleaner
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}/presets.d
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}/groups.d
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}/extras.d
install -m 644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

rm -rf %{buildroot}%{_prefix}/config/

%find_lang %{name} || echo 0

%files -f %{name}.lang
%license LICENSE
%doc AUTHORS README.md
%{_sbindir}/sos
%{_sbindir}/sosreport
%{_sbindir}/sos-collector
%dir %{_sysconfdir}/sos/cleaner
%dir %{_sysconfdir}/sos/presets.d
%dir %{_sysconfdir}/sos/extras.d
%dir %{_sysconfdir}/sos/groups.d
%{python3_sitelib}/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%config(noreplace) %{_sysconfdir}/sos/sos.conf

%changelog
* Wed May 12 2021 Thomas Crain <thcrain@microsoft.com> - 4.1-3
- Fix build break due to doubly-packaged license/doc files

* Mon May 10 2021 Thomas Crain <thcrain@microsoft.com> - 4.1-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- Linted spec to Mariner style
- License verified

* Wed Mar 10 2021 Sandro Bonazzola <sbonazzo@redhat.com> - 4.1-1
- Update to 4.1 (#1933183)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 24 2020 Sandro Bonazzola <sbonazzo@redhat.com> - 4.0-2
- Fixes BZ#1882015

* Mon Sep 14 2020 Sandro Bonazzola <sbonazzo@redhat.com> - 4.0-1
- Update to 4.0 (#1869464)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.1-2
- Rebuilt for Python 3.9

* Fri Mar 27 2020 Sandro Bonazzola <sbonazzo@redhat.com> - 3.9.1-1
- Update to 3.9.1 (#1803339)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 29 2019 Sandro Bonazzola <sbonazzo@redhat.com> - 3.8-1
- Update to 3.8 (#1747060)
- Conflicts with vdsm <= 4.30.17 (#1706060)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.7-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 28 2019 Sandro Bonazzola <sbonazzo@redhat.com> - 3.7-1
- Rebase on upstream 3.7
- Resolves: BZ#1693419

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Sandro Bonazzola <sbonazzo@redhat.com> - 3.6-3
- Rebuilt for Python 3.7

* Mon Jun 25 2018 Sandro Bonazzola <sbonazzo@redhat.com> - 3.6-2
- Upstream re-tagged the source package

* Mon Jun 25 2018 Sandro Bonazzola <sbonazzo@redhat.com> - 3.6-1
- Rebase on upstream 3.6
- Added python3-six build requirement
- Resolves: BZ#1594443

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.5.1-2
- Rebuilt for Python 3.7

* Tue May 29 2018 Sandro Bonazzola <sbonazzo@redhat.com> - 3.5.1-1
- Rebase on upstream 3.5.1
- Resolves: BZ#1583580

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 14 2017 Sandro Bonazzola <sbonazzo@fedoraproject.org> - 3.5-1
- Rebase on upstream 3.5
- Resolves: BZ#1513030

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 29 2017 Sandro Bonazzola <sbonazzo@fedoraproject.org> - 3.4-1
- Rebase on upstream 3.4
- Resolves: BZ#1436969
- Resolves: BZ#1427445

* Thu Feb 23 2017 Sandro Bonazzola <sbonazzo@fedoraproject.org> - 3.3-1
- Rebase on upstream 3.3
- Resolves: BZ#1411314

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.2-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 16 2015 Bryn M. Reeves <bmr@redhat.com> = 3.2-2
- [sosreport] ensure private temporary directory is removed
- [global] sync rawhide package with upstream
- [ceph] collect /var/lib/ceph and /var/run/ceph
- [sosreport] prepare report in a private subdirectory (CVE-2015-7529)
- [docker] collect journald logs for docker unit
- [sosreport] fix command-line report defaults
- [openstack_neutron] obfuscate server_auth in restproxy.ini
- [memory] collect swapon --show output in bytes
- [sosreport] fix command-line report defaults (proper patch ordering)
- [sapnw] call self methods properly
- [openvswitch] capture the logs, db and OVS bridges details
- [logs] fix reference to missing 'rsyslog_conf' variable
- [sapnw] Add check if saphostctrl is not present, dont use Set
- [Plugin] fix handling of symlinks in non-sysroot environments
- [openstack] Ensure openstack passwords and secrets are obfuscated
- [plugin] pass stderr through _collect_cmd_output
- [kubernetes,plugin] Support running sos inside a container
- [openstack] New Openstack Trove (DBaaS) plugin
- [services] Add more diagnostics to applications
- [openstack_neutron] Obscure passwords and secrets
- [ceph] add calamari and ragos logs and configs
- [iprconfig] enable plugin for ppc64* architectures
- [general] verify --profile contains valid plugins only
- [kernel,mpt,memory] additional kernel-related diagnostics
- [cluster] enable crm_report password scrubbing
- [sosreport] fix command-line report defaults
- [virsh] add new plugin, add listing of qemu
- [sap*,vhostmd] new plugins for SAP
- [cluster] crm_report fails to run because dir already exists
- [foreman] Skip collection of generic resources
- [apache] Added collection of conf.modules.d dir for httpd 2.4
- [pcp] collect /etc/pcp.conf
- [puppet] adding new plugin for puppet
- [block] Don't use parted human readable output
- [general] Better handling --name and --ticket-number in
- [networking] additional ip, firewall and traffic shaping
- [infiniband] add opensm and infiniband-diags support
- [plugins/rabbitmq] Added cluster_status command output
- [networking] re-add 'ip addr' with a root symlink
- [kimchi] add new plugin
- [iprconfig] add plugin for IBM Power RAID adapters
- [ovirt] Collect engine tunables and domain information.
- [activemq] Honour all_logs and get config on RHEL
- [cluster] Add luci to packages for standalone luci servers
- [hpasm] hpasmcli commands hang under timeout
- [mysql] Collect log file
- [chrony] add chrony plugin
- [openstack_sahara] redact secrets from sahara configuration
- [openstack_sahara] add new openstack_sahara plugin
- [openstack_neutron] neutron configuration and logs files not captured
- [ovirt] remove ovirt-engine setup answer file password leak
- [networking] network plugin fails if NetworkManager is disabled
- [cluster] crm_report fails to run because dir already exists
- [mysql] improve handling of dbuser, dbpass and MYSQL_PWD
- [mysql] test for boolean values in dbuser and dbpass
- [plugin] limit path names to PC_NAME_MAX
- [squid] collect files from /var/log/squid
- [sosreport] log plugin exceptions to a file
- [ctdb] fix collection of /etc/sysconfig/ctdb
- [sosreport] fix silent exception handling
- [sosreport] do not make logging calls after OSError
- [sosreport] catch OSError exceptions in SoSReport.execute()
- [anaconda] make useradd password regex tolerant of whitespace
- [mysql] fix handling of mysql.dbpass option
- [navicli] catch exceptions if stdin is unreadable
- [docs] update man page for new options
- [sosreport] make all utf-8 handling user errors=ignore
- [kpatch] do not attempt to collect data if kpatch is not installed
- [archive] drop support for Zip archives
- [sosreport] fix archive permissions regression
- [tomcat] add support for tomcat7 and default log size limits
- [mysql] obtain database password from the environment
- [corosync] add postprocessing for corosync-objctl output
- [ovirt_hosted_engine] fix exception when force-enabled
- [yum] call rhsm-debug with --no-subscriptions
- [powerpc] allow PowerPC plugin to run on ppc64le
- [package] add Obsoletes for sos-plugins-openstack
- [pam] add pam_tally2 and faillock support
- [postgresql] obtain db password from the environment
- [pcp] add Performance Co-Pilot plugin
- [nfsserver] collect /etc/exports.d
- [sosreport] handle --compression-type correctly
- [anaconda] redact passwords in kickstart configurations
- [haproxy] add new plugin
- [keepalived] add new plugin
- [lvm2] set locking_type=0 when calling lvm commands
- [tuned] add new plugin
- [cgroups] collect /etc/sysconfig/cgred
- [plugins] ensure doc text is always displayed for plugins
- [sosreport] fix the distribution version API call
- [docker] add new plugin
- [openstack_*] include broken-out openstack plugins
- [mysql] support MariaDB
- [openstack] do not collect /var/lib/nova
- [grub2] collect grub.cfg on UEFI systems
- [sosreport] handle out-of-space errors gracefully
- [firewalld] new plugin
- [networking] collect NetworkManager status
- [kpatch] new plugin
- [global] update to upstream 3.2 release
- [foreman] add new plugin

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-0.4.a
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Jul 17 2015 Miro Hrončok <mhroncok@redhat.com> - 3.2-0.3.a
- Use Python 3 (#1014595)
- Use setup.py instead of make
- Remove some deprecated statements

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-0.2.a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 17 2014 Bryn M. Reeves <bmr@redhat.com> = 3.2-0.1.a
- Make source URL handling compliant with packaging guidelines
- Update to new upstream pre-release sos-3.2-alpha1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 01 2014 Bryn M. Reeves <bmr@redhat.com> = 3.1-1
- Update to new upstream release sos-3.1
- Add collection of grub configuration for UEFI systems
- Raise a TypeError if add_copy_specs() is called with a string
- Add tests for Plugin.add_copy_spec()/add_copy_specs()
- Update Plugin tests to treat copy_paths as a set
- Use a set for Plugin.copy_paths
- Remove references to 'sub' parameter from plugin tests
- Remove 'sub' parameter from Plugin.add_copy_spec*()
- Drop RedHatPlugin from procenv
- Update plugin_tests.py to match new method names
- Remove obsolete checksum reference from utilities_tests.py
- Refactor Plugin.collect() pathway
- Fix x86 arch detection in processor plugin
- Pythonify Plugin._path_in_pathlist()
- Clean up package checks in processor plugin
- Replace self.policy().pkg_by_name() us in Logs plugin
- Convert infiniband to package list
- Dead code removal: PluginException
- Dead code removal: sos.plugins.common_prefix()
- Add vim tags to all python source files
- Dead code removal: utilities.checksum()
- Dead code removal: DirTree
- Dead code removal: sos_relative_path()
- Remove --profile support
- Fix plugin_test exception on six.PY2
- Call rhsm-debug with the --sos switch
- Do not collect isos in cobbler plugin
- Match plugins against policies
- Update policy_tests.py for validate_plugin change
- Rename validatePlugin to validate_plugin
- Fix broken binary detection in satellite plugin
- Clean up get_cmd_path/make_cmd_path/make_cmd_dirs mess
- Add tuned plugin
- Update systemd support
- Fix remaining use of obsolete 'get_cmd_dir()' in plugins
- Add PowerNV specific debug data
- powerpc: Move VPD related tool under common code
- Remove the rhevm plugin.
- Replace package check with file check in anacron
- Scrub ldap_default_authtok password in sssd plugin
- Eliminate hard-coded /var/log/sa paths in sar plugin
- Remove useless check_enabled() from sar plugin
- Improve error message when cluster.crm_from is invalid
- Fix command output substitution exception
- Add distupgrade plugin
- Fix gluster volume name extraction
- Ensure unused fds are closed when calling subprocesses via Popen
- Pass --no-archive to rhsm-debug script
- postgresql: allow use TCP socket
- postgresql: added license and copyright
- postgresql: add logs about errors / warnings
- postgresql: minor fixes
- Include geo-replication status in gluster plugin
- Make get_cmd_output_now() behaviour match 2.2
- Add rhsm-debug collection to yum plugin
- Always treat rhevm vdsmlogs option as string
- Fix verbose file logging
- Fix get_option() use in cluster plugin
- Fix cluster postproc regression
- Ensure superclass postproc method is called in ldap plugin
- Remove obsolete diagnostics code from ldap plugin
- Fix cluster module crm_report support

* Thu Mar 20 2014 Bryn M. Reeves <bmr@redhat.com> = 3.0-23
- Call rhsm-debug with the --sos switch

* Mon Mar 03 2014 Bryn M. Reeves <bmr@redhat.com>
- Fix package check in anacron plugin

* Wed Feb 12 2014 Bryn M. Reeves <bmr@redhat.com>
- Remove obsolete rhel_version() usage from yum plugin

* Tue Feb 11 2014 Bryn M. Reeves <bmr@redhat.com>
- Prevent unhandled exception during command output substitution

* Mon Feb 10 2014 Bryn M. Reeves <bmr@redhat.com>
- Fix generation of volume names in gluster plugin
- Add distupgrade plugin

* Tue Feb 04 2014 Bryn M. Reeves <bmr@redhat.com>
- Prevent file descriptor leaks when using Popen
- Disable zip archive creation when running rhsm-debug
- Include volume geo-replication status in gluster plugin

* Mon Feb 03 2014 Bryn M. Reeves <bmr@redhat.com>
- Fix get_option use in cluster plugin
- Fix debug logging to file when given '-v'
- Always treat rhevm plugin's vdsmlogs option as a string
- Run the rhsm-debug script from yum plugin

* Fri Jan 31 2014 Bryn M. Reeves <bmr@redhat.com>
- Add new plugin to collect OpenHPI configuration
- Fix cluster plugin crm_report support
- Fix file postprocessing in ldap plugin
- Remove collection of anaconda-ks.cfg from general plugin

* Fri Jan 24 2014 Bryn M. Reeves <bmr@redhat.com>
- Remove debug statements from logs plugin
- Make ethernet interface detection more robust
- Fix specifying multiple plugin options on the command line
- Make log and message levels match previous versions
- Log a warning message when external commands time out
- Remove --upload command line option
- Update sos UI text to match upstream

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com>
- Mass rebuild 2013-12-27

* Thu Nov 14 2013 Bryn M. Reeves <bmr@redhat.com>
- Fix regressions introduced with --build option

* Tue Nov 12 2013 Bryn M. Reeves <bmr@redhat.com>
- Fix typo in yum plug-in add_forbidden_paths
- Add krb5 plug-in and drop collection of krb5.keytab

* Fri Nov  8 2013 Bryn M. Reeves <bmr@redhat.com>
- Add nfs client plug-in
- Fix traceback when sar module force-enabled

* Thu Nov  7 2013 Bryn M. Reeves <bmr@redhat.com>
- Restore --build command line option
- Collect saved vmcore-dmesg.txt files
- Normalize temporary directory paths

* Tue Nov  5 2013 Bryn M. Reeves <bmr@redhat.com>
- Add domainname output to NIS plug-in
- Collect /var/log/squid in squid plug-in
- Collect mountstats and mountinfo in filesys plug-in
- Add PowerPC plug-in from upstream

* Thu Oct 31 2013 Bryn M. Reeves <bmr@redhat.com>
- Remove version checks in gluster plug-in
- Check for usable temporary directory
- Fix --alloptions command line option
- Fix configuration fail regression

* Wed Oct 30 2013 Bryn M. Reeves <bmr@redhat.com>
- Include /etc/yaboot.conf in boot plug-in
- Fix collection of brctl output in networking plug-in
- Verify limited set of RPM packages by default
- Do not strip newlines from command output
- Limit default sar data collection

* Thu Oct 3 2013 Bryn M. Reeves <bmr@redhat.com>
- Do not attempt to read RPC pseudo files in networking plug-in
- Restrict wbinfo collection to the current domain
- Add obfuscation of luci secrets to cluster plug-in
- Add XFS plug-in
- Fix policy class handling of --tmp-dir
- Do not set batch mode if stdin is not a TTY
- Attempt to continue when reading bad input in interactive mode

* Wed Aug 14 2013 Bryn M. Reeves <bmr@redhat.com>
- Add crm_report support to cluster plug-in
- Fix rhel_version() usage in cluster and s390 plug-ins
- Strip trailing newline from command output

* Mon Jun 10 2013 Bryn M. Reeves <bmr@redhat.com>
- Silence 'could not run' messages at default verbosity
- New upstream release

* Thu May 23 2013 Bryn M. Reeves <bmr@redhat.com>
- Always invoke tar with '-f-' option

* Mon Jan 21 2013 Bryn M. Reeves <bmr@redhat.com>
- Fix interactive mode regression when --ticket unspecified

* Fri Jan 18 2013 Bryn M. Reeves <bmr@redhat.com>
- Fix propagation of --ticket parameter in interactive mode

* Thu Jan 17 2013 Bryn M. Reeves <bmr@redhat.com>
- Revert OpenStack patch

* Wed Jan  9 2013 Bryn M. Reeves <bmr@redhat.com>
- Report --name and --ticket values as defaults
- Fix device-mapper command execution logging
- Fix data collection and rename PostreSQL module to pgsql

* Fri Oct 19 2012 Bryn M. Reeves <bmr@redhat.com>
- Add support for content delivery hosts to RHUI module

* Thu Oct 18 2012 Bryn M. Reeves <bmr@redhat.com>
- Add Red Hat Update Infrastructure module
- Collect /proc/iomem in hardware module
- Collect subscription-manager output in general module
- Collect rhsm log files in general module
- Fix exception in gluster module on non-gluster systems
- Fix exception in psql module when dbname is not given

* Wed Oct 17 2012 Bryn M. Reeves <bmr@redhat.com>
- Collect /proc/pagetypeinfo in memory module
- Strip trailing newline from command output
- Add sanlock module
- Do not collect archived accounting files in psacct module
- Call spacewalk-debug from rhn module to collect satellite data

* Mon Oct 15 2012 Bryn M. Reeves <bmr@redhat.com>
- Avoid calling volume status when collecting gluster statedumps
- Use a default report name if --name is empty
- Quote tilde characters passed to shell in RPM module
- Collect KDC and named configuration in ipa module
- Sanitize hostname characters before using as report path
- Collect /etc/multipath in device-mapper module
- New plug-in for PostgreSQL
- Add OpenStack module
- Avoid deprecated sysctls in /proc/sys/net
- Fix error logging when calling external programs
- Use ip instead of ifconfig to generate network interface lists

* Wed May 23 2012 Bryn M. Reeves <bmr@redhat.com>
- Collect the swift configuration directory in gluster module
- Update IPA module and related plug-ins

* Fri May 18 2012 Bryn M. Reeves <bmr@redhat.com>
- Collect mcelog files in the hardware module

* Wed May 02 2012 Bryn M. Reeves <bmr@redhat.com>
- Add nfs statedump collection to gluster module

* Tue May 01 2012 Bryn M. Reeves <bmr@redhat.com>
- Use wildcard to match possible libvirt log paths

* Mon Apr 23 2012 Bryn M. Reeves <bmr@redhat.com>
- Add forbidden paths for new location of gluster private keys

* Fri Mar  9 2012 Bryn M. Reeves <bmr@redhat.com>
- Fix katello and aeolus command string syntax
- Remove stray hunk from gluster module patch

* Thu Mar  8 2012 Bryn M. Reeves <bmr@redhat.com>
- Correct aeolus debug invocation in CloudForms module
- Update gluster module for gluster-3.3
- Add additional command output to gluster module
- Add support for collecting gluster configuration and logs

* Wed Mar  7 2012 Bryn M. Reeves <bmr@redhat.com>
- Collect additional diagnostic information for realtime systems
- Improve sanitization of RHN user and case number in report name
- Fix verbose output and debug logging
- Add basic support for CloudForms data collection
- Add support for Subscription Asset Manager diagnostics

* Tue Mar  6 2012 Bryn M. Reeves <bmr@redhat.com>
- Collect fence_virt.conf in cluster module
- Fix collection of /proc/net directory tree
- Gather output of cpufreq-info when present
- Fix brctl showstp output when bridges contain multiple interfaces
- Add /etc/modprobe.d to kernel module
- Ensure relative symlink targets are correctly handled when copying
- Fix satellite and proxy package detection in rhn plugin
- Collect stderr output from external commands
- Collect /proc/cgroups in the cgroups module
  Resolve: bz784874
- Collect /proc/irq in the kernel module
- Fix installed-rpms formatting for long package names
- Add symbolic links for truncated log files
- Collect non-standard syslog and rsyslog log files
- Use correct paths for tomcat6 in RHN module
- Obscure root password if present in anacond-ks.cfg
- Do not accept embedded forward slashes in RHN usernames
- Add new sunrpc module to collect rpcinfo for gluster systems

* Tue Nov  1 2011 Bryn M. Reeves <bmr@redhat.com>
- Do not collect subscription manager keys in general plugin

* Fri Sep 23 2011 Bryn M. Reeves <bmr@redhat.com>
- Fix execution of RHN hardware.py from hardware plugin
- Fix hardware plugin to support new lsusb path

* Fri Sep 09 2011 Bryn M. Reeves <bmr@redhat.com>
- Fix brctl collection when a bridge contains no interfaces
- Fix up2dateclient path in hardware plugin

* Mon Aug 15 2011 Bryn M. Reeves <bmr@redhat.com>
- Collect brctl show and showstp output
- Collect nslcd.conf in ldap plugin

* Sun Aug 14 2011 Bryn M. Reeves <bmr@redhat.com>
- Truncate files that exceed specified size limit
- Add support for collecting Red Hat Subscrition Manager configuration
- Collect /etc/init on systems using upstart
- Don't strip whitespace from output of external programs
- Collect ipv6 neighbour table in network module
- Collect basic cgroups configuration data

* Sat Aug 13 2011 Bryn M. Reeves <bmr@redhat.com>
- Fix collection of data from LVM2 reporting tools in devicemapper plugin
- Add /proc/vmmemctl collection to vmware plugin

* Fri Aug 12 2011 Bryn M. Reeves <bmr@redhat.com>
- Collect yum repository list by default
- Add basic Infiniband plugin
- Add plugin for scsi-target-utils iSCSI target
- Fix autofs plugin LC_ALL usage
- Fix collection of lsusb and add collection of -t and -v outputs
- Extend data collection by qpidd plugin
- Add ethtool pause, coalesce and ring (-a, -c, -g) options to network plugin

* Thu Apr 07 2011 Bryn M. Reeves <bmr@redhat.com>
- Use sha256 for report digest when operating in FIPS mode

* Tue Apr 05 2011 Bryn M. Reeves <bmr@redhat.com>
- Fix parted and dumpe2fs output on s390

* Fri Feb 25 2011 Bryn M. Reeves <bmr@redhat.com>
- Fix collection of chkconfig output in startup.py
- Collect /etc/dhcp in dhcp.py plugin
- Collect dmsetup ls --tree output in devicemapper.py
- Collect lsblk output in filesys.py

* Thu Feb 24 2011 Bryn M. Reeves <bmr@redhat.com>
- Fix collection of logs and config files in sssd.py
- Add support for collecting entitlement certificates in rhn.py

* Thu Feb 03 2011 Bryn M. Reeves <bmr@redhat.com>
- Fix cluster plugin dlm lockdump for el6
- Add sssd plugin to collect configuration and logs
- Collect /etc/anacrontab in system plugin
- Correct handling of redhat-release for el6

* Thu Jul 29 2010 Adam Stokes <ajs at redhat dot com>

* Thu Jun 10 2010 Adam Stokes <ajs at redhat dot com>

* Wed Apr 28 2010 Adam Stokes <ajs at redhat dot com>

* Mon Apr 12 2010 Adam Stokes <ajs at redhat dot com>

* Tue Mar 30 2010 Adam Stokes <ajs at redhat dot com>
- fix setup.py to autocompile translations and man pages
- rebase 1.9

* Fri Mar 19 2010 Adam Stokes <ajs at redhat dot com>
- updated translations

* Thu Mar 04 2010 Adam Stokes <ajs at redhat dot com>
- version bump 1.9
- replaced compression utility with xz
- strip threading/multiprocessing
- simplified progress indicator
- pylint update
- put global vars in class container
- unittests
- simple profiling
- make use of xgettext as pygettext is deprecated

* Mon Jan 18 2010 Adam Stokes <ajs at redhat dot com>
- more sanitizing options for log files
- rhbz fixes from RHEL version merged into trunk
- progressbar update
