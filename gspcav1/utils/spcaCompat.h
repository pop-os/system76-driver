
#ifndef SPCA_COMPAT_H
#define SPCA_COMPAT_H

#if LINUX_VERSION_CODE < KERNEL_VERSION(2, 4, 24)
static inline void *video_get_drvdata(struct video_device *vdev)
{
    return vdev->priv;
}

static inline void video_set_drvdata(struct video_device *vdev, void *data)
{
    vdev->priv = data;
}

static inline struct video_device *video_device_alloc(void)
{
    struct video_device *vdev;

    vdev = kmalloc(sizeof(*vdev), GFP_KERNEL);
    if (NULL == vdev)
	return NULL;
    memset(vdev, 0, sizeof(*vdev));
    return vdev;
}

static inline void video_device_release(struct video_device *vdev)
{
    kfree(vdev);
}
#endif

#endif
