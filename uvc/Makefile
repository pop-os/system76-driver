KERNEL_VERSION	:= `uname -r`
KERNEL_DIR	:= /lib/modules/$(KERNEL_VERSION)/build
INSTALL_MOD_DIR	:= ubuntu/media/usbvideo

PWD		:= $(shell pwd)

obj-m		:= uvcvideo.o
uvcvideo-objs   := uvc_driver.o uvc_queue.o uvc_v4l2.o uvc_video.o uvc_ctrl.o uvc_status.o uvc_isight.o

all: uvcvideo

uvcvideo:
	@echo "Building USB Video Class driver..."
	@sh svn-version.sh > version.h 2>/dev/null
	@(make -C $(KERNEL_DIR) M=$(PWD) CROSS_COMPILE=$(CROSS_COMPILE) modules)

install:
	@echo "Installing USB Video Class driver..."
	@(make -C $(KERNEL_DIR) M=$(PWD) INSTALL_MOD_DIR=$(INSTALL_MOD_DIR) INSTALL_MOD_PATH=$(INSTALL_MOD_PATH) modules_install)

clean:
	-rm -f *.o *.ko .*.cmd .*.flags *.mod.c Module.symvers version.h modules.order
	-rm -rf .tmp_versions

