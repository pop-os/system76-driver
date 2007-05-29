/*
* SPCA5xx based usb camera driver (currently supports
* yuv native stream spca501a, spca501c, spca505, spca508, spca506
* jpeg native stream spca500, spca551, spca504a, spca504b, spca533a, spca536a, zc0301, zc0302, cx11646, sn9c102p
* bayer native stream spca561a, sn9c101, sn9c102, tv8532 ).
* Z-star Vimicro chips zc0301 zc0301P zc0302
* Sunplus spca501a, spca501c, spca505, spca508, spca506, spca500, spca551, spca504a, spca504b, spca533a, spca536a
* Sonix sn9c101, sn9c102, sn9c102p sn9c105 sn9c120
* Conexant cx11646
* Transvision tv_8532 
* Etoms Et61x151 Et61x251
* Pixart Pac207-BCA-32
* SPCA5xx version by Michel Xhaard <mxhaard@users.sourceforge.net>
* Based on :
* SPCA50x version by Joel Crisp <cydergoth@users.sourceforge.net>
* OmniVision OV511 Camera-to-USB Bridge Driver
* Copyright (c) 1999-2000 Mark W. McClelland
* Kernel 2.6.x port Michel Xhaard && Reza Jelveh (feb 2004)
* Based on the Linux CPiA driver written by Peter Pregler,
* Scott J. Bertin and Johannes Erdfelt.
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License as published by the
* Free Software Foundation; either version 2 of the License, or (at your
* option) any later version.
*
* This program is distributed in the hope that it will be useful, but
* WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
* or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
* for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software Foundation,
* Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
*/
static const char version[] = GSPCA_VERSION;
#ifndef AUTOCONF_INCLUDED
#include <linux/config.h>
#endif
#include <linux/module.h>
#include <linux/version.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/vmalloc.h>
#include <linux/sched.h>
#include <linux/slab.h>
#include <linux/mm.h>
#include <linux/string.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/ctype.h>
#include <linux/pagemap.h>
#include <linux/usb.h>
#include <asm/io.h>
#include <asm/semaphore.h>
#include <asm/page.h>
#include <asm/uaccess.h>
#include <asm/atomic.h>
/* only on 2.6.x */
#include <linux/jiffies.h>
#include <linux/param.h>
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2, 6, 9)
#include <linux/moduleparam.h>
#endif
#include "gspca.h"
#include "decoder/gspcadecoder.h"
/* Video Size 640 x 480 x 4 bytes for RGB */
#define MAX_FRAME_SIZE (640 * 480 * 4)
#define MAX_DATA_SIZE (MAX_FRAME_SIZE + sizeof(struct timeval))
/* Hardware auto exposure / whiteness (PC-CAM 600) */
static int autoexpo = 1;
/* Video device number (-1 is first available) */
static int video_nr = -1;
/* 0=no debug messages
* 1=init/detection/unload and other significant messages,
* 2=some warning messages
* 3=config/control function calls
* 4=most function calls and data parsing messages
* 5=highly repetitive mesgs
* NOTE: This should be changed to 0, 1, or 2 for production kernels
*/
static int debug = 0;
/* Force image to be read in RGB instead of BGR. This option allow
* programs that expect RGB data (e.g. gqcam) to work with this driver. */
static int force_rgb = 0;
static int gamma = 3;
static int OffRed = 0;
static int OffBlue = 0;
static int OffGreen = 0;
static int GRed = 256;
static int GBlue = 256;
static int GGreen = 256;
static int usbgrabber = 0;
#ifdef GSPCA_ENABLE_COMPRESSION
/* Enable compression. This is for experimentation only; compressed images
* still cannot be decoded yet. */
static int compress = 0;
#endif
/* Light frequency banding filter 50HZ/60HZ/NoFliker */
static int lightfreq = 50;
#ifdef GSPCA_ENABLE_REGISTERPLAY
static int RegAddress = 0;
static int RegValue = 0;
static int RegStrobe = 0;
#endif
module_param(autoexpo, int, 0644);
module_param(debug, int, 0644);
module_param(force_rgb, int, 0644);
module_param(gamma, int, 0644);
module_param(OffRed, int, 0644);
module_param(OffBlue, int, 0644);
module_param(OffGreen, int, 0644);
module_param(GRed, int, 0644);
module_param(GBlue, int, 0644);
module_param(GGreen, int, 0644);
#ifdef GSPCA_ENABLE_COMPRESSION
module_param(compress, int, 0644);
#endif
module_param(usbgrabber, int, 0444);
module_param(lightfreq, int, 0644);
#ifdef GSPCA_ENABLE_REGISTERPLAY
module_param(RegAddress, int, 0644);
module_param(RegValue, int, 0644);
module_param(RegStrobe, int, 0644);
#endif
MODULE_PARM_DESC(autoexpo,
		 "Enable/Disable auto exposure (default=1: enabled) (PC-CAM 600/Zc03xx/spca561a/Etoms Only !!!)");
MODULE_PARM_DESC(debug,
		 "Debug level: 0=none, 1=init/detection, 2=warning, 3=config/control, 4=function call, 5=max");
MODULE_PARM_DESC(force_rgb, "Read RGB instead of BGR");
MODULE_PARM_DESC(gamma, "gamma setting range 0 to 7 3-> gamma=1");
MODULE_PARM_DESC(OffRed, "OffRed setting range -128 to 128");
MODULE_PARM_DESC(OffBlue, "OffBlue setting range -128 to 128");
MODULE_PARM_DESC(OffGreen, "OffGreen setting range -128 to 128");
MODULE_PARM_DESC(GRed, "Gain Red setting range 0 to 512 /256 ");
MODULE_PARM_DESC(GBlue, "Gain Blue setting range 0 to 512 /256 ");
MODULE_PARM_DESC(GGreen, "Gain Green setting range 0 to 512 /256 ");
#ifdef GSPCA_ENABLE_COMPRESSION
MODULE_PARM_DESC(compress, "Turn on/off compression (not functional yet)");
#endif				/* SPCA50X_ENABLE_COMPRESSION */
MODULE_PARM_DESC(usbgrabber, "Is a usb grabber 0x0733:0x0430 ? (default 1) ");
MODULE_PARM_DESC(lightfreq,  "Light frequency banding filter. Set to 50 or 60 Hz, or zero to NoFliker (default=50)");
#ifdef GSPCA_ENABLE_REGISTERPLAY
MODULE_PARM_DESC(RegAddress, "Register Address of PAC207");
MODULE_PARM_DESC(RegValue, "Register Value for PAC207");
MODULE_PARM_DESC(RegStrobe,
		 "Strobe to read or write a register 1=write, 2=read");
#endif				/* SPCA5XX_ENABLE_REGISTERPLAY */
/****************/
MODULE_AUTHOR
    ("Michel Xhaard <mxhaard@users.sourceforge.net> based on spca50x driver by Joel Crisp <cydergoth@users.sourceforge.net>,ov511 driver by Mark McClelland <mwm@i.am>");
MODULE_DESCRIPTION("GSPCA/SPCA5XX USB Camera Driver");
MODULE_LICENSE("GPL");

#if LINUX_VERSION_CODE < KERNEL_VERSION(2,6,19)
static void
spca50x_isoc_irq(struct urb *urb, struct pt_regs *regs);
#else
static void
spca50x_isoc_irq(struct urb *urb);
#endif

static int spca50x_move_data(struct usb_spca50x *spca50x, struct urb *urb);
static int spca5xx_set_light_freq(struct usb_spca50x *spca50x, int freq);

