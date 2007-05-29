VERSION    = 01.00.11

DEFINES    =

###
# The following flags enable experimental features.
# By default, these are enabled for development versions of the driver, and
# disabled for release versions.

# Optional: Enable driver debugging
DEFINES   += -DGSPCA_ENABLE_DEBUG

# Optional: Enable direct register read/write for PAC207 development
#DEFINES   += -DGSPCA_ENABLE_REGISTERPLAY

###
# The following flags enable features that aren't yet implemented, and
# therefore are disabled by default.

# Optional: Enable compression
DEFINES   += -DGSPCA_ENABLE_COMPRESSION

###
# Rest of Makefile follows here. You probably won't need to touch this.

# Setup defines
DEFINES   += -DCONFIG_USB_GSPCA_MODULE=1 -DMODULE -D__KERNEL__
DEFINES   += -DVID_HARDWARE_GSPCA=0xFF -DGSPCA_VERSION=\"$(VERSION)\"

ifneq ($(KERNELRELEASE),)   # We were called by kbuild
CFLAGS += $(DEFINES) 
obj-m += gspca.o
gspca-objs := gspca_core.o decoder/gspcadecoder.o 

else   # We were called from command line

KERNEL_VERSION = `uname -r`
KERNELDIR := /lib/modules/$(KERNEL_VERSION)/build
PWD  := $(shell pwd)
MODULE_INSTALLDIR = /lib/modules/$(KERNEL_VERSION)/kernel/drivers/usb/media/
MODULE_INSTALLDIR2 = /lib/modules/$(KERNEL_VERSION)/kernel/drivers/media/video/

default:
	$(MAKE) -C $(KERNELDIR) SUBDIRS=$(PWD) CC=$(CC) modules

install:
	mkdir -p $(MODULE_INSTALLDIR)
	rm -f $(MODULE_INSTALLDIR)spca5xx.ko
	rm -f $(MODULE_INSTALLDIR2)gspca.ko
	install -c -m 0644 gspca.ko $(MODULE_INSTALLDIR)
	/sbin/depmod -ae

uninstall:
	rm -f $(MODULE_INSTALLDIR)gspca.ko
	/sbin/depmod -aq

endif

############################################################################## 
# OTHER TARGETS 
##############################################################################
clean:
	rm -r -f *.o decoder/.gspcadecoder.o.cmd decoder/*.o \
	.gspca.o.cmd  *.o *.ko *.mod.* .[a-z]* core *.i \
	*.symvers *.err
	
############################################################################## 
