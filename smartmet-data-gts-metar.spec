%define smartmetroot /smartmet

Name:           smartmet-data-gts-metar
Version:        17.10.3
Release:        1%{?dist}.fmi
Summary:        SmartMet Data GTS METAR
Group:          System Environment/Base
License:        MIT
URL:            https://github.com/fmidev/smartmet-data-gts-metar
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	smartmet-qdtools
Requires:	bzip2
Requires:       wget


%description
SmartMet Data Ingestion Module for GTS METAR observations

%prep

%build

%pre

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT

mkdir -p .%{smartmetroot}/cnf/cron/{cron.d,cron.hourly}
mkdir -p .%{smartmetroot}/data/incoming/metar
mkdir -p .%{smartmetroot}/editor/in
mkdir -p .%{smartmetroot}/logs/data
mkdir -p .%{smartmetroot}/run/data/metar_gts/bin

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.d/metar-gts.cron <<EOF
*/20 * * * * /smartmet/run/data/metar/bin/dometar.sh > /smartmet/logs/data/metar-gts.log 2>&1
EOF

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.hourly/clean_data_gts_metar <<EOF
#!/bin/sh
# Clean METAR data
cleaner -maxfiles 2 '_metar.sqd' %{smartmetroot}/data/gts/metar
cleaner -maxfiles 2 '_metar.sqd' %{smartmetroot}/editor/in
EOF

install -m 755 %_topdir/SOURCES/smartmet-data-gts-metar/dometar.sh %{buildroot}%{smartmetroot}/run/data/metar_gts/bin/

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,smartmet,smartmet,-)
%config(noreplace) %{smartmetroot}/cnf/cron/cron.d/metar-gts.cron
%config(noreplace) %attr(0755,smartmet,smartmet) %{smartmetroot}/cnf/cron/cron.hourly/clean_data_gts_metar
%{smartmetroot}/*

%changelog
* Tue Oct 3 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.10.3-1.el7.fmi
- First version

