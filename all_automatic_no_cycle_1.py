#!/usr/bin/env python2.7
# Developed in 2014-02-07
# By Bernardo Malet

# Changelog
# Now it diferentiate between S and A projects
# 2015-10-22 works with changes in the database DP_DELIVERY tables 
# 2015-10-24 validates if the tar is 0 before ingesting

import cx_Oracle
import getpass
import sys
import os
import subprocess
from subprocess import Popen, PIPE, call
import random
import shlex
import time
import datetime
import tarfile
import re
import string

GLOBAL_ERROR = None

def md5sum(full_name):
    print ''
    print 'Checking MD5 of file: '+full_name
    full_name_md5_arc=full_name+'.md5sum'
    full_name_md5_jao=full_name+'.md5sum.jao'
    call("md5sum '%s' > %s "%(full_name,full_name_md5_jao), shell=True)
    call("cat '%s' | awk '{ print $1 }' > temporal0"%full_name_md5_arc, shell=True)
    call("cat '%s' | awk '{ print $1 }' > temporal1"%full_name_md5_jao, shell=True)
    output = subprocess.check_output("diff temporal0 temporal1; echo $?", shell=True)
    checkchar=output[-2:-1]
    call("rm -rf temporal0 temporal1", shell=True)
    print ""
    if checkchar is not '0':
        print ""
        print "______________________________________________________"
        print ""
        print "MD5 is incorrect - Please ask ARCs to resend the files"
        print "______________________________________________________"
        print ""
        sys.exit()
    else:
        print ""
        print "___________________________________________________"
        print ""
        print "MD5 is correct - You can proceed with the ingestion"
        print "___________________________________________________"
        print ""
    return(checkchar)


def checkReadme(tar_file_path):
   
    global GLOBAL_ERROR
    readme_path = None
    files_names_tar = []
    files_names_readme = []
    with tarfile.open(tar_file_path, 'r') as tar:
        for f in tar.getnames():
            if 'README' in f:
                readme_path = f
            #files_names_tar.append(f.split('/'))
            files_names_tar += f.split('/')
    set_names_tar = set(files_names_tar)
    if not readme_path:
        GLOBAL_ERROR ='README file is not in tar file - Please ask ARCs to resend the files'
        return False
    with tarfile.open(tar_file_path, 'r') as tar:
        tar.extract(readme_path)
    with open(readme_path, 'r') as f:
        all_lines = f.readlines()
    m = re.compile('.*(\d{4}\.([1-9]|A)\.\d{5}\.(S|T|L|V)).*')        
    #m = re.compile('.*(\d{4}\.([1-9]|A)\.\d{5}\.S).*')
    me = re.compile('^\d* directories, \d* files') #Extra! last line in tree command 
    for l in reversed(all_lines):
        e = me.match(l)
        if e:
            continue
        ascii_char = filter(lambda x: x in string.printable, l) #Remove non ASCII characters
        new_line =  re.sub('\s+|\||`|-{2}|/$|\n', '', ascii_char)
        if new_line == '':
            continue
        files_names_readme.append(new_line)
        g = m.match(l)
        if g:
            break
    set_names_readme = set(files_names_readme) 
    try:
        os.remove(readme_path)
        os.removedirs(os.path.dirname(readme_path))
    except OSError, e:
        GLOBAL_ERROR = e.args[1]
        return False    
    if not files_names_readme:
        GLOBAL_ERROR = 'README file has not directory tree or wrong character format - Please ask ARCs to resend the files'
        return False   
    not_found = list(set_names_readme - set_names_tar)
    if not_found:
        GLOBAL_ERROR = 'The following files and/or directories are not present in tar file:\n ' + '\n'.join(not_found)
        with open('diff.out', 'w') as fd:
            fd.writelines('\n'.join(not_found))
        return False 
    return True