static struct usb_driver spca5xx_driver;
#ifndef max
static inline int
max(int a, int b)
{
	return (a > b) ? a : b;
}
#endif				/* max */
/**********************************************************************
* List of known SPCA50X-based cameras
**********************************************************************/
/* Camera type jpeg yuvy yyuv yuyv grey gbrg*/
static struct palette_list Plist[] = {
	{JPEG, "JPEG"},
	{JPGH, "JPEG"},
	{JPGC, "JPEG"},
	{JPGS, "JPEG"},
	{JPGM, "JPEG"},
	{YUVY, "YUVY"},
	{YYUV, "YYUV"},
	{YUYV, "YUYV"},
	{GREY, "GREY"},
	{GBRG, "GBRG"},
	{SN9C, "SN9C"},
	{GBGR, "GBGR"},
	{S561, "S561"},
	{PGBRG, "GBRG"},
	{YUY2, "YUYV"},
	{-1, NULL}
};
static struct bridge_list Blist[] = {
	{BRIDGE_SPCA505, "SPCA505"},
	{BRIDGE_SPCA506, "SPCA506"},
	{BRIDGE_SPCA501, "SPCA501"},
	{BRIDGE_SPCA508, "SPCA508"},
	{BRIDGE_SPCA504, "SPCA504"},
	{BRIDGE_SPCA500, "SPCA500"},
	{BRIDGE_SPCA504B, "SPCA504B"},
	{BRIDGE_SPCA533, "SPCA533"},
	{BRIDGE_SPCA504C, "SPCA504C"},
	{BRIDGE_SPCA561, "SPCA561"},
	{BRIDGE_SPCA536, "SPCA536"},
	{BRIDGE_SONIX, "SN9C102"},
	{BRIDGE_ZC3XX, "ZC301-2"},
	{BRIDGE_CX11646, "CX11646"},
	{BRIDGE_TV8532, "TV8532"},
	{BRIDGE_ETOMS, "ET61XX51"},
	{BRIDGE_SN9CXXX, "SN9CXXX"},
	{BRIDGE_MR97311, "MR97311"},
	{BRIDGE_PAC207, "PAC207BCA"},
	{BRIDGE_VC032X, "VC0321"},
	{-1, NULL}
};
/* Light frequency banding filter 50HZ/60HZ/NoFliker */
enum { 
       freq_50HZ=0,
       freq_60HZ,
       NoFliker
};
enum {
	UnknownCamera = 0,	// 0
	IntelPCCameraPro,
	IntelCreateAndShare,
	GrandtecVcap,
	ViewQuestM318B,
	ViewQuestVQ110,
	KodakDVC325,
	MustekGsmartMini2,
	MustekGsmartMini3,
	CreativePCCam300,
	DLinkDSC350,		// 10
	CreativePCCam600,
	IntelPocketPCCamera,
	IntelEasyPCCamera,
	ThreeComHomeConnectLite,
	KodakEZ200,
	MaxellMaxPocket,
	AiptekMiniPenCam2,
	AiptekPocketDVII,
	AiptekPenCamSD,
	AiptekMiniPenCam13,	// 20
	MustekGsmartLCD3,
	MustekMDC5500Z,
	MegapixV4,
	AiptekPocketDV,
	HamaUSBSightcam,
	Arowana300KCMOSCamera,
	MystFromOriUnknownCamera,
	AiptekPocketDV3100,
	AiptekPocketCam3M,
	GeniusVideoCAMExpressV2,	// 30
	Flexcam100Camera,
	MustekGsmartLCD2,
	PureDigitalDakota,
	PetCam,
	BenqDC1500,
	LogitechClickSmart420,
	LogitechClickSmart510,
	BenqDC1300,
	HamaUSBSightcam2,
	MustekDV3000,		// 40
	CreativePccam750,
	MaxellCompactPM3,
	BenqDC3410,
	BenqDC1016,
	MicroInnovationIC200,
	LogitechTraveler,
	Flycam100Camera,
	UsbGrabberPV321c,
	ADSInstantVCD,
	Gsmartmini,		// 50
	Jenoptikjdc21lcd,
	LogitechClickSmart310,
	Terratec2move13,
	MustekDV4000,
	AiptekDV3500,
	LogitechClickSmart820,
	Enigma13,
	Sonix6025,
	Epsilon13,
	Nxultra,		//60
	AiptekPocketCam2M,
	DeMonUSBCapture,
	CreativeVista,
	PolaroidPDC2030,
	CreativeNotebook,
	CreativeMobile,
	LabtecPro,
	MustekWcam300A,
	GeniusVideoCamV2,
	GeniusVideoCamV3,
	GeniusVideoCamExpressV2b,
	CreativeNxPro,
	Sonix6029,		//73 74 75
	Vimicro,
	Digitrex2110,
	GsmartD30,
	CreativeNxPro2,
	Bs888e,
	Zc302,
	CreativeNoteBook2,
	AiptekSlim3200,		/* 83 84 85 */
	LabtecWebcam,
	QCExpress,
	ICM532cam,
	MustekGsmart300,
	CreativeLive,		//90
	MercuryDigital,
	Wcam300A,
	CreativeVista3b,
	VeoStingray1,
	VeoStingray2,
	TyphoonWebshotIIUSB300k,	//96
	PolaroidPDC3070,
	QCExpressEtch2,
	QCforNotebook,
	QCim,			//100
	WebCam320,
	AiptekPocketCam4M,
	AiptekPocketDV5100,
	AiptekPocketDV5300,
	SunplusGeneric536,
	QCimA1,
	QCchat,
	QCimB9,
	Labtec929,		//109 110
	Etoms61x151,
	Etoms61x251,
	PalmPixDC85,
	Optimedia,
	ToptroIndus,
	AgfaCl20,
	LogitechQC92x,
	SonixWC311P,
	Concord3045,
	Mercury21,		//120
	CreativeNX,
	CreativeInstant1,
	CreativeInstant2,
	QuickCamNB,
	WCam300AN,
	LabtecWCPlus,
	GeniusVideoCamMessenger,
	Pcam,
	GeniusDsc13,
	MustekMDC4000,		//130
	LogitechQCCommunicateSTX,
	Lic200,
	SweexTas5110,
	Pccam168,
	Sn535,
	Pccam,
	Lic300,
	PolaroidIon80,
	Zc0305b,
	BtcPc380,		//140
	LogitechNotebookDeluxe,
	LabtecNotebook,
	JvcGcA50,
	SmileIntlCamera,
	PcCam350,
	PAC207,
	QtecWb100,
	GeniusGe111,
	Vimicro303b,
	CyberpixS550V,
	GeniusGF112,
	LogitechQCim,
	AiptekSlim3000F,
	CTXM730VCam,
	GeniusVideoCamNB,
	CreativeVistaPlus,
	PhilipsSPC200NC,
	PhilipsSPC700NC,
	SpeedNVC350K,
	Mustek330K,
	PhilipsSPC600NC,
	PhilipsSPC300NC,
	Sonix6019,
	LogitechQCImage,
	Sunplus500c,
	MustekMDC3500,
	LogitechQCCool,
	QCimconnect,
	QCmessenger,
	CreativeLiveCamNotebookPro,
	CreativeWebCamVistaPro,
	CreativeLiveCamVideoIM,
	AiptekDV4100M,
	TyphoonEasyCam1_3,
	Sonix0x613b,
	Sonix0x60fb,
	Sonyc002,
	Vimicro0321,
	Orbicam,	
	LastCamera
};
static struct cam_list clist[] = {
	{UnknownCamera, "Unknown"},
	{IntelPCCameraPro, "Intel PC Camera Pro"},
	{IntelCreateAndShare, "Intel Create and Share"},
	{GrandtecVcap, "Grandtec V.cap"},
	{ViewQuestM318B, "ViewQuest M318B"},
	{ViewQuestVQ110, "ViewQuest VQ110"},
	{KodakDVC325, "Kodak DVC-325"},
	{MustekGsmartMini2, "Mustek gSmart mini 2"},
	{MustekGsmartMini3, "Mustek gSmart mini 3"},
	{CreativePCCam300, "Creative PC-CAM 300"},
	{DLinkDSC350, "D-Link DSC-350"},
	{CreativePCCam600, "Creative PC-CAM 600"},
	{IntelPocketPCCamera, "Intel Pocket PC Camera"},
	{IntelEasyPCCamera, "Intel Easy PC Camera"},
	{ThreeComHomeConnectLite, "3Com Home Connect Lite"},
	{KodakEZ200, "Kodak EZ200"},
	{MaxellMaxPocket, "Maxell Max Pocket LEdit. 1.3 MPixels"},
	{AiptekMiniPenCam2, "Aiptek Mini PenCam  2 MPixels"},
	{AiptekPocketDVII, "Aiptek PocketDVII  1.3 MPixels"},
	{AiptekPenCamSD, "Aiptek Pencam SD  2 MPixels"},
	{AiptekMiniPenCam13, "Aiptek mini PenCam 1.3 MPixels"},
	{MustekGsmartLCD3, "Mustek Gsmart LCD 3"},
	{MustekMDC5500Z, "Mustek MDC5500Z"},
	{MegapixV4, "Megapix V4"},
	{AiptekPocketDV, "Aiptek PocketDV "},
	{HamaUSBSightcam, "Hama USB Sightcam 100"},
	{Arowana300KCMOSCamera, "Arowana 300K CMOS Camera"},
	{MystFromOriUnknownCamera, "Unknow Ori Camera"},
	{AiptekPocketDV3100, "Aiptek PocketDV3100+ "},
	{AiptekPocketCam3M, "Aiptek PocketCam  3 M "},
	{GeniusVideoCAMExpressV2, "Genius VideoCAM Express V2"},
	{Flexcam100Camera, "Flexcam 100 Camera"},
	{MustekGsmartLCD2, "Mustek Gsmart LCD 2"},
	{PureDigitalDakota, "Pure Digital Dakota"},
	{PetCam, "PetCam"},
	{BenqDC1500, "Benq DC1500"},
	{LogitechClickSmart420, "Logitech Inc. ClickSmart 420"},
	{LogitechClickSmart510, "Logitech Inc. ClickSmart 510"},
	{BenqDC1300, "Benq DC1300"},
	{HamaUSBSightcam2, "Hama USB Sightcam 100 (2)"},
	{MustekDV3000, "Mustek DV 3000"},
	{CreativePccam750, "Creative PCcam750"},
	{MaxellCompactPM3, "Maxell Compact PC PM3"},
	{BenqDC3410, "Benq DC3410"},
	{BenqDC1016, "Benq DC1016"},
	{MicroInnovationIC200, "Micro Innovation IC200"},
	{LogitechTraveler, "Logitech QuickCam Traveler"},
	{Flycam100Camera, "FlyCam Usb 100"},
	{UsbGrabberPV321c, "Usb Grabber PV321c"},
	{ADSInstantVCD, "ADS Instant VCD"},
	{Gsmartmini, "Mustek Gsmart Mini"},
	{Jenoptikjdc21lcd, "Jenoptik DC 21 LCD"},
	{LogitechClickSmart310, "Logitech ClickSmart 310"},
	{Terratec2move13, "Terratec 2 move 1.3"},
	{MustekDV4000, "Mustek DV4000 Mpeg4"},
	{AiptekDV3500, "Aiptek DV3500 Mpeg4"},
	{LogitechClickSmart820, "Logitech ClickSmart 820"},
	{Enigma13, "Digital Dream Enigma 1.3"},
	{Sonix6025, "Xcam Shanga"},
	{Epsilon13, "Digital Dream Epsilon 1.3"},
	{Nxultra, "Creative Webcam NX ULTRA"},
	{AiptekPocketCam2M, "Aiptek PocketCam 2Mega"},
	{DeMonUSBCapture, "3DeMON USB Capture"},
	{CreativeVista, "Creative Webcam Vista"},
	{PolaroidPDC2030, "Polaroid PDC2030"},
	{CreativeNotebook, "Creative Notebook PD1171"},
	{CreativeMobile, "Creative Mobile PD1090"},
	{LabtecPro, "Labtec Webcam Pro"},
	{MustekWcam300A, "Mustek Wcam300A"},
	{GeniusVideoCamV2, "Genius Videocam V2"},
	{GeniusVideoCamV3, "Genius Videocam V3"},
	{GeniusVideoCamExpressV2b, "Genius Videocam Express V2 Firmware 2"},
	{CreativeNxPro, "Creative Nx Pro"},
	{Sonix6029, "Sonix sn9c10x + Pas106 sensor"},
	{Vimicro, "Z-star Vimicro zc0301p"},
	{Digitrex2110, "ApexDigital Digitrex2110 spca533"},
	{GsmartD30, "Mustek Gsmart D30 spca533"},
	{CreativeNxPro2, "Creative NX Pro FW2"},
	{Bs888e, "Kowa Bs888e MicroCamera"},
	{Zc302, "Z-star Vimicro zc0302"},
	{CreativeNoteBook2, "Creative Notebook PD1170"},
	{AiptekSlim3200, "Aiptek Slim 3200"},
	{LabtecWebcam, "Labtec Webcam"},
	{QCExpress, "QC Express"},
	{ICM532cam, "ICM532 cam"},
	{MustekGsmart300, "Mustek Gsmart 300"},
	{CreativeLive, "Creative Live! "},
	{MercuryDigital, "Mercury Digital Pro 3.1Mp"},
	{Wcam300A, "Mustek Wcamm300A 2"},
	{CreativeVista3b, "Creative Webcam Vista 0x403b"},
	{VeoStingray1, "Veo Stingray 1"},
	{VeoStingray2, "Veo Stingray 2"},
	{TyphoonWebshotIIUSB300k, " Typhoon Webshot II"},
	{PolaroidPDC3070, " Polaroid PDC3070"},
	{QCExpressEtch2, "Logitech QuickCam Express II"},
	{QCforNotebook, "Logitech QuickCam for Notebook"},
	{QCim, "Logitech QuickCam IM"},
	{WebCam320, "Micro Innovation WebCam 320"},
	{AiptekPocketCam4M, "Aiptek Pocket Cam 4M"},
	{AiptekPocketDV5100, "Aiptek Pocket DV5100"},
	{AiptekPocketDV5300, "Aiptek Pocket DV5300"},
	{SunplusGeneric536, "Sunplus Generic spca536a"},
	{QCimA1, "Logitech QuickCam IM + sound"},
	{QCchat, "Logitech QuickCam chat"},
	{QCimB9, "Logitech QuickCam IM ???"},
	{Labtec929, "Labtec Webcam Elch2 "},
	{Etoms61x151, "QCam Sangha"},
	{Etoms61x251, "QCam xxxxxx"},
	{PalmPixDC85, "PalmPix DC85"},
	{Optimedia, "Optimedia TechnoAME"},
	{ToptroIndus, "Toptro Industrial"},
	{AgfaCl20, "Agfa ephoto CL20"},
	{LogitechQC92x, "Logitech QuickCam EC"},
	{SonixWC311P, "Sonix sn9c102P Hv7131R"},
	{Concord3045, "Concord 3045 spca536a"},
	{Mercury21, "Mercury Peripherals Inc."},
	{CreativeNX, "Creative NX"},
	{CreativeInstant1, "Creative Instant P0620"},
	{CreativeInstant2, "Creative Instant P0620D"},
	{QuickCamNB, "Logitech QuickCam for Notebooks"},
	{WCam300AN, "Mustek WCam300AN "},
	{LabtecWCPlus, "Labtec Webcam Plus"},
	{GeniusVideoCamMessenger, "VideoCam Messenger sn9c101 Ov7630"},
	{Pcam, "Mars-Semi Pc-Camera MR97311 MI0360"},
	{GeniusDsc13, "Genius Dsc 1.3 Smart spca504B-P3"},
	{MustekMDC4000, "Mustek MDC4000"},
	{LogitechQCCommunicateSTX, "Logitech QuickCam Communicate STX"},
	{Lic200, "LG LIC-200"},
	{SweexTas5110, "Sweex SIF webcam"},
	{Pccam168, "Sonix PcCam"},
	{Sn535, "Sangha 350k"},
	{Pccam, "Sonix Pccam +"},
	{Lic300, "LG Lic-300"},
	{PolaroidIon80, "Polaroid Ion 80"},
	{Zc0305b, "Generic Zc0305b"},
	{BtcPc380, "Sonix Btc PC380"},
	{LogitechNotebookDeluxe, "Logitech Notebook Deluxe"},
	{LabtecNotebook, "Labtec Webcam Notebook"},
	{JvcGcA50, "JVC GC-A50"},
	{SmileIntlCamera, "Smile International"},
	{PcCam350, "PC-Cam350"},
	{PAC207, "Pixart PAC207-BCA"},
	{QtecWb100, "Qtec Webcam 100"},
	{GeniusGe111, "Genius VideoCam Ge111"},
	{Vimicro303b, "Generic Vimicro 303b"},
	{CyberpixS550V, "Mercury Cyberpix S550V"},
	{GeniusGF112, "Genius GF112"},
	{LogitechQCim, "Logitech QCIM"},
	{AiptekSlim3000F, "Aiptek Slim3000F"},
	{CTXM730VCam, "CTX M730V built in Cam"},
	{GeniusVideoCamNB, "Genius VideoCAM NB"},
	{CreativeVistaPlus, "Creative Webcam Vista Plus"},
	{PhilipsSPC200NC, "Philips SPC200NC "},
	{PhilipsSPC700NC, "Philips SPC700NC "},
	{SpeedNVC350K, "Speed NVC 350K "},
	{Mustek330K, "Mustek Digicam 330K "},
	{PhilipsSPC600NC, "Philips SPC600NC "},
	{PhilipsSPC300NC, "Philips SPC300NC "},
	{Sonix6019, "Sonix VGA Ov7630 "},
	{LogitechQCImage, "Logitech QuickCam Image "},
	{Sunplus500c, "Sunplus CA500C "},
	{MustekMDC3500, "Mustek MDC3500"},
	{LogitechQCCool, "Logitech QuickCam Cool"},
	{QCimconnect, "Logitech QuickCam IM/Connect "},
	{QCmessenger, "Logitech QuickCam Messenger "},
	{CreativeLiveCamNotebookPro, "Creative Live!Cam Notebook Pro (VF0250)"},
	{CreativeWebCamVistaPro, "Creative WebCam Vista Pro"},
	{CreativeLiveCamVideoIM, "Creative Live Cam Video IM"},
	{AiptekDV4100M, "Aiptek DV4100M"},
	{TyphoonEasyCam1_3, "Typhoon Easy Cam 1.3 MPix"},
	{Sonix0x613b, "Surfer model sn-206"},
	{Sonix0x60fb, "Surfer model noname"},
	{Sonyc002,"Vc0321"},
	{Vimicro0321,"Vc0321"},
	{Orbicam,"Logitech Orbicam"},
	{-1, NULL}
};
static __devinitdata struct usb_device_id device_table[] = {
	{USB_DEVICE(0x0733, 0x0430)},	/* Intel PC Camera Pro */
	{USB_DEVICE(0x0733, 0x0401)},	/* Intel Create and Share */
	{USB_DEVICE(0x99FA, 0x8988)},	/* Grandtec V.cap */
	{USB_DEVICE(0x0733, 0x0402)},	/* ViewQuest M318B */
	{USB_DEVICE(0x0733, 0x0110)},	/* ViewQuest VQ110 */
	{USB_DEVICE(0x040A, 0x0002)},	/* Kodak DVC-325 */
	{USB_DEVICE(0x055f, 0xc420)},	/* Mustek gSmart Mini 2 */
	{USB_DEVICE(0x055f, 0xc520)},	/* Mustek gSmart Mini 3 */
	{USB_DEVICE(0x041E, 0x400A)},	/* Creative PC-CAM 300 */
	{USB_DEVICE(0x084D, 0x0003)},	/* D-Link DSC-350 */
	{USB_DEVICE(0x041E, 0x400B)},	/* Creative PC-CAM 600 */
	{USB_DEVICE(0x8086, 0x0630)},	/* Intel Pocket PC Camera */
	{USB_DEVICE(0x8086, 0x0110)},	/* Intel Easy PC Camera */
	{USB_DEVICE(0x0506, 0x00df)},	/* 3Com HomeConnect Lite */
	{USB_DEVICE(0x040a, 0x0300)},	/* Kodak EZ200 */
	{USB_DEVICE(0x04fc, 0x504b)},	/* Maxell MaxPocket LE 1.3 */
	{USB_DEVICE(0x08ca, 0x2008)},	/* Aiptek Mini PenCam 2 M */
	{USB_DEVICE(0x08ca, 0x0104)},	/* Aiptek PocketDVII 1.3 */
	{USB_DEVICE(0x08ca, 0x2018)},	/* Aiptek Pencam SD 2M */
	{USB_DEVICE(0x04fc, 0x504a)},	/* Aiptek Mini PenCam 1.3 */
	{USB_DEVICE(0x055f, 0xc530)},	/* Mustek Gsmart LCD 3 */
	{USB_DEVICE(0x055f, 0xc650)},	/* Mustek MDC5500Z */
	{USB_DEVICE(0x052b, 0x1513)},	/* Megapix V4 */
	{USB_DEVICE(0x08ca, 0x0103)},	/* Aiptek PocketDV */
	{USB_DEVICE(0x0af9, 0x0010)},	/* Hama USB Sightcam 100 */
	{USB_DEVICE(0x1776, 0x501c)},	/* Arowana 300K CMOS Camera */
	{USB_DEVICE(0x08ca, 0x0106)},	/* Aiptek Pocket DV3100+ */
	{USB_DEVICE(0x08ca, 0x2010)},	/* Aiptek PocketCam 3M */
	{USB_DEVICE(0x0458, 0x7004)},	/* Genius VideoCAM Express V2 */
	{USB_DEVICE(0x04fc, 0x0561)},	/* Flexcam 100 */
	{USB_DEVICE(0x055f, 0xc430)},	/* Mustek Gsmart LCD 2 */
	{USB_DEVICE(0x04fc, 0xffff)},	/* Pure DigitalDakota */
	{USB_DEVICE(0xabcd, 0xcdee)},	/* Petcam */
	{USB_DEVICE(0x04a5, 0x3008)},	/* Benq DC 1500 */
	{USB_DEVICE(0x046d, 0x0960)},	/* Logitech Inc. ClickSmart 420 */
	{USB_DEVICE(0x046d, 0x0901)},	/* Logitech Inc. ClickSmart 510 */
	{USB_DEVICE(0x04a5, 0x3003)},	/* Benq DC 1300 */
	{USB_DEVICE(0x0af9, 0x0011)},	/* Hama USB Sightcam 100 */
	{USB_DEVICE(0x055f, 0xc440)},	/* Mustek DV 3000 */
	{USB_DEVICE(0x041e, 0x4013)},	/* Creative Pccam750 */
	{USB_DEVICE(0x060b, 0xa001)},	/* Maxell Compact Pc PM3 */
	{USB_DEVICE(0x04a5, 0x300a)},	/* Benq DC3410 */
	{USB_DEVICE(0x04a5, 0x300c)},	/* Benq DC1016 */
	{USB_DEVICE(0x0461, 0x0815)},	/* Micro Innovation IC200 */
	{USB_DEVICE(0x046d, 0x0890)},	/* Logitech QuickCam traveler */
	{USB_DEVICE(0x10fd, 0x7e50)},	/* FlyCam Usb 100 */
	{USB_DEVICE(0x06e1, 0xa190)},	/* ADS Instant VCD */
	{USB_DEVICE(0x055f, 0xc220)},	/* Gsmart Mini */
	{USB_DEVICE(0x0733, 0x2211)},	/* Jenoptik jdc 21 LCD */
	{USB_DEVICE(0x046d, 0x0900)},	/* Logitech Inc. ClickSmart 310 */
	{USB_DEVICE(0x055f, 0xc360)},	/* Mustek DV4000 Mpeg4  */
	{USB_DEVICE(0x08ca, 0x2024)},	/* Aiptek DV3500 Mpeg4  */
	{USB_DEVICE(0x046d, 0x0905)},	/* Logitech ClickSmart820  */
	{USB_DEVICE(0x05da, 0x1018)},	/* Digital Dream Enigma 1.3 */
	{USB_DEVICE(0x0c45, 0x6025)},	/* Xcam Shanga */
	{USB_DEVICE(0x0733, 0x1311)},	/* Digital Dream Epsilon 1.3 */
	{USB_DEVICE(0x041e, 0x401d)},	/* Creative Webcam NX ULTRA */
	{USB_DEVICE(0x08ca, 0x2016)},	/* Aiptek PocketCam 2 Mega */
	{USB_DEVICE(0x0734, 0x043b)},	/* 3DeMon USB Capture aka */
	{USB_DEVICE(0x041E, 0x4018)},	/* Creative Webcam Vista (PD1100) */
	{USB_DEVICE(0x0546, 0x3273)},	/* Polaroid PDC2030 */
	{USB_DEVICE(0x041e, 0x401f)},	/* Creative Webcam Notebook PD1171 */
	{USB_DEVICE(0x041e, 0x4017)},	/* Creative Webcam Mobile PD1090 */
	{USB_DEVICE(0x046d, 0x08a2)},	/* Labtec Webcam Pro */
	{USB_DEVICE(0x055f, 0xd003)},	/* Mustek WCam300A */
	{USB_DEVICE(0x0458, 0x7007)},	/* Genius VideoCam V2 */
	{USB_DEVICE(0x0458, 0x700c)},	/* Genius VideoCam V3 */
	{USB_DEVICE(0x0458, 0x700f)},	/* Genius VideoCam Web V2 */
	{USB_DEVICE(0x041e, 0x401e)},	/* Creative Nx Pro */
	{USB_DEVICE(0x0c45, 0x6029)},	/* spcaCam@150 */
	{USB_DEVICE(0x0c45, 0x6009)},	/* spcaCam@120 */
	{USB_DEVICE(0x0c45, 0x600d)},	/* spcaCam@120 */
	{USB_DEVICE(0x04fc, 0x5330)},	/* Digitrex 2110 */
	{USB_DEVICE(0x055f, 0xc540)},	/* Gsmart D30 */
	{USB_DEVICE(0x0ac8, 0x301b)},	/* Asam Vimicro */
	{USB_DEVICE(0x041e, 0x403a)},	/* Creative Nx Pro 2 */
	{USB_DEVICE(0x055f, 0xc211)},	/* Kowa Bs888e Microcamera */
	{USB_DEVICE(0x0ac8, 0x0302)},	/* Z-star Vimicro zc0302 */
	{USB_DEVICE(0x0572, 0x0041)},	/* Creative Notebook cx11646 */
	{USB_DEVICE(0x08ca, 0x2022)},	/* Aiptek Slim 3200 */
	{USB_DEVICE(0x046d, 0x0921)},	/* Labtec Webcam */
	{USB_DEVICE(0x046d, 0x0920)},	/* QC Express */
	{USB_DEVICE(0x0923, 0x010f)},	/* ICM532 cams */
	{USB_DEVICE(0x055f, 0xc200)},	/* Mustek Gsmart 300 */
	{USB_DEVICE(0x0733, 0x2221)},	/* Mercury Digital Pro 3.1p */
	{USB_DEVICE(0x041e, 0x4036)},	/* Creative Live ! */
	{USB_DEVICE(0x055f, 0xc005)},	/* Mustek Wcam300A */
	{USB_DEVICE(0x041E, 0x403b)},	/* Creative Webcam Vista (VF0010) */
	{USB_DEVICE(0x0545, 0x8333)},	/* Veo Stingray */
	{USB_DEVICE(0x0545, 0x808b)},	/* Veo Stingray */
	{USB_DEVICE(0x10fd, 0x8050)},	/* Typhoon Webshot II USB 300k */
	{USB_DEVICE(0x0546, 0x3155)},	/* Polaroid PDC3070 */
	{USB_DEVICE(0x046d, 0x0928)},	/* Logitech QC Express Etch2 */
	{USB_DEVICE(0x046d, 0x092a)},	/* Logitech QC for Notebook */
	{USB_DEVICE(0x046d, 0x08a0)},	/* Logitech QC IM */
	{USB_DEVICE(0x0461, 0x0a00)},	/* MicroInnovation WebCam320 */
	{USB_DEVICE(0x08ca, 0x2028)},	/* Aiptek PocketCam4M */
	{USB_DEVICE(0x08ca, 0x2042)},	/* Aiptek PocketDV5100 */
	{USB_DEVICE(0x08ca, 0x2060)},	/* Aiptek PocketDV5300 */
	{USB_DEVICE(0x04fc, 0x5360)},	/* Sunplus Generic */
	{USB_DEVICE(0x046d, 0x08a1)},	/* Logitech QC IM 0x08A1 +sound */
	{USB_DEVICE(0x046d, 0x08a3)},	/* Logitech QC Chat */
	{USB_DEVICE(0x046d, 0x08b9)},	/* Logitech QC IM ??? */
	{USB_DEVICE(0x046d, 0x0929)},	/* Labtec Webcam Elch2 */
	{USB_DEVICE(0x10fd, 0x0128)},	/* Typhoon Webshot II USB 300k 0x0128 */
	{USB_DEVICE(0x102c, 0x6151)},	/* Qcam Sangha CIF */
	{USB_DEVICE(0x102c, 0x6251)},	/* Qcam xxxxxx VGA */
	{USB_DEVICE(0x04fc, 0x7333)},	/* PalmPixDC85 */
	{USB_DEVICE(0x06be, 0x0800)},	/* Optimedia */
	{USB_DEVICE(0x2899, 0x012c)},	/* Toptro Industrial */
	{USB_DEVICE(0x06bd, 0x0404)},	/* Agfa CL20 */
	{USB_DEVICE(0x046d, 0x092c)},	/* Logitech QC chat Elch2 */
	{USB_DEVICE(0x0c45, 0x607c)},	/* Sonix sn9c102p Hv7131R */
	{USB_DEVICE(0x0733, 0x3261)},	/* Concord 3045 spca536a */
	{USB_DEVICE(0x0733, 0x1314)},	/* Mercury 2.1MEG Deluxe Classic Cam */
	{USB_DEVICE(0x041e, 0x401c)},	/* Creative NX */
	{USB_DEVICE(0x041e, 0x4034)},	/* Creative Instant P0620 */
	{USB_DEVICE(0x041e, 0x4035)},	/* Creative Instant P0620D */
	{USB_DEVICE(0x046d, 0x08ae)},	/* Logitech QuickCam for Notebooks */
	{USB_DEVICE(0x055f, 0xd004)},	/* Mustek WCam300 AN */
	{USB_DEVICE(0x046d, 0x092b)},	/* Labtec Webcam Plus */
	{USB_DEVICE(0x0c45, 0x602e)},	/* Genius VideoCam Messenger */
	{USB_DEVICE(0x0c45, 0x602c)},	/* Generic Sonix OV7630 */
	{USB_DEVICE(0x093A, 0x050F)},	/* Mars-Semi Pc-Camera */
	{USB_DEVICE(0x0458, 0x7006)},	/* Genius Dsc 1.3 Smart */
	{USB_DEVICE(0x055f, 0xc630)},	/* Mustek MDC4000 */
	{USB_DEVICE(0x046d, 0x08ad)},	/* Logitech QCCommunicate STX */
	{USB_DEVICE(0x0c45, 0x602d)},	/* LIC-200 LG */
	{USB_DEVICE(0x0c45, 0x6005)},	/* Sweex Tas5110 */
	{USB_DEVICE(0x0c45, 0x613c)},	/* Sonix Pccam168 */
	{USB_DEVICE(0x0c45, 0x6130)},	/* Sonix Pccam */
	{USB_DEVICE(0x0c45, 0x60c0)},	/* Sangha Sn535 */
	{USB_DEVICE(0x0c45, 0x60fc)},	/* LG-LIC300 */
	{USB_DEVICE(0x0546, 0x3191)},	/* Polaroid Ion 80 */
	{USB_DEVICE(0x0ac8, 0x305b)},	/* Z-star Vimicro zc0305b */
	{USB_DEVICE(0x0c45, 0x6028)},	/* Sonix Btc Pc380 */
	{USB_DEVICE(0x046d, 0x08a9)},	/* Logitech Notebook Deluxe */
	{USB_DEVICE(0x046d, 0x08aa)},	/* Labtec Webcam  Notebook */
	{USB_DEVICE(0x04f1, 0x1001)},	/* JVC GC A50 */
	{USB_DEVICE(0x0497, 0xc001)},	/* Smile International */
	{USB_DEVICE(0x041e, 0x4012)},	/* PC-Cam350 */
	{USB_DEVICE(0x0ac8, 0x303b)},	/* Vimicro 0x303b */
	{USB_DEVICE(0x093a, 0x2468)},	/* PAC207 */
	{USB_DEVICE(0x093a, 0x2471)},	/* PAC207 Genius VideoCam ge111 */
	{USB_DEVICE(0x093a, 0x2460)},	/* PAC207 Qtec Webcam 100 */
	{USB_DEVICE(0x0733, 0x3281)},	/* Cyberpix S550V */
	{USB_DEVICE(0x093a, 0x2470)},	/* Genius GF112 */
	{USB_DEVICE(0x046d, 0x08a6)},	/* Logitech QCim */
	{USB_DEVICE(0x08ca, 0x2020)},	/* Aiptek Slim 3000F */
	{USB_DEVICE(0x0698, 0x2003)},	/* CTX M730V built in */
	{USB_DEVICE(0x0c45, 0x6001)},	/* Genius VideoCAM NB */
	{USB_DEVICE(0x041E, 0x4028)},	/* Creative Webcam Vista Plus */
	{USB_DEVICE(0x0471, 0x0325)},	/* Philips SPC 200 NC */
	{USB_DEVICE(0x0471, 0x0328)},	/* Philips SPC 700 NC */
	{USB_DEVICE(0x0c45, 0x6040)},	/* Speed NVC 350K */
	{USB_DEVICE(0x055f, 0xc230)},	/* Mustek Digicam 330K */
	{USB_DEVICE(0x0c45, 0x6007)},	/* Sonix sn9c101 + Tas5110D */
	{USB_DEVICE(0x0471, 0x0327)},	/* Philips SPC 600 NC */
	{USB_DEVICE(0x0471, 0x0326)},	/* Philips SPC 300 NC */
	{USB_DEVICE(0x0c45, 0x6019)},	/* Generic Sonix OV7630 */
	{USB_DEVICE(0x0c45, 0x6024)},	/* Generic Sonix Tas5130c */
	{USB_DEVICE(0x046d, 0x08a7)},	/* Logitech QuickCam Image */
	{USB_DEVICE(0x04fc, 0x500c)},	/* Sunplus CA500C */
	{USB_DEVICE(0x055f, 0xc232)},	/* Mustek MDC3500 */
	{USB_DEVICE(0x046d, 0x08ac)},	/* Logitech QuickCam Cool */
	{USB_DEVICE(0x046d, 0x08d9)},	/* Logitech QuickCam IM/Connect */
	{USB_DEVICE(0x046d, 0x08da)},	/* Logitech QuickCam Messenger */
	{USB_DEVICE(0x046d, 0x092d)},	/* Logitech QC  Elch2 */
	{USB_DEVICE(0x046d, 0x092e)},	/* Logitech QC  Elch2 */
	{USB_DEVICE(0x046d, 0x092f)},	/* Logitech QC  Elch2 */
	{USB_DEVICE(0x041e, 0x4051)},	/* Creative Live!Cam Notebook Pro (VF0250)*/
	{USB_DEVICE(0x041E, 0x4029)},	/* Creative WebCam Vista Pro */
	{USB_DEVICE(0x041E, 0x041E)},	/* Creative WebCam Live! */
	{USB_DEVICE(0x041e, 0x4053)},	/* Creative Live!Cam Video IM*/
	{USB_DEVICE(0x046d, 0x08d7)},	/* Logitech QCam STX */
	{USB_DEVICE(0x046d, 0x08d8)},	/* Logitech Notebook Deluxe */
	{USB_DEVICE(0x08ca, 0x2040)},	/* Aiptek PocketDV4100M */
	{USB_DEVICE(0x0c45, 0x612c)},	/* Typhoon Rasy Cam 1.3MPix */
	{USB_DEVICE(0x0c45, 0x613b)},	/* Surfer SN-206 */
	{USB_DEVICE(0x0c45, 0x60fb)},	/* Surfer NoName */
	{USB_DEVICE(0x0ac8, 0xc002)},	/* Sony embedded vimicro*/
	{USB_DEVICE(0x0ac8, 0x0321)},	/* Vimicro generic vc0321 */
	{USB_DEVICE(0x046d, 0x0892)},	/* Logitech Orbicam */
	{USB_DEVICE(0x046d, 0x0896)},	/* Logitech Orbicam */
	{USB_DEVICE(0x0000, 0x0000)},	/* MystFromOri Unknow Camera */
	{}			/* Terminating entry */
};

