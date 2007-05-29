
#ifndef SPCAUSB_H
#define SPCAUSB_INIT_H

#if LINUX_VERSION_CODE > KERNEL_VERSION(2, 6, 6)
#define wait_ms(a) msleep((a))
#endif
#if LINUX_VERSION_CODE > KERNEL_VERSION(2, 6, 11)
#define TimeOut 1000
#else
#define TimeOut HZ
#endif
/* Common functions prototype */
static int spca50x_reg_read(struct usb_device *dev,
			    __u16 reg, __u16 index, __u16 length);
static int spca50x_reg_write(struct usb_device *dev,
			     __u16 reg, __u16 index, __u16 value);

static void spca5xxRegRead(struct usb_device *dev,
			   __u16 reg,
			   __u16 value,
			   __u16 index, __u8 * buffer, __u16 length);
static void spca5xxRegWrite(struct usb_device *dev,
			    __u16 reg,
			    __u16 value,
			    __u16 index, __u8 * buffer, __u16 length);
static void sonixRegRead(struct usb_device *dev,
			 __u16 reg,
			 __u16 value,
			 __u16 index, __u8 * buffer, __u16 length);
static void sonixRegWrite(struct usb_device *dev,
			  __u16 reg,
			  __u16 value,
			  __u16 index, __u8 * buffer, __u16 length);
#if 0
static void Et_RegWrite(struct usb_device *dev,
			__u16 reg,
			__u16 value,
			__u16 index, __u8 * buffer, __u16 length);
static void Et_RegRead(struct usb_device *dev,
		       __u16 reg,
		       __u16 value,
		       __u16 index, __u8 * buffer, __u16 length);
#endif
static int spca_set_interface(struct usb_device *dev,
			      int interface, int alternate);
/*
static int spca_clear_feature(struct usb_device *dev,
				 int endpoint)
{
	int inpipe;
	inpipe = usb_rcvintpipe(dev,endpoint);
	usb_clear_halt(dev, inpipe);
	return 0;
}
*/

static int spca50x_setup_qtable(struct usb_spca50x *spca50x,
				unsigned int request,
				unsigned int ybase,
				unsigned int cbase,
				unsigned char qtable[2][64]);
/* Alias setting */
#define pac207RegWrite(dev,req,value,index,buffer,length) sonixRegWrite(dev,req,value,index,buffer,length)
#define pac207RegRead(dev,req,value,index,buffer,length) sonixRegRead(dev,req,value,index,buffer,length)
#define Et_RegWrite(dev,req,value,index,buffer,length) sonixRegWrite(dev,req,value,index,buffer,length)
#define Et_RegRead(dev,req,value,index,buffer,length) sonixRegRead(dev,req,value,index,buffer,length)
/***************************** Implementation ****************************/
static void spca5xxRegRead(struct usb_device *dev,
			   __u16 reg,
			   __u16 value,
			   __u16 index, __u8 * buffer, __u16 length)
{
    int rc;
    __u8 *kbuffer = NULL;
    __u16 RegType;
    if (length > 0) {
	kbuffer = (__u8 *) kmalloc(length, GFP_KERNEL);
	memcpy(kbuffer, buffer, length);
    }
    RegType = USB_DIR_IN | USB_TYPE_VENDOR | USB_RECIP_DEVICE;
    rc = usb_control_msg(dev,
			 usb_rcvctrlpipe(dev, 0),
			 reg,
			 RegType,
			 (__u16) value, (__u16) index, kbuffer, length,
			 TimeOut);
    if (length > 0) {
	memcpy(buffer, kbuffer, length);
	kfree(kbuffer);
    }
    if (buffer) {
	PDEBUG(5, "reg read: 0x%02X, 0x%02X, 0x%02X, 0x%02X: 0x%04X",
	       RegType, reg, value, index, (int) *buffer);
    } else {
	PDEBUG(5, "reg read: 0x%02X, 0x%02X,0x%02X, 0x%02X ", RegType, reg,
	       value, index);
    }
    return;
}


