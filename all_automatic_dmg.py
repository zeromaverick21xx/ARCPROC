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
		call("echo 'Following tar has bad md5, ask arcs to resend: ' > md5error.txt", shell=True)
                call("echo '%s' >> md5error.txt "%(full_name), shell=True)
                #call("echo 'test' > cuerpo.txt", shell=True)
                call("mail -s 'FAILED MD5' bmalet@alma.cl <md5error.txt", shell=True)
                call("mail -s 'FAILED MD5' abarrien@alma.cl <md5error.txt", shell=True)
                call("mail -s 'FAILED MD5' ngonzale@alma.cl <md5error.txt", shell=True)
                call("mail -s 'FAILED MD5' darredon@alma.cl <md5error.txt", shell=True)
                sys.exit('Exiting due FAILED MD5')
		
	else:
		print ""
		print "___________________________________________________"
		print ""
		print "MD5 is correct - You can proceed with the ingestion"
		print "___________________________________________________"
		print ""
	return(checkchar)

def checkReadme(tar_file_path):
        print ""
        print "____________________________________________________________"
        print ""
        print "Checking README file in "+tar_file_path
        print "____________________________________________________________"
        print ""
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


def tarutil(full_name):
	print ""
	print "____________________________________________________________"
	print ""
	print "Checking README file in "+full_name
	print "____________________________________________________________"
	print ""
	proj_name=full_name[:14]
	call("/home/jao/bin/tarutil_zero.py '%s'"%proj_name, shell=True)
	output = subprocess.check_output("/home/jao/bin/tarutil_zero.py '%s'"%proj_name, shell=True)
	checkchartar=output[-2:-1]
	if checkchartar is '0':
		print ""
		print "____________"
		print ""	
		print "README is OK"
		print "____________"
		print
	else:
		print ""
		print "_____________________________________________________"
		print ""
		print "README file is NOT OK - Please ask ARCs to correct it"
		print "_____________________________________________________"
		print ""
                call("echo 'Following tar has bad readme, ask arcs to resend: ' > readmeerror.txt", shell=True)
                call("echo '%s' >> readmeerror.txt "%(full_name), shell=True)
                #call("echo 'test' > cuerpo.txt", shell=True)
                call("mail -s 'BAD README' bmalet@alma.cl <readmeerror.txt", shell=True)
                call("mail -s 'BAD README' abarrien@alma.cl <readmeerror.txt", shell=True)
                call("mail -s 'BAD README' ngonzale@alma.cl <readmeerror.txt", shell=True)
                call("mail -s 'BAD README' darredon@alma.cl <readmeerror.txt", shell=True)
                sys.exit('Exiting due BAD README')

	print ""
	
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
                call("echo 'Following tar has failed repacking, reingest manually: ' > packerror.txt", shell=True)
                call("echo '%s' >> packerror.txt "%(full_name), shell=True)
                #call("echo 'test' > cuerpo.txt", shell=True)
                call("mail -s 'REPACK ERROR' bmalet@alma.cl <packerror.txt", shell=True)
                call("mail -s 'REPACK ERROR' abarrien@alma.cl <packerror.txt", shell=True)
                call("mail -s 'REPACK ERROR' ngonzale@alma.cl <packerror.txt", shell=True)
                call("mail -s 'REPACK ERROR' darredon@alma.cl <packerror.txt", shell=True)
		sys.exit("Cycle 1 Tar script failed")
	else:
		return(old_check)

        old_value= subprocess.check_output("ls -lh *.tar | awk '{print $5}'", shell=True)
        if old_value == 0:
                call("echo 'Following tar has 0 filesize, reingest it manually: ' > tarerror.txt", shell=True)
                call("echo '%s' >> tarerror.txt "%(full_name), shell=True)
                #call("echo 'test' > cuerpo.txt", shell=True)
                call("mail -s 'FILESIZE 0' bmalet@alma.cl <tarerror.txt", shell=True)
                call("mail -s 'FILESIZE 0' abarrien@alma.cl <tarerror.txt", shell=True)
                call("mail -s 'FILESIZE 0' ngonzale@alma.cl <tarerror.txt", shell=True)
                call("mail -s 'FILESIZE 0' darredon@alma.cl <tarerror.txt", shell=True)
                sys.exit("Cycle 1 Tar script failed due filesize is 0")
        else:
                return(old_value)