MODULE_DEVICE_TABLE(usb, device_table);
/*
Let's include the initialization data for each camera type
*/
#include "utils/spcausb.h"
#include "Sunplus/spca501_init.h"
#include "Sunplus/spca505_init.h"
#include "Sunplus/spca506.h"
#include "Sunplus/spca508_init.h"
#include "Sunplus/spca561.h"
#include "Sunplus-jpeg/jpeg_qtables.h"
#include "Sunplus-jpeg/spca500_init.h"
#include "Sunplus-jpeg/sp5xxfw2.h"
#include "Sonix/sonix.h"
#include "Vimicro/zc3xx.h"
#include "Conexant/cx11646.h"
#include "Transvision/tv8532.h"
#include "Etoms/et61xx51.h"
#include "Mars-Semi/mr97311.h"
#include "Pixart/pac207.h"
#include "Vimicro/vc032x.h"
/* function for the tasklet */
void outpict_do_tasklet(unsigned long ptr);
/**********************************************************************
*
* Memory management
**********************************************************************/
static inline unsigned long
kvirt_to_pa(unsigned long adr)
{
	unsigned long kva, ret;
	kva = (unsigned long) page_address(vmalloc_to_page((void *) adr));
	kva |= adr & (PAGE_SIZE - 1);
	ret = __pa(kva);
	return ret;
}
static void *
rvmalloc(unsigned long size)
{
	void *mem;
	unsigned long adr;
	size = PAGE_ALIGN(size);
	mem = vmalloc_32(size);
	if (!mem)
		return NULL;
	memset(mem, 0, size);	/* Clear the ram out, no junk to the user */
	adr = (unsigned long) mem;
	while ((long) size > 0) {
		SetPageReserved(vmalloc_to_page((void *) adr));
		adr += PAGE_SIZE;
		size -= PAGE_SIZE;
	}
	return mem;
}
static void
rvfree(void *mem, unsigned long size)
{
	unsigned long adr;
	if (!mem)
		return;
	adr = (unsigned long) mem;
	while ((long) size > 0) {
		ClearPageReserved(vmalloc_to_page((void *) adr));
		adr += PAGE_SIZE;
		size -= PAGE_SIZE;
	}
	vfree(mem);
}
/* ------------------------------------------------------------------------ */
/**
* Endpoint management we assume one isoc endpoint per device
* that is not true some Zoran 0x0572:0x0001 have two
* assume ep adresse is static know 
* FIXME as I don't know how to set the bandwith budget
* we allow the maximum
**/
struct usb_host_endpoint *
gspca_set_isoc_ep(struct usb_spca50x *spca50x, int nbalt)
{
	int i, j;
	struct usb_interface *intf;
	struct usb_host_endpoint *ep;
	struct usb_device *dev = spca50x->dev;
	struct usb_host_interface *altsetting = NULL;
	int error = 0;
	PDEBUG(0, "enter get iso ep ");
	intf = usb_ifnum_to_if(dev, spca50x->iface);	
/* bandwith budget can be set here */
	for (i = nbalt; i; i--) {
		altsetting = &intf->altsetting[i];
		for (j = 0; j < altsetting->desc.bNumEndpoints; ++j) {
			ep = &altsetting->endpoint[j];
			PDEBUG(0, "test ISO EndPoint  %d",ep->desc.bEndpointAddress);
			if ((ep->desc.bEndpointAddress ==
			     (spca50x->epadr | USB_DIR_IN))
			    &&
			    ((ep->desc.
			      bmAttributes & USB_ENDPOINT_XFERTYPE_MASK) ==
			     USB_ENDPOINT_XFER_ISOC)) {
				PDEBUG(0, "ISO EndPoint found 0x%02X AlternateSet %d",
				       ep->desc.bEndpointAddress,i);
				if ((error =
				     usb_set_interface(dev, spca50x->iface,
						       i)) < 0) {
					PDEBUG(0, "Set interface err %d",
					       error);
					return NULL;
				}
				spca50x->alt = i;
				return ep;
			}
		}
	}
	PDEBUG(0, "FATAL ISO EndPoint not found ");
	return NULL;
}

static int
gspca_set_alt0(struct usb_spca50x *spca50x)
{
	int error = 0;
	if ((error = usb_set_interface(spca50x->dev, spca50x->iface, 0)) < 0) {
		PDEBUG(0, "Set interface err %d", error);
	}
	spca50x->alt = 0;
	return  error;
}
static int
gspca_kill_transfert(struct usb_spca50x *spca50x)
{
	struct urb *urb;
	unsigned int i;
	spca50x->streaming = 0;
	for (i = 0; i <  SPCA50X_NUMSBUF; ++i) {
		if ((urb = spca50x->sbuf[i].urb) == NULL)
			continue;

		usb_kill_urb(urb);
		/* urb->transfer_buffer_length is not touched by USB core, so
		 * we can use it here as the buffer length.
		 */
		if (spca50x->sbuf[i].data) {
			// kfree(gspca_dev->sbuf[i].data);
		
			usb_buffer_free(spca50x->dev,
				urb->transfer_buffer_length,
				spca50x->sbuf[i].data, urb->transfer_dma);
		
			spca50x->sbuf[i].data = NULL;
		}

		usb_free_urb(urb);
		spca50x->sbuf[i].urb = NULL;
	}
	return 0;
}
 


static int
gspca_init_transfert(struct usb_spca50x *spca50x)
{
	struct usb_host_endpoint *ep;
	struct usb_interface *intf;
	struct urb *urb;
	__u16 psize;
	int n,fx;
	struct usb_device *dev = spca50x->dev;
//	struct usb_host_interface *altsetting = NULL;
	int error = -ENOSPC;
	int nbalt = 0;
	
	if (spca50x->streaming)
		return -EBUSY;
	intf = usb_ifnum_to_if(dev, spca50x->iface);
	nbalt = intf->num_altsetting - 1;
	PDEBUG(0, "get iso nbalt %d",nbalt);
	spca50x->curframe = 0;	
while (nbalt && (error == -ENOSPC)) {
		if ((ep = gspca_set_isoc_ep(spca50x,nbalt--)) == NULL)
			return -EIO;
		psize = le16_to_cpu(ep->desc.wMaxPacketSize);
		psize = (psize & 0x07ff) * (1 + ((psize >> 11) & 3));
		PDEBUG(0, "packet size %d", psize);
		for (n = 0; n < SPCA50X_NUMSBUF; n++) {
			urb = usb_alloc_urb(FRAMES_PER_DESC, GFP_KERNEL);
			if (!urb) {
				err("init isoc: usb_alloc_urb ret. NULL");
				return -ENOMEM;
			}
			
			spca50x->sbuf[n].data = usb_buffer_alloc(spca50x->dev,
					psize * FRAMES_PER_DESC,
					GFP_KERNEL, &urb->transfer_dma);
			
			//gspca_dev->sbuf[n].data = kmalloc((psize+1)* FRAMES_PER_DESC,GFP_KERNEL);
			
			if(spca50x->sbuf[n].data == NULL){
				usb_free_urb(urb);
				gspca_kill_transfert(spca50x);
				return -ENOMEM;
			}
			spca50x->sbuf[n].urb = urb;
			urb->dev = spca50x->dev;
			urb->context = spca50x;
			urb->pipe =
			    usb_rcvisocpipe(spca50x->dev,
					    ep->desc.bEndpointAddress);
			urb->transfer_flags = URB_ISO_ASAP | URB_NO_TRANSFER_DMA_MAP;
			urb->interval = ep->desc.bInterval;
			urb->transfer_buffer = spca50x->sbuf[n].data;
			urb->complete = spca50x_isoc_irq;
			urb->number_of_packets = FRAMES_PER_DESC;
			urb->transfer_buffer_length = psize * FRAMES_PER_DESC;
			for (fx = 0; fx < FRAMES_PER_DESC; fx++) {
				urb->iso_frame_desc[fx].offset = psize * fx;
				urb->iso_frame_desc[fx].length = psize;
			}
		}
		
	
	/* mark all frame unused */
	for (n = 0; n <  SPCA50X_NUMFRAMES; n++) {
		spca50x->frame[n].grabstate = FRAME_UNUSED;
		spca50x->frame[n].scanstate = STATE_SCANNING;
	}
	/* start the cam and initialize the tasklet lock */
	spca50x->funct.start(spca50x);
	spca50x->streaming = 1;
	atomic_set(&spca50x->in_use,0);
	PDEBUG(3, "Submit URB Now");
	/* Submit the URBs. */
	for (n = 0; n < SPCA50X_NUMSBUF; ++n) {
		if ((error = usb_submit_urb(spca50x->sbuf[n].urb, GFP_KERNEL)) < 0) {
			err("init isoc: usb_submit_urb(%d) ret %d", n, error);
			gspca_kill_transfert(spca50x);
			break;	
		}
	
	}
	}
	return error;
}

/* Returns number of bits per pixel (regardless of where they are located; planar or
* not), or zero for unsupported format.
*/
static int
spca5xx_get_depth(struct usb_spca50x *spca50x, int palette)
{
	switch (palette) {
//      case VIDEO_PALETTE_GREY:     return 8;
	case VIDEO_PALETTE_RGB565:
		return 16;
	case VIDEO_PALETTE_RGB24:
		return 24;
//      case VIDEO_PALETTE_YUV422:   return 16;
//      case VIDEO_PALETTE_YUYV:
// return 16;
//      case VIDEO_PALETTE_YUV420:   return 24;
	case VIDEO_PALETTE_YUV420P:
		return 12;	/* strange need 12 this break the read method for this planar mode (6*8/4) */
//      case VIDEO_PALETTE_YUV422P:  return 24; /* Planar */
	case VIDEO_PALETTE_RGB32:
		return 32;
	case VIDEO_PALETTE_RAW_JPEG:
		return 24;	/* raw jpeg. what should we return ?? */
	case VIDEO_PALETTE_JPEG:
		if (spca50x->cameratype == JPEG ||
		    spca50x->cameratype == JPGH ||
		    spca50x->cameratype == JPGC ||
		    spca50x->cameratype == JPGS ||
		    spca50x->cameratype == JPGM) {
			return 8;
		} else
			return 0;
	default:
		return 0;	/* Invalid format */
	}
}

/**********************************************************************
* spca50x_isoc_irq
* Function processes the finish of the USB transfer by calling 
* spca50x_move_data function to move data from USB buffer to internal
* driver structures 
***********************************************************************/
#if LINUX_VERSION_CODE < KERNEL_VERSION(2,6,19)
static void
spca50x_isoc_irq(struct urb *urb, struct pt_regs *regs)
#else
static void
spca50x_isoc_irq(struct urb *urb)
#endif
{
	int i;
	struct usb_spca50x *spca50x = (struct usb_spca50x *) urb->context;
	int len;
	switch (urb->status) {
	case 0:
		break;
	default:
		PDEBUG(0, "Non-zero status (%d) in isoc "
		       "completion handler.", urb->status);
	case -ENOENT:		/* usb_kill_urb() called. */
	case -ECONNRESET:	/* usb_unlink_urb() called. */
	case -ESHUTDOWN:	/* The endpoint is being disabled. */
		return;
	}
	if (!spca50x->dev) {
		PDEBUG(4, "no device ");
		return;
	}
	if (!spca50x->user) {
		PDEBUG(4, "device not open");
		return;
	}
	if (!spca50x->streaming) {
/* Always get some of these after close but before packet engine stops */
		PDEBUG(4, "hmmm... not streaming, but got interrupt");
		return;
	}
	if (!spca50x->present) {
/*  */
		PDEBUG(4, "device disconnected ..., but got interrupt !!");
		return;
	}
/* Copy the data received into our scratch buffer */
	if (spca50x->curframe >= 0) {
		len = spca50x_move_data(spca50x, urb);
	} else if (waitqueue_active(&spca50x->wq)) {
		wake_up_interruptible(&spca50x->wq);
	}
/* Move to the next sbuf */

	urb->dev = spca50x->dev;
	urb->status = 0;
	if ((i = usb_submit_urb(urb, GFP_ATOMIC)) != 0)
		err("usb_submit_urb() ret %d", i);
	return;
}

