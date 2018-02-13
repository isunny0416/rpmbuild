#
# Don't make debug package
#
%define debug_package   %{nil}

%define version 0.41
%define release 1
%define	enable	1

Summary: IP subnet calculator
Name: iprange
Version: %{version}
Release: 1%{?dist}
Epoch: 1
URL: http://jodies.de/ipcalc/
Source: http://jodies.de/ipcalc-archive/%{name}-%{version}.tar.bz2
Group: Applications/ipcalc
BuildRoot: %{_tmppath}/%{name}-buildroot
License: GPL

%description
ipcalc takes an IP address and netmask and calculates the resulting
broadcast, network, Cisco wildcard mask, and host range. By giving
a second netmask, you can design subnets and supernets. It is also
intended to be a teaching tool and presents the subnetting results
as easy-to-understand binary values.
Applications/ipcalc

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -m 755 ipcalc %{buildroot}%{_bindir}/iprange

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/iprange

%changelog
* Wed Oct 26 2016 YoungJoo-Kim <vozlt@sk.com> 1:0.41-1
- Initial Package