static void spca5xxRegWrite(struct usb_device *dev,
			    __u16 reg,
			    __u16 value,
			    __u16 index, __u8 * buffer, __u16 length)
{
    int rc;
    __u16 RegType;
    __u8 *kbuffer = NULL;
    if (length > 0) {
	kbuffer = (__u8 *) kmalloc(length, GFP_KERNEL);
	memcpy(kbuffer, buffer, length);
    }
    RegType = USB_DIR_OUT | USB_TYPE_VENDOR | USB_RECIP_DEVICE;
    rc = usb_control_msg(dev,
			 usb_sndctrlpipe(dev, 0),
			 reg,
			 RegType,
			 (__u16) value, (__u16) index, kbuffer, length,
			 TimeOut);
    if (length > 0) {
	memcpy(buffer, kbuffer, length);
	kfree(kbuffer);
    }
    if (buffer) {
	PDEBUG(5, "reg write: 0x%02X, 0x%02X, 0x%02X, 0x%02X: 0x%04X",
	       RegType, reg, value, index, (int) *buffer);
    } else {
	PDEBUG(5, "reg write: 0x%02X, 0x%02X,0x%02X, 0x%02X ", RegType,
	       reg, value, index);
    }
    return;
}
static void sonixRegRead(struct usb_device *dev,
			 __u16 reg,
			 __u16 value,
			 __u16 index, __u8 * buffer, __u16 length)
{
    int rc;
    __u8 *kbuffer = NULL;
    __u16 RegType;
    if (length > 0) {
	kbuffer = (__u8 *) kmalloc(length, GFP_KERNEL);
	memcpy(kbuffer, buffer, length);
    }
    RegType = USB_DIR_IN | USB_TYPE_VENDOR | USB_RECIP_INTERFACE;
    rc = usb_control_msg(dev,
			 usb_rcvctrlpipe(dev, 0),
			 reg,
			 RegType,
			 (__u16) value, (__u16) index, kbuffer, length,
			 TimeOut);
    if (length > 0) {
	memcpy(buffer, kbuffer, length);
	kfree(kbuffer);
    }
    if (buffer) {
	PDEBUG(5, "reg read: 0x%02X, 0x%02X, 0x%02X, 0x%02X: 0x%04X",
	       RegType, reg, value, index, (int) *buffer);
    } else {
	PDEBUG(5, "reg read: 0x%02X, 0x%02X,0x%02X, 0x%02X ", RegType, reg,
	       value, index);
    }
    return;
}

static void sonixRegWrite(struct usb_device *dev,
			  __u16 reg,
			  __u16 value,
			  __u16 index, __u8 * buffer, __u16 length)
{
    int rc;
    __u16 RegType;
    __u8 *kbuffer = NULL;
    if (length > 0) {
	kbuffer = (__u8 *) kmalloc(length, GFP_KERNEL);
	memcpy(kbuffer, buffer, length);
    }
    RegType = USB_DIR_OUT | USB_TYPE_VENDOR | USB_RECIP_INTERFACE;
    rc = usb_control_msg(dev,
			 usb_sndctrlpipe(dev, 0),
			 reg,
			 RegType,
			 (__u16) value, (__u16) index, kbuffer, length,
			 TimeOut);
    if (length > 0) {
	memcpy(buffer, kbuffer, length);
	kfree(kbuffer);
    }
    if (buffer) {
	PDEBUG(5, "reg write: 0x%02X, 0x%02X, 0x%02X, 0x%02X: 0x%04X",
	       RegType, reg, value, index, (int) *buffer);
    } else {
	PDEBUG(5, "reg write: 0x%02X, 0x%02X,0x%02X, 0x%02X ", RegType,
	       reg, value, index);
    }
    return;
}
#if 0
static void Et_RegRead(struct usb_device *dev,
		       __u16 reg,
		       __u16 value,
		       __u16 index, __u8 * buffer, __u16 length)
{
    int rc;
    __u8 *kbuffer = NULL;
    __u16 RegType;
    if (length > 0) {
	kbuffer = (__u8 *) kmalloc(length, GFP_KERNEL);
	memcpy(kbuffer, buffer, length);
    }
    RegType = USB_DIR_IN | USB_TYPE_VENDOR | USB_RECIP_INTERFACE;
    rc = usb_control_msg(dev,
			 usb_rcvctrlpipe(dev, 0),
			 reg,
			 RegType,
			 (__u16) value, (__u16) index, kbuffer, length,
			 TimeOut);
    if (length > 0) {
	memcpy(buffer, kbuffer, length);
	kfree(kbuffer);
    }
    if (buffer) {
	PDEBUG(5, "reg read: 0x%02X, 0x%02X, 0x%02X, 0x%02X: 0x%04X",
	       RegType, reg, value, index, (int) *buffer);
    } else {
	PDEBUG(5, "reg read: 0x%02X, 0x%02X,0x%02X, 0x%02X ", RegType, reg,
	       value, index);
    }
    return;
}

static void Et_RegWrite(struct usb_device *dev,
			__u16 reg,
			__u16 value,
			__u16 index, __u8 * buffer, __u16 length)
{
    int rc;
    __u16 RegType;
    __u8 *kbuffer = NULL;
    if (length > 0) {
	kbuffer = (__u8 *) kmalloc(length, GFP_KERNEL);
	memcpy(kbuffer, buffer, length);
    }
    RegType = USB_DIR_OUT | USB_TYPE_VENDOR | USB_RECIP_INTERFACE;
    rc = usb_control_msg(dev,
			 usb_sndctrlpipe(dev, 0),
			 reg,
			 RegType,
			 (__u16) value, (__u16) index, kbuffer, length,
			 TimeOut);
    if (length > 0) {
	memcpy(buffer, kbuffer, length);
	kfree(kbuffer);
    }
    if (buffer) {
	PDEBUG(5, "reg write: 0x%02X, 0x%02X, 0x%02X, 0x%02X: 0x%04X",
	       RegType, reg, value, index, (int) *buffer);
    } else {
	PDEBUG(5, "reg write: 0x%02X, 0x%02X,0x%02X, 0x%02X ", RegType,
	       reg, value, index);
    }
    return;
}
#endif