static void
spca50x_stop_isoc(struct usb_spca50x *spca50x)
{
	if (!spca50x->streaming || !spca50x->dev)
		return;
	PDEBUG(3, "*** Stopping capture ***");
	spca50x->funct.stopN(spca50x);
	gspca_kill_transfert(spca50x);
	gspca_set_alt0(spca50x);
	spca50x->funct.stop0(spca50x);
	PDEBUG(3, "*** Capture stopped ***");
}

/**********************************************************************
* spca50x_smallest_mode_index
* Function finds the mode index in the modes table of the smallest
* available mode.
***********************************************************************/
static int
spca5xx_getDefaultMode(struct usb_spca50x *spca50x)
{
	int i;
	for (i = QCIF; i < TOTMODE; i++) {
		if (spca50x->mode_cam[i].method == 0
		    && spca50x->mode_cam[i].width) {
			spca50x->width = spca50x->mode_cam[i].width;
			spca50x->height = spca50x->mode_cam[i].height;
			spca50x->method = 0;
			spca50x->pipe_size = spca50x->mode_cam[i].pipe;
			spca50x->mode = spca50x->mode_cam[i].mode;
			return 0;
		}
	}
	return -EINVAL;
}

/**********************************************************************
* spca50x_set_mode
* Function sets up the resolution directly. 
* Attention!!! index, the index in modes array is NOT checked. 
***********************************************************************/
static int
spca5xx_getcapability(struct usb_spca50x *spca50x)
{
	int maxw, maxh, minw, minh;
	int i;
	minw = minh = 255 * 255;
	maxw = maxh = 0;
	for (i = QCIF; i < TOTMODE; i++) {
		if (spca50x->mode_cam[i].width) {
			if (maxw < spca50x->mode_cam[i].width
			    || maxh < spca50x->mode_cam[i].height) {
				maxw = spca50x->mode_cam[i].width;
				maxh = spca50x->mode_cam[i].height;
			}
			if (minw > spca50x->mode_cam[i].width
			    || minh > spca50x->mode_cam[i].height) {
				minw = spca50x->mode_cam[i].width;
				minh = spca50x->mode_cam[i].height;
			}
		}
	}
	spca50x->maxwidth = maxw;
	spca50x->maxheight = maxh;
	spca50x->minwidth = minw;
	spca50x->minheight = minh;
	PDEBUG(0, "maxw %d maxh %d minw %d minh %d", maxw, maxh, minw, minh);
	return 0;
}
static int
wxh_to_size(int width, int height)
{
	switch (width) {
	case 640:
		if (height == 480)
			return VGA;
		break;
	case 384:
		if (height == 288)
			return PAL;
		break;
	case 352:
		if (height == 288)
			return SIF;
		break;
	case 320:
		if (height == 240)
			return CIF;
		break;
	case 192:
		if (height == 144)
			return QPAL;
		break;
	case 176:
		if (height == 144)
			return QSIF;
		break;
	case 160:
		if (height == 120)
			return QCIF;
		break;
	}
	return -EINVAL;
}
static int
v4l_to_spca5xx(int format)
{
	switch (format) {
	case VIDEO_PALETTE_RGB565:
		return P_RGB16;
	case VIDEO_PALETTE_RGB24:
		return P_RGB24;
	case VIDEO_PALETTE_RGB32:
		return P_RGB32;
	case VIDEO_PALETTE_YUV422P:
		return P_YUV422;
	case VIDEO_PALETTE_YUV420P:
		return P_YUV420;
	case VIDEO_PALETTE_RAW_JPEG:
		return P_RAW;
	case VIDEO_PALETTE_JPEG:
		return P_JPEG;
	default:
		return -EINVAL;
	}
}
static inline int
spca5xx_setMode(struct usb_spca50x *spca50x, int width, int height, int format)
{
	int i, j;
	int formatIn;
	int crop = 0, cropx1 = 0, cropx2 = 0, cropy1 = 0, cropy2 = 0, x =
	    0, y = 0;
/* Avoid changing to already selected mode */
/* convert V4l format to our internal format */
	PDEBUG(3, "spca5xx set mode asked w %d h %d p %d", width, height,
	       format);
	if ((formatIn = v4l_to_spca5xx(format)) < 0)
		return -EINVAL;
	for (i = QCIF; i < TOTMODE; i++) {
		if ((spca50x->mode_cam[i].width == width) &&
		    (spca50x->mode_cam[i].height == height) &&
		    (spca50x->mode_cam[i].t_palette & formatIn)) {
			spca50x->width = spca50x->mode_cam[i].width;
			spca50x->height = spca50x->mode_cam[i].height;
			spca50x->pipe_size = spca50x->mode_cam[i].pipe;
			spca50x->mode = spca50x->mode_cam[i].mode;
			spca50x->method = spca50x->mode_cam[i].method;
			spca50x->format = format;	//palette in use
			if (spca50x->method) {
				if (spca50x->method == 1) {
					for (j = i; j < TOTMODE; j++) {
						if (spca50x->mode_cam[j].
						    method == 0
						    && spca50x->mode_cam[j].
						    width) {
							spca50x->hdrwidth =
							    spca50x->
							    mode_cam[j].width;
							spca50x->hdrheight =
							    spca50x->
							    mode_cam[j].height;
							spca50x->mode = spca50x->mode_cam[j].mode;	// overwrite by the hardware mode
							break;
						}
					}	// end match hardware mode
					if (!spca50x->hdrwidth
					    && !spca50x->hdrheight)
						return -EINVAL;
				}
			}
/* match found */
			break;
		}
	}			// end match mode
/* initialize the hdrwidth and hdrheight for the first init_source */
/* precompute the crop x y value for each frame */
	if (!spca50x->method) {
/* nothing todo hardware found stream */
		cropx1 = cropx2 = cropy1 = cropy2 = x = y = 0;
		spca50x->hdrwidth = spca50x->width;
		spca50x->hdrheight = spca50x->height;
	}
	if (spca50x->method & 0x01) {
/* cropping method */
		if (spca50x->hdrwidth > spca50x->width) {
			crop = (spca50x->hdrwidth - spca50x->width);
			if (spca50x->cameratype == JPEG
			    || spca50x->cameratype == JPGH
			    || spca50x->cameratype == JPGS)
				crop = crop >> 4;
			cropx1 = crop >> 1;
			cropx2 = cropx1 + (crop % 2);
		} else {
			cropx1 = cropx2 = 0;
		}
		if (spca50x->hdrheight > spca50x->height) {
			crop = (spca50x->hdrheight - spca50x->height);
			if (spca50x->cameratype == JPEG)
				crop = crop >> 4;
			if (spca50x->cameratype == JPGH
			    || spca50x->cameratype == JPGS)
				crop = crop >> 3;
			cropy1 = crop >> 1;
			cropy2 = cropy1 + (crop % 2);
		} else {
			cropy1 = cropy2 = 0;
		}
	}
	if (spca50x->method & 0x02) {
/* what can put here for div method */
	}
	if (spca50x->method & 0x04) {
/* and here for mult */
	}
	PDEBUG(2, "Found code %d method %d", spca50x->mode, spca50x->method);
	PDEBUG(2, "Soft Win width height %d x %d", spca50x->width,
	       spca50x->height);
	PDEBUG(2, "Hard Win width height %d x %d", spca50x->hdrwidth,
	       spca50x->hdrheight);
	for (i = 0; i < SPCA50X_NUMFRAMES; i++) {
		spca50x->frame[i].method = spca50x->method;
		spca50x->frame[i].cameratype = spca50x->cameratype;
		spca50x->frame[i].cropx1 = cropx1;
		spca50x->frame[i].cropx2 = cropx2;
		spca50x->frame[i].cropy1 = cropy1;
		spca50x->frame[i].cropy2 = cropy2;
		spca50x->frame[i].x = x;
		spca50x->frame[i].y = y;
		spca50x->frame[i].hdrwidth = spca50x->hdrwidth;
		spca50x->frame[i].hdrheight = spca50x->hdrheight;
		spca50x->frame[i].width = spca50x->width;
		spca50x->frame[i].height = spca50x->height;
		spca50x->frame[i].format = spca50x->format;
		spca50x->frame[i].scanlength =
		    spca50x->width * spca50x->height * 3 / 2;
// ?? assumes 4:2:0 data
	}
	return 0;
}

/**********************************************************************
* spca50x_mode_init_regs
* Function sets up the resolution with checking if it's necessary 
***********************************************************************/
static int
spca5xx_restartMode(struct usb_spca50x *spca50x, int width, int height,
		    int format)
{
	int was_streaming;
	int r;
/* Avoid changing to already selected mode */
	if (spca50x->width == width && spca50x->height == height)
		return 0;
	PDEBUG(1, "Mode changing to %d,%d", width, height);
	was_streaming = spca50x->streaming;
/* FIXME spca500 bridge is there a way to find an init like 
Clicksmart310 ? */
	if (was_streaming) {
		if ((spca50x->bridge != BRIDGE_SPCA500)
		    || (spca50x->desc == LogitechClickSmart310))
			spca50x_stop_isoc(spca50x);
	}
	r = spca5xx_setMode(spca50x, width, height, format);
	if (r < 0)
		goto out;
	if (was_streaming) {
		if ((spca50x->bridge != BRIDGE_SPCA500)
		    || (spca50x->desc == LogitechClickSmart310)) {
			r = gspca_init_transfert(spca50x);
		} else {
			spca50x->funct.start(spca50x);
		}
	}
      out:
	return r;
}
#if 0
/**********************************************************************
*
* SPCA50X data transfer, IRQ handler
*
**********************************************************************/
static struct spca50x_frame *
spca50x_next_frame(struct usb_spca50x
		   *spca50x, unsigned char *cdata)
{
	int iFrameNext;
	struct spca50x_frame *frame = NULL;
	PDEBUG(2, "Frame %d State %d", spca50x->curframe,
	       spca50x->frame[spca50x->curframe].grabstate);
	if (spca50x->frame[spca50x->curframe].grabstate == FRAME_ERROR) {
		PDEBUG(2, "Frame %d errdrop", spca50x->curframe);
		frame = &spca50x->frame[spca50x->curframe];
		goto dropframe;
	}
/* Cycle through the frame buffer looking for a free frame to overwrite */
	iFrameNext = (spca50x->curframe + 1) % SPCA50X_NUMFRAMES;
	while (frame == NULL && iFrameNext != (spca50x->curframe)) {
		if (spca50x->frame[iFrameNext].grabstate == FRAME_READY ||
		    spca50x->frame[iFrameNext].grabstate == FRAME_UNUSED ||
		    spca50x->frame[iFrameNext].grabstate == FRAME_ERROR) {
			spca50x->curframe = iFrameNext;
			frame = &spca50x->frame[iFrameNext];
			break;
		} else {
			iFrameNext = (iFrameNext + 1) % SPCA50X_NUMFRAMES;
		}
	}
	if (frame == NULL) {
		PDEBUG(3, "Can't find a free frame to grab into...using next. "
		       "This is caused by the application not reading fast enough.");
		spca50x->curframe = (spca50x->curframe + 1) % SPCA50X_NUMFRAMES;
		frame = &spca50x->frame[spca50x->curframe];
	}

dropframe:
	frame->grabstate = FRAME_GRABBING;
	if (spca50x->pictsetting.change) {
		memcpy(&frame->pictsetting, &spca50x->pictsetting,
		       sizeof (struct pictparam));
/* reset flag change */
		spca50x->pictsetting.change = 0;
		PDEBUG(2, "Picture setting change Pass to decoding   ");
	}
/* Reset some per-frame variables */
	frame->highwater = frame->data;
	frame->scanstate = STATE_LINES;
	frame->scanlength = 0;
	frame->last_packet = -1;
	frame->totlength = 0;
	spca50x->packet = 0;
out:
	return frame;
}
#endif
/**********************************************************************
*
* SPCA50X data transfer, IRQ handler
*
**********************************************************************/
static struct spca50x_frame *
spca50x_next_frame(struct usb_spca50x
		   *spca50x, unsigned char *cdata)
{
	struct spca50x_frame *frame = NULL;
	PDEBUG(2, "Frame %d State %d", spca50x->curframe,
	       spca50x->frame[spca50x->curframe].grabstate);
	if (spca50x->frame[spca50x->curframe].grabstate != FRAME_ERROR) 
		spca50x->curframe = (spca50x->curframe + 1) % SPCA50X_NUMFRAMES;	
	frame = &spca50x->frame[spca50x->curframe];
	if (spca50x->pictsetting.change) {
		memcpy(&frame->pictsetting, &spca50x->pictsetting,
		       sizeof (struct pictparam));
/* reset flag change */
		spca50x->pictsetting.change = 0;
		PDEBUG(2, "Picture setting change Pass to decoding   ");
	}
/* Reset some per-frame variables */
	frame->grabstate = FRAME_GRABBING;
	frame->scanstate = STATE_LINES;
	frame->highwater = frame->data;
	frame->scanlength = 0;
	frame->last_packet = -1;
	frame->totlength = 0;
	spca50x->packet = 0;
	return frame;
}
/* Tasklet function to decode */
void
outpict_do_tasklet(unsigned long ptr)
{
	int err;
	struct spca50x_frame *taskletframe = (struct spca50x_frame *) ptr;
	taskletframe->scanlength = taskletframe->highwater - taskletframe->data;
	PDEBUG(2,
	       "Tasklet ask spcadecoder hdrwidth %d hdrheight %d method %d ",
	       taskletframe->hdrwidth, taskletframe->hdrheight,
	       taskletframe->method);
	if ((err = spca50x_outpicture(taskletframe)) < 0) {
		PDEBUG(2, "frame decoder failed (%d)", err);
		taskletframe->grabstate = FRAME_ERROR;
	} else {
		taskletframe->grabstate = FRAME_DONE;
		PDEBUG(2, "Decode framestate return %d",
		       taskletframe->grabstate);
	}
	if (waitqueue_active(&taskletframe->wq))
		wake_up_interruptible(&taskletframe->wq);
	atomic_set(&taskletframe->spca50x_dev->in_use,0);
}

/*********************************************************************
time Helper function
**********************************************************************/
static inline unsigned long
spca5xx_gettimes(void)
{
	u64 times_now;
	times_now = get_jiffies_64();
	return jiffies_to_msecs(times_now);
}

/* ******************************************************************
* spca50x_move_data
* Function serves for moving data from USB transfer buffers
* to internal driver frame buffers.
******************************************************************* */
static int
spca50x_move_data(struct usb_spca50x *spca50x, struct urb *urb)
{
	unsigned char *cdata;	//Pointer to buffer where we do store next packet
	unsigned char *pData;	//Pointer to buffer where we do store next packet
	int i;
	for (i = 0; i < urb->number_of_packets; i++) {
		int datalength = urb->iso_frame_desc[i].actual_length;
		int st = urb->iso_frame_desc[i].status;
		unsigned long ms_times_now;
		unsigned long ms_times_before;
		struct spca50x_frame *frame;	//Pointer to frame data
		int sequenceNumber;
		int sof;
		int iPix;	//Offset of pixel data in the ISO packet
		if (st) {
			PDEBUG(0, "ISOC data error: [%d] len=%d, status=%d \n",
			       i, datalength, st);
			continue;
		}
		cdata = ((unsigned char *) urb->transfer_buffer) +
		    urb->iso_frame_desc[i].offset;
/* Check for zero length block or no selected frame buffer */
		if (!datalength || spca50x->curframe == -1) {
			spca50x->synchro = 0;
			continue;
		}
		PDEBUG(5, "Packet data [%d,%d,%d] Status: %d", datalength, st,
		       urb->iso_frame_desc[i].offset, st);
		frame = &spca50x->frame[spca50x->curframe];
		if (frame->last_packet == -1) {
/*initialize a new frame */
			sequenceNumber = 0;
		} else {
			sequenceNumber = frame->last_packet;
		}
/* check frame start */
		if ((sof =
		     spca50x->funct.sof_detect(spca50x, frame, cdata, &iPix,
					       sequenceNumber,
					       &datalength)) < 0)
			continue;
		sequenceNumber = sof;
		PDEBUG(3, "spca50x: Packet seqnum = 0x%02x.  curframe=%2d",
		       sequenceNumber, spca50x->curframe);
		pData = cdata;
/* Can we find a frame start */
		if (sequenceNumber == 0) {
			PDEBUG(3, "spca50x: Found Frame Start!, framenum = %d",
			       spca50x->curframe);
// Start of frame is implicit end of previous frame
// Check for a previous frame and finish it off if one exists
			if (frame->scanstate == STATE_LINES) {
				if (frame->format != VIDEO_PALETTE_RAW_JPEG) {
/* overflow ? */
					ms_times_now = spca5xx_gettimes();
					if (ms_times_now < spca50x->last_times)
						spca50x->last_times = 0;
					spin_lock(&spca50x->v4l_lock);
					ms_times_before =
					    spca50x->last_times +
					    spca50x->dtimes;
					spin_unlock(&spca50x->v4l_lock);
					if (ms_times_now >= ms_times_before) {
						PDEBUG(2,
						       "Decode frame last %d",
						       (int) (ms_times_now -
							      spca50x->
							      last_times));
						spca50x->last_times =
						    ms_times_now;
/* Decode the frame one at a times or drop*/
						if(!atomic_read(&spca50x->in_use)){
						atomic_set(&spca50x->in_use,1);
						spca50x->spca5xx_tasklet.data = (unsigned long) frame;
						tasklet_schedule(&spca50x->
								 spca5xx_tasklet);
						} else
							frame->grabstate = FRAME_ERROR;
					} else
						frame->grabstate = FRAME_ERROR;
				} else {
/* RAW DATA stream */
					frame->grabstate = FRAME_DONE;
					if (waitqueue_active(&frame->wq))
						wake_up_interruptible(&frame->
								      wq);
				}
// If someone decided to wait for ANY frame - wake him up 
				if (waitqueue_active(&spca50x->wq))
					wake_up_interruptible(&spca50x->wq);
				frame = spca50x_next_frame(spca50x, cdata);
			} else
				frame->scanstate = STATE_LINES;
		}
/* Are we in a frame? */
		if (frame == NULL || frame->scanstate != STATE_LINES)
			continue;
		frame->last_packet = sequenceNumber;
		pData = cdata + iPix;	// Skip packet header (1 or 10 bytes)
// Consume data
		PDEBUG(5, "Processing packet seq  %d,length %d,totlength %d",
		       frame->last_packet, datalength, frame->totlength);
/* this copy consume input data from the isoc stream */
		if ((datalength > 0)) {
			memcpy(frame->highwater, pData, datalength);
			frame->highwater += datalength;
			frame->totlength += datalength;
		}
	}
	return 0;
}

