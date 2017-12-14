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

echo ''
echo READING DIRECTORY
echo ''
echo '==============='
echo ''

for i in `ls | grep .tar$` ;
do

echo PERFORMING MD5 for $i
md5=$i'.md5sum'
md5sum $i| cut -d " " -f 1 > nuevo.txt
cat $md5 | cut -d " " -f 1 > original.txt

cat nuevo.txt
cat original.txt


diff nuevo.txt original.txt > temp.txt

#echo $i 
#echo $md5
#cat $i
#cat $md5
echo ''
echo '============='
echo ''
#echo VARIABLE
#echo $var
#echo =======

# CONDICIONAL

if [ -s temp.txt  ]
then
 echo $i' IS NOT READY'
 #mv $i MALO
 #mv $i'.md5sum' MALO
else
 echo $i' IS READY'
 mv $i /fromARCS/READY
 mv $i'.md5sum' /fromARCS/READY
fi
echo ''
echo '============='

#BORRADO
rm -rf nuevo.txt original.txt
rm -rf temp.txt

done;

