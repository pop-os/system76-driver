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

import dbus

from os import path
import os

import subprocess

import json

import logging

log = logging.getLogger(__name__)

# Model definitions, by bios product name
# - flash - Products that will automatically install updates
# - ec - Product has embedded controller firmware
# - ec2 - Product has second embedded controller firmware
# - me - Product has management engine firmware

MODELS = {
    'addw1': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'bonw11': {
        "flash": True,
        "ec": True,
        "ec2": True,
        "me": True,
    },
    'bonw12': {
        "flash": True,
        "ec": True,
        "ec2": True,
        "me": True,
    },
    'bonw13': {
        "flash": True,
        "ec": True,
        "ec2": True,
        "me": True,
    },
    'darp5': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'galp2': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'galp3': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'galp3-b': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'galp3-c': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'gaze10': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'gaze11': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'gaze12': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'gaze13': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'gaze14': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'kudu2': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'kudu3': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'kudu4': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'kudu5': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'lemu6': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'lemu7': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'lemu8': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'meer4': {
        "flash": True,
        "ec": False,
        "ec2": False,
        "me": False,
    },
    'orxp1': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'oryp2': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'oryp2-ess': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'oryp3': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'oryp3-b': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'oryp3-ess': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'oryp4': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'oryp4-b': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'oryp5': {
        "flash": True,
        "ec": True,
        "ec2": False,
        "me": True,
    },
    'serw9': {
        "flash": True,
        "ec": True,
        "ec2": True,
        "me": True,
    },
    'serw10': {
        "flash": True,
        "ec": True,
        "ec2": True,
        "me": True,
    },
    'serw11': {
        "flash": True,
        "ec": True,
        "ec2": True,
        "me": True,
    },
    'serw11-b': {
        "flash": True,
        "ec": True,
        "ec2": True,
        "me": True,
    },
    'thelio-b1': {
        "flash": True,
        "ec": False,
        "ec2": False,
        "me": False,
    },
    'thelio-major-b1': {
        "flash": True,
        "ec": False,
        "ec2": False,
        "me": False,
    },
    'thelio-major-b1.1': {
        "flash": True,
        "ec": False,
        "ec2": False,
        "me": False,
    },
    'thelio-major-b2': {
        "flash": True,
        "ec": False,
        "ec2": False,
        "me": False,
    },
    'thelio-major-r1': {
        "flash": True,
        "ec": False,
        "ec2": False,
        "me": False,
    },
    'thelio-r1': {
        "flash": True,
        "ec": False,
        "ec2": False,
        "me": False,
    },
}

def get_model():
    f = open("/sys/class/dmi/id/product_version")
    version = f.read().strip()
    f.close()
    return version

def call_gui(environment):
    args = [
        "env"
        ] + environment + [
        '/usr/lib/system76-driver/system76-firmware-dialog',
    ]

    return subprocess.call(args)

def confirm_dialog(data):
    if os.environ.get("DESKTOP_SESSION") == "gnome":
        data["desktop"] = 'gnome'
    elif os.environ.get("XDG_CURRENT_DESKTOP") == "pop:GNOME":
        data["desktop"] = 'gnome'
    elif os.environ.get("XDG_CURRENT_DESKTOP") == "ubuntu:GNOME":
        data["desktop"] = 'gnome'

    environment = [
        "FIRMWARE_DATA=" + json.dumps(data),
    ]

    return call_gui(environment)

def error_dialog(message):
    environment = [
        "FIRMWARE_ERROR=" + message,
    ]

    return call_gui(environment)

def network_dialog():
    environment = [
        "FIRMWARE_NETWORK=1",
    ]

    return call_gui(environment)

def success_dialog(thelio_io):
    environment = [
        "FIRMWARE_SUCCESS=" + "2" if thelio_io else "1",
    ]

    return call_gui(environment)

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
                entry[component] = version[component]
        version_entries.append(entry)
    return version_entries

