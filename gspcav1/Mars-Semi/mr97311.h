/****************************************************************************
#	 	Mars-Semi MR97311A library                                  #
# 		Copyright (C) 2005 <bradlch@hotmail.com>                    #
# Part of spca5xx project                                                   #
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
static int mr97311_init(struct usb_spca50x *pcam);
static void mr97311_start(struct usb_spca50x *pcam);
static void mr97311_stopN(struct usb_spca50x *pcam);
static void mr97311_stop0(struct usb_spca50x *pcam);
static int mr97311_config(struct usb_spca50x *pcam);
static __u16 mr97311_getbrightness(struct usb_spca50x *spca50x);
static __u16 mr97311_getcontrast(struct usb_spca50x *spca50x);
static __u16 mr97311_getcolors(struct usb_spca50x *spca50x);
static void mr97311_setbrightness(struct usb_spca50x *spca50x);
static void mr97311_setcontrast(struct usb_spca50x *spca50x);
static void mr97311_setcolors(struct usb_spca50x *spca50x);
static void mr97311_shutdown(struct usb_spca50x *spca50x);
static void mr97311_setAutobright(struct usb_spca50x *spca50x);
static void mr97311_setquality(struct usb_spca50x *spca50x);
static int mr97311_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength);
/*****************************************************************/
static int mr97311_init(struct usb_spca50x *pcam){return 0;}
static __u16 mr97311_getbrightness(struct usb_spca50x *spca50x){return 0;}
static __u16 mr97311_getcontrast(struct usb_spca50x *spca50x){return 0;}
static __u16 mr97311_getcolors(struct usb_spca50x *spca50x){return 0;}
static void mr97311_setbrightness(struct usb_spca50x *spca50x){}
static void mr97311_setcontrast(struct usb_spca50x *spca50x){}
static void mr97311_setcolors(struct usb_spca50x *spca50x){}

static void mr97311_shutdown(struct usb_spca50x *spca50x){}
static void mr97311_setAutobright(struct usb_spca50x *spca50x){}
static void mr97311_setquality(struct usb_spca50x *spca50x){}
static void mr97311_stop0(struct usb_spca50x *pcam){}
/****************************************************************/
static struct cam_operation fmr97311 = {
 	.initialize = mr97311_init,
	.configure = mr97311_config,
	.start = mr97311_start,
	.stopN = mr97311_stopN,
	.stop0 = mr97311_stop0,
	.get_bright = mr97311_getbrightness,
	.set_bright = mr97311_setbrightness,
	.get_contrast = mr97311_getcontrast,
	.set_contrast = mr97311_setcontrast,
	.get_colors = mr97311_getcolors,
	.set_colors = mr97311_setcolors,
	.set_autobright = mr97311_setAutobright,
	.set_quality = mr97311_setquality,
	.cam_shutdown = mr97311_shutdown,
	.sof_detect = mr97311_sofdetect,
 };
static int pcam_reg_write(struct usb_device *dev,
			  __u16 index, unsigned char *value, int length);

static void MISensor_BulkWrite(struct usb_device *dev, unsigned short *pch,
			       char Address, int length, char controlbyte);

