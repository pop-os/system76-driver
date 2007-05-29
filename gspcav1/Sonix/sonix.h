
#ifndef SONIXUSB_H
#define SONIXUSB_H
/****************************************************************************
#	 	sonix sn9c102 library                                       #
# 		Copyright (C) 2003 2004 Michel Xhaard   mxhaard@magic.fr    #
# Add Pas106 Stefano Mozzi (C) 2004 	 				    #
#                                                                           #
# This program is free software; you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by      #
# the Free Software Foundation; either version 2 of the License, or         #
# (at your option) any later version.                                       #
#                                                                           #
# This program is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of            #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
# GNU General Public License for more details.                              #
#                                                                           #
# You should have received a copy of the GNU General Public License         #
# along with this program; if not, write to the Free Software               #
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA #
#                                                                           #
****************************************************************************/

#define COMP2 0x8F
#define COMP 0xC7		//0x87 //0x07
#define COMP1 0xC9		//0x89 //0x09

#define MCK_INIT 0x63
#define MCK_INIT1 0x20

#define SYS_CLK 0x04
/*******************     Camera Interface   ***********************/
static int sonix_init(struct usb_spca50x *spca50x);
static void sonix_start(struct usb_spca50x *spca50x);
static void sonix_stopN(struct usb_spca50x *spca50x);
static void sonix_stop0(struct usb_spca50x *spca50x);
static __u16 sonix_getbrightness(struct usb_spca50x *spca50x);
static void sonix_setbrightness(struct usb_spca50x *spca50x);
static void sonix_setcontrast(struct usb_spca50x *spca50x);
static __u16 sonix_getcontrast(struct usb_spca50x *spca50x);
static void sonix_setcolors(struct usb_spca50x *spca50x);
static __u16 sonix_getcolors(struct usb_spca50x *spca50x);
static int sonix_config(struct usb_spca50x *spca50x);
static void sonix_shutdown(struct usb_spca50x *spca50x);
static void sonix_setAutobright(struct usb_spca50x *spca50x);
static void sonix_setquality(struct usb_spca50x *spca50x);
static int sonix_sofdetect(struct usb_spca50x *spca50x,
			   struct spca50x_frame *frame, unsigned char *cdata,
			   int *iPix, int seqnum, int *datalength);
/******************************************************************/
static void
sonix_setcolors(struct usb_spca50x *spca50x)
{
}
static __u16
sonix_getcolors(struct usb_spca50x *spca50x)
{
	return 0;
}
static void
sonix_shutdown(struct usb_spca50x *spca50x)
{
}
static void
sonix_setAutobright(struct usb_spca50x *spca50x)
{
}
static void
sonix_setquality(struct usb_spca50x *spca50x)
{
}
static void
sonix_stop0(struct usb_spca50x *spca50x)
{
}

