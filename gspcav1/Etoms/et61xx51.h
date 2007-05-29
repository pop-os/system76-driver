 /*************************************************************************** 
# Etoms Et61x151 GPL Linux driver by Michel Xhaard (09/09/2004)
# This driver is design for embedded Linux hardware but should work happy
# on Linux host computer
# Etoms compagnies did not provided any help and support
# The Linux driver is made by reverse engeneering the usb protocol. 
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

#ifndef ET61XX51_H
#define ET61XX51_H

#define ETOMS_ALT_SIZE_1000   12

#define ET_GPIO_DIR_CTRL 0x04	//Control IO bit[0..5] (0 in  1 out)
#define ET_GPIO_OUT 0x05	// Only IO data
#define ET_GPIO_IN 0x06		//Read Only IO data
#define ET_RESET_ALL 0x03
#define ET_ClCK 0x01
#define ET_CTRL 0x02		//enable i2c OutClck Powerdown mode

#define ET_COMP 0x12		//Compression register
#define ET_MAXQt 0x13
#define ET_MINQt 0x14
#define ET_COMP_VAL0 0x02
#define ET_COMP_VAL1 0x03

#define ET_REG1d 0x1d
#define ET_REG1e 0x1e
#define ET_REG1f 0x1f
#define ET_REG20 0x20
#define ET_REG21 0x21
#define ET_REG22 0x22
#define ET_REG23 0x23
#define ET_REG24 0x24
#define ET_REG25 0x25
// base registers for luma calculation
#define ET_LUMA_CENTER 0x39

#define ET_G_RED 0x4d
#define ET_G_GREEN1 0x4e
#define ET_G_BLUE 0x4f
#define ET_G_GREEN2 0x50
#define ET_G_GR_H 0x51
#define ET_G_GB_H 0x52

#define ET_O_RED 0x34
#define ET_O_GREEN1 0x35
#define ET_O_BLUE 0x36
#define ET_O_GREEN2 0x37

#define ET_SYNCHRO 0x68
#define ET_STARTX 0x69
#define ET_STARTY 0x6a
#define ET_WIDTH_LOW 0x6b
#define ET_HEIGTH_LOW 0x6c
#define ET_W_H_HEIGTH 0x6d

#define ET_REG6e 0x6e		//OBW
#define ET_REG6f 0x6f		//OBW
#define ET_REG70 0x70		//OBW_AWB
#define ET_REG71 0x71		//OBW_AWB
#define ET_REG72 0x72		//OBW_AWB
#define ET_REG73 0x73		//Clkdelay ns
#define ET_REG74 0x74		// test pattern
#define ET_REG75 0x75		// test pattern

#define ET_I2C_CLK 0x8c
#define ET_PXL_CLK 0x60

#define ET_I2C_BASE 0x89
#define ET_I2C_COUNT 0x8a
#define ET_I2C_PREFETCH 0x8b
#define ET_I2C_REG 0x88
#define ET_I2C_DATA7 0x87
#define ET_I2C_DATA6 0x86
#define ET_I2C_DATA5 0x85
#define ET_I2C_DATA4 0x84
#define ET_I2C_DATA3 0x83
#define ET_I2C_DATA2 0x82
#define ET_I2C_DATA1 0x81
#define ET_I2C_DATA0 0x80


#define PAS106_REG2 0x02	//pxlClk = systemClk/(reg2)
#define PAS106_REG3 0x03	//line/frame H [11..4]
#define PAS106_REG4 0x04	//line/frame L [3..0]
#define PAS106_REG5 0x05	//exposure time line offset(default 5)
#define PAS106_REG6 0x06	//exposure time pixel offset(default 6)
#define PAS106_REG7 0x07	//signbit Dac (default 0)
#define PAS106_REG9 0x09
#define PAS106_REG0e 0x0e	//global gain [4..0](default 0x0e)
#define PAS106_REG13 0x13	//end i2c write



static __u8 GainRGBG[] = { 0x80, 0x80, 0x80, 0x80, 0x00, 0x00 };

static __u8 I2c2[] = { 0x08, 0x08, 0x08, 0x08, 0x0d };

static __u8 I2c3[] = { 0x12, 0x05 };

static __u8 I2c4[] = { 0x41, 0x08 };

/***************************************************************************/
/*******************     Camera Interface       ***********************/
static int Et_init(struct usb_spca50x *etx);
static void Et_startCamera(struct usb_spca50x *etx);
static void Et_stopCameraN(struct usb_spca50x *etx);
static void Et_stopCamera0(struct usb_spca50x *etx);
static void Et_setbrightness(struct usb_spca50x *etx);
static __u16 Et_getbrightness(struct usb_spca50x *etx);
static void Et_setcontrast(struct usb_spca50x *etx);
static __u16 Et_getcontrast(struct usb_spca50x *etx);
static void Et_setcolors(struct usb_spca50x *etx);
static __u16 Et_getcolors(struct usb_spca50x *etx);
static void Et_setAutobright(struct usb_spca50x *etx);
static int Et_config(struct usb_spca50x *spca50x);
static void Et_shutdown(struct usb_spca50x *spca50x);
static void Et_setquality(struct usb_spca50x *spca50x);
static int Et_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength);
/*******************     Camera private  ******************************/
static void Et_stopCamera0(struct usb_spca50x *etx){}
static void Et_shutdown(struct usb_spca50x *spca50x){}
static void Et_setquality(struct usb_spca50x *spca50x){}
static __u8 Et_getgainG(struct usb_spca50x *etx);
static void Et_setgainG(struct usb_spca50x *etx, __u8 gain);
static int Et_i2cwrite(struct usb_device *dev, __u8 reg, __u8 * buffer,
		       __u16 length, __u8 mode);
