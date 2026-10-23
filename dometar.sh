#!/bin/bash
#
# Finnish Meteorological Institute / Mikko Rauhala (2015-2017)
#
# SmartMet Data Ingestion Module for GTS METAR Observations
#

# No `set -e`: the `-s` size check below gates distribution.
set -uo pipefail

if [ -d /smartmet ]; then
    BASE=/smartmet
else
    BASE=$HOME
fi

IN=$BASE/data/incoming/gts/metar
OUT=$BASE/data/gts/metar/world/querydata
EDITOR=$BASE/editor/in
TMP=$BASE/tmp/data/metar
TIMESTAMP=$(date +%Y%m%d%H%M)
LOGFILE=$BASE/logs/data/metar-gts.log

METARFILE=$TMP/${TIMESTAMP}_gts_world_metar.sqd

mkdir -p "$TMP"
mkdir -p "$OUT"
trap 'rm -f "$TMP"/*.sqd*' EXIT

# Use log file if not run interactively
if [ "${TERM:-}" = "dumb" ]; then
    exec &> "$LOGFILE"
fi

echo "IN:  $IN"
echo "OUT: $OUT"
echo "TMP: $TMP"
echo "METAR File: $METARFILE"

# Do METAR stations
metar2qd -n "$IN/*" > "$METARFILE"

if [ -s "$METARFILE" ]; then
    bzip2 -k "$METARFILE"
    mv -f "$METARFILE" "$OUT"/
    mv -f "${METARFILE}.bz2" "$EDITOR"
fi
