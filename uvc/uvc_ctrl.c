/*
 *      uvcvideo.c  --  USB Video Class driver
 *
 *      Copyright (C) 2005-2006
 *          Laurent Pinchart (laurent.pinchart@skynet.be)
 *
 *      This program is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; either version 2 of the License, or
 *      (at your option) any later version.
 *
 */

#include <linux/kernel.h>
#include <linux/version.h>
#include <linux/list.h>
#include <linux/module.h>
#include <linux/usb.h>
#include <linux/videodev.h>
#include <linux/vmalloc.h>
#include <linux/wait.h>
#include <asm/atomic.h>

#include "uvcvideo.h"

#define UVC_CONTROL_SET_CUR	(1 << 0)
#define UVC_CONTROL_GET_CUR	(1 << 1)
#define UVC_CONTROL_GET_MIN	(1 << 2)
#define UVC_CONTROL_GET_MAX	(1 << 3)
#define UVC_CONTROL_GET_RES	(1 << 4)
#define UVC_CONTROL_GET_DEF	(1 << 5)
/* Control should be saved at suspend and restored at resume. */
#define UVC_CONTROL_RESTORE	(1 << 6)

#define UVC_CONTROL_GET_RANGE	(UVC_CONTROL_GET_CUR | UVC_CONTROL_GET_MIN | \
				 UVC_CONTROL_GET_MAX | UVC_CONTROL_GET_RES | \
				 UVC_CONTROL_GET_DEF)

#define UVC_CTRL_NDATA		2
#define UVC_CTRL_DATA_CURRENT	0
#define UVC_CTRL_DATA_BACKUP	1

/* ------------------------------------------------------------------------
 * Control, formats, ...
 */

static struct uvc_control_info uvc_ctrls[] = {
	{
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_BRIGHTNESS_CONTROL,
		.index		= 0,
		.size		= 2,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_RANGE
				| UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_CONTRAST_CONTROL,
		.index		= 1,
		.size		= 2,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_RANGE
				| UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_HUE_CONTROL,
		.index		= 2,
		.size		= 2,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_RANGE
				| UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_SATURATION_CONTROL,
		.index		= 3,
		.size		= 2,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_RANGE
				| UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_SHARPNESS_CONTROL,
		.index		= 4,
		.size		= 2,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_RANGE
				| UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_GAMMA_CONTROL,
		.index		= 5,
		.size		= 2,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_RANGE
				| UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_BACKLIGHT_COMPENSATION_CONTROL,
		.index		= 8,
		.size		= 2,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_RANGE
				| UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_GAIN_CONTROL,
		.index		= 9,
		.size		= 2,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_RANGE
				| UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_POWER_LINE_FREQUENCY_CONTROL,
		.index		= 10,
		.size		= 1,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_RANGE
				| UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_HUE_AUTO_CONTROL,
		.index		= 11,
		.size		= 1,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_CUR
				| UVC_CONTROL_GET_DEF | UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_LOGITECH_MOTOR,
		.selector	= LXU_MOTOR_PANTILT_RELATIVE_CONTROL,
		.index		= 0,
		.size		= 4,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_MIN
				| UVC_CONTROL_GET_MAX | UVC_CONTROL_GET_DEF,
	},
	{
		.entity		= UVC_GUID_LOGITECH_MOTOR,
		.selector	= LXU_MOTOR_PANTILT_RESET_CONTROL,
		.index		= 1,
		.size		= 1,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_MIN
				| UVC_CONTROL_GET_MAX | UVC_CONTROL_GET_RES
				| UVC_CONTROL_GET_DEF,
	},
	{
		.entity		= UVC_GUID_LOGITECH_MOTOR,
		.selector	= LXU_MOTOR_FOCUS_MOTOR_CONTROL,
		.index		= 2,
		.size		= 6,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_RANGE,
	},
	{
		.entity		= UVC_GUID_UVC_CAMERA,
		.selector	= CT_AE_MODE_CONTROL,
		.index		= 1,
		.size		= 1,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_CUR
				| UVC_CONTROL_GET_DEF | UVC_CONTROL_GET_RES
				| UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_CAMERA,
		.selector	= CT_EXPOSURE_TIME_ABSOLUTE_CONTROL,
		.index		= 3,
		.size		= 4,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_RANGE
				| UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_CAMERA,
		.selector	= CT_FOCUS_ABSOLUTE_CONTROL,
		.index		= 5,
		.size		= 2,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_RANGE
				| UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_CAMERA,
		.selector	= CT_FOCUS_AUTO_CONTROL,
		.index		= 17,
		.size		= 1,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_CUR
				| UVC_CONTROL_GET_DEF | UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_WHITE_BALANCE_TEMPERATURE_AUTO_CONTROL,
		.index		= 12,
		.size		= 1,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_CUR
				| UVC_CONTROL_GET_DEF | UVC_CONTROL_RESTORE,
	},
	{
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_WHITE_BALANCE_TEMPERATURE_CONTROL,
		.index		= 6,
		.size		= 2,
		.flags		= UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_RANGE
				| UVC_CONTROL_RESTORE,
	},
};

