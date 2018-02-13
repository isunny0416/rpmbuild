%define phplib						%{_libdir}/php
%define extdir						%{phplib}/extensions
%define peardir						%{phplib}/pear
%define phpvar						/var/lib/php
%define oracle_instantclient_ver	10.2.0.4

%define fpm_user nobody
%define fpm_group nobody

%define _unpackaged_files_terminate_build 0

# For pdo-oci ldconfig
%define _use_internal_dependency_generator 0
%define __find_requires %{nil}

# don't build debug package
%define debug_package %{nil}

# For enhance the Performance: --with-zend-vm=GOTO 
# ------------------------------------------------------------------------
# CALL – Uses function handlers for opcodes
# SWITCH – Uses switch() statement for opcode dispatch
# GOTO – Uses goto for opcode dispatch (threaded opcodes architecture)
# ------------------------------------------------------------------------
# 
# GOTO is usually (depends on CPU and compiler) faster than SWITCH, which
# tends to be slightly faster than CALL.
# CALL is default because it doesn’t take very long to compile as opposed
# to the other two and in general the speed is quite close to the others.
%define _with_vm_goto	0	

%define build_dso	0 
%define build_oci	0 
%define build_fcgi	0
%define build_fpm	1

Summary: The PHP HTML-embedded scripting language for use with Apache2.
Summary(ko): PHP HTML - Web Server 와 함께 사용하는 embedded script 언어
Name: php-7.0.0-dso
Version: 7.0.13
Release: 1%{?dist}
Epoch: 1
Group: Development/Languages
License: PHP
Source0: http://www.php.net/distributions/php-%{version}.tar.bz2
Source1: php.conf
Source2: php.ini
Source3: php-cli.ini
Source4: php-fcgi.ini
Source5: php-fpm.ini
Source6: php-fpm.init
Source7: php-fpm.logrotate
Source8: php-fpm.sysconfig
Source9: php-fpm.service

# private patch: 0-99
Patch0: php-extra-version.patch

# compat patch: 100-
Patch100: php-compat-gdbm.patch

BuildRoot: /var/tmp/%{name}-root
Requires: webserver
Requires: glibc keyutils-libs krb5-libs libcom_err libgcc libicu
Requires: libselinux libstdc++ libxml2
Requires: nss-softokn-freebl openssl zlib

BuildRequires: readline-devel, zlib-devel, file >= 4
BuildRequires: libpng-devel, libjpeg-devel, db4-devel, gdbm-devel
BuildRequires: openssl-devel, zlib-devel, libxml2-devel, mariadb-devel
BuildRequires: curl-devel, freetds-devel, freetype-devel
BuildRequires: libmcrypt-devel, mhash-devel, libicu-devel
BuildRequires: bzip2-devel, openldap-devel, postgresql-devel
BuildRequires: net-snmp-devel libtidy-devel libxslt-devel
BuildRequires: sqlite-devel autoconf systemd-devel
%if %{build_dso}
BuildRequires: httpd-devel
%endif

Provides: php-7.0.0-dso

%description
PHP is an HTML-embedded scripting language.  PHP attempts to make it
easy for developers to write dynamically generated web pages.  PHP
also offers built-in database integration for several commercial
and non-commercial database management systems, so writing a
database-enabled web page with PHP is fairly simple.  The most
common use of PHP coding is probably as a replacement for CGI
scripts.  The mod_php module enables the Apache web server to
understand and process the embedded PHP language in web pages.

%package binary
Group: Development/Languages
Summary: php binary
Summary(ko): PHP7의 binary 파일
Requires: glibc keyutils-libs krb5-libs libcom_err libgcc libicu
Requires: libselinux libstdc++ libxml2 ncurses-libs  nss-softokn-freebl
Requires: openssl readline zlib
Provides: php-7.0.0-dso
Conflicts: php-5.6.0-dso-binary

%description binary
php binary file to use in shell

%package fcgi
Group: Development/Languages
Summary: php7 fastcgi
Summary(ko): PHP7 fastcgi
Requires: glibc keyutils-libs krb5-libs libcom_err libgcc libicu
Requires: libselinux libstdc++ libxml2 nss-softokn-freebl
Requires: openssl zlib
Provides: php-7.0.0-dso
Conflicts: php-5.6.0-dso-fcgi

