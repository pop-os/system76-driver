
#ifndef ZC3XXUSB_H
#define ZC3XXUSB_H
/****************************************************************************
#	 	Z-star zc301 zc302 P library                                #
# 		Copyright (C) 2004 Michel Xhaard   mxhaard@magic.fr         #
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
#include "tas5130c.h"
#include "tas5130c_vf0250.h"
#include "icm105a.h"
#include "hdcs2020.h"
#include "hv7131b.h"
#include "pb0330.h"
#include "hv7131c.h"
#include "cs2102.h"
#include "pas106b.h"
#include "ov7630c.h"
/*******************     Camera Interface   ***********************/
static __u16 zc3xx_getbrightness(struct usb_spca50x *spca50x);
static __u16 zc3xx_getcontrast(struct usb_spca50x *spca50x);
static __u16 zc3xx_getcolors(struct usb_spca50x *spca50x);
static void zc3xx_setbrightness(struct usb_spca50x *spca50x);
static void zc3xx_setcontrast(struct usb_spca50x *spca50x);
static void zc3xx_setcolors(struct usb_spca50x *spca50x);
static int zc3xx_init(struct usb_spca50x *spca50x);
static void zc3xx_start(struct usb_spca50x *spca50x);
static void zc3xx_stop0(struct usb_spca50x *spca50x);
static void zc3xx_stopN(struct usb_spca50x *spca50x);
static int zc3xx_config(struct usb_spca50x *spca50x);
static void zc3xx_shutdown(struct usb_spca50x *spca50x);
static void zc3xx_setAutobright(struct usb_spca50x *spca50x);
static void zc3xx_setquality(struct usb_spca50x *spca50x);
static int zc3xx_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength);
/*******************      Banding flilter   ***********************/
static void zc3xx_set50HZ(struct usb_spca50x *spca50x);
static void zc3xx_set60HZ(struct usb_spca50x *spca50x);
static void zc3xx_set50HZScale(struct usb_spca50x *spca50x);
static void zc3xx_set60HZScale(struct usb_spca50x *spca50x);
static void zc3xx_setNoFliker(struct usb_spca50x *spca50x);
static void zc3xx_setNoFlikerScale(struct usb_spca50x *spca50x);
/*******************     Camera Private     ***********************/
static void zc3xx_stopN(struct usb_spca50x *spca50x){}
/******************************************************************/
static struct cam_operation fzc3xx = {
 	.initialize = zc3xx_init,
	.configure = zc3xx_config,
	.start = zc3xx_start,
	.stopN = zc3xx_stopN,
	.stop0 = zc3xx_stop0,
	.get_bright = zc3xx_getbrightness,
	.set_bright = zc3xx_setbrightness,
	.get_contrast = zc3xx_getcontrast,
	.set_contrast = zc3xx_setcontrast,
	.get_colors = zc3xx_getcolors,
	.set_colors = zc3xx_setcolors,
	.set_autobright = zc3xx_setAutobright,
	.set_quality = zc3xx_setquality,
	.cam_shutdown = zc3xx_shutdown,
	.sof_detect = zc3xx_sofdetect,
	.set_50HZ   = zc3xx_set50HZ,
	.set_60HZ   = zc3xx_set60HZ,
	.set_50HZScale   = zc3xx_set50HZScale,
	.set_60HZScale   = zc3xx_set60HZScale,
	.set_NoFliker    = zc3xx_setNoFliker,
	.set_NoFlikerScale    = zc3xx_setNoFlikerScale,	
 };
 
enum {
    SensorId = 0,
    reg8d,
    val8d,
    SensorReg1,
    valSreg1L,
    valSreg1H,
    SensorReg2,
    valSreg2L,
    valSreg2H,
    totval,
};
#define VGATOT 9
static __u8 zcxxi2cSensor[VGATOT][totval] = {
    {0x00, 0xff, 0xff, 0x01, 0xaa, 0x00, 0xff, 0xff, 0xff},	// HV7131B
    {0x04, 0xff, 0xff, 0x01, 0xaa, 0x00, 0xff, 0xff, 0xff},	// CS2102
    {0x06, 0x8d, 0x08, 0x11, 0xaa, 0x00, 0xff, 0xff, 0xff},
    {0x08, 0xff, 0xff, 0x1c, 0x00, 0x00, 0x15, 0xaa, 0x00},	// HDCS2020 ?
    {0x0a, 0xff, 0xff, 0x07, 0xaa, 0xaa, 0xff, 0xff, 0xff},	// MI330 PB330
    {0x0c, 0xff, 0xff, 0x01, 0xaa, 0x00, 0xff, 0xff, 0xff},	// ICM105
    {0x0e, 0x8d, 0x08, 0x03, 0xaa, 0x00, 0xff, 0xff, 0xff},	// pas102
    {0x02, 0xff, 0xff, 0x01, 0xaa, 0x00, 0xff, 0xff, 0xff},
    {0x06, 0x8b, 0xa1, 0x12, 0x80, 0x00, 0x0a, 0x0b, 0xff},	// OV7630c
};

