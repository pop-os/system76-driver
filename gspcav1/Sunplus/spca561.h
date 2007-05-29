
#ifndef SPCA561_INIT_H
#define SPCA561_INIT_H

/****************************************************************************
#	 	Sunplus spca561 library                                     #
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
/* Initialization data
   I'm not very sure how to split initialization from open data
   chunks. For now, we'll consider everything as initialization
 */
/* Frame packet header offsets for the spca561 */
#define SPCA561_OFFSET_SNAP 1
#define SPCA561_OFFSET_TYPE 2
#define SPCA561_OFFSET_COMPRESS 3
#define SPCA561_OFFSET_FRAMSEQ   4
#define SPCA561_OFFSET_GPIO 5
#define SPCA561_OFFSET_USBBUFF 6
#define SPCA561_OFFSET_WIN2GRAVE 7
#define SPCA561_OFFSET_WIN2RAVE 8
#define SPCA561_OFFSET_WIN2BAVE 9
#define SPCA561_OFFSET_WIN2GBAVE 10
#define SPCA561_OFFSET_WIN1GRAVE 11
#define SPCA561_OFFSET_WIN1RAVE 12
#define SPCA561_OFFSET_WIN1BAVE 13
#define SPCA561_OFFSET_WIN1GBAVE 14
#define SPCA561_OFFSET_FREQ 15
#define SPCA561_OFFSET_VSYNC 16
#define SPCA561_OFFSET_DATA 1
#define SPCA561_INDEX_I2C_BASE 0x8800
#define SPCA561_SNAPBIT 0x20
#define SPCA561_SNAPCTRL 0x40
enum {
    Rev072A = 0,
    Rev012A,
};
/*******************     Camera Interface   ***********************/
static int spca561_init(struct usb_spca50x *spca50x);
static void spca561_start(struct usb_spca50x *spca50x);
static void spca561_stopN(struct usb_spca50x *spca50x);
static void spca561_stop0(struct usb_spca50x *spca50x);
static void spca561_setbrightness(struct usb_spca50x *spca50x);
static __u16 spca561_getbrightness(struct usb_spca50x *spca50x);
static void spca561_setcontrast(struct usb_spca50x *spca50x);
static __u16 spca561_getcontrast(struct usb_spca50x *spca50x);
static void spca561_setcolors(struct usb_spca50x *spca50x);
static __u16 spca561_getcolors(struct usb_spca50x *spca50x);
static void spca561_setAutobright(struct usb_spca50x *spca50x);
static int spca561_config(struct usb_spca50x *spca50x);
static void spca561_shutdown(struct usb_spca50x *spca50x);
static void spca561_setquality(struct usb_spca50x *spca50x);
static int spca561_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength);
/******************************************************************/
static void spca561_setcolors(struct usb_spca50x *spca50x){}
static __u16 spca561_getcolors(struct usb_spca50x *spca50x){return 0;}
static void spca561_setquality(struct usb_spca50x *spca50x){}
static void spca561_stop0(struct usb_spca50x *spca50x){}
//static __u16 spca561_setexposure(struct usb_spca50x *spca50x);
//static __u16 spca561_getexposure(struct usb_spca50x *spca50x);
/*****************************************************************/
static struct cam_operation fspca561 = {
 	.initialize = spca561_init,
	.configure = spca561_config,
	.start = spca561_start,
	.stopN = spca561_stopN,
	.stop0 = spca561_stop0,
	.get_bright = spca561_getbrightness,
	.set_bright = spca561_setbrightness,
	.get_contrast = spca561_getcontrast,
	.set_contrast = spca561_setcontrast,
	.get_colors = spca561_getcolors,
	.set_colors = spca561_setcolors,
	.set_autobright = spca561_setAutobright,
	.set_quality = spca561_setquality,
	.cam_shutdown = spca561_shutdown,
	.sof_detect = spca561_sofdetect,
 };
static void spca561_InitI2c(struct usb_spca50x *spca50x, __u8 mode)
{
    spca5xxRegWrite(spca50x->dev, 0x00, 0x92, 0x8804, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x00, mode, 0x8802, NULL, 0);
}

static void spca561_WriteI2c(struct usb_spca50x *spca50x, __u16 valeur,
			     __u16 registre)
{
    int retry = 60;
    __u8 DataLow = 0;
    __u8 DataHight = 0;
    __u8 Data = 0;
    DataLow = valeur & 0xFF;
    DataHight = (valeur >> 8) & 0xFF;
    spca5xxRegWrite(spca50x->dev, 0x00, registre, 0x8801, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x00, DataLow, 0x8805, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x00, DataHight, 0x8800, NULL, 0);
    while (retry--) {
	spca5xxRegRead(spca50x->dev, 0x00, 0, 0x8803, &Data, 1);
	if (!Data)
	    break;
    }
}

