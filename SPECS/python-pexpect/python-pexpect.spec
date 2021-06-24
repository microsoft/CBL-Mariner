%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%global modname pexpect
Summary:        Unicode-aware Pure Python Expect-like module
Name:           python-%{modname}
Version:        4.8.0
Release:        9%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/pexpect/pexpect
Source0:        %{url}/archive/%{version}/%{modname}-%{version}.tar.gz
BuildArch:      noarch
%if %{with_check}
BuildRequires:  man-db
BuildRequires:  openssl
%endif

%description
Pexpect is a pure Python module for spawning child applications; controlling
them; and responding to expected patterns in their output. Pexpect works like
Don Libes' Expect. Pexpect allows your script to spawn a child application and
control it as if a human were typing commands.

Pexpect can be used for automating interactive applications such as ssh, ftp,
passwd, telnet, etc. It can be used to automate setup scripts for duplicating
software package installations on different servers. And it can be used for
automated software testing. Pexpect is in the spirit of Don Libes' Expect, but
Pexpect is pure Python. Unlike other Expect-like modules for Python, Pexpect
does not require TCL or Expect nor does it require C extensions to be
compiled.  It should work on any platform that supports the standard Python
pty module.

%package -n python3-%{modname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-ptyprocess
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
Requires:       python3-ptyprocess

%description -n python3-%{modname}
Pexpect is a pure Python module for spawning child applications; controlling
them; and responding to expected patterns in their output. Pexpect works like
Don Libes' Expect. Pexpect allows your script to spawn a child application and
control it as if a human were typing commands. This package contains the
python3 version of this module.

Pexpect can be used for automating interactive applications such as ssh, ftp,
passwd, telnet, etc. It can be used to automate setup scripts for duplicating
software package installations on different servers. And it can be used for
automated software testing. Pexpect is in the spirit of Don Libes' Expect, but
Pexpect is pure Python. Unlike other Expect-like modules for Python, Pexpect
does not require TCL or Expect nor does it require C extensions to be
compiled.  It should work on any platform that supports the standard Python
pty module.

%prep
%autosetup -n %{modname}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}

%check
export PYTHONIOENCODING=UTF-8
# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1914843
# upstream: https://github.com/pexpect/pexpect/issues/669
# There's a patch upstream that we can presumable remove this after
# it merges and is released.
# Thx for the suggestion Miro: https://www.spinics.net/lists/fedora-devel/msg283026.html
echo "set enable-bracketed-paste off" > .inputrc
export INPUTRC=$PWD/.inputrc

python3 ./tools/display-sighandlers.py
python3 ./tools/display-terminalinfo.py
TRAVIS=true py.test-3 --verbose

%files -n python3-%{modname}
%license LICENSE
%doc doc examples
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-*.egg-info

%changelog
* Tue May 11 2021 Thomas Crain <thcrain@microsoft.com> - 4.8.0-9
- Remove /usr/bin/man dependency, replace with check-time man-db dependency

* Mon May 10 2021 Thomas Crain <thcrain@microsoft.com> - 4.8.0-8
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Dan Radez <dradez@redhat.com> - 4.8.0-6
- adding workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1914843
- while we wait for upstream fix: https://github.com/pexpect/pexpect/issues/669

* Wed Sep 16 2020 Kalev Lember <klember@redhat.com> - 4.8.0-5
- Avoid using bindir macro in BuildRequires

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 4.8.0-3
- Rebuilt for Python 3.9