#define SIFTOT 1
static __u8 zcxxi2cSensorSIF[SIFTOT][totval] = {
#if 0
    {0x01, 0xff, 0xff, 0x01, 0xaa, 0x00, 0xff, 0xff, 0xff},	// corrupt with 0x00 hv7131b reg 0 return 0x01 readonly
    {0x05, 0xff, 0xff, 0x01, 0xaa, 0x00, 0xff, 0xff, 0xff},
    {0x07, 0x8d, 0x08, 0x11, 0xaa, 0x00, 0xff, 0xff, 0xff},
    {0x09, 0xff, 0xff, 0x1c, 0x00, 0x00, 0x15, 0xaa, 0x00},	// corrupt with 0x08 hdcs2020 reg 0 return 0x18 readonly
    {0x0b, 0xff, 0xff, 0x07, 0xaa, 0xaa, 0xff, 0xff, 0xff},
    {0x0d, 0xff, 0xff, 0x01, 0x11, 0x00, 0xff, 0xff, 0xff},	// corrupt with 0x0c ICM105 reg 0 is writable
#endif
    {0x0f, 0x8d, 0x08, 0x03, 0xaa, 0x00, 0xff, 0xff, 0xff},	// PAS106 reg3 did not write with 0x0e !conflict PAS102 
};
static __u8 zcxx3wrSensor[][5] = {
    {0x8b, 0xb3, 0x11, 0x12, 0xff},	// HV7131R
    {0x8b, 0x91, 0x14, 0x15, 0x16},
    {0x8b, 0xe0, 0x14, 0x15, 0x16},
    {0, 0, 0, 0, 0}
};
static __u16 zcxx_i2cRead(struct usb_device *dev, __u8 reg)
{
    __u8 retbyte = 0;
    __u8 retval[] = { 0, 0 };

    spca5xxRegWrite(dev, 0xa0, reg, 0x92, NULL, 0);
    spca5xxRegWrite(dev, 0xa0, 0x02, 0x90, NULL, 0);	// <-read command
    spca5xxRegRead(dev, 0xa1, 0x01, 0x0091, &retbyte, 1);	// read status
    spca5xxRegRead(dev, 0xa1, 0x01, 0x0095, &retval[0], 1);	// read Lowbyte
    spca5xxRegRead(dev, 0xa1, 0x01, 0x0096, &retval[1], 1);	// read Hightbyte
    return ((retval[1] << 8) | retval[0]);
}
static __u8 zcxx_i2cWrite(struct usb_device *dev, __u8 reg, __u8 valL,
			  __u8 valH)
{
    __u8 retbyte = 0;
    spca5xxRegWrite(dev, 0xa0, reg, 0x92, NULL, 0);
    spca5xxRegWrite(dev, 0xa0, valL, 0x93, NULL, 0);
    spca5xxRegWrite(dev, 0xa0, valH, 0x94, NULL, 0);
    spca5xxRegWrite(dev, 0xa0, 0x01, 0x90, NULL, 0);	// <-write command
    spca5xxRegRead(dev, 0xa1, 0x01, 0x0091, &retbyte, 1);	// read status
    return (retbyte);
}
static int zcxx_probeSensor(struct usb_spca50x *spca50x)
{
    int i, j;
    __u8 retbyte = 0;
    __u16 checkword = 0;
   __u16 checkid = 0xffff;
/* check i2c */
/* check SIF */
    for (i = 0; i < SIFTOT; i++) {
        checkword = 0;
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0000, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, zcxxi2cSensorSIF[i][SensorId],
			0x0010, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0001, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x03, 0x0012, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0012, NULL, 0);
	wait_ms(2);
	if (zcxxi2cSensorSIF[i][reg8d] == 0x8d){
	    spca5xxRegWrite(spca50x->dev, 0xa0, zcxxi2cSensorSIF[i][val8d],
			    0x008d, NULL, 0);
	wait_ms(150);
	checkword = ((zcxx_i2cRead(spca50x->dev,0x00) & 0x0f) << 4) 
	               | ((zcxx_i2cRead(spca50x->dev,0x01) & 0xf0) >> 4 );
	
	    if (checkword == 0x07){
	        spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0000, NULL, 0);
		spca5xxRegWrite(spca50x->dev, 0xa0, 0x03, 0x003a, NULL, 0);
		spca5xxRegWrite(spca50x->dev, 0xa0, 0x0c, 0x003b, NULL, 0);
		spca5xxRegWrite(spca50x->dev, 0xa0, 0x08, 0x0038, NULL, 0);
	    return zcxxi2cSensorSIF[i][SensorId];
	    } 	    
	}
	retbyte =
	    zcxx_i2cWrite(spca50x->dev, zcxxi2cSensorSIF[i][SensorReg1],
			  zcxxi2cSensorSIF[i][valSreg1L],
			  zcxxi2cSensorSIF[i][valSreg1H]);
	wait_ms(2);
	retbyte =
	    (zcxx_i2cRead(spca50x->dev, zcxxi2cSensorSIF[i][SensorReg1])) &
	    0xff;
	wait_ms(2);
	PDEBUG(1, "sensor answer1  %d ", retbyte);
	if (retbyte != zcxxi2cSensorSIF[i][valSreg1L])
	    continue;
	if (zcxxi2cSensorSIF[i][SensorReg2] != 0xff) {
	    retbyte =
		zcxx_i2cWrite(spca50x->dev,
			      zcxxi2cSensorSIF[i][SensorReg2],
			      zcxxi2cSensorSIF[i][valSreg2L],
			      zcxxi2cSensorSIF[i][valSreg2H]);
	    retbyte =
		(zcxx_i2cRead
		 (spca50x->dev, zcxxi2cSensorSIF[i][SensorReg2])) & 0xff;
	    PDEBUG(1, "sensor answer2  %d ", retbyte);
	    if (retbyte == zcxxi2cSensorSIF[i][valSreg2L])
		return zcxxi2cSensorSIF[i][SensorId];
	}
    }
