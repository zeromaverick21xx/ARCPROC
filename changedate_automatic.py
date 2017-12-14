#!/usr/bin/env python2.7
# Developed in 2014-03-31
# By Bernardo Malet

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
from time import mktime, strptime
from datetime import datetime

def validate_date(new_date):
	result = None
	validation = 0
	for format in ['%Y-%m-%d']:
		try:
			result = datetime.strptime(new_date, format)
		except:
			pass
	if result is None:
		sys.exit('Date is not correct')
	else:
		validation=1
		print 'Date is fine'
	return(validation)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print ""
                print "===================================="
		print "                USAGE               "
		print "===================================="
		print ""
		print " changedate_automatic.py <DELIVERY>"
                print ""
		print "e.g. changedate_automatic.py 2012.1.00456.S_uid___A002_X5a9a13_X7da"
		print ""
		print "to halt public release use date 3000-01-01"
		print ""
		sys.exit()
	else:   
		delivery = sys.argv[1]

        print ''
        print '========================================================================'
        print 'PROCEED TO MODIFY RELEASE DATE OF '+delivery
        print '========================================================================'
        print ''
        passwd = getpass.getpass('Enter password for ALMA schema: ')
        print ''
        print 'Connecting to database . . .'
        print ''
        #dsn = '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS = (PROTOCOL = TCP)(HOST = oraclsco1-vip.sco.alma.cl)(PORT = 1521))(ADDRESS = (PROTOCOL = TCP)(HOST = oraclsco2-vip.sco.alma.cl)(PORT = 1521)))(CONNECT_DATA=(SERVICE_NAME=ALMA.SCO.CL))(FAILOVER_MODE=(TYPE=SELECT)(METHOD=BASIC)))'
        #orcl = cx_Oracle.connect('alma', passwd, dsn)
        #cursor = orcl.cursor()

        orcl = cx_Oracle.connect('alma', passwd, 'ALMA.OSF.CL')
        cursor = orcl.cursor()



	mouss_pre = delivery[15:]
        mouss_temp = mouss_pre.replace('uid___','uid://')
        mouss = mouss_temp.replace('_','/')

	print ''
	print '_________________________________________________________'
	print ''
	print 'DELIVERY = '+delivery
	print ''	
	print 'MOUSS = '+mouss
	print '_________________________________________________________'
	print ''
	proceed=raw_input("do you want to proceed with this MOUSS? y/n : ")
	if proceed is not 'y':
		print ''
		sys.exit('Exiting')		
	else:
		# show original date and original comment
	
		sql3='''select release_date_comment from alma.dp_delivery_status where delivery_id=\''''+delivery+'''\' '''
		sql4='''select release_date from alma.dp_delivery_status where delivery_id=\''''+delivery+'''\' '''
		cursor.execute(sql3)
		row = cursor.fetchone()
		comenta=row[0]
		print '_________________________________________________________'
		print ''
		print 'Original Comment: '+str(comenta)
                cursor.execute(sql4)
                row = cursor.fetchone()
                fecha=row[0]
		print ''
                print 'Original Release Date: '+str(fecha)
		print '_________________________________________________________'
		# end code	

		print ''
		apo = raw_input("Enter the number of the APO Ticket where the file was ingested - i.e. 658 - : ")
		print ''
		new_apo = raw_input("Enter the number of the APO Ticket that modifies the release date - i.e. 760 - : ")
		print ''
		#new_date = raw_input("Enter the new release date in YYYY-MM-DD - i.e. 2015-12-30: ")
		#print ''
		#print '=========================='
		#print '        NEW VALUES        '
		#print '=========================='
		#print ''
		#print 'APO Ingestion: '+apo
		#print 'APO Modification: '+new_apo
		#print 'New Release Date: '+new_date
		#print '___________________________'
		#print ''
		#proceed=raw_input("Do you want to proceed with this values? y/n : ")
		#if proceed is not 'y':
		#	print ''
		#	sys.exit('Exiting')
		
#FOLLOWING QUERY RETURNS THE NUMBER OF ROWS FOR THE GIVEN DELIVERY

		sql0='''select count(*) from alma.dp_delivery_status where delivery_id=\''''+delivery+'''\' '''
		#print sql0
		cursor.execute(sql0)
		row = cursor.fetchone()
		contador=row[0]
		#print 'CASE '+str(contador)
		

