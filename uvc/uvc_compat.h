#ifndef _UVC_COMPAT_H
#define _UVC_COMPAT_H

#include <linux/version.h>

#if LINUX_VERSION_CODE < KERNEL_VERSION(2,6,18)
/*
 * Extended control API
 */
struct v4l2_ext_control
{
	__u32 id;
	__u32 reserved2[2];
	union {
		__s32 value;
		__s64 value64;
		void *reserved;
	};
} __attribute__ ((packed));

struct v4l2_ext_controls
{
	__u32 ctrl_class;
	__u32 count;
	__u32 error_idx;
	__u32 reserved[2];
	struct v4l2_ext_control *controls;
};

/* Values for ctrl_class field */
#define V4L2_CTRL_CLASS_USER		0x00980000	/* Old-style 'user' controls */
#define V4L2_CTRL_CLASS_MPEG		0x00990000	/* MPEG-compression controls */

#define V4L2_CTRL_ID_MASK		(0x0fffffff)
#define V4L2_CTRL_ID2CLASS(id)		((id) & 0x0fff0000UL)
#define V4L2_CTRL_DRIVER_PRIV(id)	(((id) & 0xffff) >= 0x1000)

/* User-class control IDs defined by V4L2 */
#undef	V4L2_CID_BASE
#define V4L2_CID_BASE			(V4L2_CTRL_CLASS_USER | 0x900)
#define V4L2_CID_USER_BASE		V4L2_CID_BASE
#define V4L2_CID_USER_CLASS		(V4L2_CTRL_CLASS_USER | 1)
	
#define VIDIOC_G_EXT_CTRLS		_IOWR ('V', 71, struct v4l2_ext_controls)
#define VIDIOC_S_EXT_CTRLS		_IOWR ('V', 72, struct v4l2_ext_controls)
#define VIDIOC_TRY_EXT_CTRLS		_IOWR ('V', 73, struct v4l2_ext_controls)

#endif

#if LINUX_VERSION_CODE < KERNEL_VERSION(2,6,19)
/*
 * Frame size and frame rate enumeration
 *
 * Included in Linux 2.6.19
 */
enum v4l2_frmsizetypes
{
	V4L2_FRMSIZE_TYPE_DISCRETE	= 1,
	V4L2_FRMSIZE_TYPE_CONTINUOUS	= 2,
	V4L2_FRMSIZE_TYPE_STEPWISE	= 3,
};

struct v4l2_frmsize_discrete
{
	__u32			width;		/* Frame width [pixel] */
	__u32			height;		/* Frame height [pixel] */
};

struct v4l2_frmsize_stepwise
{
	__u32			min_width;	/* Minimum frame width [pixel] */
	__u32			max_width;	/* Maximum frame width [pixel] */
	__u32			step_width;	/* Frame width step size [pixel] */
	__u32			min_height;	/* Minimum frame height [pixel] */
	__u32			max_height;	/* Maximum frame height [pixel] */
	__u32			step_height;	/* Frame height step size [pixel] */
};

struct v4l2_frmsizeenum
{
	__u32			index;		/* Frame size number */
	__u32			pixel_format;	/* Pixel format */
	__u32			type;		/* Frame size type the device supports. */

        union {					/* Frame size */
		struct v4l2_frmsize_discrete	discrete;
		struct v4l2_frmsize_stepwise	stepwise;
	};

	__u32   reserved[2];			/* Reserved space for future use */
};

enum v4l2_frmivaltypes
{
	V4L2_FRMIVAL_TYPE_DISCRETE	= 1,
	V4L2_FRMIVAL_TYPE_CONTINUOUS	= 2,
	V4L2_FRMIVAL_TYPE_STEPWISE	= 3,
};

struct v4l2_frmival_stepwise
{
	struct v4l2_fract	min;		/* Minimum frame interval [s] */
	struct v4l2_fract	max;		/* Maximum frame interval [s] */
	struct v4l2_fract	step;		/* Frame interval step size [s] */
};

struct v4l2_frmivalenum
{
	__u32			index;		/* Frame format index */
	__u32			pixel_format;	/* Pixel format */
	__u32			width;		/* Frame width */
	__u32			height;		/* Frame height */
	__u32			type;		/* Frame interval type the device supports. */