/* check VGA */
    for (i = 0; i < VGATOT; i++) {
	if ((zcxxi2cSensor[i][reg8d] == 0x8b)
	    && (zcxxi2cSensor[i][val8d] == 0xa1)) {
	    /* code for stephane sensor ov7630c */
	    checkword = 0;
	    spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0000, NULL, 0);
	    spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0001, NULL, 0);
	    spca5xxRegWrite(spca50x->dev, 0xa0, zcxxi2cSensor[i][SensorId],
			    0x0010, NULL, 0);
	    spca5xxRegWrite(spca50x->dev, 0xa0, zcxxi2cSensor[i][val8d],
			    0x008b, NULL, 0);
	    spca5xxRegWrite(spca50x->dev, 0xa0, 0x08, 0x008d, NULL, 0);
	    wait_ms(150);
	    spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0012, NULL, 0);
	    retbyte =
		zcxx_i2cWrite(spca50x->dev, zcxxi2cSensor[i][SensorReg1],
			      zcxxi2cSensor[i][valSreg1L],
			      zcxxi2cSensor[i][valSreg1H]);

	    retbyte =
		(zcxx_i2cRead(spca50x->dev, zcxxi2cSensor[i][SensorReg2]))
		& 0xff;
	    checkword = retbyte << 8;
	    checkword |= ((zcxx_i2cRead(spca50x->dev, 0x0b)) & 0xff);
	    if (checkword == 0x7631) {
		PDEBUG(0, "sensor answervga  0x%04X ", checkword);
		spca5xxRegWrite(spca50x->dev, 0xa0,
				zcxxi2cSensor[i][SensorId], 0x0010, NULL,
				0);
		return zcxxi2cSensor[i][SensorId];
	    }
	    continue;
	}
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0000, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, zcxxi2cSensor[i][SensorId],
			0x0010, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0001, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x03, 0x0012, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0012, NULL, 0);
	wait_ms(2);
	if (zcxxi2cSensor[i][reg8d] == 0x8d)
	    spca5xxRegWrite(spca50x->dev, 0xa0, zcxxi2cSensor[i][val8d],
			    0x008d, NULL, 0);
	retbyte =
	    zcxx_i2cWrite(spca50x->dev, zcxxi2cSensor[i][SensorReg1],
			  zcxxi2cSensor[i][valSreg1L],
			  zcxxi2cSensor[i][valSreg1H]);
	if (zcxxi2cSensor[i][SensorReg2] != 0xff) {
	    retbyte =
		zcxx_i2cWrite(spca50x->dev, zcxxi2cSensor[i][SensorReg2],
			      zcxxi2cSensor[i][valSreg2L],
			      zcxxi2cSensor[i][valSreg2H]);
	    retbyte =
		(zcxx_i2cRead(spca50x->dev, zcxxi2cSensor[i][SensorReg2]))
		& 0xff;
	} else {
	checkid = (zcxx_i2cRead(spca50x->dev,0x00)) & 0xff;
	PDEBUG(1, "check sensor id  0x%04X ", checkid);
	    retbyte =
		(zcxx_i2cRead(spca50x->dev, zcxxi2cSensor[i][SensorReg1]))
		& 0xff;
	if(checkid == 2) // Who is here, that is a surprised :)
	        continue ;
	}

	PDEBUG(1, "sensor answervga  %d ", retbyte);
	if (retbyte != 0)
	    return zcxxi2cSensor[i][SensorId];
    }
