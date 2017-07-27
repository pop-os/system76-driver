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

from os import path
import os
import shutil

from .mockable import SubProcess
import subprocess

import json

import logging

log = logging.getLogger(__name__)

FIRMWARE_URI = 'https://firmware.system76.com/develop/'

FIRMWARE_SET_NEXT_BOOT = """#!/bin/bash -e

if [ "$EUID" != "0" ]
then
    echo "You are not running as root" >&2
    exit 1
fi

DISK="$(findmnt -n /boot/efi -o 'MAJ:MIN' | cut -d ':' -f 1)"
PART="$(findmnt -n /boot/efi -o 'MAJ:MIN' | cut -d ':' -f 2)"
DEV="/dev/$(lsblk -n -o 'KNAME,MAJ:MIN' | grep "${DISK}:0" | cut -d ' ' -f 1)"

echo -e "\e[1mCreating Boot1776\e[0m" >&2
efibootmgr -B -b 1776 || true
efibootmgr -C -b 1776 -d "${DEV}" -p "${PART}" -l '\\system76-firmware-update\\boot.efi' -L "System76 Firmware Update"

echo -e "\e[1mSetting BootNext\e[0m" >&2
efibootmgr -n 1776

echo -e "\e[1mInstalled system76-firmware-update\e[0m" >&2
"""

def get_ec_version():
    ec = Ec()
    version = ec.version()
    ec.close()
    return version
    
def get_bios_version():
    f = open("/sys/class/dmi/id/bios_version")
    version = f.read().strip()
    f.close()
    return version
    
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

    ec = Ec()
    project = ec.project()
    ec.close()

    project_hash = nacl.hash.sha256(bytes(project, 'utf8'), encoder=nacl.encoding.HexEncoder).decode('utf-8')

    return "{}_{}".format(model, project_hash)

def get_url(filename):
    print('{}{}'.format(FIRMWARE_URI, filename))
    return '{}{}'.format(FIRMWARE_URI, filename)

def get_file(filename):
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
    
    ssl_context.load_verify_locations("ssl/certs/firmware.system76.com.crt") 

    request.urlcleanup()
    try:
        return request.urlopen(get_url(filename), context=ssl_context).read()
    except:
        log.exception("Failed to open secure TLS connection: \
                       possible Man-in-the-Middle attack or outdated certificate. \
                       Updating to the latest driver may solve the issue.")

def get_hashed_file(filename):
    hashed_file = get_file(filename)
    digest = hashlib.sha384(hashed_file).hexdigest()
    if filename == digest:
        return hashed_file
    else:
        log.exception("Got bad checksum for file: '" 
                      + get_url(filename)
                      + "\nExpected: " + filename
                      + "\nGot: " + digest)
        raise Exception

def get_signed_file(filename, key=open('verify', 'rb')):
    signed_file = get_file(filename)
    key_file = key
    verify_key = nacl.signing.VerifyKey(key_file.read(), encoder=nacl.encoding.HexEncoder)
    try:
        f = verify_key.verify(signed_file)
        log.info("Verified manifest signature...")
        return f
    except nacl.exceptions.BadSignatureError:
        log.exception("Bad manifest signature! Aborting...")
        raise nacl.exceptions.BadSignatureError
        return
   

class Tarball():
    def __init__(self, filename):
        tarball = get_file(filename)
        self.tar = tarfile.open(fileobj=io.BytesIO(tarball))
        
    def extract(self, directory):
        os.chmod(directory, 0o700)
        self.tar.extractall(directory)
        os.chmod(directory, 0o500)


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
        try:
            # Verify checksum signature, then look up manifest by checksum.
            manifest_lookup = get_signed_file('manifest.sha384sum.signed').decode('utf-8')
            self.manifest = get_hashed_file(manifest_lookup)
        except nacl.exceptions.BadSignatureError:
            log.exception("Bad manifest signature! Aborting...")
            raise nacl.exceptions.BadSignatureError
        except:
            log.exception("Could not get manifest.")
        
    def lookup(self, filename):
        for line in self.manifest.decode().split('\n'):
            if filename in line:
                split = line.split(': ')
                return split[1]


