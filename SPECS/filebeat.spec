%define _unpackaged_files_terminate_build 0
%define __find_provides   0
%define __find_requires   0
%define _url		https://artifacts.elastic.co/downloads/beats/%{name}/%{name}-%{version}-%{_arch}.rpm
%define _appdir		/app/%{name}

AutoReqProv:    no
Name:           filebeat
Version:        5.4.3
Release:        3%{?dist}
Summary:        Lightweight Data Shippers

Group:          Applications/System
License:        ASL2.0	

Source0:        %{name}-%{version}.rpm
Source1:	filebeat.infra.yml
Source2:        filebeat.sysconfig
Source3:        filebeat.logrotate
Source4:        filebeat.init
Source5:        filebeat.service
Source6:        filebeat.external.yml

%description
Filebeat is an open source file harvester, mostly used to fetch logs files and feed them into logstash.
Together with the libbeat lumberjack output is a replacement for logstash-forwarder.
To learn more about Filebeat, check out https://www.elastic.co/products/beats/filebeat.

%prep
[ -f %{SOURCE0} ] || %{__urlhelpercmd} -o %{_sourcedir}/%{name}-%{version}.rpm %{_url}

%build
[ -d %{name}-%{version} ] && %{__rm} -rf %{name}-%{version}
%{__mkdir_p} %{name}-%{version}

pushd %{name}-%{version}
rpm2cpio %{SOURCE0} | %{__cpio} -idv
popd

%install
[ -d %{buildroot} ] && %{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}

pushd %{name}-%{version}
%{__cp} -af * %{buildroot}/.
[ -d %{buildroot}/lib/systemd ] && %{__rm} -rf %{buildroot}/lib/systemd
popd

%{__mkdir_p} %{buildroot}%{_sysconfdir}/{sysconfig,logrotate.d}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/filebeat/conf.d
%{__mkdir_p} %{buildroot}%{_unitdir}
%{__mkdir_p} %{buildroot}/%{_appdir}

%{__install} -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/filebeat/conf.d/filebeat.infra.yml
%{__install} -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/filebeat
%{__install} -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/filebeat
%{__install} -m644 %{SOURCE6} %{buildroot}%{_sysconfdir}/filebeat/filebeat.external.yml

%if 0%{?rhel} >= 7
   %{__install} -m755 %{SOURCE5} %{buildroot}%{_unitdir}/filebeat.service
   %{__mkdir_p} %{buildroot}/%{_libexecdir}/filebeat
   %{__install} -m755 %{SOURCE4} %{buildroot}%{_libexecdir}/filebeat/filebeat

%else
    %{__install} -m755 %{SOURCE4} %{buildroot}%{_sysconfdir}/init.d/filebeat
%endif

[ -f %{_tmppath}/filebeat.flist ] && %{__rm} -f %{_tmppath}/filebeat.flist
find %{buildroot} -type f -o -type l | sed "s:^%{buildroot}::g" > %{_tmppath}/filebeat.flist
#find %{buildroot} -empty -type d | sed "s:^%{buildroot}::g" >> %{_tmppath}/filebeat.dlist

%clean
rm -rf %{buildroot}

%post
%if 0%{?rhel} >= 7
	%systemd_post filebeat.service && %systemd_enalble filebeat.service || :
%else
	/sbin/chkconfig --add filebeat && /sbin/chkconfig filebeat on || :
%endif

if [ "$1" = 1 ]; then
	[ -d "%{_appdir}/etc" ] || %__ln_s %{_sysconfdir}/filebeat %{_appdir}/etc
	[ -d "%{_appdir}/log" ] || %__ln_s %{_localstatedir}/log/filebeat %{_appdir}/log
fi

%preun
if [ "$1" = 0 ]; then
	%if 0%{?rhel} >= 7
		%systemd_preun filebeat.service
	%else
		/sbin/service filebeat stop >/dev/null 2>&1
		/sbin/chkconfig --del filebeat
	%endif

	%{__rm} -rf %{_appdir}/*
fi

%postun
%if 0%{?rhel} >= 7
	%systemd_postun_with_restart filebeat.service
%else
	if [ $1 -ge 1 ]; then
		/sbin/service filebeat try-restart >/dev/null 2>&1 || :
	fi
%endif

%files -f %{_tmppath}/filebeat.flist
%dir %attr(0755,root,root) %{_sysconfdir}/filebeat/conf.d/
%dir %attr(0755,root,root) %{_appdir}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/filebeat/filebeat.external.yml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/filebeat/conf.d/filebeat.infra.yml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/filebeat
%if 0%{?rhel} >= 7
	%attr(0644,root,root) %{_unitdir}/filebeat.service
	%dir %attr(0775,root,root) %{_libexecdir}/filebeat
	%attr(0755,root,root) %{_libexecdir}/filebeat/filebeat
%endif

%changelog
* Fri Mar 9 2018 Insun.Kim <insun.kim@sk.com> - 5.4.3-3
- add filebeat libexec file (case. centos7)
- change filebeat.server
* Mon Feb 12 2018 Insun.Kim <insun.kim@sk.com> - 5.4.3-2
- change systemd file
* Fri Jan 13 2018 Insun.Kim <insun.kim@sk.com> - 5.4.3-1
- add package
