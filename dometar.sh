#!/bin/sh
#
# Finnish Meteorological Institute / Mikko Rauhala (2015-2017)
#
# SmartMet Data Ingestion Module for GTS METAR Observations
#

TIMESTAMP=`date +%Y%m%d%H%M`

if [ -d /smartmet ]; then
    IN=/smartmet/data/incoming/gts/metar
    OUT=/smartmet/data/gts/metar/world/querydata/
    TMP=/smartmet/tmp/data/metar_gts_${TIMESTAMP}
    EDITOR=/smartmet/editor/in/
else
    IN=$HOME/data/incoming/metar
    OUT=$HOME/data/gts/metar/world/querydata/
    TMP=/tmp/data_metar_gts_${TIMESTAMP}
    EDITOR=$HOME/editor/in/
fi
METARFILE=${TMP}/${TIMESTAMP}_gts_world_metar.sqd

# Use log file if not run interactively
if [ $TERM = "dumb" ]; then
    exec &> $LOGFILE
fi

echo "Temporary directory: $TMP"
echo "Output directory: $OUT"
echo "Output file: $(basename $METARFILE)"

mkdir -p ${TMP}

# Do METAR stations
metar2qd -n "$IN/*" > $METARFILE
bzip2 -k $METARFILE

if [ -s $METARFILE ]; then
    mv -f $METARFILE $OUT/
    mv -f ${METARFILE}.bz2 $EDITOR/
fi
rmdir ${TMP}
