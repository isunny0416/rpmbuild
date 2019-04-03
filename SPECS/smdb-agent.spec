%define	_appdir	/app/smdb_agent

Name:           smdb-agent
Version:        %{rhel}
Epoch:          1
Release:        4%{dist}
Summary:        Automatic system infomation collection tool
Summary(ko):	시스템 정보 자동 수집 툴

Group:          System Environment/Base
License:        GPL
URL:            http://sktechx.com
Source0:        smdb_agent.sh
Source1:		smdb_agent
BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArch:      noarch

Requires:       redhat-release >= %{rhel}

%description
Automatic system infomation collection tool

%prep
echo empty prep

%build
%{__mkdir_p} %{name}-%{version}

%install
%{__install} -d %{buildroot}%{_appdir}/{done,send,logs}
%{__install} -Dp -m0744 %{SOURCE0} %{buildroot}%{_appdir}/bin/smdb_agent.sh
%{__install} -Dp -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/smdb_agent

%clean
rm -rf $RPM_BUILD_ROOT

%post
# install or update
if [ $1 = 1 ]; then
    %{__ln_s} %{_appdir}/bin/smdb_agent.sh %{_sysconfdir}/cron.daily/smdb_agent.sh
fi

%postun
# uninstall
if [ $1 = 0 ]; then
    %{__rm} -rf %{_sysconfdir}/cron.daily/smdb_agent.sh
fi

%files
%config %attr(0644,root,root) %{_sysconfdir}/sysconfig/smdb_agent
%attr(0744,root,root) %{_appdir}/bin/smdb_agent.sh
%defattr(-,root,root,0755)
%dir %{_appdir}
%dir %{_appdir}/bin
%dir %{_appdir}/done
%dir %{_appdir}/send
%dir %{_appdir}/logs

%changelog
* Thu Dec 4 2018 insun.kim <insun.kim@sk.com> %{rhel}-4%{?dist}
- smdb_agent.sh script change (line 320)
* Thu Nov 15 2018 insun.kim <insun.kim@sk.com> %{rhel}-3%{?dist}
- smdb_agent.sh script change (line 321)
* Mon Aug 06 2018 insun.kim <insun.kim@sk.com> %{rhel}-2%{?dist}
- files =: add done directory
- smdb_agent.sh cpu bug fix
* Mon Aug 06 2018 insun.kim <insun.kim@sk.com> %{rhel}-1%{?dist}
- Initial package
