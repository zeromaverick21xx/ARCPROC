#!/usr/bin/env python2.7

import cx_Oracle
import getpass
import paramiko
from subprocess import call


#ngasdbpasswd = getpass.getpass('Enter password for ngas db: ')
dsn2 = ''' (DESCRIPTION_LIST =
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
      (ADDRESS = (PROTOCOL = TCP)(HOST = orastbsco1.sco.alma.cl)(PORT = 1521))
      (CONNECT_DATA =
        (SERVER = DEDICATED)
        (SERVICE_NAME = OFFLINE.OSF.CL)
      )
    )
  )'''
orcl = cx_Oracle.connect('ngas', "ngas$dba", dsn2)
cursorsco = orcl.cursor()
cursorsco.execute('''select

substr(last_host_id, 0, instr(last_host_id, ':') - 1) || '.osf.alma.cl', 

substr(last_host_id, instr(last_host_id, ':') + 1),

f.disk_id,f.file_id,f.file_version as DELETECOMMAND from ngas.ngas_files f

inner join ngas.ngas_disks d on d.disk_id = f.disk_id where file_id like 'Z00%' ''')

for cmd  in cursorsco.fetchall():
	print cmd
	call(["/opt/ngams/bin/ngamsCClient","-cmd","DISCARD","-host",str(cmd[0]),"-port",str(cmd[1]),"-diskId",str(cmd[2]),"-fileId",str(cmd[3]),"-fileVersion",str(cmd[4]),"-execute"])

