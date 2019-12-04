%define debug_package %{nil}
%define go_path %{_builddir}/go
%define go_package github.com/hashicorp/packer
%define go_package_src %{go_path}/src/%{go_package}

%undefine _disable_source_fetch

Name:           packer
Version:        1.4.5
Release:        1%{?dist}
Summary:        Build Automated Machine Images

Group:          Applications/System
License:        MPLv2.0
URL:            https://www.packer.io/
Source0:			  https://github.com/hashicorp/packer/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  golang

%description
HashiCorp Packer is easy to use and automates the creation of any type of machine image. It embraces modern configuration management by encouraging you to use automated scripts to install and configure the software within your Packer-made images. Packer brings machine images into the modern age, unlocking untapped potential and opening new opportunities.

%prep
%setup -q -c %{name}-%{version}

%build
%{__mkdir_p} %{go_package_src}
%{__cp} -prf ./%{name}-%{version}/* %{go_package_src}/.

export GOPATH=%{go_path}
export PATH=${PATH}:%{go_path}/bin

pushd %{go_package_src}
[ "%{_arch}" == "x86_64" ] && export XC_ARCH=amd64 || export XC_ARCH=386
export XC_OS=linux 
make bin
popd

%install
%{__mkdir_p} %{buildroot}%{_bindir}
find %{go_path}/bin -name "%{name}*" -exec install {} %{buildroot}%{_bindir} \;

%if 0%{?rhel} >= 6
  mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}.io
%endif

%clean
%{__rm} -rf %{go_path}
%{__rm} -rf %{_builddir}/%{name}-%{version}
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/%{name}*

%doc %{name}-%{version}/CHANGELOG.md %{name}-%{version}/README.md %{name}-%{version}/LICENSE

%changelog
* Wed Dec 04 2019 Insun Kim <isunny0416@gmail.com> - 1.4.5
- On some RedHat-based Linux distributions there is another tool named packer installed by default. 
- You can check for this using which -a packer. If you get an error like this it indicates there is a name conflict
- To fix this, you can create a symlink to packer that uses a different name like "packer.io"
* Wed Dec 04 2019 Insun Kim <isunny0416@gmail.com> - 1.4.5
- Initial release
