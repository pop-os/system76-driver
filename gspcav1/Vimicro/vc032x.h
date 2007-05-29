
#ifndef VC032XUSB_H
#define VC032XUSB_H
/****************************************************************************
#	 	Z-star vc0321 library                                       #
# 		Copyright (C) 2006 Koninski Artur    takeshi87@o2.pl        #
# 		Copyright (C) 2006 Michel Xhaard                            #
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

#include "vc032x_sensor.h"

/*******************     Camera Interface   ***********************/
static int vc0321_init(struct usb_spca50x *spca50x);
static void vc0321_start(struct usb_spca50x *spca50x);
static void vc0321_stop0(struct usb_spca50x *spca50x);
static void vc0321_stopN(struct usb_spca50x *spca50x);
static int vc0321_config(struct usb_spca50x *spca50x);
static void vc0321_shutdown(struct usb_spca50x *spca50x);

static __u16 vc0321_getbrightness(struct usb_spca50x *spca50x);
static __u16 vc0321_getcontrast(struct usb_spca50x *spca50x);
static __u16 vc0321_getcolors(struct usb_spca50x *spca50x);
static void vc0321_setbrightness(struct usb_spca50x *spca50x);
static void vc0321_setcontrast(struct usb_spca50x *spca50x);
static void vc0321_setcolors(struct usb_spca50x *spca50x);
;
static void vc0321_setAutobright(struct usb_spca50x *spca50x);
static void vc0321_setquality(struct usb_spca50x *spca50x);
static int vc0321_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength);
/*******************     Camera Private     ***********************/

/******************************************************************/
static struct cam_operation fvc0321 = {
 	.initialize = vc0321_init,
	.configure = vc0321_config,
	.start = vc0321_start,
	.stopN = vc0321_stopN,
	.stop0 = vc0321_stop0,
	.get_bright = vc0321_getbrightness,
	.set_bright = vc0321_setbrightness,
	.get_contrast = vc0321_getcontrast,
	.set_contrast = vc0321_setcontrast,
	.get_colors = vc0321_getcolors,
	.set_colors = vc0321_setcolors,
	.set_autobright = vc0321_setAutobright,
	.set_quality = vc0321_setquality,
	.cam_shutdown = vc0321_shutdown,
	.sof_detect = vc0321_sofdetect,
 };
 typedef struct {
	int sensorId;
 	__u8 I2cAdd;
	__u8 IdAdd;
	__u16 VpId;
	__u8 m1;
	__u8 m2;
	__u8 op;
	} sensor_info;
	
