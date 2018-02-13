%define _use_internal_dependency_generator 0

Name: remount
Version: 0.0.2
Release: 1%{?dist}
Epoch: 1
Summary: Mount/Unmount remote file system
License: Distributable
Group: System Environment/Base
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Source0: %{name}.init
Source1: %{name}.sysconfig
Source2: %{name}.functions
BuildArch: noarch
Requires: nfs-utils rpcbind

%description
Mount and Unmount remote file system

%install
rm -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/{sysconfig,rc.d/init.d}
%{__mkdir_p} %{buildroot}/usr/share/%{name}

%{__install} -m755 %{SOURCE0} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
%{__install} -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m644 %{SOURCE2} %{buildroot}%{_datadir}/%{name}/functions

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add %{name}
/sbin/chkconfig --level 35 %{name} on

%preun
if [ $1 = 0 ]; then
	/sbin/chkconfig --level 35 %{name} off
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/rc.d/init.d/%{name}
%{_datadir}/%{name}/functions

%changelog
* Mon Mar 07 2016 YoungJoo.Kim <vozlt@sk.com> - 1:0.0.2-1
- Rebuild

* Mon Feb 17 2014 JoungKyun.Kim <http://oops.org> 1:0.0.2-1
- fixed remount on fuse

* Wed Mar  2 2005 JoungKyun.Kim <http://oops.org> 1:0.0.1-1
- first packaged

