%define npm_repo_url	http://172.21.89.31:8081/repository/npm-proxy-repository/

Name: nodejs
Version: 8.4.0
Release: 3%{?dist}
Summary: JavaScript runtime
License: MIT and ASL 2.0 and ISC and BSD
Group: Development/Languages
URL: http://nodejs.org

# Exclusive archs must match v8
ExclusiveArch: %{ix86} x86_64 %{arm}

# For NodeSource, we use the sources direct from nodejs.org/dist
Source0: node-v%{version}.tar.xz
#Source1: icu4c-57_1-src.tgz

Patch1: glibc_tls_thread_local_fix.patch

%if 0%{?rhel} == 6 || 0%{?rhel} == 7
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: %{_target_cpu}
BuildRequires: scl-utils
BuildRequires: python27
BuildRequires: python27-python
BuildRequires: devtoolset-6-gcc >= 4.9.4
BuildRequires: devtoolset-6-gcc-c++ >= 4.9.4
%else
BuildRequires: python
%endif

Epoch: 2

#this corresponds to the "engine" requirement in package.json
Provides: nodejs(engine) = %{version}

# Node.js currently has a conflict with the 'node' package in Fedora
# The ham-radio group has agreed to rename their binary for us, but
# in the meantime, we're setting an explicit Conflicts: here
Conflicts: node <= 0.3.2-11

%description
Node.js is a platform built on Chrome\'s JavaScript runtime
for easily building fast, scalable network applications.
Node.js uses an event-driven, non-blocking I/O model that
makes it lightweight and efficient, perfect for data-intensive
real-time applications that run across distributed devices.

%package devel
Summary: JavaScript runtime - development headers
Group: Development/Languages
Requires: %{name}%{?_isa} == %{?epoch}:%{version}-%{release}
#Requires: nodejs-packaging

%description devel
Development headers for the Node.js JavaScript runtime.

%package docs
Summary: Node.js API documentation
Group: Documentation
BuildArch: noarch

%description docs
The API documentation for the Node.js JavaScript runtime.


%prep
%setup -q -n node-v%{version}

%if 0%{?rhel} == 6
%patch1 -p1
%endif

%build
#export CFLAGS='%{optflags} -g -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64'
#export CXXFLAGS='%{optflags} -g -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64'

export CFLAGS='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -mtune=generic -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64'
export CXXFLAGS='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -mtune=generic -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64'

%if 0%{?rhel} == 6 || 0%{?rhel} == 7
. /opt/rh/devtoolset-6/enable && . /opt/rh/python27/enable
./configure --prefix=%{_prefix} \
           --without-dtrace
%else
./configure --prefix=%{_prefix} \
           --without-dtrace
%endif

# Setting BUILDTYPE=Debug builds both release and debug binaries
make BUILDTYPE=Release %{?_smp_mflags}

%pre
if [ -d /usr/lib/node_modules/npm ]; then
  echo "Detected old npm client, removing..."
  rm -rf /usr/lib/node_modules/npm
fi

%install
rm -rf %{buildroot}

./tools/install.py install %{buildroot} %{_prefix}

# and remove dtrace file again
rm -rf %{buildroot}/%{_prefix}/lib/dtrace

# Set the binary permissions properly
chmod 0755 %{buildroot}/%{_bindir}/*

# Install the debug binary and set its permissions
# install -Dpm0755 out/Debug/node %{buildroot}/%{_bindir}/node_g

# own the sitelib directory
mkdir -p %{buildroot}%{_prefix}/lib/node_modules

#install documentation
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}-docs-%{version}/html
cp -pr doc/* %{buildroot}%{_defaultdocdir}/%{name}-docs-%{version}/html
rm -f %{_defaultdocdir}/%{name}-docs-%{version}/html/nodejs.1
cp -p LICENSE %{buildroot}%{_defaultdocdir}/%{name}-docs-%{version}/

#node-gyp needs common.gypi too
mkdir -p %{buildroot}%{_datadir}/node
cp -p common.gypi %{buildroot}%{_datadir}/node

%post
if [ "$1" = 1 ]; then
  %{_bindir}/npm set registry="%{_npm_repo_url}"
fi

%files
%doc AUTHORS LICENSE *.md
%{_bindir}/*
%{_mandir}/man1/node.*
%dir %{_prefix}/lib/node_modules
%{_prefix}/lib/node_modules/*
%dir %{_datadir}/node

%files devel
# %{_bindir}/node_g
%{_includedir}/node
%{_datadir}/node/common.gypi
%{_datadir}/systemtap/tapset/node.stp
%{_docdir}/node/*

%files docs
%{_defaultdocdir}/%{name}-docs-%{version}

%changelog
* Thu Jan 23 2018 Insun Kim <insun.kim@sk.com> - 8.4.0-3
- change npm private repository url change

* Thu Jan 18 2018 Insun Kim <insun.kim@sk.com> - 8.4.0-2
- change npm private repository

* Tue Aug 15 2017 Chris Lea <chl@nodesource.com> - 8.4.0-1
- https://nodejs.org/en/blog/release/v8.4.0/