def cycle1Tar(full_name):
    print ""
    print "____________________________________________________________"
    print ""
    print "Starting repacking for "+full_name
    print "____________________________________________________________"
    print ""
    call("/home/jao/bin/cycle1Tar.py '%s'"%full_name, shell=True)
    old_check = subprocess.check_output("ls | grep .old", shell=True)
    if old_check is None:
        sys.exit("Cycle 1 Tar script failed")
    else:
        return(old_check)
        old_value= subprocess.check_output("ls -lh *.tar | awk '{print $5}'", shell=True)
        if old_value == 0:
            sys.exit("Cycle 1 Tar script failed due filesize is 0")
        else:
            return(old_value)


def data_ingest(full_name):
    print ''
    print 'Checking size of file: '+full_name
    call("if [ -s '%s' ]; then echo 1 >temp_size.txt; else echo 0 > temp_size.txt; fi"%full_name, shell=True)   
    #call("ls -l '%s' | awk '{print $5}' > temp_size.txt"%full_name, shell=True)
    output = subprocess.check_output("cat temp_size.txt", shell=True)
    checkchar=output[:-1]
    print checkchar
    call("rm -rf temp_size.txt", shell=True)
    print ""
    if checkchar is '0':
        print ""
        print "____________________________________________________"
        print ""
        print "File Size is 0 - Please ask ARCs to resend the files"
        print "____________________________________________________"
        print ""
        sys.exit()
    print ""
    print "_______________________________________________________"
    print ""
    print "File Size is not 0 - You can proceed with the ingestion"
    print "_______________________________________________________"
    print ""
    ngas_server=random.randrange(1,4,1)
    ngas_port=random.randrange(77,80,1)
    print ""
    print "____________________________________________________________"
    print ""
    print "Starting ingestion of "+full_name
    print "____________________________________________________________"
    print ""
    ngas_string='ngamsCClient -cmd ARCHIVE -timeOut 3600 -fileUri '+full_name+' -host ngas0'+str(ngas_server)+'.sco.alma.cl -port 77'+str(ngas_port)
    #call("'%s'"%ngas_string, shell=True) # remove echo for production version
    args = shlex.split(ngas_string)
    print args
    pro = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
    ret = pro.communicate()
    print  ret[0]
    if 'FAILURE' in ret[0]:
        sys.exit('NGAS Failed to ingest')
    else:
        print ''
        print '______________________________________________________________________________________'
        print ''
        print 'File '+full_name+' was ingested Correctly in host '+str(ngas_server)+' in port '+str(ngas_port)
        print ''
        print '______________________________________________________________________________________'
        print ''
    return(checkchar)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ""
        print "===================================="
        print "                USAGE               "
        print "===================================="
        print ""
        print "1) make a <DIRECTORY>"
        print ""
        print "2) copy <PROJECT_MOUSS_PARTS>.tar and <PROJECT_MOUSS_PARTS>.tar.md5sum into <DIRECTORY>"
        print ""
        print "3) move into <DIRECTORY> and run following command:"
        print ""
        print "   all_automatic.py <PROJECT_MOUSS_PARTS>.tar"
        print ""
        sys.exit()    
    delivery = sys.argv[1]
    print ''
    print '======================================================================='
    print 'PROCEED TO INGEST '+delivery
    print '======================================================================='
    print ''
    passwdngas = 'alma4dba'
    passwd = getpass.getpass('Enter password for ALMA schema: ')
    print ''
    print 'Connecting to database . . .'
    #dsn = '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS = (PROTOCOL = TCP)(HOST = oraclsco1-vip.sco.alma.cl)(PORT = 1521))(ADDRESS = (PROTOCOL = TCP)(HOST = oraclsco2-vip.sco.alma.cl)(PORT = 1521)))(CONNECT_DATA=(SERVICE_NAME=ALMA.SCO.CL))(FAILOVER_MODE=(TYPE=SELECT)(METHOD=BASIC)))'
    ngas = cx_Oracle.connect('almasu', passwdngas, 'ALMA.SCO.CL')
    cursorngas = ngas.cursor()
    orcl = cx_Oracle.connect('alma', passwd, 'ALMA.SCO.CL')
    cursor = orcl.cursor()
    dp = cx_Oracle.connect('alma',passwd, 'ALMA.SCO.CL')
    cursordp = dp.cursor()
    full_name = delivery
    delivery = delivery[:-15]
    type=delivery[5]    
    mouss_pre = delivery[15:]
    mouss_temp = mouss_pre.replace('uid___','uid://')
    mouss = mouss_temp.replace('_','/')
    print ''
    print '_________________________________________________________'
    print ''
    print 'DELIVERY = '+delivery
    print ''
    print 'MOUSS = '+mouss
    print ''
    print 'TYPE = '+type
    print '_________________________________________________________'
    print ''
    #VALIDATES UNIQUE DP_DELIVERY
    sqlfinal='''select count (*) from alma.dp_delivery_status where delivery_id like \''''+delivery+'''%\' '''
    #print sqlfinal
    cursorngas.execute(sqlfinal)
    while 1:
        row = cursorngas.fetchone()
        if row[0] == 0:
            #print row[0]
            break
        else:
            #print row[0]
            print ''
            print '==========================================================='
            print 'WARNING - THIS TAR HAS ALREADY A FILE IN DP_DELIVERY_STATUS'
            print '==========================================================='
            print ''
        break
    #ENDS VALIDATES UNIQUE DP_DELIVERY
    proceed=raw_input("do you want to proceed with this DELIVERY and MOUSS? y/n : ")
    if proceed is not 'y':
        print ''
        sys.exit('Exiting')
    sql0='''select count (*) from ngas.ngas_files where file_id =\''''+full_name+'''\' '''
