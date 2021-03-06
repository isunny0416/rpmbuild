%define _unpackaged_files_terminate_build 0

%define _java_home		/usr/lib/jvm
%define _tomcat_home	%{_java_home}/tomcat

#
# Don't make debug package
#
%define debug_package	%{nil}

#
# Don't strip binary
# if follow define list is set, change first character # to %
# (#)(%)define is not permitted, only (#)define (for comment) or (%)define
#
%define __spec_install_post %{nil}
#define __find_requires %{nil}
#define _use_internal_dependency_generator 0
%define __jar_repack %{nil}

Summary: Apache Servlet/JSP Engine, RI for Servlet 2.4/JSP 2.0 API
Name: tomcat-8.5.0-apache
Version: 8.5.24
Release: 1%{?dist}
Epoch: 0
License: Apache Software License
Group: Networking/Daemons
URL: http://tomcat.apache.org/
Source0:  http://www.apache.org/dist/tomcat/tomcat-8/v%{version}/bin/apache-tomcat-%{version}.tar.gz
Source1:  tomcat.service
Source2:  tomcat.sysconfig
Source3:  localhost-conf.tar.gz
Source4:  tomcat-users.xml
Source5:  main-index.tar.gz
Source6:  tomcat.logrotate
Source7:  tomcat-conf.tar.gz
Source8:  tomcat.init
Source10:  tomcat-named.service
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildArch: noarch
Conflicts: tomcat-7.0.0-apache

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License. Tomcat is intended to be
a collaboration of the best-of-breed developers from around the world.
We invite you to participate in this open development project.

%prep
%setup -q -n apache-tomcat-%{version}
cd conf
tar xvfpz %{SOURCE3}
cd -
cd webapps/ROOT
tar xvfpz %{SOURCE5}
cd -

%build
%{__chown} -R root:root *
cd conf
tar xvfpz %{SOURCE3}
cd -

%install
[ -d "%{buildroot}" -a "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_tomcat_home}/{bin,work}
%{__mkdir_p} %{buildroot}/var/log/tomcat

find ./bin -name "*.sh" -exec %{__install} -m 755 {} %{buildroot}%{_tomcat_home}/bin/ \;
find ./bin -regex ".*\.\(xml\|jar\|gz\)$" -exec %{__install} -m 644 {} %{buildroot}%{_tomcat_home}/bin/ \;
%{__cp} -af conf %{buildroot}%{_tomcat_home}/
%{__cp} -af lib %{buildroot}%{_tomcat_home}/
%{__cp} -af temp %{buildroot}%{_tomcat_home}/
%{__cp} -af webapps %{buildroot}%{_tomcat_home}/

%{__ln_s} -f /var/log/tomcat %{buildroot}%{_tomcat_home}/logs

%{__mkdir_p} %{buildroot}%{_sysconfdir}/{sysconfig,logrotate.d}
## %{__mkdir_p} %{buildroot}%{_unitdir}
%{__install} -d -m 0755 %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE1} %{buildroot}%{_unitdir}/tomcat.service
%{__install} -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/tomcat
%{__install} -m600 %{SOURCE4} %{buildroot}%{_tomcat_home}/conf/tomcat-users.xml
%{__install} -m644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/tomcat

%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_libexecdir}/tomcat
%{__install} -m 0755 %{SOURCE8} \
    %{buildroot}%{_libexecdir}/tomcat/server
%{__install} -m 0644 %{SOURCE10} \
    %{buildroot}%{_unitdir}/tomcat@.service

pushd %{buildroot}%{_tomcat_home}/conf &> /dev/null
	tar xvfpz %{SOURCE7}
popd &> /dev/null

%clean
[ -d "%{buildroot}" -a "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%post
# install but don't activate
%systemd_post tomcat.service

%preun
# clean tempdir and workdir on removal or upgrade
%systemd_preun tomcat.service

%postun
%systemd_postun_with_restart tomcat.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/logrotate.d/tomcat
%dir %{_tomcat_home}/bin
%dir %{_tomcat_home}/lib
%dir %{_tomcat_home}/webapps
%attr(2775,nobody,adm) %dir %{_tomcat_home}/temp
%attr(2775,nobody,adm) %dir %{_tomcat_home}/work
%attr(2775,nobody,adm) %dir /var/log/tomcat
%attr(2775,root,nobody) %dir %{_tomcat_home}/conf
%attr(2775,root,nobody) %dir %{_tomcat_home}/conf/Catalina
%attr(2775,root,nobody) %dir %{_tomcat_home}/conf/Catalina/localhost

%attr(0660,root,nobody) %config(noreplace) %{_tomcat_home}/conf/*.xml
%attr(0660,root,nobody) %config(noreplace) %{_tomcat_home}/conf/*.policy
%attr(0660,root,nobody) %config(noreplace) %{_tomcat_home}/conf/*.properties
%attr(0660,root,nobody) %config(noreplace) %{_tomcat_home}/conf/Catalina/localhost/*.xml
%{_tomcat_home}/bin/*
%{_tomcat_home}/lib/*.jar
%{_tomcat_home}/webapps/*
%exclude %{_tomcat_home}/webapps/examples
%{_tomcat_home}/temp/*
%{_tomcat_home}/logs

%attr(0644,root,root) %{_unitdir}/tomcat.service
%attr(0644,root,root) %{_unitdir}/tomcat@.service
%attr(0755,root,root) %dir %{_libexecdir}/tomcat
%attr(0755,root,root) %{_libexecdir}/tomcat/server
%config(noreplace) %{_sysconfdir}/sysconfig/tomcat

%changelog
* Wed Dec 27 2017 YoungJoo.Kim <vozlt@sk.com> 8.5.24-1%{?dist}
- update 8.5.24

* Mon Feb 27 2017 YoungJoo.Kim <vozlt@sk.com> 8.0.41-1%{?dist}
- update 8.0.41

* Wed Dec 14 2016 YoungJoo.Kim <vozlt@sk.com> 8.0.39-1%{?dist}
- update 8.0.39

* Wed Jul 13 2016 YoungJoo.Kim <vozlt@sk.com> 8.0.36-1%{?dist}
- update 8.0.36

* Mon Feb 29 2016 YoungJoo.Kim <vozlt@sk.com> 8.0.32-1%{?dist}
- update 8.0.32
