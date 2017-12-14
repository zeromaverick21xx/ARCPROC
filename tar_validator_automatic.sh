#!/bin/bash
# Bernardo Malet 2017-06-07

# TITLE ------------------------------------------------------------------------------------------

echo ''
echo '===================================='
echo '|| LOCAL TAR VALIDATOR AUTOMATIC  ||'
echo '===================================='

if [ $# = 0 ]
then
echo ''
echo '--------------------------------------------------------------------------------------------'
echo 'Usage Example:'
echo '                tar_validator_automatic.sh 2015.1.00059.S_uid___A001_X2ca_X14_001_of_001.tar'
echo ''
echo '--------------------------------------------------------------------------------------------'
echo ''
else

# VARIABLE INITIALIZATION ------------------------------------------------------------------------

proyecto=$1
directorio=`echo $proyecto | sed s/_001_of_001.tar/_WORKING/g`
nombre=`echo $proyecto | sed s/_001_of_001.tar//g`
corto=`echo $proyecto | cut -c 1-14`
viejo=`echo $proyecto | sed s/_001_of_001.tar/_001_of_001.tar.OLD/g` 
sin_tgz=`echo $proyecto | sed s/_001_of_001.tar/_NO_TGZ/g`
formato_malo=`echo $proyecto | sed s/_001_of_001.tar/_WRONG_FORMAT/g`
arreglado=`echo $proyecto | sed s/_001_of_001.tar/_FIXED/g`

# VARIABLE CHECK ---------------------------------------------------------------------------------

echo 'VARIABLES'
echo '========='

echo ''
echo PROJECT FILE = $proyecto
echo WORK DIRECTORY = $directorio
echo PROJECT MOUSS = $nombre
echo PROJECT CODE = $corto
echo OLD NAME = $viejo
echo ''
echo '========='
echo ''

# CREATING WORK DIRECTORIES ----------------------------------------------------------------------

mkdir $directorio
cd $directorio
mkdir calibration
mkdir stage2
echo 'working on current directory...'
pwd
cd ..
echo ''


# CHECKING PROJECT LOCALLY OR REMOTE---------------------------------------------------------------

echo 'Checking local version of project file'
echo ''
if [ -f $proyecto ]
then
   echo 'Local version of '$proyecto' found'
   cp $proyecto $directorio/
   cd $directorio
else
    echo 'Local file not found, looking for file in NGAS...'
    echo ''
    cd $directorio
    wget -O $proyecto http://ngas01.sco.alma.cl:7777/RETRIEVE?file_id=$proyecto
    if [ -s $proyecto ]
    then
        echo 'Downloaded Successfully'   
    else
        echo''
        echo "The file "$proyecto" doesn't exist in the archive"
        echo ''
        cd ..
        rm -rf $directorio
        echo 'Exiting...'
        echo ''
        exit 1
    fi
fi

# UNCOMPRESSING PROJECT ----------------------------------------------------------------------------

echo 'Uncompressing tar file...'
echo ''
tar xf $proyecto
echo 'Removing old tar file...'
echo ''
rm -rf $proyecto

# CHECKING TAR FORMAT ------------------------------------------------------------------------------

cd $corto

if [ -s sg_ouss_id ]
then
    echo ''
    echo '================================'
    echo '|| TAR IS IN INCORRECT FORMAT ||'
    echo '================================'
    echo ''
    echo 'There is a sg_ouss_id directory'
    echo 'It needs to be reformatted to science_goal.uid_xxx'
    echo ''
    echo 'It needs to be downloaded and reingested using reingestion_automatic.py'
    echo ''
    cd ../..
    echo 'Renaming directory at'
    pwd 
    mv $directorio $formato_malo
    echo ''
    echo 'Exiting program'
    exit 1
else
cd ..
# RETRIEVING CALIBRATION FILES -------------------------------------------------------------------

echo 'Retrieving calibration files at'
cd 201*/science*/group*/member*/calibration
pwd
echo ''
echo 'copying caibration files to'
cp *_flagtemplate.txt ../../../../../calibration
cd ../../../../../
pwd
echo ''
echo 'Files copied to calibrarion directory...'
echo''
ls -lh calibration
echo ''

# RETRIEVING STAGE2 FILES ----------------------------------------------------------------------------

echo 'Looking for tgz file at'
cd 201*/science_goal.uid*/group.uid*/member.uid*/qa/
pwd
echo ''
echo 'Uncompressing tgz file...'
if [ -s uid*.tgz ]
then tar xf uid*.tgz
    cd pipeline*/html/stage2/
    echo ''
    echo 'Retrieving stage2 files at'
    pwd
    echo ''
    cp *_flagtemplate.txt ../../../../../../../../stage2/
    cd  ../../../../../../../../
    echo 'Copying files to'
    pwd
    echo ''
    echo 'Files copied to stage2 directory...'
    echo ''
    ls -lh stage2
    echo ''
else
   echo ''
   echo '==============================================='
   echo '|| THERE IS NO TGZ UNDER PIPELINE DIRECTORY  ||'
   echo '==============================================='
   echo ''
   echo 'So there is no files to compare....'
   echo ''
   cd ../../../../../../
   echo 'Renaming working directory to report it to DMG'
   pwd
   echo $directorio
   mv $directorio $sin_tgz
   echo ''
   echo 'DIRECTORY RENAMED'
   echo ''
   echo 'Exiting program....'
   exit 1
fi
  
# COMPARING FILES -------------------------------------------------------------------------------

echo 'Comparing files between CALIBRATION and STAGE2 directories...'
echo ''
echo '========================================'
echo '||           DIFFERENCES              ||'
echo '========================================'
echo ''
diff -ENwbur calibration/ stage2/ > diferencia.txt
if [ -s diferencia.txt ]
then
    echo ''
    echo 'THE FILES ARE DIFFERENT, REPACKING'
    echo ''
    echo 'Copying Stage2 files to Calibration...'
    echo ''
    cp -r stage2/* 201*/science*/group*/member*/calibration/
    echo COPIED SUCCESSFULLY
    echo ''
    rm -rf 201*/science*/group*/member*/qa/pipeline*
    echo DELETED PIPELINE
    echo ''
    echo 'Packing the new tar as '$proyecto
    echo ''      
    tar cf $proyecto $corto
    cd ..
    mv $directorio $arreglado
    echo 'TAR WAS REPACKED SUCCESSFULLY'
    echo ''
    echo '============================================================='
    echo '||     IMPORTANT: TAR NEEDS TO BE REINGESTED MANUALLY      ||'
    echo '============================================================='
    echo ''
else
    echo ''
    echo 'THE FILES ARE THE SAME'
    echo ''
    cd ..
    echo 'Deleting working directory'
    pwd
    echo $directorio
    rm -rf $directorio
    echo ''
    echo 'DIRECTORY DELETED'
    echo ''
fi
fi
fi
#NOTES FOR NEXT VERSION
#TRY TO DO A VERSION THAT ONLY UPDATES WITHOUT UNTARING
#
#USE FOLLOWING COMMANDS
#
#
#
#echo if DIFFERENCE above are NULL then the files are the same
#echo if NOT COPY the files inside STAGE2 to CALIBRATION and update de TAR
#cmp 201*/science_goal.uid*/group.uid*/member.uid*/calibration/execblockUid_flagtemplate.txt
# projectId/sg_ouss_id/group_ouss_id/member_ouss_id/calibration/execblockUid_flagtemplate.txt
#tar xvd $proyecto projectId/sg_ouss_id/group_ouss_id/member_ouss_id/qa/member_ouss_id.weblog.tgz pipeline-xxxxx/html/stage2/execblockUid_flagtemplate.txt
#cmp projectId/sg_ouss_id/group_ouss_id/member_ouss_id/qa/member_ouss_id.weblog.tgz pipeline-xxxxx/html/stage2/execblockUid_flagtemplate.txt projectId/sg_ouss_id/group_ouss_id/member_ouss_id/calibration/execblockUid_flagtemplate.txt
#if the files are not the same
#mv pipeline-xxxxx/html/stage2/execblockUid_flagtemplate.txt projectId/sg_ouss_id/group_ouss_id/member_ouss_id/calibration/execblockUid_flagtemplate.txt projectId/sg_ouss_id/group_ouss_id/member_ouss_id/calibration/execblockUid_flagtemplate.txt
#and update the tar
#tar uvf projectId_mous_id_001_of_01.tar projectId
#upload the tar:
#projectId_mous_id_001_of_01.tar'