/****************** not in use **********************************/
static int spca561_ReadI2c(struct usb_spca50x *spca50x, __u16 registre,
			   __u8 mode)
{
    int retry = 60;

    unsigned char value = 0;
    unsigned char vallsb = 0;
    __u8 Data = 0;
    spca5xxRegWrite(spca50x->dev, 0x00, 0x92, 0x8804, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x00, registre, 0x8801, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0x00, (mode | 0x01), 0x8802, NULL, 0);
    while (retry--) {
	spca5xxRegRead(spca50x->dev, 0x00, 0, 0x8803, &Data, 1);
	if (!Data)
	    break;
    }
    if (retry == 0)
	return -1;
    spca5xxRegRead(spca50x->dev, 0x00, 0, 0x8800, &value, 1);
    spca5xxRegRead(spca50x->dev, 0x00, 0, 0x8805, &vallsb, 1);
    return (int) value << 8 | vallsb;
}

static __u16 spca561_init_data[][3] = {
    {0, 0x0000, 0x8114},	// Software GPIO output data
    {0, 0x0001, 0x8114},	// Software GPIO output data
    {0, 0x0000, 0x8112},	// Some kind of reset
    {0, 0x0003, 0x8701},	// PCLK clock delay adjustment
    {0, 0x0001, 0x8703},	// HSYNC from cmos inverted
    {0, 0x0011, 0x8118},	// Enable and conf sensor
    {0, 0x0001, 0x8118},	// Conf sensor
    {0, 0x0092, 0x8804},	// I know nothing about these
    {0, 0x0010, 0x8802},	// 0x88xx registers, so I won't
	/*********************/
    {0, 0x000d, 0x8805},	// sensor default setting
    {0, 0x0001, 0x8801},	// 1 <- 0x0d
    {0, 0x0000, 0x8800},
    {0, 0x0018, 0x8805},
    {0, 0x0002, 0x8801},	// 2 <- 0x18
    {0, 0x0000, 0x8800},
    {0, 0x0065, 0x8805},
    {0, 0x0004, 0x8801},	// 4 <- 0x01 0x65
    {0, 0x0001, 0x8800},
    {0, 0x0021, 0x8805},
    {0, 0x0005, 0x8801},	// 5 <- 0x21
    {0, 0x0000, 0x8800},
    {0, 0x00aa, 0x8805},
    {0, 0x0007, 0x8801},	// 7 <- 0xaa
    {0, 0x0000, 0x8800},
    {0, 0x0004, 0x8805},
    {0, 0x0020, 0x8801},	// 0x20 <- 0x15 0x04
    {0, 0x0015, 0x8800},
    {0, 0x0002, 0x8805},
    {0, 0x0039, 0x8801},	// 0x39 <- 0x02
    {0, 0x0000, 0x8800},
    {0, 0x0010, 0x8805},
    {0, 0x0035, 0x8801},	// 0x35 <- 0x10
    {0, 0x0000, 0x8800},
    {0, 0x0049, 0x8805},
    {0, 0x0009, 0x8801},	// 0x09 <- 0x10 0x49
    {0, 0x0010, 0x8800},
    {0, 0x000b, 0x8805},
    {0, 0x0028, 0x8801},	// 0x28 <- 0x0b
    {0, 0x0000, 0x8800},
    {0, 0x000f, 0x8805},
    {0, 0x003b, 0x8801},	// 0x3b <- 0x0f
    {0, 0x0000, 0x8800},
    {0, 0x0000, 0x8805},
    {0, 0x003c, 0x8801},	// 0x3c <- 0x00
    {0, 0x0000, 0x8800},
	/**********************/
    {0, 0x0018, 0x8601},	// Pixel/line selection for color separation
    {0, 0x0000, 0x8602},	// Optical black level for user setting
    {0, 0x0060, 0x8604},	// Optical black horizontal offset
    {0, 0x0002, 0x8605},	// Optical black vertical offset
    {0, 0x0000, 0x8603},	// Non-automatic optical black level
    {0, 0x0002, 0x865b},	// Horizontal offset for valid pixels
    {0, 0x0000, 0x865f},	// Vertical valid pixels window (x2)
    {0, 0x00b0, 0x865d},	// Horizontal valid pixels window (x2)
    {0, 0x0090, 0x865e},	// Vertical valid lines window (x2)
    {0, 0x00e0, 0x8406},	// Memory buffer threshold
    {0, 0x0000, 0x8660},	// Compensation memory stuff
    {0, 0x0002, 0x8201},	// Output address for r/w serial EEPROM
    {0, 0x0008, 0x8200},	// Clear valid bit for serial EEPROM
    {0, 0x0001, 0x8200},	// OprMode to be executed by hardware
    {0, 0x0007, 0x8201},	// Output address for r/w serial EEPROM
    {0, 0x0008, 0x8200},	// Clear valid bit for serial EEPROM
    {0, 0x0001, 0x8200},	// OprMode to be executed by hardware
    {0, 0x0010, 0x8660},	// Compensation memory stuff
    {0, 0x0018, 0x8660},	// Compensation memory stuff

    {0, 0x0004, 0x8611},	// R offset for white balance
    {0, 0x0004, 0x8612},	// Gr offset for white balance
    {0, 0x0007, 0x8613},	// B offset for white balance
    {0, 0x0000, 0x8614},	// Gb offset for white balance
    {0, 0x008c, 0x8651},	// R gain for white balance
    {0, 0x008c, 0x8652},	// Gr gain for white balance
    {0, 0x00b5, 0x8653},	// B gain for white balance
    {0, 0x008c, 0x8654},	// Gb gain for white balance
    {0, 0x0002, 0x8502},	// Maximum average bit rate stuff


    {0, 0x0011, 0x8802},
    {0, 0x0087, 0x8700},	// Set master clock (96Mhz????)
    {0, 0x0081, 0x8702},	// Master clock output enable

    {0, 0x0000, 0x8500},	// Set image type (352x288 no compression)
    // Originally was 0x0010 (352x288 compression)

    {0, 0x0002, 0x865b},	// Horizontal offset for valid pixels
    {0, 0x0003, 0x865c},	// Vertical offset for valid lines
    /*************************/// sensor active
    {0, 0x0003, 0x8801},	// 0x03 <- 0x01 0x21 //289
    {0, 0x0021, 0x8805},
    {0, 0x0001, 0x8800},
    {0, 0x0004, 0x8801},	// 0x04 <- 0x01 0x65 //357
    {0, 0x0065, 0x8805},
    {0, 0x0001, 0x8800},
    {0, 0x0005, 0x8801},	// 0x05 <- 0x2f
    {0, 0x002f, 0x8805},
    {0, 0x0000, 0x8800},
    {0, 0x0006, 0x8801},	// 0x06 <- 0
    {0, 0x0000, 0x8805},
    {0, 0x0000, 0x8800},
    {0, 0x000a, 0x8801},	// 0x0a <- 2
    {0, 0x0002, 0x8805},
    {0, 0x0000, 0x8800},
    {0, 0x0009, 0x8801},	// 0x09 <- 0x1061
    {0, 0x0061, 0x8805},
    {0, 0x0010, 0x8800},
    {0, 0x0035, 0x8801},	// 0x35 <-0x14
    {0, 0x0014, 0x8805},
    {0, 0x0000, 0x8800},
    {0, 0x0030, 0x8112},	// ISO and drop packet enable
    {0, 0x0000, 0x8112},	// Some kind of reset ????
    {0, 0x0009, 0x8118},	// Enable sensor and set standby
    {0, 0x0000, 0x8114},	// Software GPIO output data
    {0, 0x0000, 0x8114},	// Software GPIO output data
    {0, 0x0001, 0x8114},	// Software GPIO output data
    {0, 0x0000, 0x8112},	// Some kind of reset ???
    {0, 0x0003, 0x8701},
    {0, 0x0001, 0x8703},
    {0, 0x0011, 0x8118},
    {0, 0x0001, 0x8118},
	/**************************/

    {0, 0x0092, 0x8804},
    {0, 0x0010, 0x8802},
    {0, 0x000d, 0x8805},
    {0, 0x0001, 0x8801},
    {0, 0x0000, 0x8800},
    {0, 0x0018, 0x8805},
    {0, 0x0002, 0x8801},
    {0, 0x0000, 0x8800},
    {0, 0x0065, 0x8805},
    {0, 0x0004, 0x8801},
    {0, 0x0001, 0x8800},
    {0, 0x0021, 0x8805},
    {0, 0x0005, 0x8801},
    {0, 0x0000, 0x8800},
    {0, 0x00aa, 0x8805},
    {0, 0x0007, 0x8801},	// mode 0xaa
    {0, 0x0000, 0x8800},
    {0, 0x0004, 0x8805},
    {0, 0x0020, 0x8801},
    {0, 0x0015, 0x8800},	//mode 0x0415
    {0, 0x0002, 0x8805},
    {0, 0x0039, 0x8801},
    {0, 0x0000, 0x8800},
    {0, 0x0010, 0x8805},
    {0, 0x0035, 0x8801},
    {0, 0x0000, 0x8800},
    {0, 0x0049, 0x8805},
    {0, 0x0009, 0x8801},
    {0, 0x0010, 0x8800},
    {0, 0x000b, 0x8805},
    {0, 0x0028, 0x8801},
    {0, 0x0000, 0x8800},
    {0, 0x000f, 0x8805},
    {0, 0x003b, 0x8801},
    {0, 0x0000, 0x8800},
    {0, 0x0000, 0x8805},
    {0, 0x003c, 0x8801},
    {0, 0x0000, 0x8800},
    {0, 0x0002, 0x8502},
    {0, 0x0039, 0x8801},
    {0, 0x0000, 0x8805},
    {0, 0x0000, 0x8800},

    {0, 0x0087, 0x8700},	//overwrite by start
    {0, 0x0081, 0x8702},
    {0, 0x0000, 0x8500},
//      { 0 , 0x0010 , 0x8500 },  -- Previous line was this
    {0, 0x0002, 0x865b},
    {0, 0x0003, 0x865c},
	/************************/
    {0, 0x0003, 0x8801},	// 0x121-> 289
    {0, 0x0021, 0x8805},
    {0, 0x0001, 0x8800},
    {0, 0x0004, 0x8801},	//0x165 -> 357
    {0, 0x0065, 0x8805},
    {0, 0x0001, 0x8800},
    {0, 0x0005, 0x8801},	//0x2f //blanking control colonne
    {0, 0x002f, 0x8805},
    {0, 0x0000, 0x8800},
    {0, 0x0006, 0x8801},	//0x00 //blanking mode row
    {0, 0x0000, 0x8805},
    {0, 0x0000, 0x8800},
    {0, 0x000a, 0x8801},	//0x01 //0x02
    {0, 0x0001, 0x8805},
    {0, 0x0000, 0x8800},
    {0, 0x0009, 0x8801},	// 0x1061 // setexposure times && pixel clock 0001 0 | 000 0110 0001
    {0, 0x0061, 0x8805},	//61 31
    {0, 0x0008, 0x8800},	// 08
    {0, 0x0035, 0x8801},	// 0x14 // set gain general
    {0, 0x001F, 0x8805},	//0x14
    {0, 0x0000, 0x8800},
    {0, 0x0030, 0x8112},
    {0, 0, 0}
};


