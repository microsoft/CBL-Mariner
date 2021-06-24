Summary:        Library to encode and decode webP format images
Name:           libwebp
Version:        1.0.3
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://webmproject.org/
#Source0:       https://github.com/webmproject/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
Requires:       libjpeg-turbo
Requires:       libpng
Requires:       libtiff

%description
The libwebp package contains a library and support programs to encode and decode images in WebP format.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%prep
%setup -q

%build
./autogen.sh

./configure \
        --prefix=%{_prefix} \
        --enable-libwebpmux \
        --enable-libwebpdemux \
        --enable-libwebpdecoder \
        --enable-libwebpextras  \
        --enable-swap-16bit-csp \
        --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name '*.la' -delete -print

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue May 25 2021 Mateusz Malisz <mamalisz@microsoft.com> - 1.0.3-1
- Update to version 1.0.3

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.0.0-4
-   Added %%license line automatically

*   Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 1.0.0-3
-   Verified license. Removed sha1. Fixed Source0 URL comment.  Fixed formatting. URL to https.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.0.0-1
-   Update to version 1.0.0

*   Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 0.6.0-1
-   Upgrading version to 0.6.0

*   Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 0.5.1-1
-   Initial version