/*****************************************************************/
#include "sn9cxxx.h"
static struct cam_operation fsonix = {
	.initialize = sonix_init,
	.configure = sonix_config,
	.start = sonix_start,
	.stopN = sonix_stopN,
	.stop0 = sonix_stop0,
	.get_bright = sonix_getbrightness,
	.set_bright = sonix_setbrightness,
	.get_contrast = sonix_getcontrast,
	.set_contrast = sonix_setcontrast,
	.get_colors = sonix_getcolors,
	.set_colors = sonix_setcolors,
	.set_autobright = sonix_setAutobright,
	.set_quality = sonix_setquality,
	.cam_shutdown = sonix_shutdown,
	.sof_detect = sonix_sofdetect,
};
static void
set_sonixVGA(struct usb_spca50x *spca50x)
{
	memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof (struct mwebcam));
	spca50x->mode_cam[VGA].width = 640;
	spca50x->mode_cam[VGA].height = 480;
	spca50x->mode_cam[VGA].t_palette =
	    P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	if (spca50x->customid == SN9C102P || spca50x->customid == SN9C105
	    || spca50x->customid == SN9C120)
		spca50x->mode_cam[VGA].t_palette |= P_JPEG;
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
	if (spca50x->customid == SN9C102P || spca50x->customid == SN9C105
	    || spca50x->customid == SN9C120)
		spca50x->mode_cam[CIF].t_palette |= P_JPEG;
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
	spca50x->mode_cam[QCIF].width = 160;
	spca50x->mode_cam[QCIF].height = 120;
	spca50x->mode_cam[QCIF].t_palette =
	    P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[QCIF].pipe = 1023;
	spca50x->mode_cam[QCIF].method = 0;
	spca50x->mode_cam[QCIF].mode = 2;
	if (spca50x->customid == SN9C102P || spca50x->customid == SN9C105
	    || spca50x->customid == SN9C120)
		spca50x->mode_cam[QCIF].t_palette |= P_JPEG;
}
static void
set_sonixSIF(struct usb_spca50x *spca50x)
{
	memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof (struct mwebcam));
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
	    P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
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
	    P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[QSIF].pipe = 1023;
	spca50x->mode_cam[QSIF].method = 0;
	spca50x->mode_cam[QSIF].mode = 1;
	spca50x->mode_cam[QCIF].width = 160;
	spca50x->mode_cam[QCIF].height = 120;
	spca50x->mode_cam[QCIF].t_palette =
	    P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[QCIF].pipe = 1023;
	spca50x->mode_cam[QCIF].method = 1;
	spca50x->mode_cam[QCIF].mode = 1;
}

static __u8 initTas5130[] = {
	0x04, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x11, 0x00, 0x00, 0x00,
	0x00, 0x00,
	0x00, 0x01, 0x00, 0x69, 0x0c, 0x0a,
	0x28, 0x1e, 0x60, COMP, MCK_INIT,
	0x18, 0x10, 0x04, 0x03, 0x11, 0x0c
};

static __u8 initPas106[] = {
	0x04, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x81, 0x40, 0x00, 0x00, 0x00,
	0x00, 0x00,
	0x00, 0x00, 0x00, 0x05, 0x01, 0x00,
	0x16, 0x12, 0x28, COMP1, MCK_INIT1,
	0x18, 0x10, 0x04, 0x03, 0x11, 0x0c
};

static __u8 initOv7630[] = {
	0x04, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x21, 0x00, 0x00, 0x00,
	0x00, 0x00,
	0x00, 0x00, 0x00, 0x02, 0x03, 0x0a,	//shift one pixel 0x02 is 0x01 at start
	0x28, 0x1e, 0x68, COMP1, MCK_INIT1,
	0x1d, 0x10, 0x02, 0x03, 0x0f, 0x0c
};
static __u8 initHv7131[] = {
	0x46, 0x77, 0x00, 0x04, 0x00, 0x00, 0x00, 0x80, 0x11, 0x00, 0x00, 0x00,
	0x00, 0x00,
	0x00, 0x00, 0x00, 0x03, 0x01, 0x00,	// shift from 0x02 0x01 0x00
	0x28, 0x1e, 0x60, 0x8a, 0x20,
	0x1d, 0x10, 0x02, 0x03, 0x0f, 0x0c
};
static __u8 initTas5110[] = {
	0x44, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x11, 0x00, 0x00, 0x00,
	0x00, 0x00,
	0x00, 0x01, 0x00, 0x46, 0x09, 0x0a,	// shift from 0x45 0x09 0x0a
	0x16, 0x12, 0x60, 0x86, 0x2b,
	0x14, 0x0a, 0x02, 0x02, 0x09, 0x07
};
static __u8 initPas202[] = {
	0x44, 0x44, 0x21, 0x30, 0x00, 0x00, 0x00, 0x80, 0x40, 0x00, 0x00, 0x00,
	0x00, 0x00,
	0x00, 0x00, 0x00, 0x07, 0x03, 0x0A,	//6
	0x28, 0x1e, 0x28, 0x89, 0x30,
	0x00, 0x00, 0x02, 0x03, 0x0F, 0x0C
};

