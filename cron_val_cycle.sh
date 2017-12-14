#!/bin/bash -x
source ~/.bashrc
#source /etc/profile.d/python.sh
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

chmod 777 *
sudo chown jao:jao 20*

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

echo ''
echo '============='
echo ''

if [ -s temp.txt  ]
then
 echo $i' IS NOT READY'
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


#mv /fromDMG/automatic/2012* /fromDMG/automatic/cycle1/
#mv /fromDMG/automatic/2013* /fromDMG/automatic/cycle2/

mv /fromARCS/READY/2012* /fromARCS/cycle1
mv /fromARCS/READY/2013* /fromARCS/cycle2
mv /fromARCS/READY/2015* /fromARCS/cycle3
mv /fromARCS/READY/2016* /fromARCS/cycle4


#CYCLE 1

#cd /fromDMG/automatic/cycle1/

cd /fromARCS/cycle1

#wget --http-user=arcsci --http-password="a&6%oi8" http://www.alma.cl/~evillard/ProjectTracking/Cycle1/ArchiveScientist/schedblocks_APPROVED_FOR_DELIVERY.txt

wget http://dmg02.sco.alma.cl:8000/aida/plain/getApprovedForDeliveryCycle1.txt -O schedblocks_APPROVED_FOR_DELIVERY.txt

cat schedblocks_APPROVED_FOR_DELIVERY.txt | tail -n +4 | cut -f3,5 > temp.txt

cat temp.txt | cut --complement -c15 > temp2.txt

for i in `cat temp2.txt`; do echo $i | sed -e 's$uid://$_uid___$' -e 's$/$_$g' >> temp3.txt; done;

cat temp3.txt | sort > temp4.txt

ls | cut -f1 | grep '\.tar$' | grep '^20' | sed -e 's/_001_of_001.tar//g' > lista.txt

comm -1 -2 temp4.txt lista.txt > ingestion.txt

for i in `cat ingestion.txt`; do tar=$(echo $i | sed 's/$/_001_of_001.tar/'); md5=$(echo $tar | sed 's/$/.md5sum/'); mkdir $i; mv $tar $i; mv $md5 $i; cd $i ;all_automatic_dmg.py $tar; cd ..;done;

rm -rf *.txt
rm -rf *.txt.*

#scp log.html root@10.200.114.115:/var/www/html/cycle1.html

#CYCLE 2

#cd /fromDMG/automatic/cycle2/
cd /fromARCS/cycle2/

#wget --http-user=arcsci --http-password="a&6%oi8" http://www.alma.cl/~evillard/ProjectTracking/Cycle2/ArchiveScientist/schedblocks_APPROVED_FOR_DELIVERY.txt

wget http://dmg02.sco.alma.cl:8000/aida/plain/getApprovedForDeliveryCycle2.txt -O schedblocks_APPROVED_FOR_DELIVERY.txt 

cat schedblocks_APPROVED_FOR_DELIVERY.txt | tail -n +4 | cut -f3,5 > temp.txt

cat temp.txt | cut --complement -c15 > temp2.txt

for i in `cat temp2.txt`; do echo $i | sed -e 's$uid://$_uid___$' -e 's$/$_$g' >> temp3.txt; done;

cat temp3.txt | sort > temp4.txt

ls | cut -f1 | grep '\.tar$' | grep '^20' | sed -e 's/_001_of_001.tar//g' > lista.txt

comm -1 -2 temp4.txt lista.txt > ingestion.txt

for i in `cat ingestion.txt`; do tar=$(echo $i | sed 's/$/_001_of_001.tar/'); md5=$(echo $tar | sed 's/$/.md5sum/'); mkdir $i; mv $tar $i; mv $md5 $i; cd $i ;all_automatic_dmg.py $tar; cd ..;done;

rm -rf *.txt
rm -rf *.txt.*

#CYCLE 3

cd /fromARCS/cycle3/

wget --http-user=arcsci --http-password="a&6%oi8" http://www.alma.cl/~evillard/ProjectTracking/Cycle3/ArchiveScientist/schedblocks_APPROVED_FOR_DELIVERY.txt

#wget http://dmg02.sco.alma.cl:8000/aida/plain/getApprovedForDeliveryCycle3.txt -O schedblocks_APPROVED_FOR_DELIVERY.txt

