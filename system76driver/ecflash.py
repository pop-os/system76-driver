import os

class Ec:
    def __init__(self, primary=True):
        self.fd = os.open("/dev/port", os.O_RDWR)

        if primary:
            self.data_port = 0x62
            self.cmd_port = 0x66
        else:
            self.data_port = 0x68
            self.cmd_port = 0x6c

        chip_id = self.id()
        if chip_id != 0x8587:
            raise Exception("EC: Unknown ID: {:04X}".format(chip_id))

    def close(self):
        os.close(self.fd)

    # Read one byte from a port
    def inb(self, port):
        os.lseek(self.fd, port, os.SEEK_SET)
        data = os.read(self.fd, 1)
        return data[0]

    # Write one byte to a port
    def outb(self, port, data):
        os.lseek(self.fd, port, os.SEEK_SET)
        os.write(self.fd, bytearray([data]))

    # Get the Super I/O chip ID
    def id(self):
        self.outb(0x2e, 0x20);
        a = self.inb(0x2f);
        self.outb(0x2e, 0x21);
        b = self.inb(0x2f);
        return (a << 8) | b

    # Write a one byte command to the EC
    def cmd(self, data):
        i = 1000000
        while self.inb(self.cmd_port) & 0x2 == 0x2 and i > 0:
            i -= 1

        if i == 0:
            raise Exception("EC: Failed to send command {:02X}".format(data))
        else:
            self.outb(self.cmd_port, data)

    # Read one byte from the EC
    def read(self):
        i = 1000000
        while self.inb(self.cmd_port) & 0x1 == 0 and i > 0:
            i -= 1

        if i == 0:
            raise Exception("EC: Failed to read")
        else:
            return self.inb(self.data_port)

    # Write one data byte to the EC
    def write(self, data):
        i = 1000000
        while self.inb(self.cmd_port) & 0x2 == 0x2 and i > 0:
            i -= 1

        if i == 0:
            raise Exception("EC: Failed to write {:02X}".format(data))
        else:
            self.outb(self.data_port, data)

    # Empty the EC data buffer
    def flush(self):
        while self.inb(self.cmd_port) & 0x1 == 0x1:
            self.inb(self.data_port)

    # Get an EC parameter
    def get_param(self, param):
        self.cmd(0x80)
        self.write(param)
        return self.read()

    # Set an EC parameter
    def set_param(self, param, data):
        self.cmd(0x81)
        self.write(param)
        self.write(data)

    # Read a string from the EC
    def get_str(self, index):
        string = ""

        self.cmd(index)
        for i in range(0, 256):
            byte = chr(self.read())
            if byte == '$':
                break
            else:
                string += byte

        return string

    # Get the EC size
    def size(self):
        self.flush()
        if self.get_param(0xE5) == 0x80:
            return 128 * 1024
        else:
            return 64 * 1024

    # Get the EC project
    def project(self):
        self.flush()
        return self.get_str(0x92)

    # Get the EC version
    def version(self):
        self.flush()
        return "1." + self.get_str(0x93)
