%define _unpackaged_files_terminate_build 0
%define __find_provides   0
%define __find_requires   0
%define logstash_url      https://download.elastic.co/%{name}/%{name}/packages/centos/%{name}-%{version}.noarch.rpm
%define logstash_download 0


AutoReqProv:    no
Name:           logstash
Version:        2.4.1
Release:        1%{?dist}
Summary:        Elasticsearch

Group:          Applications/System
License:        GPLv2

%if %{logstash_download}
%else
Source0:        https://download.elastic.co/%{name}/%{name}/packages/centos/%{name}-%{version}.noarch.rpm
%endif

Source1:        logstash.sysconfig

BuildRoot:      %{_tmppath}/%{name}-%{version}-root

%description
An extensible logging pipeline

%prep
%if %{logstash_download}
%{__urlhelpercmd} -o %{name}-%{version}.rpm %{logstash_url}
%endif

%build
%{__rm} -rf %{name}

%if %{logstash_download}
%{__mkdir_p} %{name}
pushd %{name}
rpm2cpio ../%{name}-%{version}.rpm | %{__cpio} -ivdu
%else
%{__mkdir_p} %{name}
pushd %{name}
rpm2cpio %{S:0} | %{__cpio} -ivdu
%endif

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig

%{__mkdir_p} %{name}%{_sysconfdir}/rc.d
%{__mv} -f %{name}%{_sysconfdir}/init.d %{name}%{_sysconfdir}/rc.d/
%{__cp} -af %{name}/* %{buildroot}
%{__install} -m644 %{S:1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

find %{name} | sed -e "s/^%{name}//g" > /tmp/logstash.list
##find %{name} -type f -o -type l | sed -e "s/^%{name}//g" >> /tmp/chef.list

%clean
rm -rf $RPM_BUILD_ROOT

%files -f /tmp/logstash.list
%attr(0660,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/logstash

%pre
# create logstash group
if ! getent group logstash >/dev/null; then
  groupadd -r logstash
fi

# create logstash user
if ! getent passwd logstash >/dev/null; then
  useradd -r -g logstash -d /opt/logstash \
    -s /sbin/nologin -c "logstash" logstash
fi

%post
/sbin/chkconfig --add logstash

%{__chown} -R logstash:logstash /opt/logstash
%{__chown} logstash /var/log/logstash
%{__chown} logstash:logstash /var/lib/logstash
%{__chmod} 0644 /etc/logrotate.d/logstash

%preun
if [ $1 -eq 0 ]; then
  /sbin/service logstash stop >/dev/null 2>&1 || true
  /sbin/chkconfig --del logstash
  if getent passwd logstash >/dev/null ; then
    userdel logstash
  fi

  if getent group logstash > /dev/null ; then
    groupdel logstash
  fi
fi

%changelog
* Fri Nov 25 2016 YoungJoo.Kim <vozlt@sk.com> 1:2.4.1-1%{?dist}
- 2.4.1

* Thu Nov 03 2016 YoungJoo.Kim <vozlt@sk.com> 1:2.4.0-1%{?dist}
- Initial package