static struct uvc_menu_info power_line_frequency_controls[] = {
	{ 0, "Disabled" },
	{ 1, "50 Hz" },
	{ 2, "60 Hz" },
};

static struct uvc_control_mapping uvc_ctrl_mappings[] = {
	{
		.id		= V4L2_CID_BRIGHTNESS,
		.name		= "Brightness",
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_BRIGHTNESS_CONTROL,
		.size		= 16,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_SIGNED,
	},
	{
		.id		= V4L2_CID_CONTRAST,
		.name		= "Contrast",
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_CONTRAST_CONTROL,
		.size		= 16,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_UNSIGNED,
	},
	{
		.id		= V4L2_CID_HUE,
		.name		= "Hue",
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_HUE_CONTROL,
		.size		= 16,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_SIGNED,
	},
	{
		.id		= V4L2_CID_SATURATION,
		.name		= "Saturation",
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_SATURATION_CONTROL,
		.size		= 16,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_UNSIGNED,
	},
	{
		.id		= V4L2_CID_SHARPNESS,
		.name		= "Sharpness",
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_SHARPNESS_CONTROL,
		.size		= 16,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_UNSIGNED,
	},
	{
		.id		= V4L2_CID_GAMMA,
		.name		= "Gamma",
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_GAMMA_CONTROL,
		.size		= 16,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_UNSIGNED,
	},
	{
		.id		= V4L2_CID_BACKLIGHT_COMPENSATION,
		.name		= "Backlight Compensation",
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_BACKLIGHT_COMPENSATION_CONTROL,
		.size		= 16,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_UNSIGNED,
	},
	{
		.id		= V4L2_CID_GAIN,
		.name		= "Gain",
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_GAIN_CONTROL,
		.size		= 16,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_UNSIGNED,
	},
	{
		.id		= V4L2_CID_POWER_LINE_FREQUENCY,
		.name		= "Power Line Frequency",
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_POWER_LINE_FREQUENCY_CONTROL,
		.size		= 2,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_MENU,
		.data_type	= UVC_CTRL_DATA_TYPE_ENUM,
		.menu_info	= power_line_frequency_controls,
		.menu_count	= ARRAY_SIZE(power_line_frequency_controls),
	},
	{
		.id		= V4L2_CID_HUE_AUTO,
		.name		= "Hue, Auto",
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_HUE_AUTO_CONTROL,
		.size		= 1,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_BOOLEAN,
		.data_type	= UVC_CTRL_DATA_TYPE_BOOLEAN,
	},
	{
		.id		= V4L2_CID_PAN_RELATIVE,
		.name		= "Pan (relative)",
		.entity		= UVC_GUID_LOGITECH_MOTOR,
		.selector	= LXU_MOTOR_PANTILT_RELATIVE_CONTROL,
		.size		= 16,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_SIGNED,
	},
	{
		.id		= V4L2_CID_TILT_RELATIVE,
		.name		= "Tilt (relative)",
		.entity		= UVC_GUID_LOGITECH_MOTOR,
		.selector	= LXU_MOTOR_PANTILT_RELATIVE_CONTROL,
		.size		= 16,
		.offset		= 16,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_SIGNED,
	},
	{
		.id		= V4L2_CID_PANTILT_RESET,
		.name		= "Pan/Tilt (reset)",
		.entity		= UVC_GUID_LOGITECH_MOTOR,
		.selector	= LXU_MOTOR_PANTILT_RESET_CONTROL,
		.size		= 2,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_ENUM,
	},
	{
		.id		= V4L2_CID_EXPOSURE_AUTO,
		.name		= "Exposure, Auto",
		.entity		= UVC_GUID_UVC_CAMERA,
		.selector	= CT_AE_MODE_CONTROL,
		.size		= 4,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_BITMASK,
	},
	{
		.id		= V4L2_CID_EXPOSURE_ABSOLUTE,
		.name		= "Exposure (Absolute)",
		.entity		= UVC_GUID_UVC_CAMERA,
		.selector	= CT_EXPOSURE_TIME_ABSOLUTE_CONTROL,
		.size		= 32,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_UNSIGNED,
	},
	{
		.id		= V4L2_CID_WHITE_BALANCE_TEMPERATURE_AUTO,
		.name		= "White Balance Temperature, Auto",
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_WHITE_BALANCE_TEMPERATURE_AUTO_CONTROL,
		.size		= 1,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_BOOLEAN,
		.data_type	= UVC_CTRL_DATA_TYPE_BOOLEAN,
	},
	{
		.id		= V4L2_CID_WHITE_BALANCE_TEMPERATURE,
		.name		= "White Balance Temperature",
		.entity		= UVC_GUID_UVC_PROCESSING,
		.selector	= PU_WHITE_BALANCE_TEMPERATURE_CONTROL,
		.size		= 16,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_UNSIGNED,
	},
	{
		.id		= V4L2_CID_FOCUS_ABSOLUTE,
		.name		= "Focus (absolute)",
		.entity		= UVC_GUID_UVC_CAMERA,
		.selector	= CT_FOCUS_ABSOLUTE_CONTROL,
		.size		= 16,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_UNSIGNED,
	},
	{
		.id		= V4L2_CID_FOCUS_AUTO,
		.name		= "Focus, Auto",
		.entity		= UVC_GUID_UVC_CAMERA,
		.selector	= CT_FOCUS_AUTO_CONTROL,
		.size		= 1,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_BOOLEAN,
		.data_type	= UVC_CTRL_DATA_TYPE_BOOLEAN,
	},
	{
		.id		= V4L2_CID_FOCUS_ABSOLUTE,
		.name		= "Focus (absolute)",
		.entity		= UVC_GUID_LOGITECH_MOTOR,
		.selector	= LXU_MOTOR_FOCUS_MOTOR_CONTROL,
		.size		= 8,
		.offset		= 0,
		.v4l2_type	= V4L2_CTRL_TYPE_INTEGER,
		.data_type	= UVC_CTRL_DATA_TYPE_UNSIGNED,
	},
};

