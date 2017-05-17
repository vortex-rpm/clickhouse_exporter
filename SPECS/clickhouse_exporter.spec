%define debug_package %{nil}

%define _git_slug src/github.com/f1yegor/clickhouse_exporter
%define _git_commit 2dfd2ce94e7a4b38189f2260f75b85ef3ec2cf8e

Name:    clickhouse_exporter
Version: 0.0
Release: 0.%{_git_commit}.vortex%{?dist}
Summary: ClickHouse Exporter for Prometheus
License: MIT
Vendor:  Vortex RPM
URL:     https://github.com/f1yegor/clickhouse_exporter

Source1: %{name}.service
Source2: %{name}.default

Requires(pre): shadow-utils
%{?systemd_requires}
BuildRequires: golang, git

%description
This is a simple server that periodically scrapes
ClickHouse stats and exports them via HTTP
for Prometheus consumption.

%prep
mkdir _build
export GOPATH=$(pwd)/_build
git clone https://github.com/f1yegor/%{name} $GOPATH/%{_git_slug}
cd $GOPATH/%{_git_slug}
git checkout %{_git_commit}

%build
export GOPATH=$(pwd)/_build
cd $GOPATH/%{_git_slug}
make format
make
strip %{name}

%install
export GOPATH=$(pwd)/_build
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 $GOPATH/%{_git_slug}/%{name} %{buildroot}/usr/bin/%{name}
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{name}.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/%{name}

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
/usr/bin/%{name}
/usr/lib/systemd/system/%{name}.service
%config(noreplace) /etc/default/%{name}
%config(noreplace) /etc/prometheus/snmp.yml
%attr(755, prometheus, prometheus)/var/lib/prometheus
%doc _build/%{_git_slug}/LICENSE _build/%{_git_slug}/README.md

%changelog
* Wed May 17 2017 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 0.0.2dfd2ce94e7a4b38189f2260f75b85ef3ec2cf8e-1.vortex
- Initial packaging
