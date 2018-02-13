%define _unpackaged_files_terminate_build 0
%define __find_provides   0
%define __find_requires   0
%define _appdir		/app/%{name}

%define _url       https://repos.influxdata.com/centos/%{rhel}/%{_arch}/stable/%{name}-%{version}.%{_arch}.rpm

AutoReqProv:    no
Name:           influxdb
Version:        1.4.2
Release:        1%{?dist}
Summary:        influxdb

Group:          Applications/System
License:        MIT
URL:            https://influxdb.com

Source0:        %{name}-%{version}.rpm
Source1:		influxdb.conf
Source2:		influxdb.sysconfig
Source3:		influxdb.service
Source4:		influxdb.init
Source5:		influxdb.logrotate

%description
An Open-Source Time Series Database
InfluxDB is an open source time series database with no external dependencies.
It's useful for recording metrics, events, and performing analytics.

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
%{__rm} -rf %{name}-%{version}/%{_prefix}/lib/influxdb/scripts
%{__cp} -af * %{buildroot}/.
popd

%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig
%{__mkdir_p} %{buildroot}/%{_appdir}

install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/influxdb/influxdb.conf
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/influxdb
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/influxdb 

%if 0%{?rhel} >= 7
	%{__mkdir_p} %{buildroot}%{_unitdir}
	install -m 0755 %{SOURCE3} %{buildroot}%{_unitdir}/influxdb.service
%else
	%{__mkdir_p} %{buildroot}%{_sysconfdir}/init.d
	install -m 0755 %{SOURCE4} %{buildroot}%{_sysconfdir}/init.d/influxdb
%endif

[ -f %{_tmppath}/influxdb.flist ] && %{__rm} -f %{_tmppath}/influxdb.flist
find %{buildroot} -type f -o -type l | sed "s:^%{buildroot}::g" > %{_tmppath}/influxdb.flist

%clean
rm -rf %{buildroot}

%pre
getent group influxdb > /dev/null || groupadd -r influxdb
getent passwd influxdb > /dev/null || \
	useradd -r -g influxdb -d %{_localstatedir}/lib/influxdb -s /sbin/nologin \
	-c "influxdb System" influxdb

%post
%if 0%{?rhel} >= 7
	%systemd_post influxdb.service && %systemd_enalble influxdb.service || :
%else
	/sbin/chkconfig --add influxdb && /sbin/chkconfig influxdb on || :
%endif

if [ "$1" = 1 ]; then
	[ -d "%{_appdir}/etc" ] || %__ln_s %{_sysconfdir}/influxdb %{_appdir}/etc
	[ -d "%{_appdir}/log" ] || %__ln_s %{_localstatedir}/log/influxdb %{_appdir}/log
fi

%preun
if [ "$1" = 0 ]; then
	%if 0%{?rhel} >= 7
		%systemd_preun influxdb.service
	%else
		/sbin/service influxdb stop >/dev/null 2>&1
		/sbin/chkconfig --del influxdb
	%endif

	%{__rm} -rf %{_appdir}
fi

%postun
%if 0%{?rhel} >= 7
	%systemd_postun_with_restart influxdb.service
%else
	if [ $1 -ge 1 ]; then
		/sbin/service influxdb try-restart >/dev/null 2>&1 || :
	fi
%endif

%files -f %{_tmppath}/influxdb.flist
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/influxdb
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/influxdb/influxdb.conf
%defattr(-,influxdb,influxdb,-)
%dir %{_localstatedir}/lib/influxdb
%dir %{_localstatedir}/log/influxdb
%dir %attr(0775, root, root) %{_appdir}

%changelog
* Wed Jan 24 2018 Insun.Kim <insun.kim@sk.com> - 1.4.2-1
- add package