//compression 0x86 mckinit1 0x2b
static __u8 pas106_data[][2] = {
	{0x02, 0x04},		/* Pixel Clock Divider 6 */
	{0x03, 0x13},		/* Frame Time MSB */
	//{ 0x03, 0x12}, /* Frame Time MSB */
	{0x04, 0x06},		/* Frame Time LSB */
	//{ 0x04, 0x05}, /* Frame Time LSB */
	{0x05, 0x65},		/* Shutter Time Line Offset */
	//{ 0x05, 0x6d}, /* Shutter Time Line Offset */
	//{ 0x06, 0xB1}, /* Shutter Time Pixel Offset */
	{0x06, 0xcd},		/* Shutter Time Pixel Offset */
	{0x07, 0xC1},		/* Black Level Subtract Sign */
	//{ 0x07, 0x00}, /* Black Level Subtract Sign */
	{0x08, 0x06}, /* Black Level Subtract Level */ {0x08, 0x06},	/* Black Level Subtract Level */
	//{ 0x08, 0x01}, /* Black Level Subtract Level */
	{0x09, 0x05},		/* Color Gain B Pixel 5 a */
	{0x0A, 0x04},		/* Color Gain G1 Pixel 1 5 */
	{0x0B, 0x04},		/* Color Gain G2 Pixel 1 0 5 */
	{0x0C, 0x05},		/* Color Gain R Pixel 3 1 */
	{0x0D, 0x00},		/* Color GainH  Pixel */
	{0x0E, 0x0E},		/* Global Gain */
	{0x0F, 0x00},		/* Contrast */
	{0x10, 0x06},		/* H&V synchro polarity */
	{0x11, 0x06},		/* ?default */
	{0x12, 0x06},		/* DAC scale */
	{0x14, 0x02},		/* ?default */
	{0x13, 0x01},		/* Validate Settings */
	{0, 0}			/* The end */
};
static __u8 ov7630_sensor_init[][8] = {
	{0xa0, 0x21, 0x12, 0x80, 0x00, 0x00, 0x00, 0x10},
	{0xb0, 0x21, 0x01, 0x77, 0x3a, 0x00, 0x00, 0x10},
	{0xd0, 0x21, 0x12, 0x78, 0x00, 0x80, 0x34, 0x10},
	{0xa0, 0x21, 0x1b, 0x04, 0x00, 0x80, 0x34, 0x10},
	{0xa0, 0x21, 0x20, 0x44, 0x00, 0x80, 0x34, 0x10},
	{0xa0, 0x21, 0x23, 0xee, 0x00, 0x80, 0x34, 0x10},
	{0xd0, 0x21, 0x26, 0xa0, 0x9a, 0xa0, 0x30, 0x10},
	{0xb0, 0x21, 0x2a, 0x80, 0x00, 0xa0, 0x30, 0x10},
	{0xb0, 0x21, 0x2f, 0x3d, 0x24, 0xa0, 0x30, 0x10},
	{0xa0, 0x21, 0x32, 0x86, 0x24, 0xa0, 0x30, 0x10},
	{0xb0, 0x21, 0x60, 0xa9, 0x42, 0xa0, 0x30, 0x10},
	{0xa0, 0x21, 0x65, 0x00, 0x42, 0xa0, 0x30, 0x10},
	{0xa0, 0x21, 0x69, 0x38, 0x42, 0xa0, 0x30, 0x10},
	{0xc0, 0x21, 0x6f, 0x88, 0x0b, 0x00, 0x30, 0x10},
	{0xc0, 0x21, 0x74, 0x21, 0x8e, 0x00, 0x30, 0x10},
	{0xa0, 0x21, 0x7d, 0xf7, 0x8e, 0x00, 0x30, 0x10},
	{0xd0, 0x21, 0x17, 0x1c, 0xbd, 0x06, 0xf6, 0x10},	//
	{0xa0, 0x21, 0x10, 0x36, 0xbd, 0x06, 0xf6, 0x16},	// exposure
	{0xa0, 0x21, 0x76, 0x03, 0xbd, 0x06, 0xf6, 0x16},
	{0xa0, 0x21, 0x11, 0x01, 0xbd, 0x06, 0xf6, 0x16},
	{0xa0, 0x21, 0x00, 0x10, 0xbd, 0x06, 0xf6, 0x15},	//gain
//{ 0xb0, 0x21, 0x2a, 0xc0, 0x3c, 0x06, 0xf6, 0x1d},//a0 1c,a0 1f,c0 3c frame rate ?line interval from ov6630
	{0xb0, 0x21, 0x2a, 0xa0, 0x1f, 0x06, 0xf6, 0x1d},
	{0, 0, 0, 0, 0, 0, 0, 0}
};
static __u8 tas5110_sensor_init[][8] = {
	{0x30, 0x11, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x10},
	{0x30, 0x11, 0x02, 0x20, 0xa9, 0x00, 0x00, 0x10},
	{0, 0, 0, 0, 0, 0, 0, 0}
};
static __u8 hv7131_sensor_init[][8] = {
	{0xc0, 0x11, 0x31, 0x38, 0x2a, 0x2e, 0x00, 0x10},
	{0xa0, 0x11, 0x01, 0x08, 0x2a, 0x2e, 0x00, 0x10},
	{0xb0, 0x11, 0x20, 0x00, 0xd0, 0x2e, 0x00, 0x10},
	{0xc0, 0x11, 0x25, 0x03, 0x0e, 0x28, 0x00, 0x16},
	{0xa0, 0x11, 0x30, 0x10, 0x0e, 0x28, 0x00, 0x15},
	{0, 0, 0, 0, 0, 0, 0, 0}
};
static __u8 pas202_sensor_init[][8] = {
	{0xA0, 0x40, 0x02, 0x03, 0x00, 0x00, 0x00, 0x10},
	{0xD0, 0x40, 0x04, 0x07, 0x34, 0x00, 0x09, 0x10},
	{0xD0, 0x40, 0x08, 0x01, 0x00, 0x00, 0x01, 0x10},
	{0xD0, 0x40, 0x0C, 0x00, 0x0C, 0x00, 0x32, 0x10},
	{0xD0, 0x40, 0x10, 0x00, 0x01, 0x00, 0x63, 0x10},
	{0xA0, 0x40, 0x15, 0x70, 0x01, 0x00, 0x63, 0x10},
	{0xA0, 0x40, 0x18, 0x00, 0x01, 0x00, 0x63, 0x10},
	{0xA0, 0x40, 0x11, 0x01, 0x01, 0x00, 0x63, 0x10},
	{0xA0, 0x40, 0x03, 0x56, 0x01, 0x00, 0x63, 0x10},
	{0xA0, 0x40, 0x11, 0x01, 0x01, 0x00, 0x63, 0x10},
	{0xB0, 0x40, 0x04, 0x07, 0x2A, 0x00, 0x63, 0x10},
	{0xB0, 0x40, 0x0E, 0x00, 0x3D, 0x00, 0x63, 0x10},

	{0xA0, 0x40, 0x11, 0x01, 0x3D, 0x00, 0x63, 0x16},
	{0xA0, 0x40, 0x10, 0x08, 0x3D, 0x00, 0x63, 0x15},
	{0xA0, 0x40, 0x02, 0x04, 0x3D, 0x00, 0x63, 0x16},
	{0xA0, 0x40, 0x11, 0x01, 0x3D, 0x00, 0x63, 0x16},
	{0xB0, 0x40, 0x0E, 0x00, 0x31, 0x00, 0x63, 0x16},
	{0xA0, 0x40, 0x11, 0x01, 0x31, 0x00, 0x63, 0x16},
	{0xA0, 0x40, 0x10, 0x0E, 0x31, 0x00, 0x63, 0x15},
	{0xA0, 0x40, 0x11, 0x01, 0x31, 0x00, 0x63, 0x16},
	{0, 0, 0, 0, 0, 0, 0, 0}
};

