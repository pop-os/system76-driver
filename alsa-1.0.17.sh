#!/bin/sh

#install necessary packages
apt-get install -y build-essential ncurses-dev gettext linux-headers-`uname -r` alsa-oss

echo "downloading alsa packages..."
wget ftp://ftp.alsa-project.org/pub/lib/alsa-lib-1.0.17.tar.bz2
wget ftp://ftp.alsa-project.org/pub/driver/alsa-driver-1.0.17.tar.bz2
wget ftp://ftp.alsa-project.org/pub/tools/alsa-tools-1.0.17.tar.bz2
wget ftp://ftp.alsa-project.org/pub/utils/alsa-utils-1.0.17.tar.bz2

echo "extracting alsa packages..."
tar -xjf alsa-driver*.tar.bz2
tar -xjf alsa-lib*.tar.bz2
tar -xjf alsa-utils*.tar.bz2
tar -xjf alsa-tools*.tar.bz2
rm alsa*.tar.bz2

echo "setting up alsa for compilation"
mkdir -p /usr/src/alsa
mv alsa-* /usr/src/alsa

#alsa-driver
cd /usr/src/alsa/alsa-driver*
./configure --with-cards=hda-intel,usb-audio --prefix=/usr
make
make install

#alsa-lib
cd /usr/src/alsa/alsa-lib*
./configure --prefix=/usr
make
make install

#alsa-tools
cd /usr/src/alsa/alsa-tools*
./configure --prefix=/usr
make
make install

#alsa-utils
cd /usr/src/alsa/alsa-utils*
./configure --prefix=/usr
make
make install

# Thanks to Ubuntu user, 'Nescafi' for help with this part
cd /usr/src/alsa/alsa-driver-1.0.17/
find ./ -name ''*.ko'' > /tmp/alsa_manifest

#Uncomment the following block of code for use with 2.6.26-x kernel
#tar -cv -T /tmp/alsa_manifest -f /lib/modules/`uname -r`/kernel/sound/alsa-driver-1.0.17.tar
#cd /lib/modules/`uname -r`/kernel/sound/

#This block of code works with 2.6.24-x Ubuntu kernels
tar -cv -T /tmp/alsa_manifest -f /lib/modules/`uname -r`/ubuntu/sound/alsa-driver/alsa-driver-1.0.17.tar
cd /lib/modules/`uname -r`/ubuntu/sound/alsa-driver

#Extract new modules, overwriting old ones
tar -xvf alsa-driver-1.0.17.tar
depmod -a

echo "ALSA 1.0.17 will not be loaded until the next reboot.."