static sensor_info sensor_info_data[] = {
//      sensorId,         I2cAdd,     IdAdd,  VpId,  m1,    m2,  op
	{SENSOR_HV7131R, 0x80 | 0x11, 0x00, 0x0209, 0x24, 0x25, 0x01},
	{SENSOR_OV7660, 0x80 | 0x21 , 0x0a, 0x7660, 0x26, 0x26, 0x05},
	{SENSOR_PO3130NC,0x80 | 0x76, 0x00, 0x3130, 0x24, 0x25, 0x01},
};
static void vc032x_read_sensor_register( struct usb_device *dev,
	__u16 address, __u16 *value)
{
	__u8	ldata, mdata, hdata;
	__u8 tmpvalue = 0;
	int retry = 50;
	ldata = 0;
	mdata = 0;
	hdata = 0;
	*value = 0;
	
	spca5xxRegRead( dev, 0xa1, 0x01, 0xb33f, &tmpvalue, 1 );
	//PDEBUG(0, " I2c Bus Busy Wait  0x%02X ", tmpvalue);
	if(!(tmpvalue & 0x02)) {
		PDEBUG(0, " I2c Bus Busy Wait  %d ", tmpvalue & 0x02);
		return;
	}
	spca5xxRegWrite( dev, 0xa0, address, 0xb33a, NULL, 0 );
	spca5xxRegWrite( dev, 0xa0, 0x02, 0xb339, NULL, 0 );
	
	tmpvalue = 0;
	spca5xxRegRead( dev, 0xa1, 0x01, 0xb33b, &tmpvalue, 1 );
	while( retry-- && tmpvalue){
		spca5xxRegRead( dev, 0xa1, 0x01, 0xb33b, &tmpvalue, 1 );
		//PDEBUG(0, "Read again 0xb33b  %d ", tmpvalue);
		udelay( 1000 );
	}
	spca5xxRegRead ( dev, 0xa1, 0x01, 0xb33e, &hdata, 1 );
	spca5xxRegRead ( dev, 0xa1, 0x01, 0xb33d, &mdata, 1 );
	spca5xxRegRead ( dev, 0xa1, 0x01, 0xb33c, &ldata, 1 );
	//PDEBUG(0, "Read Sensor h (0x%02X) m (0x%02X) l (0x%02X) ", hdata,mdata,ldata);
	tmpvalue = 0;
	spca5xxRegRead( dev, 0xa1, 0x01, 0xb334, &tmpvalue, 1 );
	if(tmpvalue == 0x02)
		*value = (ldata << 8) + mdata;
	else 
		*value = ldata;
}
static int vc032x_probe_sensor(struct usb_spca50x *spca50x)
{
	int i;
	__u8 data;
	__u16	value;
	sensor_info *ptsensor_info;
	int sensor_id = -1;
	int VCSENSOR_TOT= 3;
	spca5xxRegRead ( spca50x->dev, 0xa1, 0x01, 0xbfcf, &data, 1 );
	PDEBUG(0,"check sensor header %d",data);
	for(i= 0; i < VCSENSOR_TOT; i++){
		ptsensor_info = &sensor_info_data[i];
		spca5xxRegWrite( spca50x->dev, 0xa0, 0x02, 0xb334, NULL, 0);
		spca5xxRegWrite( spca50x->dev, 0xa0, ptsensor_info->m1, 0xb300, NULL, 0);
		spca5xxRegWrite( spca50x->dev, 0xa0, ptsensor_info->m2, 0xb300, NULL, 0);
		spca5xxRegWrite( spca50x->dev, 0xa0, 0x01, 0xb308, NULL, 0);
		spca5xxRegWrite( spca50x->dev, 0xa0, 0x0c, 0xb309, NULL, 0);
		spca5xxRegWrite( spca50x->dev, 0xa0, ptsensor_info->I2cAdd, 0xb335, NULL, 0);
	// PDEBUG(0,"check sensor VC032X -> %d Add -> ox%02X!", i, ptsensor_info->I2cAdd);
		spca5xxRegWrite( spca50x->dev, 0xa0, ptsensor_info->op, 0xb301, NULL, 0);
		vc032x_read_sensor_register ( spca50x->dev, ptsensor_info->IdAdd, &value );
		if(value == ptsensor_info->VpId) {
			// PDEBUG(0,"find sensor VC032X -> ox%04X!",ptsensor_info->VpId);
			sensor_id = ptsensor_info->sensorId;
			break;
		}
	}
return sensor_id;
}
/*
static __u8 vc0321_i2cWrite(struct usb_device *dev, __u8 reg, __u8 val)
{
    __u8 retbyte = 0;
    
    spca5xxRegRead (dev, 0xa1, 0x01, 0xb33f, &retbyte, 1);	    udelay(10);
    spca5xxRegWrite(dev, 0xa0, reg , 0xb33a, NULL    , 0);	    udelay(10);
    spca5xxRegRead (dev, 0xa1, 0x01, 0xb334, &retbyte, 1);	    udelay(10);
    spca5xxRegWrite(dev, 0xa0, val , 0xb336, NULL    , 0);	    udelay(10);
    spca5xxRegWrite(dev, 0xa0, 0x01, 0xb339, NULL    , 0);	    udelay(10);
    spca5xxRegRead (dev, 0xa1, 0x01, 0xb33b, &retbyte, 1);	    udelay(10);
    return (retbyte==0);
}
*/
static __u8 vc0321_i2cWrite(struct usb_device *dev, __u8 reg, __u8 *val, __u8 size)
{
    __u8 retbyte = 0;
    if(size > 3 || size < 1)
    	return -EINVAL;
	spca5xxRegRead (dev, 0xa1, 0x01, 0xb33f, &retbyte, 1);	    udelay(10);
	spca5xxRegWrite(dev, 0xa0, size , 0xb334, NULL    , 0);
	spca5xxRegWrite(dev, 0xa0, reg , 0xb33a, NULL    , 0);	    udelay(10);
	switch (size){
	case 1:
	spca5xxRegWrite(dev, 0xa0, val[0] , 0xb336, NULL    , 0);	    udelay(10);
	break;
	case 2:
	spca5xxRegWrite(dev, 0xa0, val[0] , 0xb336, NULL    , 0);	    udelay(10);
	spca5xxRegWrite(dev, 0xa0, val[1] , 0xb337, NULL    , 0);	    udelay(10);
	break;
	case 3:
	spca5xxRegWrite(dev, 0xa0, val[0] , 0xb336, NULL    , 0);	    udelay(10);
	spca5xxRegWrite(dev, 0xa0, val[1] , 0xb337, NULL    , 0);	    udelay(10);
	spca5xxRegWrite(dev, 0xa0, val[2] , 0xb338, NULL    , 0);	    udelay(10);
	break;
	default:
		spca5xxRegWrite(dev, 0xa0, 0x01, 0xb334, NULL    , 0);
		return -EINVAL;
	break;
	}
    spca5xxRegWrite(dev, 0xa0, 0x01, 0xb339, NULL    , 0);	    udelay(10);
    spca5xxRegRead (dev, 0xa1, 0x01, 0xb33b, &retbyte, 1);	    udelay(10);
    return (retbyte==0);
}