%description fcgi
php fastcgi package

%package fpm
Group: Development/Languages
Summary: php7 fpm
Summary(ko): PHP7 fpm
Requires: glibc keyutils-libs krb5-libs libcom_err libgcc libicu
Requires: libselinux libstdc++ libxml2 nss-softokn-freebl
Requires: openssl zlib
Provides: php-7.0.0-dso
Conflicts: php-5.6.0-dso-fpm

%description fpm
php fpm package

%package devel
Group: Development/Libraries
Summary: php development file for making extensions
Summary(ko): PHP7의 extension 을 만들기 위한 파일들
Conflicts: php-5.6.0-dso-devel

%description devel
php build file for making extensions

%package extension
Group: Development/Languages
Summary: php shared extension
Summary(ko): php 공유 확장
Requires: php-7.0.0-dso
Requires: sqlite mysql-libs file curl mhash
Requires: bzip2-libs cyrus-sasl-lib db4 freetds freetype gdbm glibc keyutils-libs
Requires: krb5-libs libcom_err libcurl libgcc libidn libjpeg libmcrypt libpng
Requires: libselinux libssh2 libstdc++ nspr nss nss-softokn-freebl nss-util
Requires: openldap openssl pcre zlib
Requires: postgresql-libs libtool-ltdl
Requires: net-snmp-libs
Conflicts: php-5.6.0-dso-fcgi php-5.6.0-dso-fpm php-5.6.0-dso-extension

%description extension
This package include php shared extension

%package pdo-oci
Group: Development/Languages
Summary: php shared pdo_oci
Summary(ko): php 공유 pdo_oci
Requires: oracle-instantclient-basic
Requires: php-7.0.0-dso
Conflicts: php-5.6.0-dso-fcgi php-5.6.0-dso-fpm php-5.6.0-dso-pdo-oci

%description pdo-oci
This package include php shared pdo_oci

%package pdo-odbc
Group: Development/Languages
Summary: php shared pdo_odbc
Summary(ko): php 공유 pdo_odbc
BuildRequires: unixODBC-devel
Requires: unixODBC
Requires: php-7.0.0-dso
Conflicts: php-5.6.0-dso-fcgi php-5.6.0-dso-fpm php-5.6.0-dso-pdo-odbc

%description pdo-odbc
This package include php shared pdo_odbc

%package pdo-pgsql
Group: Development/Languages
Summary: php shared pdo_pgsql
Summary(ko): php 공유 pdo_pgsql
Requires: postgresql-libs
Requires: php-7.0.0-dso
Conflicts: php-5.6.0-dso-fcgi php-5.6.0-dso-fpm php-5.6.0-dso-pdo-pgsql

%description pdo-pgsql
This package include php shared pdo_pgsql

%package opcache
Group: Development/Languages
Summary: php shared opcache
Summary(ko): php 공유 opcache
Requires: php-7.0.0-dso
Conflicts: php-5.6.0-dso-fcgi php-5.6.0-dso-fpm php-5.6.0-dso-opcache

%description opcache
The Zend OPcache provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.


%prep
%setup -q -n php-%{version}

%patch0 -p1
%patch100 -p1

%if %{_with_vm_goto}
pushd Zend
	if [ -f "/usr/bin/php" ]; then
		php zend_vm_gen.php --with-vm-kind=GOTO
	fi
popd
%endif

%build

