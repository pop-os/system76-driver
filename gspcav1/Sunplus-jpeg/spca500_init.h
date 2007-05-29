/*
 * SPCA500 chip based cameras initialization data
 *
 */
#ifndef SPCA500_INIT_H
#define SPCA500_INIT_H
/* Frame packet header offsets for the spca500 */
#define SPCA500_OFFSET_PADDINGLB 2
#define SPCA500_OFFSET_PADDINGHB 3
#define SPCA500_OFFSET_MODE      4
#define SPCA500_OFFSET_IMGWIDTH  5
#define SPCA500_OFFSET_IMGHEIGHT 6
#define SPCA500_OFFSET_IMGMODE   7
#define SPCA500_OFFSET_QTBLINDEX 8
#define SPCA500_OFFSET_FRAMSEQ   9
#define SPCA500_OFFSET_CDSPINFO  10
#define SPCA500_OFFSET_GPIO      11
#define SPCA500_OFFSET_AUGPIO    12
#define SPCA500_OFFSET_DATA      16
#include "spca500.dat"
/*******************     Camera Interface   *********************/
static __u16 spca500_getbrightness(struct usb_spca50x *spca50x);
static __u16 spca500_getcontrast(struct usb_spca50x *spca50x);
static __u16 spca500_getcolors(struct usb_spca50x *spca50x);
static void spca500_setbrightness(struct usb_spca50x *spca50x);
static void spca500_setcontrast(struct usb_spca50x *spca50x);
static void spca500_setcolors(struct usb_spca50x *spca50x);
static int spca500_init(struct usb_spca50x *spca50x);
static void spca500_start(struct usb_spca50x *spca50x);
static void spca500_stopN(struct usb_spca50x *spca50x);
static void spca500_stop0(struct usb_spca50x *spca50x);
static int spca500_config(struct usb_spca50x *spca50x);
static void spca500_shutdown(struct usb_spca50x *spca50x);
static void spca500_setAutobright(struct usb_spca50x *spca50x);
static void spca500_setquality(struct usb_spca50x *spca50x);
static int spca500_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame * frame,unsigned char *cdata,int *iPix, int seqnum, int *datalength);
/****************************************************************/
static void spca500_stop0(struct usb_spca50x *spca50x){}
static void spca500_shutdown(struct usb_spca50x *spca50x){}
static void spca500_setAutobright(struct usb_spca50x *spca50x){}
static void spca500_setquality(struct usb_spca50x *spca50x){}
/****************************************************************/
static void spca500_clksmart310_init(struct usb_spca50x *spca50x);
static void spca500_reinit(struct usb_spca50x *spca50x);
static int spca500_full_reset(struct usb_spca50x *spca50x);
/****************************************************************/
static struct cam_operation fspca500 = {
 	.initialize = spca500_init,
	.configure = spca500_config,
	.start = spca500_start,
	.stopN = spca500_stopN,
	.stop0 = spca500_stop0,
	.get_bright = spca500_getbrightness,
	.set_bright = spca500_setbrightness,
	.get_contrast = spca500_getcontrast,
	.set_contrast = spca500_setcontrast,
	.get_colors = spca500_getcolors,
	.set_colors = spca500_setcolors,
	.set_autobright = spca500_setAutobright,
	.set_quality = spca500_setquality,
	.cam_shutdown = spca500_shutdown,
	.sof_detect = spca500_sofdetect,
 };