/****************************************************************************
*
* Buffer management
*
***************************************************************************/
static int
spca50x_alloc(struct usb_spca50x *spca50x)
{
	int i;
	PDEBUG(4, "entered");
	down(&spca50x->buf_lock);
	if (spca50x->buf_state == BUF_ALLOCATED)
		goto out;
	spca50x->tmpBuffer = rvmalloc(MAX_FRAME_SIZE);
	if (!spca50x->tmpBuffer)
		goto error;
	spca50x->fbuf = rvmalloc(SPCA50X_NUMFRAMES * MAX_DATA_SIZE);
	if (!spca50x->fbuf)
		goto error;
	for (i = 0; i < SPCA50X_NUMFRAMES; i++) {
		spca50x->frame[i].tmpbuffer = spca50x->tmpBuffer;
		spca50x->frame[i].decoder = &spca50x->maindecode;	//connect each frame to the main data decoding 
spca50x->frame[i].spca50x_dev = spca50x;	//refind the whole structure 
		spca50x->frame[i].grabstate = FRAME_UNUSED;
		spca50x->frame[i].scanstate = STATE_SCANNING;
		spca50x->frame[i].data = spca50x->fbuf + i * MAX_DATA_SIZE;
		spca50x->frame[i].highwater = spca50x->frame[i].data;
		memset(&spca50x->frame[i].pictsetting, 0,
		       sizeof (struct pictparam));
		PDEBUG(4, "frame[%d] @ %p", i, spca50x->frame[i].data);
	}

	spca50x->buf_state = BUF_ALLOCATED;
      out:
	up(&spca50x->buf_lock);
	PDEBUG(4, "leaving");
	return 0;
      error:
	if (spca50x->fbuf) {
		rvfree(spca50x->fbuf, SPCA50X_NUMFRAMES * MAX_DATA_SIZE);
		spca50x->fbuf = NULL;
	}
	if (spca50x->tmpBuffer) {
		rvfree(spca50x->tmpBuffer, MAX_FRAME_SIZE);
		spca50x->tmpBuffer = NULL;
	}
	spca50x->buf_state = BUF_NOT_ALLOCATED;
	up(&spca50x->buf_lock);
	PDEBUG(1, "errored");
	return -ENOMEM;
}
static void
spca5xx_dealloc(struct usb_spca50x *spca50x)
{
	int i;
	PDEBUG(2, "entered dealloc");
	down(&spca50x->buf_lock);
	if (spca50x->fbuf) {
		rvfree(spca50x->fbuf, SPCA50X_NUMFRAMES * MAX_DATA_SIZE);
		spca50x->fbuf = NULL;
		for (i = 0; i < SPCA50X_NUMFRAMES; i++)
			spca50x->frame[i].data = NULL;
	}
	if (spca50x->tmpBuffer) {
		rvfree(spca50x->tmpBuffer, MAX_FRAME_SIZE);
		spca50x->tmpBuffer = NULL;
	}

	PDEBUG(2, "buffer memory deallocated");
	spca50x->buf_state = BUF_NOT_ALLOCATED;
	up(&spca50x->buf_lock);
	PDEBUG(2, "leaving dealloc");
}

/**
* Reset the camera and send the correct initialization sequence for the
* currently selected source
*/
static int
spca50x_init_source(struct usb_spca50x *spca50x)
{
	int err_code;
	if ((err_code = spca50x->funct.initialize(spca50x)) < 0)
		return -EINVAL;
	spca50x->norme = 0;
	spca50x->channel = 0;
	spca50x->light_freq = lightfreq;
	if ((err_code =
	     spca5xx_setMode(spca50x, spca50x->width, spca50x->height,
			     VIDEO_PALETTE_RGB24)) < 0)
		return -EINVAL;
	spca5xx_set_light_freq(spca50x, lightfreq); 

	return 0;
}

/****************************************************************************
*
* V4L API
*
***************************************************************************/
static inline void
spca5xx_setFrameDecoder(struct usb_spca50x *spca50x)
{
	int i;
/* configure the frame detector with default parameters */
	memset(&spca50x->pictsetting, 0, sizeof (struct pictparam));
	spca50x->pictsetting.change = 0x01;
	spca50x->pictsetting.force_rgb = force_rgb;
	spca50x->pictsetting.gamma = gamma;
	spca50x->pictsetting.OffRed = OffRed;
	spca50x->pictsetting.OffBlue = OffBlue;
	spca50x->pictsetting.OffGreen = OffGreen;
	spca50x->pictsetting.GRed = GRed;
	spca50x->pictsetting.GBlue = GBlue;
	spca50x->pictsetting.GGreen = GGreen;
/* Set default sizes in case IOCTL (VIDIOCMCAPTURE) is not used
* (using read() instead). */
	for (i = 0; i < SPCA50X_NUMFRAMES; i++) {
		spca50x->frame[i].width = spca50x->width;
		spca50x->frame[i].height = spca50x->height;
		spca50x->frame[i].cameratype = spca50x->cameratype;
		spca50x->frame[i].scanlength = spca50x->width * spca50x->height * 3 / 2;	// assumes 4:2:0 data
		spca50x->frame[i].depth = 24;
/* Note: format reflects format of data as returned to
* a process, not as read from camera hardware.
* This might be a good idea for dumb programs always
* assuming the following settings.
*/
		spca50x->frame[i].format = VIDEO_PALETTE_RGB24;
	}
	spca50x->format = VIDEO_PALETTE_RGB24;
}
static int
spca5xx_isjpeg(struct usb_spca50x *spca50x)
{
	if (spca50x->cameratype == JPGH
	    || spca50x->cameratype == JPGC
	    || spca50x->cameratype == JPGS
	    || spca50x->cameratype == JPEG || spca50x->cameratype == JPGM)
		return 1;
	return 0;
}
static void
spca5xx_initDecoder(struct usb_spca50x *spca50x)
{
	if (spca5xx_isjpeg(spca50x))
		init_jpeg_decoder(spca50x);
	if (spca50x->bridge == BRIDGE_SONIX)
		init_sonix_decoder(spca50x);
	if (spca50x->bridge == BRIDGE_PAC207)
		init_pixart_decoder(spca50x);
}
static void
spca5xx_chgAuto(struct usb_spca50x *spca50x, __u8 autoval)
{
	spca50x->autoexpo = (int) autoval;
	spca50x->funct.set_autobright(spca50x);
}
static void
spca5xx_chgQtable(struct usb_spca50x *spca50x, __u8 qtable)
{
	int intqtable = (int) qtable;
/* one frame maybe corrupted  wait for the result */
	if (spca5xx_isjpeg(spca50x) && (spca50x->qindex != intqtable)) {
		if (spca50x->cameratype == JPGH) {
/* only vimicro ATM */
			spca50x->qindex = intqtable;
			spca50x->funct.set_quality(spca50x);
			init_jpeg_decoder(spca50x);
		}
	}
}
static inline void
spca5xx_chgDtimes(struct usb_spca50x *spca50x, __u16 dtimes)
{
	unsigned long flags;
	spin_lock_irqsave(&spca50x->v4l_lock, flags);
	spca50x->dtimes = (unsigned int) dtimes;
	spin_unlock_irqrestore(&spca50x->v4l_lock, flags);
}
/* Matches the sensor's internal frame rate to the lighting frequency.
 * Valid frequencies are:
 *	50 - 50Hz, for European and Asian lighting (default)
 *	60 - 60Hz, for American lighting
 *       0 - No Fliker (for outdoore usage)
 * Returns: 0 for success
 */
static int
spca5xx_set_light_freq(struct usb_spca50x *spca50x, int freq)
{
	int freq_set;

	if (freq == 50)
		freq_set = freq_50HZ;
	else if (freq == 60)
		freq_set = freq_60HZ;
	else if (freq == 0)
		freq_set = NoFliker;
	else {
		PDEBUG(0,"Invalid light freq (%d Hz)", freq);
		return -EINVAL;
	}

	switch (spca50x->sensor) {
	case SENSOR_TAS5130C_VF0250:
	case SENSOR_TAS5130CXX:
	case SENSOR_PB0330:
	case SENSOR_PAS106:
	case SENSOR_ICM105A:
	case SENSOR_HDCS2020b:
	case SENSOR_CS2102:
	    break;
	default:
		PDEBUG(0,"Sensor currently not support light frequency banding filters.");
		return -EINVAL;
	}
	
	if (freq_set == freq_50HZ) {
          PDEBUG(1, "Light frequency banding filter set to 50HZ mode");
	 if (spca50x->mode && spca50x->funct.set_50HZ) {
            spca50x->funct.set_50HZ(spca50x);
	 }  else if (spca50x->funct.set_50HZScale) {
            spca50x->funct.set_50HZScale(spca50x); 
	 }   
    	} else if (freq_set == freq_60HZ) {
          PDEBUG(1, "Light frequency banding filter set to 60HZ mode");
         if (spca50x->mode && spca50x->funct.set_60HZ) {
            spca50x->funct.set_60HZ(spca50x);
	 } else if (spca50x->funct.set_60HZScale) {
	    spca50x->funct.set_60HZScale(spca50x);
	 }    
    	} else if (freq_set == NoFliker) {
          PDEBUG(1, "Light frequency banding filter set to NoFliker mode");
         if (spca50x->mode && spca50x->funct.set_NoFliker) {
            spca50x->funct.set_NoFliker(spca50x);
	} else if (spca50x->funct.set_NoFlikerScale) {
            spca50x->funct.set_NoFlikerScale(spca50x);
	 }    
    	}
	spca50x->light_freq = freq;
	return 0;
}

static int
spca5xx_open(struct inode *inode, struct file *file)
{
	struct video_device *vdev = video_devdata(file);
	struct usb_spca50x *spca50x = video_get_drvdata(vdev);
	int err;
	PDEBUG(2, "opening");
	down(&spca50x->lock);
/* sanity check disconnect, in use, no memory available */
	err = -ENODEV;
	if (!spca50x->present)
		goto out;
	err = -EBUSY;
	if (spca50x->user)
		goto out;
	err = -ENOMEM;
	if (spca50x_alloc(spca50x))
		goto out;
/* initialize sensor and decoding */
	err = spca50x_init_source(spca50x);
	if (err != 0) {
		PDEBUG(0, "DEALLOC error on spca50x_init_source\n");
		up(&spca50x->lock);
		spca5xx_dealloc(spca50x);
		goto out2;
	}
	spca5xx_initDecoder(spca50x);
/* open always start in rgb24 a bug in gqcam 
did not select the palette nor the size  
v4l spec need that the camera always start on the last setting */
	spca5xx_setFrameDecoder(spca50x);
	spca50x->user++;
	file->private_data = vdev;
	err = gspca_init_transfert(spca50x);
	if (err) {
		PDEBUG(0, " DEALLOC error on init_Isoc\n");
		spca50x->user--;
		gspca_kill_transfert(spca50x);
		up(&spca50x->lock);
		spca5xx_dealloc(spca50x);
		file->private_data = NULL;
		goto out2;
	}
/* Now, let's get brightness from the camera */
	spca50x->brightness = spca50x->funct.get_bright(spca50x);
	spca50x->whiteness = 0;
      out:
	up(&spca50x->lock);
      out2:
	if (err) {
		PDEBUG(2, "Open failed");
	} else {
		PDEBUG(2, "Open done");
	}
	return err;
}
static void inline
spcaCameraShutDown(struct usb_spca50x *spca50x)
{
	if (spca50x->dev) {
		spca50x->funct.cam_shutdown(spca50x);
	}
}
static int
spca5xx_close(struct inode *inode, struct file *file)
{
	struct video_device *vdev = file->private_data;
	struct usb_spca50x *spca50x = video_get_drvdata(vdev);
	int i;
	PDEBUG(2, "spca50x_close");
	down(&spca50x->lock);
	spca50x->user--;
	spca50x->curframe = -1;
	if (spca50x->present) {
		spca50x_stop_isoc(spca50x);
		spcaCameraShutDown(spca50x);
		for (i = 0; i < SPCA50X_NUMFRAMES; i++) {
			if (waitqueue_active(&spca50x->frame[i].wq))
				wake_up_interruptible(&spca50x->frame[i].wq);
		}
		if (waitqueue_active(&spca50x->wq))
			wake_up_interruptible(&spca50x->wq);
	}
/* times to dealloc ressource */
	up(&spca50x->lock);
	spca5xx_dealloc(spca50x);
	PDEBUG(2, "Release ressources done");
	file->private_data = NULL;
	return 0;
}
static int
spca5xx_testPalSize(struct usb_spca50x *spca50x, int pal, int w, int h)
{
	int needpalette;
	int needsize;
	if ((needpalette = v4l_to_spca5xx(pal)) < 0)
		return -EINVAL;
	if ((needsize = wxh_to_size(w, h)) < 0)
		return -EINVAL;
	if (!(spca50x->mode_cam[needsize].t_palette & needpalette))
		return -EINVAL;
	return 0;
}
static int
spca5xx_do_ioctl(struct inode *inode, struct file *file, unsigned int cmd,
		 void *arg)
{
	struct video_device *vdev = file->private_data;
	struct usb_spca50x *spca50x = video_get_drvdata(vdev);
	PDEBUG(2, "do_IOCtl: 0x%X", cmd);
	if (!spca50x->dev)
		return -EIO;
	switch (cmd) {
	case VIDIOCGCAP:
		{
			struct video_capability *b = arg;
			PDEBUG(2, "VIDIOCGCAP %p :", b);
			memset(b, 0, sizeof (struct video_capability));
			snprintf(b->name, 32, "%s",
				 clist[spca50x->desc].description);
			b->type = VID_TYPE_CAPTURE;
			b->channels =
			    ((spca50x->bridge == BRIDGE_SPCA506) ? 8 : 1);
			b->audios = 0;
			b->maxwidth = spca50x->maxwidth;
			b->maxheight = spca50x->maxheight;
			b->minwidth = spca50x->minwidth;
			b->minheight = spca50x->minheight;
			return 0;
		}
	case VIDIOCGCHAN:
		{
			struct video_channel *v = arg;
			switch (spca50x->bridge) {
			case BRIDGE_SPCA505:
				{
					strncpy(v->name,
						((v->channel ==
						  0) ? "SPCA505" : "Video In"),
						32);
					break;
				}
			case BRIDGE_SPCA506:
				{
					spca506_GetNormeInput(spca50x,
							      (__u16 *) & (v->
									   norm),
							      (__u16 *) & (v->
									   channel));
					if (v->channel < 4) {
						snprintf(v->name, 32,
							 "SPCA506-CBVS-%d",
							 v->channel);
					} else {
						snprintf(v->name, 32,
							 "SPCA506-S-Video-%d",
							 v->channel);
					}
					break;
				}
			default:
				snprintf(v->name, 32, "%s",
					 Blist[spca50x->bridge].name);
				break;
			}
			v->flags = 0;
			v->tuners = 0;
			v->type = VIDEO_TYPE_CAMERA;
			return 0;
		}
	case VIDIOCSCHAN:
		{
			struct video_channel *v = arg;
/* exclude hardware channel reserved */
			if ((v->channel < 0) || (v->channel > 9)
			    || (v->channel == 4)
			    || (v->channel == 5))
				return -EINVAL;
			if (spca50x->bridge == BRIDGE_SPCA506) {
				spca506_SetNormeInput(spca50x, v->norm,
						      v->channel);
			}
			return 0;
		}
	case VIDIOCGPICT:
		{
			struct video_picture *p = arg;
			p->depth = spca50x->frame[0].depth;
			p->palette = spca50x->format;
			PDEBUG(4, "VIDIOCGPICT: depth=%d, palette=%d", p->depth,
			       p->palette);
			p->brightness = spca50x->funct.get_bright(spca50x);
			p->contrast = spca50x->funct.get_contrast(spca50x);
			p->colour = spca50x->funct.get_colors(spca50x);
			p->hue = 0;
			p->whiteness = 0;
			return 0;
		}
	case VIDIOCSPICT:
		{
			int i;
			struct video_picture *p = arg;
			PDEBUG(4, "VIDIOCSPICT");
			if (spca5xx_testPalSize
			    (spca50x, p->palette, spca50x->width,
			     spca50x->height) < 0)
				return -EINVAL;
			if (spca50x->format != p->palette) {
				PDEBUG(4, "Setting depth=%d, palette=%d",
				       p->depth, p->palette);
/* change the output palette the input stream is the same */
/* no need to stop the camera streaming and restart */
				for (i = 0; i < SPCA50X_NUMFRAMES; i++) {
					spca50x->frame[i].depth = p->depth;
					spca50x->frame[i].format = p->palette;
				}
				spca50x->format = p->palette;
			}
			spca50x->contrast = p->contrast;
			spca50x->brightness = p->brightness;
			spca50x->colour = p->colour;
			spca50x->funct.set_bright(spca50x);
			spca50x->funct.set_contrast(spca50x);
			spca50x->funct.set_colors(spca50x);
			spca50x->hue = p->hue;
			spca50x->whiteness = p->whiteness;
			return 0;
		}
	case VIDIOCGCAPTURE:
		{
			int *vf = arg;
			PDEBUG(4, "VIDIOCGCAPTURE");
			*vf = 0;
// no subcapture
			return -EINVAL;
		}
	case VIDIOCSCAPTURE:
		{
			struct video_capture *vc = arg;
			if (vc->flags)
				return -EINVAL;
			if (vc->decimation)
				return -EINVAL;
			return -EINVAL;
		}
	case VIDIOCSWIN:
		{
			int result;
			struct video_window *vw = arg;
			PDEBUG(3, "VIDIOCSWIN: width=%d, height=%d, flags=%d",
			       vw->width, vw->height, vw->flags);
			if (spca5xx_testPalSize
			    (spca50x, spca50x->format, vw->width,
			     vw->height) < 0)
				return -EINVAL;
			if (vw->x)
				return -EINVAL;
			if (vw->y)
				return -EINVAL;
			if (vw->width > (unsigned int) spca50x->maxwidth)
				return -EINVAL;
			if (vw->height > (unsigned int) spca50x->maxheight)
				return -EINVAL;
			if (vw->width < (unsigned int) spca50x->minwidth)
				return -EINVAL;
			if (vw->height < (unsigned int) spca50x->minheight)
				return -EINVAL;
			result =
			    spca5xx_restartMode(spca50x, vw->width, vw->height,
						spca50x->frame[0].format);
			if (result == 0) {
				spca50x->frame[0].width = vw->width;
				spca50x->frame[0].height = vw->height;
			}
			return result;
		}
	case VIDIOCGWIN:
		{
			struct video_window *vw = arg;
			memset(vw, 0, sizeof (struct video_window));
			vw->x = 0;
			vw->y = 0;
			vw->width = spca50x->frame[0].width;
			vw->height = spca50x->frame[0].height;
			vw->flags = 0;
			PDEBUG(4, "VIDIOCGWIN: %dx%d", vw->width, vw->height);
			return 0;
		}
	case VIDIOCGMBUF:
		{
			struct video_mbuf *vm = arg;
			int i;
			PDEBUG(2, "VIDIOCGMBUF: %p ", vm);
			memset(vm, 0, sizeof (struct video_mbuf));
			vm->size = SPCA50X_NUMFRAMES * MAX_DATA_SIZE;
			vm->frames = SPCA50X_NUMFRAMES;
			for (i = 0; i < SPCA50X_NUMFRAMES; i++) {
				vm->offsets[i] = MAX_DATA_SIZE * i;
			}
			return 0;
		}
	case VIDIOCMCAPTURE:
		{
			int ret, depth;
			struct video_mmap *vm = arg;
			PDEBUG(4, "CMCAPTURE");
			PDEBUG(4, "CM frame: %d, size: %dx%d, format: %d",
			       vm->frame, vm->width, vm->height, vm->format);
			depth = spca5xx_get_depth(spca50x, vm->format);
			if (!depth) {
				err("VIDIOCMCAPTURE: invalid format (%d)",
				    vm->format);
				return -EINVAL;
			}
			if ((vm->frame < 0) || (vm->frame > 3)) {
				err("VIDIOCMCAPTURE: invalid frame (%d)",
				    vm->frame);
				return -EINVAL;
			}
			if (vm->width > spca50x->maxwidth
			    || vm->height > spca50x->maxheight) {
				err("VIDIOCMCAPTURE: requested dimensions too big");
				return -EINVAL;
			}
			if (vm->width < spca50x->minwidth
			    || vm->height < spca50x->minheight) {
				err("VIDIOCMCAPTURE: requested dimensions too small");
				return -EINVAL;
			}
			if (spca5xx_testPalSize
			    (spca50x, vm->format, vm->width, vm->height) < 0)
				return -EINVAL;
			if ((spca50x->frame[vm->frame].width != vm->width) ||
			    (spca50x->frame[vm->frame].height != vm->height) ||
			    (spca50x->frame[vm->frame].format != vm->format)) {
				ret =
				    spca5xx_restartMode(spca50x, vm->width,
							vm->height, vm->format);
				if (ret < 0)
					return ret;
				spca50x->frame[vm->frame].width = vm->width;
				spca50x->frame[vm->frame].height = vm->height;
				spca50x->frame[vm->frame].format = vm->format;
				spca50x->frame[vm->frame].depth = depth;
			}
			if (spca50x->autoexpo) {
/* set the autoexpo here exept vimicro */
				if (spca50x->cameratype != JPGH)
					spca50x->funct.set_autobright(spca50x);
			}
#ifdef GSPCA_ENABLE_REGISTERPLAY
			__u8 Rval = 0;
			if (RegStrobe != 0) {
				if (RegStrobe == 1) {
					if (spca50x->bridge == BRIDGE_PAC207) {
						pac207_RegWrite(spca50x);
					} else {
						Rval = RegValue & 0xFF;
						spca5xxRegWrite(spca50x->dev,
								0xa0, Rval,
								(__u16)
								(RegAddress &
								 0xFFFF), NULL,
								0);
					}
				} else {
					if (spca50x->bridge == BRIDGE_PAC207) {
						pac207_RegRead(spca50x);
					} else {
						spca5xxRegRead(spca50x->dev, 0xa1, 0x01, (__u16) (RegAddress & 0xFFFF), &Rval, 1);	// read Lowbyte
						RegValue = Rval;
					}
				}
				RegStrobe = 0;
			}
#endif				/* SPCA5XX_ENABLE_REGISTERPLAY */
/* Mark it as ready */
			spca50x->frame[vm->frame].grabstate = FRAME_READY;
			return 0;
		}
	case VIDIOCSYNC:
		{
			int ret;
			unsigned int frame = *((unsigned int *) arg);
			PDEBUG(4, "syncing to frame %d, grabstate = %d", frame,
			       spca50x->frame[frame].grabstate);
			switch (spca50x->frame[frame].grabstate) {
			case FRAME_UNUSED:
				return -EINVAL;
			case FRAME_ABORTING:
				return -ENODEV;
			case FRAME_READY:
			case FRAME_GRABBING:
			case FRAME_ERROR:
			      redo:
				if (!spca50x->dev)
					return -EIO;
				ret =
				    wait_event_interruptible(spca50x->
							     frame[frame].wq,
							     (spca50x->
							      frame[frame].
							      grabstate ==
							      FRAME_DONE));
				if (ret)
					return -EINTR;
				// ?????
				PDEBUG(4,
				       "Synch Ready on frame %d, grabstate = %d",
				       frame, spca50x->frame[frame].grabstate);
				if (spca50x->frame[frame].grabstate ==
				    FRAME_ERROR) {
					goto redo;
				}
/* Fallthrough.
* We have waited in state FRAME_GRABBING until it
* becomes FRAME_DONE, so now we can move along.
*/
			case FRAME_DONE:
/* Release the current frame. This means that it
* will be reused as soon as all other frames are
* full, so the app better be done with it quickly.
* Can this be avoided somehow?
*/
				spca50x->frame[frame].grabstate = FRAME_UNUSED;
				PDEBUG(4, "Release frame %d state %d\n", frame,
				       spca50x->frame[frame].grabstate);
				break;
			}	/* end switch */
			return 0;
		}
	case VIDIOCGFBUF:
		{
			struct video_buffer *vb = arg;
			memset(vb, 0, sizeof (struct video_buffer));
			vb->base = NULL;	/* frame buffer not supported, not used */
			return 0;
		}
	case SPCAGVIDIOPARAM:
		{
			struct video_param *vp = arg;
			vp->autobright = (__u8) spca50x->autoexpo;
			vp->quality = (__u8) spca50x->qindex;
			vp->time_interval = (__u16) spca50x->dtimes;
			vp->light_freq = (__u8) spca50x->light_freq;
			return 0;
		}
	case SPCASVIDIOPARAM:
		{
			struct video_param *vp = arg;
			switch (vp->chg_para) {
			case CHGABRIGHT:
				spca5xx_chgAuto(spca50x, vp->autobright);
				break;
			case CHGQUALITY:
				spca5xx_chgQtable(spca50x, vp->quality);
				break;
			case CHGTINTER:
				spca5xx_chgDtimes(spca50x, vp->time_interval);
				break;
			case CHGLIGHTFREQ:
				spca5xx_set_light_freq(spca50x, vp->light_freq);
				break;
			default:
				return -EINVAL;
				break;
			}
			return 0;
		}
/************************************/
	case VIDIOCKEY:
		return 0;
	case VIDIOCCAPTURE:
		return -EINVAL;
	case VIDIOCSFBUF:
		return -EINVAL;
	case VIDIOCGTUNER:
	case VIDIOCSTUNER:
		return -EINVAL;
	case VIDIOCGFREQ:
	case VIDIOCSFREQ:
		return -EINVAL;
	case VIDIOCGAUDIO:
	case VIDIOCSAUDIO:
		return -EINVAL;
	default:
		return -ENOIOCTLCMD;
	}			/* end switch */
	return 0;
}
static int
spca5xx_ioctl(struct inode *inode, struct file *file, unsigned int cmd,
	      unsigned long arg)
{
	int rc;
	rc = video_usercopy(inode, file, cmd, arg, spca5xx_do_ioctl);
	return rc;
}