def data_ingest(full_name):
        print ''
        print 'Checking size of file: '+full_name
        call("if [ -s '%s' ]; then echo 1 >temp_size.txt; else echo 0 > temp_size.txt; fi"%full_name, shell=True)
#	call("ls -l '%s' | awk '{print $5}' > temp_size.txt"%full_name, shell=True)
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
		call("echo 'Following tar has failed to ingest due file size 0, reingest it manually: ' > ingesterrorzero.txt", shell=True)
                call("echo '%s' >> ingesterrorzero.txt "%(full_name), shell=True)
                call("mail -s 'INGESTION FILE SIZE 0 ERROR' bmalet@alma.cl <ingesterrorzero.txt", shell=True)
                call("mail -s 'INGESTION FILE SIZE 0 ERROR' abarrien@alma.cl <ingesterrorzero.txt", shell=True)
                call("mail -s 'INGESTION FILE SIZE 0 ERROR' ngonzale@alma.cl <ingesterrorzero.txt", shell=True)
                call("mail -s 'INGESTION FILE SIZE 0 ERROR' darredon@alma.cl <ingesterrorzero.txt", shell=True)
                sys.exit()
        else:
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
			call("echo 'Following tar has failed to ingest, reingest it manually: ' > ingesterror.txt", shell=True)
			call("echo '%s' >> ingesterror.txt "%(full_name), shell=True)
			call("mail -s 'INGESTION ERROR' bmalet@alma.cl <ingesterror.txt", shell=True)
			call("mail -s 'INGESTION ERROR' abarrien@alma.cl <ingesterror.txt", shell=True)
			call("mail -s 'INGESTION ERROR' ngonzale@alma.cl <ingesterror.txt", shell=True)
			call("mail -s 'INGESTION ERROR' darredon@alma.cl <ingesterror.txt", shell=True)
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





#def data_ingest(full_name):
#	ngas_server=random.randrange(1,4,1)
#	ngas_port=random.randrange(77,80,1)
#        print ""
#        print "____________________________________________________________"
#        print ""
#        print "Starting ingestion of "+full_name
#        print "____________________________________________________________"
#        print ""

#	ngas_string='ngamsCClient -cmd ARCHIVE -timeOut 3600 -fileUri '+full_name+' -host ngas0'+str(ngas_server)+'.sco.alma.cl -port 77'+str(ngas_port)
	#call("'%s'"%ngas_string, shell=True) # remove echo for production version