static void sensor_Reset(struct usb_spca50x *spca50x)
{
    int err;
    err = spca50x_reg_write(spca50x->dev, 0, 0x8631, 0xC8);
    err = spca50x_reg_write(spca50x->dev, 0, 0x8634, 0xC8);
    err = spca50x_reg_write(spca50x->dev, 0, 0x8112, 0x00);
    err = spca50x_reg_write(spca50x->dev, 0, 0x8114, 0x00);
    err = spca50x_reg_write(spca50x->dev, 0, 0x8118, 0x21);
    spca561_InitI2c(spca50x, 0x14);
    spca561_WriteI2c(spca50x, 1, 0x0d);
    spca561_WriteI2c(spca50x, 0, 0x0d);
}

/************************* QC Express etch2 stuff ********************/
static __u16 Pb100_1map8300[][2] = {
/* reg, value */
    {0x8320, 0x3304},
    {0x8303, 0x0125},
    {0x8304, 0x0169},
    {0x8328, 0x000b},
    {0x833c, 0x0007},
    {0x832f, 0x0f00},		//419
    {0x8307, 0x00aa},
    {0x8339, 0x0000},
    {0x8335, 0x0018},
    {0x8309, 0x2048},
    {0x8301, 0x000d},		//3
    {0x8302, 0x0018},		//e
    {0, 0}
};
static __u16 Pb100_2map8300[][2] = {
/* reg, value */
    {0x8339, 0x0000},
    {0x8307, 0x00aa},
    {0, 0}
};

