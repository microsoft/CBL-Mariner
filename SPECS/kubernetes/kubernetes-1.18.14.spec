%global debug_package %{nil}
%ifarch x86_64
%define archname amd64
%endif
%ifarch aarch64
%define archname arm64
%endif
%define host_components 'kubelet kubectl kubeadm'
%define container_image_components 'kube-proxy kube-apiserver kube-controller-manager kube-scheduler'
Summary:        Microsoft Kubernetes
Name:           kubernetes
Version:        1.18.14
Release:        8%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Microsoft Kubernetes
URL:            https://mcr.microsoft.com/oss
#Source0:       https://kubernetesartifacts.azureedge.net/kubernetes/v1.18.14-hotfix.20210525/binaries/kubernetes-node-linux-amd64.tar.gz
#               Note that only amd64 tarball exist which is OK since kubernetes is built from source
Source0:        kubernetes-node-linux-amd64-%{version}-hotfix.20210525.tar.gz
Source1:        kubelet.service
Source2:        version-file-%{version}.sh
Source3:        golang-1.15-k8s-1.18-test.patch
# CVE-2020-8565 Kubernetes doc on website recommend to not enable debug level logging in production (no patch available)
Patch0:         CVE-2020-8565.nopatch
# CVE-2020-8563 Only applies when using VSphere as cloud provider,
#               Kubernetes doc on website recommend to not enable debug level logging in production (no patch available)
Patch1:         CVE-2020-8563.nopatch
BuildRequires:  flex-devel
BuildRequires:  golang >= 1.13.15
BuildRequires:  rsync
BuildRequires:  systemd-devel
BuildRequires:  which
Requires:       cni
Requires:       cri-tools
Requires:       ebtables
Requires:       ethtool
Requires:       iproute
Requires:       iptables
Requires:       moby-engine
Requires:       socat
Requires:       util-linux
Requires(postun): %{_sbindir}/groupdel
Requires(postun): %{_sbindir}/userdel
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd

%description
Microsoft Kubernetes %{version}.

%package        client
Summary:        Client utilities
Requires:       %{name} = %{version}-%{release}

%description    client
Client utilities for Microsoft Kubernetes %{version}.

%package        kubeadm
Summary:        Bootstrap utilities
Requires:       %{name} = %{version}-%{release}
Requires:       moby-cli

%description    kubeadm
Bootstrap utilities for Microsoft Kubernetes %{version}.

%package        kube-proxy
Summary:        Kubernetes proxy
Requires:       ebtables-legacy
Requires:       ethtool
Requires:       iproute
Requires:       iptables

%description    kube-proxy
Network proxy for Microsoft Kubernetes %{version}.

%package        kube-apiserver
Summary:        Kubernetes API server

%description    kube-apiserver
API server for Microsoft Kubernetes %{version}.

%package        kube-controller-manager
Summary:        Kubernetes controller manager

%description    kube-controller-manager
Controller manager for Microsoft Kubernetes %{version}.

%package        kube-scheduler
Summary:        Kubernetes scheduler

%description    kube-scheduler
Scheduler for Microsoft Kubernetes %{version}.

%package        pause
Summary:        Kubernetes pause

%description    pause
Pause component for Microsoft Kubernetes %{version}.

%prep
%setup -q -D -T -b 0 -n %{name}

%build
# expand kubernetes source tarball (which is included source0 tarball)
echo "+++ extract sources from tarball"
mkdir -p %{_builddir}/%{name}/src
cd %{_builddir}/%{name}/src
tar -xof %{_builddir}/%{name}/kubernetes-src.tar.gz

# set version information using version file
# (see k8s code: hack/lib/version.sh for more detail)
export KUBE_GIT_VERSION_FILE=%{SOURCE2}

# build host and container image related components
components_to_build=%{host_components}
for component in ${components_to_build}; do
  echo "+++ host - building ${component}"
  make WHAT=cmd/${component}
  cp -f _output/local/bin/linux/%{archname}/${component} %{_builddir}/%{name}/node/bin