# build function
BuildPHP() {
	VOZLT_FLAGS="$RPM_OPT_FLAGS -Wall -fno-strict-aliasing"
	export CFLAGS="-fPIC ${VOZLT_FLAGS}"
	export EXTENSION_DIR=%{extdir}
	export PEAR_INSTALLDIR=%{peardir}

	case "$1" in
		cli) scandir="cli"; shift ;;
		apache) scandir="apache"; shift ;;
		fcgi) scandir="fcgi"; shift ;;
		fpm) scandir="fpm"; shift ;;
	esac

	%{configure} \
		--with-libdir=%{_lib} \
		--sysconfdir=%{_sysconfdir}/php.d \
		--with-config-file-path=%{_sysconfdir}/php.d \
		--with-config-file-scan-dir=%{_sysconfdir}/php.d/$scandir \
		--disable-phpdbg \
		--disable-debug \
		--disable-xmlreader \
		--disable-xmlwriter \
		--disable-json \
		--disable-phar \
		--without-pear \
		--without-sqlite3 \
		--with-zlib \
		--with-zlib-dir=%{_prefix} \
		--with-mhash \
		--enable-sigchild \
		--enable-inline-optimization \
		--enable-sysvsem \
		--enable-sysvshm \
		--enable-sysvmsg \
		--enable-intl \
		--enable-libxml \
		--enable-pdo \
		--without-pdo-sqlite \
		--without-pdo-mysql \
		--enable-sockets \
		--enable-mbstring=all \
		--enable-mbregex \
		--enable-mbregex-backtrack \
		--enable-mysqlnd \
		--with-libmbfl \
		--with-iconv \
		--with-openssl \
		--with-xmlrpc \
		$*

	%{__make} %{?_smp_mflags}
}

%{__rm} -f configure

%if %{build_oci}
pushd /usr/lib/oracle/%{oracle_instantclient_ver}
[ ! -e "client" ] && %{__ln_s} client64 client
[ ! -e "client/include" ] && %{__ln_s} /usr/include/oracle/%{oracle_instantclient_ver}/client64 client/include
popd
%endif

# build php-cli
./buildconf --force

BuildPHP cli \
		--enable-pcntl \
		--with-readline \
		--disable-cgi \
		--enable-static

%{__mv} sapi/cli/php sapi/cli/php-cli

# build fastcgi
%if %{build_fcgi}
%{__make} clean
BuildPHP fcgi \
		--disable-cli \
		--enable-pcntl \

%{__mv} sapi/cgi/php-cgi sapi/cgi/php-fcgi

%endif

# build fpm
%if %{build_fpm}
%{__make} clean
BuildPHP fpm \
		--disable-cli \
		--enable-pcntl \
		--enable-fpm \
		--with-fpm-systemd

%{__mv} sapi/fpm/php-fpm sapi/fpm/php-fcgi-fpm

%endif

# build dso module
%{__make} clean
BuildPHP apache \
%if %{build_dso}
		--with-apxs2=/usr/sbin/apxs \
%else
		--enable-fpm \
%endif
		--disable-cli \
		--disable-cgi \
		--with-curl=shared,%{_prefix} \
		--with-gd=shared \
		--enable-gd-native-ttf \
		--with-jpeg-dir=%{_prefix} \
		--with-png-dir=%{_prefix} \
		--with-freetype-dir=%{_prefix} \
		--enable-bcmath=shared \
		--enable-calendar=shared \
		--enable-ftp=shared \
		--enable-dba=shared \
		--with-gdbm \
		--with-dbm \
		--with-db4 \
		--with-bz2=shared \
		--with-gettext=shared \
		--with-mcrypt=shared \
		--with-sqlite3=shared \
		--with-pdo-sqlite=shared,%{_prefix} \
		--with-pdo-mysql=shared,mysqlnd \
		--with-pgsql=shared \
		--with-pdo-pgsql=shared \
		--with-pdo-odbc=shared,unixODBC,%{_prefix} \
%if %{build_oci}
		--with-pdo-oci=shared,instantclient,%{_prefix},%{oracle_instantclient_ver} \
%endif
		--with-mysqli=shared,mysqlnd \
		--with-ldap=shared --with-ldap-sasl \
		--with-snmp=shared,%{_prefix} \
		--with-tidy=shared \
		--with-xsl=shared \
		--enable-json=shared \
		--enable-exif=shared \
		--enable-phar=shared \
		--enable-xmlreader=shared \
		--enable-xmlwriter=shared \
		--enable-shmop=shared \
		--enable-opcache=shared

pushd modules
/bin/ls *.so | %{__grep} -v "pdo_oci\|pdo_odbc\|pdo_pgsql\|opcache" | %{__sed} 's/^/;extension = /' > ../extensions.ini

