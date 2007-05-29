#ifndef SP5XXFW2_H
#define SP5XXFW2_H
/****************************************************************************
#	 	Sunplus spca504(abc) spca533 spca536  library               #
# 		Copyright (C) 2005 Michel Xhaard   mxhaard@magic.fr         #
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
#define SPCA504_PCCAM600_OFFSET_SNAPSHOT 3
#define SPCA504_PCCAM600_OFFSET_COMPRESS 4
#define SPCA504_PCCAM600_OFFSET_MODE	 5
#define SPCA504_PCCAM600_OFFSET_DATA	 14
 /* Frame packet header offsets for the spca533 */
#define SPCA533_OFFSET_DATA      16
#define SPCA533_OFFSET_FRAMSEQ	15
/* Frame packet header offsets for the spca536 */
#define SPCA536_OFFSET_DATA      4
#define SPCA536_OFFSET_FRAMSEQ	 1
#include "sp5xxfw2.dat"
static int sp5xxfw2_init(struct usb_spca50x *spca50x);
static void sp5xxfw2_start(struct usb_spca50x *spca50x);
static void sp5xxfw2_stopN(struct usb_spca50x *spca50x);
static void sp5xxfw2_stop0(struct usb_spca50x *spca50x);
static void sp5xxfw2_setbrightness(struct usb_spca50x *spca50x);
static __u16 sp5xxfw2_getbrightness(struct usb_spca50x *spca50x);
static void sp5xxfw2_setcontrast(struct usb_spca50x *spca50x);
static __u16 sp5xxfw2_getcontrast(struct usb_spca50x *spca50x);
static void sp5xxfw2_setcolors(struct usb_spca50x *spca50x);
static __u16 sp5xxfw2_getcolors(struct usb_spca50x *spca50x);
static void sp5xxfw2_setAutobright (struct usb_spca50x *spca50x);
static int sp5xxfw2_config(struct usb_spca50x *spca50x);
static void sp5xxfw2_setquality(struct usb_spca50x *spca50x);
static void sp5xxfw2_shutdown(struct usb_spca50x *spca50x);
static int sp5xxfw2_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum,int *datalength);
/************************** Virtual *************************/
static void sp5xxfw2_shutdown(struct usb_spca50x *spca50x){}
static void sp5xxfw2_setAutobright (struct usb_spca50x *spca50x){}
static void sp5xxfw2_setquality(struct usb_spca50x *spca50x){}
static void sp5xxfw2_stop0(struct usb_spca50x *spca50x){}
//static __u16 sp5xxfw2_setexposure(struct usb_spca50x *spca50x);
//static __u16 sp5xxfw2_getexposure(struct usb_spca50x *spca50x);
/************************** Private *************************/
static struct cam_operation fsp5xxfw2 = {
 	.initialize = sp5xxfw2_init,
	.configure = sp5xxfw2_config,
	.start = sp5xxfw2_start,
	.stopN = sp5xxfw2_stopN,
	.stop0 = sp5xxfw2_stop0,
	.get_bright = sp5xxfw2_getbrightness,
	.set_bright = sp5xxfw2_setbrightness,
	.get_contrast = sp5xxfw2_getcontrast,
	.set_contrast = sp5xxfw2_setcontrast,
	.get_colors = sp5xxfw2_getcolors,
	.set_colors = sp5xxfw2_setcolors,
	.set_autobright = sp5xxfw2_setAutobright,
	.set_quality = sp5xxfw2_setquality,
	.cam_shutdown = sp5xxfw2_shutdown,
	.sof_detect = sp5xxfw2_sofdetect,
 };

static void spca504B_SetSizeType(struct usb_spca50x *spca50x);

static void
spca504_acknowledged_command(struct usb_spca50x *spca50x,
			     __u16 reg, __u16 idx, __u16 val);

static void
spca504A_acknowledged_command(struct usb_spca50x *spca50x,
			      __u16 reg,
			      __u16 idx, __u16 val, __u8 stat, __u8 count);
