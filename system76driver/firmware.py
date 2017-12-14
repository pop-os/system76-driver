# system76-driver: Universal driver for System76 computers
# Copyright (C) 2005-2017 System76, Inc.
#
# This file is part of `system76-driver`.
#
# `system76-driver` is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# `system76-driver` is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with `system76-driver`; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
Firmware updater for System76 computers.
"""

from .ecflash import Ec

import nacl.encoding
import nacl.signing
import nacl.hash
import hashlib

import ssl
from urllib import request

import tarfile
import io
import tempfile

import array
import fcntl
from os import path
import os
import shutil
import struct
import uuid

from .mockable import SubProcess
import subprocess

import json

import logging

log = logging.getLogger(__name__)

FIRMWARE_URI = 'https://firmware.system76.com/master/'

CACHE_PATH = "/var/cache/system76-firmware"

FIRMWARE_SET_NEXT_BOOT = """#!/bin/bash -e

if [ "$EUID" != "0" ]
then
    echo "You are not running as root" >&2
    exit 1
fi

EFIDEV="$(findmnt -n /boot/efi -o SOURCE)"
EFINAME="$(basename "${EFIDEV}")"
EFISYS="$(readlink -f "/sys/class/block/${EFINAME}")"
EFIPART="$(cat "${EFISYS}/partition")"
DISKSYS="$(dirname "${EFISYS}")"
DISKNAME="$(basename "${DISKSYS}")"
DISKDEV="/dev/${DISKNAME}"

echo -e "\e[1mCreating Boot1776 on "${DISKDEV}" "${EFIPART}" \e[0m" >&2
efibootmgr -B -b 1776 || true
efibootmgr -C -b 1776 -d "${DISKDEV}" -p "${EFIPART}" -l '\\system76-firmware-update\\boot.efi' -L "system76-firmware-update"

echo -e "\e[1mSetting BootNext to 1776\e[0m" >&2
efibootmgr -n 1776