static int Et_i2cread(struct usb_device *dev, __u8 reg, __u8 * buffer,
		      __u16 length, __u8 mode);
static int Et_WaitStatus(struct usb_device *dev);
static int Et_videoOff(struct usb_device *dev);
static int Et_videoOn(struct usb_device *dev);
static void Et_init1(struct usb_spca50x *etx);
/***************************************************************************/
static struct cam_operation fet61x = {
 	.initialize = Et_init,
	.configure = Et_config,
	.start = Et_startCamera,
	.stopN = Et_stopCameraN,
	.stop0 = Et_stopCamera0,
	.get_bright = Et_getbrightness,
	.set_bright = Et_setbrightness,
	.get_contrast = Et_getcontrast,
	.set_contrast = Et_setcontrast,
	.get_colors = Et_getcolors,
	.set_colors = Et_setcolors,
	.set_autobright = Et_setAutobright,
	.set_quality = Et_setquality,
	.cam_shutdown = Et_shutdown,
	.sof_detect = Et_sofdetect,
 };
static int Et_i2cwrite(struct usb_device *dev, __u8 reg, __u8 * buffer,
		       __u16 length, __u8 mode)
{
/* buffer should be [D0..D7] */
    int i, j;
    __u8 base = 0x40;		// sensor base for the pas106
    __u8 ptchcount = 0;
    ptchcount = (((length & 0x07) << 4) | (mode & 0x03));
/* set the base address */
    Et_RegWrite(dev, 0x0, 0x0, ET_I2C_BASE, &base, 1);
/* set count and prefetch */
    Et_RegWrite(dev, 0x0, 0x0, ET_I2C_COUNT, &ptchcount, 1);
/* set the register base */
    Et_RegWrite(dev, 0x0, 0x0, ET_I2C_REG, &reg, 1);
    j = length - 1;
    for (i = 0; i < length; i++) {
	Et_RegWrite(dev, 0x0, 0x0, (ET_I2C_DATA0 + j), &buffer[j], 1);
	j--;
    }
    return 0;
}
static int Et_i2cread(struct usb_device *dev, __u8 reg, __u8 * buffer,
		      __u16 length, __u8 mode)
{
/* buffer should be [D0..D7] */
    int i, j;
    __u8 base = 0x40;		// sensor base for the pas106
    __u8 ptchcount = 0;
    __u8 prefetch = 0x02;
    ptchcount = (((length & 0x07) << 4) | (mode & 0x03));
/* set the base address */
    Et_RegWrite(dev, 0x0, 0x0, ET_I2C_BASE, &base, 1);
/* set count and prefetch */
    Et_RegWrite(dev, 0x0, 0x0, ET_I2C_COUNT, &ptchcount, 1);
/* set the register base */
    Et_RegWrite(dev, 0x0, 0x0, ET_I2C_REG, &reg, 1);
    Et_RegWrite(dev, 0x0, 0x0, ET_I2C_PREFETCH, &prefetch, 1);
    prefetch = 0x00;
    Et_RegWrite(dev, 0x0, 0x0, ET_I2C_PREFETCH, &prefetch, 1);
    j = length - 1;
    for (i = 0; i < length; i++) {
	Et_RegRead(dev, 0x0, 0x0, (ET_I2C_DATA0 + j), &buffer[j], 1);
	j--;
    }
    return 0;
}
static int Et_WaitStatus(struct usb_device *dev)
{
    __u8 bytereceived = 0;
    int retry = 10;
    while (retry--) {
	Et_RegRead(dev, 0x0, 0x0, ET_ClCK, &bytereceived, 1);
	if (bytereceived != 0)
	    return 1;
    }
    return 0;
}