static int spca_set_interface(struct usb_device *dev, int interface,
			      int alternate)
{
    struct usb_interface *iface;
    int ret;

    iface = usb_ifnum_to_if(dev, interface);
    if (!iface) {
	warn("selecting invalid interface %d", interface);
	return -EINVAL;
    }

    /* 9.4.10 says devices don't need this, if the interface
       only has one alternate setting */
    if (iface->num_altsetting == 1) {
	dbg("ignoring set_interface for dev %d, iface %d, alt %d",
	    dev->devnum, interface, alternate);
	return 0;
    }

    if ((ret = usb_control_msg(dev, usb_sndctrlpipe(dev, 0),
			       USB_REQ_SET_INTERFACE, USB_RECIP_INTERFACE,
			       alternate, interface, NULL, 0,
			       TimeOut * 5)) < 0)
	return ret;


    return 0;

}

static int spca50x_reg_write(struct usb_device *dev,
			     __u16 reg, __u16 index, __u16 value)
{
    int rc;

    rc = usb_control_msg(dev,
			 usb_sndctrlpipe(dev, 0),
			 reg,
			 USB_TYPE_VENDOR | USB_RECIP_DEVICE,
			 value, index, NULL, 0, TimeOut);

    PDEBUG(5, "reg write: 0x%02X,0x%02X:0x%02X, 0x%x", reg, index, value,
	   rc);

    if (rc < 0)
	err("reg write: error %d", rc);

    return rc;
}

static int spca50x_reg_read_with_value(struct usb_device *dev, __u16 reg,	// bRequest
				       __u16 value,	// wValue
				       __u16 index,	// wIndex
				       __u16 length)	// wLength
{
    int rc;
    unsigned char buffer[4] = { 0, 0, 0, 0 };
    /* Hope plp didn't ask for more */
    rc = usb_control_msg(dev,
			 usb_rcvctrlpipe(dev, 0),
			 reg,
			 USB_DIR_IN | USB_TYPE_VENDOR | USB_RECIP_DEVICE,
			 (__u16) value, (__u16) index, buffer, length,
			 TimeOut);

    PDEBUG(5, "reg read: 0x%02X,0x%02X:0x%04X", reg, index,
	   *(int *) &buffer[0]);

    if (rc < 0) {
	err("reg read: error %d", rc);
	return rc;
    } else {
	return *(int *) &buffer[0];
    }
}

/* returns: negative is error, pos or zero is data */
static int spca50x_reg_read(struct usb_device *dev, __u16 reg,	// bRequest
			    __u16 index,	// wIndex
			    __u16 length)	// wLength
{
    return spca50x_reg_read_with_value(dev, reg, 0, index, length);
}

/*
 * Simple function to wait for a given 8-bit value to be returned from
 * a spca50x_reg_read call.
 * Returns: negative is error or timeout, zero is success.
 */
static int spca50x_reg_readwait(struct usb_device *dev,
				__u16 reg, __u16 index, __u16 value)
{
    int count = 0;
    int result = 0;

    while (count < 20) {
	result = spca50x_reg_read(dev, reg, index, 1);
	if (result == value)
	    return 0;

	wait_ms(50);

	count++;
    }

    PDEBUG(2, "spca50x_reg_readwait failed");

    return -EIO;
}
static int spca50x_write_vector(struct usb_spca50x *spca50x,
				__u16 data[][3])
{
    struct usb_device *dev = spca50x->dev;
    int err_code;

    int I = 0;
    while ((data[I][0]) != (__u16) 0 || (data[I][1]) != (__u16) 0
	   || (data[I][2]) != (__u16) 0) {
	err_code =
	    spca50x_reg_write(dev, data[I][0], (__u16) (data[I][2]),
			      (__u16) (data[I][1]));
	if (err_code < 0) {
	    PDEBUG(1, "Register write failed for 0x%x,0x%x,0x%x",
		   data[I][0], data[I][1], data[I][2]);
	    return -1;
	}
	I++;
    }
    return 0;
}

static int spca50x_setup_qtable(struct usb_spca50x *spca50x,
				unsigned int request,
				unsigned int ybase,
				unsigned int cbase,
				unsigned char qtable[2][64])
{
    int i;
    int err;

    /* loop over y components */
    for (i = 0; i < 64; i++) {
	err =
	    spca50x_reg_write(spca50x->dev, request, ybase + i,
			      qtable[0][i]);
	if (err < 0) {
	    PDEBUG(2, "spca50x_reg_write failed");
	    return err;
	}
    }

    /* loop over c components */
    for (i = 0; i < 64; i++) {
	err =
	    spca50x_reg_write(spca50x->dev, request, cbase + i,
			      qtable[1][i]);
	if (err < 0) {
	    PDEBUG(2, "spca50x_reg_write failed");
	    return err;
	}
    }

    /* all ok */
    return 0;
}


#endif				/* SPCAUSB_H */
