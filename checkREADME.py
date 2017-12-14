#!/usr/bin/python2

from os import system
from sys import argv

## Get the argument.
## The argument must be project name + date. Ej "2011.0.00206.S_2012-06-22".
prj = argv[1]
print("Extracting content filenames from tar files of project " + prj + ".")
print("This could take some minutes ...\n")

## Following line makes the magic. 
## It extracts all filenames archived in all tar files and puts them in a single .list file.
system("rm -f " + prj + ".list")
system('for i in `ls -1 ' + prj + '*tar`; do for j in `tar -tf $i`; do echo $i";"$j >> ' + prj + '.list; done ; done')

of = open(prj + ".list")
biglist = of.readlines()
of.close()

readme = list()
for l in biglist:
	tarfilename, content = l.split(";")
	if content.rfind("README") != -1:
		readme.append([tarfilename, content[:-1]])

for r in readme:
	system("tar -xf " + r[0] + " " + r[1])
	of = open(r[1])
	checkfiles = list()
	for l in of.readlines():
		if l[0] == '|': ## The important part of README begins with '|'
			## Extract only the last part of files tree
			checkfiles.append(l.split(" ")[-1][:-1])
	of.close()

filesok = list()
for c in checkfiles:
	for b in biglist:	
		if c in b: ## If the file/directory name is found, is ok.
			filesok.append(c)

## filesno is the difference between all files and those that were found.
## Therefore, they are not present in tars.
filesno = set(checkfiles) - set(filesok)


if len(filesno) > 0:
	print("IMPORTANT: The following files were NOT found in tar files")
	print("           Please check manually README files and project content")
	for f in filesno:
		print("Not found: " + f)
else:
	print("All files in README were found successfully.")
