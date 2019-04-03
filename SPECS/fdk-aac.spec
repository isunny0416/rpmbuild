Name:           fdk-aac
Version:        2.0.0
Release:        1%{?dist}
Summary:        Fraunhofer FDK AAC Codec Library

License:        FDK-AAC
URL:            https://github.com/mstorsjo/fdk-aac
Source0:        https://github.com/mstorsjo/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  libtool


%description
The Fraunhofer FDK AAC Codec Library ("FDK AAC Codec") is software that
implements the MPEG Advanced Audio Coding ("AAC") encoding and decoding
scheme for digital audio.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.



%prep
%autosetup
autoreconf -vif

%build
%configure \
  --disable-silent-rules \
  --disable-static

%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc ChangeLog
%license NOTICE
%{_libdir}/*.so.*

%files devel
%doc documentation/*.pdf
%{_includedir}/fdk-aac/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Thu Jan 24 2019 Insun.Kim <insun.kim@sk.com> - 2.0.0
- Version Update 2.0.0

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.6-3
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 09 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.1.6-1
- Update to 1.6

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.1.5-1
- Update to 1.5

* Wed Sep 07 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.5-0.1.gita0bd8aa
- Update to github snapshot
- Spec file clean-up

* Fri Nov 06 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.1.4-1
- Update to 1.4

* Sun Jan 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.1.3-1
- Update to 1.3.0

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.1.2-1
- Update to 0.1.2

* Thu Mar 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.1.1-1
- Initial spec