static __u16 spca500_getbrightness(struct usb_spca50x *spca50x)
{
	   spca50x->brightness = (spca50x_reg_read(spca50x->dev, 0x00, 0x8167, 1)+128) << 8;
	    
return spca50x->brightness;
}
static __u16 spca500_getcontrast(struct usb_spca50x *spca50x)
{
            spca50x->contrast = spca50x_reg_read(spca50x->dev, 0x0, 0x8168, 1) << 10;
return spca50x->contrast;
}
static __u16 spca500_getcolors(struct usb_spca50x *spca50x)
{
            spca50x->colour = spca50x_reg_read(spca50x->dev, 0x0, 0x8169, 1) << 10;
return spca50x->colour;
}
static void spca500_setbrightness(struct usb_spca50x *spca50x)
{
	  spca50x_reg_write(spca50x->dev, 0x00, 0x8167,(__u8) ((spca50x->brightness >> 8)-128));
}
static void spca500_setcontrast(struct usb_spca50x *spca50x)
{
          spca50x_reg_write(spca50x->dev, 0x00, 0x8168, (spca50x->contrast >> 10));
}
static void spca500_setcolors(struct usb_spca50x *spca50x)
{
          spca50x_reg_write(spca50x->dev, 0x00, 0x8169, (spca50x->colour >> 10));
}
static int spca500_init(struct usb_spca50x *spca50x)
{
	    /* initialisation of spca500 based cameras is deferred */
	    PDEBUG(2, "Initializing SPCA500 started");
	    if (spca50x->desc == LogitechClickSmart310) {
		spca500_clksmart310_init(spca50x);
	    } else {
		//spca500_initialise(spca50x);
	    }
	    PDEBUG(2, "Initializing SPCA500 finished");
return 0;
}
static void spca500_stopN(struct usb_spca50x *spca50x)
{
	int err;
	__u8 data = 0;
    spca50x_reg_write(spca50x->dev, 0, 0x8003, 0x00);
    /* switch to video camera mode */
    err = spca50x_reg_write(spca50x->dev, 0x00, 0x8000, 0x0004);
    spca5xxRegRead(spca50x->dev, 0, 0, 0x8000, &data, 1);
    PDEBUG(0, "Stop  SPCA500 finished reg8000 = 0x%2X",data);
}
static int spca500_config(struct usb_spca50x *spca50x)
{
   memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof(struct mwebcam));
   if( spca50x->desc != LogitechClickSmart310) {
    spca50x->mode_cam[VGA].width = 640;
    spca50x->mode_cam[VGA].height = 480;
    spca50x->mode_cam[VGA].t_palette =
	P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
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
	P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
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
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QSIF].pipe = 1023;
    spca50x->mode_cam[QSIF].method = 1;
    spca50x->mode_cam[QSIF].mode = 1;
    } else {
    spca50x->mode_cam[SIF].width = 352;
    spca50x->mode_cam[SIF].height = 288;
    spca50x->mode_cam[SIF].t_palette =
	P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[SIF].pipe = 1023;
    spca50x->mode_cam[SIF].method = 0;
    spca50x->mode_cam[SIF].mode = 0;
    
    spca50x->mode_cam[CIF].width = 320;
    spca50x->mode_cam[CIF].height = 240;
    spca50x->mode_cam[CIF].t_palette =
	P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[CIF].pipe = 1023;
    spca50x->mode_cam[CIF].method = 1;
    spca50x->mode_cam[CIF].mode = 0;
    
    spca50x->mode_cam[QPAL].width = 192;
    spca50x->mode_cam[QPAL].height = 144;
    spca50x->mode_cam[QPAL].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QPAL].pipe = 1023;
    spca50x->mode_cam[QPAL].method = 1;
    spca50x->mode_cam[QPAL].mode = 0;
    
    spca50x->mode_cam[QSIF].width = 176;
    spca50x->mode_cam[QSIF].height = 144;
    spca50x->mode_cam[QSIF].t_palette =
	P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QSIF].pipe = 1023;
    spca50x->mode_cam[QSIF].method = 0;
    spca50x->mode_cam[QSIF].mode = 1;
    }
    spca50x->qindex = 5;
  return 0;
}
/***************************************************************************/
static void spca500_ping310(struct usb_spca50x *spca50x)
{
    __u8 Data[2] = { 0, 0 };
    spca5xxRegRead(spca50x->dev, 0, 0, 0x0d04, Data, 2);
    PDEBUG(5, "ClickSmart310 ping 0x0d04 0x%02X  0x%02X ", Data[0],
	   Data[1]);
}
static int spca500_synch310(struct usb_spca50x *spca50x)
{
/* Synchro the Bridge with sensor */
/* Maybe that will work on all spca500 chip */
/* because i only own a clicksmart310 try for that chip */
/* using spca50x_set_packet_size() cause an Ooops here */
/* usb_set_interface from kernel 2.6.x clear all the urb stuff */
/* up-port the same feature as in 2.4.x kernel */

    __u8 Data;


    if (spca_set_interface(spca50x->dev, spca50x->iface, 0) < 0) {
	err("Set packet size: set interface error");
	goto error;
    }
    spca500_ping310(spca50x);

    spca5xxRegRead(spca50x->dev, 0, 0, 0x0d00, &Data, 1);

    /* need alt setting here */
    PDEBUG(5, "ClickSmart310 sync pipe %d altsetting %d ",
	   spca50x->pipe_size, spca50x->alt);
    /* Windoze use pipe with altsetting 6 why 7 here */
    if (spca_set_interface(spca50x->dev, spca50x->iface, spca50x->alt) < 0) {
	err("Set packet size: set interface error");

	goto error;

    }

    return 0;
  error:

    return -EBUSY;
}