%if %{build_oci}
/bin/ls *pdo_oci*.so | %{__sed} 's/^/extension = /' > ../pdo_oci.ini
%endif

/bin/ls *pdo_odbc*.so | %{__sed} 's/^/extension = /' > ../pdo_odbc.ini
/bin/ls *pdo_pgsql*.so | %{__sed} 's/^/extension = /' > ../pdo_pgsql.ini
/bin/ls *opcache*.so | %{__sed} 's/^/zend_extension = /' > ../opcache.ini
popd

%install
[ "%{buildroot}" != "/" -a -d "${buildroot}" ] && rm -rf %{buildroot}

%{__make} install INSTALL_ROOT=%{buildroot} INSTALL_ID="echo "

%{__rm} -rf %{buildroot}%{extdir}
%{__mkdir_p} %{buildroot}%{_sbindir}
%{__mkdir_p} %{buildroot}%{extdir}
%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__mkdir_p} %{buildroot}%{_sysconfdir}/httpd/conf/module.d/
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d/{cli,apache,fpm}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/ld.so.conf.d
%{__mkdir_p} %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__mkdir_p} %{buildroot}%{_sysconfdir}/{logrotate.d,sysconfig}

%{__install} -m 755 sapi/cli/php-cli %{buildroot}%{_bindir}/php
%{__install} -m 644 sapi/cli/php.1 %{buildroot}%{_mandir}/man1/php.1
pushd %{buildroot}%{_bindir}
[ ! -e "php7" ] && %{__ln_s} php php7
popd
%{__install} -m 755 -s modules/*.so %{buildroot}%{extdir}

%{__install} -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf/module.d/php.conf
%{__install} -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/php.d/php.ini
%{__install} -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/php.d/php-cli.ini
%{__install} -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/php.d/php-cgi-fcgi.ini
%{__install} -m644 extensions.ini %{buildroot}%{_sysconfdir}/php.d/apache/extensions.ini
%{__install} -m644 extensions.ini %{buildroot}%{_sysconfdir}/php.d/cli/extensions.ini
%{__install} -m644 extensions.ini %{buildroot}%{_sysconfdir}/php.d/fpm/extensions.ini
%{__install} -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/php.d/php-fpm.ini
%{__perl} -p -i -e "s/\@php_fpm_user\@/%{fpm_user}/ms" %{buildroot}%{_sysconfdir}/php.d/php-fpm.ini
%{__perl} -p -i -e "s/\@php_fpm_group\@/%{fpm_user}/ms" %{buildroot}%{_sysconfdir}/php.d/php-fpm.ini

#%{__install} -m 644 php.ini-production %{buildroot}%{_sysconfdir}/php.d/php.ini
#%{__install} -m 644 php.ini-production %{buildroot}%{_sysconfdir}/php.d/php-cli.ini
#%{__install} -m 644 extensions.ini %{buildroot}%{_sysconfdir}/php.d/apache/shared.ini
#%{__install} -m 644 extensions.ini %{buildroot}%{_sysconfdir}/php.d/cli/shared.ini

%if %{build_oci}
%{__install} -m 644 pdo_oci.ini %{buildroot}%{_sysconfdir}/php.d/apache/pdo_oci.ini
%{__install} -m 644 pdo_oci.ini %{buildroot}%{_sysconfdir}/php.d/cli/pdo_oci.ini
%{__install} -m 644 pdo_oci.ini %{buildroot}%{_sysconfdir}/php.d/fpm/pdo_oci.ini
%endif

%{__install} -m 644 pdo_odbc.ini %{buildroot}%{_sysconfdir}/php.d/apache/pdo_odbc.ini
%{__install} -m 644 pdo_odbc.ini %{buildroot}%{_sysconfdir}/php.d/cli/pdo_odbc.ini
%{__install} -m 644 pdo_odbc.ini %{buildroot}%{_sysconfdir}/php.d/fpm/pdo_odbc.ini
%{__install} -m 644 pdo_pgsql.ini %{buildroot}%{_sysconfdir}/php.d/apache/pdo_pgsql.ini
%{__install} -m 644 pdo_pgsql.ini %{buildroot}%{_sysconfdir}/php.d/cli/pdo_pgsql.ini
%{__install} -m 644 pdo_pgsql.ini %{buildroot}%{_sysconfdir}/php.d/fpm/pdo_pgsql.ini

%{__install} -m 644 opcache.ini %{buildroot}%{_sysconfdir}/php.d/apache/opcache.ini
%{__install} -m 644 opcache.ini %{buildroot}%{_sysconfdir}/php.d/cli/opcache.ini
%{__install} -m 644 opcache.ini %{buildroot}%{_sysconfdir}/php.d/fpm/opcache.ini

%if %{build_oci}
# 64bit or 32bit
%ifarch x86_64
    echo "/usr/lib/oracle/%{oracle_instantclient_ver}/client64/lib" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/oracle-instantclient.conf
%else
    echo "/usr/lib/oracle/%{oracle_instantclient_ver}/client/lib" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/oracle-instantclient.conf
%endif
%endif

%if %{build_fcgi}
%{__install} -m 755 sapi/cgi/php-fcgi %{buildroot}%{_bindir}/php-fcgi
%{__install} -m 644 php.ini-production %{buildroot}%{_sysconfdir}/php.d/php-cgi-fcgi.ini
%endif

%if %{build_fpm}
%{__mkdir_p} %{buildroot}%{_localstatedir}/{run,log}/fpm
%{__install} -m 755 sapi/fpm/php-fcgi-fpm %{buildroot}%{_sbindir}/php-fpm
%{__install} -m 755 %{SOURCE6} %{buildroot}%{_sysconfdir}/rc.d/init.d/php-fpm
%{__install} -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/logrotate.d/php-fpm
%{__install} -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/sysconfig/php-fpm

# install systemd unit files and scripts for handling server startup
%{__install} -m 755 -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE9} %{buildroot}%{_unitdir}/

#%{__install} -m 755 sapi/fpm/init.d.php-fpm %{buildroot}%{_sysconfdir}/rc.d/init.d/php-fpm
#%{__perl} -pi -e 's/php-fpm\.conf/php-fpm\.ini/g' %{buildroot}%{_sysconfdir}/rc.d/init.d/php-fpm
%endif

#%{__install} -m 644 %{SOURCE102} %{buildroot}/%{phplib}/alias_table.php

%{__mv} LICENSE LICENSE.php7

# session and update tmp dir
%{__mkdir_p} %{buildroot}%{phpvar}/{sessions,tmp,bin}

# dependency problem
pushd %{buildroot}%{_libdir}/build
%{__chmod} 644 *
%{__chmod} 755 shtool
popd

# Generate files lists and stub .ini files for each subpackage
for mod in $(ls %{buildroot}%{extdir}/*.so | %{__grep} -v "pdo_oci\|pdo_odbc\|pdo_pgsql\|opcache")
do
	modname=$(basename $mod | %{__sed} 's/\.so//g')
	%{__cat} >> files.ext <<EOF
%attr(755,root,root) %{extdir}/${modname}.so
EOF
done

# Remove unpackaged files
%{__rm} -rf %{buildroot}%{_bindir}/{phptar} \
       %{buildroot}%{_datadir}/pear

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
%{__rm} -f files.*

# if build_oci
%if %{build_oci}
%post pdo-oci
/sbin/ldconfig

%postun pdo-oci
/sbin/ldconfig
%endif

# if build_fpm
%if %{build_fpm}
%post fpm
%if 0%{?systemd_post:1}
%systemd_post php-fpm.service
%else
if [ $1 = 1 ]; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%endif

%preun fpm
%if 0%{?systemd_preun:1}
%systemd_preun php-fpm.service
%else
if [ $1 = 0 ]; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable php-fpm.service >/dev/null 2>&1 || :
    /bin/systemctl stop php-fpm.service >/dev/null 2>&1 || :
fi
%endif

%postun fpm
%if 0%{?systemd_postun_with_restart:1}
%systemd_postun_with_restart php-fpm.service
%else
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ]; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart php-fpm.service >/dev/null 2>&1 || :
fi
%endif
%endif

# if build_dso
%if %{build_dso}
%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/conf/module.d/php.conf
%config(noreplace) %{_sysconfdir}/php.d/php.ini
%attr(755,root,root) %{_libdir}/httpd/modules/libphp7.so
%dir %{phplib}
%dir %{phplib}/extensions
%attr(755,nobody,nobody) %dir %{phpvar}/sessions
%attr(755,nobody,nobody) %dir %{phpvar}/tmp
%attr(755,root,root) %dir %{phpvar}/bin
%endif

%files binary
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/php.d/php-cli.ini
%attr(755,root,root) %{_bindir}/php
%{_bindir}/php7
%{_mandir}/man1/php.1*

%if %{build_fcgi}
%files fcgi
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/php.d/php-cgi-fcgi.ini
%config(noreplace) %{_sysconfdir}/php.d/php.ini
%attr(755,nobody,nobody) %dir %{phpvar}/sessions
%attr(755,nobody,nobody) %dir %{phpvar}/tmp
%attr(755,root,root) %dir %{phpvar}/bin
%attr(755,root,root) %{_bindir}/php-fcgi
%endif

%if %{build_fpm}
%files fpm
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/php.d/php-fpm.ini
%config(noreplace) %{_sysconfdir}/php.d/php.ini
%config(noreplace) %{_sysconfdir}/sysconfig/php-fpm
%config(noreplace) %{_sysconfdir}/logrotate.d/php-fpm
%{_unitdir}/php-fpm.service
%attr(755,nobody,nobody) %dir %{phpvar}/sessions
%attr(755,nobody,nobody) %dir %{phpvar}/tmp
%attr(755,root,root) %dir %{_localstatedir}/run/fpm
%attr(755,root,root) %dir %{_localstatedir}/log/fpm
%attr(755,root,root) %dir %{phpvar}/bin
%attr(755,root,root) %{_sbindir}/php-fpm
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/php-fpm
%{_mandir}/man8/php-fpm*
%endif

%files devel
%defattr(-,root,root)
%{_bindir}/php-config
%{_bindir}/phpize
%{_includedir}/php
%{_libdir}/build
%{_mandir}/man1/php-config.1*
%{_mandir}/man1/phpize.1*

%files extension -f files.ext
%config(noreplace) %{_sysconfdir}/php.d/apache/extensions.ini
%config(noreplace) %{_sysconfdir}/php.d/cli/extensions.ini
%config(noreplace) %{_sysconfdir}/php.d/fpm/extensions.ini

%if %{build_oci}
%files pdo-oci
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/php.d/apache/pdo_oci.ini
%config(noreplace) %{_sysconfdir}/php.d/cli/pdo_oci.ini
%config(noreplace) %{_sysconfdir}/php.d/fpm/pdo_oci.ini
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/oracle-instantclient.conf
%{extdir}/*pdo_oci*.so
%endif

%files pdo-odbc
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/php.d/apache/pdo_odbc.ini
%config(noreplace) %{_sysconfdir}/php.d/cli/pdo_odbc.ini
%config(noreplace) %{_sysconfdir}/php.d/fpm/pdo_odbc.ini
%{extdir}/*pdo_odbc*.so

%files pdo-pgsql
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/php.d/apache/pdo_pgsql.ini
%config(noreplace) %{_sysconfdir}/php.d/cli/pdo_pgsql.ini
%config(noreplace) %{_sysconfdir}/php.d/fpm/pdo_pgsql.ini
%{extdir}/*pdo_pgsql*.so

%files opcache
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/php.d/apache/opcache.ini
%config(noreplace) %{_sysconfdir}/php.d/cli/opcache.ini
%config(noreplace) %{_sysconfdir}/php.d/fpm/opcache.ini
%{extdir}/*opcache*.so


%changelog
* Mon Nov 28 2016 YoungJoo.Kim <vozlt@sk.com> 1:7.0.13-1%{?dist}
- update 7.0.13
  . php-extra-version.patch
  . php-compat-gdbm.patch