#   print sql0
    cursorngas.execute(sql0)
    while 1:
        row = cursorngas.fetchone()
        if row[0] == 0:
    #       print row[0]
            print ''
            print "================="
            print "This is a NEW tar"
            print "================="
            print ''
            break
        else:
#           print row[0]
            print ''
            print "================================================================="
            print "This is an EXISTING tar,this is a REINGESTION, so after ingestion"
            print ""
            print "You will need to get rid of the duplicates in DP_DELIVERY_STATUS "   
            print "================================================================="
            print ''
            break
    print ''
    apo = raw_input("Enter the number of the APO Ingestion - i.e. 758 - : ")
    #   sys.exit('Exiting')
    print ''
    md5sum(full_name)
    if not checkReadme(full_name):
        print GLOBAL_ERROR
        sys.exit()
    #cycle1Tar(full_name)
    data_ingest(full_name)
    f=open('query_for_'+full_name+'.sql','w')
    f.write("ALTER SESSION SET NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS';\n")
    if type is 'A':
        #sql1='''select e.obsprojectcode,a.preferredarc,s.PARENT_OBS_UNIT_SET_STATUS_ID, concat(e.obsprojectcode,concat('',replace(replace(replace(s.PARENT_OBS_UNIT_SET_STATUS_ID,'://','___'),'/','_'),'uid','_uid'))) DELIVERY_ID,e.execblockuid,e.qa0status,a.request_handler_id,sysdate+2/24,add_months( sysdate, 6 ) from alma.aqua_execblock e, alma.sched_block_status s, alma.mv_schedblock m, alma.account a, alma.mv_obsproposal p where e.SCHEDBLOCKUID=s.DOMAIN_ENTITY_ID and m.SB_ARCHIVE_UID=s.DOMAIN_ENTITY_ID and e.obsprojectcode=p.code and a.account_id=p.pi_userid AND (e.qa0status LIKE 'Pass%' or e.qa0status LIKE 'SemiPass%') and s.PARENT_OBS_UNIT_SET_STATUS_ID=\''''+mouss+'''\' '''
        sql1='''select se.se_project_code,a.preferredarc,s.PARENT_OBS_UNIT_SET_STATUS_ID, concat(se.se_project_code,concat('',replace(replace(replace(s.PARENT_OBS_UNIT_SET_STATUS_ID,'://','___'),'/','_'),'uid','_uid'))) DELIVERY_ID,se.SE_EB_UID,se.se_qa0flag,a.request_handler_id,sysdate+2/24,add_months( sysdate, 6 ) from alma.shiftlog_entries se, alma.sched_block_status s, alma.mv_schedblock m, alma.account a, alma.mv_obsproposal p where se.se_sb_id=s.DOMAIN_ENTITY_ID and m.SB_ARCHIVE_UID=s.DOMAIN_ENTITY_ID and se.se_project_code=p.code and a.account_id=p.pi_userid AND (se.se_qa0flag LIKE 'Pass%' or se.se_qa0flag LIKE 'SemiPass%') and s.PARENT_OBS_UNIT_SET_STATUS_ID=\''''+mouss+'''\' '''
    else:
        # sql1='''select e.obsprojectcode,a.preferredarc,s.PARENT_OBS_UNIT_SET_STATUS_ID, concat(e.obsprojectcode,concat('',replace(replace(replace(s.PARENT_OBS_UNIT_SET_STATUS_ID,'://','___'),'/','_'),'uid','_uid'))) DELIVERY_ID,e.execblockuid,e.qa0status,a.request_handler_id,sysdate+2/24,add_months( sysdate, 12 ) from alma.aqua_execblock e, alma.sched_block_status s, alma.mv_schedblock m, alma.account a, alma.mv_obsproposal p where e.SCHEDBLOCKUID=s.DOMAIN_ENTITY_ID and m.SB_ARCHIVE_UID=s.DOMAIN_ENTITY_ID and e.obsprojectcode=p.code and a.account_id=p.pi_userid AND (e.qa0status LIKE 'Pass%' or e.qa0status LIKE 'SemiPass%') and s.PARENT_OBS_UNIT_SET_STATUS_ID=\''''+mouss+'''\' '''
        sql1='''select se.se_project_code,a.preferredarc,s.PARENT_OBS_UNIT_SET_STATUS_ID, concat(se.se_project_code,concat('',replace(replace(replace(s.PARENT_OBS_UNIT_SET_STATUS_ID,'://','___'),'/','_'),'uid','_uid'))) DELIVERY_ID,se.SE_EB_UID,se.se_qa0flag,a.request_handler_id,sysdate+2/24,add_months( sysdate, 12 ) from alma.shiftlog_entries se, alma.sched_block_status s, alma.mv_schedblock m, alma.account a, alma.mv_obsproposal p where se.se_sb_id=s.DOMAIN_ENTITY_ID and m.SB_ARCHIVE_UID=s.DOMAIN_ENTITY_ID and se.se_project_code=p.code and a.account_id=p.pi_userid AND (se.se_qa0flag LIKE 'Pass%' or se.se_qa0flag LIKE 'SemiPass%') and s.PARENT_OBS_UNIT_SET_STATUS_ID=\''''+mouss+'''\' '''
        #print sql1 # test
    cursordp.execute(sql1)
    row = cursordp.fetchone()
    obs_proj_code = row[0]
    pref_arc = row[1]
    parent_obs_unit_set = row[2]
    delivery_id = row[3]
    exec_block = row[4]
    qa0_status = row[5]
    request_handler = row[6]
    sysdate_2 = row[7]
    sysdate_year = row[8]
    print ''
    f.write("insert into alma.dp_delivery_status (id, delivery_name, pi_account_id, qa2_passed, release_date, release_date_comment)values (asa_sequence.nextval,'"+delivery+"','"+str(request_handler)+"','Y','"+str(sysdate_year)+"','Ingestion: APO-"+apo+"');\n")
    print '_____________________________________________________________________________________'
    print ''
    print 'DP_DELIVERY_STATUS insertion query for '+delivery+' created'
    print '_____________________________________________________________________________________'
    print ''
    cursor.execute(sql1)
    while 1:
        row = cursor.fetchone()
        if row == None:
            break
        else:
            obs_proj_code = row[0]
            pref_arc = row[1]
            parent_obs_unit_set = row[2]
            delivery_id = row[3]
            exec_block = row[4]
            qa0_status = row[5]
            request_handler = row[6]
            sysdate_2 = row[7]
            sysdate_year = row[8]
            print ""            
            f.write("insert into alma.dp_delivery_asdm_ous (asdm_uid,deliverable_name,id, delivery_id) values ('"+str(exec_block)+"','"+delivery+"', asa_sequence.nextval,(select id from alma.dp_delivery_status where delivery_id='"+delivery+"'));\n")
            print '________________________________________________________________________'
            print ''
            print 'DP_DELIVERY_ASDM_OUS insertion query for '+str(exec_block)+' created'
            print '________________________________________________________________________'
            print ''
            print 'Datapacker for '+str(exec_block)+' started'
            print '______________________________________________'
            print ''
            variable=str(exec_block)
            call("/datapacker/DataPacker/scripts/asdmSize -i '%s'"%variable, shell=True)
    f.write("commit;\n")
    f.write("exit\n")
    passwd_os=passwd.replace('$','\$')
    g=open('script_'+full_name+'.sh','w')
    script_query='script_'+full_name+'.sh'
    g.write("sqlplus alma/"+passwd_os+"@'ALMA_OFFLINE.SCO.CL' @query_for_"+full_name+".sql\n")
    f.close()
    g.close()
    call("sh '%s'"%script_query, shell=True)
    proj_number=full_name[7:12]
    print ''
    print ''
    print '==========='
    print 'NEXT STEPS'
    print '==========='
    print ''
    print 'Update wiki - https://adcwiki.alma.cl/bin/view/APO/APOIngestedProjects - with following code between lines'
    print ''
    print '__________________________________________________________________________________________________________'
    print ''
    print '*DELIVERY <FILL WITH NUMBER>* ',datetime.datetime.now().strftime("%Y-%m-%d")
    print ''
    print '[[http://jira.alma.cl/browse/APO-'+apo+'][JIRA APO-'+apo+' Project '+proj_number+']]'
    print''
    print '| *FILE NAME* | *SCO* | *NA* | *EU* | *EA* |'
    print '| '+full_name+' | <strong><font color="darkgreen">OK</font></strong>  |  |   |   |'
    print ''
    print '__________________________________________________________________________________________________________'
    print ''
    print 'To check the status of the mirroring use following queries:'
    print ''
    print "select * from ngas.ngas_files where file_id='"+full_name+"';"
    print "select * from ngas.ngas_files@ALMA.ARC.NA where file_id='"+full_name+"';"
    print "select * from ngas.ngas_files@ALMA.ARC.EU where file_id='"+full_name+"';"
    print "select * from ngas.ngas_files@ALMA.ARC.EA where file_id='"+full_name+"';"
    print "select * from alma.dp_delivery_status where delivery_id like '"+delivery+"%';"
    # Extra code for validation
    sqlfinal2='''select count (*) from alma.dp_delivery_status where delivery_id like \''''+delivery+'''%\' '''
    #print sqlfinal2
    cursorngas.execute(sqlfinal2)
    while 1:
        row = cursorngas.fetchone()
        if row[0] == 1:
            #print row[0]
            break
        else:
            #print row[0]
            print ''
            print '========================================================================'
            print 'WARNING - DP_DELIVERY_STATUS HAS DUPLICATED VALUES, DELETE THEM MANUALLY'
            print '========================================================================'
            print ''
            break
#BEFORE #   print 'IMPORTANT - WHEN ARRIVED INTO ARCS RUN FOLLOWING STEPS'
    #   print '__________________________________________________________________________________________________________'
    #   print ''
        #       print 'Please review the file  - query_for_'+full_name+'.sql - and run the following command replacing XXXX for the ALMA schema password:'
        #       print ''
        #       print "sqlplus alma@'(DESCRIPTION =(ADDRESS = (PROTOCOL = TCP)(HOST = oracl1-vip.osf.alma.cl)(PORT = 1521))(CONNECT_DATA =(SERVER = DEDICATED)(SID = ALMA1)))' @query_for_"+full_name+".sql"
#BEFORE #       print ''