static int Et_videoOff(struct usb_device *dev)
{
    int err = -1;
    __u8 stopvideo = 0;
    Et_RegWrite(dev, 0x0, 0x0, ET_GPIO_OUT, &stopvideo, 1);
    err = Et_WaitStatus(dev);
    if (!err)
	PDEBUG(5, "timeout Et_waitStatus VideoON");
    return err;
}

static int Et_videoOn(struct usb_device *dev)
{
    int err = -1;
    __u8 startvideo = 0x10;	//set Bit5
    Et_RegWrite(dev, 0x0, 0x0, ET_GPIO_OUT, &startvideo, 1);
    err = Et_WaitStatus(dev);
    if (!err)
	PDEBUG(5, "timeout Et_waitStatus VideoOFF");
    return err;
}
static void Et_init2(struct usb_spca50x *etx)
{
    __u8 value = 0x00;
    __u8 received = 0x00;
    __u8 FormLine[] = { 0x84, 0x03, 0x14, 0xf4, 0x01, 0x05 };

    PDEBUG(5, "Open Init2 ET");
    value = 0x2f;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_GPIO_DIR_CTRL, &value, 1);
    value = 0x10;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_GPIO_OUT, &value, 1);
    Et_RegRead(etx->dev, 0x0, 0x0, ET_GPIO_IN, &received, 1);
    value = 0x14;		//0x14 // 0x16 enabled pattern
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_ClCK, &value, 1);
    value = 0x1b;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_CTRL, &value, 1);

    /*   compression et subsampling */
    if (etx->mode) {
	value = ET_COMP_VAL1;	// 320

    } else {
	value = ET_COMP_VAL0;	// 640

    }
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_COMP, &value, 1);
    value = 0x1f;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_MAXQt, &value, 1);
    value = 0x04;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_MINQt, &value, 1);
    /* undocumented registers */
    value = 0xff;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG1d, &value, 1);
    value = 0xff;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG1e, &value, 1);
    value = 0xff;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG1f, &value, 1);
    value = 0x35;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG20, &value, 1);
    value = 0x01;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG21, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG22, &value, 1);
    value = 0xff;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG23, &value, 1);
    value = 0xff;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG24, &value, 1);
    value = 0x0f;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG25, &value, 1);
    /* colors setting */
    value = 0x11;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x30, &value, 1);	//0x30
    value = 0x40;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x31, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x32, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_O_RED, &value, 1);	//0x34
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_O_GREEN1, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_O_BLUE, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_O_GREEN2, &value, 1);
	/*************/
    value = 0x80;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_RED, &value, 1);	//0x4d
    value = 0x80;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_GREEN1, &value, 1);
    value = 0x80;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_BLUE, &value, 1);
    value = 0x80;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_GREEN2, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_GR_H, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_GB_H, &value, 1);	//0x52
    /* Window control registers */


    value = 0x80;		/* use cmc_out */
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x61, &value, 1);


    value = 0x02;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x62, &value, 1);
    value = 0x03;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x63, &value, 1);
    value = 0x14;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x64, &value, 1);
    value = 0x0e;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x65, &value, 1);
    value = 0x02;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x66, &value, 1);
    value = 0x02;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x67, &value, 1);


	/**************************************/
    value = 0x8f;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_SYNCHRO, &value, 1);	//0x68
    value = 0x69;		//0x6a //0x69
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_STARTX, &value, 1);
    value = 0x0d;		//0x0d //0x0c
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_STARTY, &value, 1);
    value = 0x80;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_WIDTH_LOW, &value, 1);
    value = 0xe0;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_HEIGTH_LOW, &value, 1);
    value = 0x60;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_W_H_HEIGTH, &value, 1);	//6d
    value = 0x86;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG6e, &value, 1);
    value = 0x01;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG6f, &value, 1);
    value = 0x26;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG70, &value, 1);
    value = 0x7a;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG71, &value, 1);
    value = 0x01;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG72, &value, 1);
    /* Clock Pattern registers ***************** */
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG73, &value, 1);
    value = 0x18;		//0x28
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG74, &value, 1);
    value = 0x0f;		// 0x01
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG75, &value, 1);
	/**********************************************/
    value = 0x20;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x8a, &value, 1);
    value = 0x0f;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x8d, &value, 1);
    value = 0x08;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x8e, &value, 1);
	/**************************************/
    value = 0x08;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x03, &value, 1);
    value = 0x03;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_PXL_CLK, &value, 1);
    value = 0xff;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x81, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x80, &value, 1);
    value = 0xff;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x81, &value, 1);
    value = 0x20;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x80, &value, 1);
    value = 0x01;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x03, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x03, &value, 1);
    value = 0x08;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x03, &value, 1);
	/********************************************/

    // Et_RegRead(etx->dev,0x0,0x0,ET_I2C_BASE,&received,1); always 0x40 as the pas106 ???
    /* set the sensor */
    if (etx->mode) {		/* 320 */
	value = 0x04;
	Et_RegWrite(etx->dev, 0x0, 0x0, ET_PXL_CLK, &value, 1);
	/* now set by fifo the FormatLine setting */
	Et_RegWrite(etx->dev, 0x0, 0x0, 0x62, FormLine, 6);

    } else {			/* 640 */
	/* setting PixelClock 
	   0x03 mean 24/(3+1) = 6 Mhz
	   0x05 -> 24/(5+1) = 4 Mhz
	   0x0b -> 24/(11+1) = 2 Mhz
	   0x17 -> 24/(23+1) = 1 Mhz
	 */
	value = 0x1e;		//0x17
	Et_RegWrite(etx->dev, 0x0, 0x0, ET_PXL_CLK, &value, 1);
	/* now set by fifo the FormatLine setting */
	Et_RegWrite(etx->dev, 0x0, 0x0, 0x62, FormLine, 6);

    }

    value = 0x47;		// 0x47;  
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x81, &value, 1);	// set exposure times [ 0..0x78] 0->longvalue 0x78->shortvalue
    value = 0x40;		//  0x40;  
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x80, &value, 1);
    /* Pedro change */
    // Brightness change Brith+ decrease value 
    // Brigth- increase value 
    // original value = 0x70;
    value = 0x30;		// 0x20; 
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x81, &value, 1);	// set brightness
    value = 0x20;		// 0x20;
    Et_RegWrite(etx->dev, 0x0, 0x0, 0x80, &value, 1);
}