static void spca500_clksmart310_init(struct usb_spca50x *spca50x)
{
    __u8 Data[2] = { 0, 0 };
    spca5xxRegRead(spca50x->dev, 0, 0, 0x0d05, Data, 2);
    PDEBUG(5, "ClickSmart310 init 0x0d05 0x%02X  0x%02X ", Data[0],
	   Data[1]);
    spca50x_reg_write(spca50x->dev, 0x00, 0x8167, 0x5a);
    spca500_ping310(spca50x);

    spca50x_reg_write(spca50x->dev, 0x00, 0x8168, 0x22);
    spca50x_reg_write(spca50x->dev, 0x00, 0x816a, 0xc0);
    spca50x_reg_write(spca50x->dev, 0x00, 0x816b, 0x0b);
    spca50x_reg_write(spca50x->dev, 0x00, 0x8169, 0x25);
    spca50x_reg_write(spca50x->dev, 0x00, 0x8157, 0x5b);
    spca50x_reg_write(spca50x->dev, 0x00, 0x8158, 0x5b);
    spca50x_reg_write(spca50x->dev, 0x00, 0x813f, 0x03);
    spca50x_reg_write(spca50x->dev, 0x00, 0x8151, 0x4a);
    spca50x_reg_write(spca50x->dev, 0x00, 0x8153, 0x78);
    spca50x_reg_write(spca50x->dev, 0x00, 0x0d01, 0x04);	//00 for adjust shutter
    spca50x_reg_write(spca50x->dev, 0x00, 0x0d02, 0x01);
    spca50x_reg_write(spca50x->dev, 0x00, 0x8169, 0x25);
    spca50x_reg_write(spca50x->dev, 0x00, 0x0d01, 0x02);
}

