%define _unpackaged_files_terminate_build 0
%define __find_provides   0
%define __find_requires   0

%define _minor_version    1
%define	_app_user	grafana
%define _appdir		/app/%{name}
%define _url		https://s3-us-west-2.amazonaws.com/%{name}-releases/release/%{name}-%{version}-%{_minor_version}.%{_arch}.rpm

AutoReqProv:    no
Name:           grafana
Version:        4.6.3
Release:        %{_minor_version}%{?dist}
Summary:        grafana

Group:          Applications/System
License:        GPLv2
URL:            https://grafana.com

Source0:        %{name}-%{version}.rpm
Source1:		grafana.ini

%description
Grafana is an open source, feature rich metrics dashboard and graph editor for Graphite, 
Elasticsearch, OpenTSDB, Prometheus and InfluxDB.

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
popd

%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/grafana
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/grafana
%{__mkdir_p} %{buildroot}/%{_appdir}

install -m 0644 -p %{SOURCE1} %{buildroot}/%{_sysconfdir}/grafana/grafana.ini

[ -f %{_tmppath}/grafana.flist ] && %{__rm} -f %{_tmppath}/grafana.flist
find %{buildroot} -type f -o -type l | sed "s:^%{buildroot}::g" > %{_tmppath}/grafana.flist
find %{buildroot} -empty -type d | sed "s:^%{buildroot}::g" >> %{_tmppath}/grafana.dlist

%clean
rm -rf %{buildroot}

%pre
getent group grafana > /dev/null || groupadd -r grafana
getent passwd grafana > /dev/null || \
	useradd -r -g grafana -d %{_localstatedir}/lib/grafana -s /sbin/nologin \
	-c "grafana System" grafana

%post
%systemd_post grafana-server.service && %systemd_enalble grafana-server.service || :
if [ "$1" = 1 ]; then
    %{__mkdir_p} %{_appdir}
	[ -d "%{_appdir}/etc" ] || %__ln_s %{_sysconfdir}/grafana %{_appdir}/etc
	[ -d "%{_appdir}/log" ] || %__ln_s %{_localstatedir}/log/grafana %{_appdir}/log
fi

%preun
if [ "$1" = 0 ]; then
	%systemd_preun grafana-server.service
    %{__rm} -rf %{_appdir}
fi

%postun
%systemd_postun_with_restart grafana-server.service

%files -f %{_tmppath}/grafana.flist
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/grafana-server
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/grafana/grafana.ini
%defattr(0755,%{_app_user},%{_app_user},-)
%dir %{_localstatedir}/lib/grafana
%dir %{_localstatedir}/log/grafana
%defattr(-,root,root,-)
%dir %{_sysconfdir}/grafana
%dir %{_prefix}/share/grafana/scripts/benchmarks
%dir %{_prefix}/share/grafana/scripts/build
%dir %{_prefix}/share/grafana/scripts/grunt
%dir %{_prefix}/share/grafana/scripts/webpack

%changelog
* Fri Dec 28 2017 Insun.Kim <insun.kim@sk.com> - 4.6.3-1
- add package
