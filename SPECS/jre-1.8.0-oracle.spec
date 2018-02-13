%define _unpackaged_files_terminate_build 0

%define __jvmdir        /usr/lib/jvm
%define _java_ver		1.8.0
%define _java_rel		151
%define _java_home		%{__jvmdir}

#define java_rel		0%{_java_rel}
%define java_rel		%{_java_rel}

#
# Don't make debug package
#
%define debug_package %{nil}

#
# Don't strip binary
# if follow define list is set, change first character # to %
# (#)(%)define is not permitted, only (#)define (for comment) or (%)define
#
%define __spec_install_post %{nil}
%define __find_requires %{nil}
%define _use_internal_dependency_generator 0
%define __jar_repack %{nil}

Summary: Java(TM) Platform Standard Edition Runtime Environment
Name: jre-1.8.0-oracle
Version: %{_java_ver}
Release: %{_java_rel}%{?dist}
Epoch: 0
Group: Development/Tools
License: Oracle Binary Code License (BCL)
URL: http://www.oracle.com/technetwork/java/javase/downloads/index.html
#Source0: jre-%{version}_%{java_rel}.tar.bz2
Source1: jre.profile.csh
Source2: jre.profile.sh
Source3: fontconfig.properties
Source4: ko-fonts.tar.gz
Source5: US_export_policy.jar
Source6: local_policy.jar
Source7: java.security
Source100: jre-mksource.sh
Buildroot: %{_tmppath}/jre-%{version}_%{java_rel}-root
Requires: /bin/basename /bin/cat /bin/cp /bin/gawk /bin/grep
Requires: /bin/ln /bin/ls /bin/mkdir /bin/mv /bin/pwd /bin/rm
Requires: /bin/sed /bin/sort /bin/touch /usr/bin/cut /usr/bin/dirname
Requires: /usr/bin/expr /usr/bin/find /usr/bin/tail /usr/bin/tr
Requires: /usr/bin/wc /bin/sh
Conflicts: jdk-1.8.0-oracle java-1.8.0-openjdk java-1.8.0-openjdk-devel

%description
The Java Platform Standard Edition Runtime Environment (JRE) contains
everything necessary to run applets and applications designed for the
Java platform. This includes the Java virtual machine, plus the Java
platform classes and supporting files.

The JRE is freely redistributable, per the terms of the included license.


%prep
%setup -c -T -n jre-%{version}_%{java_rel}

bash %{S:100} %{version}_%{_java_rel} %{_arch}

%build

if [ "%{_arch}" = "x86_64" ]; then
	pushd x86_64
	carch="x86_64"
else
	pushd i386
	carch="i386"
fi

%{__rm} -f lib/fontconfig.*
%{__mv} -f lib/security/java.security lib/security/.java.security
%{__install} -m644 %{S:3} lib/fontconfig.properties
%{__install} -m644 %{S:5} lib/security/
%{__install} -m644 %{S:6} lib/security/
%{__install} -m644 %{S:7} lib/security/

tar xvfpz %{S:4}

if [ "%{_arch}" = "x86_64" ]; then
	find . -type d | sed -e 's!^\.!\%dir %{_java_home}/jre-%{version}_%{java_rel}/x86_64!g' > /tmp/jre.list
	find . -type f -o -type l | sed -e 's!^\.!%{_java_home}/jre-%{version}_%{java_rel}/x86_64!g' >> /tmp/jre.list
else
	find . -type d | sed -e 's!^\.!\%dir %{_java_home}/jre-%{version}_%{java_rel}/i386!g' > /tmp/jre.list
	find . -type f -o -type l | sed -e 's!^\.!%{_java_home}/jre-%{version}_%{java_rel}/i386!g' >> /tmp/jre.list
fi

popd

%install
# create directorys 
[ -d "%{buildroot}" ] && %{__rm} -rf %{buildroot}

%{__mkdir_p} -p %{buildroot}%{_sysconfdir}/profile.d

%{__install} -m755 %{S:1} %{buildroot}%{_sysconfdir}/profile.d/jre.csh
%{__install} -m755 %{S:2} %{buildroot}%{_sysconfdir}/profile.d/jre.sh

if [ "%{_arch}" = "x86_64" ]; then
	pushd x86_64
	carch="x86_64"
else
	pushd i386
	carch="i386"
fi

%{__mkdir_p} -p %{buildroot}%{_java_home}/jre-%{version}_%{java_rel}/${carch}
cp -af * %{buildroot}%{_java_home}/jre-%{version}_%{java_rel}/${carch}/
popd

%clean
[ -d "%{buildroot}" ] && %{__rm} -rf %{buildroot}
%{__rm} -f /tmp/jre.list

%post
[ -L "%{_java_home}/latest" ] && %{__rm} -f %{_java_home}/latest
if [ "`/bin/uname -m`" = "x86_64" ]; then
	ln -sf %{_java_home}/jre-%{version}_%{java_rel}/x86_64 %{_java_home}/latest
else
	ln -sf %{_java_home}/jre-%{version}_%{java_rel}/i386 %{_java_home}/latest
fi

if [ ! -f "%{_java_home}/default" ]; then
	ln -sf %{_java_home}/latest %{_java_home}/default
fi

%files -f /tmp/jre.list
%defattr(-,root,root)
%{_sysconfdir}/profile.d/jre.csh
%{_sysconfdir}/profile.d/jre.sh

%changelog
* Wed Dec 27 2017 YoungJoo.Kim <vozlt@sk.com> 1:1.8.0-151%{?dist}
- Update 8u151

* Tue Aug 09 2016 YoungJoo.Kim <vozlt@sk.com> 1:1.8.0-101%{?dist}
- Update 8u101
- Added file: jre/lib/security/java.security

* Wed Jul 13 2016 YoungJoo.Kim <vozlt@sk.com> 1:1.8.0-91%{?dist}
- initial package
