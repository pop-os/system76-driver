/* 
 * SPCA501 chip based cameras initialization data
 *
 */
#ifndef SPCA501_INIT_H
#define SPCA501_INIT_H

/*
 * Data to initialize a SPCA501. From a capture file provided by Bill Roehl
 * With SPCA501 chip description
 */

#define CCDSP_SET		// set CCDSP parameters
#define TG_SET			// set time generator set
#undef DSPWIN_SET		// set DSP windows parameters
#undef ALTER_GAMA		// Set alternate set to YUV transform coeffs.
#define SPCA501_SNAPBIT 0x80
#define SPCA501_SNAPCTRL 0x10
/* Frame packet header offsets for the spca501 */
#define SPCA501_OFFSET_GPIO   1
#define SPCA501_OFFSET_TYPE   2
#define SPCA501_OFFSET_TURN3A 3
#define SPCA501_OFFSET_FRAMSEQ 4
#define SPCA501_OFFSET_COMPRESS 5
#define SPCA501_OFFSET_QUANT 6
#define SPCA501_OFFSET_QUANT2 7
#define SPCA501_OFFSET_DATA 8

#define SPCA501_PROP_COMP_ENABLE(d) ( (d) & 1 )
#define SPCA501_PROP_SNAP(d) ( (d) & 0x40 )
#define SPCA501_PROP_SNAP_CTRL(d) ( (d) & 0x10)
#define SPCA501_PROP_COMP_THRESH(d) ( ((d) & 0xE ) >> 1)
#define SPCA501_PROP_COMP_QUANT(d) ( ((d) & 0x70 ) >> 4)

/* SPCA501 CCDSP control */
#define SPCA501_REG_CCDSP 0x1
/* SPCA501 control/status registers */
#define SPCA501_REG_CTLRL 0x2

//registers for color correction and YUV transformation
#define SPCA501_A11 0x08
#define SPCA501_A12 0x09
#define SPCA501_A13 0x0A
#define SPCA501_A21 0x0B
#define SPCA501_A22 0x0C
#define SPCA501_A23 0x0D
#define SPCA501_A31 0x0E
#define SPCA501_A32 0x0F
#define SPCA501_A33 0x10

#include "spca501.dat"

/*******************     Camera Interface   ***********************/
static __u16 spca501_getbrightness(struct usb_spca50x *spca50x);
static __u16 spca501_getcontrast(struct usb_spca50x *spca50x);
static __u16 spca501_getcolors(struct usb_spca50x *spca50x);
static void spca501_setbrightness(struct usb_spca50x *spca50x);
static void spca501_setcontrast(struct usb_spca50x *spca50x);
static void spca501_setcolors(struct usb_spca50x *spca50x);
static int spca501_init(struct usb_spca50x *spca50x);
static void spca501_start(struct usb_spca50x *spca50x);
static void spca501_stopN(struct usb_spca50x *spca50x);
static void spca501_stop0(struct usb_spca50x *spca50x);
static int spca501_config(struct usb_spca50x *spca50x);
static void spca501_shutdown(struct usb_spca50x *spca50x);
static void spca501_setAutobright(struct usb_spca50x *spca50x);
static void spca501_setquality(struct usb_spca50x *spca50x);
static int spca501_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum,int *datalength);
/******************************************************************/
static void spca501_stop0(struct usb_spca50x *spca50x){}
static void spca501_setAutobright(struct usb_spca50x *spca50x){}
static void spca501_setquality(struct usb_spca50x *spca50x){}
/*****************************************************************/
static struct cam_operation fspca501 = {
 	.initialize = spca501_init,
	.configure = spca501_config,
	.start = spca501_start,
	.stopN = spca501_stopN,
	.stop0 = spca501_stop0,
	.get_bright = spca501_getbrightness,
	.set_bright = spca501_setbrightness,
	.get_contrast = spca501_getcontrast,
	.set_contrast = spca501_setcontrast,
	.get_colors = spca501_getcolors,
	.set_colors = spca501_setcolors,
	.set_autobright = spca501_setAutobright,
	.set_quality = spca501_setquality,
	.cam_shutdown = spca501_shutdown,
	.sof_detect = spca501_sofdetect,
 };
