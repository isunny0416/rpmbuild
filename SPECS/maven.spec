%define debug_package                     %{nil}
%define _unpackaged_files_terminate_build 0
%define __find_provides   0
%define __find_requires   0

%define _maven_home       /usr/local/maven
%define _minor_version    1
%define _download         1
%define _url              http://mirror.navercorp.com/apache/maven/maven-3/3.5.3/binaries/apache-%{name}-%{version}-bin.tar.gz

AutoReqProv:    no
Name:           maven
Version:        3.5.3
Release:        %{_minor_version}%{?dist}
Summary:        Maven is a software project management and comprehension tool.

Group:          Applications/System
License:        GPLv2
URL:            https://maven.apache.org

Source0:        %{name}-%{version}.tar.bz2
Source1:		maven.sh
Source2:		maven.csh

%description
Maven is a software project management and comprehension tool. Based on the
concept of a project object model (POM), Maven can manage a project's build,
reporting and documentation from a central piece of information.

%prep
#[ -f %{S:0} ] || %{__urlhelpercmd} -o %{_sourcedir}/apache-%{name}-%{version}.tar.gz %{S:0}
%setup -q

%build
%{__mkdir_p} -p %{buildroot}%{_sysconfdir}/profile.d

#find . > /tmp/maven.list
find . -type d | sed -e 's!^\.!\%dir %{_maven_home}!g' > %{_tmppath}/maven.flist
find . -type f -o -type l | sed -e 's!^\.!%{_maven_home}!g' >> %{_tmppath}/maven.flist

%install
[ -d "%{buildroot}" ] && %{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_maven_home}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/profile.d

%{__cp} -af * %{buildroot}%{_maven_home}

%{__install} -m755 %{S:1} %{buildroot}%{_sysconfdir}/profile.d/maven.sh
%{__install} -m755 %{S:2} %{buildroot}%{_sysconfdir}/profile.d/maven.csh


%clean
rm -rf %{buildroot}

%pre

%post

%preun

%postun

%files -f %{_tmppath}/maven.flist
%defattr(-,root,root,-)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/profile.d/maven.sh
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/profile.d/maven.csh

%changelog
* Mon Mar 19 2018 YoungJoo.Kim <vozlt@sk.com> - 3.5.3-1
- Init