static void spca500_reinit(struct usb_spca50x *spca50x)
{
    int err;
    __u8 Data;

    // some unknow command from Aiptek pocket dv and family300

    spca50x_reg_write(spca50x->dev, 0x00, 0x0d01, 0x01);
    spca50x_reg_write(spca50x->dev, 0x00, 0x0d03, 0x00);
    spca50x_reg_write(spca50x->dev, 0x00, 0x0d02, 0x01);

    /* enable drop packet */
    spca50x_reg_write(spca50x->dev, 0x00, 0x850a, 0x0001);

    err =
	spca50x_setup_qtable(spca50x, 0x00, 0x8800, 0x8840,
			     qtable_pocketdv);
    if (err < 0) {
	PDEBUG(2, "spca50x_setup_qtable failed on init");
    }
    /* set qtable index */
    spca50x_reg_write(spca50x->dev, 0x00, 0x8880, 2);
    /* family cam Quicksmart stuff */
    spca50x_reg_write(spca50x->dev, 0x00, 0x800a, 0x00);
    //Set agc transfer: synced inbetween frames
    spca50x_reg_write(spca50x->dev, 0x00, 0x820f, 0x01);
    //Init SDRAM - needed for SDRAM access
    spca50x_reg_write(spca50x->dev, 0x00, 0x870a, 0x04);
    /*Start init sequence or stream */

    spca50x_reg_write(spca50x->dev, 0, 0x8003, 0x00);
    /* switch to video camera mode */
    err = spca50x_reg_write(spca50x->dev, 0x00, 0x8000, 0x0004);
    wait_ms(2000);
    if (spca50x_reg_readwait(spca50x->dev, 0, 0x8000, 0x44) != 0)

	spca5xxRegRead(spca50x->dev, 0, 0, 0x816b, &Data, 1);
    spca50x_reg_write(spca50x->dev, 0x00, 0x816b, Data);

}
static void spca500_setmode(struct usb_spca50x *spca50x , __u8 xmult, __u8 ymult)
{
	/* set x multiplier */
	spca50x_reg_write(spca50x->dev, 0, 0x8001,xmult);

	/* set y multiplier */
	spca50x_reg_write(spca50x->dev, 0, 0x8002,ymult);

	/* use compressed mode, VGA, with mode specific subsample */
	spca50x_reg_write(spca50x->dev, 0, 0x8003,spca50x->mode << 4);
}
static void spca500_start(struct usb_spca50x *spca50x)
{

    int err;
    __u8 Data;
    __u8 xmult, ymult;
    
   if( spca50x->desc == LogitechClickSmart310){
   	xmult = 0x16;
	ymult = 0x12;
   } else {
        xmult = 0x28;
	ymult = 0x1e;
   }
    /* is there a sensor here ? */
    spca5xxRegRead(spca50x->dev, 0, 0, 0x8a04, &Data, 1);
    PDEBUG(0, "Spca500 Sensor Address  0x%02X ", Data);
PDEBUG(0, "Spca500 mode %d ,Xmult 0x%02X,  Ymult  0x%02X ", spca50x->mode,xmult,ymult);
    /* setup qtable */
    switch (spca50x->desc) {
    case LogitechClickSmart310:
	 spca500_setmode(spca50x,xmult,ymult);
	/* enable drop packet */
	if ((err =
	     spca50x_reg_write(spca50x->dev, 0x00, 0x850a, 0x0001)) < 0) {
	    PDEBUG(2, "failed to enable drop packet");

	}
	err = spca50x_reg_write(spca50x->dev, 0x00, 0x8880, 3);
	if (err < 0) {
	    PDEBUG(2, "spca50x_reg_write failed");

	}
	err = spca50x_setup_qtable(spca50x,
				   0x00, 0x8800, 0x8840,
				   qtable_creative_pccam);
	if (err < 0) {
	    PDEBUG(2, "spca50x_setup_qtable failed");

	}
	//Init SDRAM - needed for SDRAM access
	spca50x_reg_write(spca50x->dev, 0x00, 0x870a, 0x04);



	/* switch to video camera mode */
	err = spca50x_reg_write(spca50x->dev, 0x00, 0x8000, 0x0004);
	if (err < 0) {
	    PDEBUG(2, "spca50x_reg_write camera mode failed");

	}
	wait_ms(500);
	if (spca50x_reg_readwait(spca50x->dev, 0, 0x8000, 0x44) != 0) {
	    PDEBUG(2, "spca50x_reg_readwait() failed");

	}

	spca5xxRegRead(spca50x->dev, 0, 0, 0x816b, &Data, 1);
	spca50x_reg_write(spca50x->dev, 0x00, 0x816b, Data);

	err = spca500_synch310(spca50x);

	spca50x_write_vector(spca50x, spca500_visual_defaults);
 spca500_setmode(spca50x,xmult,ymult);
	/* enable drop packet */
	if ((err =
	     spca50x_reg_write(spca50x->dev, 0x00, 0x850a, 0x0001)) < 0) {
	    PDEBUG(2, "failed to enable drop packet");

	}
	err = spca50x_reg_write(spca50x->dev, 0x00, 0x8880, 3);
	if (err < 0) {
	    PDEBUG(2, "spca50x_reg_write failed");

	}
	err = spca50x_setup_qtable(spca50x,
				   0x00, 0x8800, 0x8840,
				   qtable_creative_pccam);
	if (err < 0) {
	    PDEBUG(2, "spca50x_setup_qtable failed");

	}
	//Init SDRAM - needed for SDRAM access
	spca50x_reg_write(spca50x->dev, 0x00, 0x870a, 0x04);


	/* switch to video camera mode */
	err = spca50x_reg_write(spca50x->dev, 0x00, 0x8000, 0x0004);
	if (err < 0) {
	    PDEBUG(2, "spca50x_reg_write camera mode failed");

	}

	if (spca50x_reg_readwait(spca50x->dev, 0, 0x8000, 0x44) != 0) {
	    PDEBUG(2, "spca50x_reg_readwait() failed");

	}

	spca5xxRegRead(spca50x->dev, 0, 0, 0x816b, &Data, 1);
	spca50x_reg_write(spca50x->dev, 0x00, 0x816b, Data);

	break;

    case CreativePCCam300:	/* Creative PC-CAM 300 640x480 CCD */
    case IntelPocketPCCamera:	/* FIXME: Temporary fix for Intel Pocket PC Camera - NWG (Sat 29th March 2003) */

	/* do a full reset */
	if ((err = spca500_full_reset(spca50x)) < 0) {
	    PDEBUG(2, "spca500_full_reset failed");

	}
	
	/* enable drop packet */
	if ((err =
	     spca50x_reg_write(spca50x->dev, 0x00, 0x850a, 0x0001)) < 0) {
	    PDEBUG(2, "failed to enable drop packet");

	}
	err = spca50x_reg_write(spca50x->dev, 0x00, 0x8880, 3);
	if (err < 0) {
	    PDEBUG(2, "spca50x_reg_write failed");

	}
	err = spca50x_setup_qtable(spca50x,
				   0x00, 0x8800, 0x8840,
				   qtable_creative_pccam);
	if (err < 0) {
	    PDEBUG(2, "spca50x_setup_qtable failed");

	}
 spca500_setmode(spca50x,xmult,ymult);
	spca50x_reg_write(spca50x->dev, 0x20, 0x0001, 0x0004);

	/* switch to video camera mode */
	err = spca50x_reg_write(spca50x->dev, 0x00, 0x8000, 0x0004);
	if (err < 0) {
	    PDEBUG(2, "spca50x_reg_write camera mode failed");

	}

	if (spca50x_reg_readwait(spca50x->dev, 0, 0x8000, 0x44) != 0) {
	    PDEBUG(2, "spca50x_reg_readwait() failed");

	}

	spca5xxRegRead(spca50x->dev, 0, 0, 0x816b, &Data, 1);
	spca50x_reg_write(spca50x->dev, 0x00, 0x816b, Data);

	//spca50x_write_vector(spca50x, spca500_visual_defaults);

	break;
    case KodakEZ200:		/* Kodak EZ200 */

	/* do a full reset */
	if ((err = spca500_full_reset(spca50x)) < 0) {
	    PDEBUG(2, "spca500_full_reset failed");

	}
	/* enable drop packet */
	if ((err =
	     spca50x_reg_write(spca50x->dev, 0x00, 0x850a, 0x0001)) < 0) {
	    PDEBUG(2, "failed to enable drop packet");

	}
	err = spca50x_reg_write(spca50x->dev, 0x00, 0x8880, 0);
	if (err < 0) {
	    PDEBUG(2, "spca50x_reg_write failed");

	}
	err = spca50x_setup_qtable(spca50x,
				   0x00, 0x8800, 0x8840,
				   qtable_kodak_ez200);
	if (err < 0) {
	    PDEBUG(2, "spca50x_setup_qtable failed");

	}
	 spca500_setmode(spca50x,xmult,ymult);
	
	spca50x_reg_write(spca50x->dev, 0x20, 0x0001, 0x0004);

	/* switch to video camera mode */
	err = spca50x_reg_write(spca50x->dev, 0x00, 0x8000, 0x0004);
	if (err < 0) {
	    PDEBUG(2, "spca50x_reg_write camera mode failed");

	}

	if (spca50x_reg_readwait(spca50x->dev, 0, 0x8000, 0x44) != 0) {
	    PDEBUG(2, "spca50x_reg_readwait() failed");

	}

	spca5xxRegRead(spca50x->dev, 0, 0, 0x816b, &Data, 1);
	spca50x_reg_write(spca50x->dev, 0x00, 0x816b, Data);

	//spca50x_write_vector(spca50x, spca500_visual_defaults);

	break;

    case BenqDC1016:
    case DLinkDSC350:		/* FamilyCam 300 */
    case AiptekPocketDV:	/* Aiptek PocketDV */
    case Gsmartmini:		/*Mustek Gsmart Mini */
    case MustekGsmart300:	// Mustek Gsmart 300
    case PalmPixDC85:
    case Optimedia:
    case ToptroIndus:
    case AgfaCl20:

	spca500_reinit(spca50x);
	spca50x_reg_write(spca50x->dev, 0x00, 0x0d01, 0x01);
	/* enable drop packet */
	spca50x_reg_write(spca50x->dev, 0x00, 0x850a, 0x0001);

	err = spca50x_setup_qtable(spca50x,
				   0x00, 0x8800, 0x8840, qtable_pocketdv);
	if (err < 0) {
	    PDEBUG(2, "spca50x_setup_qtable failed");

	}
	spca50x_reg_write(spca50x->dev, 0x00, 0x8880, 2);

	/* familycam Quicksmart pocketDV stuff */
	spca50x_reg_write(spca50x->dev, 0x00, 0x800a, 0x00);
	//Set agc transfer: synced inbetween frames
	spca50x_reg_write(spca50x->dev, 0x00, 0x820f, 0x01);
	//Init SDRAM - needed for SDRAM access
	spca50x_reg_write(spca50x->dev, 0x00, 0x870a, 0x04);

 spca500_setmode(spca50x,xmult,ymult);
	/* switch to video camera mode */
	err = spca50x_reg_write(spca50x->dev, 0x00, 0x8000, 0x0004);
	
	spca50x_reg_readwait(spca50x->dev, 0, 0x8000, 0x44);

	spca5xxRegRead(spca50x->dev, 0, 0, 0x816b, &Data, 1);
	spca50x_reg_write(spca50x->dev, 0x00, 0x816b, Data);

	break;
    case LogitechTraveler:
    case LogitechClickSmart510:
	{

	    spca50x_reg_write(spca50x->dev, 0x02, 0x00, 0x00);
	    /* enable drop packet */
	    if ((err =
		 spca50x_reg_write(spca50x->dev, 0x00, 0x850a,
				   0x0001)) < 0) {
		PDEBUG(2, "failed to enable drop packet");

	    }

	    err = spca50x_setup_qtable(spca50x,
				       0x00, 0x8800,
				       0x8840, qtable_creative_pccam);
	    if (err < 0) {
		PDEBUG(2, "spca50x_setup_qtable failed");

	    }
	    err = spca50x_reg_write(spca50x->dev, 0x00, 0x8880, 3);
	    if (err < 0) {
		PDEBUG(2, "spca50x_reg_write failed");

	    }
	    spca50x_reg_write(spca50x->dev, 0x00, 0x800a, 0x00);
	    //Init SDRAM - needed for SDRAM access
	    spca50x_reg_write(spca50x->dev, 0x00, 0x870a, 0x04);
	    
	     spca500_setmode(spca50x,xmult,ymult);
	     
	    /* switch to video camera mode */
	    err = spca50x_reg_write(spca50x->dev, 0x00, 0x8000, 0x0004);
	    spca50x_reg_readwait(spca50x->dev, 0, 0x8000, 0x44);
	    
	    spca5xxRegRead(spca50x->dev, 0, 0, 0x816b, &Data, 1);
	    spca50x_reg_write(spca50x->dev, 0x00, 0x816b, Data);
	    spca50x_write_vector(spca50x, Clicksmart510_defaults);
	}

	break;

    default:
    PDEBUG(0, "UNKNOW spca500 WEBCAM  MODEL !! ");
     break;
    }
}

