#!/usr/bin/env python2.7

import sys
import os
from xml.dom import minidom
import cx_Oracle
from asdmExportconf import oradict
from asdmExportconf import schemadict
from asdmExportconf import db_alma,db_apo05, db_testbench

def CheckUID(uid=None, table=None):
    ''' CheckUID: checks if a given uid is in the Archive, returns True or False
    Parameters:
        uid : the uid of the record
        table : the Table to look the record
    '''
    if uid==None or table == None:
        print "Must provide UID and Table"
        sys.exit(1)

    conn_string = db_alma
#    conn_string = db_testbench
    conn = cx_Oracle.connect(conn_string)
    query = u"SELECT ARCHIVE_UID FROM ALMA." + table + u" WHERE ARCHIVE_UID='" + uid + "'"
    #print query
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        if cursor.fetchone() != None:
            conn.close()
            return True
        else:
            conn.close()
            return False
    except Exception as exc:
        conn.close()
        print 'exception'
        print exc
        sys.exit(1)
        

def CreateSQL(uid = None, uiddir = None, entity = None ,table = None, schemauid = None, toc = None):
    ''' CreateSQL: Creates the SQL statement to ingest any XML into the table that correspond
    Parameters:
        uid: UID of the given XML
        uiddir: Normaly the folder that contains all the XML i.e.: uid__XXXX_XXX/
        entity: The type of entity thats going to be inserted, this is used to locate the file .xml in the folder
        table: the Model table in the Archive ,i.e.: XML_ASDM_ENTITIES
        schemauid: the UID of the schema definition (XSD) this is defined in the table XML_SCHEMA_ENTITIES
        toc: Time of Creation in format YYYY-MM-DD"T"HH24:MI:SS
    '''
    if uid == None or uiddir==None or entity== None or table == None or schemauid == None or toc == None:
        print "Must provide UID ,uiddir, entity, table, schemauid, toc"
        sys.exit(1)
    query = "INSERT INTO "+table
    query += " SELECT '" + uid + "',"
    query += " TO_DATE('"+ toc +"', 'YYYY-MM-DD\"T\"HH24:MI:SS') ,"
    query += " XMLTYPE (bfilename('APO_XML_LOCATION', '"+ uiddir + "/" + entity +".xml'), nls_charset_id('AL16UTF8')) ,"
    query += " '" +schemauid + "',"
    query += " 'USER',"
    query += " 0,"
    query += " NULL,"
    query += " NULL,"
    query += " 0,"
    query += " 0,"
    query += " 0"
    query += " FROM DUAL; \n"
    return query
    
def CreateUpdateSQL(uid = None, uiddir = None, entity = None ,table = None):
    ''' CreateSQL: Creates the SQL statement to ingest any XML into the table that correspond
    Parameters:
        uid: UID of the given XML
        uiddir: Normaly the folder that contains all the XML i.e.: uid__XXXX_XXX/
        entity: The type of entity thats going to be inserted, this is used to locate the file .xml in the folder
        table: the Model table in the Archive ,i.e.: XML_ASDM_ENTITIES
    '''
    if uid == None or uiddir==None or entity== None or table == None:
        print "Must provide UID ,uiddir, entity, table, schemauid, toc"
        sys.exit(1)
    query = "UPDATE ALMA."+table+" AL1 "
    query += "SET AL1.XML = XMLTYPE (bfilename('APO_XML_LOCATION', '"+ uiddir + "/" + entity +".xml'), nls_charset_id('AL16UTF8')) "
    query += "WHERE AL1.ARCHIVE_UID = '"+uid+"'; \n" 
    return query
    
    

if __name__=="__main__":

    #print "USAGE: asdmReingest APO/uid___XXXX_XXX"
    #print "APO is a symbolic link to /home/jao/asdm_reingestion/APO"
    #print "If .bin are included use following command"
    #print "ngamsCClient -cmd ARCHIVE -timeOut 3600 -fileUri <FILE>.bin -mimetype multipart/related -host ngobe01.osf.alma.cl -port 7777"

    
    UID = sys.argv[1]   #Parse the first Argument , the Directory where is the ASDM.xml
    asdmxml = minidom.parse(UID+'ASDM.xml') #Parsing the ASDM.XML Document
    nodes = asdmxml.getElementsByTagName("Entity") #Gets all the nodes in the ASDM.xml Document
    uid = asdmxml.getElementsByTagName("Entity")[0].getAttribute("entityId") #Gets only the UID of the ASDM
    uiddir = uid.replace(':','_').replace('/','_') #transform the UID from uid:// into uid___
    timeofcreation = asdmxml.getElementsByTagName("TimeOfCreation")[0].childNodes[0].nodeValue #Gets the Time of creation of the ASDM.xml
    sqlfile = open(uiddir+'.sql','w+')

    for i in nodes:
        #print i.getAttribute("entityTypeName"), oradict[i.getAttribute("entityTypeName")], i.getAttribute("entityId")
        #print i.getAttribute("entityTypeName"), oradict[i.getAttribute("entityTypeName")], i.getAttribute("entityId")
        if CheckUID(i.getAttribute("entityId"),oradict[i.getAttribute("entityTypeName")]) == False:
            #IMPORTANT!! the isfile function aim at a particular folder! MUST change if the enviroment changes
            if os.path.isfile('./APO/'+ uiddir + '/' + i.getAttribute("entityTypeName").replace('Table','')+'.xml' ):
                query = CreateSQL(i.getAttribute("entityId"),uiddir,i.getAttribute("entityTypeName").replace('Table',''),oradict[i.getAttribute("entityTypeName")],schemadict[i.getAttribute("entityTypeName")],timeofcreation[:20])
                print query
                sqlfile.write(query)
            else:
                print 'The File '+uiddir + '/' + i.getAttribute("entityTypeName").replace('Table','')+'.xml Does not exist'
                #sys.exit(1)
        else:
            if os.path.isfile('./APO/'+ uiddir + '/' + i.getAttribute("entityTypeName").replace('Table','')+'.xml' ):
                query = CreateUpdateSQL(i.getAttribute("entityId"),uiddir,i.getAttribute("entityTypeName").replace('Table',''),oradict[i.getAttribute("entityTypeName")])
                print query
                sqlfile.write(query)
            else:
                print 'The File '+uiddir + '/' + i.getAttribute("entityTypeName").replace('Table','')+'.xml Does not exist'
                #sys.exit(1)

    sqlfile.write('COMMIT;\nQUIT;\n')
    sqlfile.close()
