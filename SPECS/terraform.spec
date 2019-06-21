%define debug_package %{nil}
%define go_path %{_builddir}/go
%define go_package github.com/hashicorp/terraform
%define go_package_src %{go_path}/src/%{go_package}

%undefine _disable_source_fetch

Name:           terraform
Version:        0.12.2
Release:        1%{?dist}
Summary:        Write, Plan, and Create Infrastructure as Code

Group:          Applications/System
License:        MPLv2.0
URL:            https://www.terraform.io/
Source0:	https://github.com/hashicorp/terraform/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  golang

%description
Terraform enables you to safely and predictably create, change, and improve infrastructure. 
It is an open source tool that codifies APIs into declarative configuration files that can be shared amongst team members, treated as code, edited, reviewed, and versioned.

%prep
%setup -q -c %{name}-%{version}

%build
%{__mkdir_p} %{go_package_src}
%{__cp} -prf ./%{name}-%{version}/* %{go_package_src}/.

export GOPATH=%{go_path}
export PATH=${PATH}:%{go_path}/bin

pushd %{go_package_src}
XC_ARCH=amd64 XC_OS=linux make bin
popd

%install
%{__mkdir_p} %{buildroot}%{_bindir}
find %{go_path}/bin -name "%{name}*" -exec install {} %{buildroot}%{_bindir} \;

%clean
%{__rm} -rf %{go_path}
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/%{name}*

%doc %{name}-%{version}/CHANGELOG.md %{name}-%{version}/README.md %{name}-%{version}/LICENSE

%changelog
* Fri Jun 06 2019 Insun Kim <isunny0416@gmail.com> - 0.12.2-1
- Initial release