static void put_tab_to_reg(struct usb_spca50x *spca50x, __u8 *tab, __u8 tabsize, __u16 addr)
{
    __u8 j;
    __u16 ad=addr;
	for(j=0; j < tabsize; j++)
	{
	    spca5xxRegWrite(spca50x->dev, 0xa0, tab[j], ad++, NULL, 0);
	    udelay(10);
	}
}



static __u16 vc0321WriteVector(struct usb_spca50x *spca50x, __u8 data[][4])
{
    struct usb_device *dev = spca50x->dev;
    int err = 0;
    int i = 0;
    while (data[i][3]) {
	if (data[i][3] == 0xcc)	{	//normal op
		/* write registers */
	        spca5xxRegWrite(dev, 0xa0, data[i][2], ((data[i][0])<<8) | data[i][1], NULL,
	    		    0);
	}
	else if(data[i][3] == 0xaa) {  //i2c op
		vc0321_i2cWrite(dev, data[i][1], &data[i][2],1);
	}
	else if(data[i][3] == 0xdd) {
	    mdelay(data[i][2]+10);
	}
	i++;
	udelay(10);
    }

    return err;
}

#define CLAMP(x) (unsigned char)(((x)>0xFF)?0xff:(((x)<1)?1:(x)))

/*
"GammaT"=hex:04,17,31,4f,6a,83,99,ad,bf,ce,da,e5,ee,f5,fb,ff,ff
"MatrixT"=hex:60,f9,e5,e7,50,05,f3,e6,66
*/



static __u16 vc0321_getbrightness(struct usb_spca50x *spca50x)
{
    spca50x->brightness = 0x80 << 8;
    spca50x->contrast = 0x80 << 8;
    return spca50x->brightness;
}
static __u16 vc0321_getcontrast(struct usb_spca50x *spca50x)
{
    spca50x->contrast = 0x80 << 8;
    return spca50x->contrast;
}
static void vc0321_setbrightness(struct usb_spca50x *spca50x)
{
    __u8 brightness;
    brightness = spca50x->brightness >> 8 ;

}
static void vc0321_setcontrast(struct usb_spca50x *spca50x)
{

    __u16 contrast;
    contrast = vc0321_getcontrast(spca50x);

}



