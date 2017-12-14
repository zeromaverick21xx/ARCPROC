#! /bin/bash
# -*- coding: iso-8859-1 -*-              

#*******************************************************************************
# ALMA - Atacama Large Millimiter Array                                         
# (c) European Southern Observatory, 2011.                                      
# Copyright by ESO (in the framework of the ALMA collaboration).                
# All rights reserved.                                                          
#                                                                               
# This library is free software; you can redistribute it and/or                 
# modify it under the terms of the GNU Lesser General Public                    
# License as published by the Free Software Foundation; either                  
# version 2.1 of the License, or (at your option) any later version.            
#                                                                               
# This library is distributed in the hope that it will be useful,               
# but WITHOUT ANY WARRANTY; without even the implied warranty of                
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU             
# Lesser General Public License for more details.                               
#                                                                               
# You should have received a copy of the GNU Lesser General Public              
# License along with this library; if not, write to the Free Software           
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA      
#                                                                               
# "@(#) $Id: getfilesfromjao.sh,v 1.2 2014/09/23 17:38:27 pipetemp Exp $"                                                                   
#                                                                               
# who       when        what                                                    
# --------  ----------  ----------------------------------------------          
# fstoehr   2016-12-20  created                                                 
# emorita   2017-03-15  added MOUS_UID to notification email title and text  
# fstoehr   2017-07-13  in case of error, only one email is sent per run
# fstoehr   2017-07-28  the basedirectory now also can contain the runname and still the copying is correct
#                       the file-upload was parallelized
#                       following the workflow decision, the creation of the fits headers was removed again
#                       fits files get now fully uploaded 
#                       added check to make sure the upload directory is available
# fstoehr   2017-07-31  added tar file support including the taring up of subdirectories
#                       added a separate logfile that does not get overwritten
# fstoehr   2017-08-02  added support for renaming of the manual directory to allow APA to pick it up
# fstoehr   2017-08-03  improved error reporting
# ------------------------------------------------------------------------------------------------------------------------

# This script checks for new directories in the working directory of the ARC rsyncs the files to a JAO directory (e.g. mounted on the processing cluster). 
# After the transfer an email is sent.


if [ "$#" -ne 1 ]
then
    echo "usage: $0 ARC"
    echo
    echo "where ARC must be either EU, EA or NA"
    echo
    echo "- passwordless login to the arcproc machine at JAO is required"
    echo "- The machine from which the script is run must be within the VPN tunnel"
    echo "- The directories and the tar files must be MOVED or SYMLINKD to the magic uploaddirectories, so that they appear complete instantaneously"
    echo "- The packages must have a README file (it can be empty)"
    echo "- Only single tar files can be uploaded. I.e. 001_of_001.tar. Others will be ignored."
    echo "- Manual packages must be formed correctly(!) and must not contain symbolic links within them."
    echo "- Each ARC is responsible for maintaining their config section at the top of this script."
    echo "- The magic upload directory should only (approximately) contain the runs that need to be uploaded. The script will be inefficient if there are many already-uploaded packages in the dir."
    echo "- The script will not delete any runs. This is responsibility of the ARCs/DRM." 
    
    exit
fi

ARC="$1"

if [[ $ARC == "EU" ]]
then
   ##EMAILLIST="fstoehr@eso.org"
   EMAILLIST="fstoehr@eso.org,srandall@eso.org,Vinodiran.Arumugam@eso.org,fgugliel@eso.org,dpetry@eso.org,tstanke@eso.org,fpalla@eso.org"
   LOCALDIRECTORY1="/lustre/opsw/work/pipeproc/pipeline/uploadtojao"
   LOCALDIRECTORY2="$LOCALDIRECTORY1"
   LOGIN="euarc@10.200.60.191"   
   ##LOGIN="arcproc@arcp1"
elif [[ $ARC == "EA" ]]
then 
   EMAILLIST="ea_drm@alma.mtk.nao.ac.jp,almaj_dbadm@alma.mtk.nao.ac.jp"
   LOCALDIRECTORY1="/data/toAPA/work"
   LOCALDIRECTORY2="$LOCALDIRECTORY1"   # if there is only one, set LOCALDIRECTORY2=$LOCALDIRECTORY1
   LOGIN="eaarc@200.2.6.191"   