/* ------------------------------------------------------------------------
 * Utility functions
 */

static inline __u8 *uvc_ctrl_data(struct uvc_control *ctrl, int id)
{
	return ctrl->data + id * ctrl->info->size;
}

static inline int uvc_get_bit(const __u8 *data, int bit)
{
	return (data[bit >> 3] >> (bit & 7)) & 1;
}

/* Extract the bit string specified by mapping->offset and mapping->size
 * from the little-endian data stored at 'data' and return the result as
 * a signed 32bit integer. Sign extension will be performed if the mapping
 * references a signed data type.
 */
static __s32 uvc_get_le_value(const __u8 *data,
	struct uvc_control_mapping *mapping)
{
	int bits = mapping->size;
	int offset = mapping->offset;
	__s32 value = 0;
	__u8 mask;

	data += offset / 8;
	offset &= 7;
	mask = ((1LL << bits) - 1) << offset;

	for (; bits > 0; data++) {
		__u8 byte = *data & mask;
		value |= offset > 0 ? (byte >> offset) : (byte << (-offset));
		bits -= 8 - (offset > 0 ? offset : 0);
		offset -= 8;
		mask = (1 << bits) - 1;
	}

	/* Sign-extend the value if needed */
	if (mapping->data_type == UVC_CTRL_DATA_TYPE_SIGNED)
		value |= -(value & (1 << (mapping->size - 1)));