static int vc0321_init(struct usb_spca50x *spca50x)
{
    return 0;
}

static void set_vc0321VGA(struct usb_spca50x *spca50x)
{
    memset(spca50x->mode_cam, 0x00, TOTMODE * sizeof(struct mwebcam));
    spca50x->mode_cam[VGA].width = 640;
    spca50x->mode_cam[VGA].height = 480;
    spca50x->mode_cam[VGA].t_palette =
	 P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[VGA].pipe = 3072;
    spca50x->mode_cam[VGA].method = 0;
    spca50x->mode_cam[VGA].mode = 0;

    spca50x->mode_cam[PAL].width = 384;
    spca50x->mode_cam[PAL].height = 288;
    spca50x->mode_cam[PAL].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[PAL].pipe = 3072;
    spca50x->mode_cam[PAL].method = 1;
    spca50x->mode_cam[PAL].mode = 0;
    
    spca50x->mode_cam[SIF].width = 352;
    spca50x->mode_cam[SIF].height = 288;
    spca50x->mode_cam[SIF].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[SIF].pipe = 3072;
    spca50x->mode_cam[SIF].method = 1;
    spca50x->mode_cam[SIF].mode = 0;
    
    spca50x->mode_cam[CIF].width = 320;
    spca50x->mode_cam[CIF].height = 240;
    spca50x->mode_cam[CIF].t_palette =
	 P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[CIF].pipe = 3072;
    spca50x->mode_cam[CIF].method = 0;
    spca50x->mode_cam[CIF].mode = 1;
    
    spca50x->mode_cam[QPAL].width = 192;
    spca50x->mode_cam[QPAL].height = 144;
    spca50x->mode_cam[QPAL].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QPAL].pipe = 3072;
    spca50x->mode_cam[QPAL].method = 1;
    spca50x->mode_cam[QPAL].mode = 1;
    
    spca50x->mode_cam[QSIF].width = 176;
    spca50x->mode_cam[QSIF].height = 144;
    spca50x->mode_cam[QSIF].t_palette =
	P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QSIF].pipe = 3072;
    spca50x->mode_cam[QSIF].method = 1;
    spca50x->mode_cam[QSIF].mode = 1;
    
}
static int vc0321_reset(struct usb_spca50x *spca50x)
{
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x00, 0xb04d, NULL, 0);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0xb301, NULL, 0); 
	msleep(100);
	spca5xxRegWrite(spca50x->dev, 0xa0, 0x01, 0xb003, NULL, 0);
	msleep(100);