/* check 3 wires bus */
    i = 0;
    while (zcxx3wrSensor[i][0]) {
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x02, 0x0010, NULL, 0);
	spca5xxRegRead(spca50x->dev, 0xa1, 0x01, 0x0010, &retbyte, 1);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0000, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x00, 0x0010, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0001, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, zcxx3wrSensor[i][1],
			zcxx3wrSensor[i][0], NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x03, 0x0012, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0012, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x05, 0x0012, NULL, 0);
	for (j = 2; j < 5; j++) {
	    if (zcxx3wrSensor[i][j] != 0xff) {
		retbyte =
		    (zcxx_i2cRead(spca50x->dev, zcxx3wrSensor[i][j])) &
		    0xff;
		if (retbyte != 0)
		    return (i | 0x10);
	    }
	}
	if (zcxx3wrSensor[i][1] == 0x91) {
	    /* check Aurelien Jurgen sensor */
	    checkword = 0;
	    spca5xxRegWrite(spca50x->dev, 0xa0, 0x02, 0x0010, NULL, 0);
	    spca5xxRegRead(spca50x->dev, 0xa1, 0x01, 0x000b, &retbyte, 1);
	    checkword = retbyte << 8;
	    spca5xxRegRead(spca50x->dev, 0xa1, 0x01, 0x000a, &retbyte, 1);
	    checkword |= retbyte;
	    PDEBUG(1, "sensor 3w Vga ??? 0x%04X ", (checkword & 0xffff));
	    if (checkword == 0xc001 || checkword == 0xe001 || checkword == 0x8001) {
		spca50x->chip_revision = checkword;
		spca5xxRegRead(spca50x->dev, 0xa1, 0x01, 0x0010, &retbyte,
			       1);
		spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0000, NULL, 0);
		spca5xxRegWrite(spca50x->dev, 0xa0, 0x0d, 0x003a, NULL, 0);
		spca5xxRegWrite(spca50x->dev, 0xa0, 0x02, 0x003b, NULL, 0);
		spca5xxRegWrite(spca50x->dev, 0xa0, 0x00, 0x0038, NULL, 0);
		return 0x13;
	    }

	}
	i++;
    }
    return (-1);
}

static __u16 zc3xxWriteVector(struct usb_spca50x *spca50x, __u16 data[][3])
{
    struct usb_device *dev = spca50x->dev;
    int err = 0;
    int i = 0;
    __u8 buffread;
    while (data[i][0]) {
	if (data[i][0] == 0xa0) {
	    /* write registers */
	    spca5xxRegWrite(dev, data[i][0], data[i][1], data[i][2], NULL,
			    0);
	} else {
	    /* read status */
	    spca5xxRegRead(dev, data[i][0], data[i][1], data[i][2],
			   &buffread, 1);
	}
	i++;
	udelay(1000);
    }

    return err;
}

#define CLAMP(x) (unsigned char)(((x)>0xFF)?0xff:(((x)<1)?1:(x)))

static __u8 Tgamma_default[16] =
    { 0x13, 0x38, 0x59, 0x79, 0x92, 0xa7, 0xb9, 0xc8, 0xd4, 0xdf, 0xe7, 0xee, 0xf4, 0xf9, 0xfc, 0xff };
static __u8 Tgradient_default[16] =
    { 0x26, 0x22, 0x20, 0x1c, 0x16, 0x13, 0x10, 0x0d, 0x0b, 0x09, 0x07, 0x06, 0x05, 0x04, 0x03, 0x02 };
static __u8 Tgamma_VF0250[16] =
    { 0x04, 0x16, 0x30, 0x4e, 0x68, 0x81, 0x98, 0xac, 0xbe, 0xcd, 0xda, 0xe4, 0xed, 0xf5, 0xfb, 0xff };
static __u8 Tgradient_VF0250[16] =
    { 0x00, 0x16, 0x1b, 0x1c, 0x19, 0x18, 0x15, 0x12, 0x10, 0x0d, 0x0b, 0x09, 0x08, 0x06, 0x05, 0x00 };
static __u8 Tgamma_CS2102[16] =
    { 0x24, 0x44, 0x64, 0x84, 0x9d, 0xb2, 0xc4, 0xd3, 0xe0, 0xeb, 0xf4, 0xff, 0xff, 0xff, 0xff ,0xff }; 
static __u8 Tgradient_CS2102[16] = 
    { 0x18, 0x20, 0x20, 0x1c, 0x16, 0x13, 0x10, 0x0e, 0x0b, 0x09, 0x07, 0x00, 0x00, 0x00, 0x00, 0x01 };

static __u16 zc3xx_getbrightness(struct usb_spca50x *spca50x)
{
    spca50x->brightness = 0x80 << 8;
    spca50x->contrast = 0x80 << 8;
    return spca50x->brightness;
}
static __u16 zc3xx_getcontrast(struct usb_spca50x *spca50x)
{
    return spca50x->contrast;
}
static void zc3xx_setbrightness(struct usb_spca50x *spca50x)
{
    __u8 brightness;
    brightness = spca50x->brightness >> 8;
    spca5xxRegWrite(spca50x->dev, 0xa0, brightness, 0x011d, NULL, 0);
    if (brightness < 0x70) {
	spca5xxRegWrite(spca50x->dev, 0xa0, brightness + 0x10, 0x018d,
			NULL, 0);
    } else {
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x80, 0x018d, NULL, 0);
    }

}
static void zc3xx_setcontrast(struct usb_spca50x *spca50x)
{

    __u16 contrast;
    __u8 *   Tgamma = Tgamma_default;
    __u8 *   Tgradient = Tgradient_default;
    int gm0 = 0;
    int gr0 = 0;
    int index = 0;
    int i;

    switch (spca50x->sensor) {
     case SENSOR_TAS5130C_VF0250:
       Tgamma = Tgamma_VF0250;
       Tgradient = Tgradient_VF0250;
     break;
     case SENSOR_CS2102:
       Tgamma = Tgamma_CS2102;
       Tgradient = Tgradient_CS2102;
     break;
    }

    /* now get the index of gamma table */
    contrast = zc3xx_getcontrast(spca50x);
    if ((index = contrast >> 13) > 6)
	index = 6;
    PDEBUG(2, "starting new table index %d ", index);
    for (i = 0; i < 16; i++) {
	gm0 = Tgamma[i] * index >> 2;
	gr0 = Tgradient[i] * index >> 2;
	spca5xxRegWrite(spca50x->dev, 0xa0, CLAMP(gm0), 0x0120 + i, NULL, 0);	//brightness
	spca5xxRegWrite(spca50x->dev, 0xa0, CLAMP(gr0), 0x0130 + i, NULL, 0);	// contrast
	//PDEBUG(0,"i %d gamma %d gradient %d",i ,Tgamma[i],Tgradient[i]);
    }

}