done

components_to_build=%{container_image_components}
for component in ${components_to_build}; do
  echo "+++ container image - building ${component}"
  make WHAT=cmd/${component}
  cp -f _output/local/bin/linux/%{archname}/${component} %{_builddir}/%{name}/node/bin
done

# build pause
pushd build/pause
gcc -Os -Wall -Werror -static -o %{_builddir}/%{name}/node/bin/pause pause.c
strip %{_builddir}/%{name}/node/bin/pause
popd

%check
# patch test script so it supports golang 1.15 which is now used to build kubernetes
cd %{_builddir}/%{name}/src/hack/make-rules
patch -p1 test.sh < %{SOURCE3}

# perform unit tests
# Note:
#   - components are not unit tested the same way
#   - not all components have unit
cd %{_builddir}/%{name}/src
components_to_test=$(ls -1 %{_builddir}/%{name}/node/bin)

for component in ${components_to_test}; do
  if [[ ${component} == "kubelet" || ${component} == "kubectl" ]]; then
    echo "+++ unit test pkg ${component}"
    make test WHAT=./pkg/${component}
  elif [[ ${component} == "kube-proxy" ]]; then
    echo "+++ unit test pkg ${component}"
    make test WHAT=./pkg/proxy
  elif [[ ${component} == "kube-scheduler" ]]; then
    echo "+++ unit test pkg ${component}"
    make test WHAT=./pkg/scheduler
  elif [[ ${component} == "kube-apiserver" ]]; then
    echo "+++ unit test pkg ${component}"
    make test WHAT=./pkg/kubeapiserver
  elif [[ ${component} == "kube-controller-manager" ]]; then
    echo "+++ unit test pkg ${component}"
    make test WHAT=./pkg/controller
  else
    echo "+++ no unit test available for ${component}"
  fi
done

%install
# install binaries
install -m 755 -d %{buildroot}%{_bindir}
cd %{_builddir}
binaries=%{host_components}
for bin in ${binaries}; do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 -t %{buildroot}%{_bindir} %{name}/node/bin/${bin}
done

binaries=%{container_image_components}
for bin in ${binaries}; do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 -t %{buildroot}%{_bindir} %{name}/node/bin/${bin}
done

install -p -m 755 -t %{buildroot}%{_bindir} %{name}/node/bin/pause

# install service files
install -d -m 0755 %{buildroot}/%{_libdir}/systemd/system
install -p -m 644 -t %{buildroot}%{_libdir}/systemd/system %{SOURCE1}

# install config files
install -d -m 0755 %{buildroot}%{_sysconfdir}/kubernetes
install -d -m 644 %{buildroot}%{_sysconfdir}/kubernetes/manifests

# install the place the kubelet defaults to put volumes
install -dm755 %{buildroot}%{_sharedstatedir}/kubelet
install -dm755 %{buildroot}%{_var}/run/kubernetes

install -d -m 0755 %{buildroot}/%{_libdir}/tmpfiles.d
cat << EOF >> %{buildroot}/%{_libdir}/tmpfiles.d/kubernetes.conf
d %{_var}/run/kubernetes 0755 kube kube -
EOF

