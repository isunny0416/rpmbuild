Name:           skt-release
Version:        %{rhel}
Epoch:          1
Release:        1%{dist}
Summary:        YUM configuration for skt repository
Summary(ko):	Skt 저장소를 위한 Yum 설정

Group:          System Environment/Base
License:        GPL
URL:            http://sktelecom.com
Source0:        RPM-GPG-KEY-CentOS-7-Skt
Source1:		Skt.repo
Source2:        RPM-GPG-KEY-EPEL-7
BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArch:      noarch

Requires:       yum
Requires:       redhat-release >= %{rhel}

%description
This package contains yum configuration for the "Skt" RPM Repository, 
as well as the public GPG keys used to sign them.

%description -l ko
이 패키지는 Skt RPM 저장소를 위한 Yum 설정 및 GPG 키를 포함한다.

%prep
echo empty prep

%build
echo empty build

%install
rm -rf $RPM_BUILD_ROOT
%{__install} -Dp -m0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7-Skt
%{__install} -Dp -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/yum.repos.d/Skt.repo
%{__install} -Dp -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7

%clean
rm -rf $RPM_BUILD_ROOT

%post
# install or update
if [ $1 = 1 ]; then
	rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7-Skt &> /dev/null
	rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7 &> /dev/null
fi

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/Skt.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7-Skt
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7

%changelog
* Tue Jul 12 2016 YoungJoo.Kim <vozlt@sk.com> %{rhel}-1%{?dist}
- Initial package
