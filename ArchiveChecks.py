#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import cx_Oracle
import os
import getpass
import sys
import paramiko
import ssl
import urllib2
import ast


#server = 'dmg06.osf.alma.cl'
#tnsname = 'DMG06'

def printSensorData(sensorId, user, passwd):
        url1='https://prtg.alma.cl/api/getsensordetails.json?username='+user+'&password='+passwd+'&id='+str(sensorId)
        req = urllib2.Request(url1, headers={ 'X-Mashape-Key': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' })
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        info = urllib2.urlopen(req, context=gcontext).read()
        dict1 = ast.literal_eval(info)
        print dict1["sensordata"]["name"]+': '+dict1["sensordata"]["lastvalue"]



def pgprint(desc,rows,tot=True):
     """pretty print a query result set, a la postgresql"""

     ncols=len(desc)

     # each column is at least as wide as its header
     # grab the type of each column so we can rjust numbers
     maxlen=[]
     types=[]
     for i in desc:
         maxlen.append(len(i[0]))
         types.append(i[1])

     # get the max width of each column
     for r in rows:
         for i in range(0,ncols):
             tmps=str(r[i])
             tmpl=len(tmps)
             if maxlen[i]<tmpl:
                 maxlen[i]=tmpl

     # print header
     line=""
     for i in range(0,ncols):
         if (i>0): line +=' | '
         line+=desc[i][0].center(maxlen[i]).lower()
     print line

     # underline
     line=""
     for i in range(0,ncols):
         if (i>0): line +='-+-'
         line+='-'*maxlen[i]
     print line

     # rows
     for r in rows:
         line=""
         for i in range(0,ncols):
             if (i>0): line+=' | '
             if types[i]==cx_Oracle.NUMBER:
                 line+=str(r[i]).rjust(maxlen[i])
             else:
                 line+=str(r[i]).ljust(maxlen[i])
         print line
     if tot:
         print '(%d rows)'%(len(rows))


if __name__ == '__main__':

#	stdout, stderr = Popen(['ssh','oracle@'+server,'source ~/.bash_profile ; tnsping '+tnsname], stdout=PIPE).communicate()
#	print '##### Database PING #####'
#	print(stdout)


	#dsn = cx_Oracle.makedsn(server, 1521, tnsname)
	print ""
	print '######## SSH CHECKS #######'
	casauser = raw_input("Enter user for CASA and RED-OSF: ")
	casapass = getpass.getpass('password :')
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	passwd = getpass.getpass('Enter password for almasu: ')
	ngasdbpasswd = getpass.getpass('Enter password for ngas db: ')
	ngaspass = getpass.getpass('password for ssh user ngas :')
	ape1passwd = getpass.getpass('password for root at ape2 :')
	prtguser = raw_input('user for PRTG (ex: alejandro.barrientos) :')
	prtgpasswd = getpass.getpass('password for PRTG user '+prtguser+' :')
	print ""
#	ssh.connect('ngas01.sco.alma.cl', username='ngas', password=ngaspass)
#	stdin, stdout, stderr = ssh.exec_command("netstat -t -n | grep 1521 | wc -l")
#	for line in stdout:

#		sys.stdout.write('amount of connections in port 1521 for ngas01.sco.alma.cl: ' + line)
#	ssh.connect('ngas02.sco.alma.cl', username='ngas', password=ngaspass)
#	stdin, stdout, stderr = ssh.exec_command("netstat -t -n | grep 1521 | wc -l")
#	for line in stdout:
#		sys.stdout.write('amount of connections in port 1521 for ngas02.sco.alma.cl: ' + line)	
#	ssh.connect('ngas03.sco.alma.cl', username='ngas', password=ngaspass)
#	stdin, stdout, stderr = ssh.exec_command("netstat -t -n | grep 1521 | wc -l")
#	for line in stdout:
#		sys.stdout.write('amount of connections in port 1521 for ngas03.sco.alma.cl: ' + line)
#	ssh.connect('ngas04.sco.alma.cl', username='ngas', password=ngaspass)
#	stdin, stdout, stderr = ssh.exec_command("netstat -t -n | grep 1521 | wc -l")
#	for line in stdout:
#		sys.stdout.write('amount of connections in port 1521 for ngas04.sco.alma.cl: ' + line)
        
	try:
		ssh.connect('tfint-gns.aiv.alma.cl', username=casauser, password=casapass)
		stdin, stdout, stderr = ssh.exec_command("/users/abarrien/NGASCheckup/ngasCheckup.sh")
		print ""
		print '---- NGAS Retrieval test at OSF -----'
		for line in stdout:
			sys.stdout.write(line)
	except Exception as e:
		print "exception: " + str(e)
	try:
		stdin, stdout, stderr = ssh.exec_command("/users/abarrien/NGASCheckup/ngasCheckup-SCO.sh")
		print ""
		print '---- NGAS Retrieval test at SCO -----'
        	for line in stdout:
                	sys.stdout.write(line)   	
	except Exception as e:
		print "exception: " + str(e)
	try:		
		print '---- NGAS Status Check ----'
		stdin, stdout, stderr = ssh.exec_command("python /users/abarrien/NGASCheckup/ngasStatus.py -a")
		print ""
		print '---- NGAS Status at OSF, SCO -----'
		for line in stdout:
			sys.stdout.write(line)
	except Exception as e:
		print "exception: " + str(e)
	try:		
		stdin, stdout, stderr = ssh.exec_command("ls -ltrha /mnt/gas01/data1/archiverd/NGAMS_ARCHIVE_CLIENT/queue/ |wc -l")
		print ""
		print '---- Number of files at NgamsArchiveClient Queue at TFINT -----'
		for line in stdout:
			sys.stdout.write(line)
	except Exception as e:
		print "exception: " + str(e)
	try:		
		stdin, stdout, stderr = ssh.exec_command("ssh gas01 'ps -fea | grep ngams'")
		print ""
		print '---- NgamsArchiveClient process at TFINT -----'
		for line in stdout:
			sys.stdout.write(line)
	except Exception as e:
		print "exception: " + str(e)
#	try:		
#		ssh.connect('tfsd-gns.aiv.alma.cl', username=casauser, password=casapass)
#		stdin, stdout, stderr = ssh.exec_command("ls -ltrha /mnt/gas01/data1/archiverd/NGAMS_ARCHIVE_CLIENT/queue/ |wc -l")
#		print ""
#		print '---- Number of files at NgamsArchiveClient Queue at TFSD -----'
#		for line in stdout:
#			sys.stdout.write(line)
#	except Exception as e:
#		print "exception: " + str(e)
#	try:
#		stdin, stdout, stderr = ssh.exec_command("ssh gas01 'ps -fea | grep ngams'")
#		print ""
#		print '---- NgamsArchiveClient process at TFSD -----'
#		for line in stdout:
#			sys.stdout.write(line)
#	except Exception as e:
#		print "exception: " + str(e)
	try:		
		
		ssh.connect('ape2-gns.osf.alma.cl', username='root', password=ape1passwd)
		stdin, stdout, stderr = ssh.exec_command('ssh gas03 "ls -ltrha /mnt/gas03/data2/archiverd/NGAMS_ARCHIVE_CLIENT/queue/ |wc -l"')
		print ""
		print '---- Number of files at NgamsArchiveClient Queue at APE2 -----'
		for line in stdout:
			sys.stdout.write(line)
	except Exception as e:
		print "exception: " + str(e)
	try:    
		stdin, stdout, stderr = ssh.exec_command("ssh gas03 'ps -fea | grep ngams'")
		print ""
		print '---- NgamsArchiveClient process at APE2 -----'
		for line in stdout:
			sys.stdout.write(line)
	except Exception as e:
		print "exception: " + str(e)

#	print ""
#	print '#######  ORACLE CHECKS ########'
#	print 'Connecting to OSF Database'
	dsn = '''(DESCRIPTION_LIST =
   (FAILOVER = TRUE)
  (LOAD_BALANCE = FALSE)
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = ora.osf.alma.cl)(PORT = 1521))
      (CONNECT_DATA =
        (SERVER = DEDICATED)
        (SERVICE_NAME = OFFLINE.OSF.CL)
      )
    )
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = orastbosf1.osf.alma.cl)(PORT = 1521))
      (CONNECT_DATA =
        (SERVER = DEDICATED)
        (SERVICE_NAME = OFFLINE.OSF.CL)
      )
    )
  )'''
	dsn2 = ''' (DESCRIPTION_LIST =
    (FAILOVER = TRUE)
    (LOAD_BALANCE = FALSE)
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = ora1.sco.alma.cl)(PORT = 1521))
      (CONNECT_DATA =
        (SERVER = DEDICATED)
        (SERVICE_NAME = OFFLINE.SCO.CL)
      )
    )
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = orastbsco1.sco.alma.cl)(PORT = 1521))
      (CONNECT_DATA =
        (SERVER = DEDICATED)
        (SERVICE_NAME = OFFLINE.SCO.CL)
      )
    )
  )'''

	orcl = cx_Oracle.connect('almasu', passwd, dsn)
	cursorosf = orcl.cursor()
	orcl = cx_Oracle.connect('almasu', passwd, dsn2)
	cursorsco = orcl.cursor()
	orcl = cx_Oracle.connect('ngas', ngasdbpasswd, dsn2)
	cursor2 = orcl.cursor()
	print ""
#	print '##### Instance Status #####'
#	cursorosf.execute('select instance_name, status, database_status from v$instance')
#	while 1:
#        	row = cursorosf.fetchone()
#        	if row == None:
#          	      break
#       		else:
#			print 'Instance: '+row[0]
#			print 'Status: ' +row[1]
#			print 'Database Status: '+row[2]
#
	#print '##### Database uptime #####'
	#cursor.execute('''select SYSDATE-logon_time "Days", (SYSDATE-logon_time)*24 "Hours"
#from   sys.v_$session
#where  sid=1 /* this is PMON */''')
#	pgprint(cursor.description,cursor.fetchall())
#	print ""
#	print '##### Tablespaces #####'

#	cursorosf.execute('select * from almasu.dbo_tablespaces')
#	pgprint(cursorosf.description,cursorosf.fetchall())
	
	#print '##### Streams #####'
	#cursor.execute('''select streams_name, streams_type, first_message_time, last_message_time from v$streams_transaction''')
	#pgprint(cursor.description,cursor.fetchall())	
	
	print "Connecting to SCO Database"
	
	print ""
	print '##### NGAS File Size ingested last 7 days #####'
        cursorsco.execute('''select 
    substr(replace(ingestion_date,'T',' '),1,10) as ingestion,
    to_char(round((sum(file_size)/1048576),2),'999,999,999.99') as Insertion_in_MB 
from NGAS.NGAS_FILES 
where 
    to_date(substr(replace(ingestion_date,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > sysdate-7
GROUP BY SUBSTR(REPLACE(INGESTION_DATE,'T',' '),1,10) 
order by 1''')
        pgprint(cursorsco.description,cursorsco.fetchall())
       

	print '##### Days left to complete NGAS SCO based on weekly ingestion average #####'
        cursorsco.execute('''SELECT ROUND(
  (SELECT SUM(AVAILABLE_MB) FROM ngas.ngas_disks WHERE completed = 0
  )                     /
  (SELECT SUM(file_size)/1024/1024/8
  FROM NGAS.NGAS_FILES
  WHERE to_date(SUBSTR(REPLACE(ingestion_date,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > sysdate-7
  ),2) days_until_complete
FROM dual''')
        pgprint(cursorsco.description,cursorsco.fetchall())








 
        
	print '##### NGAS Mirroring OSF-SCO, Files pending (7 Days) #####'
	try:
		cursor2.execute('''
SELECT count(*) , round(sum(src.file_size)/1024/1024/1024,2) GB FROM
    ( SELECT
        D.HOST_ID,
        F.FILE_ID,
        F.FILE_VERSION,
        F.FILE_SIZE,
        F.INGESTION_DATE
    FROM
        NGAS_FILES@NGASGG.LOCAL.CL F,
        NGAS_DISKS@NGASGG.LOCAL.CL D
    WHERE
        D.DISK_ID = F.DISK_ID
        AND D.HOST_ID LIKE 'ngobe%'
        AND F.INGESTION_DATE >= TO_CHAR(TRUNC(SYSDATE-7), 'YYYY-MM-DD')
        AND F.FILE_ID LIKE  'A00%' ) SRC
LEFT JOIN
    ( SELECT
        F.FILE_ID,
        F.FILE_VERSION,
        F.FILE_SIZE,
        F.INGESTION_DATE
        FROM NGAS.NGAS_FILES F
        WHERE F.INGESTION_DATE >= TO_CHAR(TRUNC(SYSDATE-7), 'YYYY-MM-DD') ) DST
ON ( SRC.FILE_ID = DST.FILE_ID AND SRC.FILE_VERSION = DST.FILE_VERSION )
WHERE
   DST.FILE_ID IS NULL
''') 
		pgprint(cursor2.description,cursor2.fetchall())
	except:
				print "Problems Executing query"
				
	


	print '########## Duplicated files at SCO  ###############'
	try:
		cursorsco.execute(''' SELECT count(*)
  FROM ngas.ngas_files
 WHERE ROWID IN
     (SELECT ROWID
        FROM ngas.ngas_files
       WHERE (file_id, file_version) IN
           (SELECT file_id, file_version
              FROM ngas.ngas_files
             GROUP BY file_id, file_version
            HAVING COUNT(*) >= 2)
      MINUS
      SELECT MIN(ROWID)
        FROM ngas.ngas_files
       WHERE (file_id, file_version) IN
           (SELECT file_id, file_version
              FROM ngas.ngas_files
             GROUP BY file_id, file_version
            HAVING COUNT(*) >= 2)
       GROUP BY file_id, file_version) ''')
		pgprint(cursorsco.description,cursorsco.fetchall())
	except:
		print "Problems Executing query" 
	
	
	print '############ Zero byte files at SCO ###########'
	try:
		cursorsco.execute(''' select count(*) from ngas.ngas_files where file_size = 0 ''')
		pgprint(cursorsco.description,cursorsco.fetchall())
	except:
		print 'error while executing query'

	#backlogdays = raw_input('how many days of backlog in the arcs you want to check?: ')
	backlogdays='15'
	print '########## NA ARC Backlog ('+backlogdays+' days) ###############'
	try:
#		cursorsco.execute('''SELECT
#		COUNT(SRC.FILE_ID) FILES_IN_BACKLOG,
#		ROUND(SUM(SRC.FILE_SIZE/1024/1024/1024),4) SIZE_IN_GB
#	FROM
#		(SELECT FILE_ID,FILE_VERSION,FILE_SIZE,CHECKSUM,INGESTION_DATE 
#		FROM NGAS.NGAS_FILES 
#		WHERE TO_DATE(SUBSTR(REPLACE(INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > SYSDATE-'''+backlogdays+''') SRC LEFT JOIN
#		(SELECT FILE_ID,FILE_VERSION,FILE_SIZE,CHECKSUM,INGESTION_DATE 
#		FROM NGAS.NGAS_FILES@ALMA.ARC.NA
#		WHERE TO_DATE(SUBSTR(REPLACE(INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > SYSDATE-'''+backlogdays+''') DST ON (SRC.FILE_ID = DST.FILE_ID AND SRC.FILE_VERSION = DST.FILE_VERSION)
#	WHERE
#	   DST.FILE_ID IS NULL and (SRC.FILE_ID like 'A002%' or SRC.FILE_ID like '%.tar') And SRC.FILE_ID not like 'TEST%.tar' ''')
		cursorsco.execute('''SELECT COUNT(SRC.FILE_ID) FILES_IN_BACKLOG,ROUND(SUM(SRC.FILE_SIZE/1024/1024/1024),2) SIZE_IN_GB 
from NGAS.NGAS_FILES SRC WHERE 
TO_DATE(SUBSTR(REPLACE(INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > SYSDATE-:backlogdays AND 
FILE_ID || '.' || FILE_VERSION || '.' || CHECKSUM not in (select FILE_ID || '.' || FILE_VERSION || '.' || CHECKSUM 
from ngas.ngas_files@ALMA.ARC.NA WHERE 
TO_DATE(SUBSTR(REPLACE(INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > SYSDATE-:backlogdays) AND 
(SRC.FILE_ID like 'A002%' or SRC.FILE_ID like '%.tar') AND SRC.FILE_ID not like 'TEST%.tar' ''',{'backlogdays':backlogdays})

		pgprint(cursorsco.description,cursorsco.fetchall())
	except:
		print "Problems connecting to NA ARC"
		
	print ""
	print '########## EU ARC Backlog ('+backlogdays+' days) ###############'
	try:
#		cursorsco.execute('''SELECT
#		COUNT(SRC.FILE_ID) FILES_IN_BACKLOG,
#		ROUND(SUM(SRC.FILE_SIZE/1024/1024/1024),4) SIZE_IN_GB
#	FROM
#		(SELECT FILE_ID,FILE_VERSION,FILE_SIZE,CHECKSUM,INGESTION_DATE 
#		FROM NGAS.NGAS_FILES 
#		WHERE TO_DATE(SUBSTR(REPLACE(INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > SYSDATE-'''+backlogdays+''') SRC LEFT JOIN
#		(SELECT FILE_ID,FILE_VERSION,FILE_SIZE,CHECKSUM,INGESTION_DATE 
#		FROM NGAS.NGAS_FILES@ALMA.ARC.EU
#		WHERE TO_DATE(SUBSTR(REPLACE(INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > SYSDATE-'''+backlogdays+''') DST ON (SRC.FILE_ID = DST.FILE_ID AND SRC.FILE_VERSION = DST.FILE_VERSION)
#	WHERE
#	   DST.FILE_ID IS NULL and (SRC.FILE_ID like 'A002%' or SRC.FILE_ID like '%.tar') And SRC.FILE_ID not like 'TEST%.tar' ''')
		cursorsco.execute('''SELECT COUNT(SRC.FILE_ID) FILES_IN_BACKLOG,ROUND(SUM(SRC.FILE_SIZE/1024/1024/1024),2) SIZE_IN_GB 
from NGAS.NGAS_FILES SRC WHERE 
TO_DATE(SUBSTR(REPLACE(INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > SYSDATE- :backlogdays AND 
FILE_ID || '.' || FILE_VERSION || '.' || CHECKSUM not in (select FILE_ID || '.' || FILE_VERSION || '.' || CHECKSUM 
from ngas.ngas_files@ALMA.ARC.EU WHERE 
TO_DATE(SUBSTR(REPLACE(INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > SYSDATE- :backlogdays) AND 
(SRC.FILE_ID like 'A002%' or SRC.FILE_ID like '%.tar') AND SRC.FILE_ID not like 'TEST%.tar' ''',{'backlogdays':backlogdays})

		pgprint(cursorsco.description,cursorsco.fetchall())
	except:
		print "Problems connecting to EU ARC"
	print ""
	print '########## EA ARC Backlog ('+backlogdays+' days) ###############'
	try:
#		cursorsco.execute('''SELECT
#		COUNT(SRC.FILE_ID) FILES_IN_BACKLOG,
#		ROUND(SUM(SRC.FILE_SIZE/1024/1024/1024),4) SIZE_IN_GB
#	FROM
#		(SELECT FILE_ID,FILE_VERSION,FILE_SIZE,CHECKSUM,INGESTION_DATE 
#		FROM NGAS.NGAS_FILES 
#		WHERE TO_DATE(SUBSTR(REPLACE(INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > SYSDATE-'''+backlogdays+''') SRC LEFT JOIN
#		(SELECT FILE_ID,FILE_VERSION,FILE_SIZE,CHECKSUM,INGESTION_DATE 
#		FROM NGAS.NGAS_FILES@ALMA2.ARC.EA
#		WHERE TO_DATE(SUBSTR(REPLACE(INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > SYSDATE-'''+backlogdays+''') DST ON (SRC.FILE_ID = DST.FILE_ID AND SRC.FILE_VERSION = DST.FILE_VERSION)
#	WHERE
#	   DST.FILE_ID IS NULL and (SRC.FILE_ID like 'A002%' or SRC.FILE_ID like '%.tar') And SRC.FILE_ID not like 'TEST%.tar' ''')

		cursorsco.execute('''SELECT COUNT(SRC.FILE_ID) FILES_IN_BACKLOG,ROUND(SUM(SRC.FILE_SIZE/1024/1024/1024),2) SIZE_IN_GB 
from NGAS.NGAS_FILES SRC WHERE 
TO_DATE(SUBSTR(REPLACE(INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > SYSDATE-'''+backlogdays+''' AND 
FILE_ID || '.' || FILE_VERSION || '.' || CHECKSUM not in (select FILE_ID || '.' || FILE_VERSION || '.' || CHECKSUM 
from ngas.ngas_files@ALMA.ARC.EA WHERE 
TO_DATE(SUBSTR(REPLACE(INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > SYSDATE-'''+backlogdays+''') AND 
(SRC.FILE_ID like 'A002%' or SRC.FILE_ID like '%.tar') AND SRC.FILE_ID not like 'TEST%.tar' ''')
		pgprint(cursorsco.description,cursorsco.fetchall())
	except:
		print "Problems connecting to EA ARC"

	print ""
	print '########## LAST INSERTION INTO ASA TABLES ##############'
	try:
		cursorsco.execute('''select (sysdate + (sysdate - max(end_date)) - sysdate)*24  as HoursAgo from alma.asa_science ''')
		pgprint(cursorsco.description,cursorsco.fetchall())
		print ""
	except:
		print "Problems calculating last insertion into asa tables"





	try:
                ssh.connect('arcproc.sco.alma.cl', username='jao', password='jao')
		print ""
		print "logged into arcproc"
                stdin, stdout, stderr = ssh.exec_command("cat /proc/cpuinfo | grep processor | wc -l")
		numberofcpus = 1.0
		for line in stdout:
			numberofcpus = float(line)
			print "number of cpu's: "+ str(numberofcpus)
		stdin, stdout, stderr = ssh.exec_command("MYAR=\"$(uptime)\";echo ${MYAR##*load} |awk {'print $2'}|sed s/','/''/g")
		loadaverage=0.0
		for line in stdout:
			loadaverage= float(line)
			print "load average: "+str(loadaverage)
		print "Real Load: " +str(loadaverage/numberofcpus)
		stdin, stdout, stderr = ssh.exec_command("df -h")
		print ""
                print '---- PARTITIONS ARCPROC -----'
                for line in stdout:
                        sys.stdout.write(line)
        except:
                print "Problems connecting to arcproc.sco.alma.cl"

        try:
                ssh.connect('jaopost001.sco.alma.cl', username=casauser, password=casapass)
                print "logged into jaopost"
                stdin, stdout, stderr = ssh.exec_command("cat /proc/cpuinfo | grep processor | wc -l")
                numberofcpus = 1.0
                for line in stdout:
                        numberofcpus = float(line)
                        print "number of cpu's: "+ str(numberofcpus)
                stdin, stdout, stderr = ssh.exec_command("MYAR=\"$(uptime)\";echo ${MYAR##*load} |awk {'print $2'}|sed s/','/''/g")
                loadaverage=0.0
                for line in stdout:
                        loadaverage= float(line)
                        print "load average: "+str(loadaverage)
                print "Normalized Load: " +str(loadaverage/numberofcpus)
                stdin, stdout, stderr = ssh.exec_command("lfs df -h")
                print ""
                print '---- JAOPOST LUSTRE SPACE -----'
		for line in stdout:
                	sys.stdout.write(line)
		stdin, stdout, stderr = ssh.exec_command("lfs df -i")

                print ""
                print '---- JAOPOST LUSTRE INODES -----'
                for line in stdout:
                        sys.stdout.write(line)
        except:
                print "Problems connecting to jaopost001.sco.alma.cl"



	serverlist = ['jaopost020.sco.alma.cl', 'tfint-gns.aiv.alma.cl','red-osf.osf.alma.cl','sciops01.sco.alma.cl','sciops02.sco.alma.cl','sciops03.sco.alma.cl','sciops04.sco.alma.cl' ]
	for server in serverlist:
	 
		try:
                	ssh.connect(server, username=casauser, password=casapass)
			print "Logged into: "+server
                	stdin, stdout, stderr = ssh.exec_command("cat /proc/cpuinfo | grep processor | wc -l")
                	numberofcpus = 1.0
                	for line in stdout:
                        	numberofcpus = float(line)
                        	print "number of cpu's: "+ str(numberofcpus)
                	stdin, stdout, stderr = ssh.exec_command("MYAR=\"$(uptime)\";echo ${MYAR##*load} |awk {'print $2'}|sed s/','/''/g")
                	loadaverage=0.0
                	for line in stdout:
                        	loadaverage= float(line)
                        	print "load average: "+str(loadaverage)
                	print "Normalized Load: " +str(loadaverage/numberofcpus)
			stdin, stdout, stderr = ssh.exec_command("smem -sswap -r -p| head -5")
                        print ""
                        print '---- Top Swap usage processes for '+server+' -----'
			for line in stdout:
                                sys.stdout.write(line)

			stdin, stdout, stderr = ssh.exec_command("df -h")
                	print ""
                	print '---- PARTITIONS AT '+server+' -----'
                	for line in stdout:
                        	sys.stdout.write(line)
        	except:
                	print "Problems connecting to "+server

        ngasserverlist = ['ngofe01.osf.alma.cl', 'ngofe02.osf.alma.cl','ngofe03.osf.alma.cl','ngobe01.osf.alma.cl','ngobe02.osf.alma.cl','ngas01.sco.alma.cl','ngas02.sco.alma.cl','ngas03.sco.alma.cl','ngas04.sco.alma.cl']
        for server in ngasserverlist:

                try:
                        ssh.connect(server, username='ngas', password=ngaspass)
                        stdin, stdout, stderr = ssh.exec_command("cat /proc/cpuinfo | grep processor | wc -l")
                        numberofcpus = 1.0
                        for line in stdout:
                                numberofcpus = float(line)
                                print "number of cpu's: "+ str(numberofcpus)
                        stdin, stdout, stderr = ssh.exec_command("MYAR=\"$(uptime)\";echo ${MYAR##*load} |awk {'print $2'}|sed s/','/''/g")
                        loadaverage=0.0
                        for line in stdout:
                                loadaverage= float(line)
                                print "load average: "+str(loadaverage)
                        print "Normalized Load: " +str(loadaverage/numberofcpus)                        
			stdin, stdout, stderr = ssh.exec_command("df -h")
                        print ""
                        print '---- PARTITIONS AT '+server+' -----'
                        for line in stdout:
                                sys.stdout.write(line)
                except:
                        print "Problems connecting to "+server


	try:
		print "Connectivity test: NGAS FE -> BE"
		ssh.connect('ngofe01.osf.alma.cl', username='ngas', password=ngaspass)
                stdin, stdout, stderr = ssh.exec_command("ping -c 3 ngobe01.osf.alma.cl")
		exitstatus = stdout.channel.recv_exit_status()
		if exitstatus == 0:
			print 'OK'
		else:
			print 'NOT OK'
	except:
                print "Problems connecting to NGAS FE"	

        try:
                print "Connectivity test: NGAS BE -> SCO"
                ssh.connect('ngobe01.osf.alma.cl', username='ngas', password=ngaspass)
                stdin, stdout, stderr = ssh.exec_command("ping -c 3 ngas01.sco.alma.cl")
                exitstatus = stdout.channel.recv_exit_status()
                if exitstatus == 0:
                        print 'OK'
                else:
                        print 'NOT OK'
        except:
                print "Problems connecting to NGAS BE"


        print "############### File Consistency checksum test between osf and sco, last 4 days"
        cursor2.execute('''SELECT
    AL2.FILE_ID ORIGIN_FILE_ID,
    AL2.FILE_VERSION ORIGIN_FILE_VERSION,
    ROUND(AL2.FILE_SIZE/1024/1024,3) FILE_SIZE_MB,
    AL1.FILE_ID DEST_FILE_ID,
    AL1.FILE_VERSION DEST_FILE_VERSION,
    (TO_TIMESTAMP(SUBSTR(REPLACE(AL2.INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI')) ORIG_INGESTION,
    (TO_TIMESTAMP(SUBSTR(REPLACE(AL1.INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI')) DEST_INGESTION,
    NUMTODSINTERVAL((TO_DATE(SUBSTR(REPLACE(AL2.INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') -  TO_DATE(SUBSTR(REPLACE(AL1.INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI')),'DAY') TIME_DELTA,
    AL1.FILE_SIZE ORIGIN_FILE_SIZE,
    AL2.FILE_SIZE DEST_FILE_SIZE,
    AL1.CHECKSUM ORIGIN_CHECKSUM,
    AL2.CHECKSUM DEST_CHECKSUM,
    AL3.HOST_ID
FROM
    NGAS.NGAS_FILES AL1,
    NGAS.NGAS_FILES@ALMA.OSF.CL AL2,
    NGAS.NGAS_DISKS@ALMA.OSF.CL AL3
WHERE
    TO_DATE(SUBSTR(REPLACE(AL2.INGESTION_DATE,'T',' '),1,16),'YYYY-MM-DD HH24:MI') > SYSDATE-4
    AND AL3.HOST_ID LIKE '%ngobe%'
    AND AL2.DISK_ID = AL3.DISK_ID
    AND AL2.FILE_ID = AL1.FILE_ID(+)
    AND AL2.FILE_VERSION = AL1.FILE_VERSION(+)
    AND ((AL2.FILE_SIZE != AL1.FILE_SIZE) or (al2.checksum != al1.checksum))
ORDER BY 6 DESC ''')
        pgprint(cursor2.description,cursor2.fetchall())
        print ""
        print "##### Files in FE without copies in BE ####"
        cursorsco.execute('''
select count(fe.file_id) count_retained_files, round(sum(fe.file_size)/1024/1024/1024, 2) retained_size_GiB
  from
    (
      select d.host_id, file_id, file_version, file_size
        from ngasgg.ngas_disks d, ngasgg.ngas_files f
        where d.disk_id = f.disk_id and d.host_id like :fe
    ) fe
  left join
    (
  select d.host_id, file_id, file_version, file_size
      from ngasgg.ngas_disks d, ngasgg.ngas_files f
      where d.disk_id = f.disk_id and d.host_id like :be
    ) be
    on (fe.file_id = be.file_id and fe.file_size = be.file_size)
  where be.file_id is null and fe.file_id like 'A002%' ''',{'fe':'ngofe0%', 'be':'ngobe0%'})



        pgprint(cursorsco.description,cursorsco.fetchall())
####   Print PRTG DATA ###########
        print "PRTG Sensors Data:"
        for sensorId in [4710,4712,4703,4895,4896]:
                printSensorData(sensorId, prtguser,prtgpasswd)

	ssh.close()