static void Et_init1(struct usb_spca50x *etx)
{
    __u8 value = 0x00;
    __u8 received = 0x00;
    //__u8 I2c0 [] ={0x0a,0x12,0x05,0x22,0xac,0x00,0x01,0x00};
    __u8 I2c0[] = { 0x0a, 0x12, 0x05, 0x6d, 0xcd, 0x00, 0x01, 0x00 };	// try 1/120 0x6d 0xcd 0x40
    //__u8 I2c0 [] ={0x0a,0x12,0x05,0xfe,0xfe,0xc0,0x01,0x00}; // 1/60000 hmm ??
    PDEBUG(5, "Open Init1 ET");

    value = 7;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_GPIO_DIR_CTRL, &value, 1);
    Et_RegRead(etx->dev, 0x0, 0x0, ET_GPIO_IN, &received, 1);
    value = 1;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_RESET_ALL, &value, 1);
    value = 0;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_RESET_ALL, &value, 1);
    value = 0x10;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_ClCK, &value, 1);
    value = 0x19;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_CTRL, &value, 1);
    /*   compression et subsampling */
    if (etx->mode) {
	value = ET_COMP_VAL1;

    } else {
	value = ET_COMP_VAL0;
    }
    PDEBUG(0, "Open mode %d Compression %d", etx->mode, value);
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_COMP, &value, 1);
    value = 0x1d;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_MAXQt, &value, 1);
    value = 0x02;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_MINQt, &value, 1);
    /* undocumented registers */
    value = 0xff;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG1d, &value, 1);
    value = 0xff;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG1e, &value, 1);
    value = 0xff;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG1f, &value, 1);
    value = 0x35;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG20, &value, 1);
    value = 0x01;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG21, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG22, &value, 1);
    value = 0xf7;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG23, &value, 1);
    value = 0xff;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG24, &value, 1);
    value = 0x07;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG25, &value, 1);
    /* colors setting */
    value = 0x80;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_RED, &value, 1);
    value = 0x80;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_GREEN1, &value, 1);
    value = 0x80;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_BLUE, &value, 1);
    value = 0x80;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_GREEN2, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_GR_H, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_GB_H, &value, 1);
    /* Window control registers */
    value = 0xf0;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_SYNCHRO, &value, 1);
    value = 0x56;		//0x56
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_STARTX, &value, 1);
    value = 0x05;		//0x04
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_STARTY, &value, 1);
    value = 0x60;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_WIDTH_LOW, &value, 1);
    value = 0x20;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_HEIGTH_LOW, &value, 1);
    value = 0x50;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_W_H_HEIGTH, &value, 1);
    value = 0x86;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG6e, &value, 1);
    value = 0x01;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG6f, &value, 1);
    value = 0x86;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG70, &value, 1);
    value = 0x14;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG71, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG72, &value, 1);
    /* Clock Pattern registers */
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG73, &value, 1);
    value = 0x00;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG74, &value, 1);
    value = 0x0a;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_REG75, &value, 1);
    value = 0x04;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_I2C_CLK, &value, 1);
    value = 0x01;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_PXL_CLK, &value, 1);
    /* set the sensor */
    if (etx->mode) {
	I2c0[0] = 0x06;
	Et_i2cwrite(etx->dev, PAS106_REG2, I2c0, sizeof(I2c0), 1);
	Et_i2cwrite(etx->dev, PAS106_REG9, I2c2, sizeof(I2c2), 1);
	value = 0x06;
	Et_i2cwrite(etx->dev, PAS106_REG2, &value, 1, 1);
	Et_i2cwrite(etx->dev, PAS106_REG3, I2c3, sizeof(I2c3), 1);
	//value = 0x1f;
	value = 0x04;
	Et_i2cwrite(etx->dev, PAS106_REG0e, &value, 1, 1);
    } else {
	I2c0[0] = 0x0a;

	Et_i2cwrite(etx->dev, PAS106_REG2, I2c0, sizeof(I2c0), 1);
	Et_i2cwrite(etx->dev, PAS106_REG9, I2c2, sizeof(I2c2), 1);
	value = 0x0a;

	Et_i2cwrite(etx->dev, PAS106_REG2, &value, 1, 1);
	Et_i2cwrite(etx->dev, PAS106_REG3, I2c3, sizeof(I2c3), 1);
	value = 0x04;
	//value = 0x10;
	Et_i2cwrite(etx->dev, PAS106_REG0e, &value, 1, 1);
	/* bit 2 enable bit 1:2 select 0 1 2 3 
	   value = 0x07;// curve 0
	   Et_i2cwrite(etx->dev,PAS106_REG0f,&value,1,1);
	 */
    }

    //value = 0x01;
    //value = 0x22;
    //Et_i2cwrite(etx->dev,PAS106_REG5,&value,1,1);
    /* magnetude and sign bit for DAC */
    Et_i2cwrite(etx->dev, PAS106_REG7, I2c4, sizeof(I2c4), 1);
    /* now set by fifo the whole colors setting */
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_RED, GainRGBG, 6);
    etx->colour = Et_getcolors(etx);
    Et_setcolors(etx);
}