static int zc3xx_init(struct usb_spca50x *spca50x)
{
    spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0000, NULL, 0);
    return 0;
}
static void set_zc3xxVGA(struct usb_spca50x *spca50x)
{
    memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof(struct mwebcam));
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
}
static void set_zc3xxSIF(struct usb_spca50x *spca50x)
{
    memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof(struct mwebcam));
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
	P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QSIF].pipe = 1023;
    spca50x->mode_cam[QSIF].method = 0;
    spca50x->mode_cam[QSIF].mode = 1;
}

static int zc3xx_config(struct usb_spca50x *spca50x)
{

    int sensor = 0;
    __u8 bsensor = 0;
    spca50x->qindex = 1;
    PDEBUG(0, "Sensor ID:%d",spca50x->sensor);

    sensor = zcxx_probeSensor(spca50x);
    
    switch (sensor) {
    case -1:
         if(spca50x->sensor == SENSOR_TAS5130C_VF0250) {
            PDEBUG(0, "Find Sensor Tas5130 (VF0250)");
	    set_zc3xxVGA(spca50x);
        } else { 	
	    PDEBUG(0, "Find Sensor UNKNOW_0 force Tas5130");
	    spca50x->sensor = SENSOR_TAS5130CXX;
	    set_zc3xxVGA(spca50x);
	}
	break;
    case 0:
	PDEBUG(0, "Find Sensor HV7131B");
	spca50x->sensor = SENSOR_HV7131B;
	set_zc3xxVGA(spca50x);
	break;
    case 1:
	PDEBUG(0, "Find Sensor SIF UNKNOW_1");
	break;
    case 0x02:
	PDEBUG(0, "Find Sensor UNKNOW_2");
	break;
    case 0x04:
	PDEBUG(0, "Find Sensor CS2102");
	spca50x->sensor = SENSOR_CS2102;
	set_zc3xxVGA(spca50x);
	break;
    case 5:
	PDEBUG(0, "Find Sensor SIF UNKNOW_5");
	break;
    case 0x06:
	PDEBUG(0, "Find Sensor OV7630C");
	spca50x->sensor = SENSOR_OV7630C;
	set_zc3xxVGA(spca50x);
	break;
    case 7:
	PDEBUG(0, "Find Sensor SIF UNKNOW_7");
	break;
    case 0x08:
	PDEBUG(0, "Find Sensor HDCS2020(b)");
	spca50x->sensor = SENSOR_HDCS2020b;
	set_zc3xxVGA(spca50x);
	break;
    case 9:
	PDEBUG(0, "Find Sensor SIF UNKNOW_9");
	break;
    case 0x0a:
	PDEBUG(0, "Find Sensor PB0330");
	spca50x->sensor = SENSOR_PB0330;
	set_zc3xxVGA(spca50x);
	break;
    case 0x0b:
	PDEBUG(0, "Find Sensor SIF UNKNOW_b");
	break;
    case 0x0c:
	PDEBUG(0, "Find Sensor ICM105T");
	spca50x->sensor = SENSOR_ICM105A;
	set_zc3xxVGA(spca50x);
	break;
    case 0x0d:
	PDEBUG(0, "Find Sensor SIF UNKNOW_d");
	break;
    case 0x0e:
	PDEBUG(0, "Find Sensor PAS202BCB");
	spca50x->sensor = SENSOR_HDCS2020;
	set_zc3xxVGA(spca50x);
	break;
    case 0x0f:
	PDEBUG(0, "Find Sensor PAS106");
	spca50x->sensor = SENSOR_PAS106;
	set_zc3xxSIF(spca50x);
	break;
    case 0x10:
	PDEBUG(0, "Find Sensor TAS5130");
	spca50x->sensor = SENSOR_TAS5130CXX;
	set_zc3xxVGA(spca50x);
	break;
    case 0x11:
	PDEBUG(0, "Find Sensor HV7131R(c)");
	spca50x->sensor = SENSOR_HV7131C;
	set_zc3xxVGA(spca50x);
	break;
    case 0x12:
	PDEBUG(0, "Find Sensor TAS5130");
	spca50x->sensor = SENSOR_TAS5130CXX;
	set_zc3xxVGA(spca50x);
	break;
    case 0x13:
	PDEBUG(0, "Find Sensor MI0360");
	spca50x->sensor = SENSOR_PB0330;
	set_zc3xxVGA(spca50x);
	break;
    };

    if ((sensor == 0x02) || (sensor == 0x01) || (sensor == 0x05)
	|| (sensor == 0x07) || (sensor == 0x09) || (sensor == 0x0b)
	|| (sensor == 0x0d)) {
	PDEBUG(0,
	       "Our Sensor is unknow at the moment please report mxhaard@free.fr ");
	return -EINVAL;
    }

    if ((sensor == -1) || (sensor == 0x10) || (sensor == 0x12)) {
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x02, 0x0010, NULL, 0);
	spca5xxRegRead(spca50x->dev, 0xa1, 0x01, 0x0010, &bsensor, 1);
    } else {
	spca5xxRegWrite(spca50x->dev, 0xa0, sensor & 0x0f, 0x0010, NULL, 0);
	spca5xxRegRead(spca50x->dev, 0xa1, 0x01, 0x0010, &bsensor, 1);
    }
    /* switch the led off */
    if( sensor == 0x06 || sensor == 0x11)
      spca5xxRegWrite(spca50x->dev,0xa0,0x01,0x0000,NULL,0);

    return 0;
}
static void zc3xx_setquality(struct usb_spca50x *spca50x)
{
    __u8 quality = 0;
    __u8 frxt = 0x30;
    quality = (spca50x->qindex) & 0x0f;
    spca5xxRegWrite(spca50x->dev, 0xa0, quality, 0x0008, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0xa0, frxt, 0x0007, NULL, 0);
    switch (quality){
    case 0:
    case 1:
    case 2:
    frxt = 0xff;
    break;
    case 3:
    frxt = 0xf0;
    break;
    case 4:
    frxt = 0xe0;
    break;
    case 5:
    frxt = 0x20;
    break;
    }
    spca5xxRegWrite(spca50x->dev, 0xa0, frxt, 0x0018, NULL, 0);
    
}
static void zc3xx_setAutobright(struct usb_spca50x *spca50x)
{
    __u8 autoval = 0;
    if (spca50x->autoexpo)
	autoval = 0x42;
    else
	autoval = 0x02;
	spca5xxRegWrite(spca50x->dev, 0xa0, autoval, 0x0180, NULL, 0);
}
static void zc3xx_start(struct usb_spca50x *spca50x)
{
    int err = 0;
    /* Assume start use the good resolution from spca50x->mode */
    //err = zcxx_probeSensor(spca50x);
    switch (spca50x->sensor) {
    case SENSOR_TAS5130CXX:
	if (spca50x->mode) {
	    /* 320x240 */
	    err = zc3xxWriteVector(spca50x, tas5130cxx_start_data);
	} else {
	    /* 640x480 */
	    err = zc3xxWriteVector(spca50x, tas5130cxx_scale_data);
	}
	break;
    case SENSOR_TAS5130C_VF0250: // Firmware version 0250
	if (spca50x->mode) {
	    /* 320x240 */
	    err = zc3xxWriteVector(spca50x, tas5130c_vf0250_start_data);
	} else {
	    /* 640x480 */
	    err = zc3xxWriteVector(spca50x, tas5130c_vf0250_scale_data);
	}
	break;
    case SENSOR_ICM105A:
	if (spca50x->mode) {
	    /* 320x240 */
	    err = zc3xxWriteVector(spca50x, icm105axx_start_data);
	} else {
	    /* 640x480 */
	    err = zc3xxWriteVector(spca50x, icm105axx_scale_data);
	}
	break;
    case SENSOR_HDCS2020:
	if (spca50x->mode) {
	    /* 320x240 */
	    err = zc3xxWriteVector(spca50x, hdcs2020xx_start_data);
	} else {
	    /* 640x480 */
	    err = zc3xxWriteVector(spca50x, hdcs2020xx_scale_data);
	}
	break;
    case SENSOR_HDCS2020b:
	if (spca50x->mode) {
	    /* 320x240 */
	    err = zc3xxWriteVector(spca50x, hdcs2020xb_start_data);
	} else {
	    /* 640x480 */
	    err = zc3xxWriteVector(spca50x, hdcs2020xb_scale_data);
	}
	break;
    case SENSOR_HV7131B:
    err = zcxx_probeSensor(spca50x);
	if (spca50x->mode) {
	    /* 320x240 */
	    err = zc3xxWriteVector(spca50x, hv7131bxx_start_data);
	} else {
	    /* 640x480 */
	    err = zc3xxWriteVector(spca50x, hv7131bxx_scale_data);
	}
	break;
    case SENSOR_HV7131C:	//HV7131R
    err = zcxx_probeSensor(spca50x);
	if (spca50x->mode) {
	    /* 320x240 */
	    err = zc3xxWriteVector(spca50x, hv7131cxx_start_data);
	} else {
	    /* 640x480 */
	    err = zc3xxWriteVector(spca50x, hv7131cxx_scale_data);
	}
	break;
    case SENSOR_PB0330:
	if (spca50x->mode) {
	    /* 320x240 */
	    if ((spca50x->chip_revision == 0xc001)
		|| (spca50x->chip_revision == 0xe001)
		|| (spca50x->chip_revision == 0x8001))
		err = zc3xxWriteVector(spca50x, pb03303x_start_data);
	    else
		err = zc3xxWriteVector(spca50x, pb0330xx_start_data);
	} else {
	    /* 640x480 */
	    if ((spca50x->chip_revision == 0xc001)
		|| (spca50x->chip_revision == 0xe001)
		|| (spca50x->chip_revision == 0x8001))
		err = zc3xxWriteVector(spca50x, pb03303x_scale_data);
	    else
		err = zc3xxWriteVector(spca50x, pb0330xx_scale_data);
	}
	break;
    case SENSOR_CS2102:
	if (spca50x->mode) {
	    /* 320x240 */
	    err = zc3xxWriteVector(spca50x, cs2102_start_data);
	} else {
	    /* 640x480 */
	    err = zc3xxWriteVector(spca50x, cs2102_scale_data);
	}
	break;
    case SENSOR_OV7630C:
	if (spca50x->mode) {
	    /* 320x240 */
	    err = zc3xxWriteVector(spca50x, ov7630c_start_data);
	} else {
	    /* 640x480 */
	    err = zc3xxWriteVector(spca50x, ov7630c_scale_data);
	}
	break;
    case SENSOR_PAS106:
    err= zc3xxWriteVector(spca50x, pas106b_com_data);
	if (spca50x->mode) {
	    /* 176x144 */
	    err = zc3xxWriteVector(spca50x, pas106b_start_data);	   
	} else {
	    /* 352x288 */
	    err = zc3xxWriteVector(spca50x, pas106b_scale_data);   
	}
	break;
    }
    zc3xx_setbrightness(spca50x);
    zc3xx_setquality(spca50x);
    zc3xx_setAutobright(spca50x);
}

