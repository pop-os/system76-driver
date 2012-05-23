#!/usr/bin/env python

import os
import shutil

WORKDIR = os.path.join(os.path.dirname(__file__), '.')
WIRELESS8187B = os.path.join(os.path.dirname(__file__), 'rtl8187B/rtl8187/')

os.system("sudo rm /etc/modprobe.d/rtl8187.conf")
os.system("echo blacklist rtl8187 | sudo tee -a /etc/modprobe.d/rtl8187.conf")

# Get the driver
os.chdir(WORKDIR)
os.system("sudo wget http://planet76.com/drivers/star1/rtl8187B.tar.gz")
os.system("tar -xf rtl8187B.tar.gz")

# Configure rtl8187 Makefile
fileList = []
for file in os.listdir("/usr/src/"):
	if "linux-headers" and "generic" not in file:
		pass
	else:
		fileList.append(file)

fileList.sort()

latest = (fileList.pop()).lstrip("linux-headers-")

makefileLocation = "/opt/system76/system76-driver/src/rtl8187B/rtl8187/Makefile"
newMakefileLocation = makefileLocation + "new" 

makefile = open(makefileLocation,'r')
newmakefile = open(newMakefileLocation,'w')

for line in makefile:
	if "KVER  := " in line:
		newmakefile.write("KVER  := " + latest + "\n")
	else:
		newmakefile.write(line)

makefile.close()
newmakefile.close()
shutil.copyfile(makefileLocation, (makefileLocation + ".bk")) #Back up makefile
shutil.copyfile(newMakefileLocation, makefileLocation) #Copy in the new makefile

# Configure ieee80211 Makefile
fileList = []
for file in os.listdir("/usr/src/"):
	if "linux-headers" and "generic" not in file:
		pass
	else:
		fileList.append(file)

fileList.sort()

latest = (fileList.pop()).lstrip("linux-headers-")

makefileLocation = "/opt/system76/system76-driver/src/rtl8187B/ieee80211/Makefile"
newMakefileLocation = makefileLocation + "new" 

makefile = open(makefileLocation,'r')
newmakefile = open(newMakefileLocation,'w')

for line in makefile:
	if "KVER  := " in line:
		newmakefile.write("KVER  := " + latest + "\n")
	else:
		newmakefile.write(line)

makefile.close()
newmakefile.close()
shutil.copyfile(makefileLocation, (makefileLocation + ".bk")) #Back up makefile
shutil.copyfile(newMakefileLocation, makefileLocation) #Copy in the new makefile

# Configure and Install Driver
os.chdir(WIRELESS8187B)
os.system("sudo make && sudo make install")
os.chdir(WORKDIR)
os.system('sudo rm -r rtl8187B.tar.gz rtl8187B/')
