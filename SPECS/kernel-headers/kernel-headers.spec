Summary:        Linux API header files
Name:           kernel-headers
Version:        5.10.42.1
Release:        4%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
#Source0:       https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner/%%{version}.tar.gz
Source0:        kernel-%{version}.tar.gz
BuildArch:      noarch

%description
The Linux API Headers expose the kernel's API for use by Glibc.

%prep
%setup -q -n CBL-Mariner-Linux-Kernel-rolling-lts-mariner-%{version}

%build
make mrproper
make headers_check

%install
cd %{_builddir}/CBL-Mariner-Linux-Kernel-rolling-lts-mariner-%{version}
make headers
find usr/include -name '.*' -delete
rm usr/include/Makefile
mkdir -p /%{buildroot}%{_includedir}
cp -rv usr/include/* /%{buildroot}%{_includedir}

%files
%defattr(-,root,root)
%license COPYING
%{_includedir}/*

%changelog
* Wed Jun 30 2021 Chris Co <chrco@microsoft.com> - 5.10.42.1-4
- Bump release number to match kernel release

* Tue Jun 22 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.10.42.1-3
- Bump release number to match kernel release

* Wed Jun 16 2021 Chris Co <chrco@microsoft.com> - 5.10.42.1-2
- Bump release number to match kernel release

* Tue Jun 08 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.42.1-1
- Update source to 5.10.42.1

* Thu Jun 03 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.37.1-2
- Bump release number to match kernel release

* Fri May 28 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.37.1-1
- Update source to 5.10.37.1

* Thu May 27 2021 Chris Co <chrco@microsoft.com> - 5.10.32.1-7
- Bump release number to match kernel release

* Wed May 26 2021 Chris Co <chrco@microsoft.com> - 5.10.32.1-6
- Bump release number to match kernel release

* Tue May 25 2021 Daniel Mihai <dmihai@microsoft.com> - 5.10.32.1-5
- Bump release number to match kernel release

* Thu May 20 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.10.32.1-4
- Bump release number to match kernel-signed update

* Tue May 17 2021 Andrew Phelps <anphel@microsoft.com> - 5.10.32.1-3
- Bump release number to match kernel release

* Thu May 13 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.32.1-2
- Bump release number to match kernel release

* Mon May 03 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.32.1-1
- Update source to 5.10.32.1

* Thu Apr 22 2021 Chris Co <chrco@microsoft.com> - 5.10.28.1-4
- Bump release number to match kernel release

* Mon Apr 19 2021 Chris Co <chrco@microsoft.com> - 5.10.28.1-3
- Bump release number to match kernel-signed update

* Thu Apr 15 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.28.1-2
- Update to kernel release 5.10.28.1-2

* Thu Apr 08 2021 Chris Co <chrco@microsoft.com> - 5.10.28.1-1
- Update source to 5.10.28.1

* Fri Mar 26 2021 Daniel Mihai <dmihai@microsoft.com> - 5.10.21.1-4
- Update to kernel release 5.10.21.1-4

* Thu Mar 18 2021 Chris Co <chrco@microsoft.com> - 5.10.21.1-3
- Update to kernel release 5.10.21.1-3

* Wed Mar 17 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.10.21.1-2
- Update to kernel release 5.10.21.1-2

* Thu Mar 11 2021 Chris Co <chrco@microsoft.com> - 5.10.21.1-1
- Update source to 5.10.21.1

* Fri Mar 05 2021 Chris Co <chrco@microsoft.com> - 5.10.13.1-4
- Update to kernel release 5.10.13.1-4

* Thu Mar 04 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.10.13.1-3
- Update to kernel release 5.10.13.1-3

* Mon Feb 22 2021 Thomas Crain <thcrain@microsoft.com> - 5.10.13.1-2
- Update to kernel release 5.10.13.1-2

* Thu Feb 18 2021 Chris Co <chrco@microsoft.com> - 5.10.13.1-1
- Update source to 5.10.13.1

* Tue Feb 16 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.91-5
- Update to kernel release 5.4.91-5

* Tue Feb 09 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.91-4
- Update to kernel release 5.4.91-4

* Thu Jan 28 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.91-3
- Update to kernel release 5.4.91-3

* Thu Jan 28 2021 Daniel McIlvaney <damcilva@microsoft.com> - 5.4.91-2
- Update release number to match kernel spec

* Wed Jan 20 2021 Chris Co <chrco@microsoft.com> - 5.4.91-1
- Update source to 5.4.91

* Tue Jan 12 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.4.83-4
- Update release number to match kernel spec

* Sat Jan 09 2021 Andrew Phelps <anphel@microsoft.com> - 5.4.83-3
- Update to kernel release 5.4.83-3

* Mon Dec 28 2020 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.83-2
- Update to kernel release 5.4.83-2

* Tue Dec 15 2020 Henry Beberman <henry.beberman@microsoft.com> - 5.4.83-1
- Update source to 5.4.83

* Fri Dec 04 2020 Chris Co <chrco@microsoft.com> - 5.4.81-1
- Update source to 5.4.81

* Mon Oct 26 2020 Chris Co <chrco@microsoft.com> - 5.4.72-1
- Update source to 5.4.72
- Add license file
- Lint spec

* Tue Sep 01 2020 Chris Co <chrco@microsoft.com> - 5.4.51-2
- Update source hash

* Wed Aug 19 2020 Chris Co <chrco@microsoft.com> - 5.4.51-1
- Update source to 5.4.51

* Fri Jun 12 2020 Chris Co <chrco@microsoft.com> - 5.4.42-1
- Update source to 5.4.42

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 5.4.23-2
- Renaming linux-api-headers to kernel-headers

* Tue Dec 10 2019 Chris Co <chrco@microsoft.com> - 5.4.23-1
- Update to Microsoft Linux Kernel 5.4.23.
- Use make headers since with 5.4, headers_install now requires rsync.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.19.52-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
- Update to version 4.19.52

* Tue May 07 2019 Ajay Kaher <akaher@vmware.com> - 4.19.40-1
- Update to version 4.19.40

* Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
- Update to version 4.19.32

* Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
- Update to version 4.19.29

* Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> - 4.19.26-1
- Update to version 4.19.26

* Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
- Update to version 4.19.15

* Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
- Update to version 4.19.6

* Mon Nov 05 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
- Update to version 4.19.1

* Thu Sep 20 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
- Update to version 4.18.9

* Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
- Update to version 4.14.67

* Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 4.14.54-1
- Update to version 4.14.54

* Fri Dec 22 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.14.8-1
- Version update

* Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
- Version update

* Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
- Version update

* Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
- Version update

* Thu Oct 05 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-1
- Version update

* Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-1
- Version update

* Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.47-1
- Version update

* Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.43-1
- Version update

* Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.34-1
- Version update

* Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.30-1
- Version update

* Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.28-1
- Version update

* Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.27-1
- Update to linux-4.9.27

* Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.26-1
- Update to linux-4.9.26

* Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.24-1
- Update to linux-4.9.24

* Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.13-1
- Update to linux-4.9.13

* Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.9-1
- Update to linux-4.9.9

* Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.2-1
- Update to linux-4.9.2

* Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.9.0-1
- Update to linux-4.9.0

* Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.4.35-1
- Update to linux-4.4.35

* Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.4.31-1
- Update to linux-4.4.31

* Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.4.20-1
- Update kernel version to 4.4.20

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.4.8-2
- GA - Bump release of all rpms

* Thu Apr 28 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.4.8-1
- Update to linux-4.4.8

* Wed Dec 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 4.2.0-1
- Upgrading kernel version to 4.2.0.

* Wed Aug 12 2015 Sharath George <sharathg@vmware.com> - 4.0.9-1
- Upgrading kernel version.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 3.13.3-1
- Initial build. First version
