#!/bin/sh
#Increase screen brightness after resume from suspend

brtNum=`cat /proc/acpi/asus/brn`
echo $brtNum > /proc/acpi/asus/brn