static __u16 spca561_161rev12A_data1[][3] = {
    {0x00, 0x21, 0x8118},	//0x29 enable sensor
    {0x00, 0x01, 0x8114},
    {0x00, 0x00, 0x8112},
    {0x00, 0x92, 0x8804},
    {0x00, 0x04, 0x8802},
};
static __u16 spca561_161rev12A_data2[][3] = {
    {0x00, 0x21, 0x8118},
    //{ 0x00, 0x04, 0x8501 },
    //
    {0x00, 0x00, 0x8114},
    {0x00, 0x01, 0x8114},	//
    {0x00, 0x90, 0x8604},
    {0x00, 0x00, 0x8605},
    {0x00, 0xb0, 0x8603},	//b0 00
    {0x00, 0x02, 0x8201},
    {0x00, 0x08, 0x8200},
    {0x00, 0x01, 0x8200},
    {0x00, 0x07, 0x8201},
    {0x00, 0x08, 0x8200},
    {0x00, 0x01, 0x8200},
    {0x00, 0x08, 0x8620},
    {0x00, 0x0C, 0x8620},
    {0x00, 0x00, 0x8610},	// *rouge
    {0x00, 0x00, 0x8611},	//3f   *vert 
    {0x00, 0x00, 0x8612},	// vert *bleu
    {0x00, 0x00, 0x8613},	//bleu  *vert
    {0x00, 0x35, 0x8614},	// vert *rouge
    {0x00, 0x35, 0x8615},	//40   *vert
    {0x00, 0x35, 0x8616},	//7a   *bleu
    {0x00, 0x35, 0x8617},	//40 *vert

    {0x00, 0xf0, 0x8505},
    {0x00, 0x32, 0x850a},
    {0x00, 0x10, 0x8500},	//11 
    {0x00, 0x07, 0x8601},	//7 18
    {0x00, 0x07, 0x8602},	//7 00
    {0x00, 0x0c, 0x8620},	//0c

    {0x00, 0x7a, 0x8616},	//7a no comments
    {0x00, 0x40, 0x8617},	//40
    {0x00, 0xc8, 0x8631},	//c8
    {0x00, 0xc8, 0x8634},	//c8
    {0x00, 0x23, 0x8635},	//23
    {0x00, 0x1f, 0x8636},	//1f
    {0x00, 0xdd, 0x8637},	//dd
    {0x00, 0xe1, 0x8638},	//e1
    {0x00, 0x1d, 0x8639},	//1d
    {0x00, 0x21, 0x863a},	//21
    {0x00, 0xe3, 0x863b},	//e3
    {0x00, 0xdf, 0x863c},	//df


    {0, 0, 0}
};

