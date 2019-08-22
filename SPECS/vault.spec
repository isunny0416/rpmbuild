%define debug_package %{nil}
%define go_path %{_builddir}/go
%define go_package github.com/hashicorp
%define go_package_src %{go_path}/src/%{go_package}/%{name}
%define git_remote_url https://%{go_package}/%{name}.git

%undefine _disable_source_fetch

Name:           vault 
Version:        1.2.2
Release:        1%{?dist}
Summary:        Write, Plan, and Create Infrastructure as Code

Group:          Applications/System
License:        MPLv2.0
URL:            https://www.vaultproject.io

BuildRequires:  golang >= 1.12.7
BuildRequires:  git

%description
Terraform enables you to safely and predictably create, change, and improve infrastructure. 
It is an open source tool that codifies APIs into declarative configuration files that can be shared amongst team members, treated as code, edited, reviewed, and versioned.

%prep
%{__rm} -rf %{_builddir}/%{name}-%{version}
git clone -b v%{version} %{git_remote_url} %{_builddir}/%{name}-%{version}

%build
%{__mkdir_p} %{go_path}/src/%{go_package}
%{__ln_s} %{_builddir}/%{name}-%{version}/ %{go_package_src}

export GOPATH=%{go_path}
export PATH=${PATH}:%{go_path}/bin

pushd %{go_package_src}
make bootstrap
make dev
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
* Tue Aug 20 2019 Insun Kim <isunny0416@gmail.com> - 1.2.2-1
- Initial release