%clean
rm -rf %{buildroot}/*

%pre
if [ $1 -eq 1 ]; then
    # Initial installation.
    getent group kube >/dev/null || groupadd -r kube
    getent passwd kube >/dev/null || useradd -r -g kube -d / -s /sbin/nologin \
            -c "Kubernetes user" kube
fi

%post
chown -R kube:kube %{_sharedstatedir}/kubelet
chown -R kube:kube %{_var}/run/kubernetes
systemctl daemon-reload

%post kubeadm
systemctl daemon-reload
systemctl stop kubelet
systemctl enable kubelet

%postun
if [ $1 -eq 0 ]; then
    # Package deletion
    userdel kube
    groupdel kube
    systemctl daemon-reload
fi

%files
%defattr(-,root,root)
%license LICENSES
%{_bindir}/kubelet
%{_libdir}/tmpfiles.d/kubernetes.conf
%dir %{_sysconfdir}/kubernetes
%dir %{_sysconfdir}/kubernetes/manifests
%dir %{_sharedstatedir}/kubelet
%dir %{_var}/run/kubernetes
%{_libdir}/systemd/system/kubelet.service

%files client
%defattr(-,root,root)
%{_bindir}/kubectl

%files kubeadm
%defattr(-,root,root)
%{_bindir}/kubeadm

%files kube-proxy
%defattr(-,root,root)
%license LICENSES
%{_bindir}/kube-proxy

%files kube-apiserver
%defattr(-,root,root)
%license LICENSES
%{_bindir}/kube-apiserver

%files kube-controller-manager
%defattr(-,root,root)
%license LICENSES
%{_bindir}/kube-controller-manager

%files kube-scheduler
%defattr(-,root,root)
%license LICENSES
%{_bindir}/kube-scheduler

%files pause
%defattr(-,root,root)
%license LICENSES
%{_bindir}/pause

%changelog
* Wed May 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.18.14-8
- Update to version  "1.18.14-hotfix.20210525".

* Tue May 17 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.18.14-7
- Manually set version variables.

* Thu May 13 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.18.14-6
- Update to version  "1.18.14-hotfix.20210511".

* Mon May 03 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.18.14-5
- Increment release to force republishing using golang 1.15.11.

* Thu Apr 29 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.18.14-4
- Update to version  "1.18.14-hotfix.20210428".

* Mon Mar 29 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.18.14-3
- Update to version  "1.18.14-hotfix.20210322".

* Thu Mar 18 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.18.14-2
- Update to version  "1.18.14-hotfix.20210310".

* Wed Jan 20 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.18.14-1
- Move to version 1.18.14

* Fri Jan 15 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.18.8-8
- Packages for container images

* Tue Jan 05 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.18.8-7
- Fix test issue when building against golang 1.15
- CVE-2020-8563

* Mon Jan 04 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.18.8-6
- CVE-2020-8564, CVE-2020-8565, CVE-2020-8566

* Thu Dec 17 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 1.18.8-5
- Rename spec file

* Wed Dec 02 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 1.18.8-4
- Rename ms-kubernetes-1.81.8 into kubernetes and lint spec

* Wed Nov 18 2020 George Mileka <gmileka@microsoft.com> 1.18.8-3
- Added license file and macro.

* Thu Oct 29 2020 Anirudh Gopal <angop@microsoft.com> 1.18.8-2
- Update k8s to v1.18.8-hotfix.20200917 release

* Fri Oct 2 2020 George Mileka <gmileka@microsoft.com> 1.18.8-1
- Moved k8s to 1.18.8.

* Mon Aug 17 2020 Jiri Appl <jiria@microsoft.com> 1.18.6-4
- Clean up the spec.

* Thu Aug 6 2020 George Mileka <gmileka@microsoft.com> 1.18.6-3
- Create /etc/kubernetes/manifests.

* Wed Jul 30 2020 Jiri Appl <jiria@microsoft.com> 1.18.6-2
- Removed container images.

* Fri Jul 24 2020 George Mileka <gmileka@microsoft.com> 1.18.6
- Moved to 1.18.6.

* Tue Jun 30 2020 George Mileka <gmileka@microsoft.com> 1.18.2
- Adding the 1.16 knd 1.17 ubeproxy and coredns for downgrade scenarios.

* Fri Jun 05 2020 George Mileka <gmileka@microsoft.com> 1.18.2
- Switched to K8s 1.18.2.

* Thu Jun 04 2020 Nicolas Guibourge <nicolasg@microsoft.com> 1.18.0-2
- Renaming iproute2 to iproute.

* Fri May 29 2020 George Mileka <gmileka@microsoft.com> 1.18.0
- Switched to ecpacr.

* Tue Apr 14 2020 George Mileka <gmileka@microsoft.com> 1.18.0
- Original version for CBL-Mariner of K8s 1.18.0.
