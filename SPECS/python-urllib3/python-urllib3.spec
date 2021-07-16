%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        A powerful, sanity-friendly HTTP client for Python.
Name:           python-urllib3
Version:        1.25.9
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/urllib3
Source0:        https://github.com/shazow/urllib3/archive/%{version}/urllib3-%{version}.tar.gz
Patch0: CVE-2021-33503.patch
BuildRequires:  curl-devel
#%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  python-pip
BuildRequires:  python-psutil
BuildRequires:  python-setuptools
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
#%endif
Requires:       python2
Requires:       python2-libs
BuildArch:      noarch

%description
urllib3 is a powerful, sanity-friendly HTTP client for Python. Much of the Python ecosystem already uses urllib3 and you should too.

%package -n     python3-urllib3
Summary:        python-urllib3
Requires:       python3
Requires:       python3-libs

%description -n python3-urllib3
Python 3 version.

%prep
%autosetup -n urllib3-%{version}
# Dummyserver tests are failing when running in chroot. So disabling the tests.
rm -rf test/with_dummyserver/

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check

nofiles=$(ulimit -n)
ulimit -n 5000
pip2 install -r dev-requirements.txt
pip3 install -r dev-requirements.txt

ignoretestslist='not test_select_interrupt_exception and not test_selector_error and not timeout and not test_request_host_header_ignores_fqdn_dot and not test_dotted_fqdn'
case $(uname -m) in
ppc*)
ignoretestslist="$ignoretestslist and not test_select_timing and not test_select_multiple_interrupts_with_event and not test_interrupt_wait_for_read_with_event and not test_select_interrupt_with_event";;
esac

PYTHONPATH="%{buildroot}%{$python2_sitelib}" pytest \
                --ignore=test/appengine \
                --ignore=test/with_dummyserver/test_proxy_poolmanager.py \
                --ignore=test/with_dummyserver/test_poolmanager.py \
                --ignore=test/contrib/test_pyopenssl.py \
                --ignore=test/contrib/test_securetransport.py \
                -k "${ignoretestslist}" \
                urllib3 test


PYTHONPATH="%{buildroot}%{$python3_sitelib}" pytest \
                --ignore=test/appengine \
                --ignore=test/with_dummyserver/test_proxy_poolmanager.py \
                --ignore=test/with_dummyserver/test_poolmanager.py \
                --ignore=test/contrib/test_pyopenssl.py \
                --ignore=test/contrib/test_securetransport.py \
                -k "${ignoretestslist}" \
                urllib3 test
ulimit -n $nofiles


%files
%defattr(-,root,root)
%license LICENSE.txt
%{python2_sitelib}/*

%files -n python3-urllib3
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sat Jul 03 2021 Mariner Autopatcher <cblmargh@microsoft.com> 1.25.9-2
-   Added patch file(s) CVE-2021-33503.patch
* Wed Dec 23 2020 Rachel Menge <rachelmenge@microsoft.com> - 1.25.9-1
- Updated to version 1.25.9

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.24.2-2
- Added %%license line automatically

* Thu Mar 19 2020 Paul Monson <paulmon@microsoft.com> - 1.24.2-1
- Update to version 1.24.2. Updated Source0 URL. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.23-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> - 1.23-2
- Fix make check

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 1.23-1
- Update to version 1.23

* Tue Aug 15 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.20-5
- Increased number of open files per process to 5000 before run make check.

* Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> - 1.20-4
- Fixed rpm check errors

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.20-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.20-2
- Use python2 explicitly

* Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.20-1
- Initial packaging for Photon