#define ISDONE4(fr1,fr2,fr3,fr4) (((fr1|fr2|fr3|fr4) & FRAME_DONE ) ? 1:0)
#define ISDONE2(fr1,fr2) (((fr1|fr2) & FRAME_DONE) ? 1:0)
static ssize_t
spca5xx_read(struct file *file, char *buf, size_t cnt, loff_t * ppos)
{
	struct video_device *dev = file->private_data;
	int noblock = file->f_flags & O_NONBLOCK;
	unsigned long count = cnt;
	struct usb_spca50x *spca50x = video_get_drvdata(dev);
	int i;
	int frmx = -1;
	int rc;
	volatile struct spca50x_frame *frame;
	PDEBUG(4, "%ld bytes, noblock=%d", count, noblock);
	if (down_interruptible(&spca50x->lock))
		return -ERESTARTSYS;
	if (!dev || !buf) {
		up(&spca50x->lock);
		return -EFAULT;
	}
	if (!spca50x->dev) {
		up(&spca50x->lock);
		return -EIO;
	}
	if (!spca50x->streaming) {
		up(&spca50x->lock);
		return -EIO;
	}
/* Wait while we're grabbing the image */
	PDEBUG(4, "Waiting for a frame done");
#if (SPCA50X_NUMFRAMES == 4)
	if (noblock
	    && !ISDONE4(spca50x->frame[0].grabstate,
			spca50x->frame[1].grabstate,
			spca50x->frame[2].grabstate,
			spca50x->frame[3].grabstate)) {
		up(&spca50x->lock);
		return -EAGAIN;
	}
	if ((rc =
	     wait_event_interruptible(spca50x->wq,
				      ISDONE4(spca50x->frame[0].grabstate,
					      spca50x->frame[1].grabstate,
					      spca50x->frame[2].grabstate,
					      spca50x->frame[3].grabstate)))) {
		up(&spca50x->lock);
		return rc;
	}
#else				// should be two
	if (noblock
	    && !ISDONE2(spca50x->frame[0].grabstate,
			spca50x->frame[1].grabstate)) {
		up(&spca50x->lock);
		return -EAGAIN;
	}
	if ((rc =
	     wait_event_interruptible(spca50x->wq,
				      ISDONE2(spca50x->frame[0].grabstate,
					      spca50x->frame[1].grabstate)))) {
		up(&spca50x->lock);
		return rc;
	}
#endif
/* One frame has just been set to DONE. Find it. */
	for (i = 0; i < SPCA50X_NUMFRAMES; i++)
		if (spca50x->frame[i].grabstate == FRAME_DONE)
			frmx = i;
	PDEBUG(4, "Frame number: %d", frmx);
	if (frmx < 0) {
/* We havent found a frame that is DONE. Damn. Should
* not happen. */
		PDEBUG(2, "Couldnt find a frame ready to be read.");
		up(&spca50x->lock);
		return -EFAULT;
	}
	frame = &spca50x->frame[frmx];
	if (count > frame->scanlength)
		count = frame->scanlength;
	if ((i = copy_to_user(buf, frame->data, count))) {
		PDEBUG(2, "Copy failed! %d bytes not copied", i);
		up(&spca50x->lock);
		return -EFAULT;
	}
/* Release the frame */
	frame->grabstate = FRAME_READY;
/* set the autoexpo here */
	if (spca50x->autoexpo) {
/* set the autoexpo here exept vimicro*/
		if (spca50x->cameratype != JPGH)
			spca50x->funct.set_autobright(spca50x);
	}
	up(&spca50x->lock);
	return count;
}
static int
spca5xx_mmap(struct file *file, struct vm_area_struct *vma)
{
	struct video_device *dev = file->private_data;
	unsigned long start = vma->vm_start;
	unsigned long size = vma->vm_end - vma->vm_start;
	struct usb_spca50x *spca50x = video_get_drvdata(dev);
	unsigned long page, pos;
	if (spca50x->dev == NULL)
		return -EIO;
	PDEBUG(4, "mmap: %ld (%lX) bytes", size, size);
	if (size >
	    (((SPCA50X_NUMFRAMES * MAX_DATA_SIZE) + PAGE_SIZE -
	      1) & ~(PAGE_SIZE - 1)))
		return -EINVAL;
	if (down_interruptible(&spca50x->lock))
		return -EINTR;
	pos = (unsigned long) spca50x->fbuf;
	while (size > 0) {
		page = kvirt_to_pa(pos);
		if (remap_pfn_range
		    (vma, start, page >> PAGE_SHIFT, PAGE_SIZE, PAGE_SHARED)) {
			up(&spca50x->lock);
			return -EAGAIN;
		}
		start += PAGE_SIZE;
		pos += PAGE_SIZE;
		if (size > PAGE_SIZE)
			size -= PAGE_SIZE;
		else
			size = 0;
	}
	up(&spca50x->lock);
	return 0;
}
static struct file_operations spca5xx_fops = {
	.owner = THIS_MODULE,
	.open = spca5xx_open,
	.release = spca5xx_close,
	.read = spca5xx_read,
	.mmap = spca5xx_mmap,
	.ioctl = spca5xx_ioctl,
	.llseek = no_llseek,
};
static struct video_device spca50x_template = {
	.owner = THIS_MODULE,
	.name = "GSPCA USB Camera",
	.type = VID_TYPE_CAPTURE,
	.hardware = VID_HARDWARE_GSPCA,
	.fops = &spca5xx_fops,
	.release = video_device_release,
	.minor = -1,
};

/****************************************************************************
*
* SPCA50X configuration
*
***************************************************************************/
static int
spca50x_configure_sensor(struct usb_spca50x *spca50x)
{
	return spca5xx_getcapability(spca50x);;
}
static int
spca50x_configure(struct usb_spca50x *spca50x)
{
	PDEBUG(2, "video_register_device succeeded");
/* Initialise the camera bridge */
	if (spca50x->funct.configure(spca50x) < 0)
		goto error;
	gspca_set_alt0(spca50x);
/* Set an initial pipe size; this will be overridden by
* spca50x_set_mode(), called indirectly by the open routine.
*/
	if (spca5xx_getDefaultMode(spca50x) < 0)
		return -EINVAL;
	spca50x->force_rgb = force_rgb;
	if (spca50x_configure_sensor(spca50x) < 0) {
		err("failed to configure");
		goto error;
	}
/* configure the frame detector with default parameters */
	spca5xx_setFrameDecoder(spca50x);
	PDEBUG(2, "Spca5xx Configure done !!");
	return 0;
      error:
	return -EBUSY;
}

/************************************************************************************/
/****************************************************************************
*  sysfs
***************************************************************************/
static inline struct usb_spca50x *
cd_to_spca50x(struct class_device *cd)
{
	struct video_device *vdev = to_video_device(cd);
	return video_get_drvdata(vdev);
}

static ssize_t
show_stream_id(struct class_device *cd, char *buf)
{
	struct usb_spca50x *spca50x = cd_to_spca50x(cd);
	return snprintf(buf, 5, "%s\n", Plist[spca50x->cameratype].name);
}

static CLASS_DEVICE_ATTR(stream_id, S_IRUGO, show_stream_id, NULL);
static ssize_t
show_model(struct class_device *cd, char *buf)
{
	struct usb_spca50x *spca50x = cd_to_spca50x(cd);
	return snprintf(buf, 32, "%s\n", (spca50x->desc) ?
			clist[spca50x->desc].description : " Unknow ");
}

static CLASS_DEVICE_ATTR(model, S_IRUGO, show_model, NULL);
static ssize_t
show_pictsetting(struct class_device *cd, char *buf)
{
	struct usb_spca50x *spca50x = cd_to_spca50x(cd);
	struct pictparam *gcorrect = &spca50x->pictsetting;
	return snprintf(buf, 128,
			"force_rgb=%d, gamma=%d, OffRed=%d, OffBlue=%d, OffGreen=%d, GRed=%d, GBlue=%d, GGreen= %d \n",
			gcorrect->force_rgb, gcorrect->gamma, gcorrect->OffRed,
			gcorrect->OffBlue, gcorrect->OffGreen, gcorrect->GRed,
			gcorrect->GBlue, gcorrect->GGreen);
}

static CLASS_DEVICE_ATTR(pictsetting, S_IRUGO, show_pictsetting, NULL);
static void
spca50x_create_sysfs(struct video_device *vdev)
{
	video_device_create_file(vdev, &class_device_attr_stream_id);
	video_device_create_file(vdev, &class_device_attr_model);
	video_device_create_file(vdev, &class_device_attr_pictsetting);
}

