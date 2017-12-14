#!/usr/bin/env python2.7

# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2012 Nicolas Gonzalez <hyperion@Neptune>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#        /\/\  
#       ( 00 ) Hyperion 2013
#       /  ¯ \ 
#     (((/  \)))
#     

import sys
import os
import base64
import urllib2
import cx_Oracle


class db_handler:
    '''
    This class gets methods for basics queries in a databases
    '''
    
    def __init__(self, **params):
        
        self.params = params
        self.ERR_ORA_CONN_MSJ = ''
        self.RES = None
    
    
    def query(self, query):
        
        try:
            CONN = cx_Oracle.connect(self.params['username'], self.params['passwd'], self.params['connstr'])
        except cx_Oracle.Error, e:
            self.ERR_ORA_CONN_MSJ = "ERROR [ %s ] in data base connection" % e
            return False
        
        CUR = CONN.cursor()
        
        try:
            CUR.execute(query)
        except cx_Oracle.Error, e:
            self.ERR_ORA_CONN_MSJ = "ERROR [ %s ] in query execution" % e
            return False
            
        self.RES = CUR.fetchall()
        CUR.close()
        CONN.close()
        
        return True
        
    
    def resulset(self):
        
        return self.RES
    
    
    def error(self):
        
        return self.ERR_ORA_CONN_MSJ
        
        
def main():
    
    input_name = raw_input('Project code: ')
    
    dsn2 = '''(DESCRIPTION_LIST=
    (LOAD_BALANCE=off)(FAILOVER=on)
    (DESCRIPTION=
      (LOAD_BALANCE=on)
      (ADDRESS_LIST=
        (ADDRESS = (PROTOCOL = TCP)(HOST = oraclsco1-vip.sco.alma.cl)(PORT = 1521))
        (ADDRESS = (PROTOCOL = TCP)(HOST = oraclsco2-vip.sco.alma.cl)(PORT = 1521)))
    (CONNECT_DATA=(SERVICE_NAME=ALMA.SCO.CL))))'''
    
    url = 'http://%s.sco.alma.cl:%s/RETRIEVE?file_id=%s'

    q0 = '''SELECT ngas_disks.host_id, ngas_files.file_id FROM NGAS.ngas_files, NGAS.ngas_disks 
         WHERE ngas.ngas_files.file_id like '%s%%' 
         and ngas.ngas_disks.disk_id = ngas.ngas_files.disk_id 
         ORDER BY ngas.ngas_files.file_id''' % input_name.strip()
    
    user = 'almasu'
    passwd = 'YWxtYTRkYmE='#!!
    
    db = db_handler(username = user, passwd = base64.b64decode(passwd), connstr = dsn2)# !!
    rset = None
    if db.query(q0):
        rset = db.resulset()
        print 'The query was running successfully'
    else:
        sys.exit(db.error())
    
    if not rset:
        sys.exit('No values were returned')
    
    try:
        for file_info in rset:
            host, port = file_info[0].split(':')
            file_name = file_info[1]
            url_file = url % (host, port, file_name)
            u = urllib2.urlopen(url_file)
            meta = u.info()
            file_size = float(meta.getheaders("Content-Length")[0])
            print 'Downloading %s file size %f GB' % (file_name, file_size/1024**3)
            f = open(file_name, 'wb')
            file_size_dl = 0
            block_sz = 8192
            while True:
                buff = u.read(block_sz)
                if not buff:
                    break
                file_size_dl += len(buff)
                f.write(buff)
                sys.stdout.write("\r%d%% " % (int(file_size_dl/file_size * 100)))
                sys.stdout.flush()
            if file_size_dl != file_size:
                print 'Error in file: ' + file_name 
            else:    
                print 'Done'
            f.close()
    except Exception, e:
        print 'Error [%s]' % e[0]
    return 0



if __name__ == '__main__':
    main()