static void sensor_mapwrite(struct usb_spca50x *spca50x,
			    __u16 sensormap[][2])
{
    int i = 0;
    __u8 usbval[] = { 0, 0 };

    while (sensormap[i][0]) {
	usbval[0] = sensormap[i][1] & 0xff;
	usbval[1] = (sensormap[i][1] >> 8) & 0xff;
	spca5xxRegWrite(spca50x->dev, 0x00, 0x00, sensormap[i][0], usbval,
			2);
	i++;
    }
}
static int init_161rev12A(struct usb_spca50x *spca50x)
{
    int err;
    __u8 Reg8391[] = { 0x23, 0x31, 0x10, 0x00, 0x3a, 0x00, 0x00, 0x00 };	//14
    __u8 Reg8307[] = { 0xaa, 0x00 };
    err = spca50x_reg_write(spca50x->dev, 0, 0x8620, 0x00);	//
    sensor_Reset(spca50x);
    spca50x_write_vector(spca50x, spca561_161rev12A_data1);
    sensor_mapwrite(spca50x, Pb100_1map8300);
    spca50x_write_vector(spca50x, spca561_161rev12A_data2);
    sensor_mapwrite(spca50x, Pb100_2map8300);
    err = spca50x_reg_write(spca50x->dev, 0, 0x8700, 0x85);	// 0x27 clock
    spca5xxRegWrite(spca50x->dev, 0, 0, 0x8391, Reg8391, 8);
    spca5xxRegWrite(spca50x->dev, 0, 0, 0x8390, Reg8391, 8);
    err = spca50x_reg_write(spca50x->dev, 0, 0x8112, 0x10 | 0x20);
    err = spca50x_reg_write(spca50x->dev, 0, 0x850b, 0x03);
    err = spca50x_reg_write(spca50x->dev, 0, 0x8112, 0x00);

//set_alternate setting 0
    err = spca50x_reg_write(spca50x->dev, 0, 0x8118, 0x29);
    err = spca50x_reg_write(spca50x->dev, 0, 0x8114, 0x00);
//set_alternate setting 7

    spca50x_write_vector(spca50x, spca561_161rev12A_data2);
    spca5xxRegWrite(spca50x->dev, 0, 0, 0x8307, Reg8307, 2);
    err = spca50x_reg_write(spca50x->dev, 0, 0x8700, 0x85);	// 0x27 clock
    spca5xxRegWrite(spca50x->dev, 0, 0, 0x8391, Reg8391, 8);
    spca5xxRegWrite(spca50x->dev, 0, 0, 0x8390, Reg8391, 8);
    err = spca50x_reg_write(spca50x->dev, 0, 0x8112, 0x10 | 0x20);
    err = spca50x_reg_write(spca50x->dev, 0, 0x850b, 0x03);
    err = spca50x_reg_write(spca50x->dev, 0, 0x8112, 0x20);	//
    return 0;

}