//MI Register table //elvis
enum {
    REG_HW_MI_0,
    REG_HW_MI_1,
    REG_HW_MI_2,
    REG_HW_MI_3,
    REG_HW_MI_4,
    REG_HW_MI_5,
    REG_HW_MI_6,
    REG_HW_MI_7,
    REG_HW_MI_9 = 0x09,
    REG_HW_MI_B = 0x0B,
    REG_HW_MI_C,
    REG_HW_MI_D,
    REG_HW_MI_1E = 0x1E,
    REG_HW_MI_20 = 0x20,
    REG_HW_MI_2B = 0x2B,
    REG_HW_MI_2C,
    REG_HW_MI_2D,
    REG_HW_MI_2E,
    REG_HW_MI_35 = 0x35,
    REG_HW_MI_5F = 0x5F,
    REG_HW_MI_60,
    REG_HW_MI_61,
    REG_HW_MI_62,
    REG_HW_MI_63,
    REG_HW_MI_64,
    REG_HW_MI_F1 = 0xF1,
    ATTR_TOTAL_MI_REG = 242
};
static void mr97311_stopN(struct usb_spca50x *pcam)
{
    int result;
    char data[2];
    memset(data, 0, 2);
    data[0] = 1;
    data[1] = 0;
    result = pcam_reg_write(pcam->dev, data[0], data, 2);
    if (result < 0)
	printk("Camera Stop failed \n");

}
static int pcam_reg_write(struct usb_device *dev,
			  __u16 index, unsigned char *value, int length)
{
    unsigned char buf[12];
    int rc;
    int i;
    unsigned char index_value = 0;

    memset(buf, 0, sizeof(buf));

    for (i = 0; i < length; i++)
	buf[i] = value[i];

    rc = usb_control_msg(dev,
			 usb_sndbulkpipe(dev, 4),
			 0x12,
			 0xc8, index_value, index, value, length, 5 * HZ);

    PDEBUG(1, "reg write: 0x%02X , result = 0x%x \n", index, rc);

    if (rc < 0) {
	PDEBUG(1, "reg write: error %d \n", rc);
    }
    return rc;
}

