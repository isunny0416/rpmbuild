%define _daemon_user tomcat

%define debug_package %{nil}
%define	__jar_repack %{nil}
%define __spec_install_post %{nil}

Name:           jarvis-glu-agent
Version:        5.4.1
Release:        2%{?dist}
Summary:        SK techx Packages for Cent OS %{version} Jarvis GLU Agent

Group:          System Environment/Daemons
License:        GPLv2
URL:            http://sktechx.com
Source0:        jarvis-glu-agent-%{version}.tar.gz
Source1:        jarvis-glu-agent.sh
Source2:        croncheck_jarvis-glu-agent.sh
Source3:        Jlogrotate.conf
Source4:        jarvis.cron
Source5:        jarvis-glu-agent.init
Source6:        jarvis-glu-agent.service

AutoReqProv:	no

BuildArch:      noarch

%description
This package contains the SK tehcx Packages for CentOS %{version} Jarvis GLU Agent

%prep
%setup -c -q -n %{name}-%{version}

%install
[ -d $RPM_BUILD_ROOT ] && %{__rm} -rf $RPM_BUILD_ROOT

%{__mkdir_p} $RPM_BUILD_ROOT%{_app_home}
%{__cp} -af * $RPM_BUILD_ROOT%{_app_home}

%{__install} -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_app_home}/jarvis-glu-agent.sh
%{__install} -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_app_home}/croncheck_jarvis-glu-agent.sh

%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/Jlogrotate.conf

# Change Daemon User
%{__sed} -i 's|@@USERID@@|%{_daemon_user}|g' \
    $RPM_BUILD_ROOT%{_app_home}/jarvis-glu-agent.sh \
    $RPM_BUILD_ROOT%{_app_home}/croncheck_jarvis-glu-agent.sh

# Change APP PREFIX
%{__sed} -i 's|@@APP_PREFIX@@|%{_app_home}|g' \
    $RPM_BUILD_ROOT%{_app_home}/jarvis-glu-agent.sh \
    $RPM_BUILD_ROOT%{_app_home}/croncheck_jarvis-glu-agent.sh \
    $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/Jlogrotate.conf

%{__mkdir_p} $RPM_BUILD_ROOT/app/log

# install startup scripts
%if 0%{?rhel} >= 7
%{__mkdir_p} $RPM_BUILD_ROOT%{_unitdir}
install -Dm 0644 -p %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/jarvis-glu-agent.service
%{__sed} -i 's|@@USERID@@|%{_daemon_user}|g' \
    $RPM_BUILD_ROOT%{_unitdir}/jarvis-glu-agent.service
%{__sed} -i 's|@@APP_PREFIX@@|%{_app_home}|g' \
    $RPM_BUILD_ROOT%{_unitdir}/jarvis-glu-agent.service
%else
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}
install -Dm 0755 -p %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/jarvis-glu-agent
%{__sed} -i 's|@@USERID@@|%{_daemon_user}|g' \
    $RPM_BUILD_ROOT%{_sysconfdir}/init.d/jarvis-glu-agent
%{__sed} -i 's|@@APP_PREFIX@@|%{_app_home}|g' \
    $RPM_BUILD_ROOT%{_sysconfdir}/init.d/jarvis-glu-agent
%endif

%clean
[ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT

%pre
getent group tomcat > /dev/null || groupadd -r tomcat
getent passwd tomcat > /dev/null || \
    useradd -r -g tomcat -s /bin/bash -c "Tomcat User" -M tomcat -p '$6$gwXIrtY6WWP0KWC/$6nvL10KcdcLXJg32bWvwzdCDEmFxcOn8KEHi1xDkev4ETu26dXCj9r95siN1wgBnmYNq7hlWfKn71JaG2LCvx0'

%post
if [ $1 -eq 1 ]; then
    ln -s %{_app_home}/org.linkedin.glu.agent-server-zkc1-5.4.1/data/logs \
	/app/log/%{name}
    ln -s %{_app_home}/org.linkedin.glu.agent-server-zkc1-5.4.1/data/logs \
	%{_app_home}/logs
fi

%if 0%{?rhel} >= 7
%systemd_post jarvis-glu-agent.service
%else
/sbin/chkconfig --add jarvis-glu-agent && \
/sbin/chkconfig --level 2345 jarvis-glu-agent on
crontab -l -u root | %{__grep} 'jarvis-glu-agent start' | %{__grep} -v 'grep' || \
    (crontab -l -u root; echo '*/5 * * * * /sbin/service jarvis-glu-agent start') | crontab -u root -
%endif

%preun
if [ $1 -eq 0 ]; then
    %{__rm} -f /app/log/%{name}
    %{__rm} -f %{_app_home}/logs
fi

%if 0%{?rhel} >= 7
%systemd_preun jarvis-glu-agent.service
%else
/sbin/service jarvis-glu-agent stop >/dev/null 2>&1
/sbin/chkconfig --del jarvis-glu-agent
crontab -l -u root | %{__grep} 'jarvis-glu-agent start' | %{__grep} -v 'grep' && \
    %{__sed} -i '/jarvis-glu-agent start/d' %{_var}/spool/cron/root
%endif

%postun
%if 0%{?rhel} >= 7
%systemd_postun_with_restart jarvis-glu-agent.service
%else
if [ $1 -ge 1 ]; then
/sbin/service jarvis-glu-agent try-restart >/dev/null 2>&1
fi
%endif

%files
%attr(0755,tomcat,tomcat) %dir %{_app_home}
%defattr(-,tomcat,tomcat,-)
%{_app_home}/*

%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/logrotate.d/Jlogrotate.conf
%if 0%{?rhel} >= 7
%config(noreplace) %{_unitdir}/jarvis-glu-agent.service
%else
%config(noreplace) %{_sysconfdir}/init.d/jarvis-glu-agent
%endif

%changelog
* Wed Aug 31 2017 Insun Kim <insun.kim@sk.com> - 5.4.1-2
- chkconfig on add
* Wed Aug 29 2017 Insun Kim <insun.kim@sk.com> - 5.4.1-1
- init.d, systemd script add
* Wed Aug 28 2017 Insun Kim <insun.kim@sk.com> - 5.4.1-1
- Create Package