# CASE 0 - THE ROW DOESNT EXIST, IT NEEDS TO BE ISERTED

		if contador == 0:
			print ''
			print 'Delivery was not found in DELIVERY tables, please enter following values:'
			print '========================================================================='
			print ''
			ingestion_date = raw_input("Enter the Ingestion Date in YYYY-MM-DD - i.e. 2013-11-28: ")
			print ""
			new_date = raw_input("Enter the new release date in YYYY-MM-DD - i.e. 2015-12-30: ")
			print ""
                	print '=========================='
               		print '        NEW VALUES        '
                	print '=========================='
                	print ''
                	print 'APO Ingestion: '+apo
                	print 'APO Modification: '+new_apo
               		print 'Ingestion Date: ' +ingestion_date
		 	print 'New Release Date: '+new_date
                	print '___________________________'
                	print ''
                	proceed=raw_input("Do you want to proceed with this values? y/n : ")
                	if proceed is not 'y':
                	       print ''
                	       sys.exit('Exiting')

			validate_date(ingestion_date)
			validate_date(new_date)

			f=open('query_for_'+delivery+'.sql','w')
			f.write("ALTER SESSION SET NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS';\n")
		
			sql1='''select se.se_project_code,a.preferredarc,s.PARENT_OBS_UNIT_SET_STATUS_ID, concat(se.se_project_code,concat('',replace(replace(replace(s.PARENT_OBS_UNIT_SET_STATUS_ID,'://','___'),'/','_'),'uid','_uid'))) DELIVERY_ID,se.SE_EB_UID,se.se_qa0flag,a.request_handler_id,sysdate+2/24,add_months( sysdate, 12 ) from alma.shiftlog_entries se, alma.sched_block_status s, alma.mv_schedblock m, alma.account a, alma.mv_obsproposal p where se.se_sb_id=s.DOMAIN_ENTITY_ID and m.SB_ARCHIVE_UID=s.DOMAIN_ENTITY_ID and se.se_project_code=p.code and a.account_id=p.pi_userid AND (se.se_qa0flag LIKE 'Pass%' or se.se_qa0flag LIKE 'SemiPass%') and s.PARENT_OBS_UNIT_SET_STATUS_ID=\''''+mouss+'''\' '''
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
                       			sysdate_2 = str(ingestion_date)+ " 00:00:00" #row[7]
					sysdate_year = str(new_date)+ " 00:00:00" #row[8]
					print ""			
					f.write("insert into alma.dp_delivery_asdm_ous (asdm_uid,deliverable_name,id) values ('"+str(exec_block)+"','"+delivery+"', asa_sequence.nextval);\n")
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
			

			print ''
			f.write("insert into alma.dp_delivery_status (id, delivery_id, pi_account_id, qa2_passed, notification_date, original_release_date, release_date, release_date_comment) values (asa_sequence.nextval,'"+delivery+"','"+str(request_handler)+"','Y','"+str(sysdate_2)+"','"+str(sysdate_year)+"','"+str(sysdate_year)+"','Ingestion: APO-"+apo+" Modification: APO-"+new_apo+"');\n")
			f.write("commit;\n")
			f.write("exit\n")
			print '_____________________________________________________________________________________'
			print ''
			print 'DP_DELIVERY_STATUS insertion query for '+delivery+' created'
			print '_____________________________________________________________________________________'
			print ''
			passwd_os=passwd.replace('$','\$')
			g=open('script_'+delivery+'.sh','w')
			script_query='script_'+delivery+'.sh'

			g.write("sqlplus alma/"+passwd_os+"@'ALMA.OSF.CL' @query_for_"+delivery+".sql\n")

	                f.close()
	                g.close()
	
        	        call("sh '%s'"%script_query, shell=True)


#			g.write("sqlplus alma/"+passwd_os+"@'ALMA_OFFLINE.SCO.CL' @query_for_"+delivery+".sql\n")

#			f.close()
#			g.close()

#			call("sh '%s'"%script_query, shell=True)

# CASE 1 - THE ROW ALREADY EXISTS SO IT NEEDS TO BE UPDATED

		if contador==1:
			print ''
			print 'Delivery was found so Release Date and Comments will be updated'
			print '==============================================================='
                        print ""
                        new_date = raw_input("Enter the new release date in YYYY-MM-DD - i.e. 2015-12-30: ")
                        print ""
                        print '=========================='
                        print '        NEW VALUES        '
                        print '=========================='
                        print ''
                        print 'APO Ingestion: '+apo
                        print 'APO Modification: '+new_apo
                        print 'New Release Date: '+new_date
                        print '___________________________'
                        print ''
                        proceed=raw_input("Do you want to proceed with this values? y/n : ")
                        if proceed is not 'y':
                               print ''
                               sys.exit('Exiting')

                        validate_date(new_date)

			print ''
			f=open('query_for_'+delivery+'.sql','w')
                        f.write("ALTER SESSION SET NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS';\n")
	                sql2='''select release_date_comment from alma.dp_delivery_status where delivery_id=\''''+delivery+'''\' '''
                	print sql2
                	cursor.execute(sql2)
                	row = cursor.fetchone()
                	comentario=row[0]
                	print comentario
		
			f.write("UPDATE ALMA.DP_DELIVERY_STATUS SET RELEASE_DATE='"+str(new_date)+" 00:00:00', RELEASE_DATE_COMMENT='Ingestion: APO-"+str(apo)+" Modification: APO-"+str(new_apo)+"' where delivery_id = '"+str(delivery)+"' ;\n")
                        f.write("commit;\n")
                        f.write("exit\n")
                        print '_____________________________________________________________________________________'
                        print ''
                        print 'DP_DELIVERY_STATUS insertion query for '+delivery+' created'
                        print '_____________________________________________________________________________________'
                        print ''
                        passwd_os=passwd.replace('$','\$')
                        g=open('script_'+delivery+'.sh','w')
                        script_query='script_'+delivery+'.sh'
			g.write("sqlplus alma/"+passwd_os+"@'ALMA.OSF.CL' @query_for_"+delivery+".sql\n")

#g.write("sqlplus alma/"+passwd_os+"@'(DESCRIPTION =(ADDRESS = (PROTOCOL = TCP)(HOST = oracl1-vip.osf.alma.cl)(PORT = 1521))(CONNECT_DATA =(SERVER = DEDICATED)(SID = ALMA1)))' @query_for_"+delivery+".sql\n")



                        f.close()
                        g.close()

                        call("sh '%s'"%script_query, shell=True)

# CASE 2 - THERE IS A DUPLICATED ROW	

		if contador>1:
			print '========================================================================'
			print 'THE DELIVERY SEEMS TO BE DUPLICATED PLEASE CORRECT IT MANUALLY IN THE DB'
			print '========================================================================'
			sys.exit('Exiting')	
		print ''
		print '==================================================================================================='
		print 'To check the new status use the following query:           '
		print ''
		print "select * from alma.dp_delivery_status where delivery_id ='"+delivery+"';"
		print ''
		print '==================================================================================================='
		print ''	
		