static int Et_init(struct usb_spca50x *etx)
{
    int err = -1;
    __u8 value = 0x00;

    PDEBUG(5, "Initialize ET1");
    if (etx->desc == Etoms61x151) {
	Et_init1(etx);
    } else {
	Et_init2(etx);
    }
    value = 0x08;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_RESET_ALL, &value, 1);
    err = Et_videoOff(etx->dev);
    PDEBUG(5, "Et_Init_VideoOff %d", err);
    return 0;
}

static void Et_startCamera(struct usb_spca50x *etx)
{
    int err = -1;
    __u8 value = 0x00;

    if (etx->desc == Etoms61x151) {
	Et_init1(etx);
    } else {
	Et_init2(etx);
    }

    value = 0x08;
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_RESET_ALL, &value, 1);
    err = Et_videoOn(etx->dev);
    PDEBUG(5, "Et_VideoOn %d", err);
}

static void Et_stopCameraN(struct usb_spca50x *etx)
{
    int err = -1;
    err = Et_videoOff(etx->dev);
    PDEBUG(5, "Et_VideoOff %d", err);

}

static void Et_setbrightness(struct usb_spca50x *etx)
{
    int i;
    __u8 brightness = etx->brightness >> 9;
    for (i = 0; i < 4; i++) {
	Et_RegWrite(etx->dev, 0x0, 0x0, (ET_O_RED + i), &brightness, 1);
    }
}