return 0;
}
static int vc0321_config(struct usb_spca50x *spca50x)
{
 __u8 tmp2[3];
    int sensor = 0;
    spca50x->qindex = 1;
    vc0321_reset(spca50x);
    sensor = vc032x_probe_sensor(spca50x);
    switch (sensor) {
    	case -1:
		PDEBUG(0,"Unknown sensor...");
		return -EINVAL;
	break;
   	case SENSOR_OV7660:
		PDEBUG(0, "Find Sensor OV7660");
		spca50x->sensor = SENSOR_OV7660;
		set_vc0321VGA(spca50x);
	break;
	case SENSOR_PO3130NC:
		PDEBUG(0, "Find Sensor PO3130NC");
		spca50x->sensor = SENSOR_PO3130NC;
		set_vc0321VGA(spca50x);
	break;
	case SENSOR_HV7131R:
		PDEBUG(0, "Find Sensor HV7131R");
		spca50x->sensor = SENSOR_HV7131R;
		set_vc0321VGA(spca50x);
	break;
    };
spca5xxRegRead (spca50x->dev, 0x8a, 0x01, 0     , tmp2, 3); udelay(10);
spca5xxRegWrite(spca50x->dev, 0x87, 0x00, 0x0f0f, NULL, 0); udelay(10);

spca5xxRegRead (spca50x->dev, 0x8b, 0x01, 0     , tmp2, 3); udelay(10);
spca5xxRegWrite(spca50x->dev, 0x88, 0x00, 0x0202, NULL, 0); udelay(10);
    return 0;
}
static void vc0321_setquality(struct usb_spca50x *spca50x)
{
    __u8 quality = 0;
    quality = (spca50x->qindex) & 0xff;
//    spca5xxRegWrite(spca50x->dev, 0xa0, quality, 0x0008, NULL, 0);
}
static void vc0321_setAutobright(struct usb_spca50x *spca50x)
{
    __u8 autoval = 0;
    if (spca50x->autoexpo)
	autoval = 0x42;
    else
	autoval = 0x02;
//    spca5xxRegWrite(spca50x->dev, 0xa0, autoval, 0x0180, NULL, 0);

}

static void vc0321_start(struct usb_spca50x *spca50x)
{
	// __u8 tmp2;
    int err = 0;
    __u8 *GammaT = NULL;
    __u8 *MatrixT = NULL;
    /* Assume start use the good resolution from spca50x->mode */
    spca5xxRegWrite(spca50x->dev, 0xa0, 0xff, 0xbfec, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0xa0, 0xff, 0xbfed, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0xa0, 0xff, 0xbfee, NULL, 0);
    spca5xxRegWrite(spca50x->dev, 0xa0, 0xff, 0xbfef, NULL, 0);
    switch (spca50x->sensor) {
    	case SENSOR_OV7660:
    		GammaT = ov7660_gamma;
    		MatrixT = ov7660_matrix;
		if (spca50x->mode) {
	    		/* 320x240 */
			 err = vc0321WriteVector(spca50x, ov7660_initQVGA_data);
		} else {
	    		/* 640x480 */
	   		 err = vc0321WriteVector(spca50x, ov7660_initVGA_data);
		}
			
	break;
	case SENSOR_PO3130NC:
		GammaT = po3130_gamma;
    		MatrixT = po3130_matrix;
		if (spca50x->mode) {
	    		/* 320x240 */
			 err = vc0321WriteVector(spca50x, po3130_initQVGA_data);
		} else {
	    		/* 640x480 */
	   		 err = vc0321WriteVector(spca50x, po3130_initVGA_data);
		}
	err = vc0321WriteVector(spca50x, po3130_rundata);
	break;
	case SENSOR_HV7131R:
		GammaT = hv7131r_gamma;
    		MatrixT = hv7131r_matrix;
		
		if (spca50x->mode) {
	    		/* 320x240 */
			 err = vc0321WriteVector(spca50x, hv7131r_initQVGA_data);
		} else {
	    		/* 640x480 */
	   		 err = vc0321WriteVector(spca50x, hv7131r_initVGA_data);
		}
		 
	break;
	default:
		PDEBUG(0, "Damned !! no sensor found Bye");
		return;
	break;
    }
    if (GammaT && MatrixT){
	put_tab_to_reg(spca50x, GammaT, 17, 0xb84a);
	put_tab_to_reg(spca50x, GammaT, 17, 0xb85b);
	put_tab_to_reg(spca50x, GammaT, 17, 0xb86c);
	put_tab_to_reg(spca50x, MatrixT, 9, 0xb82c);
	
		// Seem SHARPNESS
		/*
		 spca5xxRegWrite(spca50x->dev, 0xa0, 0x80, 0xb80a, NULL, 0);
		 spca5xxRegWrite(spca50x->dev, 0xa0, 0xff, 0xb80b, NULL, 0);
		 spca5xxRegWrite(spca50x->dev, 0xa0, 0xff, 0xb80e, NULL, 0);
		 */
		 /* all 0x40 ??? do nothing
		 spca5xxRegWrite(spca50x->dev, 0xa0, 0x40, 0xb822, NULL, 0);
		  spca5xxRegWrite(spca50x->dev, 0xa0, 0x40, 0xb823, NULL, 0);
		   spca5xxRegWrite(spca50x->dev, 0xa0, 0x40, 0xb824, NULL, 0);
		 */
		 /* Only works for HV7131R ?? 
		 spca5xxRegRead (spca50x->dev, 0xa1, 0x01, 0xb881, &tmp2, 1); udelay(10);
		 spca5xxRegWrite(spca50x->dev, 0xa0, 0xfe01, 0xb881, NULL, 0);
		 spca5xxRegWrite(spca50x->dev, 0xa0, 0x79, 0xb801, NULL, 0);
		 */
		 /* only hv7131r et ov7660 
		 spca5xxRegWrite(spca50x->dev, 0xa0, 0x20, 0xb827, NULL, 0);
		 spca5xxRegWrite(spca50x->dev, 0xa0, 0xff, 0xb826, NULL, 0); //ISP_GAIN 80
		 spca5xxRegWrite(spca50x->dev, 0xa0, 0x23, 0xb800, NULL, 0); // ISP CTRL_BAS
		 */
	// set the led on 0x0892 0x0896
        spca5xxRegWrite(spca50x->dev, 0x89, 0xffff, 0xfdff, NULL, 0);
	msleep(100);
    	vc0321_setbrightness(spca50x);
    	vc0321_setquality(spca50x);
    	vc0321_setAutobright(spca50x);
    }
}

