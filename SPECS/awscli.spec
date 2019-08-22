%if 0%{?rhel} && 0%{?rhel} <= 8
%bcond_with python3
%else
%bcond_without python3
%endif

%global botocore_version 1.4.43

# python-colorama
%global colorama_version   0.3.7
%global bundled_lib_dir    bundled
%global colorama_dir       %{bundled_lib_dir}/colorama

Name:           awscli
Version:        1.16.184
Release:        5%{?dist}.1
Summary:        Universal Command Line Environment for AWS

License:        ASL 2.0
URL:            http://aws.amazon.com/cli
Source0:        https://github.com/aws/aws-cli/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        colorama-%{colorama_version}.tar.gz
BuildArch:      noarch
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-botocore = %{botocore_version}
Requires:       python3-colorama >= 0.2.5
Requires:       python3-docutils >= 0.10
Requires:       python3-cryptography >= 1.7.2
Requires:       python3-s3transfer >= 0.1.9
Requires:       python3-PyYAML >= 3.10
%else
BuildRequires:  python-devel
BuildRequires:  python-setuptools
# python-botocore bundled in python-s3transfer
#Requires:       python-botocore >= %{botocore_version}
# python-colorama bundle
#Requires:       python-colorama >= 0.2.5
Provides:       bundled(python-colorama) = %{colorama_version}
Requires:       python-docutils >= 0.10
Requires:       python-cryptography >= 1.7.2
Requires:       python-s3transfer >= 0.1.9
Requires:       PyYAML >= 3.10
%endif # with python3
%if 0%{?fedora}
Recommends: bash-completion
Recommends: zsh
%endif # Fedora

%if %{with python3}
%{?python_provide:%python_provide python3-%{name}}
%else
%{?python_provide:%python_provide python-%{name}}
%endif # with python3

%description
This package provides a unified
command line interface to Amazon Web Services.

%prep
%setup -q -n aws-cli-%{version}
rm -rf %{name}.egg-info

# python-colorama bundle
mkdir -p %{bundled_lib_dir}
tar -xzf %SOURCE1 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/colorama-%{colorama_version} %{colorama_dir}
cp %{colorama_dir}/LICENSE.txt colorama_LICENSE.txt
cp %{colorama_dir}/README.rst colorama_README.rst

pushd %{colorama_dir}
# remove bundled egg-info
rm -rf *.egg-info
popd
# python-colorama: append bundled-directory to search path
pwd
sed -i "/^from colorama/iimport sys\nsys.path.insert(0, '%{_libdir}/fence-agents/bundled')" scripts/performance/perfcmp
sed -i "/^import colorama/isys.path.insert(0, '%{_libdir}/fence-agents/bundled')" awscli/customizations/history/show.py awscli/table.py
# python-jmespath: append bundled-directory to search path
sed -i "/^import jmespath/iimport sys\nsys.path.insert(0, '%{_libdir}/fence-agents/bundled')" awscli/customizations/arguments.py

%build
%if %{with python3}
%py3_build
%else
%py2_build
%endif # with python3

# python-colorama bundle
pushd %{colorama_dir}
%{__python2} setup.py build
popd

%install
%if %{with python3}
%py3_install
%else
%py2_install
%endif # with python3
# Fix path and permissions for bash completition
%global bash_completion_dir /etc/bash_completion.d
mkdir -p %{buildroot}%{bash_completion_dir}
mv %{buildroot}%{_bindir}/aws_bash_completer %{buildroot}%{bash_completion_dir}
chmod 644 %{buildroot}%{bash_completion_dir}/aws_bash_completer
# Fix path and permissions for zsh completition
%global zsh_completion_dir /usr/share/zsh/site-functions
mkdir -p %{buildroot}%{zsh_completion_dir}
mv %{buildroot}%{_bindir}/aws_zsh_completer.sh %{buildroot}%{zsh_completion_dir}
chmod 644 %{buildroot}%{zsh_completion_dir}/aws_zsh_completer.sh
ls -alh %{buildroot}%{zsh_completion_dir}/aws_zsh_completer.sh
# We don't need the Windows CMD script
rm %{buildroot}%{_bindir}/aws.cmd
# python-botocore bundle
pushd %{colorama_dir}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot} --install-lib %{_libdir}/fence-agents/bundled
popd