	return value;
}

/* Set the bit string specified by mapping->offset and mapping->size
 * in the little-endian data stored at 'data' to the value 'value'.
 */
static void uvc_set_le_value(__s32 value, __u8 *data,
	struct uvc_control_mapping *mapping)
{
	int bits = mapping->size;
	int offset = mapping->offset;
	__u8 mask;

	data += offset / 8;
	offset &= 7;

	for (; bits > 0; data++) {
		mask = ((1LL << bits) - 1) << offset;
		*data = (*data & ~mask) | ((value << offset) & mask);
		value >>= offset ? offset : 8;
		bits -= 8 - offset;
		offset = 0;
	}
}

/* ------------------------------------------------------------------------
 * Terminal and unit management
 */

static const __u8 uvc_processing_guid[16] = UVC_GUID_UVC_PROCESSING;
static const __u8 uvc_camera_guid[16] = UVC_GUID_UVC_CAMERA;
static const __u8 uvc_media_transport_input_guid[16] = UVC_GUID_UVC_MEDIA_TRANSPORT_INPUT;

static int uvc_entity_match_guid(struct uvc_entity *entity, __u8 guid[16])
{
	switch (entity->type) {
	case ITT_CAMERA:
		return memcmp(uvc_camera_guid, guid, 16) == 0;

	case ITT_MEDIA_TRANSPORT_INPUT:
		return memcmp(uvc_media_transport_input_guid, guid, 16) == 0;

	case VC_PROCESSING_UNIT:
		return memcmp(uvc_processing_guid, guid, 16) == 0;

	case VC_EXTENSION_UNIT:
		return memcmp(entity->extension.guidExtensionCode, guid, 16) == 0;

	default:
		return 0;
	}
}

/* ------------------------------------------------------------------------
 * UVC Controls
 */

static struct uvc_control *__uvc_find_control(struct uvc_entity *entity,
	__u32 v4l2_id, struct uvc_control_mapping **mapping)
{
	struct uvc_control *ctrl;
	struct uvc_control_mapping *map;
	unsigned int i;

	if (entity == NULL)
		return NULL;

	for (i = 0; i < entity->ncontrols; ++i) {
		ctrl = &entity->controls[i];
		if (ctrl->info == NULL)
			continue;

		list_for_each_entry(map, &ctrl->info->mappings, list) {
			if (map->id == v4l2_id) {
				*mapping = map;
				return ctrl;
			}
		}
	}

	return NULL;
}

struct uvc_control *uvc_find_control(struct uvc_video_device *video,
	__u32 v4l2_id, struct uvc_control_mapping **mapping)
{
	struct uvc_control *ctrl;
	struct uvc_entity *entity;

	/* Find the control. */
	ctrl = __uvc_find_control(video->processing, v4l2_id, mapping);
	if (ctrl)
		return ctrl;

	list_for_each_entry(entity, &video->iterms, chain) {
		ctrl = __uvc_find_control(entity, v4l2_id, mapping);
		if (ctrl)
			return ctrl;
	}

	list_for_each_entry(entity, &video->extensions, chain) {
		ctrl = __uvc_find_control(entity, v4l2_id, mapping);
		if (ctrl)
			return ctrl;
	}

	uvc_trace(UVC_TRACE_CONTROL, "Control 0x%08x not found.\n", v4l2_id);
	return NULL;
}