elif [[ $ARC == "NA" ]]
then
   EMAILLIST="naasc-admin@cv.nrao.edu,cv_analysts@nrao.edu,mlacy@nrao.edu"
   LOCALDIRECTORY1=""
   LOCALDIRECTORY2="$LOCALDIRECTORY1"   # if there is only one, set LOCALDIRECTORY2=$LOCALDIRECTORY1
   LOGIN="naarc@10.200.60.191"   
elif [[ $ARC == "JAO" ]]
then 
   #Test ngonzale 21-sep-2017
   EMAILLIST="sacm@alma.cl"
   LOCALDIRECTORY1="/mnt/jaosco/arcs/to_apa"
   LOCALDIRECTORY2="$LOCALDIRECTORY1"   
   LOGIN="jao@arcproc.sco.alma.cl"
else
   echo "ARC must be either EU, EA, NA or JAO. Have to stop here. ARC given was $ARC"
   exit
fi

LOCALLOGFILE="getfilestojao_locallogfile.log"
REMOTELOGFILE="uploaded_from_arcs.txt"

REMOTEDIRECTORY="/data/apa-staging-area/"
##REMOTEDIRECTORY="/opsw/work/dataforqa2/uploadtest"

THREADNUMBER=20
export RSYNCCOMMAND="rsync -a --copy-links"

# -------------------------------------------------------------------------------------------------------------------------------
# check if there is already an other job running. If so exit. We can not use pidof as this is not available everywhere so we have
# to make it by hand. Note that these commands have to be on separate lines.

THISSCRIPT=`basename $0`
ISRUNNING=`ps -o pid= -C $THISSCRIPT`
RUNCOUNT=`echo $ISRUNNING | wc -w`

if (( RUNCOUNT > 1 )); 
then
   echo "An other $THISSCRIPT is already runing. Exiting this one here." "pids="$ISRUNNING "count="$RUNCOUNT
   echo "done"
   exit
fi

THISPWD=$PWD

echo "===============================================================================================================" | tee -a $THISPWD/$LOCALLOGFILE
echo "Run at `date +%Y_%m_%dT%H_%M_%S.%3N` "  | tee -a $THISPWD/$LOCALLOGFILE

function fileupload {
   LOGIN=$1
   REMOTEDIRECTORY=$2
   RUNNAME=$3
   TAILDIRECTORY=$4
   FILENAME=$5   
   
   # We add a random sleep so that not during the start up $TRHREADNUMBER threads are created simultaneously which would result in rsync/ssh errors
   # On average, the entire MOUS upload is thus delayed by 100 files * 5 seconds / 20 streams = 25 seconds which is completely negligible of course
   
   sleep $[ ( $RANDOM % 10 )]s
   
   ### echo Starting $RUNNAME  `basename $FILENAME` $SLEEPCOUNTER ...
   $RSYNCCOMMAND $FILENAME $LOGIN:$REMOTEDIRECTORY/${RUNNAME}.TMP/$TAILDIRECTORY     
   ### echo Finished $RUNNAME  `basename $FILENAME` ...
}
export -f fileupload

ERROROCURRED=""

# Identifying tar files and unpacking them if appropriate
# Deleting README from the unpacked directories and moving files 1-level down
TARFILELIST=`ls -1 -d $LOCALDIRECTORY1/*.tar $LOCALDIRECTORY2/*.tar | sort -u`