cat schedblocks_APPROVED_FOR_DELIVERY.txt | tail -n +4 | cut -f3,5 > temp.txt

cat temp.txt | cut --complement -c15 > temp2.txt

for i in `cat temp2.txt`; do echo $i | sed -e 's$uid://$_uid___$' -e 's$/$_$g' >> temp3.txt; done;

cat temp3.txt | sort > temp4.txt

ls | cut -f1 | grep '\.tar$' | grep '^20' | sed -e 's/_001_of_001.tar//g' > lista.txt

comm -1 -2 temp4.txt lista.txt > ingestion.txt

for i in `cat ingestion.txt`; do tar=$(echo $i | sed 's/$/_001_of_001.tar/'); md5=$(echo $tar | sed 's/$/.md5sum/'); mkdir $i; mv $tar $i; mv $md5 $i; cd $i ;all_automatic_dmg.py $tar; cd ..;done;

rm -rf *.txt
rm -rf *.txt.*

echo SUCCESSFULLY ENDED

#REDUNDANCY WITH FMORALES EPT

cd /fromARCS/cycle3/

#wget --http-user=arcsci --http-password="a&6%oi8" http://www.alma.cl/~evillard/ProjectTracking/Cycle3/ArchiveScientist/schedblocks_APPROVED_FOR_DELIVERY.txt

wget http://dmg02.sco.alma.cl:8000/aida/plain/getApprovedForDeliveryCycle3.txt -O schedblocks_APPROVED_FOR_DELIVERY.txt

cat schedblocks_APPROVED_FOR_DELIVERY.txt | tail -n +4 | cut -f3,5 > temp.txt

cat temp.txt | cut --complement -c15 > temp2.txt

for i in `cat temp2.txt`; do echo $i | sed -e 's$uid://$_uid___$' -e 's$/$_$g' >> temp3.txt; done;

cat temp3.txt | sort > temp4.txt

ls | cut -f1 | grep '\.tar$' | grep '^20' | sed -e 's/_001_of_001.tar//g' > lista.txt

comm -1 -2 temp4.txt lista.txt > ingestion.txt

for i in `cat ingestion.txt`; do tar=$(echo $i | sed 's/$/_001_of_001.tar/'); md5=$(echo $tar | sed 's/$/.md5sum/'); mkdir $i; mv $tar $i; mv $md5 $i; cd $i ;all_automatic_dmg.py $tar; cd ..;done;

rm -rf *.txt
rm -rf *.txt.*

echo SUCCESSFULLY ENDED

#END OF REDUNDANCY







#scp log.html root@10.200.114.115:/var/www/html/cycle2.html


#CYCLE 4

cd /fromARCS/cycle4/

wget --http-user=arcsci --http-password="a&6%oi8" http://www.alma.cl/~evillard/ProjectTracking/Cycle4/ArchiveScientist/schedblocks_APPROVED_FOR_DELIVERY.txt

#wget http://dmg02.sco.alma.cl:8000/aida/plain/getApprovedForDeliveryCycle4.txt -O schedblocks_APPROVED_FOR_DELIVERY.txt

cat schedblocks_APPROVED_FOR_DELIVERY.txt | tail -n +4 | cut -f3,5 > temp.txt

cat temp.txt | cut --complement -c15 > temp2.txt

for i in `cat temp2.txt`; do echo $i | sed -e 's$uid://$_uid___$' -e 's$/$_$g' >> temp3.txt; done;

cat temp3.txt | sort > temp4.txt

ls | cut -f1 | grep '\.tar$' | grep '^20' | sed -e 's/_001_of_001.tar//g' > lista.txt

comm -1 -2 temp4.txt lista.txt > ingestion.txt

for i in `cat ingestion.txt`; do tar=$(echo $i | sed 's/$/_001_of_001.tar/'); md5=$(echo $tar | sed 's/$/.md5sum/'); mkdir $i; mv $tar $i; mv $md5 $i; cd $i ;all_automatic_dmg.py $tar; cd ..;done;

rm -rf *.txt
rm -rf *.txt.*

echo SUCCESSFULLY ENDED

#scp log.html root@10.200.114.115:/var/www/html/cycle2.html