int uvc_query_v4l2_ctrl(struct uvc_video_device *video, struct v4l2_queryctrl *v4l2_ctrl)
{
	struct uvc_control *ctrl;
	struct uvc_control_mapping *mapping;
	__u8 data[8];
	int ret;

	ctrl = uvc_find_control(video, v4l2_ctrl->id, &mapping);
	if (ctrl == NULL) {
		/* If the V4L2 control ID is in the private control ID range,
		 * there's a chance the application is enumerating our private
		 * controls, so we can't return EINVAL because (according to the
		 * V4L2 spec) it will think that this was the last one. However,
		 * it might just be this particular control that is not
		 * supported and we want the enumeration to continue.
		 */
		if (v4l2_ctrl->id < V4L2_CID_PRIVATE_BASE ||
		    v4l2_ctrl->id > V4L2_CID_PRIVATE_LAST) {
			return -EINVAL;
		} else {
			v4l2_ctrl->name[0] = '\0';
			v4l2_ctrl->flags = V4L2_CTRL_FLAG_DISABLED;
			return 0;
		}
	}

	if (ctrl->info->flags & UVC_CONTROL_GET_DEF) {
		if ((ret = uvc_query_ctrl(video->dev, GET_DEF, ctrl->entity->id,
					video->dev->intfnum, ctrl->info->selector,
					&data, ctrl->info->size)) < 0)
			return ret;
		v4l2_ctrl->default_value = uvc_get_le_value(data, mapping);
	}
	if (ctrl->info->flags & UVC_CONTROL_GET_MIN) {
		if ((ret = uvc_query_ctrl(video->dev, GET_MIN, ctrl->entity->id,
					video->dev->intfnum, ctrl->info->selector,
					&data, ctrl->info->size)) < 0)
			return ret;
		v4l2_ctrl->minimum = uvc_get_le_value(data, mapping);
	}
	if (ctrl->info->flags & UVC_CONTROL_GET_MAX) {
		if ((ret = uvc_query_ctrl(video->dev, GET_MAX, ctrl->entity->id,
					video->dev->intfnum, ctrl->info->selector,
					&data, ctrl->info->size)) < 0)
			return ret;
		v4l2_ctrl->maximum = uvc_get_le_value(data, mapping);
	}
	if (ctrl->info->flags & UVC_CONTROL_GET_RES) {
		if ((ret = uvc_query_ctrl(video->dev, GET_RES, ctrl->entity->id,
					video->dev->intfnum, ctrl->info->selector,
					&data, ctrl->info->size)) < 0)
			return ret;
		v4l2_ctrl->step = uvc_get_le_value(data, mapping);
	}

	v4l2_ctrl->type = mapping->v4l2_type;
	strncpy(v4l2_ctrl->name, mapping->name, sizeof v4l2_ctrl->name);
	v4l2_ctrl->flags = 0;

	return 0;
}


/* --------------------------------------------------------------------------
 * Control transactions
 *
 * To make extended set operations as atomic as the hardware allows, controls
 * are handled using begin/commit/rollback operations.
 *
 * At the beginning of a set request, uvc_ctrl_begin should be called to
 * initialize the request. This function acquires the control lock.
 *
 * When setting a control, the new value is stored in the control data field
 * at position UVC_CTRL_DATA_CURRENT. The control is then marked as dirty for
 * later processing. If the UVC and V4L2 control sizes differ, the current
 * value is loaded from the hardware before storing the new value in the data
 * field.
 *
 * After processing all controls in the transaction, uvc_ctrl_commit or
 * uvc_ctrl_rollback must be called to apply the pending changes to the
 * hardware or revert them. When applying changes, all controls marked as
 * dirty will be modified in the UVC device, and the dirty flag will be
 * cleared. When reverting controls, the control data field
 * UVC_CTRL_DATA_CURRENT is reverted to its previous value
 * (UVC_CTRL_DATA_BACKUP) for all dirty controls. Both functions release the
 * control lock.
 */
int uvc_ctrl_begin(struct uvc_video_device *video)
{
	return mutex_lock_interruptible(&video->ctrl_mutex) ? -ERESTARTSYS : 0;
}

static int uvc_ctrl_commit_entity(struct uvc_device *dev,
	struct uvc_entity *entity, int rollback)
{
	struct uvc_control *ctrl;
	unsigned int i;
	int ret;

	if (entity == NULL)
		return 0;

	for (i = 0; i < entity->ncontrols; ++i) {
		ctrl = &entity->controls[i];
		if (ctrl->info == NULL || !ctrl->dirty)
			continue;

		if (!rollback)
			ret = uvc_query_ctrl(dev, SET_CUR, ctrl->entity->id,
				dev->intfnum, ctrl->info->selector,
				uvc_ctrl_data(ctrl, UVC_CTRL_DATA_CURRENT),
				ctrl->info->size);
		else
			ret = 0;

		if (rollback || ret < 0)
			memcpy(uvc_ctrl_data(ctrl, UVC_CTRL_DATA_CURRENT),
			       uvc_ctrl_data(ctrl, UVC_CTRL_DATA_BACKUP),
			       ctrl->info->size);

		if ((ctrl->info->flags & UVC_CONTROL_GET_CUR) == 0)
			ctrl->loaded = 0;

		ctrl->dirty = 0;

		if (ret < 0)
			return ret;
	}