static void spca504_wait_status(struct usb_spca50x *spca50x);
static void spca50x_GetFirmware(struct usb_spca50x *spca50x);
static int spca504B_PollingDataReady(struct usb_device *dev);
static void spca504B_WaitCmdStatus(struct usb_spca50x *spca50x);
static void spca504B_setQtable(struct usb_spca50x *spca50x);
static void sp5xx_initContBrigHueRegisters(struct usb_spca50x *spca50x);
/************************************************************/
static int sp5xxfw2_init(struct usb_spca50x *spca50x)
{
    int rc;
    __u8 Data = 0;
    __u8 i;
    __u8 info[6];
    int err_code;
    switch (spca50x->bridge) {
    case BRIDGE_SPCA504B:{
	    spca5xxRegWrite(spca50x->dev, 0x1d, 0, 0, NULL, 0);
	    spca5xxRegWrite(spca50x->dev, 0, 1, 0x2306, NULL, 0);
	    spca5xxRegWrite(spca50x->dev, 0, 0, 0x0d04, NULL, 0);
	    spca5xxRegWrite(spca50x->dev, 0, 0, 0x2000, NULL, 0);
	    spca5xxRegWrite(spca50x->dev, 0, 0x13, 0x2301, NULL, 0);
	    spca5xxRegWrite(spca50x->dev, 0, 0, 0x2306, NULL, 0);
	}			// becare no break here init follow
    case BRIDGE_SPCA533:
	rc = spca504B_PollingDataReady(spca50x->dev);
	spca50x_GetFirmware(spca50x);
	break;
    case BRIDGE_SPCA536:
	spca50x_GetFirmware(spca50x);
	spca5xxRegRead(spca50x->dev, 0x00, 0, 0x5002, &Data, 1);
	Data = 0;
	spca5xxRegWrite(spca50x->dev, 0x24, 0, 0, &Data, 1);
	spca5xxRegRead(spca50x->dev, 0x24, 0, 0, &Data, 1);
	rc = spca504B_PollingDataReady(spca50x->dev);
	spca5xxRegWrite(spca50x->dev, 0x34, 0, 0, NULL, 0);
	spca504B_WaitCmdStatus(spca50x);
	break;
    case BRIDGE_SPCA504C:	//pccam600
	PDEBUG(2, "Opening SPCA504 (PC-CAM 600)");
	spca50x_reg_write(spca50x->dev, 0xe0, 0x0000, 0x0000);
	spca50x_reg_write(spca50x->dev, 0xe0, 0x0000, 0x0001);	// reset
	spca504_wait_status(spca50x);
	if (spca50x->desc == LogitechClickSmart420) {	/* clicksmart 420 */
	    spca50x_write_vector(spca50x,
				 spca504A_clicksmart420_open_data);
	} else {
	    spca50x_write_vector(spca50x, spca504_pccam600_open_data);
	}
	err_code = spca50x_setup_qtable(spca50x,
					0x00, 0x2800,
					0x2840, qtable_creative_pccam);
	if (err_code < 0) {
	    PDEBUG(2, "spca50x_setup_qtable failed");
	    return err_code;
	}
	break;
    case BRIDGE_SPCA504:
	PDEBUG(2, "Opening SPCA504");
	if (spca50x->desc == AiptekMiniPenCam13) {
	  /***************************************************************/
	    for (i = 0; i < 6; i++) {
		info[i] = spca50x_reg_read_with_value(spca50x->dev,
						      0x20, i, 0x0000, 1);
	    }
	    PDEBUG(0,
		   "Read info: %d %d %d %d %d %d . Should be 1,0,2,2,0,0\n",
		   info[0], info[1], info[2], info[3], info[4], info[5]);
	    /* spca504a aiptek */
	    // Set AE AWB Banding Type 3-> 50Hz 2-> 60Hz           
	    spca504A_acknowledged_command(spca50x, 0x24, 8, 3, 0x9e, 1);
	    // Twice sequencial need status 0xff->0x9e->0x9d 
	    spca504A_acknowledged_command(spca50x, 0x24, 8, 3, 0x9e, 0);

	    spca504A_acknowledged_command(spca50x, 0x24, 0, 0, 0x9d, 1);
	/**************************************************************/
	    /* spca504a aiptek */
	    spca504A_acknowledged_command(spca50x, 0x08, 6, 0, 0x86, 1);
	    // spca50x_reg_write (spca50x->dev, 0, 0x2000, 0);
	    // spca50x_reg_write (spca50x->dev, 0, 0x2883, 1);
	    // spca504A_acknowledged_command (spca50x, 0x08, 6, 0, 0x86, 1);
	    //spca504A_acknowledged_command (spca50x, 0x24, 0, 0, 0x9D, 1);
	    spca50x_reg_write(spca50x->dev, 0x0, 0x270c, 0x5);	// L92 sno1t.txt 
	    spca50x_reg_write(spca50x->dev, 0x0, 0x2310, 0x5);
	    spca504A_acknowledged_command(spca50x, 1, 0x0f, 0, 0xFF, 0);
	}
	/* setup qtable */
	spca50x_reg_write(spca50x->dev, 0, 0x2000, 0);
	spca50x_reg_write(spca50x->dev, 0, 0x2883, 1);
	err_code = spca50x_setup_qtable(spca50x,
					0x00, 0x2800,
					0x2840, qtable_spca504_default);
	if (err_code < 0) {
	    PDEBUG(2, "spca50x_setup_qtable failed");
	    return err_code;
	}
	break;
    }
    return 0;
}
static void sp5xxfw2_start(struct usb_spca50x *spca50x)
{
    int rc;
    int enable;
    __u8 i;
    __u8 info[6];
    if (spca50x->bridge == BRIDGE_SPCA504B)
	spca504B_setQtable(spca50x);
    spca504B_SetSizeType(spca50x);
    switch (spca50x->bridge) {
    case BRIDGE_SPCA504B:
    case BRIDGE_SPCA533:
    case BRIDGE_SPCA536:
	if (spca50x->desc == MegapixV4 ||
	    spca50x->desc == LogitechClickSmart820) {
	    spca5xxRegWrite(spca50x->dev, 0xF0, 0, 0, NULL, 0);
	    spca504B_WaitCmdStatus(spca50x);
	    spca5xxRegRead(spca50x->dev, 0xF0, 0, 4, NULL, 0);
	    spca504B_WaitCmdStatus(spca50x);
	} else {
	    spca5xxRegWrite(spca50x->dev, 0x31, 0, 4, NULL, 0);
	    spca504B_WaitCmdStatus(spca50x);
	    rc = spca504B_PollingDataReady(spca50x->dev);
	}
	break;
    case BRIDGE_SPCA504:
	if (spca50x->desc == AiptekMiniPenCam13) {
	    for (i = 0; i < 6; i++) {
		info[i] = spca50x_reg_read_with_value(spca50x->dev,
						      0x20, i, 0x0000, 1);
	    }
	    PDEBUG(0,
		   "Read info: %d %d %d %d %d %d . Should be 1,0,2,2,0,0\n",
		   info[0], info[1], info[2], info[3], info[4], info[5]);
	    /* spca504a aiptek */
	    // Set AE AWB Banding Type 3-> 50Hz 2-> 60Hz           
	    spca504A_acknowledged_command(spca50x, 0x24, 8, 3, 0x9e, 1);
	    // Twice sequencial need status 0xff->0x9e->0x9d 
	    spca504A_acknowledged_command(spca50x, 0x24, 8, 3, 0x9e, 0);

	    spca504A_acknowledged_command(spca50x, 0x24, 0, 0, 0x9d, 1);
	} else {
	    spca504_acknowledged_command(spca50x, 0x24, 8, 3);
	    for (i = 0; i < 6; i++) {
		info[i] = spca50x_reg_read_with_value(spca50x->dev,
						      0x20, i, 0x0000, 1);
	    }
	    PDEBUG(0,
		   "Read info: %d %d %d %d %d %d . Should be 1,0,2,2,0,0\n",
		   info[0], info[1], info[2], info[3], info[4], info[5]);
	    spca504_acknowledged_command(spca50x, 0x24, 8, 3);

	    spca504_acknowledged_command(spca50x, 0x24, 0, 0);
	}

	spca504B_SetSizeType(spca50x);
	spca50x_reg_write(spca50x->dev, 0x0, 0x270c, 0x5);	// L92 sno1t.txt 

	spca50x_reg_write(spca50x->dev, 0x0, 0x2310, 0x5);
	break;
    case BRIDGE_SPCA504C:
	if (spca50x->desc == LogitechClickSmart420) {
	    spca50x_write_vector(spca50x,
				 spca504A_clicksmart420_init_data);
	} else {
	    spca50x_write_vector(spca50x, spca504_pccam600_init_data);
	}
	enable = (spca50x->autoexpo ? 0x4 : 0x1);
	spca50x_reg_write(spca50x->dev, 0x0c, 0x0000, enable);	// auto exposure
	spca50x_reg_write(spca50x->dev, 0xb0, 0x0000, enable);	// auto whiteness

	/* set default exposure compensation and whiteness balance */
	spca50x_reg_write(spca50x->dev, 0x30, 0x0001, 800);	// ~ 20 fps
	spca50x_reg_write(spca50x->dev, 0x30, 0x0002, 1600);
	spca504B_SetSizeType(spca50x);
	break;
    }
    sp5xx_initContBrigHueRegisters(spca50x);
}
static void sp5xxfw2_stopN(struct usb_spca50x *spca50x)
{
    int rc;
    switch (spca50x->bridge) {
    case BRIDGE_SPCA533:
    case BRIDGE_SPCA536:
    case BRIDGE_SPCA504B:
	spca5xxRegWrite(spca50x->dev, 0x31, 0, 0, NULL, 0);
	spca504B_WaitCmdStatus(spca50x);
	rc = spca504B_PollingDataReady(spca50x->dev);
	break;
    case BRIDGE_SPCA504:
    case BRIDGE_SPCA504C:
	spca50x_reg_write(spca50x->dev, 0x00, 0x2000, 0x0000);

	if (spca50x->desc == AiptekMiniPenCam13) {
	    /* spca504a aiptek */
	    // spca504A_acknowledged_command (spca50x, 0x08, 6, 0, 0x86, 1);
	    spca504A_acknowledged_command(spca50x, 0x24, 0x0000, 0x0000,
					  0x9d, 1);
	    spca504A_acknowledged_command(spca50x, 0x01, 0x000f, 0x0000,
					  0xFF, 1);
	} else {
	    spca504_acknowledged_command(spca50x, 0x24, 0x0000, 0x0000);
	    spca50x_reg_write(spca50x->dev, 0x01, 0x000f, 0x0);
	}
	break;
    }
}
static void sp5xxfw2_setbrightness(struct usb_spca50x *spca50x)
{
    switch (spca50x->bridge) {
    case BRIDGE_SPCA533:
    case BRIDGE_SPCA504B:
    case BRIDGE_SPCA504:
    case BRIDGE_SPCA504C:
	spca50x_reg_write(spca50x->dev, 0x0, 0x21a7,
			  (spca50x->brightness >> 8));
	break;
    case BRIDGE_SPCA536:
	spca50x_reg_write(spca50x->dev, 0x0, 0x20f0,
			  (spca50x->brightness >> 8));
	break;
    }
}
static __u16 sp5xxfw2_getbrightness(struct usb_spca50x *spca50x)
{
    __u16 brightness = 0;
    switch (spca50x->bridge) {
    case BRIDGE_SPCA533:
    case BRIDGE_SPCA504B:
    case BRIDGE_SPCA504:
    case BRIDGE_SPCA504C:
	brightness = spca50x_reg_read(spca50x->dev, 0x0, 0x21a7, 2);
	spca50x->brightness = (((brightness & 0xFF) - 128) % 255) << 8;
	break;
    case BRIDGE_SPCA536:
	brightness = spca50x_reg_read(spca50x->dev, 0x0, 0x20f0, 2);
	spca50x->brightness = (((brightness & 0xFF) - 128) % 255) << 8;
	break;
    }
    return (((brightness & 0xFF) - 128) % 255) << 8;
}
static void sp5xxfw2_setcontrast(struct usb_spca50x *spca50x)
{
    switch (spca50x->bridge) {
    case BRIDGE_SPCA533:
    case BRIDGE_SPCA504B:
    case BRIDGE_SPCA504:
    case BRIDGE_SPCA504C:
	spca50x_reg_write(spca50x->dev, 0x0, 0x21a8,
			  spca50x->contrast >> 8);
	break;
    case BRIDGE_SPCA536:
	spca50x_reg_write(spca50x->dev, 0x0, 0x20f1,
			  spca50x->contrast >> 8);
	break;
    }
}
static __u16 sp5xxfw2_getcontrast(struct usb_spca50x *spca50x)
{
    switch (spca50x->bridge) {
    case BRIDGE_SPCA533:
    case BRIDGE_SPCA504B:
    case BRIDGE_SPCA504:
    case BRIDGE_SPCA504C:
	spca50x->contrast =
	    spca50x_reg_read(spca50x->dev, 0x0, 0x21a8, 2) << 8;
	break;
    case BRIDGE_SPCA536:
	spca50x->contrast =
	    spca50x_reg_read(spca50x->dev, 0x0, 0x20f1, 2) << 8;
	break;
    }
    return spca50x->contrast;
}
static void sp5xxfw2_setcolors(struct usb_spca50x *spca50x)
{
    switch (spca50x->bridge) {
    case BRIDGE_SPCA533:
    case BRIDGE_SPCA504B:
    case BRIDGE_SPCA504:
    case BRIDGE_SPCA504C:
	spca50x_reg_write(spca50x->dev, 0x0, 0x21ae, spca50x->colour >> 8);
	break;
    case BRIDGE_SPCA536:
	spca50x_reg_write(spca50x->dev, 0x0, 0x20f6, spca50x->colour >> 8);
	break;
    }
}


