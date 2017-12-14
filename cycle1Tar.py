#!/usr/bin/env python2

# __author__ = 'sagonzal'
import cx_Oracle
import sys
import os
import subprocess as sp

db = {
    "osf": "almasu/alma4dba@ALMA_OFFLINE.OSF.CL", 

    "sco": "almasu/alma4dba@ALMA_OFFLINE.SCO.CL"}

conn = cx_Oracle.connect(db['sco'])


hierarchy = {1: 'project.', 2: 'science_goal.', 3: 'group.', 4: 'member.'}

arg = sys.argv[1]
code = arg[:14]
uid = arg[15:]
member_uid = uid.replace('uid___','').split('_')
member_uid = 'uid://'+member_uid[0]+'/'+member_uid[1]+'/'+member_uid[2]

try:
    print 'MEMBER UID '+member_uid
    cursor = conn.cursor()
    sql = "SELECT OBS_PROJECT_ID FROM ALMA.OBS_UNIT_SET_STATUS WHERE STATUS_ENTITY_ID = '" + member_uid + "'"
    cursor.execute(sql)
    prj_uid = cursor.fetchone()[0]
    print 'PROJECT UID'+prj_uid
    sql = " SELECT PRJ_CODE FROM  ALMA.BMMV_OBSPROJECT WHERE PRJ_ARCHIVE_UID = '" + prj_uid + "'"
    cursor.execute(sql)
    prj_code = cursor.fetchone()[0]

except Exception as e:
    print 'Project Code / UID Not found in the Database'
    print e
    conn.close()
    sys.exit(1)

query = """SELECT status_entity_id as id , parent_obs_unit_set_status_id as parent_id
      FROM ALMA.OBS_UNIT_SET_STATUS
     WHERE OBS_PROJECT_ID = 'XXXXYYYY'
           AND domain_entity_state != 'Deleted'
START WITH parent_obs_unit_set_status_id IS NULL
CONNECT BY PRIOR status_entity_id = parent_obs_unit_set_status_id"""

query = query.replace('XXXXYYYY', prj_uid)

try:
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

except:
    conn.close()
    sys.exit(1)

print '************************************'
print 'Project Code: ', prj_code
print 'Project UID: ', prj_uid


tree_of_project = list()
deep = 1
for i in rows:
    try:
        if i[1] is None:
            tree_of_project.append((i[0].replace(':', '_').replace('/', '_'), None))
        else:
            tree_of_project.append((i[0].replace(':', '_').replace('/', '_'), i[1].replace(':', '_').replace('/', '_')))
    except Exception as e:
        print e
        sys.exit(1)

back = dict(tree_of_project)
tree_of_member = list()
temp = member_uid.replace('://','___').replace('/','_')

while True:
    tree_of_member.append((temp, back[temp]))
    if back[temp] is None:
        break
    else:
        temp = back[temp]

def createDir(dirlist=None):
    global tree_of_member
    global hierarchy
    global deep
    if deep > 1:
        for i in dirlist:
            os.mkdir(hierarchy[deep] + i)

        for i in dirlist:
            b = [v[0] for x, v in enumerate(tree_of_member) if v[1] == i]
            os.chdir(hierarchy[deep] + i)
            if len(b) > 0:
                deep += 1
                createDir(b)
                deep -= 1
    else:
        deep += 1
        createDir([v[0] for x, v in enumerate(tree_of_member) if v[1] == dirlist[0]])
        deep -= 1
    os.chdir('..')


try:
    print 'Creating Directory Structure'
    z = [v[0] for i, v in enumerate(tree_of_member) if v[1] is None]
    os.mkdir(prj_code + '_temp')
    os.chdir(prj_code + '_temp')
    createDir(z)
except Exception as e:
    print "Error creating the directory"
    print e
    sys.exit(1)

try:
    print 'Untar the file: ', arg

    sp.call(['tar', '-xf', arg])

    print 'Getting the directories'
    source = sp.Popen(['find', '.', '-type','d','-name','member_ouss*'], stdout=sp.PIPE).communicate()[0]
    dest = sp.Popen(['find', '.', '-name', 'member.' + member_uid.replace('://', '___').replace('/', '_')], stdout=sp.PIPE).communicate()[0]
    dest = dest.replace('\n','/')
    source = source.replace('\n','/*')
    if len(dest) < 1 or len(source) < 1:
        print "No matched Source or Destination directory"
        print 'Source Directory: ', source
        print 'Destination Directory: ', dest
        sys.exit(1)
    print 'Source Directory: ', source , '<-'
    print 'Destination Directory: ', dest  , '<-'


    print 'Copying the Files'
    os.system('cp -R '+source+' '+dest)

    print 'Renaming the Directories'

    os.system('mv ' + prj_code + ' ' + prj_code + '_old')
    os.system('mv ' + prj_code + '_temp' + ' ' + prj_code)


    print 'Renaming old tar file'
    os.system('mv ' + arg + ' ' + arg + '.old')

    print 'Renaming files'



    print 'Creating new README file with the following content'
    tree = sp.Popen(['tree', '-L', '5', prj_code], stdout=sp.PIPE).communicate()[0]
    readme = sp.Popen(['find', './'+prj_code, '-name' ,'README'], stdout=sp.PIPE).communicate()[0]
    original = open(readme.replace('\n',''),'r')
    new = open('NEW_README','w')
    for i in original.readlines():
        if not i.find('|--'):
            new.write(tree)
            break
        else:
            new.write(i)
    original.close()
    new.close()
    os.system('cp NEW_README ' + readme.replace('\n', ''))
    print tree

    print 'Creating new tar file'

    os.system('tar -cf '+ arg + ' ' + prj_code)
except Exception as e:

    print e
    sys.exit(1)


