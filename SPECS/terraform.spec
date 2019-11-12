%define debug_package %{nil}

%undefine _disable_source_fetch

Name:           terraform
Version:        0.12.13
Release:        1%{?dist}
Summary:        Write, Plan, and Create Infrastructure as Code

Group:          Applications/System
License:        MPLv2.0
URL:            https://www.terraform.io/
Source0:	      https://releases.hashicorp.com/terraform/%{version}/terraform_%{version}_linux_amd64.zip 

%description
Terraform enables you to safely and predictably create, change, and improve infrastructure. 
It is an open source tool that codifies APIs into declarative configuration files that can be shared amongst team members, treated as code, edited, reviewed, and versioned.

%prep
%setup -q -c %{name}-%{version}

%install
install -p -d -m 0755 %{buildroot}%{_bindir}
install -p -m 0744 %{name} %{buildroot}%{_bindir}

%clean
%{__rm} -rf %{_builddir}/%{name}-%{version}
%{__rm} -rf %{buildroot}

%files
%attr(0755,root,root) %{_bindir}/%{name}

%changelog
* Tue Nov 12 2019 Insun Kim <insun.kim@sk.com> - 0.12.13-1
- Version update
* Fri Jun 06 2019 Insun Kim <isunny0416@gmail.com> - 0.12.2-1
- Initial release
