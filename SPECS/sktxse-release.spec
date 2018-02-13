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

%build

%install
rm -rf $RPM_BUILD_ROOT

# GPG Key
install -Dpm 0644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SKtx-%{version}

# yum.repos.d file copy
install -Dpm 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/sktxse.repo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/sktxse.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SKtx-%{version}

%changelog
* Wed Aug 10 2017 Insun Kim <insun.kim@sk.com> - %{rhel}-%{release}
- Create Package

