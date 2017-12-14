#!/usr/bin/env python2.7

from sys import argv
from os import system
from time import time

file_id = argv[1]
sql = """
select * from (
-- North America
with na as
(select /*+ materialize */ file_id, file_version, checksum
      from ngas.ngas_files@alma.arc.na f
      where f.format like 'application/x-tar' and file_id like '%""" + file_id + """%') 
select 'NA' arc, sco.file_id, sco.file_version, sco.checksum, sco.ingestion_date from 
(select file_id, file_version, checksum, ingestion_date
      from ngas.ngas_files f
      where f.format like 'application/x-tar' and file_id like '%""" + file_id + """%') sco
  left join na    
  on (sco.file_id = na.file_id and sco.file_version = na.file_version and sco.checksum = na.checksum)
  where na.file_id is null)
union
-- Europan Union
select * from (
with na as
(select /*+ materialize */ file_id, file_version, checksum
      from ngas.ngas_files@alma.arc.eu f
      where f.format like 'application/x-tar' and file_id like '%""" + file_id + """%') 
select 'EU' arc, sco.file_id, sco.file_version, sco.checksum, sco.ingestion_date from 
(select file_id, file_version, checksum, ingestion_date
      from ngas.ngas_files f
      where f.format like 'application/x-tar' and file_id like '%""" + file_id + """%') sco
  left join na    
  on (sco.file_id = na.file_id and sco.file_version = na.file_version and sco.checksum = na.checksum)
  where na.file_id is null)
union
select * from (
-- East Asia
with na as
(select  /*+ materialize */  file_id, file_version, checksum
      from ngas.ngas_files@alma.arc.ea f
      where f.format like 'application/x-tar' and file_id like '%""" + file_id + """%') 
select 'EA' arc, sco.file_id, sco.file_version, sco.checksum, sco.ingestion_date from 
(select file_id, file_version, checksum, ingestion_date
      from ngas.ngas_files f
      where f.format like 'application/x-tar' and file_id like '%""" + file_id + """%') sco
  left join na    
  on (sco.file_id = na.file_id and sco.file_version = na.file_version and sco.checksum = na.checksum)
  where na.file_id is null)
order by 1, 2, 3;
"""

sql = """
col arc format a3
col file_id format a40
col checksum format a12

select 'SCO' arc, file_id, file_version, checksum
  from ngas.ngas_files f
  where f.format like 'application/x-tar' and file_id like '%""" + file_id + """%'
  order by 2;

      
select 'NA' arc, file_id, file_version, checksum
  from ngas.ngas_files@alma.arc.na f
  where f.format like 'application/x-tar' and file_id like '%""" + file_id + """%'
  order by 2;

  
select 'EU' arc, file_id, file_version, checksum
  from ngas.ngas_files@alma.arc.eu f
  where f.format like 'application/x-tar' and file_id like '%""" + file_id + """%'
  order by 2;


select 'EA' arc, file_id, file_version, checksum
  from ngas.ngas_files@alma.arc.ea f
  where f.format like 'application/x-tar' and file_id like '%""" + file_id + """%'
  order by 2;


quit;

"""

tmpfile = "/tmp/.check-file_id-in-ARCs." + str(time()) + ".sql"
of = open(tmpfile, "w")
of.write(sql)
of.close()

system("sqlplus almasu/alma4dba@ALMA.SCO.CL @" + tmpfile)