static void zc3xx_stop0(struct usb_spca50x *spca50x)
{
// Nothing todo 
    switch (spca50x->sensor) {
     case SENSOR_PAS106:
                spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0x0000, NULL, 0);
		spca5xxRegWrite(spca50x->dev, 0xa0, 0x03, 0x003a, NULL, 0);
		spca5xxRegWrite(spca50x->dev, 0xa0, 0x0c, 0x003b, NULL, 0);
		spca5xxRegWrite(spca50x->dev, 0xa0, 0x08, 0x0038, NULL, 0);
     break;
    }
}

static void zc3xx_shutdown(struct usb_spca50x *spca50x)
{
    struct usb_device *dev = spca50x->dev;
    __u8 buffread;
    spca5xxRegRead(dev, 0xa1, 0x01, 0x0180, &buffread, 1);
    spca5xxRegWrite(dev, 0xa0, 0x00, 0x0180, NULL, 0);
    spca5xxRegWrite(dev, 0xa0, 0x01, 0x0000, NULL, 0);
}

static __u16 zc3xx_getcolors(struct usb_spca50x *spca50x)
{
//Nothing
return spca50x->colour;
}

static void zc3xx_setcolors(struct usb_spca50x *spca50x)
{
//Nothing
 spca50x->colour = 0;
}