	return 0;
}

int __uvc_ctrl_commit(struct uvc_video_device *video, int rollback)
{
	struct uvc_entity *entity;
	int ret = 0;

	/* Find the control. */
	ret = uvc_ctrl_commit_entity(video->dev, video->processing, rollback);
	if (ret < 0)
		goto done;

	list_for_each_entry(entity, &video->iterms, chain) {
		ret = uvc_ctrl_commit_entity(video->dev, entity, rollback);
		if (ret < 0)
			goto done;
	}

	list_for_each_entry(entity, &video->extensions, chain) {
		ret = uvc_ctrl_commit_entity(video->dev, entity, rollback);
		if (ret < 0)
			goto done;
	}

done:
	mutex_unlock(&video->ctrl_mutex);
	return ret;
}

int uvc_ctrl_get(struct uvc_video_device *video,
	struct v4l2_ext_control *xctrl)
{
	struct uvc_control *ctrl;
	struct uvc_control_mapping *mapping;
	int ret;

	ctrl = uvc_find_control(video, xctrl->id, &mapping);
	if (ctrl == NULL || (ctrl->info->flags & UVC_CONTROL_GET_CUR) == 0)
		return -EINVAL;

	if (!ctrl->loaded) {
		ret = uvc_query_ctrl(video->dev, GET_CUR, ctrl->entity->id,
				video->dev->intfnum, ctrl->info->selector,
				uvc_ctrl_data(ctrl, UVC_CTRL_DATA_CURRENT),
				ctrl->info->size);
		if (ret < 0)
			return ret;

		ctrl->loaded = 1;
	}

	xctrl->value = uvc_get_le_value(
		uvc_ctrl_data(ctrl, UVC_CTRL_DATA_CURRENT), mapping);

	return 0;
}

int uvc_ctrl_set(struct uvc_video_device *video,
	struct v4l2_ext_control *xctrl)
{
	struct uvc_control *ctrl;
	struct uvc_control_mapping *mapping;
	int ret;

	ctrl = uvc_find_control(video, xctrl->id, &mapping);
	if (ctrl == NULL || (ctrl->info->flags & UVC_CONTROL_SET_CUR) == 0)
		return -EINVAL;

	if (!ctrl->loaded && (ctrl->info->size * 8) != mapping->size) {
		if ((ctrl->info->flags & UVC_CONTROL_GET_CUR) == 0) {
			memset(uvc_ctrl_data(ctrl, UVC_CTRL_DATA_CURRENT),
				0, ctrl->info->size);
		} else {
			ret = uvc_query_ctrl(video->dev, GET_CUR,
				ctrl->entity->id, video->dev->intfnum,
				ctrl->info->selector,
				uvc_ctrl_data(ctrl, UVC_CTRL_DATA_CURRENT),
				ctrl->info->size);
			if (ret < 0)
				return ret;
		}

		ctrl->loaded = 1;
	}

	if (!ctrl->dirty) {
		memcpy(uvc_ctrl_data(ctrl, UVC_CTRL_DATA_BACKUP),
		       uvc_ctrl_data(ctrl, UVC_CTRL_DATA_CURRENT),
		       ctrl->info->size);
	}

	uvc_set_le_value(xctrl->value,
		uvc_ctrl_data(ctrl, UVC_CTRL_DATA_CURRENT), mapping);

	ctrl->dirty = 1;
	ctrl->modified = 1;
	return 0;
}


/* --------------------------------------------------------------------------
 * Suspend/resume
 */

/*
 * Restore control values after resume, skipping controls that haven't been
 * changed.
 *
 * TODO
 * - Don't restore modified controls that are back to their default value.
 * - Handle restore order (Auto-Exposure Mode should be restored before
 *   Exposure Time).
 */