echo -e "\e[1mInstalled system76-firmware-update\e[0m" >&2
efibootmgr -v
"""

def get_ec_version(primary=True):
    try:
        ec = Ec(primary)
        version = ec.version()
        ec.close()
        return version
    except:
        return ""

def get_bios_version():
    f = open("/sys/class/dmi/id/bios_version")
    version = f.read().strip()
    f.close()
    return version

def get_me_version():
    mei_fd = os.open("/dev/mei0", os.O_RDWR)

    # Connect to ME version interface
    _id = uuid.UUID('8e6a6715-9abc-4043-88ef-9e39c6f63e0f')
    buf = array.array('b', _id.bytes_le)
    fcntl.ioctl(mei_fd, 0xc0104801, buf, 1)

    # Send FW version request
    os.write(mei_fd, struct.pack("I", 0x000002FF))

    # Receive FW version response
    fw_ver = struct.unpack("4BH2B2HH2B2HH2B2H", os.read(mei_fd, 28))

    os.close(mei_fd)

    # Return FW software version
    return "%d.%d.%d.%d" % (fw_ver[5], fw_ver[4], fw_ver[8], fw_ver[7])

def needs_update(new_bios_version, new_ec_version):
    if not new_bios_version:
        log.warn("Couldn't get the new bios version from changelog!")
    elif new_bios_version != get_bios_version():
        return True
    if not new_ec_version:
        log.warn("Couldn't get the new ec version from changelog!")
    elif new_ec_version != get_ec_version():
        return True
    return False

def get_firmware_id():
    f = open("/sys/class/dmi/id/product_version")
    model = f.read().strip()
    f.close()

    try:
        ec = Ec()
        project = ec.project()
        ec.close()
    except:
        project = "none"

    project_hash = nacl.hash.sha256(bytes(project, 'utf8'), encoder=nacl.encoding.HexEncoder).decode('utf-8')

    return "{}_{}".format(model, project_hash)

def get_url(filename):
    return '{}{}'.format(FIRMWARE_URI, filename)

def get_file(filename, cache=None):
    if cache:
        log.info("Fetching {} with cache {}".format(filename, cache))

        if not os.path.isdir(CACHE_PATH):
            log.info("Creating cache directory at {}".format(cache))
            os.mkdir(CACHE_PATH)

        p = path.join(cache, filename)
        if path.isfile(p):
            f = open(p, 'rb')
            return f.read()
        else:
            data = get_file(filename)
            f = open(p, 'wb')
            f.write(data)
            f.close()
            return data
    else:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.options |= ssl.OP_NO_COMPRESSION
        #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        #ssl_options = (ssl.OP_NO_SSLv2
        #              | ssl.OP_NO_SSLv3
        #              | ssl.OP_NO_TLSv1
        #              | ssl.OP_NO_TLSv1_1
        #              | ssl.OP_NO_COMPRESSION)
        #ssl_context.options |= ssl_options
        ssl_context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384')
        ssl_context.verify_mode=ssl.CERT_REQUIRED
        ssl_context.check_hostname = True

        ssl_context.load_verify_locations("/usr/share/system76-driver/ssl/certs/firmware.system76.com.cert")

        request.urlcleanup()
        try:
            url = get_url(filename)
            f = request.urlopen(url, context=ssl_context)
            return f.read()
        except:
            log.exception("Failed to open secure TLS connection:\n"
                          + "    possible Man-in-the-Middle attack or outdated certificate.\n"
                          + "    Updating to the latest driver may solve the issue.")


def get_hashed_file(filename, decode=None):
    hashed_file = get_file(filename, CACHE_PATH)
    if hashed_file is not None:
        digest = hashlib.sha384(hashed_file).hexdigest()
        if filename == digest:
            if decode is not None:
                return hashed_file.decode(decode)
            else:
                return hashed_file
        else:
            log.exception("Got bad checksum for file: '"
                          + get_url(filename)
                          + "\nExpected: " + filename
                          + "\nGot: " + digest)
            raise Exception
    else:
        log.error("Hashed file not found: " + filename)

def get_signed_file(filename, key='/usr/share/system76-driver/keys/verify', decode=None):
    # DO NOT CACHE - get_signed_file is used to fetch the manifest location.
    # There is no way to verify ahead of time that what's on disk matches repo.
    signed_file = get_file(filename)
    key_file = open(key, 'rb')
    verify_key = nacl.signing.VerifyKey(key_file.read(), encoder=nacl.encoding.HexEncoder)
    if signed_file is not None:
        try:
            f = verify_key.verify(signed_file)
            log.info("Verified manifest signature...")
            if decode is not None:
                return f.decode(decode)
            else:
                return f
        except nacl.exceptions.BadSignatureError:
            log.exception("Bad manifest signature! Aborting...")
            raise nacl.exceptions.BadSignatureError
            return
    else:
        log.error("Signed file not found: " + filename)


class Tarball():
    def __init__(self, filename):
        tarball = get_file(filename)
        self.tar = tarfile.open(fileobj=io.BytesIO(tarball))

    def extract(self, directory):
        os.chmod(directory, 0o700)
        self.tar.extractall(directory)
        os.chmod(directory, 0o500)

    def extractfile(self, f):
        return self.tar.extractfile(f)


class HashedTarball(Tarball):
    def __init__(self, filename):
        hashed_tarball = get_hashed_file(filename)
        self.tar = tarfile.open(fileobj=io.BytesIO(hashed_tarball))


class SignedTarball(Tarball):
    def __init__(self, filename):
        try:
            signed_tarball = get_signed_file(filename).read()
            self.tar = tarfile.open(fileobj=io.BytesIO(signed_tarball))
        except nacl.exceptions.BadSignatureError:
            log.exception("Bad firmware signature! Aborting...")
            raise nacl.exceptions.BadSignatureError


class SignedManifest():
    def __init__(self):
        manifest_lookup = get_signed_file('manifest.sha384sum.signed', decode='utf-8')
        if manifest_lookup is not None:
            try:
                # Verify checksum signature, then look up manifest by checksum.
                self.manifest = json.loads(get_hashed_file(manifest_lookup, decode='utf-8'))
            except nacl.exceptions.BadSignatureError:
                log.exception("Bad manifest signature! Aborting...")
                raise nacl.exceptions.BadSignatureError
            except:
                log.exception("Could not get manifest.")
        else:
            log.exception("Could not locate manifest.")
            raise Exception

    def lookup(self, filename):
        return self.manifest["files"][filename]


def get_user_session():
    user_name = subprocess.check_output(
                    "who | awk -v vt=tty$(fgconsole) '$0 ~ vt {print $1}'",
                    shell=True
                ).decode('utf-8').rstrip('\n')

    display_name = subprocess.check_output(
                    "who | awk -v vt=tty$(fgconsole) '$0 ~ vt {print $5}'",
                    shell=True
                ).decode('utf-8').rstrip('\n').lstrip('(').rstrip(')')

    user_pid = subprocess.check_output(
                    "who -u | awk -v vt=tty$(fgconsole) '$0 ~ vt {print $6}'",
                    shell=True
                ).decode('utf-8').rstrip('\n')

    user_session_pids = subprocess.check_output(['pgrep', '-P', user_pid]
                ).decode('utf-8').rstrip('\n')
    user_session_pid = user_session_pids.split()[0]

    environ = subprocess.check_output(['cat', '/proc/' + str(user_session_pid)
                                      + '/environ']
                ).decode('utf-8').rstrip('\n')

    return user_name, display_name, environ

def create_environment(is_notification, user_name, display_name, environ):
    if "DESKTOP_SESSION=gnome" in environ:
        desktop_env = 'gnome'
    else:
        desktop_env = ''

    environment = [
        "NOTIFICATION_ENVIRONMENT=" + desktop_env,
        "IS_NOTIFICATION=" + str(is_notification),
        "FIRMWARE_CHANGELOG=" + json.dumps(get_processed_changelog()),
        "FIRMWARE_CURRENT=" + json.dumps({
            'bios': get_bios_version(),
            'ec': get_ec_version(True),
            'ec2': get_ec_version(False),
            'me': get_me_version()
        }),
        "XAUTHORITY=/home/" + user_name + "/.Xauthority", #" + "/run/user/1000/gdm/Xauthority",
        "DISPLAY=" + display_name
    ]

    for var in environ.split("\00"):
        if len(var.split("=", maxsplit=1)) == 2:
            environment.append(str(var))

    return environment

def call_gui(user_name, display_name, environment):
    if len(user_name) == 0 or len(display_name) == 0:
        return

    args = [
        "sudo"
        ] + environment + [
        "su",
        user_name,
        "-c",
        '/usr/lib/system76-driver/system76-firmware-dialog',
    ]

    return subprocess.call(args)

def confirm_dialog(is_notification=False):
    user_name, display_name, environ = get_user_session()
    environment = create_environment(is_notification, user_name, display_name, environ)
    return call_gui(user_name, display_name, environment)

def abort_dialog(is_notification=False):
    if is_notification:
        return

    user_name, display_name, environ = get_user_session()

    environment = [
        "FIRMWARE_ABORT=True",
        "XAUTHORITY=/home/" + user_name + "/.Xauthority", #" + "/run/user/1000/gdm/Xauthority",
        "DISPLAY=" + display_name
    ]

    for var in environ.split("\00"):
        if len(var.split("=", maxsplit=1)) == 2:
            environment.append(str(var))

    return call_gui(user_name, display_name, environment)

def set_next_boot():
    handle, name = tempfile.mkstemp()
    f = open(handle, 'w')
    f.write(FIRMWARE_SET_NEXT_BOOT)
    f.close()
    os.chmod(name, 0o500)
    try:
        SubProcess.check_output(['sudo', name])
    except:
        return

def download_from_repo():
    try:
        manifest = SignedManifest()
    except:
        log.error("Failed to get firmware manifest. Aborting!")
        return None, None

    #Download the latest updater and firmware for this machine and verify source.
    firmware = HashedTarball(manifest.lookup(get_firmware_id() + '.tar.xz'))
    updater = HashedTarball(manifest.lookup('system76-firmware-update.tar.xz'))
    return firmware, updater

def get_changelog(tempdirname):
    with open(path.join(tempdirname, 'firmware', 'changelog.json')) as f:
        changelog = json.load(f)
        return changelog

#Submit the subset of json relevant to the GUI (And add the detected version)
def process_changelog(changelog):
    if changelog['versions']:
        versions = changelog['versions']
    else:
        return None, None

    version_entries = []
    for version in versions:
        entry = {}
        for component in ['description', 'bios', 'ec', 'ec2', 'me']:
            if component in version.keys():
                entry[component] = str(version[component])
        version_entries.append(entry)
    return version_entries

def get_processed_changelog():
    firmware, updater = download_from_repo()

    if firmware and updater:
        with firmware.extractfile('./changelog.json') as f:
            c = f.read().decode('utf-8')
            changelog = json.loads(c)
            return process_changelog(changelog)


def _run_firmware_updater(reinstall, is_notification):
    # Download the manifest and check that it is signed by the private master key.
    # The public master key is pinned in our driver.
    # Then download the firmware and check the checksum against the manifest.
    firmware, updater = download_from_repo()

    if firmware and updater:
        #Extract to temporary directory and set safe permissions.
        with tempfile.TemporaryDirectory() as tempdirname:
            updater.extract(tempdirname)
            os.mkdir(path.join(tempdirname, 'firmware'))
            firmware.extract(path.join(tempdirname, 'firmware'))

            #Process changelog and component versions
            changelog = get_changelog(tempdirname)
            version = changelog['versions'][0]

            if 'bios' in version.keys():
                bios_version = version['bios']
            else:
                bios_version = ''

            if 'ec' in version.keys():
                ec_version = version['ec']
            else:
                ec_version = ''

            update_needed = needs_update(bios_version, ec_version)

            #Don't offer the update if its already installed
            if not update_needed:
                log.info('No new firmware to install.')
                if not reinstall:
                    return

            #Confirm installation with the user.
            if confirm_dialog(is_notification) == 76:
                log.info("Setting up firmware installation.")

                #Remove old firmware updater
                try:
                    shutil.rmtree('/boot/efi/system76-firmware-update')
                except:
                    pass

                #Install firmware to /efi/boot and set boot.efi on next boot.
                shutil.copytree(tempdirname, '/boot/efi/system76-firmware-update')
                set_next_boot()
            else:
                return

    else:
        abort_dialog(is_notification)
        return
    log.info("Installed firmware updater to boot partition. Firmware update will run on next boot.")

def run_firmware_updater(reinstall=None, notification=False):
    # Make sure we're running as root.  Should fail anyway
    if os.getuid() != 0:
        return
    try:
        ret = _run_firmware_updater(reinstall, notification)
        return ret
    except Exception:
        log.exception('Error calling _run_firmware_updater()')
