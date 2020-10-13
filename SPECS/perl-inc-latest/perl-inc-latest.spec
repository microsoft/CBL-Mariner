Name:           perl-inc-latest
Epoch:          2
Version:        0.500
Release:        16%{?dist}
Summary:        Use modules bundled in inc/ if they are newer than installed ones
License:        ASL 2.0
URL:            https://metacpan.org/release/inc-latest
Source0:        https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/inc-latest-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Tests
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(ExtUtils::Installed)

Provides: perl(inc::latest) = %{version}-%{release}
Provides: perl(inc::latest::private) = %{version}-%{release}

%description
The inc::latest module helps bootstrap configure-time dependencies for CPAN
distributions. These dependencies get bundled into the inc directory within
a distribution and are used by Makefile.PL or Build.PL.

%prep
%setup -q -n inc-latest-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> - 2:0.500-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- License verified.
- Explicitly provide perl(inc::*).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.500-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.500-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.500-13
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.500-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.500-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.500-10
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.500-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.500-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.500-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.500-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.500-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.500-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.500-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.500-2
- Perl 5.22 rebuild

* Fri Jan 30 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.500-1
- Set epoch to compete with perl-Module-Build sub-package

* Thu Jan 29 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.500-1
- Specfile autogenerated by cpanspec 1.78.