for TARFILE in $TARFILELIST
do

   if [[ "$TARFILE" != *001_of_001.tar ]]
   then
       echo "ERROR Tarfile $TARFILE does not end with 001_of_001.tar. Skipping this tarfile alltogether." | tee -a $THISPWD/$LOCALLOGFILE
       ERROROCURRED=$ERROROCURRED$'\nERROR in Tarfile.'
       continue
   fi    

   TARFILEDIR=`echo $TARFILE | sed 's/.tar//'g`
   PROJECTCODE=`basename $TARFILE | awk -F \_ '{print $1}'`
   MOUS=`basename $TARFILE | awk -F \_ '{print $2"___"$5"_"$6"_"$7}'`    #A bit fragile but not much choice
      
   if [ ! -d "$TARFILEDIR" ]
   then
       echo "Found tarfile `basename $TARFILE` with project code $PROJECTCODE and member OUS $MOUS. Unpacking, removing README, flattening, putting to productsm taring subdirectories and renaming the directory tree ..." | tee -a $THISPWD/$LOCALLOGFILE
       mkdir -p $TARFILEDIR
       cd $TARFILEDIR; tar -xf $TARFILE; chmod -R a+rwX $TARFILEDIR
       DATESTRING=`date +%Y_%m_%dT%H_%M_%S.%3N -r $TARFILEDIR/$PROJECTCODE`
       cd $THISPWD
       mv $TARFILEDIR/$PROJECTCODE $TARFILEDIR/${PROJECTCODE}_${DATESTRING}
       READMELOCATION=`find $TARFILEDIR/${PROJECTCODE}_${DATESTRING} -name "README"`
       if [ "$READMELOCATION" == "" ]
       then
         echo "There is no README file in the untarred directory. Have to stop!"  | tee -a $THISPWD/$LOCALLOGFILE
         ERROROCURRED=$ERROROCURRED$'\nError in Tarfile. No README.'
         # Dangerous but OK as by construction that dir was NOT present already
         rm -rf $TARFILEDIR 
         continue
       fi
       MOUSDIRECTORY=`dirname $READMELOCATION`
       MOUSDIRECTORYPRODUCTS="$MOUSDIRECTORY/products"
       rm $READMELOCATION
       mkdir -p $MOUSDIRECTORYPRODUCTS
       mv $MOUSDIRECTORY/*/* $MOUSDIRECTORYPRODUCTS
       rmdir $MOUSDIRECTORY/{log,product,qa,script,calibration}
       
       # if there are directories remaining (GRRRRRR!), these get tared up
       MOUSDIRLIST=`find $MOUSDIRECTORYPRODUCTS -maxdepth 1 -type d ! -path $MOUSDIRECTORYPRODUCTS`
       for MOUSDIR in $MOUSDIRLIST
       do
          LOCALMOUSDIR=`basename $MOUSDIR`
          cd $MOUSDIRECTORYPRODUCTS && tar -cf $LOCALMOUSDIR.tgz $LOCALMOUSDIR && rm -rf $LOCALMOUSDIR
       done
              
       cd $MOUSDIRECTORY/.. && mv member_ouss_id "MOUS_"$MOUS && cd .. && mv group_ouss_id GOUS_uid___A000_X000_X000 && cd .. && mv sg_ouss_id SOUS_uid___A000_X000_X000       
       cd $THISPWD
   fi
   
done

# Just to be 100% on the safe side
cd $THISPWD

# Get list of directories in local directory
DIRECTORYLIST=`ls -1 -d $LOCALDIRECTORY1/*/*/*/*/*/products $LOCALDIRECTORY2/*/*/*/*/*/products | sort -u`

#echo "ls -1 -d $LOCALDIRECTORY1/*/*/*/*/*/products $LOCALDIRECTORY2/*/*/*/*/*/products | sort -u"

ssh $LOGIN "cd $REMOTEDIRECTORY"
if [ "$?" -ne "0" ]
then
    echo "Can not change into the remote directory. Have to stop here." | tee -a $THISPWD/$LOCALLOGFILE
    echo ssh $LOGIN "cd $REMOTEDIRECTORY" | tee -a $THISPWD/$LOCALLOGFILE
    ERROROCURRED=$ERROROCURRED$'\nERROR Can not change into remote directory.'
    DIRECTORYLIST=""
fi

for DIRECTORY in $DIRECTORYLIST
do
   RUNNAME=`echo $DIRECTORY | awk -F/ '{print $(NF-4)}'`

   if [[ $RUNNAME != 20* ]]
   then
      echo "Run $RUNNAME does not start with 20 and does therefore not look like a run! This is probably an error. Skipping." | tee -a $THISPWD/$LOCALLOGFILE
      ERROROCURRED=$ERROROCURRED$'\nWEEOE Run does not start with 20.'
      continue
   fi
   
   MOUSUID=`echo $DIRECTORY | awk -F/ '{print $(NF-1)}'`   
   TAILDIRECTORY=`echo $DIRECTORY | awk -F/ '{print "/"$(NF-3)"/"$(NF-2)"/"$(NF-1)"/"$(NF)}'`
   RUNNAMETAILDIRECTORY=$RUNNAME$TAILDIRECTORY
   BASEDIRECTORY=${DIRECTORY%$RUNNAMETAILDIRECTORY}
   
   # check that the intended remote directories do not yet exist
   if [ `ssh $LOGIN " grep -w -c $RUNNAME ${REMOTEDIRECTORY}/$REMOTELOGFILE"` -ne 0 ] 
   then
      echo "Skipping    $RUNNAME as the logfile does already contain the entry for this run. ..." | tee -a $THISPWD/$LOCALLOGFILE
      continue      
   fi

   # check that the intended remote directories do not yet exist
   if (ssh $LOGIN "[ -d ${REMOTEDIRECTORY}/${RUNNAME}/ ]") 
   then
      echo "The remote directory does already exist. Skipping $RUNNAME ..." | tee -a $THISPWD/$LOCALLOGFILE
      continue      
   fi
   
   if (ssh $LOGIN "[ -d ${REMOTEDIRECTORY}/${RUNNAME}.TMP ]")
   then
      echo "The data of $RUNNAME apparently were only partly copied previously. Trying to complete ..." | tee -a $THISPWD/$LOCALLOGFILE
   fi
      
   ssh $LOGIN "cd $REMOTEDIRECTORY; mkdir -p ${RUNNAME}.TMP/$TAILDIRECTORY"
       
   # The content of the products directory must be just files
   FILELIST=`find -L $DIRECTORY -maxdepth 1 -mindepth 1`
   
   # the last argument, provided by xargs, is the file name with directory
   #echo $FILELIST | xargs -P 5 -n1 upload $LOGIN $REMOTEDIRECTORY ${RUNNAME} $TAILDIRECTORY
   echo $FILELIST | tr \  \\n | xargs -P $THREADNUMBER -n1 -I '{}' bash -c "fileupload $LOGIN $REMOTEDIRECTORY ${RUNNAME} $TAILDIRECTORY {};"
   
   # Running rsync again with one stream to get the correct error status, and potentially to catch uploads that have failed
   # CHECK: are really only the check bytes transferred in that run? YES
   # The trailing slash on the source is important to copy only the subdirectories
   $RSYNCCOMMAND $DIRECTORY/ $LOGIN:$REMOTEDIRECTORY/${RUNNAME}.TMP/$TAILDIRECTORY
   if [ "$?" -eq "0" ]
   then        
     ssh $LOGIN "cd $REMOTEDIRECTORY; chmod -R a+rwX ${RUNNAME}.TMP" && ssh $LOGIN "cd $REMOTEDIRECTORY; mv ${RUNNAME}.TMP $RUNNAME"  && ssh $LOGIN "echo "$RUNNAME $ARC `date`" >> $REMOTEDIRECTORY/$REMOTELOGFILE" && echo "The data of $RUNNAME were copied successfully to JAO using $THREADNUMBER streams" | tee -a $THISPWD/$LOCALLOGFILE && echo "The data of $RUNNAME ($MOUSUID) were copied successfully to JAO using $THREADNUMBER streams" | mail -s "getfilestojao: run $RUNNAME ($MOUSUID) available for AQUA" $EMAILLIST
   else
      ERROROCURRED=$ERROROCURRED$'\nERROR in the rsync'
   fi         
done

if [ "$ERROROCURRED" != "" ]
then
    echo $'\nERRORS:'  | tee -a $THISPWD/$LOCALLOGFILE
    echo $ERROROCURRED | tee -a $THISPWD/$LOCALLOGFILE
    echo $ERROROCURRED | mail -s "getfilestojao: ERROR in file-upload to JAO" $EMAILLIST  
fi

echo "===============================================================================================================" | tee -a $THISPWD/$LOCALLOGFILE