static int
sonix_i2cwrite(struct usb_device *dev, __u8 * buffer, __u16 length)
{
	int retry = 60;
	__u8 ByteReceive = 0x00;
	/* is i2c ready */
	if (length > 8 || !buffer)
		return -1;
	sonixRegWrite(dev, 0x08, 0x08, 0x0000, buffer, length);
	while (retry--) {
		wait_ms(10);
		sonixRegRead(dev, 0x00, 0x08, 0x0000, &ByteReceive, 1);
		if (ByteReceive == 4)
			return 0;
	}
	return -1;
}

static __u16
sonix_getbrightness(struct usb_spca50x *spca50x)
{				/*FIXME hardcoded as we need to read register of the tasc */
	spca50x->brightness = 0x80 << 8;
	spca50x->contrast = 0x80 << 8;
	return spca50x->brightness;
}
static __u16
sonix_getcontrast(struct usb_spca50x *spca50x)
{				/*FIXME hardcoded as we need to read register of the tasc */

	spca50x->contrast = 0x80 << 8;
	return spca50x->contrast;
}
static void
sonix_setbrightness(struct usb_spca50x *spca50x)
{
	__u8 value;
	__u8 i2c[] = { 0x30, 0x11, 0x02, 0x20, 0x70, 0x00, 0x00, 0x10 };
	__u8 i2c1[] = { 0xA1, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x14 };
	__u8 i2cOV[] = { 0xa0, 0x21, 0x06, 0x36, 0xbd, 0x06, 0xf6, 0x16 };
	__u8 i2cp202[] = { 0xA0, 0x40, 0x10, 0x0E, 0x31, 0x00, 0x63, 0x15 };
	__u8 i2cpdoit[] = { 0xA0, 0x40, 0x11, 0x01, 0x31, 0x00, 0x63, 0x16 };
	//__u8 i2cpexpo1[] = { 0xB0,0x40,0x04,0x07,0x2A,0x00,0x63,0x16 };
	__u8 i2cpexpo[] = { 0xB0, 0x40, 0x0e, 0x01, 0xab, 0x00, 0x63, 0x16 };
	if (spca50x->sensor == SENSOR_TAS5130CXX ||
	    spca50x->sensor == SENSOR_TAS5110) {
		value = (0xFF - (spca50x->brightness >> 8));
		i2c[4] = value & 0xFF;
		PDEBUG(4, "brightness %d :%d ", value, i2c[4]);
		if (sonix_i2cwrite(spca50x->dev, i2c, 8) < 0)
			PDEBUG(0, "i2c error brightness");
	} else if (spca50x->sensor == SENSOR_PAS106) {
		i2c1[3] = spca50x->brightness >> 11;
		i2c1[2] = 0x0e;;
		if (sonix_i2cwrite(spca50x->dev, i2c1, 8) < 0)
			PDEBUG(0, "i2c error brightness");
		i2c1[3] = 0x01;
		i2c1[2] = 0x13;;
		if (sonix_i2cwrite(spca50x->dev, i2c1, 8) < 0)
			PDEBUG(0, "i2c error brightness");
	} else if (spca50x->sensor == SENSOR_OV7630) {
		// change reg 0x06
		i2cOV[3] = (spca50x->brightness >> 8);
		if (sonix_i2cwrite(spca50x->dev, i2cOV, 8) < 0)
			PDEBUG(0, "i2c error brightness");
	} else if (spca50x->sensor == SENSOR_PAS202) {
		// change reg 0x10
		i2cpexpo[4] = 0xff - (spca50x->brightness >> 8);
		//if(sonix_i2cwrite(spca50x->dev,i2cpexpo1,8) < 0) PDEBUG(0,"i2c error brightness");
		//if(sonix_i2cwrite(spca50x->dev,i2cpdoit,8) < 0) PDEBUG(0,"i2c error brightness");
		if (sonix_i2cwrite(spca50x->dev, i2cpexpo, 8) < 0)
			PDEBUG(0, "i2c error brightness");
		if (sonix_i2cwrite(spca50x->dev, i2cpdoit, 8) < 0)
			PDEBUG(0, "i2c error brightness");
		i2cp202[3] = (spca50x->brightness >> 11);
		if (sonix_i2cwrite(spca50x->dev, i2cp202, 8) < 0)
			PDEBUG(0, "i2c error brightness");
		if (sonix_i2cwrite(spca50x->dev, i2cpdoit, 8) < 0)
			PDEBUG(0, "i2c error brightness");
	}
}
static void
sonix_setcontrast(struct usb_spca50x *spca50x)
{
	__u8 gain = 0;
	__u8 rgb_value = 0;
	gain = (spca50x->contrast >> 13) & 0x0F;
	/* red and blue gain */
	rgb_value = gain << 4 | gain;
	sonixRegWrite(spca50x->dev, 0x08, 0x10, 0x0000, &rgb_value, 1);
	/* green gain */
	rgb_value = gain;
	sonixRegWrite(spca50x->dev, 0x08, 0x11, 0x0000, &rgb_value, 1);
}
static int
sonix_init(struct usb_spca50x *spca50x)
{
	__u8 ByteReceive = 0x00;
	sonixRegRead(spca50x->dev, 0x00, 0x00, 0x0000, &ByteReceive, 1);
	if (ByteReceive != 0x10)
		return -ENODEV;

	return 0;
}

