Name:           sktx-manager
Version:        %{rhel}
Release:        1%{?dist}
Epoch:          0
Summary:        SKTechx Management Tools
Group:          System Environment/Base
License:        GPL
URL:            http://sktechx.com
Source0:        functions.bash
Source1:        sktx-manager.bash
Source2:        sktx-tar.bash
Source3:        sktx.conf

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
Requires:       yum
Requires:       curl

%description
This package contains tools for SKTechx management.

%prep

%install
rm -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_datadir}/sktx/manager/common/bash
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sktx

%{__install} -m 644 %{SOURCE0} %{buildroot}%{_datadir}/sktx/manager/common/bash/functions
%{__install} -m 700 %{SOURCE1} %{buildroot}%{_bindir}/sktx-manager
%{__install} -m 700 %{SOURCE2} %{buildroot}%{_bindir}/txtar
%{__install} -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sktx/sktx.conf

%clean
rm -rf %{buildroot}

%post

%postun

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/sktx
%dir %{_datadir}/sktx
%dir %{_datadir}/sktx/manager
%dir %{_datadir}/sktx/manager/common
%dir %{_datadir}/sktx/manager/common/bash
%attr(644,root,root) %{_datadir}/sktx/manager/common/bash/functions
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/sktx/sktx.conf
%attr(700,root,root) %{_bindir}/sktx-manager
%attr(755,root,root) %{_bindir}/txtar

%changelog
* Mon Jan 01 2018 YoungJoo.Kim <vozlt@sk.com> %{rhel}-1%{?dist}
- Initial package

