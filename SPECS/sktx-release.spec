Name:           sktx-release
Version:        %{rhel}
Epoch:          1
Release:        2%{dist}
Summary:        YUM configuration for SKtechx repository
Summary(ko):	Sk 저장소를 위한 Yum 설정

Group:          System Environment/Base
License:        GPL
URL:            http://sktechx.com
Source0:        RPM-GPG-KEY-SKTechx-CentOS-%{version}
Source1:		sktx.repo
Source2:        RPM-GPG-KEY-EPEL-%{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArch:      noarch

Requires:       yum
Requires:       redhat-release >= %{rhel}

%description
This package contains yum configuration for the "SKtechx" RPM Repository, 
as well as the public GPG keys used to sign them.

%description -l ko
이 패키지는 SKtechx RPM 저장소를 위한 Yum 설정 및 GPG 키를 포함한다.

%prep
echo empty prep

%build
echo empty build

%install
rm -rf $RPM_BUILD_ROOT
%{__install} -Dp -m0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-SKTechx-CentOS-%{version}
%{__install} -Dp -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/yum.repos.d/sktx.repo
%{__install} -Dp -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
# install or update
if [ $1 = 1 ]; then
	rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-SKTechx-CentOS-%{version} &> /dev/null
	rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL-%{version} &> /dev/null
fi

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/sktx.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-SKTechx-CentOS-%{version}
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL-%{version}

%changelog
* Mon Jan 15 2018 Insun.Kim <insun.kim@sk.com> %{rhel}-2%{?dist}
- CentOS 6 ADD
- change centos yum mirror site url pkgrepos -> 172.21.89.31

* Tue Dec 26 2017 YoungJoo.Kim <vozlt@sk.com> %{rhel}-1%{?dist}
- Initial package