/************************* End spca561rev12A stuff **********************/
/************************* Core spca561 stuff ************************/
static int spca561_init(struct usb_spca50x *spca50x)
{
    int err;

    switch (spca50x->chip_revision) {
    case Rev072A:
	PDEBUG(0, "Find spca561 USB Product ID %x", spca50x->customid);
	spca50x_write_vector(spca50x, spca561_init_data);
	break;
    case Rev012A:
	PDEBUG(0, "Find spca561 USB Product ID %x", spca50x->customid);
	err = init_161rev12A(spca50x);
	break;
    default:
	PDEBUG(0, "Error reading USB Product ID from Global register");
	break;
    }
    return 0;
}

#if 0
static void spca561_dumpSensor(struct usb_spca50x *spca50x)
{
    int i;
    __u8 RegSens[] = { 0, 0 };
    switch (spca50x->chip_revision) {
    case Rev072A:
	/*dump sensor registers */
	for (i = 0; i < 0x36; i++) {
	    /* mode 0x10 561, 0x14 mapped */
	    err = spca561_ReadI2c(spca50x, i, 0x10);
	    PDEBUG(0, "reading Sensor i2c register 0x%02X -> 0x%04X", i,
		   err);
	}
	break;
    case Rev012A:
	/* Sensor mapped registers */
	for (i = 0; i < 0x36; i++) {
	    spca5xxRegRead(spca50x->dev, 0, 0, 0x8300 + i, RegSens, 2);
	    PDEBUG(0, "reading Sensor map0x8300 register 0x%02X -> 0x%04X",
		   i, RegSens[1] << 8 | RegSens[0]);
	}
	break;
    }
}
#endif
static void spca561_start(struct usb_spca50x *spca50x)
{
    int err;
    int Clck = 0;
    __u8 Reg8307[] = { 0xaa, 0x00 };
    __u8 Reg8391[] = { 0x90, 0x31, 0x0b, 0x00, 0x25, 0x00, 0x00, 0x00 };	//90 31 0c 
    switch (spca50x->chip_revision) {
    case Rev072A:
	switch (spca50x->mode) {
	case 0:
	case 1:
	    Clck = 0x25;
	    break;
	case 2:
	    Clck = 0x22;
	    break;
	case 3:
	    Clck = 0x21;
	    break;
	default:
	    Clck = 0x25;
	    break;
	}
	err = spca50x_reg_write(spca50x->dev, 0, 0x8500, spca50x->mode);	// mode
	err = spca50x_reg_write(spca50x->dev, 0, 0x8700, Clck);	// 0x27 clock
	err = spca50x_reg_write(spca50x->dev, 0, 0x8112, 0x10 | 0x20);

	break;
    case Rev012A:

	switch (spca50x->mode) {
	case 0:
	    //Clck =(spca50x->customid == 0x403b) ? 0x8a : 0x8f;
	    Clck = 0x8a;
	    break;
	case 1:
	    Clck = 0x8a;
	    break;
	case 2:
	    Clck = 0x85;
	    Reg8391[1] = 0x22;	// increase pixel clock increase time exposure
	    break;
	case 3:
	    Clck = 0x83;
	    Reg8391[1] = 0x22;
	    break;
	default:
	    Clck = 0x25;
	    break;
	}
	if (compress && spca50x->mode <= 1) {
	    // this is correct for 320x240; it also works at 352x288
	    // hell, I don't even know what this value means :)
	    Clck = 0x83;
	    err =
		spca50x_reg_write(spca50x->dev, 0, 0x8500,
				  0x10 + spca50x->mode);
	} else {
	    // I couldn't get the compression to work below 320x240
	    // Fortunately at these resolutions the bandwidth is sufficient
	    // to push raw frames at ~20fps
	    err =
		spca50x_reg_write(spca50x->dev, 0, 0x8500, spca50x->mode);

	}			// -- qq@kuku.eu.org
	spca5xxRegWrite(spca50x->dev, 0, 0, 0x8307, Reg8307, 2);
	err = spca50x_reg_write(spca50x->dev, 0, 0x8700, Clck);	// 0x8f 0x85 0x27 clock

	spca5xxRegWrite(spca50x->dev, 0, 0, 0x8391, Reg8391, 8);
	spca5xxRegWrite(spca50x->dev, 0, 0, 0x8390, Reg8391, 8);
	spca50x->exposure = ((Reg8391[1]) << 8) | Reg8391[0];	//set exposure with clock 
	err = spca50x_reg_write(spca50x->dev, 0, 0x8112, 0x10 | 0x20);

	err = spca50x_reg_write(spca50x->dev, 0, 0x850b, 0x03);

	spca561_setcontrast(spca50x);

	break;
    default:
	PDEBUG(0, "Error reading USB Product ID from Global register");
	break;
    }

}