%files
%{!?_licensedir:%global license %doc} 
%doc README.rst colorama_README.rst
%license LICENSE.txt colorama_LICENSE.txt
%{_bindir}/aws
%{_bindir}/aws_completer
%dir %{bash_completion_dir}
%{bash_completion_dir}/aws_bash_completer
%dir %{zsh_completion_dir}
%{zsh_completion_dir}/aws_zsh_completer.sh
%if %{with python3}
%{python3_sitelib}/awscli
%{python3_sitelib}/%{name}-%{version}-py?.?.egg-info
%else
%{python2_sitelib}/awscli
%{python2_sitelib}/%{name}-%{version}-py?.?.egg-info
%endif # with python3
# python-colorama bundle
%{_libdir}/fence-agents/bundled

%changelog
* Thu May 24 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 1.14.28-5.1
- Fix unsupported max_bandwidth issue

  Resolves: rhbz#1581138

* Mon Feb 12 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 1.14.28-5
- Append python-botocore and python-jmespath bundled directory to
  search path where needed

  Resolves: rhbz#1509434

* Wed Feb  7 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 1.14.28-4
- Bundle python-colorama

  Resolves: rhbz#1509434

* Fri Jan 19 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 1.14.28-1
- Update to 1.14.28
- Replace python-rsa with python-cryptography

  Resolves: rhbz#1509434

* Sun Aug 13 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.133-1
- Update to 1.11.133

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.109-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.109-2
- Forgot to update

* Wed Jun 21 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.109-1
- Update to 1.11.109

* Tue May 23 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.90-1
- Update to 1.11.90

* Wed Mar 15 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.63-1
- Update to 1.11.63

* Sat Feb 25 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.55-1
- Update to 1.11.55

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.40-1
- Update to 1.11.40

* Wed Dec 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.34-2
- Update to 1.11.34

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.11.28-3
- Rebuild for Python 3.6

* Tue Dec 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.28-2
- Add PyYAML dependency

* Sun Dec 11 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.28-1
- Update to 1.11.28

* Sat Dec 03 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.24-1
- Update to 1.11.24

* Thu Nov 24 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.21-1
- Update to 1.11.21

* Mon Oct 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.12-1
- Update to 1.11.12

* Sun Oct 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.0-1
- Update to 1.11.0

* Wed Sep 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.67-1
- Update to 1.10.67

* Wed Sep 07 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.62-1
- Update to 1.10.62

* Wed Aug 24 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.59-1
- Update to current upstream version

* Fri Aug 05 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.53-1
- Update to current upstream version

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.45-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 06 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.45-1
- Update to current upstream version

* Wed Jun 08 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.36-1
- Update to current upstream version

* Sat May 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.34-1
- Update to current upstream version

* Wed Feb 24 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.7-1
- Update to current upstream version

* Tue Feb 23 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.6-2
- Fix broken dependency

* Fri Feb 19 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.6-1
- Update to current upstream version

* Wed Feb 17 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.5-1
- Update to current upstream version

* Fri Feb 12 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.4-1
- Update to current upstream version

* Wed Feb 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.3-1
- Update to current upstream version

* Tue Feb 09 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.2-1
- Update to current upstream version

* Tue Feb 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.1-1
- Update to current upstream version

* Fri Jan 22 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.0-1
- Update to current upstream version

* Wed Jan 20 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.9.21-1
- Update to current upstream version
- Don't fix documentation permissions any more (pull request merged)

* Fri Jan 15 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.920-1
- Update to current upstream version

* Fri Jan 15 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.9.19-1
- Update to current upstream version
- Don't substitue the text of bin/aws_bash_completer anymore (pull request merged)
- Don't remove the shabang from awscli/paramfile.py anymore (pull request merged)

* Wed Jan 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.9.18-1
- Update to current upstream version
- Fix completion for bash
- Remove bcdoc dependency that is not used anymore

* Sun Jan 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.9.17-1
- Update to current upstream version
- Lock the botocore dependency version

* Sat Jan 09 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.9.16-1
- Update to current upstream version
- Add dir /usr/share/zsh
- Add dir /usr/share/zsh/site-functions
- Add MIT license (topictags.py is MIT licensed)
- Move dependency from python-devel to python2-devel
- Add Recommends lines for zsh and bsah-completion for Fedora
- Remove BuildReuires: bash-completion
- Remove the macros py2_build and py2_install to prefer the extended form
- Force non-executable bit for documentation
- Remove shabang from awscli/paramfile.py
- Fix bash completion
- Fix zsh completion
- Remove aws.cmd

* Tue Dec 29 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.9.15-1
- Initial package.
