%global pypi_name jsonpatch

%if 0%{?fedora} || 0%{?rhel} > 7
# Enable python3 build by default
%bcond_without python3
%else
%bcond_with python3
%endif

%if 0%{?rhel} > 7
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

Name:           python-%{pypi_name}
Version:        1.21
Release:        2%{?dist}
Summary:        Applying JSON Patches in Python

License:        BSD
URL:            https://github.com/stefankoegl/%{github_name}
Source0:        https://pypi.io/packages/source/j/jsonpatch/%{pypi_name}-%{version}.tar.gz
# tarball from pypi does not include file tests.js required for a specific test.
# upstream issue https://github.com/stefankoegl/python-json-patch/issues/82
Patch0:         0001-Skip-unit-test-in-packaging.patch

BuildArch:      noarch

%description
Library to apply JSON Patches according to RFC 6902 - Python 2 build.

%if %{with python2}
%package -n python2-%{pypi_name}
Summary:        Applying JSON Patches in Python 2

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-jsonpointer
Requires:       python2-jsonpointer

%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Library to apply JSON Patches according to RFC 6902 - Python 2 build.
%endif # with python2

%if %{with python3}
%package -n python3-%{pypi_name}
Summary:        Applying JSON Patches in Python 3

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-jsonpointer
Requires:       python3-jsonpointer

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Library to apply JSON Patches according to RFC 6902 - Python 3 build.
%endif # with python3

%prep
%setup -qn %{pypi_name}-%{version}
%patch0 -p1


%build
%if %{with python2}
%py2_build
%endif # with python2

%if %{with python3}
LANG=en_US.utf8 %py3_build
%endif # with python3

%install
%if %{with python2}
%py2_install
for bin in jsondiff jsonpatch; do
mv %{buildroot}%{_bindir}/$bin %{buildroot}%{_bindir}/$bin-%{python2_version}
ln -s ./$bin-%{python2_version} %{buildroot}%{_bindir}/$bin-2
%if !0%{?with_python3}
ln -s ./$bin-%{python2_version} %{buildroot}%{_bindir}/$bin
%endif
done;
%endif # with python2

%if %{with python3}
LANG=en_US.utf8 %py3_install
for bin in jsondiff jsonpatch; do
mv %{buildroot}%{_bindir}/$bin %{buildroot}%{_bindir}/$bin-%{python3_version}
ln -s ./$bin-%{python3_version} %{buildroot}%{_bindir}/$bin-3
ln -s ./$bin-%{python3_version} %{buildroot}%{_bindir}/$bin
done;
%endif # with python3

%check
%if %{with python2}
%{__python2} tests.py
%endif # with python2

%if %{with python3}
%{__python3} tests.py
%endif # with python3

%if %{with python2}
%files -n python2-%{pypi_name}
%doc README.md
%license COPYING
%if !0%{?with_python3}
%{_bindir}/jsondiff
%{_bindir}/jsonpatch
%endif
%{_bindir}/jsondiff-2*
%{_bindir}/jsonpatch-2*
%{python2_sitelib}/%{pypi_name}.py*
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with python2

%if %{with python3}
%files -n python3-%{pypi_name}
%doc README.md
%license COPYING
%{_bindir}/jsondiff
%{_bindir}/jsonpatch
%{_bindir}/jsondiff-3*
%{_bindir}/jsonpatch-3*
%{python3_sitelib}/%{pypi_name}.py*
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with python3

%changelog
* Thu Mar 15 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.21-2
- Don't build Python 2 subpackage on EL > 7

* Tue Feb 6 2018 Alfredo Moralejo <amoralej@redhat.com> - 1.21-1
- Update to 1.21

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 1.14-5
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.14-2
- Rebuild for Python 3.6
- Added upstream patch for fixing python3 tests failures

* Mon Sep  5 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.14-1
- Upstream 1.14
- Update to latest python packaging guidelines

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 29 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2-5
- Introduce python3- subpackage.

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 1.2-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 15 2013 Alan Pevec <apevec@gmail.com> - 1.2-2
- add runtime dep on jsonpointer

* Fri Oct 11 2013 Alan Pevec <apevec@gmail.com> - 1.2-1
- Update to 1.2

* Fri Sep 13 2013 Alan Pevec <apevec@gmail.com> - 1.1-2
- review feedback: move %%check section, add missing build requirements

* Mon Jul 01 2013 Alan Pevec <apevec@gmail.com> - 1.1-1
- Initial package.