def get_data(model, model_data, iface, changelog, is_notification):
    _model, bios = iface.Bios()

    if model_data.get("ec"):
        _project, ec = iface.EmbeddedController(True)
    else:
        ec = ""

    if model_data.get("ec2"):
        _project, ec2 = iface.EmbeddedController(False)
    else:
        ec2 = ""

    me_enabled = False
    if model_data.get("me"):
        me_enabled, me_version = iface.ManagementEngine()
        if me_enabled:
            me = me_version
        else:
            me = "disabled"
    else:
        me = ""

    current = {
        'bios': bios,
        'ec': ec,
        'ec2': ec2,
        'me': me
    }

    latest = {
        "bios": "",
        "ec": "",
        "ec2": "",
        "me": ""
    }

    for entry in changelog:
        if (entry.get("bios_me") and not me_enabled) or entry.get("me_hap") or entry.get("me_cr"):
            entry["me"] = "disabled"
        for component in latest.keys():
            if component in entry and not latest[component]:
                latest[component] = entry[component]

    return {
        'desktop': '',
        'notification': is_notification,
        'model': model,
        'flash': model_data.get("flash"),
        'changelog': changelog,
        'current': current,
        'latest': latest
    }

def _run_firmware_updater(reinstall, is_notification, thelio_io):
    # For now, whitelist the models that can update firmware
    model = get_model()
    model_data = MODELS.get(model)
    if not model_data:
        message = "Updates are currently unavailable for " + model
        log.info(message)
        if not is_notification:
            error_dialog(message)
        return

    bus = dbus.SystemBus()
    proxy = bus.get_object('com.system76.FirmwareDaemon', '/com/system76/FirmwareDaemon')
    iface = dbus.Interface(proxy, dbus_interface='com.system76.FirmwareDaemon')

    if thelio_io:
        try:
            digest, revision = iface.ThelioIoDownload()
        except Exception:
            message = "Failed to download firmware for Thelio Io"
            log.exception(message)
            if not is_notification:
                network_dialog()
            return

        try:
            devices = iface.ThelioIoList()
        except Exception:
            message = "Failed to list Thelio Io devices"
            log.exception(message)
            if not is_notification:
                error_dialog(message)
            return

        needs_update = False
        current = {}
        latest = {}
        for dev in devices:
            dev_name = "Thelio Io #" + str(len(current) + 1)
            current[dev_name] = str(devices[dev])
            if not current[dev_name]:
                # Hack to ensure that the UI remains consistent but updates are
                # always available and applied
                current[dev_name] = "0.0.0"
            latest[dev_name] = str(revision)
            if current[dev_name] != latest[dev_name]:
                needs_update = True

        #Don't offer the update if its already installed
        if not needs_update:
            log.info('No new firmware to install.')
            if not reinstall:
                return

        #Confirm installation with the user.
        data = {
            'desktop': '',
            'notification': is_notification,
            'model': 'thelio-io',
            'flash': True,
            'changelog': {},
            'current': current,
            'latest': latest,
        }
        if confirm_dialog(data) == 76:
            try:
                iface.ThelioIoUpdate(digest)
            except Exception:
                message = "Failed to install Thelio Io firmware"
                log.exception(message)
                error_dialog(message)
                return

            success_dialog(thelio_io)
        else:
            return

        log.info("Updated Thelio Io firmware.")
    else:
        try:
            digest, changelog_json = iface.Download()
            changelog = process_changelog(json.loads(changelog_json))
        except Exception:
            message = "Failed to download firmware for " + model
            log.exception(message)
            if not is_notification:
                network_dialog()
            return

        data = get_data(model, model_data, iface, changelog, is_notification)

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

                iface.Schedule(digest)

                if success_dialog(thelio_io) == 76:
                    log.info("Restarting computer")
                    subprocess.call(["reboot"])
            else:
                message = "Not running in EFI mode, aborting firmware installation"
                log.info(message)
                error_dialog(message)
                return
        else:
            return

        log.info("Installed firmware updater to boot partition. Firmware update will run on next boot.")

def run_firmware_updater(reinstall=None, notification=False, thelio_io=False):
    try:
        ret = _run_firmware_updater(reinstall, notification, thelio_io)
        return ret
    except Exception:
        log.exception('Error calling _run_firmware_updater()')