static int zc3xx_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength)
{
		
		if (cdata[0] == 0xFF && cdata[1] == 0xD8) {
		    *iPix = 2;	//18 remove 0xff 0xd8;
		    *datalength -= *iPix;
		    return 0;
		    PDEBUG(5,
			   "Zc301 header packet found datalength %d !!",
			   *datalength );
		} 
		*iPix = 0;
		return (seqnum +1);
}
 
static void zc3xx_set50HZ(struct usb_spca50x *spca50x) {
     switch (spca50x->sensor) {
      case SENSOR_TAS5130C_VF0250:
 	  zc3xxWriteVector(spca50x, tas5130c_vf0250_50HZ);
      break;
      case SENSOR_TAS5130CXX:
 	  zc3xxWriteVector(spca50x, tas5130cxx_50HZ);
      case SENSOR_PB0330:
 	  zc3xxWriteVector(spca50x, pb0330_50HZ);
      break;
      case SENSOR_PAS106:
 	  zc3xxWriteVector(spca50x, pas106b_50HZ);
      break;
      case SENSOR_ICM105A:
 	  zc3xxWriteVector(spca50x, icm105a_50HZ);
      break;
      case SENSOR_HDCS2020b:
 	  zc3xxWriteVector(spca50x, hdcs2020b_50HZ);
      break;
      case SENSOR_CS2102:
 	  zc3xxWriteVector(spca50x, cs2102_50HZ);
      break;
      default:     
      break;
     }
 }
 
