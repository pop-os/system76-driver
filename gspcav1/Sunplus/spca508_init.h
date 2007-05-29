/* 
 * SPCA508 chip based cameras initialization data
 *
 */
#ifndef SPCA508_INIT_H
#define SPCA508_INIT_H

/* Frame packet header offsets for the spca508 */
#define SPCA508_OFFSET_TYPE 1
#define SPCA508_OFFSET_COMPRESS 2
#define SPCA508_OFFSET_FRAMSEQ 8
#define SPCA508_OFFSET_WIN1LUM 11
#define SPCA508_OFFSET_DATA 37

#define SPCA508_SNAPBIT 0x20
#define SPCA508_SNAPCTRL 0x40
/*************** I2c ****************/
#define SPCA508_INDEX_I2C_BASE 0x8800

#include "spca508.dat"
/*******************     Camera Interface   ***********************/
static __u16 spca508_getbrightness(struct usb_spca50x *spca50x);
static __u16 spca508_getcontrast(struct usb_spca50x *spca50x);
static __u16 spca508_getcolors(struct usb_spca50x *spca50x);
static void spca508_setbrightness(struct usb_spca50x *spca50x);
static void spca508_setcontrast(struct usb_spca50x *spca50x);
static void spca508_setcolors(struct usb_spca50x *spca50x);
static int spca508_init(struct usb_spca50x *spca50x);
static void spca508_start(struct usb_spca50x *spca50x);
static void spca508_stopN(struct usb_spca50x *spca50x);
static void spca508_stop0(struct usb_spca50x *spca50x);
static int spca508_config(struct usb_spca50x *spca50x);
static void spca508_shutdown(struct usb_spca50x *spca50x);
static void spca508_setAutobright(struct usb_spca50x *spca50x);
static void spca508_setquality(struct usb_spca50x *spca50x);
static int spca508_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum,int *datalength);
/******************************************************************/
static void spca508_stop0(struct usb_spca50x *spca50x){}
static void spca508_shutdown(struct usb_spca50x *spca50x){}
static void spca508_setAutobright(struct usb_spca50x *spca50x){}
static void spca508_setquality(struct usb_spca50x *spca50x){}
static void spca508_setcontrast(struct usb_spca50x *spca50x){}
static void spca508_setcolors(struct usb_spca50x *spca50x){}
/*****************************************************************/
static struct cam_operation fspca508 = {
 	.initialize = spca508_init,
	.configure = spca508_config,
	.start = spca508_start,
	.stopN = spca508_stopN,
	.stop0 = spca508_stop0,
	.get_bright = spca508_getbrightness,
	.set_bright = spca508_setbrightness,
	.get_contrast = spca508_getcontrast,
	.set_contrast = spca508_setcontrast,
	.get_colors = spca508_getcolors,
	.set_colors = spca508_setcolors,
	.set_autobright = spca508_setAutobright,
	.set_quality = spca508_setquality,
	.cam_shutdown = spca508_shutdown,
	.sof_detect = spca508_sofdetect,
 };
static __u16 spca508_getbrightness(struct usb_spca50x *spca50x)
{
__u8 brightness;
brightness = spca50x_reg_read(spca50x->dev, 0, 0x8651, 1);
	spca50x->brightness = brightness << 8;
return spca50x->brightness;
}
static __u16 spca508_getcontrast(struct usb_spca50x *spca50x)
{
return spca50x->contrast;
}
static __u16 spca508_getcolors(struct usb_spca50x *spca50x)
{
return spca50x->colour;
}
static void spca508_setbrightness(struct usb_spca50x *spca50x)
{
__u8 brightness = spca50x->brightness >> 8;
/* MX seem contrast */
            spca50x_reg_write(spca50x->dev, 0, 0x8651, brightness);
	    spca50x_reg_write(spca50x->dev, 0, 0x8652, brightness);
	    spca50x_reg_write(spca50x->dev, 0, 0x8653, brightness);
	    spca50x_reg_write(spca50x->dev, 0, 0x8654, brightness);
}

static int spca508_init(struct usb_spca50x *spca50x)
{
      spca50x_write_vector(spca50x, spca508_open_data);
      return 0;
}
static void spca508_start(struct usb_spca50x *spca50x)
{
int err_code = 0;
        spca50x_reg_write(spca50x->dev, 0, 0x8500, spca50x->mode);	// mode
	switch (spca50x->mode){
	case 0:
	case 1:
	spca50x_reg_write(spca50x->dev, 0, 0x8700, 0x28);	// clock
	break;
	case 2:
	case 3:
	spca50x_reg_write(spca50x->dev, 0, 0x8700, 0x23);	// clock
	break;
	default:
	spca50x_reg_write(spca50x->dev, 0, 0x8700, 0x28);	// clock
	break;
	}
    err_code = spca50x_reg_write(spca50x->dev, 0, 0x8112, 0x10 | 0x20);
}
static void spca508_stopN(struct usb_spca50x *spca50x)
{
 // Video ISO disable, Video Drop Packet enable:
	    spca50x_reg_write(spca50x->dev, 0, 0x8112, 0x20);
}