static __u16 Et_getbrightness(struct usb_spca50x *etx)
{
    int i;
    int brightness = 0;
    __u8 value = 0;
    for (i = 0; i < 4; i++) {
	Et_RegRead(etx->dev, 0x0, 0x0, (ET_O_RED + i), &value, 1);
	brightness += value;
    }
    etx->brightness = (brightness << 6);
    return etx->brightness;
}

static void Et_setcontrast(struct usb_spca50x *etx)
{
    __u8 RGBG[] = { 0x80, 0x80, 0x80, 0x80, 0x00, 0x00 };
    __u8 contrast = etx->contrast >> 8;
    memset(RGBG, contrast, sizeof(RGBG) - 2);
    Et_RegWrite(etx->dev, 0x0, 0x0, ET_G_RED, RGBG, 6);
}

static __u16 Et_getcontrast(struct usb_spca50x *etx)
{
    int i;
    int contrast = 0;
    __u8 value = 0;
    for (i = 0; i < 4; i++) {
	Et_RegRead(etx->dev, 0x0, 0x0, (ET_G_RED + i), &value, 1);
	contrast += value;
    }
    etx->contrast = (contrast << 6);
    return etx->contrast;
}

static __u8 Et_getgainG(struct usb_spca50x *etx)
{

    __u8 value = 0;
    if (etx->sensor == SENSOR_PAS106) {
	Et_i2cread(etx->dev, PAS106_REG0e, &value, 1, 1);
	PDEBUG(5, "Etoms gain G %d", value);
	return value;
    } else {
	return 0x1f;
    }
}

static void Et_setgainG(struct usb_spca50x *etx, __u8 gain)
{

    __u8 i2cflags = 0x01;
    if (etx->sensor == SENSOR_PAS106) {
	Et_i2cwrite(etx->dev, PAS106_REG13, &i2cflags, 1, 3);
	Et_i2cwrite(etx->dev, PAS106_REG0e, &gain, 1, 1);
#if 0
	Et_i2cwrite(etx->dev, 0x09, &gain, 1, 1);
	Et_i2cwrite(etx->dev, 0x0a, &gain, 1, 1);
	Et_i2cwrite(etx->dev, 0x0b, &gain, 1, 1);
	Et_i2cwrite(etx->dev, 0x0c, &gain, 1, 1);
#endif
    }

}