int uvc_ctrl_resume_device(struct uvc_device *dev)
{
	struct uvc_control *ctrl;
	struct uvc_entity *entity;
	unsigned int i;
	int ret;

	/* Walk the entities list and restore controls when possible. */
	list_for_each_entry(entity, &dev->entities, list) {

		for (i = 0; i < entity->ncontrols; ++i) {
			ctrl = &entity->controls[i];

			if (ctrl->info == NULL || !ctrl->modified ||
			    (ctrl->info->flags & UVC_CONTROL_RESTORE) == 0)
				continue;

			printk(KERN_INFO "restoring control " UVC_GUID_FORMAT
				"/%u/%u\n", UVC_GUID_ARGS(ctrl->info->entity),
				ctrl->info->index, ctrl->info->selector);
			ctrl->dirty = 1;
		}

		ret = uvc_ctrl_commit_entity(dev, entity, 0);
		if (ret < 0)
			return ret;
	}

	return 0;
}

/* --------------------------------------------------------------------------
 * Control and mapping handling
 */

static void uvc_ctrl_add_ctrl(struct uvc_device *dev,
	struct uvc_control_info *info)
{
	struct uvc_entity *entity;
	struct uvc_control *ctrl;
	unsigned int i;

	list_for_each_entry(entity, &dev->entities, list) {
		if (!uvc_entity_match_guid(entity, info->entity))
			continue;

		for (i = 0; i < entity->ncontrols; ++i) {
			ctrl = &entity->controls[i];
			if (ctrl->index == info->index) {
				ctrl->info = info;
				ctrl->data = kmalloc(info->size * UVC_CTRL_NDATA, GFP_KERNEL);
				uvc_trace(UVC_TRACE_CONTROL, "Added control "
					UVC_GUID_FORMAT "/%u to device %s entity %u\n",
					UVC_GUID_ARGS(ctrl->info->entity),
					ctrl->info->selector,
					dev->udev->devpath, entity->id);
				break;
			}
		}
	}
}

/*
 * Add an item to the UVC control information list, and instantiate a control
 * structure for each device that supports the control.
 */
void uvc_ctrl_add_info(struct uvc_control_info *info)
{
	struct uvc_control_info *ctrl;
	struct uvc_device *dev;

	/* Find matching controls by walking the devices, entities and
	 * controls list.
	 */
	mutex_lock(&uvc_driver.ctrl_mutex);

	/* First check if the list contains a control matching the new one.
	 * Bail out if it does.
	 */
	list_for_each_entry(ctrl, &uvc_driver.controls, list) {
		if (memcmp(ctrl->entity, info->entity, 16))
			continue;

		if (ctrl->selector == info->selector) {
			uvc_trace(UVC_TRACE_CONTROL, "Control "
				UVC_GUID_FORMAT "/%u is already defined.\n",
				UVC_GUID_ARGS(info->entity), info->selector);
			goto end;
		}
		if (ctrl->index == info->index) {
			uvc_trace(UVC_TRACE_CONTROL, "Control "
				UVC_GUID_FORMAT "/%u would overwrite index "
				"%d.\n", UVC_GUID_ARGS(info->entity),
				info->selector, info->index);
			goto end;
		}
	}

	list_for_each_entry(dev, &uvc_driver.devices, list)
		uvc_ctrl_add_ctrl(dev, info);

	INIT_LIST_HEAD(&info->mappings);
	list_add_tail(&info->list, &uvc_driver.controls);
end:
	mutex_unlock(&uvc_driver.ctrl_mutex);
}

