#ifndef SPCA50X_H
#define SPCA50X_H
/*
* Header file for SPCA50x based camera driver. Originally copied from ov511 driver.
* Originally by Mark W. McClelland
* SPCA50x version by Joel Crisp; all bugs are mine, all nice features are his.
* Spca5xx version by Michel Xhaard 
*/
#ifdef __KERNEL__
#include <asm/uaccess.h>
#include <linux/videodev.h>
#include <linux/smp_lock.h>
#include <linux/usb.h>
#include <linux/version.h>
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,18)
#include <media/v4l2-common.h>
#endif
/* V4L API extension for raw JPEG (=JPEG without header) and JPEG with header   
*/
#define VIDEO_PALETTE_RAW_JPEG  20
#define VIDEO_PALETTE_JPEG 21
#ifdef GSPCA_ENABLE_DEBUG
#  define PDEBUG(level, fmt, args...) \
if (debug >= level) info("[%s:%d] " fmt, __PRETTY_FUNCTION__, __LINE__ , ## args)
#else				/* SPCA50X_ENABLE_DEBUG */
#  define PDEBUG(level, fmt, args...) do {} while(0)
#endif				/* SPCA50X_ENABLE_DEBUG */
//#define FRAMES_PER_DESC               10      /* Default value, should be reasonable */
#define FRAMES_PER_DESC  16	/* Default value, should be reasonable */
#define MAX_FRAME_SIZE_PER_DESC 1024
#define SPCA50X_MAX_WIDTH 640
#define SPCA50X_MAX_HEIGHT 480
#define SPCA50X_ENDPOINT_ADDRESS 1	/* Isoc endpoint number */
#define PAC207_ENDPOINT_ADDRESS 5	/* Isoc endpoint number */
/* only 2 or 4 frames are allowed here !!! */
#define SPCA50X_NUMFRAMES 2
#define SPCA50X_NUMSBUF 2
#define VENDOR_SONIX 0x0c45
#define VENDOR_ETOMS 0x102c
#define VENDOR_SUNPLUS 0x04fc
#define VENDOR_AIPTEK 0x08ca
#define VENDOR_LOGITECH 0x046d
#define VENDOR_CREATIVE 0x041e
#define VENDOR_KODAK 0x040a
#define VENDOR_POLAROID 0x0546
#define VENDOR_VIEWQUEST 0x0733
#define VENDOR_INTEL 0x8086
#define VENDOR_GRANDTECH 0x99FA
#define VENDOR_MUSTEK 0x055f
#define VENDOR_DLINK 0x084D
#define VENDOR_3COM 0x0506
#define VENDOR_MEGAPIX 0x052b
#define VENDOR_HAMA 0x0af9
#define VENDOR_AROWANA 0x1776
#define VENDOR_GENIUS 0x0458
#define VENDOR_PETCAM 0xabcd
#define VENDOR_BENQ 0x04a5
#define VENDOR_MAXELL 0x060b
#define VENDOR_UINOVATION 0x0461
#define VENDOR_FLYCAM 0x10fd
#define VENDOR_ADS 0x06e1
#define VENDOR_DIGIDREAM 0x05da
#define VENDOR_VIMICRO 0x0ac8
#define VENDOR_CONEXANT 0x0572
#define VENDOR_ICMEDIA 0x0923
#define VENDOR_VEOSTINGRAY 0x0545
#define VENDOR_OPTIMEDIA 0x06be
#define VENDOR_TOPTRO 0x2899
#define VENDOR_AGFA 0x06bd
#define VENDOR_PIXART 0x093A
#define VENDOR_JVC 0x04f1
#define VENDOR_SMILE 0x0497
#define VENDOR_CTX 0x0698
#define VENDOR_PHILIPS 0x0471

#define BRIDGE_SPCA505 0
#define BRIDGE_SPCA506 1
#define BRIDGE_SPCA501 2
#define BRIDGE_SPCA508 3
#define BRIDGE_SPCA504 4
#define BRIDGE_SPCA500 5
#define BRIDGE_SPCA504B 6
#define BRIDGE_SPCA533 7
#define BRIDGE_SPCA504C 8
#define BRIDGE_SPCA561 9
#define BRIDGE_SPCA536 10
#define BRIDGE_SONIX 11
#define BRIDGE_ZC3XX 12
#define BRIDGE_CX11646 13
#define BRIDGE_TV8532 14
#define BRIDGE_ETOMS 15
#define BRIDGE_SN9CXXX 16
#define BRIDGE_MR97311 17
#define BRIDGE_PAC207 18
#define BRIDGE_VC032X 19

#define SENSOR_SAA7113 0
#define SENSOR_INTERNAL 1
#define SENSOR_HV7131B  2
#define SENSOR_HDCS1020 3
#define SENSOR_PB100_BA 4
#define SENSOR_PB100_92 5
#define SENSOR_PAS106_80 6
#define SENSOR_TAS5130CXX 7
#define SENSOR_ICM105A 8
#define SENSOR_HDCS2020 9
#define SENSOR_PAS106 10
#define SENSOR_PB0330 11
#define SENSOR_HV7131C 12
#define SENSOR_CS2102 13
#define SENSOR_HDCS2020b 14
#define SENSOR_HV7131R 15
#define SENSOR_OV7630 16
#define SENSOR_MI0360 17
#define SENSOR_TAS5110 18
#define SENSOR_PAS202 19
#define SENSOR_PAC207 20
#define SENSOR_OV7630C 21
#define SENSOR_TAS5130C_VF0250 22
#define SENSOR_MO4000 23
#define SENSOR_OV7660 24
#define SENSOR_PO3130NC 25

/* Alternate interface transfer sizes */
#define SPCA50X_ALT_SIZE_0       0
#define SPCA50X_ALT_SIZE_128     1
#define SPCA50X_ALT_SIZE_256     1
#define SPCA50X_ALT_SIZE_384     2
#define SPCA50X_ALT_SIZE_512     3
#define SPCA50X_ALT_SIZE_640     4
#define SPCA50X_ALT_SIZE_768     5
#define SPCA50X_ALT_SIZE_896     6
#define SPCA50X_ALT_SIZE_1023    7
/* Sequence packet identifier for a dropped packet */
#define SPCA50X_SEQUENCE_DROP 0xFF
/* Offsets into the 10 byte header on the first ISO packet */
#define SPCA50X_OFFSET_SEQUENCE 0
#define SPCA50X_OFFSET_FRAMSEQ 6
#define SPCA50X_OFFSET_DATA 10
#define SPCA50X_REG_USB 0x2	// spca505 501
/* I2C interface on an SPCA505, SPCA506, SPCA508 */
#define SPCA50X_REG_I2C_CTRL 0x7
#define SPCA50X_I2C_DEVICE 0x4
#define SPCA50X_I2C_SUBADDR 0x1
#define SPCA50X_I2C_VALUE 0x0
#define SPCA50X_I2C_TRIGGER 0x2
#define SPCA50X_I2C_TRIGGER_BIT 0x1
#define SPCA50X_I2C_READ 0x0
#define SPCA50X_I2C_STATUS 0x3
/* Brightness autoadjustment parameters*/
#define NSTABLE_MAX 4
#define NUNSTABLE_MAX 600
#define MIN_BRIGHTNESS 10
/* Camera type jpeg yuvy yyuv yuyv grey gbrg*/
enum {
	JPEG = 0,		//Jpeg 4.1.1 Sunplus
	JPGH,			//jpeg 4.2.2 Zstar
	JPGC,			//jpeg 4.2.2 Conexant
	JPGS,			//jpeg 4.2.2 Sonix
	JPGM,			//jpeg 4.2.2 Mars-Semi
	YUVY,// Sunplus packed lines
	YYUV,// Sunplus packed lines
	YUYV,// Sunplus packed lines
	GREY,
	GBRG,
	SN9C,			// Sonix compressed stream
	GBGR,
	S561,			// Sunplus Compressed stream
	PGBRG,			// Pixart RGGB bayer
	YUY2, // YUYV packed
};
enum { QCIF = 1,
	QSIF,
	QPAL,
	CIF,
	SIF,
	PAL,
	VGA,
	CUSTOM,
	TOTMODE,
};
/* available palette */
#define P_RGB16  1
#define P_RGB24  (1 << 1)
#define P_RGB32  (1 << 2)
#define P_YUV420  (1 << 3)
#define P_YUV422 ( 1 << 4)
#define P_RAW  (1 << 5)
#define P_JPEG  (1 << 6)
struct mwebcam {
	int width;
	int height;
	__u16 t_palette;
	__u16 pipe;
	int method;
	int mode;
};
struct video_param {
	int chg_para;
#define CHGABRIGHT   1
#define CHGQUALITY   2
#define CHGLIGHTFREQ 3
#define CHGTINTER    4
	__u8 autobright;
	__u8 quality;
	__u16 time_interval;
	__u8 light_freq;
};
/* Our private ioctl */
#define SPCAGVIDIOPARAM _IOR('v',BASE_VIDIOCPRIVATE + 1,struct video_param)
#define SPCASVIDIOPARAM _IOW('v',BASE_VIDIOCPRIVATE + 2,struct video_param)
/* State machine for each frame in the frame buffer during capture */
enum {
	STATE_SCANNING,		/* Scanning for start */
	STATE_HEADER,		/* Parsing header */
	STATE_LINES,		/* Parsing lines */
};
/* Buffer states */
enum {
	BUF_NOT_ALLOCATED,
	BUF_ALLOCATED,
	BUF_PEND_DEALLOC,	/* spca50x->buf_timer is set */
};
struct usb_device;
/* One buffer for the USB ISO transfers */
struct spca50x_sbuf {
	char *data;
	struct urb *urb;
};
/* States for each frame buffer. */
//enum {
#define    FRAME_UNUSED 0x00	/* Unused (no MCAPTURE) */
#define    FRAME_READY 0x01	/* Ready to start grabbing */
#define    FRAME_GRABBING 0x02	/* In the process of being grabbed into */
#define    FRAME_DONE 0x04	/* Finished grabbing, but not been synced yet */
#define    FRAME_ERROR 0x08	/* Something bad happened while processing */
#define    FRAME_ABORTING 0x10	/* Aborting everything. Caused by hot unplugging. */
//};
/************************ decoding data  **************************/
struct pictparam {
	int change;
	int force_rgb;
	int gamma;
	int OffRed;
	int OffBlue;
	int OffGreen;
	int GRed;
	int GBlue;
	int GGreen;
};
#define MAXCOMP 4
struct dec_hufftbl;
struct enc_hufftbl;
union hufftblp {
	struct dec_hufftbl *dhuff;
	struct enc_hufftbl *ehuff;
};
struct scan {
	int dc;			/* old dc value */
	union hufftblp hudc;	/* pointer to huffman table dc */
	union hufftblp huac;	/* pointer to huffman table ac */
	int next;		/* when to switch to next scan */
	int cid;		/* component id */
	int hv;			/* horiz/vert, copied from comp */
	int tq;			/* quant tbl, copied from comp */
};
/*********************************/
#define DECBITS 10		/* seems to be the optimum */
struct dec_hufftbl {
	int maxcode[17];
	int valptr[16];
	unsigned char vals[256];
	unsigned int llvals[1 << DECBITS];
};
/*********************************/
struct in {
	unsigned char *p;
	unsigned int bits;
	int omitescape;
	int left;
	int marker;
};
struct jpginfo {
	int nc;			/* number of components */
	int ns;			/* number of scans */
	int dri;		/* restart interval */
	int nm;			/* mcus til next marker */
	int rm;			/* next restart marker */
};
struct comp {
	int cid;
	int hv;
	int tq;
};
/* Sonix decompressor struct B.S.(2004) */
struct code_table_t {
	int is_abs;
	int len;
	int val;
};
struct dec_data {
	struct in in;
	struct jpginfo info;
	struct comp comps[MAXCOMP];
	struct scan dscans[MAXCOMP];
	unsigned char quant[3][64];
	int dquant[3][64];
	struct code_table_t table[256];
	unsigned char Red[256];
	unsigned char Green[256];
	unsigned char Blue[256];
};
/*************************End decoding data ********************************/
struct spca50x_frame {
	unsigned char *data;	/* Frame buffer */
	unsigned char *tmpbuffer;	/* temporary buffer spca50x->tmpbuffer need for decoding */
	struct dec_data *decoder;
	struct usb_spca50x *spca50x_dev; /* need to find the atomic_t lock */
/* Memory allocation for the jpeg decoders */
	int dcts[6 * 64 + 16];
	int out[6 * 64];
	int max[6];
/*******************************************/
	int depth;		/* Bytes per pixel */
	int width;		/* Width application is expecting */
	int height;		/* Height */
	int hdrwidth;		/* Width the frame actually is */
	int hdrheight;		/* Height */
	int method;		/* The decoding method for that frame 0 nothing 1 crop 2 div 4 mult */
	int cropx1;		/* value to be send with the frame for decoding feature */
	int cropx2;
	int cropy1;
	int cropy2;
	int x;
	int y;
	unsigned int format;	/* Format asked by apps for this frame */
	int cameratype;		/* native in frame format */
	struct pictparam pictsetting;
	volatile int grabstate;	/* State of grabbing */
	int scanstate;		/* State of scanning */
	long scanlength;	/* uncompressed, raw data length of frame */
	int totlength;		/* length of the current reading byte in the Iso stream */
	wait_queue_head_t wq;	/* Processes waiting */
	int snapshot;		/* True if frame was a snapshot */
	int last_packet;	/* sequence number for last packet */
	unsigned char *highwater;	/* used for debugging */
};
struct usb_spca50x;
typedef void (*cam_ops) (struct usb_spca50x *);
typedef int (*intcam_ops) (struct usb_spca50x *);
typedef __u16(*u16cam_ops) (struct usb_spca50x *);
typedef int (*intcam_detect) (struct usb_spca50x *, struct spca50x_frame *,
			      unsigned char *, int *, int, int *);
struct cam_operation {
	intcam_ops initialize;
	intcam_ops configure;
	cam_ops start;
	cam_ops stopN;
	cam_ops stop0;
	u16cam_ops get_bright;
	cam_ops set_bright;
	u16cam_ops get_contrast;
	cam_ops set_contrast;
	u16cam_ops get_colors;
	cam_ops set_colors;
	cam_ops set_autobright;
	cam_ops set_quality;
	cam_ops cam_shutdown;
	intcam_detect sof_detect;
	cam_ops  set_50HZ;
	cam_ops  set_60HZ;
	cam_ops  set_50HZScale;
	cam_ops  set_60HZScale;
	cam_ops  set_NoFliker;
	cam_ops  set_NoFlikerScale;
};
struct usb_spca50x {
	struct video_device *vdev;
	struct usb_device *dev;	/* Device structure */
	struct tasklet_struct spca5xx_tasklet;	/* use a tasklet per device */
	atomic_t in_use; /*tasklet list protect */
	struct dec_data maindecode;
	unsigned long last_times;	//timestamp
	unsigned int dtimes;	//nexttimes to acquire
	unsigned char iface;	/* interface in use */
	int alt;		/* current alternate setting */
	int epadr;		/* endpoint in used */
	int customid;		/* product id get by probe */
	int desc;		/* enum camera name */
	int ccd;		/* If true, using the CCD otherwise the external input */
	int chip_revision;	/* set when probe the camera spca561 zc0301p for vm303 */
	struct mwebcam mode_cam[TOTMODE];	/* all available mode registers by probe */
	int bridge;		/* Type of bridge (BRIDGE_SPCA505 or BRIDGE_SPCA506) */
	int sensor;		/* Type of image sensor chip */
	int packet_size;	/* Frame size per isoc desc */
/* Determined by sensor type */
	int maxwidth;
	int maxheight;
	int minwidth;
	int minheight;
/* What we think the hardware is currently set to */
	int brightness;
	int colour;
	int contrast;
	int hue;
	int whiteness;
	int exposure;		// used by spca561 
	int autoexpo;
	int qindex;
	int width;		/* use here for the init of each frame */
	int height;
	int hdrwidth;
	int hdrheight;
	unsigned int format;
	int method;		/* method ask for output pict */
	int mode;		/* requested frame size */
	int pipe_size;		// requested pipe size set according to mode
	__u16 norme;		/* norme in use Pal Ntsc Secam */
	__u16 channel;		/* input composite video1 or svideo */
	int cameratype;		/* native in frame format */
	struct pictparam pictsetting;
/* Statistics variables */
	spinlock_t v4l_lock;	/* lock to protect shared data between isoc and process context */
	int avg_lum;		//The average luminance (if available from theframe header)
	int avg_bg, avg_rg;	//The average B-G and R-G for white balancing 
	struct semaphore lock;
	int user;		/* user count for exclusive use */
	int present;		/* driver loaded */
	int streaming;		/* Are we streaming Isochronous? */
	int grabbing;		/* Are we grabbing? */
	int packet;
	int synchro;		/* set to 0 if usb packet length = 0 */
	int compress;		/* Should the next frame be compressed? */
	char *fbuf;		/* Videodev buffer area */
	int curframe;		/* Current receiving frame buffer */
	struct spca50x_frame frame[SPCA50X_NUMFRAMES];
	struct spca50x_sbuf sbuf[SPCA50X_NUMSBUF];
/* Temporary jpeg decoder workspace */
	char *tmpBuffer;
/* Framebuffer/sbuf management */
	int buf_state;
	struct semaphore buf_lock;
	wait_queue_head_t wq;	/* Processes waiting */
	uint i2c_ctrl_reg;	// Camera I2C control register
	uint i2c_base;		// Camera I2C address base
	char i2c_trigger_on_write;	//do trigger bit on write
	struct cam_operation funct;
	__u8 force_rgb;		//Read RGB instead of BGR
	__u8 light_freq;	//light frequency banding filter setting
};
struct cam_list {
	int id;
	const char *description;
};
struct palette_list {
	int num;
	const char *name;
};
struct bridge_list {
	int num;
	const char *name;
};
#endif				/* __KERNEL__ */
#endif				/* SPCA50X_H */