static __u16 sp5xxfw2_getcolors(struct usb_spca50x *spca50x)
{
    switch (spca50x->bridge) {
    case BRIDGE_SPCA533:
    case BRIDGE_SPCA504B:
    case BRIDGE_SPCA504:
    case BRIDGE_SPCA504C:
	spca50x->colour =
	    spca50x_reg_read(spca50x->dev, 0x0, 0x21ae, 2) << 7;
	break;
    case BRIDGE_SPCA536:
	spca50x->colour =
	    spca50x_reg_read(spca50x->dev, 0x0, 0x20f6, 2) << 7;
	break;
    }
    return spca50x->colour;
}
static int sp5xxfw2_config(struct usb_spca50x *spca50x)
{
    switch (spca50x->bridge) {
    case BRIDGE_SPCA504B:
    case BRIDGE_SPCA504:
    case BRIDGE_SPCA536:
	memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof(struct mwebcam));
	spca50x->mode_cam[VGA].width = 640;
	spca50x->mode_cam[VGA].height = 480;
	spca50x->mode_cam[VGA].t_palette =
	    P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[VGA].pipe = 1023;
	spca50x->mode_cam[VGA].method = 0;
	spca50x->mode_cam[VGA].mode = 1;
	spca50x->mode_cam[PAL].width = 384;
	spca50x->mode_cam[PAL].height = 288;
	spca50x->mode_cam[PAL].t_palette =
	    P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[PAL].pipe = 1023;
	spca50x->mode_cam[PAL].method = 1;
	spca50x->mode_cam[PAL].mode = 1;
	spca50x->mode_cam[SIF].width = 352;
	spca50x->mode_cam[SIF].height = 288;
	spca50x->mode_cam[SIF].t_palette =
	    P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[SIF].pipe = 1023;
	spca50x->mode_cam[SIF].method = 1;
	spca50x->mode_cam[SIF].mode = 1;
	spca50x->mode_cam[CIF].width = 320;
	spca50x->mode_cam[CIF].height = 240;
	spca50x->mode_cam[CIF].t_palette =
	    P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
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
	    P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[QSIF].pipe = 896;
	spca50x->mode_cam[QSIF].method = 1;
	spca50x->mode_cam[QSIF].mode = 2;
	break;
    case BRIDGE_SPCA533:
	memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof(struct mwebcam));
	spca50x->mode_cam[CUSTOM].width = 464;
	spca50x->mode_cam[CUSTOM].height = 480;
	spca50x->mode_cam[CUSTOM].t_palette =
	    P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[CUSTOM].pipe = 1023;
	spca50x->mode_cam[CUSTOM].method = 0;
	spca50x->mode_cam[CUSTOM].mode = 1;
	spca50x->mode_cam[PAL].width = 384;
	spca50x->mode_cam[PAL].height = 288;
	spca50x->mode_cam[PAL].t_palette =
	    P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[PAL].pipe = 1023;
	spca50x->mode_cam[PAL].method = 1;
	spca50x->mode_cam[PAL].mode = 1;
	spca50x->mode_cam[SIF].width = 352;
	spca50x->mode_cam[SIF].height = 288;
	spca50x->mode_cam[SIF].t_palette =
	    P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[SIF].pipe = 1023;
	spca50x->mode_cam[SIF].method = 1;
	spca50x->mode_cam[SIF].mode = 1;
	spca50x->mode_cam[CIF].width = 320;
	spca50x->mode_cam[CIF].height = 240;
	spca50x->mode_cam[CIF].t_palette =
	    P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[CIF].pipe = 1023;
	spca50x->mode_cam[CIF].method = 0;
	spca50x->mode_cam[CIF].mode = 2;
	spca50x->mode_cam[QPAL].width = 192;
	spca50x->mode_cam[QPAL].height = 144;
	spca50x->mode_cam[QPAL].t_palette =
	    P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[QPAL].pipe = 1023;
	spca50x->mode_cam[QPAL].method = 1;
	spca50x->mode_cam[QPAL].mode = 2;
	spca50x->mode_cam[QSIF].width = 176;
	spca50x->mode_cam[QSIF].height = 144;
	spca50x->mode_cam[QSIF].t_palette =
	    P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[QSIF].pipe = 1023;
	spca50x->mode_cam[QSIF].method = 1;
	spca50x->mode_cam[QSIF].mode = 2;
	break;
    case BRIDGE_SPCA504C:
	memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof(struct mwebcam));
	spca50x->mode_cam[VGA].width = 640;
	spca50x->mode_cam[VGA].height = 480;
	spca50x->mode_cam[VGA].t_palette =
	    P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[VGA].pipe = 1023;
	spca50x->mode_cam[VGA].method = 0;
	spca50x->mode_cam[VGA].mode = 1;
	spca50x->mode_cam[PAL].width = 384;
	spca50x->mode_cam[PAL].height = 288;
	spca50x->mode_cam[PAL].t_palette =
	    P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[PAL].pipe = 1023;
	spca50x->mode_cam[PAL].method = 1;
	spca50x->mode_cam[PAL].mode = 1;
	spca50x->mode_cam[SIF].width = 352;
	spca50x->mode_cam[SIF].height = 288;
	spca50x->mode_cam[SIF].t_palette =
	    P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[SIF].pipe = 1023;
	spca50x->mode_cam[SIF].method = 0;
	spca50x->mode_cam[SIF].mode = 2;
	spca50x->mode_cam[CIF].width = 320;
	spca50x->mode_cam[CIF].height = 240;
	spca50x->mode_cam[CIF].t_palette =
	    P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[CIF].pipe = 896;
	spca50x->mode_cam[CIF].method = 0;
	spca50x->mode_cam[CIF].mode = 3;
	spca50x->mode_cam[QPAL].width = 192;
	spca50x->mode_cam[QPAL].height = 144;
	spca50x->mode_cam[QPAL].t_palette =
	    P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[QPAL].pipe = 896;
	spca50x->mode_cam[QPAL].method = 1;
	spca50x->mode_cam[QPAL].mode = 3;
	spca50x->mode_cam[QSIF].width = 176;
	spca50x->mode_cam[QSIF].height = 144;
	spca50x->mode_cam[QSIF].t_palette =
	    P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
	spca50x->mode_cam[QSIF].pipe = 768;
	spca50x->mode_cam[QSIF].method = 0;
	spca50x->mode_cam[QSIF].mode = 4;
	break;
    }
    spca50x->qindex = 5;
    return 0;
}