static void vc0321_stopN(struct usb_spca50x *spca50x)
{
    struct usb_device *dev = spca50x->dev;
    spca5xxRegWrite(dev, 0x89, 0xffff, 0xffff, NULL, 0);
    spca5xxRegWrite(dev, 0xa0, 0x01, 0xb301, NULL, 0);
    spca5xxRegWrite(dev, 0xa0, 0x09, 0xb003, NULL, 0);
}

static void vc0321_stop0(struct usb_spca50x *spca50x)
{
    struct usb_device *dev = spca50x->dev;
    spca5xxRegWrite(dev, 0x89, 0xffff, 0xffff, NULL, 0);
}

static void vc0321_shutdown(struct usb_spca50x *spca50x)
{
/*    struct usb_device *dev = spca50x->dev;
    __u8 buffread;
    spca5xxRegWrite(dev, 0x89, 0xffff, 0xffff, NULL, 0);
    spca5xxRegWrite(dev, 0xa0, 0x01, 0xb301, NULL, 0);
    spca5xxRegWrite(dev, 0xa0, 0x09, 0xb303, NULL, 0);
    spca5xxRegWrite(dev, 0x89, 0xffff, 0xffff, NULL, 0);
*/
}

static __u16 vc0321_getcolors(struct usb_spca50x *spca50x)
{
//Nothing
return spca50x->colour;
}

static void vc0321_setcolors(struct usb_spca50x *spca50x)
{
//Nothing
 spca50x->colour = 0;
}

static int vc0321_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength)
{
		
		if (cdata[0] == 0xFF && cdata[1] == 0xD8) {
		// FIXME how can we change Hstart ??
			if(spca50x->sensor == SENSOR_OV7660)
		    	*iPix = 44 ;// 46;	//18 remove 0xff 0xd8;
		    	else 
			*iPix = 46 ;
		     PDEBUG(5,
			   "vc0321 header packet found datalength %d !!",
			   *datalength );
		    *datalength -= *iPix;
		    return 0;
		   
		} 
		*iPix = 0;
		PDEBUG(5, "vc0321 process packet %d datalength %d ",seqnum+1,*datalength);
		return (seqnum +1);
}
#endif				// VC032XUSB_H
