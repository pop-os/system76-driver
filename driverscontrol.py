#
#!/usr/bin/env python
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Controls driver installation

import ubuntuversion
import model
import sound
import misc
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
    if version == ('0.2'):
        version = '12.04'
    
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('bonp2'):
        if version == ('8.04'):
            audio = sound.alsa10
            video = uvc.camera
            finger = fprint.install
            power = acpi.osiNotWindows
            
            audio.install()
            video.install()
            finger.install()
            power.install()
        elif version == ('8.10'):
            audio = sound.alsa10
            video = uvc.camera
            finger = fprint.install
            power = acpi.osiNotWindows
            
            audio.install()
            video.install()
            finger.install()
            power.install()
        elif version == ('9.04'):
            finger = fprint.install
            power = acpi.osiNotWindows
            other = misc.linux_backports
            
            finger.install()
            power.install()
            other.install()
        elif version == ('9.10'):
            finger = fprint.installPackages()
            
            finger.install()
        elif version == ('10.04'):
            finger = fprint.installPackages()
            finger.install()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('bonp3'):
        if version == ('9.10'):
            power = acpi.os_linux
            finger = fprint.installUpek1
            other1 = misc.jme_nic
            other2 = misc.rm_aticatalyst
            
            power.install()
            finger.install()
            other1.install()
            other2.install()
        elif version == ('10.04'):
            fprint.installUpek1()
            acpi.os_linux()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('bonp4'):
        if version == ('10.10'):
            power = acpi.xhcihcdModule
            power.install()
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('bonp5'):
        if version == ('11.04'):
            power = acpi.pcie_aspm
            audio = sound.audioDevPPA
            power.install()
            audio.install()
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            finger = fprint.fingerprintGUI
            finger.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('daru1'):
        if version == ('6.06'):
            audio = sound.alsa6
            audio.install()
        elif version == ('6.10'):
            audio = sound.alsa6
            audio.install()
        elif version == ('7.04'):
            other = misc.piix
            power = acpi.acpi1
            keys = hotkey.daru1_monitor_switch
            other.install()
            power.install()
            keys.install()
        elif version == ('7.10'):
            power = acpi.acpi3
            keys = hotkey.daru1_monitor_switch()
            power.install()
            keys.install()
        elif version == ('8.04'):
            power = acpi.acpi3
            power.install()
            keys = hotkey.daru1_monitor_switch
            keys.install()
            led = hardy_led.install
            led.install()
        elif version == ('8.10'):
            keys = hotkey.daru1_touchpad_switch
            keys.install()
        elif version == ('9.04'):
            keys = hotkey.daru1_touchpad_switch
            keys.install()
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('daru2'):
        if version == ('7.04'):
            other = misc.piix2
            other.install()
            power = acpi.acpi2
            power.install()
            power1 = acpi.daru2()
            power1.install()
            audio = sound.alsa4
            audio.install()
        elif version == ('7.10'):
            power1 = acpi.acpi3
            power1.install()
            power2 = acpi.daru2
            power2.install()
            audio = sound.alsa4
            audio.install()
        elif version == ('8.04'):
            audio = sound.alsa4
            audio.install()
            led = hardy_led.install
            led.install()
        elif version == ('8.10'):
            audio = sound.alsa4
            audio.install()
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('daru3'):
        if version == ('8.04'):
            audio = sound.alsa10
            audio.install()
            video = uvc.camera
            video.install()
            finger = fprint.install
            finger.install()
        elif version == ('8.10'):
            audio = sound.alsa10
            audio.install()
            video = uvc.camera
            video.install()
            finger = fprint.install
            finger.install()
            power = acpi.acpi4
            power.install()
        elif version == ('9.04'):
            finger = fprint.install
            finger.install()
        elif version == ('9.10'):
            finger = fprint.installPackages
            finger.install()
        elif version == ('10.04'):
            finger = fprint.installPackages()
            finger.install()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            power = acpi.lemu1
            power.install()
        elif version == ('12.04'):
            finger = fprint.fingerprintGUI
            finger.install()
            power = acpi.lemu1
            power.install()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp1'):
        if version == ('6.06'):
            audio = sound.alsa6
            audio.install()
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            audio = sound.alsa6
            audio.install()
            power = acpi.acpi1
            power.install()
        elif version == ('7.10'):
            audio = sound.alsa6
            audio.install()
            power = acpi.acpi3
            power.install()
        elif version == ('8.04'):
            led = hardy_led.install
            led.install()
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp2'):
        if version == ('6.06'):
            audio = sound.alsa6
            audio.install()
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp5'):
        if version == ('7.04'):
            misc.piix2()
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
        elif version == ('8.10'):
            sound.alsa9()
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp6'):
        if version == ('10.10'):
            fprint.fingerprintGUI()
            acpi.xhcihcdModule()
            misc.gnomeThemeRace()
            acpi.pcie_aspm()
        elif version == ('11.04'):
            acpi.pcie_aspm()
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp7'):
        if version == ('12.04'):
            acpi.lemu1()
            misc.realtek_rts_bpp()
        else:
            nodrivers = "true"
            return nodrivers
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
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
            misc.piix()
            acpi.acpi2()
        elif version == ('7.10'):
            sound.alsa6()
            acpi.acpi3()
        elif version == ('8.04'):
            hardy_led.install()
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
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
            misc.piix()
            acpi.acpi2()
        elif version == ('7.10'):
            sound.alsa6()
            acpi.acpi3()
        elif version == ('8.04'):
            hardy_led.install()
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazv5'):
        if version == ('7.04'):
            misc.piix2()
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
        elif version == ('8.10'):
            sound.alsa9()
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazu1'):
        if version == ('8.04'):
            sound.alsa10()
            uvc.camera()
            uvc.quirks()
            fprint.install()
        elif version == ('8.10'):
            sound.alsa10()
            uvc.quirks()
            fprint.install()
        elif version == ('9.04'):
            uvc.quirks()
            fprint.install()
        elif version == ('9.10'):
            uvc.quirks()
            fprint.installPackages()
        elif version == ('10.04'):
            uvc.quirks()
            fprint.installPackages()
        elif version == ('10.10'):
            uvc.quirks()
        elif version == ('11.04'):
            uvc.quirks()
        elif version == ('11.10'):
            uvc.quirks()
        elif version == ('12.04'):
            uvc.quirks()
            fprint.fingerprintGUI()
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('lemu1'):
        if version == ('9.04'):
            uvc.lemur()
            acpi.lemu1()
        elif version == ('9.10'):
            uvc.lemur()
            acpi.lemu1()
            misc.jme_nic()
        elif version == ('10.04'):
            uvc.lemur()
            acpi.lemu1()
        elif version == ('10.10'):
            acpi.lemu1()
        elif version == ('11.04'):
            acpi.lemu1()
        elif version == ('11.10'):
            acpi.lemu1()
        elif version == ('12.04'):
            acpi.lemu1()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('lemu2'):
        if version == ('10.04'):
            uvc.lemur()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('lemu3'):
        if version == ('11.04'):
            acpi.lemu1()
        elif version == ('11.10'):
            acpi.lemu1()
        elif version == ('12.04'):
            acpi.lemu1()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('lemu4'):
        if version == ('11.10'):
            acpi.lemu1()
            misc.realtek_rts_bpp()
        elif version == ('12.04'):
            acpi.lemu1()
            misc.realtek_rts_bpp()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('leo1'):
        if version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('leox2'):
        if version == ('10.10'):
            acpi.xhcihcdModule()
            misc.gnomeThemeRace()
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('leox3'):
        if version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ment1'):
        if version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ment2'):
        if version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ment3'):
        if version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ment5'):
        if version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
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
        elif version == ('8.10'):
            uvc.camera()
            sound.alsa10()
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panp4n'):
        if version == ('8.04'):
            uvc.camera()
            fprint.install()
            sound.alsa11()
        elif version == ('8.10'):
            uvc.camera()
            fprint.install()
            sound.alsa10()
        elif version == ('9.04'):
            fprint.install()
            misc.linux_backports()
        elif version == ('9.10'):
            fprint.installPackages()
        elif version == ('10.04'):
            fprint.installPackages()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panp5'):
        if version == ('8.04'):
            uvc.camera()
            fprint.install()
            sound.alsa11()
        elif version == ('8.10'):
            uvc.camera()
            fprint.install()
            sound.alsa10()
        elif version == ('9.04'):
            fprint.install()
            misc.linux_backports()
        elif version == ('9.10'):
            fprint.installPackages()
        elif version == ('10.04'):
            fprint.installPackages()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panp6'):
        if version == ('8.04'):
            uvc.camera()
            fprint.install()
            sound.alsa11()
        elif version == ('8.10'):
            uvc.camera()
            fprint.install()
            sound.alsa10()
        elif version == ('9.04'):
            fprint.install()
            misc.linux_backports()
        elif version == ('9.10'):
            fprint.installPackages()
        elif version == ('10.04'):
            fprint.installPackages()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panp7'):
        if version == ('9.10'):
            acpi.os_linux()
            fprint.installUpek1()
            misc.jme_nic()
            misc.rm_aticatalyst()
        elif version == ('10.04'):
            acpi.os_linux()
            fprint.installUpek1()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panp8'):
        if version == ('11.04'):
            acpi.lemu1()
            misc.elantech()
        elif version == ('11.10'):
            acpi.lemu1()
        elif version == ('12.04'):
            acpi.lemu1()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panp9'):
        if version == ('11.10'):
            acpi.lemu1()
            misc.realtek_rts_bpp()
        elif version == ('12.04'):
            acpi.lemu1()
            misc.realtek_rts_bpp()
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panv3'):
        if version == ('7.04'):
            misc.piix2()
            sound.alsa5()
            acpi.acpi1()
            ricoh_cr.card_reader()
        elif version == ('7.10'):
            sound.alsa5()
            ricoh_cr.card_reader()
        elif version == ('8.04'):
            sound.alsa9()
            hardy_led.install()
        elif version == ('8.10'):
            sound.alsa9()
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ratu1'):
        if version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ratu2'):
        if version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ratp1'):
        if version == ('12.04'):
            nodrivers = "true"
            return nodrivers
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
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
        elif version == ('8.10'):
            sound.alsa8()
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ratv6'):
        if version == ('8.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('sabv3'):
        if version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
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
        elif version == ('8.10'):
            sound.alsa9()
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
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
        elif version == ('8.10'):
            sound.alsa9()
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('serp5'):
        if version == ('8.10'):
            sound.alsa10()
            uvc.camera()
            fprint.install()
            acpi.osiNotWindows()
        elif version == ('9.04'):
            fprint.install()
            misc.linux_backports()
        elif version == ('9.10'):
            fprint.installPackages()
        elif version == ('10.04'):
            fprint.installPackages()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('serp6'):
        if version == ('9.10'):
            acpi.os_linux()
            uvc.lemur()
            fprint.installUpek1()
            misc.gnomeThemeRace()
        elif version == ('10.04'):
            acpi.os_linux()
            uvc.lemur()
            fprint.installUpek1()
        elif version == ('10.10'):
            acpi.xhcihcdModule()
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('serp7'):
        if version == ('10.10'):
            fprint.fingerprintGUI()
            acpi.xhcihcdModule()
            misc.gnomeThemeRace()
            acpi.pcie_aspm()
        elif version == ('11.04'):
            acpi.pcie_aspm()
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('star1'):
        if version == ('9.04'):
            sound.alsa12()
            misc.linux_backports()
            acpi.star1()
            hotkey.star1_904()
            misc.wireless8187b()
        elif version == ('9.10'):
            sound.alsa13()
            acpi.star1()
            misc.wireless8187b()
        elif version == ('10.04'):
            sound.alsa13()
            acpi.star1()
            misc.wireless8187b()
        elif version == ('10.10'):
            sound.alsa13()
            acpi.star1()
            misc.wireless8187b()
        elif version == ('11.04'):
            sound.alsa13()
            acpi.star1()
            misc.wireless8187b()
        elif version == ('11.10'):
            sound.alsa13()
            acpi.star1()
            misc.wireless8187b()
        elif version == ('12.04'):
            sound.alsa13()
            acpi.star1()
            misc.wireless8187b()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('star2'):
        if version == ('10.04'):
            acpi.star2()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('star3'):
        if version == ('10.04'):
            sound.alsabackportsLucid()
            acpi.sdCardBug()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('star4'):
        if version == ('10.04'):
            sound.alsabackportsLucid()
            acpi.sdCardBug()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('star5'):
        if version == ('10.04'):
            sound.alsabackportsLucid()
            acpi.sdCardBug()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('wilb1'):
        if version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            misc.gnomeThemeRace()
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('wilb2'):
        if version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
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
        elif version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('wilp6'):
        if version == ('8.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('wilp7'):
        if version == ('9.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('wilp8'):
        if version == ('10.10'):
            acpi.xhcihcdModule()
            misc.gnomeThemeRace()
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('wilp9'):
        if version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    else:
        nodrivers = "true"
        return nodrivers