/****************************************************************************
*
*  USB routines
*
***************************************************************************/
static int
gspca_attach_bridge(struct usb_spca50x *spca50x)
{
/* set the default epadr */
	spca50x->epadr =1;
	switch (spca50x->bridge) {
	case BRIDGE_SPCA500:
		spca50x->cameratype = JPEG;
		info("USB SPCA5XX camera found.(SPCA500+unknown CCD)");
		memcpy(&spca50x->funct, &fspca500,
		       sizeof (struct cam_operation));
		break;
	case BRIDGE_SPCA501:
		spca50x->i2c_ctrl_reg = SPCA50X_REG_I2C_CTRL;
		spca50x->i2c_base = 0;
		spca50x->i2c_trigger_on_write = 0;
		spca50x->cameratype = YUYV;
		info("USB SPCA5XX camera found. (SPCA501 )");
		memcpy(&spca50x->funct, &fspca501,
		       sizeof (struct cam_operation));
		break;
	case BRIDGE_SPCA505:
		spca50x->i2c_ctrl_reg = SPCA50X_REG_I2C_CTRL;
		spca50x->i2c_base = 0;
		spca50x->i2c_trigger_on_write = 0;
		spca50x->cameratype = YYUV;
		info("USB SPCA5XX camera found.(SPCA505)");
		memcpy(&spca50x->funct, &fspca505,
		       sizeof (struct cam_operation));
		break;
	case BRIDGE_SPCA506:
		spca50x->i2c_ctrl_reg = SPCA50X_REG_I2C_CTRL;
		spca50x->i2c_base = 0;
		spca50x->i2c_trigger_on_write = 0;
		spca50x->cameratype = YYUV;
		info("USB SPCA5XX grabber found. (SPCA506+SAA7113)");
		memcpy(&spca50x->funct, &fspca506,
		       sizeof (struct cam_operation));
		break;
	case BRIDGE_SPCA508:
		spca50x->i2c_ctrl_reg = 0;
		spca50x->i2c_base = SPCA508_INDEX_I2C_BASE;
		spca50x->i2c_trigger_on_write = 1;
		spca50x->cameratype = YUVY;
		info("USB SPCA5XX camera found.(SPCA508?)");
		memcpy(&spca50x->funct, &fspca508,
		       sizeof (struct cam_operation));
		break;
	case BRIDGE_SPCA561:
		spca50x->cameratype = S561;
		info("USB SPCA5XX camera found.(SPCA561A)");
		memcpy(&spca50x->funct, &fspca561,
		       sizeof (struct cam_operation));
		break;
	case BRIDGE_SPCA533:
	case BRIDGE_SPCA536:
	case BRIDGE_SPCA504:
	case BRIDGE_SPCA504B:
	case BRIDGE_SPCA504C:
		spca50x->cameratype = JPEG;
		info("USB SPCA5XX camera found.Sunplus FW 2");
		memcpy(&spca50x->funct, &fsp5xxfw2,
		       sizeof (struct cam_operation));
		break;
	case BRIDGE_ZC3XX:
		spca50x->cameratype = JPGH;
		info("USB SPCA5XX camera found.(ZC3XX) ");
		memcpy(&spca50x->funct, &fzc3xx, sizeof (struct cam_operation));
		break;
	case BRIDGE_VC032X:
	spca50x->epadr = 2;
		spca50x->cameratype = YUY2;
		info("USB SPCA5XX camera found.(VC0321) ");
		memcpy(&spca50x->funct, &fvc0321, sizeof (struct cam_operation));
		break;
	case BRIDGE_SONIX:
		spca50x->cameratype = SN9C;
		info("USB SPCA5XX camera found. SONIX sn9c10[1 2]");
		memcpy(&spca50x->funct, &fsonix, sizeof (struct cam_operation));
		break;
	case BRIDGE_SN9CXXX:
		spca50x->cameratype = JPGS;	// jpeg 4.2.2 whithout header ;
		info("USB SPCA5XX camera found. SONIX JPEG (sn9c1xx) ");
		memcpy(&spca50x->funct, &fsn9cxx,
		       sizeof (struct cam_operation));
		break;
	case BRIDGE_PAC207:
	spca50x->epadr = 5;
		spca50x->cameratype = PGBRG;
		info("USB SPCA5XX camera found. (PAC207)");
		memcpy(&spca50x->funct, &fpac207,
		       sizeof (struct cam_operation));
		break;
	case BRIDGE_TV8532:
		spca50x->cameratype = GBGR;
		info("USB SPCA5xx camera found. (TV8532)");
		memcpy(&spca50x->funct, &ftv8532,
		       sizeof (struct cam_operation));
		break;
	case BRIDGE_ETOMS:
		spca50x->cameratype = GBRG;
		info("USB SPCA5XX camera found (ET61X51) ");
		memcpy(&spca50x->funct, &fet61x, sizeof (struct cam_operation));
		break;
	case BRIDGE_CX11646:
		spca50x->cameratype = JPGC;
		info("USB SPCA5XX camera found. Conexant(CX11646) ");
		memcpy(&spca50x->funct, &fcx11646,
		       sizeof (struct cam_operation));
		break;
	case BRIDGE_MR97311:
		spca50x->cameratype = JPGM;
		info("USB SPCA5XX camera found. PIXART MR97311 ");
		memcpy(&spca50x->funct, &fmr97311,
		       sizeof (struct cam_operation));
		break;
	default:
		return -ENODEV;
	}
	return 0;
}
static int
spcaDetectCamera(struct usb_spca50x *spca50x)
{
	struct usb_device *dev = spca50x->dev;
	__u8 fw = 0;
	__u16 vendor;
	__u16 product;
/* Is it a recognised camera ? */
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,11)
	vendor = le16_to_cpu(dev->descriptor.idVendor);
	product = le16_to_cpu(dev->descriptor.idProduct);
#else
	vendor = dev->descriptor.idVendor;
	product = dev->descriptor.idProduct;