static void uvc_ctrl_add_mapping(struct uvc_control_mapping *mapping)
{
	struct uvc_control_info *info;
	struct uvc_control_mapping *map;

	mutex_lock(&uvc_driver.ctrl_mutex);
	list_for_each_entry(info, &uvc_driver.controls, list) {
		if (memcmp(info->entity, mapping->entity, 16) ||
			info->selector != mapping->selector)
			continue;

		if (info->size * 8 < mapping->size + mapping->offset) {
			uvc_trace(UVC_TRACE_CONTROL, "Mapping '%s' would "
				"overflow control " UVC_GUID_FORMAT "/%u\n",
				mapping->name, UVC_GUID_ARGS(info->entity),
				info->selector);
			goto end;
		}

		/* Check if the list contains a mapping matching the new one.
		 * Bail out if it does.
		 */
		list_for_each_entry(map, &info->mappings, list) {
			if (map->id == mapping->id) {
				uvc_trace(UVC_TRACE_CONTROL, "Mapping '%s' is already "
					"defined.\n", mapping->name);
				goto end;
			}
		}

		mapping->ctrl = info;
		list_add_tail(&mapping->list, &info->mappings);
		uvc_trace(UVC_TRACE_CONTROL, "Adding mapping %s to control "
			UVC_GUID_FORMAT "/%u.\n", mapping->name,
			UVC_GUID_ARGS(info->entity), info->selector);

		break;
	}
end:
	mutex_unlock(&uvc_driver.ctrl_mutex);
}

/*
 * Initialize device controls.
 */
int uvc_ctrl_init_device(struct uvc_device *dev)
{
	struct uvc_control_info *info;
	struct uvc_control *ctrl;
	struct uvc_entity *entity;
	unsigned int i;

	/* Walk the entities list and instantiate controls */
	list_for_each_entry(entity, &dev->entities, list) {
		unsigned int bControlSize = 0, ncontrols = 0;
		__u8 *bmControls = NULL;

		if (entity->type == VC_EXTENSION_UNIT) {
			bmControls = entity->extension.bmControls;
			bControlSize = entity->extension.bControlSize;
		} else if (entity->type == VC_PROCESSING_UNIT) {
			bmControls = entity->processing.bmControls;
			bControlSize = entity->processing.bControlSize;
		} else if (entity->type == ITT_CAMERA) {
			bmControls = entity->camera.bmControls;
			bControlSize = entity->camera.bControlSize;
		}

		for (i = 0; i < bControlSize; ++i)
			ncontrols += hweight8(bmControls[i]);

		if (ncontrols == 0)
			continue;

		entity->controls = kzalloc(ncontrols*sizeof *ctrl, GFP_KERNEL);
		if (entity->controls == NULL)
			return -ENOMEM;

		entity->ncontrols = ncontrols;

		ctrl = entity->controls;
		for (i = 0; i < bControlSize * 8; ++i) {
			if (uvc_get_bit(bmControls, i) == 0)
				continue;

			ctrl->entity = entity;
			ctrl->index = i;
			ctrl++;
		}
	}

	/* Walk the controls info list and associate them with the device
	 * controls, then add the device to the global device list. This has
	 * to be done while holding the controls lock, to make sure
	 * uvc_ctrl_add_info() will not get called in-between.
	 */
	mutex_lock(&uvc_driver.ctrl_mutex);
	list_for_each_entry(info, &uvc_driver.controls, list)
		uvc_ctrl_add_ctrl(dev, info);

	list_add_tail(&dev->list, &uvc_driver.devices);
	mutex_unlock(&uvc_driver.ctrl_mutex);

	return 0;
}

/*
 * Cleanup device controls.
 */
void uvc_ctrl_cleanup_device(struct uvc_device *dev)
{
	struct uvc_entity *entity;
	unsigned int i;

	/* Remove the device from the global devices list */
	mutex_lock(&uvc_driver.ctrl_mutex);
	list_del(&dev->list);
	mutex_unlock(&uvc_driver.ctrl_mutex);

	list_for_each_entry(entity, &dev->entities, list) {
		for (i = 0; i < entity->ncontrols; ++i)
			kfree(entity->controls[i].data);

		kfree(entity->controls);
	}
}

void uvc_ctrl_init(void)
{
	struct uvc_control_info *ctrl = uvc_ctrls;
	struct uvc_control_info *cend = ctrl + ARRAY_SIZE(uvc_ctrls);
	struct uvc_control_mapping *mapping = uvc_ctrl_mappings;
	struct uvc_control_mapping *mend = mapping + ARRAY_SIZE(uvc_ctrl_mappings);

	for (; ctrl < cend; ++ctrl)
		uvc_ctrl_add_info(ctrl);

	for (; mapping < mend; ++mapping)
		uvc_ctrl_add_mapping(mapping);
}