/****************************************************************************************/
static void spca504B_SetSizeType(struct usb_spca50x *spca50x)
{
    __u8 Size;
    __u8 Type;
    int rc;
    Size = spca50x->mode;
    Type = 0;
    switch (spca50x->bridge) {
    case BRIDGE_SPCA533:{
	    spca5xxRegWrite(spca50x->dev, 0x31, 0, 0, NULL, 0);
	    spca504B_WaitCmdStatus(spca50x);
	    rc = spca504B_PollingDataReady(spca50x->dev);
	    spca50x_GetFirmware(spca50x);

	    Type = 2;
	    spca5xxRegWrite(spca50x->dev, 0x24, 0, 8, &Type, 1);
	    spca5xxRegRead(spca50x->dev, 0x24, 0, 8, &Type, 1);

	    spca5xxRegWrite(spca50x->dev, 0x25, 0, 4, &Size, 1);
	    spca5xxRegRead(spca50x->dev, 0x25, 0, 4, &Size, 1);
	    rc = spca504B_PollingDataReady(spca50x->dev);

	    /* Init the cam width height with some values get on init ? */
	    spca5xxRegWrite(spca50x->dev, 0x31, 0, 4, NULL, 0);
	    spca504B_WaitCmdStatus(spca50x);
	    rc = spca504B_PollingDataReady(spca50x->dev);

	}
	break;
    case BRIDGE_SPCA504B:
    case BRIDGE_SPCA536:
	{
	    Type = 6;
	    spca5xxRegWrite(spca50x->dev, 0x25, 0, 4, &Size, 1);
	    spca5xxRegRead(spca50x->dev, 0x25, 0, 4, &Size, 1);
	    spca5xxRegWrite(spca50x->dev, 0x27, 0, 0, &Type, 1);
	    spca5xxRegRead(spca50x->dev, 0x27, 0, 0, &Type, 1);

	    rc = spca504B_PollingDataReady(spca50x->dev);
	}
	break;
    case BRIDGE_SPCA504:
	Size += 3;
	if (spca50x->desc == AiptekMiniPenCam13) {
	    /* spca504a aiptek */
	    spca504A_acknowledged_command(spca50x, 0x8, Size, 0,
					  (0x80 | (Size & 0x0F)), 1);
	    spca504A_acknowledged_command(spca50x, 1, 3, 0, 0x9F, 0);
	} else {
	    spca504_acknowledged_command(spca50x, 0x8, Size, 0);
	}
	break;
    case BRIDGE_SPCA504C:
	spca50x_reg_write(spca50x->dev, 0xa0, (0x0500 | (Size & 0x0F)), 0x0);	// capture mode
	spca50x_reg_write(spca50x->dev, 0x20, 0x1,
			  (0x0500 | (Size & 0x0F)));
	break;
    }
    return;
}
static void
spca504_acknowledged_command(struct usb_spca50x *spca50x,
			     __u16 reg, __u16 idx, __u16 val)
{
    __u8 notdone = 0;

    spca50x_reg_write(spca50x->dev, reg, idx, val);
    notdone = spca50x_reg_read(spca50x->dev, 0x01, 0x0001, 1);
    spca50x_reg_write(spca50x->dev, reg, idx, val);

    PDEBUG(5, "before wait 0x%x", notdone);

    wait_ms(200);
    notdone = spca50x_reg_read(spca50x->dev, 0x01, 0x0001, 1);
    PDEBUG(5, "after wait 0x%x", notdone);

    return;
}

