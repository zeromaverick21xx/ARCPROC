#!/usr/bin/env python2.7

from sys import argv
from random import choice
from os import system

## Get the argument.
files = argv[1:]
for f in files:
	cmd = ("ngamsCClient -host ngassco0" + str(choice(range(1, 9))) + ".sco.alma.cl -port 777"  
		+ str(choice(range(7, 9))) + " -cmd ARCHIVE -timeOut 360000 -fileUri " + f)
	print(cmd)
	system(cmd)