* Wed Apr 08 2020 Scott Talbert <swt@techie.net> - 4.8.0-2
- Fix tests when building under COPR (#1822060)

* Tue Apr 07 2020 Scott Talbert <swt@techie.net> - 4.8.0-1
- Update to new upstream release 4.8.0 and re-enable tests (#1793613)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 24 2019 Dan Radez <dradez@redhat.com> - 4.7.0-4
- Remove Python2 packaging

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 4.7.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 11 2019 Dan Radez <dradez@redhat.com> - 4.7.0-1
- update to 4.7.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.6-2
- Drop explicit locale setting
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Wed Jul 25 2018 Dan Radez <dradez@redhat.com> - 4.6-1
- update to 4.6

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 4.5-2
- Rebuilt for Python 3.7

* Wed May 23 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.5.0-1
- Update to 4.5.0

* Mon Mar 12 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.4.0-1
- Update to 4.4.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 22 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.3.1-1
- Update to 4.3.1

* Fri Nov 10 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.3-1
- Update to 4.3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 14 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.2.1-1
- Update to 4.2.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 4.1.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 30 2016 Igor Gnatenko <ignatenko@redhat.com> - 4.1.0-1
- Update to 4.1.0
- Improve packaging

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Oct 18 2015 Kalev Lember <klember@redhat.com> - 4.0.1-4
- Move pexpect provides to the right subpackage

* Tue Oct 13 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.0.1-3
- Fix asyncio issue (3.4.3+)

* Thu Oct 08 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.0.1-2
- Fix RPM macroses

* Tue Oct 06 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.0.1-1
- Update to 4.0.1

* Mon Oct 05 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.0-1
- Update to 4.0
- Follow modern RPM Packaging guidelines

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Apr 08 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 3.1-1
- Update to 3.1

* Tue Nov 12 2013 Thomas Spura <tomspur@fedoraproject.org> - 3.0-1
- update to 3.0

* Wed Oct 30 2013 Thomas Spura <tomspur@fedoraproject.org> - 3.0-0.1
- new upstream is github/pexpect/pexpect
- update to rc3
- build on noarch again
- consistently use %%{buildroot} everywhere
- be more explicit in %%files
- remove CFLAGS

* Thu Sep 05 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-11
- Fix the name of the arm architecture in ExcludeArch

* Thu Sep 05 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-10
- Remove noarch because of arm build problems (bug #999174)

* Tue Aug 20 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-9
- Exclude the arm architecture (bug #999174)

* Tue Aug 20 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-8
- Bump the obsoletes version

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-5
- Exclude test scripts from the files list

* Tue Nov 20 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-4
- Moved unit tests to a check section

* Tue Nov 20 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-3
- Added unit tests and fixed metadata fields

* Tue Nov 20 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-2
- Added versions to the obsoletes and provides fields

* Tue Nov 20 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-1
- Updated to version 2.5.1 (pexpect-u fork) and added support for Python 3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 2.3-3
- Rebuild for gcc 4.4 and rpm 4.6

* Fri Dec  5 2008 Jeremy Katz <katzj@redhat.com> - 2.3-2
- Rebuild for python 2.6

* Tue Jan 08 2008 Robert Scheck <robert@fedoraproject.org> 2.3-1
- Upgrade to 2.3
- Updated the source URL to match with the guidelines

* Wed Aug 29 2007 Robert Scheck <robert@fedoraproject.org> 2.1-5
- Rebuilt (and some minor spec file tweaks)

* Sat Dec 09 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.1-4
- Bump and rebuild because I forgot to cvs up before the last build.

* Sat Dec 09 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.1-3
- Bump and rebuild for python 2.5 on devel.
- Add BR: python-devel as it provides a header necessary for python modules
  on python 2.5.

* Fri Sep 01 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.1-2
- Remove pyver define as it's not needed with the automatic python(abi).
- Stop ghosting .pyos.
- Let automatic python compilation take care of creating pyos.
- Rebuild for FC6.

* Mon Jul 17 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.1-1
- Update to 2.1.

* Thu Feb 16 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.0-2
- Bump and rebuild for FC5.
- Convert from python-abi to python(abi) requires.

* Thu Nov 17 2005 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.0-1
- Update to 2.0.

* Sat Sep 3 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 0.99999b-2
- Add LICENSE File.
- Make noarch.
- Remove executable permissions from the modules copied to examples.

* Fri Sep  2 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 0.99999b
- Update to version 0.99999b.
- Add dist tag.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Feb 03 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 0.999-2
- Use python_sitelib macro to resolve build issues on x86_64.
- %%ghost *.pyo
- Install ANSI.py, screen.py, and FSM.py into the examples.  These are intended
  to suplement pexpect eventually but they are currently much less robust and
  not installed to by default.  But they are needed by some examples.
- Use __python macro in build/install for consistency.
- Add --skip-build to the invocation of setup.py in install.

* Mon May 31 2004 Panu Matilainen <pmatilai@welho.com> 0.999-0.fdr.1
- get rid of distrel munging, buildsys does that...
- update to 0.999
- update doc and example tarballs
- fix build on python <> 2.2
- use -O1 in install to generate .pyo files instead of manually creating the files
- require python-abi = pyver to get dependencies right

* Sun Jul 27 2003 Panu Matilainen <pmatilai@welho.com> 0.98-0.fdr.3
- own .pyo files too as suggested by Ville (#517)

* Sat Jul 26 2003 Panu Matilainen <pmatilai@welho.com> 0.98-0.fdr.2
- fixes by Ville (bug #517) applied

* Sat Jul 26 2003 Panu Matilainen <pmatilai@welho.com>
- Initial Fedora packaging