def confirm_dialog(changes_list=['No Changes']):
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
            
    if "DESKTOP_SESSION=gnome" in environ:
        desktop_env = 'gnome'
    #changes = ["Quieter fan curve", "Added HyperThreading toggle"]
    changes = changes_list
    bios_changes = ["Quieter fan curve", "Added HyperThreading toggle"]
    ec_changes = ["Quieter fan curve"]

    if len(user_name) == 0 or len(display_name) == 0:
        return

    args = [
        "sudo",
        "DESKTOP_SESSION=" + desktop_env,
        "FIRMWARE_CHANGES=" + json.dumps(changes),
        "BIOS_CHANGES=" + json.dumps(bios_changes),
        "EC_CHANGES=" + json.dumps(ec_changes),
        "su",
        user_name,
        "XAUTHORITY=/home/" + user_name + "/.Xauthority", 
        "DISPLAY=" + display_name,
        "-c",
        './system76-firmware-dialog',
    ]

    return subprocess.call(args)

def read_changelog(f):
    version_token = None
    indent_level = 0
    section = None
    sections = []
    for line in f.readlines():
        #parse 'version'
        if not version_token:
            if line == 'versions:\n':
                version_token = line
                indent_level = 6
        else:
            #Parse each section.  Indented section starts with a '-'
            if line[4] == '-':
                if section:
                    sections.append(section)
                section = {'description': None, 'bios': None, 'ec': None, 'ec2': None}
            if True:
                section_line = line[indent_level:]
                for key in ['description', 'bios', 'ec', 'ec2']:
                    key_str = key + ': '
                    if (section_line.startswith(key_str) and len(section_line) > len(key_str)):
                        value = section_line[len(key_str):].strip('\n')
                        section[key] = value
    sections.append(section)
    return sections

def get_changes_list(changelog_entries, current_bios, current_ec, current_ec2=None):
    found_bios = False
    found_ec = False
    found_ec2 = False
    changes_list = []
    if not current_ec2:
        found_ec2 = True
    if not current_ec:
        pass
    if not current_bios:
        pass
    for entry in changelog_entries:
        if True:
            if entry['bios'] and current_bios:
                if current_bios >= entry['bios']:
                    found_bios = True
            if entry['ec'] and current_ec:
                if current_ec >= entry['ec']:
                    found_ec = True
            if entry['ec2'] and current_ec2:
                if current_ec2 >= entry['ec2']:
                    found_ec2 = True
        if not (found_bios and found_ec and found_ec2):
            changes_list.append(entry['description'])
        else:
            break
    if changes_list == []:
        changes_list.append('No Changes')
    return changes_list
            

def set_next_boot():
    handle, name = tempfile.mkstemp()
    f = open(handle, 'w')
    f.write(FIRMWARE_SET_NEXT_BOOT)
    f.close()
    os.chmod(name, 0o500)
    try:
        output = SubProcess.check_output(['sudo', name])
    except:
        return

def _run_firmware_updater(model):
    # Download the manifest and check that it is signed by the private master key.
    # The public master key is pinned in our driver.
    # Then download the firmware and check the checksum against the manifest.
    manifest = SignedManifest()
    
    #Download the latest updater and firmware for this machine and verify source.
    firmware = HashedTarball(manifest.lookup(get_firmware_id()))
    updater = HashedTarball(manifest.lookup('system76-firmware-update'))

    if updater and firmware:
        #Extract to temporary directory and set safe permissions.
        with tempfile.TemporaryDirectory() as tempdirname:
            updater.extract(tempdirname)
            os.mkdir(path.join(tempdirname, 'firmware'))
            firmware.extract(path.join(tempdirname, 'firmware'))
            
            #Process changelog and component versions
            with open(path.join(tempdirname, 'firmware', 'changelog.yaml')) as f:
                changelog_entries = read_changelog(f)
                
                #Don't offer the update if its already installed
                if not needs_update(changelog_entries[0]['bios'], changelog_entries[0]['ec']):
                    log.info('No new firmware to install.')
                    return
                    
                changes_list = get_changes_list(changelog_entries, get_bios_version(), get_ec_version())

            #Confirm installation with the user.
            if confirm_dialog(changes_list) == 0:
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
    log.info("Installed firmware updater to boot partition. Firmware update will run on next boot.")

def run_firmware_updater(model):
    try:
        return _run_firmware_updater(model)
    except Exception:
        log.exception('Error calling _run_firmware_updater(%r):', model)