#	args = shlex.split(ngas_string)
#	print args
#	pro = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
#	ret = pro.communicate()
#	print  ret[0]	
#	if 'FAILURE' in ret[0]:
#                call("echo 'Following tar has failed to ingest, reingest it manually: ' > ingesterror.txt", shell=True)
#                call("echo '%s' >> ingesterror.txt "%(full_name), shell=True)
#                #call("echo 'test' > cuerpo.txt", shell=True)
#                call("mail -s 'INGESTION ERROR' bmalet@alma.cl <ingesterror.txt", shell=True)
#                call("mail -s 'INGESTION ERROR' abarrien@alma.cl <ingesterror.txt", shell=True)
#                call("mail -s 'INGESTION ERROR' ngonzale@alma.cl <ingesterror.txt", shell=True)
#                call("mail -s 'INGESTION ERROR' darredon@alma.cl <ingesterror.txt", shell=True)
#		sys.exit('NGAS Failed to ingest')
#	else:
#		print ''
#		print '______________________________________________________________________________________'
#		print ''
#		print 'File '+full_name+' was ingested Correctly in host '+str(ngas_server)+' in port '+str(ngas_port)
#		print ''
#		print '______________________________________________________________________________________'
#		print ''


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
                print "               all_automatic.py <PROJECT_MOUSS_PARTS>.tar"
                print ""
		sys.exit()
	else:      
		delivery = sys.argv[1]

        print ''
        print '======================================================================='
        print 'PROCEED TO INGEST '+delivery
        print '======================================================================='
        print ''
        passwdngas = 'alma4dba'
	passwd = 'alma$dba' # PARA ESTA VERSION SE USA EL PASSWORD AUTOMATICO
	#passwd = getpass.getpass('Enter password for ALMA schema: ')
        print ''
        print 'Connecting to database . . .'
        #dsn = '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS = (PROTOCOL = TCP)(HOST = oraclsco1-vip.sco.alma.cl)(PORT = 1521))(ADDRESS = (PROTOCOL = TCP)(HOST = oraclsco2-vip.sco.alma.cl)(PORT = 1521)))(CONNECT_DATA=(SERVICE_NAME=ALMA.SCO.CL))(FAILOVER_MODE=(TYPE=SELECT)(METHOD=BASIC)))'
	ngas = cx_Oracle.connect('almasu', passwdngas, 'ALMA.SCO.CL')
	cursorngas = ngas.cursor()

        orcl = cx_Oracle.connect('alma', passwd, 'ALMA.SCO.CL')
        cursor = orcl.cursor()

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
			call("echo 'Following tar has to be ingested manually: ' > cuerpo.txt", shell=True)
			call("echo '%s' >> cuerpo.txt "%(full_name), shell=True)
			#call("echo 'test' > cuerpo.txt", shell=True)
			call("mail -s 'EXISTING DP_DELIVERY' bmalet@alma.cl <cuerpo.txt", shell=True)
                        call("mail -s 'EXISTING DP_DELIVERY' abarrien@alma.cl <cuerpo.txt", shell=True)
                        call("mail -s 'EXISTING DP_DELIVERY' ngonzale@alma.cl <cuerpo.txt", shell=True)
                        call("mail -s 'EXISTING DP_DELIVERY' darredon@alma.cl <cuerpo.txt", shell=True)
			sys.exit('Exiting due existing DP_DELIVERY_STATUS')
			#break