static int
tas5130_I2cinit(struct usb_spca50x *spca50x)
{

	//__u8 i2c10[]= { 0x30,0x11,0x00,0x40,0x47,0x00,0x00,0x10 }; // shutter 0x47 short exposure?
	__u8 i2c10[] = { 0x30, 0x11, 0x00, 0x40, 0x01, 0x00, 0x00, 0x10 };	// shutter 0x01 long exposure 
	__u8 i2c2[] = { 0x30, 0x11, 0x02, 0x20, 0x70, 0x00, 0x00, 0x10 };

	if (sonix_i2cwrite(spca50x->dev, i2c10, 8) < 0)
		PDEBUG(0, "i2c error i2c10");
	if (sonix_i2cwrite(spca50x->dev, i2c2, 8) < 0)
		PDEBUG(0, "i2c error i2c2");

	return 0;
}

static int
pas106_I2cinit(struct usb_spca50x *spca50x)
{
	__u8 i2c1[] = { 0xA1, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x14 };
	int i = 0;
	while (pas106_data[i][0]) {
		memcpy(&i2c1[2], &pas106_data[i++][0], 2);	//copy 2 bytes from the template
		if (sonix_i2cwrite(spca50x->dev, i2c1, 8) < 0)
			PDEBUG(0, "i2c error pas106");
	}
	return 0;
}
static int
ov7630_I2cinit(struct usb_spca50x *spca50x)
{
	int i = 0;
	while (ov7630_sensor_init[i][0]) {
		if (sonix_i2cwrite(spca50x->dev, ov7630_sensor_init[i], 8) < 0)
			PDEBUG(0, "i2c error ov7630");
		i++;
	}
	return 0;
}
static int
tas5110_I2cinit(struct usb_spca50x *spca50x)
{
	int i = 0;
	while (tas5110_sensor_init[i][0]) {
		if (sonix_i2cwrite(spca50x->dev, tas5110_sensor_init[i], 8) < 0)
			PDEBUG(0, "i2c error tas5110");
		i++;
	}
	return 0;
}
static int
hv7131_I2cinit(struct usb_spca50x *spca50x)
{
	int i = 0;
	while (hv7131_sensor_init[i][0]) {
		if (sonix_i2cwrite(spca50x->dev, hv7131_sensor_init[i], 8) < 0)
			PDEBUG(0, "i2c error hv7131");
		i++;
	}
	return 0;
}
static int
pas202_I2cinit(struct usb_spca50x *spca50x)
{
	int i = 0;
	while (pas202_sensor_init[i][0]) {
		if (sonix_i2cwrite(spca50x->dev, pas202_sensor_init[i], 8) < 0)
			PDEBUG(0, "i2c error pas202");
		i++;
	}
	return 0;
}
static void
sonix_start(struct usb_spca50x *spca50x)
{

	__u8 compress = 0;
	__u8 MCK_SIZE = 0x33;
	__u8 frmult = 0x28;
	__u8 *sn9c10x = NULL;
	__u8 CompressCtrl[] = { 0, 0 };
	int err = 0;
	switch (spca50x->sensor) {
	case SENSOR_OV7630:
		sn9c10x = initOv7630;
		compress = spca50x->mode << 4 | COMP2;
		CompressCtrl[0] = compress;
		frmult = 0x68;
		CompressCtrl[1] = 0x20;
		MCK_SIZE = 0x20;
		break;
	case SENSOR_TAS5130CXX:
		sn9c10x = initTas5130;
		compress = spca50x->mode << 4 | COMP;
		CompressCtrl[0] = compress;
		frmult = 0x60;
		switch (spca50x->mode) {
		case 0:	/* 640x480 3fp/s */
			CompressCtrl[1] = 0x43;	//0xA3 3fp/s ;// 0xF3;
			MCK_SIZE = 0x43;	// 0xA3;//0xF3;
			break;
		case 1:	/* 320x240 0x33 10fp/s */
			CompressCtrl[1] = 0x23;
			MCK_SIZE = 0x23;
			break;
		case 2:	/* 160x120 15fp/s */
			CompressCtrl[1] = 0x23;
			MCK_SIZE = 0x23;
			break;
		default:
			break;
		}
		break;
	case SENSOR_PAS106:
		sn9c10x = initPas106;;
		compress = spca50x->mode << 4 | COMP1;
		CompressCtrl[0] = compress;
		frmult = 0x24;	//0x28
		CompressCtrl[1] = 0x20;	//0xF3;
		MCK_SIZE = 0x20;	//0xF3;
		break;
	case SENSOR_TAS5110:
		sn9c10x = initTas5110;
		compress = spca50x->mode << 4 | 0x86;
		CompressCtrl[0] = compress;
		frmult = 0x60;
		CompressCtrl[1] = 0x2b;	//0xF3;
		MCK_SIZE = 0x2b;	//0xF3;
		break;
	case SENSOR_HV7131R:
		sn9c10x = initHv7131;
		compress = spca50x->mode << 4 | 0x8a;
		CompressCtrl[0] = compress;
		frmult = 0x60;
		CompressCtrl[1] = 0x20;
		MCK_SIZE = 0x20;
		break;
	case SENSOR_PAS202:
		sn9c10x = initPas202;
		compress = spca50x->mode << 4 | 0x89;
		CompressCtrl[0] = compress;
		frmult = 0x20;	//reg17 // 7 fp/s VGA
		if (spca50x->mode)
			frmult = 0x24;	// 0x28->11fp/s SIF 0x24
		CompressCtrl[1] = 0x20;	//reg19 30
		MCK_SIZE = 0x20;
		break;
	}
	/* reg 0x01 bit 2 video transfert on */

	sonixRegWrite(spca50x->dev, 0x08, 0x01, 0x0000, &sn9c10x[0], 1);
	/* reg 0x17 SensorClk enable inv Clk 0x60 */
	sonixRegWrite(spca50x->dev, 0x08, 0x17, 0x0000, &sn9c10x[0x17 - 1], 1);
	/* Set the whole registers from the template */
	sonixRegWrite(spca50x->dev, 0x08, 0x01, 0x0000, sn9c10x, 0x1f);
	switch (spca50x->sensor) {
	case SENSOR_TAS5130CXX:
		err = tas5130_I2cinit(spca50x);
		break;
	case SENSOR_PAS106:
		err = pas106_I2cinit(spca50x);
		break;
	case SENSOR_OV7630:
		err = ov7630_I2cinit(spca50x);
		break;
	case SENSOR_HV7131R:
		err = hv7131_I2cinit(spca50x);
		break;
	case SENSOR_TAS5110:
		err = tas5110_I2cinit(spca50x);
		break;
	case SENSOR_PAS202:
		err = pas202_I2cinit(spca50x);
		break;
	default:
		err = -EINVAL;
		break;
	}
	/* H_size V_size  0x28,0x1e maybe 640x480 */
	sonixRegWrite(spca50x->dev, 0x08, 0x15, 0x0000, &sn9c10x[0x15 - 1],
		      0x02);
	/* compression register */
	sonixRegWrite(spca50x->dev, 0x08, 0x18, 0x0000, &compress, 1);
	// H_start      
	sonixRegWrite(spca50x->dev, 0x08, 0x12, 0x0000, &sn9c10x[0x12 - 1], 1);
	// V_START      
	sonixRegWrite(spca50x->dev, 0x08, 0x13, 0x0000, &sn9c10x[0x13 - 1], 1);
	/* re set 0x17 SensorClk enable inv Clk 0x60 */
	sonixRegWrite(spca50x->dev, 0x08, 0x17, 0x0000, &frmult, 1);
	/*MCKSIZE ->3 */
	sonixRegWrite(spca50x->dev, 0x08, 0x19, 0x0000, &MCK_SIZE, 1);
	/* AE_STRX AE_STRY AE_ENDX AE_ENDY */
	sonixRegWrite(spca50x->dev, 0x08, 0x1c, 0x0000, &sn9c10x[0x1c - 1], 4);
	/* Enable video transfert */
	sonixRegWrite(spca50x->dev, 0x08, 0x01, 0x0000, &sn9c10x[0], 1);
	/* Compression */
	sonixRegWrite(spca50x->dev, 0x08, 0x18, 0x0000, CompressCtrl, 2);

	sonix_setcontrast(spca50x);
	sonix_setbrightness(spca50x);

}
static int
sonix_config(struct usb_spca50x *spca50x)
{
	switch (spca50x->sensor) {
	case SENSOR_OV7660:
	case SENSOR_MO4000:
	case SENSOR_OV7630:
	case SENSOR_TAS5130CXX:
	case SENSOR_HV7131R:
	case SENSOR_MI0360:
	case SENSOR_PAS202:
		set_sonixVGA(spca50x);
		break;
	case SENSOR_PAS106:
	case SENSOR_TAS5110:
		set_sonixSIF(spca50x);
		break;
	default:
		return -EINVAL;
		break;
	}
	spca50x->qindex = 4;	//set the quantization table
	return 0;
}
static void
sonix_stopN(struct usb_spca50x *spca50x)
{
	__u8 ByteSend = 0;

	ByteSend = 0x09;	// 0X00
	sonixRegWrite(spca50x->dev, 0x08, 0x01, 0x0000, &ByteSend, 1);
}
static int
sonix_sofdetect(struct usb_spca50x *spca50x, struct spca50x_frame *frame,
		unsigned char *cdata, int *iPix, int seqnum, int *datalength)
{

	int sof = 0;
	int j = 0;
	int p = 0;

	if (*datalength < 24) {
		if (*datalength > 6) {
			j = *datalength - 6;
		} else {
			j = 0;
		}
		if (j > 0) {
			for (p = 0; p < j; p++) {
				if ((cdata[0 + p] == 0xFF)
				    && (cdata[1 + p] == 0xFF)
				    && (cdata[2 + p] == 0x00)
				    && (cdata[3 + p] == 0xC4)
				    && (cdata[4 + p] == 0xC4)
				    && (cdata[5 + p] == 0x96)) {
					sof = 1;
					break;
				}
			}
		}
	}
	if (sof) {
		*iPix = p + 12;
		*datalength -= *iPix;
		return 0;
		PDEBUG(5,
		       "Sonix header packet found %d datalength %d !!",
		       p, *datalength);
	} else
		*iPix = 0;
	return seqnum + 1;
}
#endif				/* SONIXUSB_H */