static void
spca504A_acknowledged_command(struct usb_spca50x *spca50x,
			      __u16 reg,
			      __u16 idx, __u16 val, __u8 stat, __u8 count)
{
    __u8 status;
    __u8 endcode;


    spca50x_reg_write(spca50x->dev, reg, idx, val);
    status = spca50x_reg_read(spca50x->dev, 0x01, 0x0001, 1);
    endcode = stat;
    PDEBUG(5, "Status 0x%x Need 0x%x", status, stat);
    if (count) {
	while (1) {
	    wait_ms(10);
	    /* gsmart mini2 write a each wait setting 1 ms is enought */
	    //spca50x_reg_write(spca50x->dev,reg,idx,val);
	    status = spca50x_reg_read(spca50x->dev, 0x01, 0x0001, 1);
	    if (status == endcode) {
		PDEBUG(5, "status 0x%x after wait 0x%x", status, count);
		break;
	    }
	    count++;
	    if (count > 200)
		break;

	}
    }
    return;
}
static void spca504_wait_status(struct usb_spca50x *spca50x)
{
    int ret = 256;
    do {
	/* With this we get the status, when return 0 it's all ok */
	ret = spca50x_reg_read(spca50x->dev, 0x06, 0x00, 1);
    } while (ret--);
}
static void spca50x_GetFirmware(struct usb_spca50x *spca50x)
{
    __u8 FW[5] = { 0, 0, 0, 0, 0 };
    __u8 ProductInfo[64];

    spca5xxRegRead(spca50x->dev, 0x20, 0, 0, FW, 5);
    PDEBUG(0, "FirmWare : %d %d %d %d %d ", FW[0], FW[1], FW[2], FW[3],
	   FW[4]);
    spca5xxRegRead(spca50x->dev, 0x23, 0, 0, ProductInfo, 64);
    spca5xxRegRead(spca50x->dev, 0x23, 0, 1, ProductInfo, 64);
    return;
}


