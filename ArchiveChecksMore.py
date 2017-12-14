echo 'LUSTRE SPACE'
echo '============'
echo ''
ssh root@jaopost001.sco.alma.cl lfs df -h
echo ''
echo 'LUSTRE INODES'
echo '============='
echo ''
echo '--------------------------------'
echo ''
ssh root@jaopost001.sco.alma.cl lfs df -i
echo ''
echo 'OSS 01 RAIDS'
echo '============'
echo ''
ssh root@jaopost-oss01.sco.alma.cl /opt/MegaRAID/storcli/storcli64 show
echo ''
echo 'OSS 02 RAIDS'
echo '============'
echo ''
ssh root@jaopost-oss02.sco.alma.cl /opt/MegaRAID/storcli/storcli64 show
echo ''
echo 'OSS 03 RAIDS'
echo '============'
echo ''
ssh root@jaopost-oss03.sco.alma.cl /opt/MegaRAID/storcli/storcli64 show
echo ''
echo 'OSS 04 RAIDS'
echo '============'
echo ''
ssh root@jaopost-oss04.sco.alma.cl /opt/MegaRAID/storcli/storcli64 show
echo ''
echo 'OSS 06 RAIDS (OSS 05 is currently used for test)'
echo '================================================'
echo ''
ssh root@jaopost-oss06.sco.alma.cl /opt/MegaRAID/storcli/storcli64 show
echo ''
echo 'There is a INACTIVE RAID here'
ssh root@jaopost-oss06.sco.alma.cl /opt/MegaRAID/storcli/storcli64 /c0 show
echo 'PING TO NRAO SERVER FOR SYNCRONIZING'
echo ''
ping -c 5 10.2.96.86
echo ''
echo 'HARVESTER PROCESS'
echo ''
ssh root@harvester64.sco.alma.cl ps -fea | grep harvest | grep bin
echo ''
echo 'LOGS'
echo '===='
echo ''
#ls /data/toARCS/harvester_logs/
ls /data/toARCS/harvester_logs/ | tail -n 6 | grep -v APO
echo ''
variable_dia=$(date +"%Y-%m-%d" --date='yesterday')
echo ''
echo 'Checking harvester.log, only showing 50 lines of errors'
echo ''
echo 'Last 50 lines'
echo '-------------'
echo ''
ssh root@harvester64.sco.alma.cl cat /users/almaproc/harvester/Harvester/harvester.log | tail -n 50
echo ''
echo 'Last 10 lines with ERROR'
echo '------------------------'
echo ''
ssh root@harvester64.sco.alma.cl cat /users/almaproc/harvester/Harvester/harvester.log | grep -i ERROR | tail -n 10
echo ''
echo 'Last 10 lines with ORA-'
echo '-----------------------'
echo ''
ssh root@harvester64.sco.alma.cl cat /users/almaproc/harvester/Harvester/harvester.log | grep -i ORA- | tail -n 10
echo ''
echo 'Last 10 lines with ORA-00600'
echo '----------------------------'
echo ''
ssh root@harvester64.sco.alma.cl cat /users/almaproc/harvester/Harvester/harvester.log | grep -i ORA-00600 | tail -n 10
echo ''






#echo 'ORA-00600 ERROR in current log'
#echo ''
#ssh root@harvester64.sco.alma.cl cat /users/almaproc/harvester/Harvester/harvester.log | grep ORA-00600
echo ''
echo 'Amount of ORA-00600 errors'
ssh root@harvester64.sco.alma.cl cat /users/almaproc/harvester/Harvester/harvester.log | grep ORA-00600 | wc -l
#echo ''
#echo 'ORA- ERROR in current log'
#echo ''
#ssh root@harvester64.sco.alma.cl cat /users/almaproc/harvester/Harvester/harvester.log | grep ORA-
#echo ''
echo 'Amount of ORA errors'
ssh root@harvester64.sco.alma.cl cat /users/almaproc/harvester/Harvester/harvester.log | grep ORA- | wc -l
echo ''
echo 'For errors create an ICT Ticket against Harvester'
echo ''
echo 'JAOPOST NODES'
echo '============='
echo ''
ssh root@jaopost-master.sco.alma.cl pbsnodes | grep down | wc -l
echo ''
echo 'if output is greater than 0, connect to jaopost-master and perform'
echo 'pbsnodes and look for the machine with down status and reboot it'
echo ''

