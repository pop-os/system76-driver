/*
 * SPCA505 chip based cameras initialization data
 *
 */
#ifndef SPCA505_INIT_H
#define SPCA505_INIT_H

#define SPCA50X_USB_CTRL 0x0 // spca505
#define SPCA50X_CUSB_ENABLE 0x1 // spca505
#define SPCA50X_REG_GLOBAL 0x3 // spca505
#define SPCA50X_GMISC0_IDSEL 0x1	// Global control device ID select spca505
#define SPCA50X_GLOBAL_MISC0 0x0	// Global control miscellaneous 0 spca505

#define SPCA50X_GLOBAL_MISC1 0x1 // 505
#define SPCA50X_GLOBAL_MISC3 0x3 // 505
#define SPCA50X_GMISC3_SAA7113RST 0x20	/* Not sure about this one spca505 */

#include "spca505.dat"
static int spca505_init(struct usb_spca50x *spca50x);
static void spca505_start(struct usb_spca50x *spca50x);
static void spca505_stopN(struct usb_spca50x *spca50x);
static void spca505_stop0(struct usb_spca50x *spca50x);
static __u16 spca505_getbrightness(struct usb_spca50x *spca50x);
static __u16 spca505_getcontrast(struct usb_spca50x *spca50x);
static __u16 spca505_getcolors(struct usb_spca50x *spca50x);
static void spca505_setbrightness(struct usb_spca50x *spca50x);
static void spca505_setcontrast(struct usb_spca50x *spca50x);
static void spca505_setcolors(struct usb_spca50x *spca50x);
static int spca505_config(struct usb_spca50x *spca50x);
static void spca505_shutdown(struct usb_spca50x *spca50x);
static void spca505_setAutobright(struct usb_spca50x *spca50x);
static void spca505_setquality(struct usb_spca50x *spca50x);
static int spca505_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength);
/***************************************************************/
static void spca505_stop0(struct usb_spca50x *spca50x){}
static void spca505_setAutobright(struct usb_spca50x *spca50x){}
static void spca505_setquality(struct usb_spca50x *spca50x){}
/**************************************************************/
static struct cam_operation fspca505 = {
 	.initialize = spca505_init,
	.configure = spca505_config,
	.start = spca505_start,
	.stopN = spca505_stopN,
	.stop0 = spca505_stop0,
	.get_bright = spca505_getbrightness,
	.set_bright = spca505_setbrightness,
	.get_contrast = spca505_getcontrast,
	.set_contrast = spca505_setcontrast,
	.get_colors = spca505_getcolors,
	.set_colors = spca505_setcolors,
	.set_autobright = spca505_setAutobright,
	.set_quality = spca505_setquality,
	.cam_shutdown = spca505_shutdown,
	.sof_detect = spca505_sofdetect,
 };
