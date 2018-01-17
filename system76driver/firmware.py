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

# Products that will check for updates
CHECK_UPDATES = (
    'serw11',
)

# Products to flash firmware automatically
FLASH_FIRMWARE = (
    'bonw11',
    'bonw12',
    'bonw13',
    'galp2',
    'galp3',
    'gaze10',
    'gaze11',
    'gaze12',
    'kudu2',
    'kudu3',
    'kudu4',
    'lemu6',
    'lemu7',
    'lemu8',
    'orxp1',
    'oryp2',
    'oryp2-ess',
    'oryp3',
    'oryp3-ess',
    'oryp3-b',
    'serw9',
    'serw10',
    'serw11',
)

# Products with a second EC
HAS_EC2 = (
    'bonw11',
    'bonw12',
    'bonw13',
    'serw9',
    'serw10',
    'serw11',
)

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

def get_model():
    f = open("/sys/class/dmi/id/product_version")
    version = f.read().strip()
    f.close()
    return version

def get_bios_version():
    try:
        f = open("/sys/class/dmi/id/bios_version")
        version = f.read().strip()
        f.close()
        return version
    except:
        return ""

def get_ec_version(primary=True):
    try:
        ec = Ec(primary)
        version = ec.version()
        ec.close()
        return version
    except:
        return ""

def get_me_enabled():
    return path.exists("/dev/mei0")

def get_me_version():
    try:
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
    except:
        return ""

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

        if not path.isdir(CACHE_PATH):
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
    #user_session_pid = user_session_pids.split()[0]

    environ = ""
    for user_session_pid in user_session_pids.split():
        environ = subprocess.check_output(['cat', '/proc/' + str(user_session_pid)
                                      + '/environ']
                ).decode('utf-8').rstrip('\n')
        if len(environ) > 0:
            break

    return user_name, display_name, environ

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

def confirm_dialog(data):
    user_name, display_name, environ = get_user_session()

    if "DESKTOP_SESSION=gnome" in environ:
        data["desktop"] = 'gnome'
    elif "XDG_CURRENT_DESKTOP=pop:GNOME" in environ:
        data["desktop"] = 'gnome'
    elif "XDG_CURRENT_DESKTOP=ubuntu:GNOME" in environ:
        data["desktop"] = 'gnome'

    environment = [
        "FIRMWARE_DATA=" + json.dumps(data),
        "XAUTHORITY=/home/" + user_name + "/.Xauthority", #" + "/run/user/1000/gdm/Xauthority",
        "DISPLAY=" + display_name
    ]

    for var in environ.split("\00"):
        if len(var.split("=", maxsplit=1)) == 2:
            environment.append(str(var))

    return call_gui(user_name, display_name, environment)

def abort_dialog():
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

def success_dialog():
    user_name, display_name, environ = get_user_session()

    environment = [
        "FIRMWARE_SUCCESS=True",
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
        
        for component in ['bios_me', 'bios_set', 'me_hap', 'me_cr']:
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

def get_data(is_notification):
    model = get_model()
    flash = model in FLASH_FIRMWARE

    changelog = get_processed_changelog()

    latest = {
        "bios": "",
        "ec": "",
        "ec2": "",
        "me": ""
    }

    for entry in changelog:
        for component in latest.keys():
            if component in entry and not latest[component]:
                latest[component] = entry[component]

    if model in HAS_EC2:
        ec2 = get_ec_version(False)
    else:
        ec2 = ""

    enable_me = False
    for me_component in ['bios_me', 'me_hap', 'me_cr']:
        if latest[component] == 'true':
            # ME will be purposely enabled by next update.
            enable_me = True
    
    if get_me_enabled():
        me = get_me_version()
        if not enable_me:
            latest['me'] = latest['me'] + ' (disabled)'
    else:
        me = "disabled"
        if not enable_me:
            latest['me'] = 'disabled'

    current = {
        'bios': get_bios_version(),
        'ec': get_ec_version(True),
        'ec2': ec2,
        'me': me
    }

    return {
        'desktop': '',
        'notification': is_notification,
        'model': model,
        'flash': flash,
        'changelog': changelog,
        'current': current,
        'latest': latest
    }

def _run_firmware_updater(reinstall, is_notification):
    # For now, whitelist the models that can update firmware
    model = get_model()
    if not model in CHECK_UPDATES:
        log.info("Updates are not available for " + model + " yet.")
        return

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

            data = get_data(is_notification)

            current = data["current"]
            latest = data["latest"]

            needs_update = False
            for component in current.keys():
                if component == 'me' and current[component] == 'disabled' and 'disabled' in latest[component]:
                    pass
                elif current[component] and latest[component] and current[component] != latest[component]:
                    needs_update = True

            #Don't offer the update if its already installed
            if not needs_update:
                log.info('No new firmware to install.')
                if not reinstall:
                    return

            #Confirm installation with the user.
            if confirm_dialog(data) == 76:
                if path.isdir("/sys/firmware/efi"):
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
                    log.info("Not running in EFI mode, aborting firmware installation")
                    return
                
                # Prompt user if we can't automatically disable the ME.
                # bios_me: ME is configurable in bios.
                # bios_set: BIOS settings can be set automatically.
                if data['changelog'][0]:
                    latest_entry = data['changelog'][0]
                    if latest_entry['bios_me']:
                        if latest_entry['bios_me'] == 'True':
                            if latest_entry['bios_set']:
                                if latest_entry['bios_set'] == 'False':
                                    # Me is configurable, but default settings 
                                    # need to be loaded manually to disable.
                                    success_dialog()
                                # else:
                                #     ME is configurable and set/disabled by default.
            else:
                return

    else:
        if not is_notification:
            abort_dialog()
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