static void zc3xx_set60HZ(struct usb_spca50x *spca50x) {
     switch (spca50x->sensor) {
      case SENSOR_TAS5130C_VF0250:
 	  zc3xxWriteVector(spca50x, tas5130c_vf0250_60HZ);
      break;
      case SENSOR_TAS5130CXX:
 	  zc3xxWriteVector(spca50x, tas5130cxx_60HZ);
      break;
      case SENSOR_PB0330:
 	  zc3xxWriteVector(spca50x, pb0330_60HZ);
      break;
      case SENSOR_PAS106:
 	  zc3xxWriteVector(spca50x, pas106b_60HZ);
      break;
      case SENSOR_ICM105A:
 	  zc3xxWriteVector(spca50x, icm105a_60HZ);
      break;
      case SENSOR_HDCS2020b:
 	  zc3xxWriteVector(spca50x, hdcs2020b_60HZ);
      break;
      case SENSOR_CS2102:
 	  zc3xxWriteVector(spca50x, cs2102_60HZ);
      break;
      default:     
      break;
     }
 }
 
static void zc3xx_set50HZScale(struct usb_spca50x *spca50x) {
     switch (spca50x->sensor) {     
      case SENSOR_TAS5130C_VF0250:
 	  zc3xxWriteVector(spca50x, tas5130c_vf0250_50HZScale);
      break;
      case SENSOR_TAS5130CXX:
 	  zc3xxWriteVector(spca50x, tas5130cxx_50HZScale);
      break;
      case SENSOR_PB0330:
 	  zc3xxWriteVector(spca50x, pb0330_50HZScale);
      break;
      case SENSOR_PAS106:
 	  zc3xxWriteVector(spca50x, pas106b_50HZ);
      break;
      case SENSOR_ICM105A:
 	  zc3xxWriteVector(spca50x, icm105a_50HZScale);
      break;
      case SENSOR_HDCS2020b:
 	  zc3xxWriteVector(spca50x, hdcs2020b_50HZScale);
      break;
      case SENSOR_CS2102:
 	  zc3xxWriteVector(spca50x, cs2102_50HZScale);
      break;
      default:
      break;
     }
 
 }
 
static void zc3xx_set60HZScale(struct usb_spca50x *spca50x) {
     switch (spca50x->sensor) {
      case SENSOR_TAS5130C_VF0250:
 	  zc3xxWriteVector(spca50x, tas5130c_vf0250_60HZScale);
      break;
      case SENSOR_TAS5130CXX:
 	  zc3xxWriteVector(spca50x, tas5130cxx_60HZScale);
      break;
      case SENSOR_PB0330:
 	  zc3xxWriteVector(spca50x, pb0330_60HZScale);
      break;
      case SENSOR_PAS106:
 	  zc3xxWriteVector(spca50x, pas106b_60HZ);
      break;
      case SENSOR_ICM105A:
 	  zc3xxWriteVector(spca50x, icm105a_60HZScale);
      break;
      case SENSOR_HDCS2020b:
 	  zc3xxWriteVector(spca50x, hdcs2020b_60HZScale);
      break;
      case SENSOR_CS2102:
 	  zc3xxWriteVector(spca50x, cs2102_60HZScale);
      break;
      default:
      break;
     }
 
 }
 
static void zc3xx_setNoFliker(struct usb_spca50x *spca50x) {
     switch (spca50x->sensor) {
      case SENSOR_TAS5130C_VF0250:
 	  zc3xxWriteVector(spca50x, tas5130c_vf0250_NoFliker);
      break;
      case SENSOR_TAS5130CXX:
 	  zc3xxWriteVector(spca50x, tas5130cxx_NoFliker);
      break;
      case SENSOR_PB0330:
 	  zc3xxWriteVector(spca50x, pb0330_NoFliker);
      break;
      case SENSOR_PAS106:
 	  zc3xxWriteVector(spca50x, pas106b_NoFliker);
      break;
      case SENSOR_ICM105A:
 	  zc3xxWriteVector(spca50x, icm105a_NoFliker);
      break;
      case SENSOR_HDCS2020b:
 	  zc3xxWriteVector(spca50x, hdcs2020b_NoFliker);
      break;
      case SENSOR_CS2102:
 	  zc3xxWriteVector(spca50x, cs2102_NoFliker);
      break;
      default:
      break;
     }
 
 }
 
static void zc3xx_setNoFlikerScale(struct usb_spca50x *spca50x) {
     switch (spca50x->sensor) {
      case SENSOR_TAS5130C_VF0250:
 	  zc3xxWriteVector(spca50x, tas5130c_vf0250_NoFlikerScale);
      break;
      case SENSOR_TAS5130CXX:
 	  zc3xxWriteVector(spca50x, tas5130cxx_NoFlikerScale);
      break;
      case SENSOR_PB0330:
 	  zc3xxWriteVector(spca50x, pb0330_NoFlikerScale);
      break;
      case SENSOR_PAS106:
 	  zc3xxWriteVector(spca50x, pas106b_NoFliker);
      break;
      case SENSOR_ICM105A:
 	  zc3xxWriteVector(spca50x, icm105a_NoFlikerScale);
      break;
      case SENSOR_HDCS2020b:
 	  zc3xxWriteVector(spca50x, hdcs2020b_NoFlikerScale);
      break;
      case SENSOR_CS2102:
 	  zc3xxWriteVector(spca50x, cs2102_NoFlikerScale);
      break;
      default:
      break;
     }
 }
#endif				// ZC3XXUSB_H
