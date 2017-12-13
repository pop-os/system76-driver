import array
import fcntl
import os
import struct
import uuid

def get_me_version():
    mei_fd = os.open("/dev/mei0", os.O_RDWR)

    _id = uuid.UUID('8e6a6715-9abc-4043-88ef-9e39c6f63e0f')
    buf = array.array('b', _id.bytes_le)
    fcntl.ioctl(mei_fd, 0xc0104801, buf, 1)

    os.write(mei_fd, struct.pack("I", 0x000002FF))

    fw_ver = struct.unpack("4BH2B2HH2B2HH2B2H", os.read(mei_fd, 28))

    os.close(mei_fd)

    return "%d.%d.%d.%d" % (fw_ver[5], fw_ver[4], fw_ver[8], fw_ver[7])