#define BLIMIT(bright) (__u8)((bright>0x1F)?0x1f:((bright<4)?3:bright))
#define LIMIT(color) (unsigned char)((color>0xFF)?0xff:((color<0)?0:color))

static void Et_setAutobright(struct usb_spca50x *etx)
{
    __u8 GRBG[] = { 0, 0, 0, 0 };
    __u8 luma = 0;
    __u8 luma_mean = 128;
    __u8 luma_delta = 20;
    __u8 spring = 4;
    int Gbright = 0;
    __u8 r, g, b;
    Gbright = Et_getgainG(etx);
    Et_RegRead(etx->dev, 0x0, 0x0, ET_LUMA_CENTER, GRBG, 4);
    g = (GRBG[0] + GRBG[3]) >> 1;
    r = GRBG[1];
    b = GRBG[2];
    r = ((r << 8) - (r << 4) - (r << 3)) >> 10;
    b = ((b << 7) >> 10);
    g = ((g << 9) + (g << 7) + (g << 5)) >> 10;
    luma = LIMIT(r + g + b);
    PDEBUG(5, "Etoms luma G %d", luma);
    if ((luma < (luma_mean - luma_delta)) ||
	(luma > (luma_mean + luma_delta))) {
	Gbright += ((luma_mean - luma) >> spring);
	Gbright = BLIMIT(Gbright);
	PDEBUG(5, "Etoms Gbright %d", Gbright);
	Et_setgainG(etx, (__u8) Gbright);
    }
}
#undef BLIMIT
#undef LIMIT

static void Et_setcolors(struct usb_spca50x *etx)
{

    static __u8 I2cc[] = { 0x05, 0x02, 0x02, 0x05, 0x0d };
    __u8 i2cflags = 0x01;
    //__u8 green = 0;
    __u8 colors = (etx->colour >> 12) & 0x0f;

    I2cc[3] = colors;		//red
    I2cc[0] = 15 - colors;	//blue     
    // green = 15 - ((((7*I2cc[0]) >> 2 ) + I2cc[3]) >> 1);
    // I2cc[1] = I2cc[2] = green;
    if (etx->sensor == SENSOR_PAS106) {
	Et_i2cwrite(etx->dev, PAS106_REG13, &i2cflags, 1, 3);
	Et_i2cwrite(etx->dev, PAS106_REG9, I2cc, sizeof(I2cc), 1);
    }
    //PDEBUG(5 , "Etoms red %d blue %d green %d",I2cc[3],I2cc[0],green);
}
static __u16 Et_getcolors(struct usb_spca50x *etx)
{

    //__u8 valblue = 0;
    __u8 valred = 0;
    etx->colour = 0;
    if (etx->sensor == SENSOR_PAS106) {
	//Et_i2cread(etx->dev,PAS106_REG9,&valblue,1,1);
	Et_i2cread(etx->dev, PAS106_REG9 + 3, &valred, 1, 1);
	etx->colour = (((valred) & 0x0f) << 12);
    }
    return etx->colour;
}
static void set_EtxxVGA(struct usb_spca50x *spca50x)
{
    memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof(struct mwebcam));
#if 0
    spca50x->mode_cam[VGA].width = 640;
    spca50x->mode_cam[VGA].height = 480;
    spca50x->mode_cam[VGA].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[VGA].pipe = 1000;
    spca50x->mode_cam[VGA].method = 0;
    spca50x->mode_cam[VGA].mode = 0;
    spca50x->mode_cam[PAL].width = 384;
    spca50x->mode_cam[PAL].height = 288;
    spca50x->mode_cam[PAL].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[PAL].pipe = 1000;
    spca50x->mode_cam[PAL].method = 1;
    spca50x->mode_cam[PAL].mode = 0;
    spca50x->mode_cam[SIF].width = 352;
    spca50x->mode_cam[SIF].height = 288;
    spca50x->mode_cam[SIF].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[SIF].pipe = 1000;
    spca50x->mode_cam[SIF].method = 1;
    spca50x->mode_cam[SIF].mode = 0;
