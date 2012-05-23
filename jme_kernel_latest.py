#!/usr/bin/env python

import os
import shutil

def makefile_kernel():
	fileList = []
	for file in os.listdir("/usr/src/"):
		if "linux-headers" and "generic" not in file:
			pass
		else:
			fileList.append(file)
	
	fileList.sort()
	
	latest = (fileList.pop()).lstrip("linux-headers-")
	
	makefileLocation = "/opt/system76/system76-driver/src/jme-1.0.5/Makefile"
	newMakefileLocation = makefileLocation + "new" 
	
	makefile = open(makefileLocation,'r')
	newmakefile = open(newMakefileLocation,'w')
	
	for line in makefile:
		if "BUILD_KERNEL=" in line:
			newmakefile.write("BUILD_KERNEL=" + latest + "\n")
		else:
			newmakefile.write(line)
	
	makefile.close()
	newmakefile.close()
	shutil.copyfile(makefileLocation, (makefileLocation + ".bk")) #Back up makefile
	shutil.copyfile(newMakefileLocation, makefileLocation) #Copy in the new makefile



