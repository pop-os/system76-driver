#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Controls driver installation

import ubuntuversion
import model
import sound
import feisty_ata_fix
import acpi
import hotkey
import uvc
import ricoh_cr
import detect
import usplash
import hardy_led
import fprint

## KEEP ALL MODELS IN ALPHABETICAL ORDER

def installDrivers():
    """This function installs the appropriate drivers for each machine"""
    
    global nodrivers
    nodrivers = "false"
    modelname = model.determine_model()
    version = ubuntuversion.release()
    arch = detect.arch()
    
    if version == ('8.04.1'):
        version = '8.04'
    
    if modelname == ('bonp1'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            sound.alsa6()
        elif version == ('7.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('bonp2'):
        if version == ('8.04'):
            sound.alsa10()
            uvc.camera()
            fprint.install()
            acpi.osiNotWindows()
        elif verison == ('8.10'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('daru1'):
        if version == ('6.06'):
            sound.alsa6()
        elif version == ('6.10'):
            sound.alsa6()
        elif version == ('7.04'):
            feisty_ata_fix.piix()
            acpi.acpi1()
            hotkey.daru1_monitor_switch()
        elif version == ('7.10'):
            acpi.acpi3()
            hotkey.daru1_monitor_switch()
        elif version == ('8.04'):
            acpi.acpi3()
            hotkey.daru1_monitor_switch()
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('daru2'):
        if version == ('7.04'):
            feisty_ata_fix.piix2()
            acpi.acpi2()
            acpi.daru2()
            sound.alsa4()
        elif version == ('7.10'):
            acpi.acpi3()
            acpi.daru2()
            sound.alsa4()
        elif version == ('8.04'):
            sound.alsa4()
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('daru3'):
        if version == ('8.04'):
            sound.alsa10()
            uvc.camera()
            fprint.install()
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp1'):
        if version == ('6.06'):
            sound.alsa6()
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            sound.alsa6()
            acpi.acpi1()
        elif version == ('7.10'):
            sound.alsa6()
            acpi.acpi3()
        elif version == ('8.04'):
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp2'):
        if version == ('6.06'):
            sound.alsa6()
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            sound.alsa6()
            acpi.acpi1()
        elif version == ('7.10'):
            sound.alsa6()
            acpi.acpi3()
        elif version == ('8.04'):
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp3'):
        if version == ('6.06'):
            sound.alsa6()
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            sound.alsa6()
            acpi.acpi1()
        elif version == ('7.10'):
            sound.alsa6()
            acpi.acpi3()
        elif version == ('8.04'):
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp5'):
        if version == ('7.04'):
            feisty_ata_fix.piix2()
            sound.alsa5()
            uvc.camera()
            acpi.acpi1()
            ricoh_cr.card_reader()
        elif version == ('7.10'):
            sound.alsa5()
            acpi.acpi3()
            ricoh_cr.card_reader()
        elif version == ('8.04'):
            sound.alsa9()
            hardy_led.install()
    elif modelname == ('gazv1'):
        nodrivers = "true"
        return nodrivers
    elif modelname == ('gazv2'):
        if version == ('6.06'):
            sound.alsa6()
        elif version == ('6.10'):
            sound.alsa6()
        elif version == ('7.04'):
            sound.alsa6()
            acpi.acpi1()
        elif version == ('7.10'):
            sound.alsa6()
            acpi.acpi3()
        elif version == ('8.04'):
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazv3'):
        if version == ('6.06'):
            sound.alsa6()
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            sound.alsa6()
            feisty_ata_fix.piix()
            acpi.acpi2()
        elif version == ('7.10'):
            sound.alsa6()
            acpi.acpi3()
        elif version == ('8.04'):
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazv4'):
        if version == ('6.06'):
            sound.alsa6()
        elif version == ('6.10'):
            sound.alsa6()
        elif version == ('7.04'):
            sound.alsa6()
            feisty_ata_fix.piix()
            acpi.acpi2()
        elif version == ('7.10'):
            sound.alsa6()
            acpi.acpi3()
        elif version == ('8.04'):
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazv5'):
        if version == ('7.04'):
            feisty_ata_fix.piix2()
            sound.alsa5()
            uvc.camera()
            acpi.acpi1()
            ricoh_cr.card_reader()
        elif version == ('7.10'):
            sound.alsa5()
            ricoh_cr.card_reader()
        elif version == ('8.04'):
            sound.alsa9()
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('koap1'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            acpi.acpi1()
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('meec1'):
        if version == ('8.04'):
            uvc.camera()
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('nonsystem76'):
        nodrivers = "true"
        return nodrivers
    elif modelname == ('panp4i'):
        if version == ('8.04'):
            uvc.camera()
            sound.alsa11()
    elif modelname == ('panp4n'):
        if version == ('8.04'):
            uvc.camera()
            fprint.install()
            sound.alsa11()
        elif verison == ('8.10'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panv2'):
        if version == ('6.06'):
            sound.alsa6()
        elif version == ('6.10'):
            sound.alsa6()
        elif version == ('7.04'):
            sound.alsa6()
            acpi.acpi1()
        elif version == ('7.10'):
            sound.alsa6()
        elif version == ('8.04'):
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panv3'):
        if version == ('7.04'):
            feisty_ata_fix.piix2()
            sound.alsa5()
            acpi.acpi1()
            ricoh_cr.card_reader()
        elif version == ('7.10'):
            sound.alsa5()
            ricoh_cr.card_reader()
        elif version == ('8.04'):
            sound.alsa9()
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ratv1'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            acpi.acpi1()
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ratv2'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            acpi.acpi1()
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ratv3'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            acpi.acpi1()
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ratv4'):
        if version == ('7.10'):
            sound.alsa7()
        elif version == ('8.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ratv5'):
        if version == ('7.10'):
            sound.alsa7()
        elif version == ('8.04'):
            sound.alsa8()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ratv6'):
        if version == ('8.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('sabv1'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            acpi.acpi1()
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('sabv2'):
        if version == ('6.06'):
            sound.alsa6()
        elif version == ('6.10'):
            sound.alsa6()
        elif version == ('7.04'):
            sound.alsa6()
            acpi.acpi1()
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('sabv3'):
        if version == ('7.10'):
            nodrivers = "true"
            return nodrivers
    elif modelname == ('serp1'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            acpi.acpi1()
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('serp2'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            acpi.acpi1()
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('serp3'):
        if version == ('7.04'):
            acpi.acpi1()
            sound.alsa5()
        elif version == ('7.10'):
            if arch == ('x86'):
                sound.alsa5()
                ricoh_cr.card_reader()
            else:
                usplash.gutsy_64_nvidia()
                sound.alsa5()
                ricoh_cr.card_reader()
        elif version == ('8.04'):
            sound.alsa9()
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('serp4'):
        if version == ('7.04'):
            acpi.acpi1()
            sound.alsa5()
        elif version == ('7.10'):
            if arch == ('x86'):
                sound.alsa5()
                ricoh_cr.card_reader()
            else:
                usplash.gutsy_64_nvidia()
                sound.alsa5()
                ricoh_cr.card_reader()
        elif version == ('8.04'):
            sound.alsa9()
            hardy_led.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('serp5'):
        if version == ('8.10'):
            sound.alsa10()
            fprint.install()
            acpi.osiNotWindows()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('wilp1'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('wilp2'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('wilp3'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('wilp5'):
        if version == ('7.10'):
            if arch == ('x86'):
                nodrivers = "true"
                return nodrivers
            else:
                usplash.gutsy_64_nvidia()
        elif version == ('8.04'):
            nodrivers = "true"
            return nodrivers
    else:
        nodrivers = "true"
        return nodrivers