#endif
    spca50x->mode_cam[CIF].width = 320;
    spca50x->mode_cam[CIF].height = 240;
    spca50x->mode_cam[CIF].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[CIF].pipe = 1000;
    spca50x->mode_cam[CIF].method = 0;
    spca50x->mode_cam[CIF].mode = 1;
    spca50x->mode_cam[QPAL].width = 192;
    spca50x->mode_cam[QPAL].height = 144;
    spca50x->mode_cam[QPAL].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QPAL].pipe = 1000;
    spca50x->mode_cam[QPAL].method = 1;
    spca50x->mode_cam[QPAL].mode = 1;
    spca50x->mode_cam[QSIF].width = 176;
    spca50x->mode_cam[QSIF].height = 144;
    spca50x->mode_cam[QSIF].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QSIF].pipe = 1000;
    spca50x->mode_cam[QSIF].method = 1;
    spca50x->mode_cam[QSIF].mode = 1;
    spca50x->mode_cam[QCIF].width = 160;
    spca50x->mode_cam[QCIF].height = 120;
    spca50x->mode_cam[QCIF].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QCIF].pipe = 1000;
    spca50x->mode_cam[QCIF].method = 1;
    spca50x->mode_cam[QCIF].mode = 1;
}
static void set_EtxxSIF(struct usb_spca50x *spca50x)
{
    memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof(struct mwebcam));
    spca50x->mode_cam[SIF].width = 352;
    spca50x->mode_cam[SIF].height = 288;
    spca50x->mode_cam[SIF].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[SIF].pipe = 1000;
    spca50x->mode_cam[SIF].method = 0;
    spca50x->mode_cam[SIF].mode = 0;
    spca50x->mode_cam[CIF].width = 320;
    spca50x->mode_cam[CIF].height = 240;
    spca50x->mode_cam[CIF].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[CIF].pipe = 1000;
    spca50x->mode_cam[CIF].method = 1;
    spca50x->mode_cam[CIF].mode = 0;
    spca50x->mode_cam[QPAL].width = 192;
    spca50x->mode_cam[QPAL].height = 144;
    spca50x->mode_cam[QPAL].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QPAL].pipe = 1000;
    spca50x->mode_cam[QPAL].method = 1;
    spca50x->mode_cam[QPAL].mode = 0;
    spca50x->mode_cam[QSIF].width = 176;
    spca50x->mode_cam[QSIF].height = 144;
    spca50x->mode_cam[QSIF].t_palette =
	P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QSIF].pipe = 1000;
    spca50x->mode_cam[QSIF].method = 0;
    spca50x->mode_cam[QSIF].mode = 1;
    spca50x->mode_cam[QCIF].width = 160;
    spca50x->mode_cam[QCIF].height = 120;
    spca50x->mode_cam[QCIF].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QCIF].pipe = 1000;
    spca50x->mode_cam[QCIF].method = 1;
    spca50x->mode_cam[QCIF].mode = 1;
}
static int Et_config(struct usb_spca50x *spca50x)
{
    switch (spca50x->sensor) {
    case SENSOR_TAS5130CXX:
	set_EtxxVGA(spca50x);
	break;
    case SENSOR_PAS106:
	set_EtxxSIF(spca50x);
	break;
    default:
	return -EINVAL;
	break;
    }
    return 0;
}
static int Et_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength)
{
int seqframe;
		seqframe = cdata[0] & 0x3f;
		*datalength = (int) (((cdata[0] & 0xc0) << 2) | cdata[1]);
		if (seqframe == 0x3f) {
		    PDEBUG(5,
			   "Etoms header packet found datalength %d !!",
			   *datalength);
		    PDEBUG(5, "Etoms G %d R %d G %d B %d", cdata[2],
			   cdata[3], cdata[4], cdata[5]);
		    
		    *iPix = 30;
		    /* don't change datalength as the chips provided it */
		    return 0;
		} else {
		    if (*datalength) {
		    *iPix = 8;
			return (seqnum+1);
		    } else {
			/* Drop Packet */
			return -1;
		    }
		}
}
#endif				/* ET61XX51_H */
