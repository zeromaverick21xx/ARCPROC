#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Usage asdm_reconstruction.sh uid___XXXX.tgz"
    exit 1
fi

varname=$1
echo ''
echo ''
echo ASDM RECONSTRUCTION
echo '===================='
echo ''
echo STARTING RECONSTRUCTION OF $varname
echo ''

cd /home/jao/asdm_reingestion/APO/

maquina=jaopost001.sco.alma.cl
ruta=/mnt/jaosco/data/ToUpload/

echo Default path is: jaopost001.sco.alma.cl:/mnt/jaosco/data/ToUpload/
echo ''
while true; do
    read -p "Do you want to use the default path? (y/n): " yn
    echo ""
    case $yn in
        [Yy]* ) echo Proceeding...;break;;

        [Nn]* )
	echo Insert new machine .i.e localhost;read maquina;
        echo ''
        echo ''
        echo Insert new path .i.e. /mnt/jao/;read ruta;break;;
        * ) echo "Please answer Y or N.";;
    esac
done

echo ''
echo Following file is going to be downloade from 
echo ''
echo $maquina:$ruta$varname
echo ''
while true; do
    read -p "Do you want to proceed? (y/n): " yn
    case $yn in
        [Yy]* ) echo Proceeding...;break;;
        [Nn]* ) exit;;
        * ) echo "Please answer Y or N.";;
    esac
done

echo 'NAVIGATING TO'

pwd

echo 'GETTING FILE FROM CASA'

scp -r root@$maquina:$ruta$varname .

tar zxvf $varname

echo CREATING BIN DIRECTORY

directory=${varname%.*}

mkdir /home/jao/asdm_reingestion/APO/BIN_$directory

cd $directory

mv *.bin ../BIN_$directory

cd ..

echo COMPLETED COPY AND EXTRACTION

echo STARTING REINGESTION OF XML DATA

cd /home/jao/asdm_reingestion/


asdmReingest.py APO/$directory/

echo COPYING DATA TO ORAOSF2

scp -r $directory.sql apo@ora2.osf.alma.cl:/u01/backups/xmlfix/

cd APO

scp -r $directory apo@ora2.osf.alma.cl:/u01/backups/xmlfix/

echo INGESTING BINARIES IN NGAS

cd /home/jao/asdm_reingestion/APO/BIN_$directory

for i in `ls | grep .bin`; 
do ngamsCClient -cmd ARCHIVE -timeOut 3600 -fileUri $i -mimetype multipart/related -host ngobe02.osf.alma.cl -port 7778; 
done;

echo RUNNING SQL

cd /home/jao/asdm_reingestion/APO/

ssh apo@ora2.osf.alma.cl sh NO_DELETE_sql_script.sh $directory.sql

echo =======================
echo        IMPORTANT       
echo  =======================
echo
echo If errors occurred when performing sql then
echo
echo connect into ssh apo@ora2.osf.alma.cl
echo
echo cd /u01/backups/xmlfix/
echo
echo "run  sqlplus alma/alma\$dba@ora2.osf.alma.cl:1521/ALMA.OSF.CL @$directory.sql"
echo