static int spca500_full_reset(struct usb_spca50x *spca50x)
{
    int err;

    /* send the reset command */
    err = spca50x_reg_write(spca50x->dev, 0xe0, 0x0001, 0x0000);
    if (err < 0) {
	return err;
    }

    /* wait for the reset to complete */
    err = spca50x_reg_readwait(spca50x->dev, 0x06, 0x0000, 0x0000);
    if (err < 0) {
	return err;
    }
    if ((err =
	     spca50x_reg_write(spca50x->dev, 0xe0, 0x0000, 0x0000)) < 0) {
	    PDEBUG(2, "spca50x_reg_write() failed");
	    return err;
	}
	if ((err = spca50x_reg_readwait(spca50x->dev, 0x06, 0, 0)) < 0) {
	    PDEBUG(2, "spca50x_reg_readwait() failed");
	    return err;
	}
    /* all ok */
    return 0;
}
static int spca500_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength)
{
		if (cdata[0] == SPCA50X_SEQUENCE_DROP) {
		    if (cdata[1] == 0x01) {
		    *iPix = SPCA500_OFFSET_DATA;
		    *datalength -= *iPix;
			return 0;
		    } else {
			/* drop packet */
			return -1;
		    }
		} else {
		*iPix = 1;
		*datalength -= *iPix;
		        return (seqnum+1);
		}
}



#endif				/* SPCA500_INIT_H */
