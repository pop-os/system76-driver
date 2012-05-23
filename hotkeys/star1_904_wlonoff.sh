#!/bin/sh
#
# "Toggle wireless on/off"
#

if [ $USER != "root" ]; then
	echo "You need admin rights to run this script. Try with sudo."
	exit 1
fi

# If $SUDO_USER is not specified, defaults to root.
if [ -z $SUDO_USER ]; then
	SUDO_USER="root"
fi

if lsmod | grep r8187 > /dev/null; then
	modprobe -r r8187
else
	modprobe r8187
fi
exit 0