#endif
	switch (vendor) {
	case 0x0733:		/* Rebadged ViewQuest (Intel) and ViewQuest cameras */
		switch (product) {
		case 0x430:
			if (usbgrabber) {
				spca50x->desc = UsbGrabberPV321c;
				spca50x->bridge = BRIDGE_SPCA506;
				spca50x->sensor = SENSOR_SAA7113;
			} else {
				spca50x->desc = IntelPCCameraPro;
				spca50x->bridge = BRIDGE_SPCA505;
				spca50x->sensor = SENSOR_INTERNAL;;
			}
			break;
		case 0x1314:
			spca50x->desc = Mercury21;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x2211:
			spca50x->desc = Jenoptikjdc21lcd;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x2221:
			spca50x->desc = MercuryDigital;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x1311:
			spca50x->desc = Epsilon13;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x401:
			spca50x->desc = IntelCreateAndShare;
			spca50x->bridge = BRIDGE_SPCA501;	
			spca50x->sensor = SENSOR_INTERNAL;;
			break;
		case 0x402:
			spca50x->desc = ViewQuestM318B;
			spca50x->bridge = BRIDGE_SPCA501;	
			spca50x->sensor = SENSOR_INTERNAL;;
			break;
		case 0x110:
			spca50x->desc = ViewQuestVQ110;
			spca50x->bridge = BRIDGE_SPCA508;
			spca50x->sensor = SENSOR_INTERNAL;;
			break;
		case 0x3261:
			spca50x->desc = Concord3045;
			spca50x->bridge = BRIDGE_SPCA536;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x3281:
			spca50x->desc = CyberpixS550V;
			spca50x->bridge = BRIDGE_SPCA536;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x0734:
		switch (product) {
		case 0x043b:
			spca50x->desc = DeMonUSBCapture;
			spca50x->bridge = BRIDGE_SPCA506;
			spca50x->sensor = SENSOR_SAA7113;
			break;
		default:
			goto error;
		};
		break;
	case 0x99FA:		/* GrandTec cameras */
		switch (product) {
		case 0x8988:
			spca50x->desc = GrandtecVcap;
			spca50x->bridge = BRIDGE_SPCA506;
			spca50x->sensor = SENSOR_SAA7113;
			break;
		default:
			goto error;
		};
		break;
	case 0x0AF9:		/* Hama cameras */
		switch (product) {
		case 0x0010:
			spca50x->desc = HamaUSBSightcam;
			spca50x->bridge = BRIDGE_SPCA508;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0011:
			spca50x->desc = HamaUSBSightcam2;
			spca50x->bridge = BRIDGE_SPCA508;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x040A:		/* Kodak cameras */
		switch (product) {
		case 0x0002:
			spca50x->desc = KodakDVC325;
			spca50x->bridge = BRIDGE_SPCA501;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0300:
			spca50x->desc = KodakEZ200;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x04a5:		/* Benq */
	case 0x08ca:		/* Aiptek */
	case 0x055f:		/* Mustek cameras */
	case 0x04fc:		/* SunPlus */
	case 0x052b:		/* ?? Megapix */
	case 0x04f1:		/* JVC */
		switch (product) {
		case 0xc520:
			spca50x->desc = MustekGsmartMini3;
			spca50x->bridge = BRIDGE_SPCA504;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc420:
			spca50x->desc = MustekGsmartMini2;
			spca50x->bridge = BRIDGE_SPCA504;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc360:
			spca50x->desc = MustekDV4000;
			spca50x->bridge = BRIDGE_SPCA536;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc211:
			spca50x->desc = Bs888e;
			spca50x->bridge = BRIDGE_SPCA536;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc005:	// zc302 chips 
			spca50x->desc = Wcam300A;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0xd003:	// zc302 chips 
			spca50x->desc = MustekWcam300A;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0xd004:	// zc302 chips 
			spca50x->desc = WCam300AN;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0x504a:
/*try to get the firmware as some cam answer 2.0.1.2.2 
and should be a spca504b then overwrite that setting */
			spca5xxRegRead(dev, 0x20, 0, 0, &fw, 1);
			if (fw == 1) {
				spca50x->desc = AiptekMiniPenCam13;
				spca50x->bridge = BRIDGE_SPCA504;
				spca50x->sensor = SENSOR_INTERNAL;
			} else if (fw == 2) {
				spca50x->desc = Terratec2move13;
				spca50x->bridge = BRIDGE_SPCA504B;
				spca50x->sensor = SENSOR_INTERNAL;
			} else
				return -ENODEV;
			break;
		case 0x2018:
			spca50x->desc = AiptekPenCamSD;
			spca50x->bridge = BRIDGE_SPCA504B;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x1001:
			spca50x->desc = JvcGcA50;
			spca50x->bridge = BRIDGE_SPCA504B;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x2008:
			spca50x->desc = AiptekMiniPenCam2;
			spca50x->bridge = BRIDGE_SPCA504B;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x504b:
			spca50x->desc = MaxellMaxPocket;
			spca50x->bridge = BRIDGE_SPCA504B;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x500c:
			spca50x->desc = Sunplus500c;
			spca50x->bridge = BRIDGE_SPCA504B;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xffff:
			spca50x->desc = PureDigitalDakota;
			spca50x->bridge = BRIDGE_SPCA504B;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0103:
			spca50x->desc = AiptekPocketDV;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0104:
			spca50x->desc = AiptekPocketDVII;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0106:
			spca50x->desc = AiptekPocketDV3100;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc232:
			spca50x->desc = MustekMDC3500;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc630:
			spca50x->desc = MustekMDC4000;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x5330:
			spca50x->desc = Digitrex2110;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x2020:
			spca50x->desc = AiptekSlim3000F;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x2022:
			spca50x->desc = AiptekSlim3200;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x2028:
			spca50x->desc = AiptekPocketCam4M;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x5360:
			spca50x->desc = SunplusGeneric536;
			spca50x->bridge = BRIDGE_SPCA536;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x2024:
			spca50x->desc = AiptekDV3500;
			spca50x->bridge = BRIDGE_SPCA536;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x2042:
			spca50x->desc = AiptekPocketDV5100;
			spca50x->bridge = BRIDGE_SPCA536;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x2040:
			spca50x->desc = AiptekDV4100M;
			spca50x->bridge = BRIDGE_SPCA536;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x2060:
			spca50x->desc = AiptekPocketDV5300;
			spca50x->bridge = BRIDGE_SPCA536;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x3008:
			spca50x->desc = BenqDC1500;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x3003:
			spca50x->desc = BenqDC1300;
			spca50x->bridge = BRIDGE_SPCA504B;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x300a:
			spca50x->desc = BenqDC3410;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x300c:
			spca50x->desc = BenqDC1016;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x2010:
			spca50x->desc = AiptekPocketCam3M;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x2016:
			spca50x->desc = AiptekPocketCam2M;
			spca50x->bridge = BRIDGE_SPCA504B;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0561:
			spca50x->desc = Flexcam100Camera;
			spca50x->bridge = BRIDGE_SPCA561;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc200:
			spca50x->desc = MustekGsmart300;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x7333:
			spca50x->desc = PalmPixDC85;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc220:
			spca50x->desc = Gsmartmini;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc230:
			spca50x->desc = Mustek330K;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc530:
			spca50x->desc = MustekGsmartLCD3;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc430:
			spca50x->desc = MustekGsmartLCD2;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc440:
			spca50x->desc = MustekDV3000;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc540:
			spca50x->desc = GsmartD30;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0xc650:
			spca50x->desc = MustekMDC5500Z;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x1513:
			spca50x->desc = MegapixV4;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x046d:		/* Logitech Labtec */
	case 0x041E:		/* Creative cameras */
		switch (product) {
		case 0x400A:
			spca50x->desc = CreativePCCam300;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x4012:
			spca50x->desc = PcCam350;
			spca50x->bridge = BRIDGE_SPCA504C;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0890:
			spca50x->desc = LogitechTraveler;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x08a0:
			spca50x->desc = QCim;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0x08a1:
			spca50x->desc = QCimA1;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0x08a2:	// zc302 chips 
			spca50x->desc = LabtecPro;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_HDCS2020;
			break;
		case 0x08a3:
			spca50x->desc = QCchat;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0x08a6:
			spca50x->desc = LogitechQCim;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_HV7131C;
			break;
		case 0x08a7:
			spca50x->desc = LogitechQCImage;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_PAS202;
			break;
		case 0x08d8:
		case 0x08a9:
			spca50x->desc = LogitechNotebookDeluxe;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_HDCS2020;
			break;
		case 0x08ae:
			spca50x->desc = QuickCamNB;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_HDCS2020;
			break;
		case 0x08ac:
			spca50x->desc = LogitechQCCool;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_HV7131B;
			break;
		case 0x08ad:
		case 0x08d7:
			spca50x->desc = LogitechQCCommunicateSTX;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_HV7131C;
			break;
		case 0x08aa:
			spca50x->desc = LabtecNotebook;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_HDCS2020;
			break;
		case 0x08b9:
			spca50x->desc = QCimB9;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0x08d9:
			spca50x->desc = QCimconnect;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0x08da:
			spca50x->desc = QCmessenger;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0x0900:
			spca50x->desc = LogitechClickSmart310;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_HDCS1020;
			break;
		case 0x0901:
			spca50x->desc = LogitechClickSmart510;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0905:
			spca50x->desc = LogitechClickSmart820;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x400B:
			spca50x->desc = CreativePCCam600;
			spca50x->bridge = BRIDGE_SPCA504C;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x4013:
			spca50x->desc = CreativePccam750;
			spca50x->bridge = BRIDGE_SPCA504C;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0960:
			spca50x->desc = LogitechClickSmart420;
			spca50x->bridge = BRIDGE_SPCA504C;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x4018:
			spca50x->desc = CreativeVista;
			spca50x->bridge = BRIDGE_SPCA508;
			spca50x->sensor = SENSOR_PB100_BA;
			break;
		case 0x4028:
			spca50x->desc = CreativeVistaPlus;
			spca50x->bridge = BRIDGE_PAC207;
			spca50x->sensor = SENSOR_PAC207;
			break;
		case 0x401d:	//here505b
			spca50x->desc = Nxultra;
			spca50x->bridge = BRIDGE_SPCA505;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x401c:	// zc301 chips 
			spca50x->desc = CreativeNX;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_PAS106;
			break;
		case 0x401e:	// zc301 chips 
			spca50x->desc = CreativeNxPro;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_HV7131B;
			break;
		case 0x4029:
			spca50x->desc = CreativeWebCamVistaPro;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_PB0330;
			break;
		case 0x4034:	// zc301 chips 
			spca50x->desc = CreativeInstant1;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_PAS106;
			break;
		case 0x4035:	// zc301 chips 
			spca50x->desc = CreativeInstant2;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_PAS106;
			break;
		case 0x403a:
			spca50x->desc = CreativeNxPro2;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0x403b:
			spca50x->desc = CreativeVista3b;
			spca50x->bridge = BRIDGE_SPCA561;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x041e:
		case 0x4036:
			spca50x->desc = CreativeLive;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0x401f:	// zc301 chips 
			spca50x->desc = CreativeNotebook;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0x4017:	// zc301 chips 
			spca50x->desc = CreativeMobile;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_ICM105A;
			break;
		case 0x4051:	// zc301 chips 
			spca50x->desc = CreativeLiveCamVideoIM;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130C_VF0250; // VF0250
			break;
		case 0x4053:	// zc301 chips 
			spca50x->desc = CreativeLiveCamNotebookPro;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130C_VF0250; // VF0250
			break;
		case 0x0920:
			spca50x->desc = QCExpress;
			spca50x->bridge = BRIDGE_TV8532;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0921:
			spca50x->desc = LabtecWebcam;
			spca50x->bridge = BRIDGE_TV8532;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0928:
			spca50x->desc = QCExpressEtch2;
			spca50x->bridge = BRIDGE_SPCA561;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0929:
			spca50x->desc = Labtec929;
			spca50x->bridge = BRIDGE_SPCA561;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x092a:
			spca50x->desc = QCforNotebook;
			spca50x->bridge = BRIDGE_SPCA561;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x092b:
			spca50x->desc = LabtecWCPlus;
			spca50x->bridge = BRIDGE_SPCA561;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x092c:
		case 0x092d:
		case 0x092e:
		case 0x092f:
			spca50x->desc = LogitechQC92x;
			spca50x->bridge = BRIDGE_SPCA561;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0892:
		case 0x0896:
			spca50x->desc = Orbicam;
			spca50x->bridge = BRIDGE_VC032X;
			spca50x->sensor = SENSOR_OV7660;	//overwrite by the sensor detect routine
			
		break;
		default:
			goto error;
		};
		break;
	case 0x0AC8:		/* Vimicro z-star */
		switch (product) {
		case 0x301b:	/* Wasam 350r */
			spca50x->desc = Vimicro;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_PB0330;	//overwrite by the sensor detect routine
			break;
		case 0x303b:	/* Wasam 350r */
			spca50x->desc = Vimicro303b;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_PB0330;	//overwrite by the sensor detect routine
			break;
		case 0x305b:	/* Generic */
			spca50x->desc = Zc0305b;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;	//overwrite by the sensor detect routine
			break;
		case 0x0302:	/* Generic */
			spca50x->desc = Zc302;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_ICM105A;	//overwrite by the sensor detect routine
			break;
		case 0x0321:
			spca50x->desc = Vimicro0321;
			spca50x->bridge = BRIDGE_VC032X;
			spca50x->sensor = SENSOR_OV7660;	//overwrite by the sensor detect routine
			break;
		case 0xc002:
			spca50x->desc = Sonyc002;
			spca50x->bridge = BRIDGE_VC032X;
			spca50x->sensor = SENSOR_OV7660;	//overwrite by the sensor detect routine
			break;
		default:
			goto error;
		};
		break;
	case 0x084D:		/* D-Link / Minton */
		switch (product) {
		case 0x0003:	/* DSC-350 / S-Cam F5 */
			spca50x->desc = DLinkDSC350;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x0923:		/* ICM532 cams */
		switch (product) {
		case 0x010f:
			spca50x->desc = ICM532cam;
			spca50x->bridge = BRIDGE_TV8532;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x0545:		/* tv8532 cams */
		switch (product) {
		case 0x808b:
			spca50x->desc = VeoStingray2;
			spca50x->bridge = BRIDGE_TV8532;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x8333:
			spca50x->desc = VeoStingray1;
			spca50x->bridge = BRIDGE_TV8532;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x102c:		/* Etoms */
		switch (product) {
		case 0x6151:
			spca50x->desc = Etoms61x151;
			spca50x->bridge = BRIDGE_ETOMS;
			spca50x->sensor = SENSOR_PAS106;
			break;
		case 0x6251:
			spca50x->desc = Etoms61x251;
			spca50x->bridge = BRIDGE_ETOMS;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		default:
			goto error;
		};
		break;
	case 0x1776:		/* Arowana */
		switch (product) {
		case 0x501c:	/* Arowana 300k CMOS Camera */
			spca50x->desc = Arowana300KCMOSCamera;
			spca50x->bridge = BRIDGE_SPCA501;
			spca50x->sensor = SENSOR_HV7131B;
			break;
		default:
			goto error;
		};
		break;
	case 0x0000:		/* Unknow Camera */
		switch (product) {
		case 0x0000:	/* UnKnow from Ori CMOS Camera */
			spca50x->desc = MystFromOriUnknownCamera;
			spca50x->bridge = BRIDGE_SPCA501;
			spca50x->sensor = SENSOR_HV7131B;
			break;
		default:
			goto error;
		};
		break;
	case 0x8086:		/* Intel */
		switch (product) {
		case 0x0110:
			spca50x->desc = IntelEasyPCCamera;
			spca50x->bridge = BRIDGE_SPCA508;
			spca50x->sensor = SENSOR_PB100_BA;
			break;
		case 0x0630:	/* Pocket PC Camera */
			spca50x->desc = IntelPocketPCCamera;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x0506:		/* 3COM cameras */
		switch (product) {
		case 0x00DF:
			spca50x->desc = ThreeComHomeConnectLite;
			spca50x->bridge = BRIDGE_SPCA501;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x0458:		/* Genius KYE cameras */
		switch (product) {
		case 0x7004:
			spca50x->desc = GeniusVideoCAMExpressV2;
			spca50x->bridge = BRIDGE_SPCA561;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x7006:
			spca50x->desc = GeniusDsc13;
			spca50x->bridge = BRIDGE_SPCA504B;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x7007:	// zc301 chips 
			spca50x->desc = GeniusVideoCamV2;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0x700c:	// zc301 chips 
			spca50x->desc = GeniusVideoCamV3;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		case 0x700f:	// zc301 chips 
			spca50x->desc = GeniusVideoCamExpressV2b;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		default:
			goto error;
		};
		break;
	case 0xabcd:		/* PetCam  */
		switch (product) {
		case 0xcdee:
			spca50x->desc = PetCam;
			spca50x->bridge = BRIDGE_SPCA561;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x060b:		/* Maxell  */
		switch (product) {
		case 0xa001:
			spca50x->desc = MaxellCompactPM3;
			spca50x->bridge = BRIDGE_SPCA561;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x10fd:		/* FlyCam usb 100  */
		switch (product) {
		case 0x7e50:
			spca50x->desc = Flycam100Camera;
			spca50x->bridge = BRIDGE_SPCA561;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x0128:
		case 0x8050:	// zc301 chips
			spca50x->desc = TyphoonWebshotIIUSB300k;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		default:
			goto error;
		};
		break;
	case 0x0461:		/* MicroInnovation  */
		switch (product) {
		case 0x0815:
			spca50x->desc = MicroInnovationIC200;
			spca50x->bridge = BRIDGE_SPCA508;
			spca50x->sensor = SENSOR_PB100_BA;
			break;
		case 0x0a00:	// zc301 chips 
			spca50x->desc = WebCam320;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			break;
		default:
			goto error;
		};
		break;
	case 0x06e1:		/* ADS Technologies  */
		switch (product) {
		case 0xa190:
			spca50x->desc = ADSInstantVCD;
			spca50x->bridge = BRIDGE_SPCA506;
			spca50x->sensor = SENSOR_SAA7113;
			break;
		default:
			goto error;
		};
		break;
	case 0x05da:		/* Digital Dream cameras */
		switch (product) {
		case 0x1018:
			spca50x->desc = Enigma13;
			spca50x->bridge = BRIDGE_SPCA504B;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x0c45:		/* Sonix6025 TAS 5130d1b */
		switch (product) {
		case 0x6001:
			spca50x->desc = GeniusVideoCamNB;
			spca50x->bridge = BRIDGE_SONIX;
			spca50x->sensor = SENSOR_TAS5110;
			spca50x->customid = SN9C102;
			spca50x->i2c_ctrl_reg = 0x20;
			spca50x->i2c_base = 0x11;
			break;
		case 0x6007:
		case 0x6005:
			spca50x->desc = SweexTas5110;
			spca50x->bridge = BRIDGE_SONIX;
			spca50x->sensor = SENSOR_TAS5110;
			spca50x->customid = SN9C101;
			spca50x->i2c_ctrl_reg = 0x20;
			spca50x->i2c_base = 0x11;
			break;
		case 0x6024:
		case 0x6025:
			spca50x->desc = Sonix6025;
			spca50x->bridge = BRIDGE_SONIX;
			spca50x->sensor = SENSOR_TAS5130CXX;
			spca50x->customid = SN9C102;
			spca50x->i2c_ctrl_reg = 0x20;
			spca50x->i2c_base = 0x11;
			break;
		case 0x6028:
			spca50x->desc = BtcPc380;
			spca50x->bridge = BRIDGE_SONIX;
			spca50x->sensor = SENSOR_PAS202;
			spca50x->customid = SN9C102;
			spca50x->i2c_ctrl_reg = 0x80;
			spca50x->i2c_base = 0x40;
			break;
		case 0x6019:
			spca50x->desc = Sonix6019;
			spca50x->bridge = BRIDGE_SONIX;
			spca50x->sensor = SENSOR_OV7630;
			spca50x->customid = SN9C101;
			spca50x->i2c_ctrl_reg = 0x80;
			spca50x->i2c_base = 0x21;
			break;
		case 0x602c:
		case 0x602e:
			spca50x->desc = GeniusVideoCamMessenger;
			spca50x->bridge = BRIDGE_SONIX;
			spca50x->sensor = SENSOR_OV7630;
			spca50x->customid = SN9C102;
			spca50x->i2c_ctrl_reg = 0x80;
			spca50x->i2c_base = 0x21;
			break;
		case 0x602d:
			spca50x->desc = Lic200;
			spca50x->bridge = BRIDGE_SONIX;
			spca50x->sensor = SENSOR_HV7131R;
			spca50x->customid = SN9C102;
			spca50x->i2c_ctrl_reg = 0x80;
			spca50x->i2c_base = 0x11;
			break;
		case 0x6009:
		case 0x600d:
		case 0x6029:
			spca50x->desc = Sonix6029;
			spca50x->bridge = BRIDGE_SONIX;
			spca50x->sensor = SENSOR_PAS106;
			spca50x->customid = SN9C101;
			spca50x->i2c_ctrl_reg = 0x81;
			spca50x->i2c_base = 0x40;
			break;
		case 0x6040:
			spca50x->desc = SpeedNVC350K;
			spca50x->bridge = BRIDGE_SN9CXXX;
			spca50x->sensor = SENSOR_HV7131R;
			spca50x->customid = SN9C102P;
			spca50x->i2c_ctrl_reg = 0x81;
			spca50x->i2c_base = 0x11;
			break;
		case 0x607c:
			spca50x->desc = SonixWC311P;
			spca50x->bridge = BRIDGE_SN9CXXX;
			spca50x->sensor = SENSOR_HV7131R;
			spca50x->customid = SN9C102P;
			spca50x->i2c_ctrl_reg = 0x81;
			spca50x->i2c_base = 0x11;
			break;
		case 0x612c:
			spca50x->desc = TyphoonEasyCam1_3;
			spca50x->bridge = BRIDGE_SN9CXXX;
			spca50x->sensor = SENSOR_MO4000;
			spca50x->customid = SN9C110;
			spca50x->i2c_ctrl_reg = 0x81;
			spca50x->i2c_base = 0x21;
			break;
		case 0x613b:
			spca50x->desc = Sonix0x613b;
			spca50x->bridge = BRIDGE_SN9CXXX;
			spca50x->sensor = SENSOR_OV7660;
			spca50x->customid = SN9C120;
			spca50x->i2c_ctrl_reg = 0x81;
			spca50x->i2c_base = 0x21;
			break;
		case 0x613c:
			spca50x->desc = Pccam168;
			spca50x->bridge = BRIDGE_SN9CXXX;
			spca50x->sensor = SENSOR_HV7131R;
			spca50x->customid = SN9C120;
			spca50x->i2c_ctrl_reg = 0x81;
			spca50x->i2c_base = 0x11;
			break;
		case 0x6130:
			spca50x->desc = Pccam;
			spca50x->bridge = BRIDGE_SN9CXXX;
			spca50x->sensor = SENSOR_MI0360;
			spca50x->customid = SN9C120;
			spca50x->i2c_ctrl_reg = 0x81;
			spca50x->i2c_base = 0x5d;
			break;
		case 0x60c0:
			spca50x->desc = Sn535;
			spca50x->bridge = BRIDGE_SN9CXXX;
			spca50x->sensor = SENSOR_MI0360;
			spca50x->customid = SN9C105;
			spca50x->i2c_ctrl_reg = 0x81;
			spca50x->i2c_base = 0x5d;
			break;
		case 0x60fb:
			spca50x->desc = Sonix0x60fb;
			spca50x->bridge = BRIDGE_SN9CXXX;
			spca50x->sensor = SENSOR_OV7660;
			spca50x->customid = SN9C105;
			spca50x->i2c_ctrl_reg = 0x81;
			spca50x->i2c_base = 0x21;
			break;
		case 0x60fc:
			spca50x->desc = Lic300;
			spca50x->bridge = BRIDGE_SN9CXXX;
			spca50x->sensor = SENSOR_HV7131R;
			spca50x->customid = SN9C105;
			spca50x->i2c_ctrl_reg = 0x81;
			spca50x->i2c_base = 0x11;
			break;
		default:
			goto error;
		};
		break;
	case 0x0546:		/* Polaroid */
		switch (product) {
		case 0x3273:
			spca50x->desc = PolaroidPDC2030;
			spca50x->bridge = BRIDGE_SPCA504B;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x3155:
			spca50x->desc = PolaroidPDC3070;
			spca50x->bridge = BRIDGE_SPCA533;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		case 0x3191:
			spca50x->desc = PolaroidIon80;
			spca50x->bridge = BRIDGE_SPCA504B;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x0572:		/* Connexant */
		switch (product) {
		case 0x0041:
			spca50x->desc = CreativeNoteBook2;
			spca50x->bridge = BRIDGE_CX11646;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x06be:		/* Optimedia */
		switch (product) {
		case 0x0800:
			spca50x->desc = Optimedia;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x2899:		/* ToptroIndustrial */
		switch (product) {
		case 0x012c:
			spca50x->desc = ToptroIndus;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x06bd:		/* Agfa Cl20 */
		switch (product) {
		case 0x0404:
			spca50x->desc = AgfaCl20;
			spca50x->bridge = BRIDGE_SPCA500;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x093a:		/* Mars-semi ~ Pixart */
		switch (product) {
		case 0x050f:
			spca50x->desc = Pcam;
			spca50x->bridge = BRIDGE_MR97311;
			spca50x->sensor = SENSOR_MI0360;
			break;
		case 0x2460:
			spca50x->desc = QtecWb100;
			spca50x->bridge = BRIDGE_PAC207;
			spca50x->sensor = SENSOR_PAC207;
			break;
		case 0x2468:
			spca50x->desc = PAC207;
			spca50x->bridge = BRIDGE_PAC207;
			spca50x->sensor = SENSOR_PAC207;
			break;
		case 0x2470:
			spca50x->desc = GeniusGF112;
			spca50x->bridge = BRIDGE_PAC207;
			spca50x->sensor = SENSOR_PAC207;
			break;
		case 0x2471:
			spca50x->desc = GeniusGe111;
			spca50x->bridge = BRIDGE_PAC207;
			spca50x->sensor = SENSOR_PAC207;
			break;
		default:
			goto error;
		};
		break;
	case 0x0497:		/* Smile International */
		switch (product) {
		case 0xc001:
// Modal NO. VA30UC2 8/nq h0 106250
// Hone-Tec Inc. VA30UC2
			spca50x->desc = SmileIntlCamera;
			spca50x->bridge = BRIDGE_SPCA501;
			spca50x->sensor = SENSOR_INTERNAL;
			break;
		default:
			goto error;
		};
		break;
	case 0x0698:		/* Chuntex (CTX) */
		switch (product) {
		case 0x2003:	/* The Webcam built in the CTX M730V TFT-Display, behind an USB-HUB */
			spca50x->desc = CTXM730VCam;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_ICM105A;	//overwrite by the sensor detect routine
			break;
		default:
			goto error;
		};
		break;
	case 0x0471:		/* Philips Product */
		switch (product) {
		case 0x0325:	/* Low cost Philips Webcam */
			spca50x->desc = PhilipsSPC200NC;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_PAS106;	//overwrite by the sensor detect routine
			break;
		case 0x0326:	/* Low cost Philips Webcam */
			spca50x->desc = PhilipsSPC300NC;
			spca50x->bridge = BRIDGE_ZC3XX;
			spca50x->sensor = SENSOR_PAS106;	//overwrite by the sensor detect routine
			break;
		case 0x0328:
			spca50x->desc = PhilipsSPC700NC;
			spca50x->bridge = BRIDGE_SN9CXXX;
			spca50x->sensor = SENSOR_MI0360;
			spca50x->customid = SN9C105;
			spca50x->i2c_ctrl_reg = 0x81;
			spca50x->i2c_base = 0x5d;
			break;
		case 0x0327:
			spca50x->desc = PhilipsSPC600NC;
			spca50x->bridge = BRIDGE_SN9CXXX;
			spca50x->sensor = SENSOR_MI0360;
			spca50x->customid = SN9C105;
			spca50x->i2c_ctrl_reg = 0x81;
			spca50x->i2c_base = 0x5d;
			break;
		default:
			goto error;
		};
		break;
	default:
		goto error;
	}
	return gspca_attach_bridge(spca50x);
      error:
	return -ENODEV;
}
static int
spca5xx_probe(struct usb_interface *intf, const struct usb_device_id *id)
{
	struct usb_interface_descriptor *interface;
	struct usb_spca50x *spca50x;
	int err_probe;
	int i;
	struct usb_device *dev = interface_to_usbdev(intf);
/* We don't handle multi-config cameras */
	if (dev->descriptor.bNumConfigurations != 1)
		goto nodevice;
	interface = &intf->cur_altsetting->desc;
	if (interface->bInterfaceNumber > 0)
		goto nodevice;
	if ((spca50x =
	     kmalloc(sizeof (struct usb_spca50x), GFP_KERNEL)) == NULL) {
		err("couldn't kmalloc spca50x struct");
		goto error;
	}
	memset(spca50x, 0, sizeof (struct usb_spca50x));
	spca50x->dev = dev;
	spca50x->iface = interface->bInterfaceNumber;
	if ((err_probe = spcaDetectCamera(spca50x)) < 0) {
		err(" Devices not found !! ");
		goto error;
	}
	PDEBUG(0, "Camera type %s ", Plist[spca50x->cameratype].name);
	for (i = 0; i < SPCA50X_NUMFRAMES; i++)
		init_waitqueue_head(&spca50x->frame[i].wq);
	init_waitqueue_head(&spca50x->wq);
	if (!spca50x_configure(spca50x)) {
		spca50x->user = 0;
		spca50x->last_times = 0;
		spca50x->dtimes = 0;
		spca50x->autoexpo = autoexpo;
		init_MUTEX(&spca50x->lock);	/* to 1 == available */
		init_MUTEX(&spca50x->buf_lock);
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2, 6, 10)
		spin_lock_init(&spca50x->v4l_lock);
#else
		spca50x->v4l_lock = SPIN_LOCK_UNLOCKED;
#endif
		spca50x->buf_state = BUF_NOT_ALLOCATED;
	} else {
		err("Failed to configure camera");
		goto error;
	}
/* Init video stuff */
	spca50x->vdev = video_device_alloc();
	if (!spca50x->vdev)
		goto error;
	memcpy(spca50x->vdev, &spca50x_template, sizeof (spca50x_template));
	spca50x->vdev->dev = &dev->dev;
	video_set_drvdata(spca50x->vdev, spca50x);
	PDEBUG(2, "setting video device = %p, spca50x = %p", spca50x->vdev,
	       spca50x);
	if (video_register_device(spca50x->vdev, VFL_TYPE_GRABBER, video_nr) <
	    0) {
		err("video_register_device failed");
		goto error;
	}
/* test on disconnect */
	spca50x->present = 1;
/* Workaround for some applications that want data in RGB
* instead of BGR */
	if (spca50x->force_rgb)
		info("data format set to RGB");
	usb_set_intfdata(intf, spca50x);
	spca50x_create_sysfs(spca50x->vdev);
	tasklet_init(&spca50x->spca5xx_tasklet,
		outpict_do_tasklet,(unsigned long) 0);
	return 0;
      error:
	if (spca50x->vdev) {
		if (spca50x->vdev->minor == -1)
			video_device_release(spca50x->vdev);
		else
			video_unregister_device(spca50x->vdev);
		spca50x->vdev = NULL;
	}
	if (spca50x) {
		kfree(spca50x);
		spca50x = NULL;
	}
	return -EIO;
      nodevice:
	return -ENODEV;
}
static void
spca5xx_disconnect(struct usb_interface *intf)
{
	struct usb_spca50x *spca50x = usb_get_intfdata(intf);
	int n;
	if (!spca50x)
		return;
	down(&spca50x->lock);
	spca50x->present = 0;
	for (n = 0; n < SPCA50X_NUMFRAMES; n++)
		spca50x->frame[n].grabstate = FRAME_ABORTING;
	spca50x->curframe = -1;
/* This will cause the process to request another frame */
	for (n = 0; n < SPCA50X_NUMFRAMES; n++)
		if (waitqueue_active(&spca50x->frame[n].wq))
			wake_up_interruptible(&spca50x->frame[n].wq);
	if (waitqueue_active(&spca50x->wq))
		wake_up_interruptible(&spca50x->wq);
	gspca_kill_transfert(spca50x);
	PDEBUG(3, "Disconnect Kill isoc done");
	up(&spca50x->lock);
	while (spca50x->user)
		schedule();
	down(&spca50x->lock);
	dev_set_drvdata(&intf->dev, NULL);
/* We don't want people trying to open up the device */
	if (spca50x->vdev)
		video_unregister_device(spca50x->vdev);
	spca50x->dev = NULL;
	up(&spca50x->lock);
/* Free the memory */
	if (spca50x && !spca50x->user) {
		spca5xx_dealloc(spca50x);
		kfree(spca50x);
		spca50x = NULL;
	}
	PDEBUG(3, "Disconnect complete");
}
static struct usb_driver spca5xx_driver = {
#if LINUX_VERSION_CODE < KERNEL_VERSION(2,6,16)
	.owner = THIS_MODULE,
#endif
	.name = "gspca",
	.id_table = device_table,
	.probe = spca5xx_probe,
	.disconnect = spca5xx_disconnect
};

/****************************************************************************
*
*  Module routines
*
***************************************************************************/
static int __init
usb_spca5xx_init(void)
{
	if (usb_register(&spca5xx_driver) < 0)
		return -1;
	info("gspca driver %s registered", version);
	return 0;
}
static void __exit
usb_spca5xx_exit(void)
{
	usb_deregister(&spca5xx_driver);
	info("driver gspca deregistered");
}

module_init(usb_spca5xx_init);
module_exit(usb_spca5xx_exit);
//eof
