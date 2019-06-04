
# Created by pyp2rpm-3.3.2
%global pypi_name prometheus_client

Name:           python-%{pypi_name}
Version:        0.3.1
Release:        1%{?dist}
Summary:        Python client for the Prometheus monitoring system

License:        Apache Software License 2.0
URL:            https://github.com/prometheus/client_python
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(twisted)

%description
See for documentation.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3dist(twisted)
%description -n python3-%{pypi_name}
See for documentation.

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
# %{__python3} setup.py test

%files -n python3-%{pypi_name}
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Tue Jun 04 2019 mockbuilder - 0.3.1-1
- Initial package.
