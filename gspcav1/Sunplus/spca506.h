/*
 * SPCA506 chip based cameras function
 * M Xhaard 15/04/2004 based on different work Mark Taylor and others
 * and my own snoopy file on a pv-321c donate by a german compagny
 *                "Firma Frank Gmbh" from  Saarbruecken
 */
#ifndef SPCA506_INIT_H
#define SPCA506_INIT_H

#define SAA7113_bright 0x0A	// defaults 0x80
#define SAA7113_contrast 0x0B	// defaults 0x47
#define SAA7113_saturation 0x0C	//defaults 0x40
#define SAA7113_hue 0x0D	//defaults 0x00
#define SAA7113_I2C_BASE_WRITE 0x4A

/* define from v4l */
//#define VIDEO_MODE_PAL                0
//#define VIDEO_MODE_NTSC               1
//#define VIDEO_MODE_SECAM              2
//#define VIDEO_MODE_AUTO               3
/**************************     Camera interface    ************************/
static int spca506_init(struct usb_spca50x *spca50x);
static void spca506_start(struct usb_spca50x *spca50x);
static void spca506_stopN(struct usb_spca50x *spca50x);
static void spca506_stop0(struct usb_spca50x *spca50x);
static __u16 spca506_getbrightness(struct usb_spca50x *spca50x);
static __u16 spca506_getcontrast(struct usb_spca50x *spca50x);
static __u16 spca506_getcolors(struct usb_spca50x *spca50x);
static void spca506_setbrightness(struct usb_spca50x *spca50x);
static void spca506_setcontrast(struct usb_spca50x *spca50x);
static void spca506_setcolors(struct usb_spca50x *spca50x);
static int spca506_config(struct usb_spca50x *spca50x);
static void spca506_shutdown(struct usb_spca50x *spca50x);
static void spca506_setAutobright(struct usb_spca50x *spca50x);
static void spca506_setquality(struct usb_spca50x *spca50x);
static int spca506_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum,int *datalength);
/****************************************************************************/
static void spca506_stop0(struct usb_spca50x *spca50x){}
static void spca506_shutdown(struct usb_spca50x *spca50x){}
static void spca506_setAutobright(struct usb_spca50x *spca50x){}
static void spca506_setquality(struct usb_spca50x *spca50x){}
/*********************** Specific spca506 Usbgrabber ************************/
static void spca506_SetNormeInput(struct usb_spca50x *spca50x, __u16 norme,
				  __u16 channel);
static void spca506_GetNormeInput(struct usb_spca50x *spca50x,
				  __u16 * norme, __u16 * channel);
/****************************   Private     *********************************/
static void spca506_Setsize(struct usb_spca50x *spca50x, __u16 code,
			    __u16 xmult, __u16 ymult);

/****************************************************************************/
static struct cam_operation fspca506 = {
 	.initialize = spca506_init,
	.configure = spca506_config,
	.start = spca506_start,
	.stopN = spca506_stopN,
	.stop0 = spca506_stop0,
	.get_bright = spca506_getbrightness,
	.set_bright = spca506_setbrightness,
	.get_contrast = spca506_getcontrast,
	.set_contrast = spca506_setcontrast,
	.get_colors = spca506_getcolors,
	.set_colors = spca506_setcolors,
	.set_autobright = spca506_setAutobright,
	.set_quality = spca506_setquality,
	.cam_shutdown = spca506_shutdown,
	.sof_detect = spca506_sofdetect,
 };
static void spca506_Initi2c(struct usb_spca50x *spca50x)
{
    spca5xxRegWrite(spca50x->dev, 0x07, SAA7113_I2C_BASE_WRITE, 0x0004,
		    NULL, 0);
}

static void spca506_WriteI2c(struct usb_spca50x *spca50x, __u16 valeur,
			     __u16 registre)
{
    int retry = 60;
    unsigned char Data[2];
    spca5xxRegWrite(spca50x->dev, 0x07, registre, 0x0001, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x07, valeur, 0x0000, NULL, 0);
    while (retry--) {
	spca5xxRegRead(spca50x->dev, 0x07, 0, 0x0003, Data, 2);
	if ((Data[0] | Data[1]) == 0x00)
	    break;
    }
}

