%define	prerel	beta3

Name:           luajit
Version:        2.1.0
Release:        1%{?dist}
Summary:        Just-In-Time Compiler for Lua
License:        MIT
URL:            https://openresty.org/
Source0:	https://github.com/openresty/luajit2/archive/v%{version}-%{prerel}/%{name}-%{version}-%{prerel}.tar.gz

%if 0%{?rhel}
ExclusiveArch:  %{ix86} x86_64
%endif

%description
This is the official OpenResty branch for LuaJIT.
This is not really a fork since we still synchronize any upstream changes all the time.
We introduce our own changes which will never merge or haven't yet merged into the upstream LuaJIT (https://github.com/LuaJIT/LuaJIT), which are as follows


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%setup -q -n %{name}2-%{version}-%{prerel}
echo '#!/bin/sh' > ./configure
chmod +x ./configure

# preserve timestamps (cicku)
sed -i -e '/install -m/s/-m/-p -m/' Makefile
sed -i -e '/SYMLINK/s/@echo "  //' Makefile
sed -i -e '/SYMLINK/s/"//' Makefile

%ifarch x86_64
%global multilib_flag MULTILIB=lib64
%endif

%build
%configure
# Q= - enable verbose output
# E= @: - disable @echo messages
# NOTE: we use amalgamated build as per documentation suggestion doc/install.html
make amalg Q= E=@: PREFIX=%{_prefix} TARGET_STRIP=: \
           CFLAGS="%{optflags}" \
           %{?multilib_flag} \
           %{?_smp_mflags}

%install
# PREREL= - disable -betaX suffix
# INSTALL_TNAME - executable name
%make_install PREFIX=%{_prefix} \
              %{?multilib_flag}

rm -rf _tmp_html ; mkdir _tmp_html
cp -a doc _tmp_html/html

# Remove static .a
find %{buildroot} -type f -name *.a -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYRIGHT
%doc README
%{_bindir}/%{name}
%{_bindir}/%{name}-%{version}-%{prerel}
%{_libdir}/libluajit*.so.*
%{_mandir}/man1/luajit*
%{_datadir}/%{name}-%{version}-%{prerel}/

%files devel
%doc _tmp_html/html/
%{_includedir}/luajit-2.1/
%{_libdir}/libluajit*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Sep 02 2019 Insun Kim <isunny0416@gmail.com> - 2.1.0-1
- Create openresty luajit

