obj-m	    += tifm_core.o tifm_7xx1.o tifm_sd.o

KERNELDIR ?= /lib/modules/$(shell uname -r)/build
PWD       := $(shell pwd)
MODULE_INSTALLDIR = /lib/modules/$(shell uname -r)/misc

all:
	$(MAKE) -C $(KERNELDIR) M=$(PWD)

clean:
	rm -rf *.o *.o.d *.ko.d .depend .*.cmd *.ko *.mod.c .tmp_versions

install:
	mkdir -p $(MODULE_INSTALLDIR)
	rm -f $(MODULE_INSTALLDIR)/tifm_core.ko
	rm -f $(MODULE_INSTALLDIR)/tifm_sd.ko
	rm -f $(MODULE_INSTALLDIR)/tifm_7xx1.ko
	install -c -m 644 tifm_core.ko tifm_7xx1.ko tifm_sd.ko $(MODULE_INSTALLDIR)
	/sbin/depmod -ae