static int spca506_ReadI2c(struct usb_spca50x *spca50x, __u16 registre)
{
    int retry = 60;
    unsigned char Data[2];
    unsigned char value = 0;
    spca5xxRegWrite(spca50x->dev, 0x07, SAA7113_I2C_BASE_WRITE, 0x0004,
		    NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x07, registre, 0x0001, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x07, 0x01, 0x0002, NULL, 0);
    while (retry--) {
	spca5xxRegRead(spca50x->dev, 0x07, 0, 0x0003, Data, 2);
	if ((Data[0] | Data[1]) == 0x00)
	    break;
    }
    if (retry == 0)
	return -1;
    spca5xxRegRead(spca50x->dev, 0x07, 0, 0x0000, &value, 1);
    return (int) value;
}

static void spca506_SetNormeInput(struct usb_spca50x *spca50x, __u16 norme,
				  __u16 channel)
{
    __u8 setbit0 = 0x00;
    __u8 setbit1 = 0x00;
    __u8 videomask = 0x00;
    PDEBUG(3, "************ Open Set Norme  **************");
    spca506_Initi2c(spca50x);
    /* NTSC bit0 -> 1(525 l) PAL SECAM bit0 -> 0 (625 l) */
    /* Composite channel bit1 -> 1 S-video bit 1 -> 0 */
    /* and exclude SAA7113 reserved channel set default 0 otherwise */
    if (norme == VIDEO_MODE_NTSC)
	setbit0 = 0x01;
    if ((channel == 4) || (channel == 5) || (channel > 9))
	channel = 0;
    if (channel < 4)
	setbit1 = 0x02;
    videomask = (0x48 | setbit0 | setbit1);
    spca5xxRegWrite(spca50x->dev, 0x08, videomask, 0x0000, NULL, 0);
    spca506_WriteI2c(spca50x, (0xc0 | (channel & 0x0F)), 0x02);

    switch (norme) {
    case VIDEO_MODE_PAL:
	spca506_WriteI2c(spca50x, 0x03, 0x0e);	//Chrominance Control PAL BGHIV
	break;
    case VIDEO_MODE_NTSC:
	spca506_WriteI2c(spca50x, 0x33, 0x0e);	//Chrominance Control NTSC N
	break;
    case VIDEO_MODE_SECAM:
	spca506_WriteI2c(spca50x, 0x53, 0x0e);	//Chrominance Control SECAM
	break;
    default:
	spca506_WriteI2c(spca50x, 0x03, 0x0e);	//Chrominance Control PAL BGHIV
	break;
    }
    spca50x->norme = norme;
    spca50x->channel = channel;
    PDEBUG(3, "Set Video Byte to 0x%2X ", videomask);
    PDEBUG(3, "Set Norme : %d Channel %d ", norme, channel);
    PDEBUG(3, "************ Close SetNorme  **************");


}

static void spca506_GetNormeInput(struct usb_spca50x *spca50x,
				  __u16 * norme, __u16 * channel)
{

    PDEBUG(3, "************ Open Get Norme  **************");
    /* Read the register is not so good value change so
       we use your own copy in spca50x struct          */
    *norme = spca50x->norme;
    *channel = spca50x->channel;
    PDEBUG(3, "Get Norme  : %d Channel %d ", *norme, *channel);
    PDEBUG(3, "************ Close Get Norme  **************");
}