static int spca504B_PollingDataReady(struct usb_device *dev)
{
    __u8 DataReady = 0;
    int count = 0;
    while (1) {
	spca5xxRegRead(dev, 0x21, 0, 0, &DataReady, 1);
	if ((DataReady & 0x01) == 0)
	    break;
	wait_ms(10);
	count++;
	if (count > 10)
	    break;

    }
    return DataReady;
}


static void spca504B_WaitCmdStatus(struct usb_spca50x *spca50x)
{
    __u8 DataReady = 0;
    int ReqDone;
    int count = 0;
    while (1) {
	spca5xxRegRead(spca50x->dev, 0x21, 0, 1, &DataReady, 1);

	if (DataReady) {
	    DataReady = 0;
	    spca5xxRegWrite(spca50x->dev, 0x21, 0, 1, &DataReady, 1);
	    spca5xxRegRead(spca50x->dev, 0x21, 0, 1, &DataReady, 1);
	    ReqDone = spca504B_PollingDataReady(spca50x->dev);
	    break;
	}
	wait_ms(10);
	count++;
	if (count > 50)
	    break;

    }
    return;
}


static void spca504B_setQtable(struct usb_spca50x *spca50x)
{
    __u8 Data = 3;
    int rc;
    spca5xxRegWrite(spca50x->dev, 0x26, 0, 0, &Data, 1);
    spca5xxRegRead(spca50x->dev, 0x26, 0, 0, &Data, 1);
    rc = spca504B_PollingDataReady(spca50x->dev);
    return;
}
static void sp5xx_initContBrigHueRegisters(struct usb_spca50x *spca50x)
{
    int rc;
    int pollreg = 1;
    switch (spca50x->bridge) {
    case BRIDGE_SPCA504:
    case BRIDGE_SPCA504C:
	pollreg = 0;
    case BRIDGE_SPCA533:
    case BRIDGE_SPCA504B:
	spca5xxRegWrite(spca50x->dev, 0, 0, 0x21a7, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, 0x20, 0x21a8, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, 0, 0x21ad, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, 1, 0x21ac, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, 0x20, 0x21ae, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, 0, 0x21a3, NULL, 0);
	break;
    case BRIDGE_SPCA536:
	spca5xxRegWrite(spca50x->dev, 0, 0, 0x20f0, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, 0x21, 0x20f1, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, 0x40, 0x20f5, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, 1, 0x20f4, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, 0x40, 0x20f6, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, 0, 0x2089, NULL, 0);
	break;
    }
    if (pollreg)
	rc = spca504B_PollingDataReady(spca50x->dev);
    return;
}
static int sp5xxfw2_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum,int *datalength)
{
	switch (spca50x->bridge){
	case BRIDGE_SPCA533:
	    {
		if (cdata[0] == SPCA50X_SEQUENCE_DROP) {
		    if (cdata[1] == 0x01) {
		        *iPix = SPCA533_OFFSET_DATA;
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
	    break;
	case BRIDGE_SPCA536:
	    {
		if (cdata[0] == SPCA50X_SEQUENCE_DROP) {
		        *iPix = SPCA536_OFFSET_DATA;
		        *datalength -= *iPix;
		    return 0;
		} else {
		     *iPix = 2;
		     *datalength -= *iPix;
		    return (seqnum+1);
		}
	    }
	    break;
	case BRIDGE_SPCA504:
	case BRIDGE_SPCA504B:
	        switch (cdata[0]) {
		case 0xfe:
		        *iPix =SPCA50X_OFFSET_DATA;
		        *datalength -= *iPix;
		    return 0;
		    break;
		case SPCA50X_SEQUENCE_DROP:
		    /* drop packet */
		    return -1;
		default:
		     *iPix = 1;
		     *datalength -= *iPix;
		    return (seqnum+1);
		    break;
		}
	break;
	case BRIDGE_SPCA504C:
	    {
		switch (cdata[0]) {
		case 0xfe:
		        *iPix = SPCA504_PCCAM600_OFFSET_DATA;
		        *datalength -= *iPix;
		    return 0;
		    break;
		case SPCA50X_SEQUENCE_DROP:
		    /* drop packet */
		    return -1;
		default:
		     *iPix = 1;
		     *datalength -= *iPix;
		    return (seqnum+1);
		    break;
		}
	    }
	    break;
	 default:
	 return -1;
	 break;
	}
}
#endif				//SP5XXFW2
