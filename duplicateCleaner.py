#!/usr/bin/env python2.7
import cx_Oracle
import getpass
import paramiko
from subprocess import call


ngasdbpasswd = getpass.getpass('Enter password for ngas db: ')
dsn2 = ''' (DESCRIPTION_LIST =
    (FAILOVER = TRUE)
    (LOAD_BALANCE = FALSE)
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = ora.sco.alma.cl)(PORT = 1521))
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
orcl = cx_Oracle.connect('ngas', ngasdbpasswd, dsn2)
cursorsco = orcl.cursor()
cursorsco.execute('''select  'ngamsCClient -cmd DISCARD -host ' || substr(c.host_id, 0,
instr(c.host_id, ':') - 1) || ' -port ' || substr(c.host_id,
instr(c.host_id, ':') + 1) || ' -diskId ' || a.disk_id || ' -fileId ' ||
a.file_id || ' -fileVersion ' || a.file_version || ' -execute' as
DELETECOMMAND 
FROM ngas.ngas_files a, ngas.ngas_disks c where a.disk_id = c.disk_id and a.ROWID IN
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

for cmd  in cursorsco.fetchall():
	print cmd[0]
	#call([str(cmd[0])])