static void mr97311_start(struct usb_spca50x *pcam)
{
    int err_code;
    unsigned char data[242];
    unsigned short MI_buf[242];
    int h_size, v_size;
    int intpipe;
    //struct usb_device *dev = pcam->dev;
    memset(data, 0, 242);
    memset(MI_buf, 0, 242);

    PDEBUG(1,
	   "usb_set_interface in pcamCameraStart , interface %d , alt 8 \n",
	   pcam->iface);
    if (usb_set_interface(pcam->dev, pcam->iface, 8) < 0) {
	err("Set packet size: set interface error");
	return ;
    }

    data[0] = 0x01;		//address
    data[1] = 0x01;

    err_code = pcam_reg_write(pcam->dev, data[0], data, 0x02);
    if (err_code < 0) {
	printk("Register write failed \n");
	return ;
    }


    /*
       Initialize the MR97113 chip register
     */

    data[0] = 0x00;		//address
    data[1] = 0x0c | 0x01;	//reg 0
    data[2] = 0x01;		//reg 1

    switch (pcam->width) {
    case 1280:
	h_size = 1280;
	v_size = 1024;
	break;
    case 640:
	h_size = 640;
	v_size = 480;
	break;
    case 384:
	h_size = 384;
	v_size = 288;
	break;
    case 352:
	h_size = 352;
	v_size = 288;
	break;
    case 320:
	h_size = 320;
	v_size = 240;
	break;
    default:
	h_size = 352;
	v_size = 288;
	break;
    }
    data[3] = h_size / 8;	//h_size , reg 2
    data[4] = v_size / 8;	//v_size , reg 3
    data[5] = 0x30;		// reg 4, MI, PAS5101 : 0x30 for 24mhz , 0x28 for 12mhz
    data[6] = 4;		// reg 5, H start
    data[7] = 0xc0;		// reg 6, gamma 1.5
    data[8] = 3;		// reg 7, V start
    //if(pcam->width == 320 )
    //data[9]= 0x56;        // reg 8, 24MHz, 2:1 scale down
    //else
    data[9] = 0x52;		// reg 8, 24MHz, no scale down
    data[10] = 0x5d;		// reg 9, I2C device address [for PAS5101 (0x40)] [for MI (0x5d)]

    err_code = pcam_reg_write(pcam->dev, data[0], data, 0x0b);
    if (err_code < 0) {
	PDEBUG(1, "Register write failed \n");
	return ;
    }


    data[0] = 0x23;		//address
    data[1] = 0x09;		// reg 35, append frame header

    err_code = pcam_reg_write(pcam->dev, data[0], data, 0x02);
    if (err_code < 0) {
	PDEBUG(1, "Register write failed \n");
	return ;
    }



    data[0] = 0x3C;		//address
    if (pcam->width == 1280)
	data[1] = 200;		// reg 60, pc-cam frame size (unit: 4KB) 800KB
    else
	data[1] = 50;		// 50 reg 60, pc-cam frame size (unit: 4KB) 200KB
    err_code = pcam_reg_write(pcam->dev, data[0], data, 0x02);
    if (err_code < 0) {
	PDEBUG(1, "Register write failed \n");
	return ;
    }


    if (0) {			// fixed dark-gain
	data[1] = 0;		// reg 94, Y Gain (1.75)
	data[2] = 0;		// reg 95, UV Gain (1.75)
	data[3] = 0x3f;		// reg 96, Y Gain/UV Gain/disable auto dark-gain
	data[4] = 0;		// reg 97, set fixed dark level
	data[5] = 0;		// reg 98, don't care
    } else {			// auto dark-gain
	data[1] = 0;		// reg 94, Y Gain (auto)
	data[2] = 0;		// reg 95, UV Gain (1.75)
	data[3] = 0x78;		// reg 96, Y Gain/UV Gain/disable auto dark-gain
	switch (pcam->width) {
	case 1280:
	    data[4] = 154;	// reg 97, %3 shadow point (unit: 256 pixel)
	    data[5] = 51;	// reg 98, %1 highlight point (uint: 256 pixel)
	    break;
	case 640:
	    data[4] = 36;	// reg 97, %3 shadow point (unit: 256 pixel)
	    data[5] = 12;	// reg 98, %1 highlight point (uint: 256 pixel)
	    break;
	case 320:
	    data[4] = 9;	// reg 97, %3 shadow point (unit: 256 pixel)
	    data[5] = 3;	// reg 98, %1 highlight point (uint: 256 pixel)
	    break;
	}
    }
    // auto dark-gain
    data[0] = 0x5E;		// address

    err_code = pcam_reg_write(pcam->dev, data[0], data, 0x06);
    if (err_code < 0) {
	PDEBUG(1, "Register write failed \n");
	return ;
    }



    data[0] = 0x67;
    data[1] = 0x13;		// reg 103, first pixel B, disable sharpness
    err_code = pcam_reg_write(pcam->dev, data[0], data, 0x02);
    if (err_code < 0) {
	PDEBUG(1, "Register write failed \n");
	return ;
    }


    /*
       initialize the value of MI sensor...
     */

    MI_buf[REG_HW_MI_1] = 0x000a;
    MI_buf[REG_HW_MI_2] = 0x000c;
    MI_buf[REG_HW_MI_3] = 0x0405;
    MI_buf[REG_HW_MI_4] = 0x0507;
    //mi_Attr_Reg_[REG_HW_MI_5]     = 0x01ff;//13
    MI_buf[REG_HW_MI_5] = 0x0013;	//13
    MI_buf[REG_HW_MI_6] = 0x001f;	// vertical blanking
    //mi_Attr_Reg_[REG_HW_MI_6]     = 0x0400;  // vertical blanking
    MI_buf[REG_HW_MI_7] = 0x0002;
    //mi_Attr_Reg_[REG_HW_MI_9]     = 0x015f;
    //mi_Attr_Reg_[REG_HW_MI_9]     = 0x030f;
    MI_buf[REG_HW_MI_9] = 0x0374;
    MI_buf[REG_HW_MI_B] = 0x0000;
    MI_buf[REG_HW_MI_C] = 0x0000;
    MI_buf[REG_HW_MI_D] = 0x0000;
    MI_buf[REG_HW_MI_1E] = 0x8000;
//      mi_Attr_Reg_[REG_HW_MI_20]      = 0x1104;
    MI_buf[REG_HW_MI_20] = 0x1104;	//0x111c;
    MI_buf[REG_HW_MI_2B] = 0x0008;
//      mi_Attr_Reg_[REG_HW_MI_2C]      = 0x000f;
    MI_buf[REG_HW_MI_2C] = 0x001f;	//lita suggest
    MI_buf[REG_HW_MI_2D] = 0x0008;
    MI_buf[REG_HW_MI_2E] = 0x0008;
    MI_buf[REG_HW_MI_35] = 0x0051;
    MI_buf[REG_HW_MI_5F] = 0x0904;	//fail to write
    MI_buf[REG_HW_MI_60] = 0x0000;
    MI_buf[REG_HW_MI_61] = 0x0000;
    MI_buf[REG_HW_MI_62] = 0x0498;
    MI_buf[REG_HW_MI_63] = 0x0000;
    MI_buf[REG_HW_MI_64] = 0x0000;
    MI_buf[REG_HW_MI_F1] = 0x0001;
    //changing while setting up the different value of dx/dy

    if (pcam->width != 1280) {
	MI_buf[0x01] = 0x010a;
	MI_buf[0x02] = 0x014c;
	MI_buf[0x03] = 0x01e5;
	MI_buf[0x04] = 0x0287;
    }
    MI_buf[0x20] = 0x1104;

    MISensor_BulkWrite(pcam->dev, MI_buf + 1, 1, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 2, 2, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 3, 3, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 4, 4, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 5, 5, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 6, 6, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 7, 7, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 9, 9, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x0B, 0x0B, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x0C, 0x0C, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x0D, 0x0D, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x1E, 0x1E, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x20, 0x20, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x2B, 0x2B, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x2C, 0x2C, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x2D, 0x2D, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x2E, 0x2E, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x35, 0x35, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x5F, 0x5F, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x60, 0x60, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x61, 0x61, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x62, 0x62, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x63, 0x63, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0x64, 0x64, 1, 0);


    MISensor_BulkWrite(pcam->dev, MI_buf + 0xF1, 0xF1, 1, 0);



    intpipe = usb_sndintpipe(pcam->dev, 0);
    err_code = usb_clear_halt(pcam->dev, intpipe);

    data[0] = 0x00;
    data[1] = 0x4D;		// ISOC transfering enable...
    err_code = pcam_reg_write(pcam->dev, data[0], data, 0x02);
    if (err_code < 0) {
	PDEBUG(1, "Register write failed \n");
	return ;
    }


    return ;
}
static void MISensor_BulkWrite(struct usb_device *dev, unsigned short *pch,
			       char Address, int length, char controlbyte)
{
    int dest, src, result;
    unsigned char data[6];

    memset(data, 0, 6);

    for (dest = 3, src = 0; src < length; src++) {
	data[0] = 0x1f;
	data[1] = controlbyte;
	data[2] = Address + src;
	data[dest] = pch[src] >> 8;	//high byte;
	data[dest + 1] = pch[src];	//low byte;
	data[dest + 2] = 0;

	result = usb_control_msg(dev,
				 usb_sndbulkpipe(dev, 4),
				 0x12, 0xc8, 0, Address, data, 5, 5 * HZ);

	PDEBUG(1, "reg write: 0x%02X , result = 0x%x \n", Address, result);

	if (result < 0) {
	    printk("reg write: error %d \n", result);
	}

    }

}
static int mr97311_config(struct usb_spca50x *spca50x)
{
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
    spca50x->qindex = 1;	// set quantization table
    return 0;
}
static int mr97311_sofdetect(struct usb_spca50x *spca50x,struct spca50x_frame *frame, unsigned char *cdata,int *iPix, int seqnum, int *datalength)
{
	int sof = 0;
	int p;
		
		if (*datalength < 6)
		    return -1;
		else {
		    for (p = 0; p < *datalength - 6; p++) {
			if ((cdata[0 + p] == 0xFF)
			    && (cdata[1 + p] == 0xFF)
			    && (cdata[2 + p] == 0x00)
			    && (cdata[3 + p] == 0xFF)
			    && (cdata[4 + p] == 0x96)
			    ) {
			    if ((cdata[5 + p] == 0x64)
				|| (cdata[5 + p] == 0x65)
				|| (cdata[5 + p] == 0x66)
				|| (cdata[5 + p] == 0x67)) {
				sof = 1;
				break;
			    }
			}
		    }

		    if (sof) {
			*iPix = p + 16;
			*datalength -= *iPix;
			PDEBUG(5,
			       "Pcam header packet found, %d datalength %d !",
			       p, *datalength );
			       return 0;
		    } else {
			*iPix = 0;
			return (seqnum+1);
		    }

		}
}
