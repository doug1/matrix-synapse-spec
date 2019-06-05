%global srcname synapse

%{?python_enable_dependency_generator}

Name:       matrix-%{srcname}
Version:    0.99.5.2
Release:    1%{?dist}
Summary:    A Matrix reference homeserver written in Python using Twisted
License:    ASL 2.0
URL:        https://github.com/matrix-org/%{srcname}
Source0:    %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz
Source1:    synapse.sysconfig
Source2:    synapse.service
BuildArch:  noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

# Test dependencies
BuildRequires:  python3-lxml
BuildRequires:  python3-mock

# Package dependencies
BuildRequires:  python3-bcrypt
BuildRequires:  python3-pyOpenSSL >= 0.15
BuildRequires:  python3-bleach >= 1.4.2
BuildRequires:  python3-canonicaljson >= 1.1.3
BuildRequires:  python3-daemonize
BuildRequires:  python3-frozendict >= 0.4
BuildRequires:  python3-jinja2 >= 2.8
BuildRequires:  python3-jsonschema
BuildRequires:  python3-matrix-synapse-ldap3 >= 0.1
BuildRequires:  python3-msgpack >= 0.3.0
BuildRequires:  python3-netaddr >= 0.7.18
#BuildRequires:  python3-parameterized
BuildRequires:  python3-phonenumbers >= 8.2.0
BuildRequires:  python3-pillow
BuildRequires:  python3-psutil >= 2.0.0
BuildRequires:  python3-pyasn1
BuildRequires:  python3-pymacaroons >= 0.13.0
BuildRequires:  python3-pynacl >= 1.2.0
BuildRequires:  python3-pysaml2 >= 3.0.0
BuildRequires:  python3-service-identity >= 1.0.0
BuildRequires:  python3-signedjson >= 1.0.0
BuildRequires:  python3-six
BuildRequires:  python3-sortedcontainers
BuildRequires:  python3-systemd
BuildRequires:  python3-twisted >= 17.0.0
BuildRequires:  python3-treq
BuildRequires:  python3-unpaddedbase64 >= 1.1.0
BuildRequires:  python3-prometheus_client < 0.4.0
BuildRequires:  python3-pyyaml
BuildRequires:  systemd

Requires(pre):  shadow-utils
Requires:       systemd
%{?systemd_requires}

%description
Matrix is an ambitious new ecosystem for open federated Instant Messaging and
VoIP. Synapse is a reference "homeserver" implementation of Matrix from the
core development team at matrix.org, written in Python/Twisted. It is intended
to showcase the concept of Matrix and let folks see the spec in the context of
a coded base and let you run your own homeserver and generally help bootstrap
the ecosystem.

%prep
%autosetup -p1 -n %{srcname}-%{version}

# We don't support the built-in client so remove all the bundled JS.
rm -rf synapse/static

%build
%py3_build

%install
%py3_install

install -p -D -T -m 0644 contrib/systemd/log_config.yaml %{buildroot}%{_sysconfdir}/synapse/log_config.yaml
install -p -D -T -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/synapse
install -p -D -T -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/synapse.service
install -p -d -m 755 %{buildroot}/%{_sharedstatedir}/synapse

%check
# PYTHONPATH=. trial-3 tests

%pre
getent group synapse >/dev/null || groupadd -r synapse
getent passwd synapse >/dev/null || \
    useradd -r -g synapse -d %{_sharedstatedir}/synapse -s /sbin/nologin \
    -c "The user for the Synapse Matrix server" synapse
exit 0

%post
%systemd_post synapse.service

%preun
%systemd_preun synapse.service

%postun
%systemd_postun_with_restart synapse.service

%files
%license LICENSE
%doc *.rst
%config(noreplace) %{_sysconfdir}/sysconfig/synapse
%{python3_sitelib}/synapse/
%{python3_sitelib}/matrix_synapse*.egg-info/
%{_bindir}/*
%{_unitdir}/synapse.service
%attr(755,synapse,synapse) %dir %{_sharedstatedir}/synapse
%attr(755,synapse,synapse) %dir %{_sysconfdir}/synapse
%attr(644,synapse,synapse) %config(noreplace) %{_sysconfdir}/synapse/*

%changelog
* Tue Jun 04 2019 Doug - 0.99.5.2-1
- Upstream version bump (WIP)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 24 2019 Jeremy Cline <jeremy@jcline.org> - 0.34.0.1-2
- synapse user should own its configuration directory (rhbz 1662672)

* Fri Jan 11 2019 Jeremy Cline <jeremy@jcline.org> - 0.34.0.1-1
- Update to v0.34.0.1, fixes CVE-2019-5885

* Fri Dec 28 2018 Jeremy Cline <jeremy@jcline.org> - 0.34.0-1
- Update to v0.34.0
- Switch to Python 3

* Thu Sep 06 2018 Jeremy Cline <jeremy@jcline.org> - 0.33.3.1-1
- Update to v0.33.3.1
- Use the Python dependency generator.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Jeremy Cline <jeremy@jcline.org> - 0.31.2-1
- Update to v0.31.2
- https://github.com/matrix-org/synapse/releases/tag/v0.31.2

* Wed Jun 13 2018 Jeremy Cline <jeremy@jcline.org> - 0.31.1-2
- Stop using Python dependency generator

* Wed Jun 13 2018 Jeremy Cline <jeremy@jcline.org> - 0.31.1-1
- Update to v0.31.1
- Fix CVE-2018-12291

* Thu May 24 2018 Jeremy Cline <jeremy@jcline.org> - 0.29.1-1
- Update to the latest upstream release.
- Use the Python dependency generator.

* Tue May 01 2018 Jeremy Cline <jeremy@jcline.org> - 0.28.1-1
- Update to the latest upstream release.

* Wed Apr 11 2018 Jeremy Cline <jeremy@jcline.org> - 0.27.3-1
- Update to the latest upstream release.

* Mon Mar 26 2018 Jeremy Cline <jeremy@jcline.org> - 0.27.2-1
- Update to the latest upstream release.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 10 2018 Jeremy Cline <jeremy@jcline.org> - 0.26.0-1
- Update to latest upstream

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.23.1-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Oct 03 2017 Jeremy Cline <jeremy@jcline.org> - 0.23.1-1
- Update to latest upstream
- Include patch to work with ujson-2.0+

* Fri Sep 29 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.22.1-4
- Use python2 prefix for packages whenever possible
- Add missing %%{?systemd_requires}

* Wed Aug 09 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.22.1-3
- Switch to python-bcrypt, BZ 1473018.

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Jeremy Cline <jeremy@jcline.org> - 0.22.1-1
- Update to the latest upstream release

* Thu Jul 06 2017 Jeremy Cline <jeremy@jcline.org> - 0.22.0-1
- Update to the latest upstream release (#1462045)

* Fri Jun 23 2017 Jeremy Cline <jeremy@jcline.org> - 0.21.1-1
- Update to latest upstream release

* Tue May 30 2017 Jeremy Cline <jeremy@jcline.org> - 0.19.3-4
- use _sharedstatedir  rather than _localstatedir

* Wed May 17 2017 Jeremy Cline <jeremy@jcline.org> - 0.19.3-3
- Remove bundled JS
- Fix some typos in the summary and description

* Tue Apr 04 2017 Jeremy Cline <jeremy@jcline.org> - 0.19.3-2
- Remove the duplicate requirement on pysaml

* Tue Mar 28 2017 Jeremy Cline <jeremy@jcline.org> - 0.19.3-1
- Initial package