#ENDS VALIDATES UNIQUE DP_DELIVERY
	proceed='y'
	#proceed=raw_input("do you want to proceed with this DELIVERY and MOUSS? y/n : ")
        if proceed is not 'y':
                print ''
                sys.exit('Exiting')
        else:

                sql0='''select count (*) from ngas.ngas_files where file_id =\''''+full_name+'''\' '''
	#	print sql0
                cursorngas.execute(sql0)
                while 1:
                        row = cursorngas.fetchone()
                        if row[0] == 0:
	#			print row[0]
				print ''
				print "================="
                                print "This is a NEW tar"
				print "================="
				print ''
                        	break
			else:
	#			print row[0]
				print ''
				print "================================================================="
                                print "This is an EXISTING tar,this is a REINGESTION, so after ingestion"
				print ""
				print "You will need to get rid of the duplicates in DP_DELIVERY_STATUS "	
				print "================================================================="
				print ''
				call("echo 'Following tar has to be ingested manually: ' > reingest.txt", shell=True)
                        	call("echo '%s' >> reingest.txt "%(full_name), shell=True)
	                        #call("echo 'test' > cuerpo.txt", shell=True)
		                call("mail -s 'REINGESTION' bmalet@alma.cl <reingest.txt", shell=True)
				call("mail -s 'REINGESTION' abarrien@alma.cl <reingest.txt", shell=True)
				call("mail -s 'REINGESTION' darredon@alma.cl <reingest.txt", shell=True)
				call("mail -s 'REINGESTION' ngonzale@alma.cl <reingest.txt", shell=True)
				sys.exit('Exiting due Reingestion')
				#break
                print ''
        	apo = "NOT APPLICABLE"
	#       apo = raw_input("Enter the number of the APO Ingestion - i.e. 758 - : ")
	#	sys.exit('Exiting')
	
		print ''
		#md5sum(full_name)
	#	tarutil(full_name)
		if not checkReadme(full_name):
			print GLOBAL_ERROR
	                print ""
	                print "_____________________________________________________"
	                print ""
	                print "README file is NOT OK - Please ask ARCs to correct it"
	                print "_____________________________________________________"
	                print ""
	                call("echo 'Following tar has bad readme, ask arcs to resend:\n"+GLOBAL_ERROR+"' > readmeerror.txt", shell=True)
	                call("echo '%s' >> readmeerror.txt "%(full_name), shell=True)
	                call("mail -s 'BAD README' bmalet@alma.cl <readmeerror.txt", shell=True)
	                call("mail -s 'BAD README' abarrien@alma.cl <readmeerror.txt", shell=True)
	                call("mail -s 'BAD README' ngonzale@alma.cl <readmeerror.txt", shell=True)
	                call("mail -s 'BAD README' darredon@alma.cl <readmeerror.txt", shell=True)
	                sys.exit('Exiting due BAD README')
                print ""
                print "____________"
                print ""
                print "README is OK"
                print "____________"
                print ""
		cycle1Tar(full_name)
		data_ingest(full_name)

		f=open('query_for_'+full_name+'.sql','w')
		f.write("ALTER SESSION SET NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS';\n")
		
		if type is 'A':
		
			#sql1='''select e.obsprojectcode,a.preferredarc,s.PARENT_OBS_UNIT_SET_STATUS_ID, concat(e.obsprojectcode,concat('',replace(replace(replace(s.PARENT_OBS_UNIT_SET_STATUS_ID,'://','___'),'/','_'),'uid','_uid'))) DELIVERY_ID,e.execblockuid,e.qa0status,a.request_handler_id,sysdate+2/24,add_months( sysdate, 6 ) from alma.aqua_execblock e, alma.sched_block_status s, alma.mv_schedblock m, alma.account a, alma.mv_obsproposal p where e.SCHEDBLOCKUID=s.DOMAIN_ENTITY_ID and m.SB_ARCHIVE_UID=s.DOMAIN_ENTITY_ID and e.obsprojectcode=p.code and a.account_id=p.pi_userid AND (e.qa0status LIKE 'Pass%' or e.qa0status LIKE 'SemiPass%') and s.PARENT_OBS_UNIT_SET_STATUS_ID=\''''+mouss+'''\' '''
			sql1='''select se.se_project_code,a.preferredarc,s.PARENT_OBS_UNIT_SET_STATUS_ID, concat(se.se_project_code,concat('',replace(replace(replace(s.PARENT_OBS_UNIT_SET_STATUS_ID,'://','___'),'/','_'),'uid','_uid'))) DELIVERY_ID,se.SE_EB_UID,se.se_qa0flag,a.request_handler_id,sysdate+2/24,add_months( sysdate, 6 ) from alma.shiftlog_entries se, alma.sched_block_status s, alma.mv_schedblock m, alma.account a, alma.mv_obsproposal p where se.se_sb_id=s.DOMAIN_ENTITY_ID and m.SB_ARCHIVE_UID=s.DOMAIN_ENTITY_ID and se.se_project_code=p.code and a.account_id=p.pi_userid AND (se.se_qa0flag LIKE 'Pass%' or se.se_qa0flag LIKE 'SemiPass%') and s.PARENT_OBS_UNIT_SET_STATUS_ID=\''''+mouss+'''\' '''
		else:
			

                       # sql1='''select e.obsprojectcode,a.preferredarc,s.PARENT_OBS_UNIT_SET_STATUS_ID, concat(e.obsprojectcode,concat('',replace(replace(replace(s.PARENT_OBS_UNIT_SET_STATUS_ID,'://','___'),'/','_'),'uid','_uid'))) DELIVERY_ID,e.execblockuid,e.qa0status,a.request_handler_id,sysdate+2/24,add_months( sysdate, 12 ) from alma.aqua_execblock e, alma.sched_block_status s, alma.mv_schedblock m, alma.account a, alma.mv_obsproposal p where e.SCHEDBLOCKUID=s.DOMAIN_ENTITY_ID and m.SB_ARCHIVE_UID=s.DOMAIN_ENTITY_ID and e.obsprojectcode=p.code and a.account_id=p.pi_userid AND (e.qa0status LIKE 'Pass%' or e.qa0status LIKE 'SemiPass%') and s.PARENT_OBS_UNIT_SET_STATUS_ID=\''''+mouss+'''\' '''
			sql1='''select se.se_project_code,a.preferredarc,s.PARENT_OBS_UNIT_SET_STATUS_ID, concat(se.se_project_code,concat('',replace(replace(replace(s.PARENT_OBS_UNIT_SET_STATUS_ID,'://','___'),'/','_'),'uid','_uid'))) DELIVERY_ID,se.SE_EB_UID,se.se_qa0flag,a.request_handler_id,sysdate+2/24,add_months( sysdate, 12 ) from alma.shiftlog_entries se, alma.sched_block_status s, alma.mv_schedblock m, alma.account a, alma.mv_obsproposal p where se.se_sb_id=s.DOMAIN_ENTITY_ID and m.SB_ARCHIVE_UID=s.DOMAIN_ENTITY_ID and se.se_project_code=p.code and a.account_id=p.pi_userid AND (se.se_qa0flag LIKE 'Pass%' or se.se_qa0flag LIKE 'SemiPass%') and s.PARENT_OBS_UNIT_SET_STATUS_ID=\''''+mouss+'''\' '''

                #NEW CODE

                cursor.execute(sql1)
                row = cursor.fetchone()
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