static int spca506_init(struct usb_spca50x *spca50x)
{
    PDEBUG(3, "************ Open Init spca506  **************");
    spca5xxRegWrite(spca50x->dev, 0x03, 0x00, 0x0004, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0xFF, 0x0003, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x00, 0x0000, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x1c, 0x0001, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x18, 0x0001, NULL, 0);
    /* Init on PAL and composite input0 */
    spca506_SetNormeInput(spca50x, 0, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x1c, 1, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x18, 0x0001, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x05, 0x00, 0x0000, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x05, 0xef, 0x0001, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x05, 0x00, 0x00c1, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x05, 0x00, 0x00c2, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x06, 0x18, 0x0002, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x06, 0xf5, 0x0011, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x06, 0x02, 0x0012, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x06, 0xfb, 0x0013, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x06, 0x00, 0x0014, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x06, 0xa4, 0x0051, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x06, 0x40, 0x0052, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x06, 0x71, 0x0053, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x06, 0x40, 0x0054, NULL, 0);
	/***********************************************************/
    spca5xxRegWrite(spca50x->dev, 0x03, 0x00, 0x0004, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x00, 0x0003, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x00, 0x0004, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0xFF, 0x0003, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x02, 0x00, 0x0000, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x60, 0x0000, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x18, 0x0001, NULL, 0);
    /* for a better reading mx :)      */
    /*spca506_WriteI2c(value,register) */
    spca506_Initi2c(spca50x);
    spca506_WriteI2c(spca50x, 0x08, 0x01);
    spca506_WriteI2c(spca50x, 0xc0, 0x02);	// input composite video
    spca506_WriteI2c(spca50x, 0x33, 0x03);
    spca506_WriteI2c(spca50x, 0x00, 0x04);
    spca506_WriteI2c(spca50x, 0x00, 0x05);
    spca506_WriteI2c(spca50x, 0x0d, 0x06);
    spca506_WriteI2c(spca50x, 0xf0, 0x07);
    spca506_WriteI2c(spca50x, 0x98, 0x08);
    spca506_WriteI2c(spca50x, 0x03, 0x09);
    spca506_WriteI2c(spca50x, 0x80, 0x0a);
    spca506_WriteI2c(spca50x, 0x47, 0x0b);
    spca506_WriteI2c(spca50x, 0x48, 0x0c);
    spca506_WriteI2c(spca50x, 0x00, 0x0d);
    spca506_WriteI2c(spca50x, 0x03, 0x0e);	// Chroma Pal adjust
    spca506_WriteI2c(spca50x, 0x2a, 0x0f);
    spca506_WriteI2c(spca50x, 0x00, 0x10);
    spca506_WriteI2c(spca50x, 0x0c, 0x11);
    spca506_WriteI2c(spca50x, 0xb8, 0x12);
    spca506_WriteI2c(spca50x, 0x01, 0x13);
    spca506_WriteI2c(spca50x, 0x00, 0x14);
    spca506_WriteI2c(spca50x, 0x00, 0x15);
    spca506_WriteI2c(spca50x, 0x00, 0x16);
    spca506_WriteI2c(spca50x, 0x00, 0x17);
    spca506_WriteI2c(spca50x, 0x00, 0x18);
    spca506_WriteI2c(spca50x, 0x00, 0x19);
    spca506_WriteI2c(spca50x, 0x00, 0x1a);
    spca506_WriteI2c(spca50x, 0x00, 0x1b);
    spca506_WriteI2c(spca50x, 0x00, 0x1c);
    spca506_WriteI2c(spca50x, 0x00, 0x1d);
    spca506_WriteI2c(spca50x, 0x00, 0x1e);
    spca506_WriteI2c(spca50x, 0xa1, 0x1f);
    spca506_WriteI2c(spca50x, 0x02, 0x40);
    spca506_WriteI2c(spca50x, 0xff, 0x41);
    spca506_WriteI2c(spca50x, 0xff, 0x42);
    spca506_WriteI2c(spca50x, 0xff, 0x43);
    spca506_WriteI2c(spca50x, 0xff, 0x44);
    spca506_WriteI2c(spca50x, 0xff, 0x45);
    spca506_WriteI2c(spca50x, 0xff, 0x46);
    spca506_WriteI2c(spca50x, 0xff, 0x47);
    spca506_WriteI2c(spca50x, 0xff, 0x48);
    spca506_WriteI2c(spca50x, 0xff, 0x49);
    spca506_WriteI2c(spca50x, 0xff, 0x4a);
    spca506_WriteI2c(spca50x, 0xff, 0x4b);
    spca506_WriteI2c(spca50x, 0xff, 0x4c);
    spca506_WriteI2c(spca50x, 0xff, 0x4d);
    spca506_WriteI2c(spca50x, 0xff, 0x4e);
    spca506_WriteI2c(spca50x, 0xff, 0x4f);
    spca506_WriteI2c(spca50x, 0xff, 0x50);
    spca506_WriteI2c(spca50x, 0xff, 0x51);
    spca506_WriteI2c(spca50x, 0xff, 0x52);
    spca506_WriteI2c(spca50x, 0xff, 0x53);
    spca506_WriteI2c(spca50x, 0xff, 0x54);
    spca506_WriteI2c(spca50x, 0xff, 0x55);
    spca506_WriteI2c(spca50x, 0xff, 0x56);
    spca506_WriteI2c(spca50x, 0xff, 0x57);
    spca506_WriteI2c(spca50x, 0x00, 0x58);
    spca506_WriteI2c(spca50x, 0x54, 0x59);
    spca506_WriteI2c(spca50x, 0x07, 0x5a);
    spca506_WriteI2c(spca50x, 0x83, 0x5b);
    spca506_WriteI2c(spca50x, 0x00, 0x5c);
    spca506_WriteI2c(spca50x, 0x00, 0x5d);
    spca506_WriteI2c(spca50x, 0x00, 0x5e);
    spca506_WriteI2c(spca50x, 0x00, 0x5f);
    spca506_WriteI2c(spca50x, 0x00, 0x60);
    spca506_WriteI2c(spca50x, 0x05, 0x61);
    spca506_WriteI2c(spca50x, 0x9f, 0x62);
    PDEBUG(3, "************ Close Init spca506  **************");
    return 0;
}
static void spca506_start(struct usb_spca50x *spca50x)
{
    __u16 norme = 0;
    __u16 channel = 0;
    unsigned char Data[2];
    PDEBUG(3, "************ Open Start spca506  **************");
	/***********************************************************/
    spca5xxRegWrite(spca50x->dev, 0x03, 0x00, 0x0004, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x00, 0x0003, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x00, 0x0004, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0xFF, 0x0003, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x02, 0x00, 0x0000, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x60, 0x0000, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x18, 0x0001, NULL, 0);

    /*spca506_WriteI2c(value,register) */
    spca506_Initi2c(spca50x);
    spca506_WriteI2c(spca50x, 0x08, 0x01);	//Increment Delay
    //spca506_WriteI2c(spca50x,0xc0,0x02);//Analog Input Control 1
    spca506_WriteI2c(spca50x, 0x33, 0x03);	//Analog Input Control 2
    spca506_WriteI2c(spca50x, 0x00, 0x04);	//Analog Input Control 3
    spca506_WriteI2c(spca50x, 0x00, 0x05);	//Analog Input Control 4
    spca506_WriteI2c(spca50x, 0x0d, 0x06);	//Horizontal Sync Start 0xe9-0x0d
    spca506_WriteI2c(spca50x, 0xf0, 0x07);	//Horizontal Sync Stop  0x0d-0xf0

    spca506_WriteI2c(spca50x, 0x98, 0x08);	//Sync Control
    /*                      Defaults value                       */
    spca506_WriteI2c(spca50x, 0x03, 0x09);	//Luminance Control
    spca506_WriteI2c(spca50x, 0x80, 0x0a);	//Luminance Brightness
    spca506_WriteI2c(spca50x, 0x47, 0x0b);	//Luminance Contrast
    spca506_WriteI2c(spca50x, 0x48, 0x0c);	//Chrominance Saturation
    spca506_WriteI2c(spca50x, 0x00, 0x0d);	//Chrominance Hue Control
    spca506_WriteI2c(spca50x, 0x2a, 0x0f);	//Chrominance Gain Control
	/*************************************************************/
    spca506_WriteI2c(spca50x, 0x00, 0x10);	//Format/Delay Control
    spca506_WriteI2c(spca50x, 0x0c, 0x11);	//Output Control 1
    spca506_WriteI2c(spca50x, 0xb8, 0x12);	//Output Control 2
    spca506_WriteI2c(spca50x, 0x01, 0x13);	//Output Control 3
    spca506_WriteI2c(spca50x, 0x00, 0x14);	//reserved
    spca506_WriteI2c(spca50x, 0x00, 0x15);	//VGATE START
    spca506_WriteI2c(spca50x, 0x00, 0x16);	//VGATE STOP
    spca506_WriteI2c(spca50x, 0x00, 0x17);	//VGATE Control (MSB)
    spca506_WriteI2c(spca50x, 0x00, 0x18);
    spca506_WriteI2c(spca50x, 0x00, 0x19);
    spca506_WriteI2c(spca50x, 0x00, 0x1a);
    spca506_WriteI2c(spca50x, 0x00, 0x1b);
    spca506_WriteI2c(spca50x, 0x00, 0x1c);
    spca506_WriteI2c(spca50x, 0x00, 0x1d);
    spca506_WriteI2c(spca50x, 0x00, 0x1e);
    spca506_WriteI2c(spca50x, 0xa1, 0x1f);
    spca506_WriteI2c(spca50x, 0x02, 0x40);
    spca506_WriteI2c(spca50x, 0xff, 0x41);
    spca506_WriteI2c(spca50x, 0xff, 0x42);
    spca506_WriteI2c(spca50x, 0xff, 0x43);
    spca506_WriteI2c(spca50x, 0xff, 0x44);
    spca506_WriteI2c(spca50x, 0xff, 0x45);
    spca506_WriteI2c(spca50x, 0xff, 0x46);
    spca506_WriteI2c(spca50x, 0xff, 0x47);
    spca506_WriteI2c(spca50x, 0xff, 0x48);
    spca506_WriteI2c(spca50x, 0xff, 0x49);
    spca506_WriteI2c(spca50x, 0xff, 0x4a);
    spca506_WriteI2c(spca50x, 0xff, 0x4b);
    spca506_WriteI2c(spca50x, 0xff, 0x4c);
    spca506_WriteI2c(spca50x, 0xff, 0x4d);
    spca506_WriteI2c(spca50x, 0xff, 0x4e);
    spca506_WriteI2c(spca50x, 0xff, 0x4f);
    spca506_WriteI2c(spca50x, 0xff, 0x50);
    spca506_WriteI2c(spca50x, 0xff, 0x51);
    spca506_WriteI2c(spca50x, 0xff, 0x52);
    spca506_WriteI2c(spca50x, 0xff, 0x53);
    spca506_WriteI2c(spca50x, 0xff, 0x54);
    spca506_WriteI2c(spca50x, 0xff, 0x55);
    spca506_WriteI2c(spca50x, 0xff, 0x56);
    spca506_WriteI2c(spca50x, 0xff, 0x57);
    spca506_WriteI2c(spca50x, 0x00, 0x58);
    spca506_WriteI2c(spca50x, 0x54, 0x59);
    spca506_WriteI2c(spca50x, 0x07, 0x5a);
    spca506_WriteI2c(spca50x, 0x83, 0x5b);
    spca506_WriteI2c(spca50x, 0x00, 0x5c);
    spca506_WriteI2c(spca50x, 0x00, 0x5d);
    spca506_WriteI2c(spca50x, 0x00, 0x5e);
    spca506_WriteI2c(spca50x, 0x00, 0x5f);
    spca506_WriteI2c(spca50x, 0x00, 0x60);
    spca506_WriteI2c(spca50x, 0x05, 0x61);
    spca506_WriteI2c(spca50x, 0x9f, 0x62);
	/***********************************************************/
    spca5xxRegWrite(spca50x->dev, 0x05, 0x00, 0x0003, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x05, 0x00, 0x0004, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x10, 0x0001, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x78, 0x0000, NULL, 0);
    switch(spca50x->mode){
    case 0:
    spca506_Setsize(spca50x, 0,
			    0x10, 0x10);
    break;
    case 1:
    spca506_Setsize(spca50x, 1,
			    0x1a, 0x1a);
    break;
    case 2:
    spca506_Setsize(spca50x, 2,
			    0x1c, 0x1c);
    break;
    case 4:
    spca506_Setsize(spca50x, 4,
			    0x34, 0x34);
    break;
    case 5:
    spca506_Setsize(spca50x, 5,
			    0x40, 0x40);
    break;
    default:
    spca506_Setsize(spca50x, 5,
			    0x40, 0x40);
    break;
    }
    /* compress setting and size */
    /* set i2c luma */
    spca5xxRegWrite(spca50x->dev, 0x02, 0x01, 0x0000, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x12, 0x0001, NULL, 0);
    spca5xxRegRead(spca50x->dev, 0x04, 0, 0x0001, Data, 2);
    PDEBUG(3, "************ Close Start spca506  **************");
    spca506_GetNormeInput(spca50x, &norme, &channel);
    spca506_SetNormeInput(spca50x, norme, channel);
}
static void spca506_stopN(struct usb_spca50x *spca50x)
{
    spca5xxRegWrite(spca50x->dev, 0x02, 0x00, 0x0000, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x00, 0x0004, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x03, 0x00, 0x0003, NULL, 0);
}
static void spca506_Setsize(struct usb_spca50x *spca50x, __u16 code,
			    __u16 xmult, __u16 ymult)
{
    PDEBUG(3, "************ Open SetSize spca506  **************");
    spca5xxRegWrite(spca50x->dev, 0x04, (0x18 | (code & 0x07)), 0x0000,
		    NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x04, 0x41, 0x0001, NULL, 0);	// Soft snap 0x40 Hard 0x41
    spca5xxRegWrite(spca50x->dev, 0x04, 0x00, 0x0002, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x04, 0x00, 0x0003, NULL, 0);	//reserved
    spca5xxRegWrite(spca50x->dev, 0x04, 0x00, 0x0004, NULL, 0);	//reserved
    spca5xxRegWrite(spca50x->dev, 0x04, 0x01, 0x0005, NULL, 0);	//reserved
    spca5xxRegWrite(spca50x->dev, 0x04, xmult, 0x0006, NULL, 0);	//reserced
    spca5xxRegWrite(spca50x->dev, 0x04, ymult, 0x0007, NULL, 0);	//reserved
    spca5xxRegWrite(spca50x->dev, 0x04, 0x00, 0x0008, NULL, 0);	// compression 1
    spca5xxRegWrite(spca50x->dev, 0x04, 0x00, 0x0009, NULL, 0);	//T=64 -> 2
    spca5xxRegWrite(spca50x->dev, 0x04, 0x21, 0x000a, NULL, 0);	//threshold2D
    spca5xxRegWrite(spca50x->dev, 0x04, 0x00, 0x000b, NULL, 0);	//quantization
    PDEBUG(3, "************ Close SetSize spca506  **************");
}

