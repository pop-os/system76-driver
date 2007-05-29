#ifndef CX11646USB_H
#define CX11646USB_H
/****************************************************************************
#	 	Connexant Cx11646    library                                #
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
#include "cxlib.h"
/**************************************************************************/
static int cx11646_init(struct usb_spca50x *spca50x);
static void cx11646_start(struct usb_spca50x *spca50x);
static void cx11646_stop0(struct usb_spca50x *spca50x);
static void cx11646_stopN(struct usb_spca50x *spca50x);
static __u16 cx_getbrightness(struct usb_spca50x *spca50x);
static __u16 cx_getcontrast(struct usb_spca50x *spca50x);
static __u16 cx_getcolors(struct usb_spca50x *spca50x);
static void cx_setbrightness(struct usb_spca50x *spca50x);
static void cx_setcontrast(struct usb_spca50x *spca50x);
static void cx_setcolors(struct usb_spca50x *spca50x);
static int cx11646_config(struct usb_spca50x *spca50x);
static void cx11646_shutdown(struct usb_spca50x *spca50x);
static void cx11646_setAutobright(struct usb_spca50x *spca50x);
static void cx11646_setquality(struct usb_spca50x *spca50x);
static int cx11646_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char* cdata,int *iPix, int seqnum, int *datalength);
/**************************************************************************/
static void cx11646_stopN(struct usb_spca50x *spca50x){}
static void cx11646_shutdown(struct usb_spca50x *spca50x){}
static void cx11646_setAutobright(struct usb_spca50x *spca50x){}
static void cx11646_setquality(struct usb_spca50x *spca50x){}
/**************************************************************************/
static struct cam_operation fcx11646 = {
 	.initialize = cx11646_init,
	.configure = cx11646_config,
	.start = cx11646_start,
	.stopN = cx11646_stopN,
	.stop0 = cx11646_stop0,
	.get_bright = cx_getbrightness,
	.set_bright = cx_setbrightness,
	.get_contrast = cx_getcontrast,
	.set_contrast = cx_setcontrast,
	.get_colors = cx_getcolors,
	.set_colors = cx_setcolors,
	.set_autobright = cx11646_setAutobright,
	.set_quality = cx11646_setquality,
	.cam_shutdown = cx11646_shutdown,
	.sof_detect = cx11646_sofdetect,
 };
static int cx11646_init(struct usb_spca50x *spca50x)
{
    int err;
    cx11646_init1(spca50x);
    err = cx11646_initsize(spca50x);
    cx11646_fw(spca50x);
    cx_sensor(spca50x);
    cx11646_jpegInit(spca50x);
    return 0;
}
static void cx11646_start(struct usb_spca50x *spca50x)
{
    int err;
    err = cx11646_initsize(spca50x);
    cx11646_fw(spca50x);
    cx_sensor(spca50x);
    cx11646_jpeg(spca50x);
}
static void cx11646_stop0(struct usb_spca50x *spca50x)
{

    int retry = 50;
    __u8 val = 0;
    spca5xxRegWrite(spca50x->dev, 0x00, 0x00, 0x0000, &val, 1);
    spca5xxRegRead(spca50x->dev, 0x00, 0x00, 0x0002, &val, 1);
    val = 0;
    spca5xxRegWrite(spca50x->dev, 0x00, 0x00, 0x0053, &val, 1);

    while (retry--) {
	//spca5xxRegRead (spca50x->dev,0x00,0x00,0x0002,&val,1);
	spca5xxRegRead(spca50x->dev, 0x00, 0x00, 0x0053, &val, 1);
	if (val == 0)
	    break;
    }
    val = 0;
    spca5xxRegWrite(spca50x->dev, 0x00, 0x00, 0x0000, &val, 1);
    spca5xxRegRead(spca50x->dev, 0x00, 0x00, 0x0002, &val, 1);

    val = 0;
    spca5xxRegWrite(spca50x->dev, 0x00, 0x00, 0x0010, &val, 1);
    spca5xxRegRead(spca50x->dev, 0x00, 0x00, 0x0033, &val, 1);
    val = 0xE0;
    spca5xxRegWrite(spca50x->dev, 0x00, 0x00, 0x00fc, &val, 1);

}
static int cx11646_config(struct usb_spca50x *spca50x)
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
	P_JPEG | P_RAW | P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[SIF].pipe = 1023;
    spca50x->mode_cam[SIF].method = 0;
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
	P_JPEG | P_RAW |P_YUV420 | P_RGB32 | P_RGB24 | P_RGB16;
    spca50x->mode_cam[QSIF].pipe = 640;
    spca50x->mode_cam[QSIF].method = 0;
    spca50x->mode_cam[QSIF].mode = 3;
    
return 0;
}
static int cx11646_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength)
{
   *iPix = 0;
		if (cdata[0] == 0xFF && cdata[1] == 0xD8) {
		    *iPix = 2;
		    *datalength -= *iPix;
		    PDEBUG(5,
			   "Cx11646 header packet found datalength %d !!",
			   *datalength);
		   return 0;
		} else 
		   return (seqnum+1);
}
#endif				//CX11646USB_H