static int spca505_init(struct usb_spca50x *spca50x)
{
int err_code = 0;
	    PDEBUG(2, "Initializing SPCA505");
	    if (spca50x->desc == Nxultra) {

		spca50x_write_vector(spca50x, spca505b_open_data_ccd);

	    } else {

		spca50x_write_vector(spca50x, spca505_open_data_ccd);

	    }
	    err_code = 0;
	    err_code = spca50x_reg_read(spca50x->dev, 6, (__u16) 0x16, 2);

	    if (err_code < 0) {
		PDEBUG(1,
		       "register read failed for after vector read err = %d",
		       err_code);
		return -EIO;
	    } else {
		PDEBUG(3,
		       "After vector read returns : 0x%x should be 0x0101",
		       err_code & 0xFFFF);
	    }

	    err_code =
		spca50x_reg_write(spca50x->dev, 6, (__u16) 0x16, (__u16) 0xa);
	    if (err_code < 0) {
		PDEBUG(1, "register write failed for (6,0xa,0x16) err=%d",
		       err_code);
		return -EIO;
	    }

	    spca50x_reg_write(spca50x->dev, 5, 0xc2, 18);

return 0;
}
static void spca505_start(struct usb_spca50x *spca50x)
{
    struct usb_device *dev = spca50x->dev;
    int err_code;
	    //nessesary because without it we can see stream only once after loading module
	    //stopping usb registers Tomasz change
	    spca50x_reg_write(dev, 0x2, 0x0, 0x0);
switch(spca50x->mode){
    case 0:
    spca50x_reg_write(dev, 0x04, 0x0,
			  0);
    spca50x_reg_write(dev, 0x04, 0x06,
			  0x10);
    spca50x_reg_write(dev, 0x04, 0x07,
			  0x10);			    
    break;
    case 1:
    spca50x_reg_write(dev, 0x04, 0x0,
			  1);
    spca50x_reg_write(dev, 0x04, 0x06,
			  0x1a);
    spca50x_reg_write(dev, 0x04, 0x07,
			  0x1a);	
    break;
    case 2:
    spca50x_reg_write(dev, 0x04, 0x0,
			  2);
    spca50x_reg_write(dev, 0x04, 0x06,
			  0x1c);
    spca50x_reg_write(dev, 0x04, 0x07,
			  0x1d);	
    break;
    case 4:
    spca50x_reg_write(dev, 0x04, 0x0,
			  4);
    spca50x_reg_write(dev, 0x04, 0x06,
			  0x34);
    spca50x_reg_write(dev, 0x04, 0x07,
			  0x34);	
    break;
    case 5:
    spca50x_reg_write(dev, 0x04, 0x0,
			  5);
    spca50x_reg_write(dev, 0x04, 0x06,
			  0x40);
    spca50x_reg_write(dev, 0x04, 0x07,
			  0x40);	
    break;
    default:
     spca50x_reg_write(dev, 0x04, 0x0,
			  5);
    spca50x_reg_write(dev, 0x04, 0x06,
			  0x40);
    spca50x_reg_write(dev, 0x04, 0x07,
			  0x40);	
    break;
    }
	    /* Enable ISO packet machine - should we do this here or in ISOC init ? */
	    err_code = spca50x_reg_write(dev, SPCA50X_REG_USB,
					 SPCA50X_USB_CTRL,
					 SPCA50X_CUSB_ENABLE);

//                      spca50x_reg_write(dev, 0x5, 0x0, 0x0);
//                      spca50x_reg_write(dev, 0x5, 0x0, 0x1);
//                      spca50x_reg_write(dev, 0x5, 0x11, 0x2);
}
static void spca505_stopN(struct usb_spca50x *spca50x)
{
	    spca50x_reg_write(spca50x->dev, 0x2, 0x0, 0x0);	//Disable ISO packet machine
}
static __u16 spca505_getbrightness(struct usb_spca50x *spca50x)
{
        spca50x->brightness =
	    65535 - ((spca50x_reg_read(spca50x->dev, 5, 0x01, 1) >> 2) +
		     (spca50x_reg_read(spca50x->dev, 5, 0x0, 1) << 6));
return spca50x->brightness;
}
static __u16 spca505_getcontrast(struct usb_spca50x *spca50x)
{
spca50x->contrast = 0;
return spca50x->contrast;
}
static __u16 spca505_getcolors(struct usb_spca50x *spca50x)
{
spca50x->colour = 0;
return spca50x->colour;
}
static void spca505_setbrightness(struct usb_spca50x *spca50x)
{
    __u8 brightness = spca50x->brightness >> 8;
	    spca50x_reg_write(spca50x->dev, 5, 0x0,
			      (255 - brightness) >> 6);
	    spca50x_reg_write(spca50x->dev, 5, 0x01,
			      (255 - brightness) << 2);

}
static void spca505_setcontrast(struct usb_spca50x *spca50x)
{
}
static void spca505_setcolors(struct usb_spca50x *spca50x)
{
}
static int spca505_config(struct usb_spca50x *spca50x)
{
    memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof(struct mwebcam));
  if (spca50x->desc == Nxultra) {  
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
    }
    spca50x->mode_cam[SIF].width = 352;
    spca50x->mode_cam[SIF].height = 288;
    spca50x->mode_cam[SIF].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[SIF].pipe = 1023;
    spca50x->mode_cam[SIF].method = 0;
    spca50x->mode_cam[SIF].mode = 1;
    
    spca50x->mode_cam[CIF].width = 320;
    spca50x->mode_cam[CIF].height = 240;
    spca50x->mode_cam[CIF].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[CIF].pipe = 896;
    spca50x->mode_cam[CIF].method = 0;
    spca50x->mode_cam[CIF].mode = 2;
    
    spca50x->mode_cam[QPAL].width = 192;
    spca50x->mode_cam[QPAL].height = 144;
    spca50x->mode_cam[QPAL].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QPAL].pipe = 896;
    spca50x->mode_cam[QPAL].method = 1;
    spca50x->mode_cam[QPAL].mode = 2;
    
    spca50x->mode_cam[QSIF].width = 176;
    spca50x->mode_cam[QSIF].height = 144;
    spca50x->mode_cam[QSIF].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QSIF].pipe = 512;
    spca50x->mode_cam[QSIF].method = 0;
    spca50x->mode_cam[QSIF].mode = 4;
    
    spca50x->mode_cam[QCIF].width = 160;
    spca50x->mode_cam[QCIF].height = 120;
    spca50x->mode_cam[QCIF].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QCIF].pipe = 384;
    spca50x->mode_cam[QCIF].method = 0;
    spca50x->mode_cam[QCIF].mode = 5;
    
    	    if (spca50x->desc == Nxultra) {
		if (spca50x_write_vector(spca50x, spca505b_init_data))
		    return -EIO;
	    } else {
		if (spca50x_write_vector(spca50x, spca505_init_data))
		    return -EIO;
	    }
    return 0;
}
static void spca505_shutdown(struct usb_spca50x *spca50x)
{
	    spca50x_reg_write(spca50x->dev, 0x3, 0x3, 0x20);	// This maybe reset or power control
	    spca50x_reg_write(spca50x->dev, 0x3, 0x1, 0x0);
	    spca50x_reg_write(spca50x->dev, 0x3, 0x0, 0x1);
	    spca50x_reg_write(spca50x->dev, 0x5, 0x10, 0x1);
	    spca50x_reg_write(spca50x->dev, 0x5, 0x11, 0xF);
}
static int spca505_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength)
{
	switch (cdata[0]){
	   case 0:
	   	*iPix = SPCA50X_OFFSET_DATA;
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
#endif				/* SPCA505_INIT_H */
//eof
