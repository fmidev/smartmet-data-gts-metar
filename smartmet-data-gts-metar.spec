%define smartmetroot /smartmet

Name:           smartmet-data-gts-metar
Version:        26.10.23
Release:        1%{?dist}.fmi
Summary:        SmartMet Data GTS METAR
Group:          System Environment/Base
License:        MIT
URL:            https://github.com/fmidev/smartmet-data-gts-metar
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       smartmet-qdtools
Requires:       bzip2

%description
Reads GTS WMO FM-15 METAR files and converts them to SmartMet
querydata for the data server and the editor.

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT

mkdir -p .%{smartmetroot}/cnf/cron/{cron.d,cron.hourly}
mkdir -p .%{smartmetroot}/data/incoming/gts/metar
mkdir -p .%{smartmetroot}/data/gts/metar/world/querydata
mkdir -p .%{smartmetroot}/editor/in
mkdir -p .%{smartmetroot}/tmp/data/metar
mkdir -p .%{smartmetroot}/logs/data
mkdir -p .%{smartmetroot}/run/data/metar_gts/bin

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.d/metar-gts.cron <<EOF
*/10 * * * * /smartmet/run/data/metar_gts/bin/dometar.sh
EOF

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.hourly/clean_data_gts_metar <<EOF
#!/bin/sh
# Clean METAR data
cleaner -maxfiles 2 '_metar.sqd' %{smartmetroot}/data/gts/metar
cleaner -maxfiles 2 '_metar.sqd' %{smartmetroot}/editor/in

# Clean incoming METAR data older than 7 days (7 * 24 * 60 = 10080 min)
find %{smartmetroot}/data/incoming/gts/metar -type f -mmin +10080 -delete
EOF

install -m 755 %_topdir/SOURCES/smartmet-data-gts-metar/dometar.sh %{buildroot}%{smartmetroot}/run/data/metar_gts/bin/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,smartmet,smartmet,-)
%config(noreplace) %{smartmetroot}/cnf/cron/cron.d/metar-gts.cron
%config(noreplace) %attr(0755,smartmet,smartmet) %{smartmetroot}/cnf/cron/cron.hourly/clean_data_gts_metar
%{smartmetroot}/*

%changelog
* Fri Oct 23 2026 Mikko Visa <mikko.visa@fmi.fi> 26.10.23-1.el10.fmi
- Create data/gts/metar/world/querydata and tmp/data/metar (output dir was missing)
- Harden dometar.sh: switch to #!/bin/bash, enable set -uo pipefail,
  quote every variable expansion, replace legacy backticks with $(),
  guard TERM expansion, and clean tmp on EXIT via trap
- Only bzip2 output when it is non-empty
- Drop unused wget requirement and empty spec stanzas
- Add CI workflow that builds RPMs for Rocky 8/9/10
* Tue Oct 3 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.10.3-1.el7.fmi
- First version