static __u16 spca506_getbrightness(struct usb_spca50x *spca50x)
{
spca50x->brightness = (spca506_ReadI2c(spca50x, SAA7113_bright)) << 8;
return spca50x->brightness;
}
static __u16 spca506_getcontrast(struct usb_spca50x *spca50x)
{
spca50x->contrast = (spca506_ReadI2c(spca50x, SAA7113_contrast)) << 8;
return spca50x->contrast;
}
static __u16 spca506_getcolors(struct usb_spca50x *spca50x)
{
spca50x->hue = (spca506_ReadI2c(spca50x, SAA7113_hue)) << 8;
spca50x->colour = (spca506_ReadI2c(spca50x, SAA7113_saturation)) << 8;
return spca50x->colour;
}
static void spca506_setbrightness(struct usb_spca50x *spca50x)
{
    spca506_Initi2c(spca50x);
    spca506_WriteI2c(spca50x, ((spca50x->brightness >> 8) & 0xFF), SAA7113_bright);
    spca506_WriteI2c(spca50x, 0x01, 0x09);
}
static void spca506_setcontrast(struct usb_spca50x *spca50x)
{
 spca506_Initi2c(spca50x);
 spca506_WriteI2c(spca50x, ((spca50x->contrast >> 8) & 0xFF), SAA7113_contrast);
 spca506_WriteI2c(spca50x, 0x01, 0x09);
}
static void spca506_setcolors(struct usb_spca50x *spca50x)
{
    spca506_Initi2c(spca50x);
    spca506_WriteI2c(spca50x, ((spca50x->hue >> 8) & 0xFF), SAA7113_hue);
    spca506_WriteI2c(spca50x, ((spca50x->colour >> 8) & 0xFF), SAA7113_saturation);
    spca506_WriteI2c(spca50x, 0x01, 0x09);
}
static int spca506_config(struct usb_spca50x *spca50x)
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
    return 0;
}
static int spca506_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum,int *datalength)
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

#endif				/* SPCA506_INIT_H */
//eof