static void spca501_shutdown(struct usb_spca50x *spca50x)
{
// This maybe reset or power control
	    spca50x_reg_write(spca50x->dev, SPCA501_REG_CTLRL, 0x5, 0x0);
}
static __u16 spca501_getbrightness(struct usb_spca50x *spca50x)
{
__u16 brightness;
 brightness =
		spca50x_reg_read(spca50x->dev,SPCA501_REG_CCDSP , 0x11, 2) & 0xFF;
	    brightness <<= 8;
	    spca50x->brightness = brightness;
  return spca50x->brightness;
}
static __u16 spca501_getcontrast(struct usb_spca50x *spca50x)
{
#if 0
 __u8 byte = 0;
 	byte =(spca50x_reg_read(spca50x->dev,
						     0x00,
						     0x00,
						     1) & 0xFF) << 8;
	spca50x->contrast = byte | (spca50x_reg_read(spca50x->dev,
						     0x00,
						     0x01,
						     1) & 0xFF);
#endif
spca50x->contrast = 0xaa01;						     
PDEBUG(0, "SPCA501 Getcontrast %d",spca50x->contrast);
return spca50x->contrast;
}
static void spca501_setbrightness(struct usb_spca50x *spca50x)
{
	spca50x_reg_write(spca50x->dev, SPCA501_REG_CCDSP, 0x11,
			      spca50x->brightness >> 9);
	spca50x_reg_write(spca50x->dev, SPCA501_REG_CCDSP, 0x12,
			      spca50x->brightness >> 9);
	spca50x_reg_write(spca50x->dev, SPCA501_REG_CCDSP, 0x13,
			      spca50x->brightness >> 9);
}
static void spca501_setcontrast(struct usb_spca50x *spca50x)
{
spca50x_reg_write(spca50x->dev,0x00, 0x00,
			      (spca50x->contrast >> 8) & 0xff);
spca50x_reg_write(spca50x->dev,0x00, 0x01,
			      spca50x->contrast & 0xff);			      
}
static int spca501_init(struct usb_spca50x *spca50x)
{
	    PDEBUG(2, "Initializing SPCA501 started");
	    if (spca50x->dev->descriptor.idVendor == 0x0506
		&& spca50x->dev->descriptor.idProduct == 0x00df) {
		/* Special handling for 3com data */
		spca50x_write_vector(spca50x, spca501_3com_open_data);
	    } else if (spca50x->desc == Arowana300KCMOSCamera ||
		       spca50x->desc == SmileIntlCamera) {
		/* Arowana 300k CMOS Camera data */
		spca50x_write_vector(spca50x, spca501c_arowana_open_data);
	    } else if (spca50x->desc == MystFromOriUnknownCamera) {
		/* UnKnow  CMOS Camera data */
		spca50x_write_vector(spca50x,
				     spca501c_mysterious_init_data);
	    } else {
		/* Generic 501 open data */
		spca50x_write_vector(spca50x, spca501_open_data);
	    }
#ifdef SPCA50X_ENABLE_EXPERIMENTAL
	    spca50x->a_blue = spca50x_reg_read(spca50x->dev,
					       SPCA501_REG_CCDSP,
					       SPCA501_A11, 2) & 0xFF;
	    spca50x->a_green =
		spca50x_reg_read(spca50x->dev, SPCA501_REG_CCDSP,
				 SPCA501_A21, 2) & 0xFF;
	    spca50x->a_red =
		spca50x_reg_read(spca50x->dev, SPCA501_REG_CCDSP,
				 SPCA501_A31, 2) & 0xFF;
#endif				/* SPCA50X_ENABLE_EXPERIMENTAL */
	    PDEBUG(2, "Initializing SPCA501 finished");
return 0;
}
static void spca501_start(struct usb_spca50x *spca50x)
{
int err_code = 0;
struct usb_device *dev = spca50x->dev;
	    /* Enable ISO packet machine CTRL reg=2,
	     * index=1 bitmask=0x2 (bit ordinal 1) */
	spca50x_reg_write(dev, SPCA50X_REG_USB, 0x6, 0x94);
	switch (spca50x->mode){
	case 0: //640x480
	spca50x_reg_write(dev, SPCA50X_REG_USB, 0x7,0x004a);
	break;
	case 1: //320x240
	spca50x_reg_write(dev, SPCA50X_REG_USB, 0x7, 0x104a);
	break;
	case 2: //160x120
	spca50x_reg_write(dev, SPCA50X_REG_USB, 0x7, 0x204a);
	break;
	default:
	spca50x_reg_write(dev, SPCA50X_REG_USB, 0x7, 0x204a);
	break;
	}
	err_code = spca50x_reg_write(dev, SPCA501_REG_CTLRL,
					 (__u16) 0x1, (__u16) 0x2);
}
static void spca501_stopN(struct usb_spca50x *spca50x)
{
	    /* Disable ISO packet machine CTRL reg=2, index=1 bitmask=0x0 (bit ordinal 1) */
	    spca50x_reg_write(spca50x->dev, SPCA501_REG_CTLRL,
			      (__u16) 0x1, (__u16) 0x0);
}
static int spca501_config(struct usb_spca50x *spca50x)
{
   memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof(struct mwebcam));
    spca50x->mode_cam[VGA].width = 640;
    spca50x->mode_cam[VGA].height = 480;
    spca50x->mode_cam[VGA].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[VGA].pipe = 1023;
    spca50x->mode_cam[VGA].method = 0;
    spca50x->mode_cam[VGA].mode = 0;
    spca50x->mode_cam[PAL].width = 384;
    spca50x->mode_cam[PAL].height = 288;
    spca50x->mode_cam[PAL].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[PAL].pipe = 1023;
    spca50x->mode_cam[PAL].method = 1;
    spca50x->mode_cam[PAL].mode = 0;
    spca50x->mode_cam[SIF].width = 352;
    spca50x->mode_cam[SIF].height = 288;
    spca50x->mode_cam[SIF].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[SIF].pipe = 1023;
    spca50x->mode_cam[SIF].method = 1;
    spca50x->mode_cam[SIF].mode = 0;
    
    spca50x->mode_cam[CIF].width = 320;
    spca50x->mode_cam[CIF].height = 240;
    spca50x->mode_cam[CIF].t_palette =
        P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[CIF].pipe = 896;
    spca50x->mode_cam[CIF].method = 0;
    spca50x->mode_cam[CIF].mode = 1;
    spca50x->mode_cam[QPAL].width = 192;
    spca50x->mode_cam[QPAL].height = 144;
    spca50x->mode_cam[QPAL].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QPAL].pipe = 896;
    spca50x->mode_cam[QPAL].method = 1;
    spca50x->mode_cam[QPAL].mode = 1;
    spca50x->mode_cam[QSIF].width = 176;
    spca50x->mode_cam[QSIF].height = 144;
    spca50x->mode_cam[QSIF].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QSIF].pipe = 896;
    spca50x->mode_cam[QSIF].method = 1;
    spca50x->mode_cam[QSIF].mode = 1;
    
    spca50x->mode_cam[QCIF].width = 160;
    spca50x->mode_cam[QCIF].height = 120;
    spca50x->mode_cam[QCIF].t_palette =
        P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QCIF].pipe = 384;
    spca50x->mode_cam[QCIF].method = 0;
    spca50x->mode_cam[QCIF].mode = 2;
    
    	    if (spca50x->desc == Arowana300KCMOSCamera ||
		spca50x->desc == SmileIntlCamera) {
		/* Arowana 300k CMOS Camera data */
		if (spca50x_write_vector
		    (spca50x, spca501c_arowana_init_data))
		    goto error;
	    } else if (spca50x->desc == MystFromOriUnknownCamera) {
		/* UnKnow Ori CMOS Camera data */
		if (spca50x_write_vector
		    (spca50x, spca501c_mysterious_open_data))
		    goto error;
	    } else {
		/* generic spca501 init data */
		if (spca50x_write_vector(spca50x, spca501_init_data))
		    goto error;
	    }
return 0;
error:
return -EINVAL;
}


static __u16 spca501_getcolors(struct usb_spca50x *spca50x)
{
             spca50x->colour = (spca50x_reg_read(spca50x->dev,SPCA501_REG_CCDSP, 0x0c,
			           2) & 0xFF) << 10;
	     spca50x->hue = (spca50x_reg_read (spca50x->dev, SPCA501_REG_CCDSP, 0x13,
			  2) & 0xFF) << 8;
return spca50x->colour;
}
static void spca501_setcolors(struct usb_spca50x *spca50x)
{
             spca50x_reg_write(spca50x->dev,SPCA501_REG_CCDSP, 0x0c,
			           spca50x->colour >> 10);
}
static int spca501_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum,int *datalength)
{
	switch (cdata[0]){
	   case 0:
	   	*iPix = SPCA501_OFFSET_DATA;
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

			/* SPCA501_INIT_H */
#endif
//eof
