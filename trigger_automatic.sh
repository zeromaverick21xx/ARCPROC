#!/bin/bash

export ACSROOT=/datapacker/ExternalDependencies/
export DATAPACKER_HOME=/datapacker/DataPacker
export JARSDIR=${DATAPACKER_HOME}/lib
export ARCHIVE_CONFIG=${DATAPACKER_HOME}/archiveConfig.properties
export PATH="$PATH:${DATAPACKER_HOME}/scripts"

#export ORACLE_HOME=/home/jao/opt/instantclient_11_2/
export ORACLE_HOME=/usr/lib/oracle/11.2/client64/
export PATH=$PATH:$HOME/bin:$ORACLE_HOME
export LD_LIBRARY_PATH=$HOME/lib/:$ORACLE_HOME/lib
export TNS_ADMIN=$ORACLE_HOME
export

cd /fromARCS/

if [ -e /fromARCS/running.txt ]
then
echo BUSY
else
touch running.txt
echo RUNNING INGESTIONS
/home/jao/bin/cron_val_cycle.sh
rm -rf /fromARCS/running.txt
fi