#END OF NEW CODE

























#OLD CODE
#

		#print sql1 # test
#		cursor.execute(sql1)
 #       	while 1:
#	       	       	row = cursor.fetchone()
 #       	       	if row == None:
  #      	       	        break
   #     	       	else:
    #    	       	        obs_proj_code = row[0]
     #         		        pref_arc = row[1]
#				parent_obs_unit_set = row[2]
#				delivery_id = row[3]
#				exec_block = row[4]
#				qa0_status = row[5]
#				request_handler = row[6]
#                      		sysdate_2 = row[7]
#				sysdate_year = row[8]
#				print ""			
#				f.write("insert into alma.dp_delivery_asdm_ous (asdm_uid,deliverable_name,id) values ('"+str(exec_block)+"','"+delivery+"', asa_sequence.nextval);\n")
#				print '________________________________________________________________________'
#				print ''
#				print 'DP_DELIVERY_ASDM_OUS insertion query for '+str(exec_block)+' created'
#				print '________________________________________________________________________'
#				print ''
#				print 'Datapacker for '+str(exec_block)+' started'
#				print '______________________________________________'
#				print ''
#				variable=str(exec_block)
#				call("/datapacker/DataPacker/scripts/asdmSize '%s'"%variable, shell=True)
			

#		print ''
#		f.write("insert into alma.dp_delivery_status (id, delivery_id, pi_account_id, qa2_passed, notification_date, original_release_date, release_date, release_date_comment) values (asa_sequence.nextval,'"+delivery+"','"+str(request_handler)+"','Y','"+str(sysdate_2)+"','"+str(sysdate_year)+"','"+str(sysdate_year)+"','Ingestion: APO-"+apo+"');\n")
#		f.write("insert into alma.dp_delivery_status (id, delivery_id, pi_account_id, qa2_passed, release_date, release_date_comment) values (asa_sequence.nextval,'"+delivery+"','"+str(request_handler)+"','Y','"+str(sysdate_year)+"','Ingestion: APO-"+apo+"');\n")



#		f.write("commit;\n")
#		f.write("exit\n")
#		print '_____________________________________________________________________________________'
#		print ''
#		print 'DP_DELIVERY_STATUS insertion query for '+delivery+' created'
#		print '_____________________________________________________________________________________'
#		print ''
#		passwd_os=passwd.replace('$','\$')
#		g=open('script_'+full_name+'.sh','w')
#		script_query='script_'+full_name+'.sh'
#BEFORE		#g.write("sqlplus alma/"+passwd_os+"@'(DESCRIPTION =(ADDRESS = (PROTOCOL = TCP)(HOST = oracl1-vip.osf.alma.cl)(PORT = 1521))(CONNECT_DATA =(SERVER = DEDICATED)(SID = ALMA1)))' @query_for_"+full_name+".sql\n")
#		g.write("sqlplus alma/"+passwd_os+"@'ALMA_OFFLINE.SCO.CL' @query_for_"+full_name+".sql\n")
#
#		f.close()
#		g.close()