static void spca561_stopN(struct usb_spca50x *spca50x)
{
    int err;
    err = spca50x_reg_write(spca50x->dev, 0, 0x8112, 0x20);	//
}
static void spca561_setbrightness(struct usb_spca50x *spca50x)
{
    __u8 value = 0;
    value = spca50x->brightness >> 9;
    switch (spca50x->chip_revision) {
    case Rev072A:
	spca5xxRegWrite(spca50x->dev, 0, value, 0x8611, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, value, 0x8612, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, value, 0x8613, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, value, 0x8614, NULL, 0);
	break;
    case Rev012A:
	spca5xxRegWrite(spca50x->dev, 0, value, 0x8615, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, value, 0x8614, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, value, 0x8616, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, value, 0x8617, NULL, 0);
	break;
    }
}
static __u16 spca561_getbrightness(struct usb_spca50x *spca50x)
{
    __u8 value = 0;
    __u16 tot = 0;
    switch (spca50x->chip_revision) {
    case Rev072A:

	spca5xxRegRead(spca50x->dev, 0, 0, 0x8611, &value, 1);
	tot += value;
	spca5xxRegRead(spca50x->dev, 0, 0, 0x8612, &value, 1);
	tot += value;
	spca5xxRegRead(spca50x->dev, 0, 0, 0x8613, &value, 1);
	tot += value;
	spca5xxRegRead(spca50x->dev, 0, 0, 0x8614, &value, 1);
	tot += value;
	spca50x->brightness = tot << 7;
	break;
    case Rev012A:
	spca5xxRegRead(spca50x->dev, 0, 0, 0x8615, &value, 1);
	spca50x->brightness = value << 9;
	break;
    }

    return spca50x->brightness;
}
static void spca561_setcontrast(struct usb_spca50x *spca50x)
{

    __u8 lowb = 0;
    int expotimes = 0;
    int pixelclk = 0;
    __u8 Reg8391[] = { 0x90, 0x31, 0x0b, 0x00, 0x25, 0x00, 0x00, 0x00 };
    switch (spca50x->chip_revision) {
    case Rev072A:
	lowb = (spca50x->contrast >> 8) & 0xFF;
	spca5xxRegWrite(spca50x->dev, 0, lowb, 0x8651, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, lowb, 0x8652, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, lowb, 0x8653, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0, lowb, 0x8654, NULL, 0);
	break;
    case Rev012A:
	lowb = (spca50x->contrast >> 10) & 0x7F;
	if (lowb < 4)
	    lowb = 3;
	pixelclk = spca50x->exposure & 0xf800;
	spca50x->exposure = ((spca50x->contrast >> 5) & 0x07ff) | pixelclk;
	expotimes = spca50x->exposure & 0x07ff;
	Reg8391[0] = expotimes & 0xff;
	Reg8391[1] = ((pixelclk >> 8) & 0xf8) | ((expotimes >> 8) & 0x07);
	Reg8391[2] = lowb;
	PDEBUG(4, "Set Exposure 0x%02x 0x%02x gain 0x%02x", Reg8391[0],
	       Reg8391[1], Reg8391[2]);
	spca5xxRegWrite(spca50x->dev, 0, 0, 0x8390, Reg8391, 8);
	break;
    }

}
static __u16 spca561_getcontrast(struct usb_spca50x *spca50x)
{
    __u8 value = 0;
    __u16 tot = 0;
    __u8 contrast = 0x0b;
    __u8 RegSens[] = { 0, 0 };
    switch (spca50x->chip_revision) {
    case Rev072A:

	value = 0;
	spca5xxRegRead(spca50x->dev, 0, 0, 0x8651, &value, 1);
	tot += value;
	spca5xxRegRead(spca50x->dev, 0, 0, 0x8652, &value, 1);
	tot += value;
	spca5xxRegRead(spca50x->dev, 0, 0, 0x8653, &value, 1);
	tot += value;
	spca5xxRegRead(spca50x->dev, 0, 0, 0x8654, &value, 1);
	tot += value;
	spca50x->contrast = tot << 6;
	break;
    case Rev012A:

	spca5xxRegWrite(spca50x->dev, 0, 0, 0x8335, &contrast, 1);
	/* always 0x8335 return 0 */
	spca5xxRegRead(spca50x->dev, 0, 0, 0x8335, RegSens, 2);
	spca50x->contrast = (contrast & 0x7f) << 10;
	PDEBUG(2, "Get constrast 0x8335 0x%04x",
	       RegSens[1] << 8 | RegSens[0]);
	break;
    }
    PDEBUG(4,"get contrast %d\n",spca50x->contrast);
    return spca50x->contrast;
}
static int spca561_config(struct usb_spca50x *spca50x)
{
    __u8 data1, data2;
    // Read frm global register the USB product and vendor IDs, just to     
    // prove that we can communicate with the device.  This works, which
    // confirms at we are communicating properly and that the device
    // is a 561.
    spca5xxRegRead(spca50x->dev, 0, 0, 0x8104, &data1, 1);
    spca5xxRegRead(spca50x->dev, 0, 0, 0x8105, &data2, 1);
    PDEBUG(1, "Read from GLOBAL: USB Vendor ID 0x%02x%02x", data2, data1);
    spca5xxRegRead(spca50x->dev, 0, 0, 0x8106, &data1, 1);
    spca5xxRegRead(spca50x->dev, 0, 0, 0x8107, &data2, 1);
    PDEBUG(1, "Read from GLOBAL: USB Product ID 0x%02x%02x", data2, data1);
    spca50x->customid = ((data2 << 8) | data1) & 0xffff;
    switch (spca50x->customid) {
    case 0x7004:
    case 0xa001:
    case 0x0815:
    case 0x0561:
    case 0xcdee:
    case 0x7e50:
	spca50x->chip_revision = Rev072A;
	break;
    case 0x0928:
    case 0x0929:
    case 0x092a:
    case 0x403b:
    case 0x092b:
    case 0x092c:
    case 0x092d:
    case 0x092e:
    case 0x092f:
	spca50x->chip_revision = Rev012A;
	break;
    default:
	PDEBUG(0, "Spca561 chip Unknow Contact the Author");
	return -EINVAL;
	break;
    }
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
    return 0;			// success
}
static void spca561_shutdown(struct usb_spca50x *spca50x)
{
    spca5xxRegWrite(spca50x->dev, 0, 0, 0x8114, NULL, 0);
}
static void spca561_setAutobright(struct usb_spca50x *spca50x)
{
    int expotimes = 0;
    int pixelclk = 0;
    int gainG = 0;
    __u8 R, Gr, Gb, B;
    int y;
    __u8 luma_mean = 110;
    __u8 luma_delta = 20;
    __u8 spring = 4;
    switch (spca50x->chip_revision) {
    case Rev072A:
	spca5xxRegRead(spca50x->dev, 0, 0, 0x8621, &Gr, 1);
	spca5xxRegRead(spca50x->dev, 0, 0, 0x8622, &R, 1);
	spca5xxRegRead(spca50x->dev, 0, 0, 0x8623, &B, 1);
	spca5xxRegRead(spca50x->dev, 0, 0, 0x8624, &Gb, 1);
	y = (77 * R + 75 * (Gr + Gb) + 29 * B) >> 8;
	//u= (128*B-(43*(Gr+Gb+R))) >> 8;
	//v= (128*R-(53*(Gr+Gb))-21*B) >> 8;
	//PDEBUG(0,"reading Y %d U %d V %d ",y,u,v);

	if ((y < (luma_mean - luma_delta)) ||
	    (y > (luma_mean + luma_delta))) {
	    expotimes = spca561_ReadI2c(spca50x, 0x09, 0x10);
	    pixelclk = 0x0800;
	    expotimes = expotimes & 0x07ff;
	    //PDEBUG(0,"Exposition Times 0x%03X Clock 0x%04X ",expotimes,pixelclk);
	    gainG = spca561_ReadI2c(spca50x, 0x35, 0x10);
	    //PDEBUG(0,"reading Gain register %d",gainG);

	    expotimes += ((luma_mean - y) >> spring);
	    gainG += ((luma_mean - y) / 50);
	    // PDEBUG(0 , "compute expotimes %d gain %d",expotimes,gainG);

	    if (gainG > 0x3F)
		gainG = 0x3f;
	    else if (gainG < 4)
		gainG = 3;
	    spca561_WriteI2c(spca50x, (__u16) gainG, 0x35);


	    if (expotimes >= 0x0256)
		expotimes = 0x0256;
	    else if (expotimes < 4) {
		expotimes = 3;
	    }

	    spca561_WriteI2c(spca50x, (__u16) (expotimes | pixelclk),
			     0x09);
	}

	break;
    case Rev012A:
	/* sensor registers is access and memory mapped to 0x8300 */
	/* readind all 0x83xx block the sensor */
	/*
	   The data from the header seem wrong where is the luma and chroma mean value
	   at the moment set exposure in contrast set 
	 */
	;
	break;
    default:
	break;
    }
}
static int spca561_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength)
{
	    
	   switch (cdata[0]){
	   case 0:
	   	*iPix = SPCA561_OFFSET_DATA;
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
#endif