	union {					/* Frame interval */
		struct v4l2_fract		discrete;
		struct v4l2_frmival_stepwise	stepwise;
	};

	__u32	reserved[2];			/* Reserved space for future use */
};

#define VIDIOC_ENUM_FRAMESIZES		_IOWR ('V', 74, struct v4l2_frmsizeenum)
#define VIDIOC_ENUM_FRAMEINTERVALS	_IOWR ('V', 75, struct v4l2_frmivalenum)
#endif

#ifdef __KERNEL__

#if LINUX_VERSION_CODE < KERNEL_VERSION(2,6,14)
/*
 * kzalloc()
 */
static inline void *
kzalloc(size_t size, unsigned int __nocast gfp_flags)
{
	void *mem = kmalloc(size, gfp_flags);
	if (mem)
		memset(mem, 0, size);
	return mem;
}
#endif

#if LINUX_VERSION_CODE < KERNEL_VERSION(2,6,15)
/*
 * vm_insert_page()
 */
static inline int
vm_insert_page(struct vm_area_struct *vma, unsigned long addr,
		struct page *page)
{
	/* Not sure if this is needed. remap_pfn_range() sets VM_RESERVED
	 * in 2.6.14.
	 */
	vma->vm_flags |= VM_RESERVED;

	SetPageReserved(page);
	return remap_pfn_range(vma, addr, page_to_pfn(page), PAGE_SIZE,
				vma->vm_page_prot);
}
#endif

#if LINUX_VERSION_CODE < KERNEL_VERSION(2,6,16)
/*
 * v4l_printk_ioctl()
 */
static inline void
v4l_printk_ioctl(unsigned int cmd)
{
	switch (_IOC_TYPE(cmd)) {
	case 'v':
		printk(KERN_DEBUG "ioctl 0x%x (V4L1)\n", cmd);
		break;
	case 'V':
		printk(KERN_DEBUG "ioctl 0x%x (%s)\n",
			cmd, v4l2_ioctl_names[_IOC_NR(cmd)]);
		break;
	default:
		printk(KERN_DEBUG "ioctl 0x%x (?)\n", cmd);
		break;
	}
}
#endif

#if LINUX_VERSION_CODE < KERNEL_VERSION(2,6,16)
/*
 * Mutex API
 */
#include <asm/semaphore.h>
#define mutex_lock(mutex) down(mutex)
#define mutex_lock_interruptible(mutex) down_interruptible(mutex)
#define mutex_unlock(mutex) up(mutex)
#define mutex_init(mutex) init_MUTEX(mutex)
#define mutex semaphore
#else
#include <asm/mutex.h>
#endif

#if LINUX_VERSION_CODE < KERNEL_VERSION(2,6,19)
/*
 * usb_endpoint_* functions
 *
 * Included in Linux 2.6.19
 */
static inline int usb_endpoint_dir_in(const struct usb_endpoint_descriptor *epd)
{
	return ((epd->bEndpointAddress & USB_ENDPOINT_DIR_MASK) == USB_DIR_IN);
}

static inline int usb_endpoint_xfer_int(const struct usb_endpoint_descriptor *epd)
{
	return ((epd->bmAttributes & USB_ENDPOINT_XFERTYPE_MASK) ==
		USB_ENDPOINT_XFER_INT);
}

static inline int usb_endpoint_xfer_isoc(const struct usb_endpoint_descriptor *epd)
{
	return ((epd->bmAttributes & USB_ENDPOINT_XFERTYPE_MASK) ==
		USB_ENDPOINT_XFER_ISOC);
}

static inline int usb_endpoint_xfer_bulk(const struct usb_endpoint_descriptor *epd)
{
	return ((epd->bmAttributes & USB_ENDPOINT_XFERTYPE_MASK) ==
		USB_ENDPOINT_XFER_BULK);
}

static inline int usb_endpoint_is_int_in(const struct usb_endpoint_descriptor *epd)
{
	return (usb_endpoint_xfer_int(epd) && usb_endpoint_dir_in(epd));
}
#endif

#endif /* __KERNEL__ */

#endif /* _UVC_COMPAT_H */