static int spca508_config(struct usb_spca50x *spca50x)
{
    struct usb_device *dev = spca50x->dev;
    int data1, data2;

    // Read frm global register the USB product and vendor IDs, just to
    // prove that we can communicate with the device.  This works, which
    // confirms at we are communicating properly and that the device
    // is a 508.
    data1 = spca50x_reg_read(dev, 0, 0x8104, 1);
    if (data1 < 0)
	PDEBUG(1, "Error reading USB Vendor ID from Global register");
    data2 = spca50x_reg_read(dev, 0, 0x8105, 1);
    if (data2 < 0)
	PDEBUG(1, "Error reading USB Vendor ID from Global register");
    PDEBUG(1, "Read from GLOBAL: USB Vendor ID 0x%02x%02x", data2, data1);

    data1 = spca50x_reg_read(dev, 0, 0x8106, 1);
    if (data1 < 0)
	PDEBUG(1, "Error reading USB Product ID from Global register");
    data2 = spca50x_reg_read(dev, 0, 0x8107, 1);
    if (data2 < 0)
	PDEBUG(1, "Error reading USB Product ID from Global register");
    PDEBUG(1, "Read from GLOBAL: USB Product ID 0x%02x%02x", data2, data1);

    data1 = spca50x_reg_read(dev, 0, 0x8621, 1);
    if (data1 < 0)
	PDEBUG(1,
	       "Error reading Window 1 Average Luminance from Global register");
    PDEBUG(1, "Read from GLOBAL: Window 1 average luminance %3d", data1);
   
       memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof(struct mwebcam));
    spca50x->mode_cam[SIF].width = 352;
    spca50x->mode_cam[SIF].height = 288;
    spca50x->mode_cam[SIF].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[SIF].pipe = 1023;
    spca50x->mode_cam[SIF].method = 0;
    spca50x->mode_cam[SIF].mode = 0;
    spca50x->mode_cam[CIF].width = 320;
    spca50x->mode_cam[CIF].height = 240;
    spca50x->mode_cam[CIF].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[CIF].pipe = 1023;
    spca50x->mode_cam[CIF].method = 0;
    spca50x->mode_cam[CIF].mode = 1;
    spca50x->mode_cam[QPAL].width = 192;
    spca50x->mode_cam[QPAL].height = 144;
    spca50x->mode_cam[QPAL].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QPAL].pipe = 1023;
    spca50x->mode_cam[QPAL].method = 1;
    spca50x->mode_cam[QPAL].mode = 1;
    spca50x->mode_cam[QSIF].width = 176;
    spca50x->mode_cam[QSIF].height = 144;
    spca50x->mode_cam[QSIF].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QSIF].pipe = 1023;
    spca50x->mode_cam[QSIF].method = 0;
    spca50x->mode_cam[QSIF].mode = 2;
    spca50x->mode_cam[QCIF].width = 160;
    spca50x->mode_cam[QCIF].height = 120;
    spca50x->mode_cam[QCIF].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QCIF].pipe = 1023;
    spca50x->mode_cam[QCIF].method = 0;
    spca50x->mode_cam[QCIF].mode = 3;
    
       switch (spca50x->desc) {
    case ViewQuestVQ110:
	{
	    if (spca50x_write_vector(spca50x, spca508_init_data))
		return -1;
	    break;
	}
    case MicroInnovationIC200:
    case IntelEasyPCCamera:
	{
	    if (spca50x_write_vector(spca50x, spca508cs110_init_data))
		return -1;
	    break;
	}
    case HamaUSBSightcam:
	{
	    if (spca50x_write_vector(spca50x, spca508_sightcam_init_data))
		return -1;
	    break;
	}
    case HamaUSBSightcam2:
	{
	    if (spca50x_write_vector(spca50x, spca508_sightcam2_init_data))
		return -1;
	    break;
	}
    case CreativeVista:
	{
	    if (spca50x_write_vector(spca50x, spca508_vista_init_data))
		return -1;
	    break;
	}
    default:
	return -1;
    }
    return 0;			// success     
}
static int spca508_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum,int *datalength)
{
           switch (cdata[0]){
	   case 0:
	        *iPix = SPCA508_OFFSET_DATA;
		*datalength -= *iPix;
	   	return 0;
	   case SPCA50X_SEQUENCE_DROP:
	   	return -1;
	   default:
	   	*iPix = 1;
		*datalength -= *iPix;
	   	return seqnum+1 ;
           }
}
#endif				/* SPCA508_INIT_H */