#		call("sh '%s'"%script_query, shell=True)
#END OF OLD CODE

		proj_number=full_name[7:12]
		f = open('exitoso.txt', 'w')
		f.write('\n')
		f.write('\n')
		f.write('===========\n')
		f.write('NEXT STEPS\n')
		f.write('===========\n')
		f.write('\n')
		f.write('Update wiki - https://adcwiki.alma.cl/bin/view/APO/APOIngestedProjects - with following code between lines\n')
		f.write('\n')
		f.write('__________________________________________________________________________________________________________\n')
		f.write('\n')
		#f.write('*DELIVERY <FILL WITH NUMBER>* ',datetime.datetime.now().strftime("%Y-%m-%d")
		datenow=datetime.datetime.now().strftime("%Y-%m-%d")
		f.write('*DELIVERY <FILL WITH NUMBER>* '+datenow)
		f.write('\n')
		f.write('\n')
		f.write('[[http://jira.alma.cl/browse/APO-'+apo+'][JIRA APO-'+apo+' Project '+proj_number+']]\n')
		f.write('\n')
		f.write( '| *FILE NAME* | *SCO* | *NA* | *EU* | *EA* |\n')
		f.write( '| '+full_name+' | <strong><font color="darkgreen">OK</font></strong>  |  |   |   |\n')
		f.write('\n')
                f.write('__________________________________________________________________________________________________________\n')
		f.write('\n')
		f.write('To check the status of the mirroring use following queries:\n')
		f.write('\n')
		f.write("select * from ngas.ngas_files where file_id='"+full_name+"';")
		f.write('\n')
                f.write("select * from ngas.ngas_files@ALMA.ARC.NA where file_id='"+full_name+"';")
		f.write('\n')
                f.write("select * from ngas.ngas_files@ALMA.ARC.EU where file_id='"+full_name+"';")
		f.write('\n')
                f.write("select * from ngas.ngas_files@ALMA.ARC.EA where file_id='"+full_name+"';")
		f.write('\n')
		f.write("select * from alma.dp_delivery_status where delivery_id like '"+delivery+"%';")
		f.write('\n')
		f.close()
		call("mail -s 'SUCCESSFULLY INGESTED' bmalet@alma.cl <exitoso.txt", shell=True)
                call("mail -s 'SUCCESSFULLY INGESTED' abarrien@alma.cl <exitoso.txt", shell=True)
                call("mail -s 'SUCCESSFULLY INGESTED' ngonzale@alma.cl <exitoso.txt", shell=True)
		call("mail -s 'SUCCESSFULLY INGESTED' darredon@alma.cl <exitoso.txt", shell=True)
                call("mail -s 'SUCCESSFULLY INGESTED' gallardo@alma.cl <exitoso.txt", shell=True)
                call("mail -s 'SUCCESSFULLY INGESTED' hfrancke@alma.cl <exitoso.txt", shell=True)
		call("mail -s 'SUCCESSFULLY INGESTED' sagonzal@alma.cl <exitoso.txt", shell=True)

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

#BEFORE	#	print 'IMPORTANT - WHEN ARRIVED INTO ARCS RUN FOLLOWING STEPS'
	#	print '__________________________________________________________________________________________________________'
	#	print ''
        #       print 'Please review the file  - query_for_'+full_name+'.sql - and run the following command replacing XXXX for the ALMA schema password:'
        #       print ''
        #       print "sqlplus alma@'(DESCRIPTION =(ADDRESS = (PROTOCOL = TCP)(HOST = oracl1-vip.osf.alma.cl)(PORT = 1521))(CONNECT_DATA =(SERVER = DEDICATED)(SID = ALMA1)))' @query_for_"+full_name+".sql"
#BEFORE #       print ''

