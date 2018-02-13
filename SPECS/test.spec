Name:           sktx-release
Version:        %{rhel}
Release:        1%{?dist}
Summary:        SK techx Packages for Cent OS %{version} repository configuration

Group:          System Environment/Base
License:        GPLv1
URL:            http://sktechx.com
Source0:        http://172.21.89.31/sktx/RPM-GPG-KEY-CentOS-SKtx-%{version}
#Source0:       RPM-GPG-KEY-CentOS-SKtx-%{version}
Source1:        sktxse.repo

BuildArch:      noarch

Requires:       redhat-release >= %{version}

%description
This package contains the SK tehcx Packages for CentOS %{version} repository
GPG key as well as configuration for yum and up2date

%prep
echo %{_prefix}
echo %{_localstatedir}
echo %{_prefix}/var
echo %{_prefix}/%{_lib}
