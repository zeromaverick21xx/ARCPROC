echo ''
echo 'PIPELINE INSTALLATION AUTOMATIC '
echo '================================'
echo ''
echo 'Set the variables'
echo '-----------------'
echo ''
echo 'Does the CASA version already contains a PIPELINE version?'
while true; do
    read -p "Enter (Y/N)?" yn
    case $yn in
        [Yy]* ) echo Proceeding...;PIPELINE='Y';break;;
        [Nn]* ) echo Proceeding...;PIPELINE='N';break;;
        * ) echo "Please answer Y or N.";;
    esac
done

if [ $PIPELINE == 'N' ]
then
	echo 'BRANCH = release branch'
	echo 'i.e. BRANCH = Pipeline-Cycle4-R2-B'
	read BRANCH
	echo ''
	echo 'REVISION = revision number'
	echo 'i.e. REVISION=37783'
	read REVISION
else
	BRANCH='NOT_APPLICABLE'
	REVISION='NOT_APPLICABLE'
fi
echo ''
echo 'SOURCE_CASA= path of needed casa in ARCPROC'
echo 'i.e. SOURCE_CASA = /home/casa/packages/RHEL6/stable/casa-stable-4.7.107'
read CASA_SOURCE
echo ''

CASA_DIR=`echo $CASA_SOURCE | rev | cut -d'/' -f1 | rev`

while true; do
    read -p "Enter T for Testing or P for Production?" tp
    case $tp in
        [Tt]* ) echo Set for Testing;variable=test;name=TEST;break;;
        [Pp]* ) echo Set for Production;variable=current;name=PRODUCTION;break;;
        * ) echo "Please enter T or P.";;
    esac
done

echo ''
echo 'The Pipeline will be set as following'
echo '-------------------------------------'
echo ''
echo BRANCH=$BRANCH
echo REVISION=$REVISION
echo CASA_SOURCE=$CASA_SOURCE
echo CASA_DIR=$CASA_DIR
echo Environment is $name
echo Symbolic Link is $variable

echo ''

while true; do
    read -p "Do you wish to proceed?" yn
    case $yn in
        [Yy]* ) echo Proceeding...;break;;
        [Nn]* ) exit;;
        * ) echo "Please answer Y or N.";;
    esac
done

echo ''
echo 'COPYING CASA VERSION'
echo ''

cd /home/casa/packages/pipeline
#cp -r ${CASA_SOURCE} ${CASA_DIR}.${REVISION}
rsync -avP jao@arcproc.sco.alma.cl:${CASA_SOURCE}/ ${CASA_DIR}.${REVISION}



if [ $PIPELINE == 'N' ]
then
	echo ''
	echo 'DOWNLOADING PIPELINE HEURISTICS'
	echo ''

	cd /home/casa/packages/pipeline/${CASA_DIR}.${REVISION}
	svn co -r ${REVISION} https://svn.cv.nrao.edu/svn/casa/branches/project/pipeline ${BRANCH}.${REVISION}

	echo ''
	echo 'INSTALLING PIPELINE'
	echo ''

	chmod -R o+r ${BRANCH}.${REVISION}
	ln -fs ${BRANCH}.${REVISION} pipeline
	export LD_PRELOAD=/lib64/libuuid.so.1
	export SCIPIPE_HEURISTICS=/home/casa/packages/pipeline/${CASA_DIR}.${REVISION}/pipeline
	export SCIPIPE_SCRIPTDIR=${SCIPIPE_HEURISTICS}/pipeline/recipes/
	export SCIPIPE_ROOTDIR=/mnt/jaosco/pipeline/data
	export SCIPIPE_LOGDIR=/mnt/jaosco/pipeline/logs
	export LD_LIBRARY_PATH=/home/casa/packages/pipeline/${CASA_DIR}.${REVISION}/lib:${LD_LIBRARY_PATH}
	export CASAPATH=/home/casa/packages/pipeline/${CASA_DIR}.${REVISION}/bin
	export PATH=/home/casa/packages/pipeline/${CASA_DIR}.${REVISION}/bin:${PATH}
	cd /home/casa/packages/pipeline/${CASA_DIR}.${REVISION}/pipeline
	./runsetup
fi
echo ''
echo 'SETTING PIPELINE FOR PRODUCTION OR TESTING'
echo ''

cd /home/casa/packages/pipeline/

unlink $variable
ln -fs ${CASA_DIR}.${REVISION} $variable

echo ''
echo 'TESTING THE PIPELINE'
echo ''
echo 'Follow these instruction to test the Pipeline'
echo ''
echo 'Run casa-pipe for production pipeline'
echo 'Run casa-pipe-test for test pipeline'
echo ''
echo 'Inside CASA software use pipeline.revision'
echo ''
