#
#!/usr/bin/env python
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Controls driver installation

#import driver files
import ubuntuversion
import model
import detect

#import function files - KEEP IN ALPHABETICAL ORDER!
import acpi
import fprint
import hardy_led
import hotkey
import misc
import ricoh_cr
import sound
import usplash
import uvc

## KEEP ALL MODELS IN ALPHABETICAL ORDER

global descriptionFile
descriptionFile = "/tmp/sys76-drivers"

def describeDrivers():
    """This function describes drivers installed for each machine"""
    
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
            sound.alsa6().describe()
        elif version == ('7.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            hardy_led.install().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('bonp2'):
        if version == ('8.04'):
            sound.alsa10().describe()
            uvc.camera().describe()
            fprint.install().describe()
            acpi.osiNotWindows().describe()
        elif version == ('8.10'):
            sound.alsa10().describe()
            uvc.camera().describe()
            fprint.install().describe()
            acpi.osiNotWindows().describe()
        elif version == ('9.04'):
            fprint.install().describe()
            acpi.osiNotWindows().describe()
            misc.linux_backports().describe()
        elif version == ('9.10'):
            fprint.installPackages().describe()
        elif version == ('10.04'):
            fprint.installPackages().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('bonp3'):
        if version == ('9.10'):
            acpi.os_linux().describe()
            fprint.installUpek1().describe()
            misc.jme_nic().describe()
            misc.rm_aticatalyst().describe()
        elif version == ('10.04'):
            fprint.installUpek1().describe()
            acpi.os_linux().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('bonp4'):
        if version == ('10.10'):
            acpi.xhcihcdModule().describe()
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('bonp5'):
        if version == ('11.04'):
            acpi.pcie_aspm().describe()
            sound.audioDevPPA().describe()
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            fprint.fingerprintGUI().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('bonx6'):
        if version == ('12.04'):
            fprint.fingerprintGUI().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            fprint.fingerprintGUI().describe()
            misc.realtek_rts_bpp().describe()
            misc.lightdm_race().describe()
            misc.plymouth1080().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('daru1'):
        if version == ('6.06'):
            sound.alsa6().describe()
        elif version == ('6.10'):
            sound.alsa6().describe()
        elif version == ('7.04'):
            misc.piix().describe()
            acpi.acpi1().describe()
            hotkey.daru1_monitor_switch().describe()
        elif version == ('7.10'):
            acpi.acpi3().describe()
            hotkey.daru1_monitor_switch().describe()
        elif version == ('8.04'):
            acpi.acpi3().describe()
            hotkey.daru1_monitor_switch().describe()
            hardy_led.install().describe()
        elif version == ('8.10'):
            hotkey.daru1_touchpad_switch().describe()
        elif version == ('9.04'):
            hotkey.daru1_touchpad_switch().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('daru2'):
        if version == ('7.04'):
            misc.piix2().describe()
            acpi.acpi2().describe()
            acpi.daru2().describe()
            sound.alsa4().describe()
        elif version == ('7.10'):
            acpi.acpi3().describe()
            acpi.daru2().describe()
            sound.alsa4().describe()
        elif version == ('8.04'):
            sound.alsa4().describe()
            hardy_led.install().describe()
        elif version == ('8.10'):
            sound.alsa4().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('daru3'):
        if version == ('8.04'):
            sound.alsa10().describe()
            uvc.camera().describe()
            fprint.install().describe()
        elif version == ('8.10'):
            sound.alsa10().describe()
            uvc.camera().describe()
            fprint.install().describe()
            acpi.acpi4().describe()
        elif version == ('9.04'):
            fprint.install().describe()
        elif version == ('9.10'):
            fprint.installPackages().describe()
        elif version == ('10.04'):
            fprint.installPackages().describe()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            acpi.lemu1().describe()
        elif version == ('12.04'):
            fprint.fingerprintGUI().describe()
            acpi.lemu1().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            fprint.fingerprintGUI().describe()
            acpi.lemu1().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp1'):
        if version == ('6.06'):
            sound.alsa6().describe()
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            sound.alsa6().describe()
            acpi.acpi1().describe()
        elif version == ('7.10'):
            sound.alsa6().describe()
            acpi.acpi3().describe()
        elif version == ('8.04'):
            hardy_led.install().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp2'):
        if version == ('6.06'):
            sound.alsa6().describe()
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            sound.alsa6().describe()
            acpi.acpi1().describe()
        elif version == ('7.10'):
            sound.alsa6().describe()
            acpi.acpi3().describe()
        elif version == ('8.04'):
            hardy_led.install().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp3'):
        if version == ('6.06'):
            sound.alsa6().describe()
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            sound.alsa6().describe()
            acpi.acpi1().describe()
        elif version == ('7.10'):
            sound.alsa6().describe()
            acpi.acpi3().describe()
        elif version == ('8.04'):
            hardy_led.install().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp5'):
        if version == ('7.04'):
            misc.piix2().describe()
            sound.alsa5().describe()
            uvc.camera().describe()
            acpi.acpi1().describe()
            ricoh_cr.card_reader().describe()
        elif version == ('7.10'):
            sound.alsa5().describe()
            acpi.acpi3().describe()
            ricoh_cr.card_reader().describe()
        elif version == ('8.04'):
            sound.alsa9().describe()
            hardy_led.install().describe()
        elif version == ('8.10'):
            sound.alsa9().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp6'):
        if version == ('10.10'):
            fprint.fingerprintGUI().describe()
            acpi.xhcihcdModule().describe()
            misc.gnomeThemeRace().describe()
            acpi.pcie_aspm().describe()
        elif version == ('11.04'):
            acpi.pcie_aspm().describe()
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            fprint.fingerprintGUI().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp7'):
        if version == ('12.04'):
            acpi.lemu1().describe()
            misc.realtek_rts_bpp().describe()
            misc.lightdm_race().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            acpi.lemu1().describe()
            misc.realtek_rts_bpp().describe()
            misc.lightdm_race().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazp8'):
        if version == ('12.04'):
            acpi.lemu1().describe()
            misc.realtek_rts_bpp().describe()
            misc.lightdm_race().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            acpi.lemu1().describe()
            misc.realtek_rts_bpp().describe()
            misc.lightdm_race().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazv1'):
        nodrivers = "true"
        return nodrivers
    elif modelname == ('gazv2'):
        if version == ('6.06'):
            sound.alsa6().describe()
        elif version == ('6.10'):
            sound.alsa6().describe()
        elif version == ('7.04'):
            sound.alsa6().describe()
            acpi.acpi1().describe()
        elif version == ('7.10'):
            sound.alsa6().describe()
            acpi.acpi3().describe()
        elif version == ('8.04'):
            hardy_led.install().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazv3'):
        if version == ('6.06'):
            sound.alsa6().describe()
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            sound.alsa6().describe()
            misc.piix().describe()
            acpi.acpi2().describe()
        elif version == ('7.10'):
            sound.alsa6().describe()
            acpi.acpi3().describe()
        elif version == ('8.04'):
            hardy_led.install().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazv4'):
        if version == ('6.06'):
            sound.alsa6().describe()
        elif version == ('6.10'):
            sound.alsa6().describe()
        elif version == ('7.04'):
            sound.alsa6().describe()
            misc.piix().describe()
            acpi.acpi2().describe()
        elif version == ('7.10'):
            sound.alsa6().describe()
            acpi.acpi3().describe()
        elif version == ('8.04'):
            hardy_led.install().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazv5'):
        if version == ('7.04'):
            misc.piix2().describe()
            sound.alsa5().describe()
            uvc.camera().describe()
            acpi.acpi1().describe()
            ricoh_cr.card_reader().describe()
        elif version == ('7.10'):
            sound.alsa5().describe()
            ricoh_cr.card_reader().describe()
        elif version == ('8.04'):
            sound.alsa9().describe()
            hardy_led.install().describe()
        elif version == ('8.10'):
            sound.alsa9().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('gazu1'):
        if version == ('8.04'):
            sound.alsa10().describe()
            uvc.camera().describe()
            uvc.quirks().describe()
            fprint.install().describe()
        elif version == ('8.10'):
            sound.alsa10().describe()
            uvc.quirks().describe()
            fprint.install().describe()
        elif version == ('9.04'):
            uvc.quirks().describe()
            fprint.install().describe()
        elif version == ('9.10'):
            uvc.quirks().describe()
            fprint.installPackages().describe()
        elif version == ('10.04'):
            uvc.quirks().describe()
            fprint.installPackages().describe()
        elif version == ('10.10'):
            uvc.quirks().describe()
        elif version == ('11.04'):
            uvc.quirks().describe()
        elif version == ('11.10'):
            uvc.quirks().describe()
        elif version == ('12.04'):
            uvc.quirks().describe()
            fprint.fingerprintGUI().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            uvc.quirks().describe()
            fprint.fingerprintGUI().describe()
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
            acpi.acpi1().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('lemu1'):
        if version == ('9.04'):
            uvc.lemur().describe()
            acpi.lemu1().describe()
        elif version == ('9.10'):
            uvc.lemur().describe()
            acpi.lemu1().describe()
            misc.jme_nic().describe()
        elif version == ('10.04'):
            uvc.lemur().describe()
            acpi.lemu1().describe()
        elif version == ('10.10'):
            acpi.lemu1().describe()
        elif version == ('11.04'):
            acpi.lemu1().describe()
        elif version == ('11.10'):
            acpi.lemu1().describe()
        elif version == ('12.04'):
            acpi.lemu1().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            acpi.lemu1().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('lemu2'):
        if version == ('10.04'):
            uvc.lemur().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('lemu3'):
        if version == ('11.04'):
            acpi.lemu1().describe()
        elif version == ('11.10'):
            acpi.lemu1().describe()
        elif version == ('12.04'):
            acpi.lemu1().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            acpi.lemu1().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('lemu4'):
        if version == ('11.10'):
            acpi.lemu1().describe()
            misc.realtek_rts_bpp().describe()
        elif version == ('12.04'):
            acpi.lemu1().describe()
            misc.realtek_rts_bpp().describe()
            misc.lightdm_race().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            acpi.lemu1().describe()
            misc.realtek_rts_bpp().describe()
            misc.lightdm_race().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('leox2'):
        if version == ('10.10'):
            acpi.xhcihcdModule().describe()
            misc.gnomeThemeRace().describe()
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('leox3'):
        if version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            misc.lightdm_race().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            misc.lightdm_race().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('nonsystem76'):
        nodrivers = "true"
        return nodrivers
    elif modelname == ('panp4i'):
        if version == ('8.04'):
            uvc.camera().describe()
            sound.alsa11().describe()
        elif version == ('8.10'):
            uvc.camera().describe()
            sound.alsa10().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panp4n'):
        if version == ('8.04'):
            uvc.camera().describe()
            fprint.install().describe()
            sound.alsa11().describe()
        elif version == ('8.10'):
            uvc.camera().describe()
            fprint.install().describe()
            sound.alsa10().describe()
        elif version == ('9.04'):
            fprint.install().describe()
            misc.linux_backports().describe()
        elif version == ('9.10'):
            fprint.installPackages().describe()
        elif version == ('10.04'):
            fprint.installPackages().describe()
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
            fprint.fingerprintGUI().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            fprint.fingerprintGUI().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panp5'):
        if version == ('8.04'):
            uvc.camera().describe()
            fprint.install().describe()
            sound.alsa11().describe()
        elif version == ('8.10'):
            uvc.camera().describe()
            fprint.install().describe()
            sound.alsa10().describe()
        elif version == ('9.04'):
            fprint.install().describe()
            misc.linux_backports().describe()
        elif version == ('9.10'):
            fprint.installPackages().describe()
        elif version == ('10.04'):
            fprint.installPackages().describe()
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
            fprint.fingerprintGUI().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            fprint.fingerprintGUI().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panp6'):
        if version == ('8.04'):
            uvc.camera().describe()
            fprint.install().describe()
            sound.alsa11().describe()
        elif version == ('8.10'):
            uvc.camera().describe()
            fprint.install().describe()
            sound.alsa10().describe()
        elif version == ('9.04'):
            fprint.install().describe()
            misc.linux_backports().describe()
        elif version == ('9.10'):
            fprint.installPackages().describe()
        elif version == ('10.04'):
            fprint.installPackages().describe()
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
            fprint.fingerprintGUI().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            fprint.fingerprintGUI().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panp7'):
        if version == ('9.10'):
            acpi.os_linux().describe()
            fprint.installUpek1().describe()
            misc.jme_nic().describe()
            misc.rm_aticatalyst().describe()
        elif version == ('10.04'):
            acpi.os_linux().describe()
            fprint.installUpek1().describe()
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
            fprint.fingerprintGUI().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            fprint.fingerprintGUI().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panp8'):
        if version == ('11.04'):
            acpi.lemu1().describe()
            misc.elantech().describe()
        elif version == ('11.10'):
            acpi.lemu1().describe()
        elif version == ('12.04'):
            acpi.lemu1().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            acpi.lemu1().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panp9'):
        if version == ('11.10'):
            acpi.lemu1().describe()
            misc.realtek_rts_bpp().describe()
        elif version == ('12.04'):
            acpi.lemu1().describe()
            misc.realtek_rts_bpp().describe()
            misc.lightdm_race().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            acpi.lemu1().describe()
            misc.realtek_rts_bpp().describe()
            misc.lightdm_race().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panv2'):
        if version == ('6.06'):
            sound.alsa6().describe()
        elif version == ('6.10'):
            sound.alsa6().describe()
        elif version == ('7.04'):
            sound.alsa6().describe()
            acpi.acpi1().describe()
        elif version == ('7.10'):
            sound.alsa6().describe()
        elif version == ('8.04'):
            hardy_led.install().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('panv3'):
        if version == ('7.04'):
            misc.piix2().describe()
            sound.alsa5().describe()
            acpi.acpi1().describe()
            ricoh_cr.card_reader().describe()
        elif version == ('7.10'):
            sound.alsa5().describe()
            ricoh_cr.card_reader().describe()
        elif version == ('8.04'):
            sound.alsa9().describe()
            hardy_led.install().describe()
        elif version == ('8.10'):
            sound.alsa9().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ratp1'):
        if version == ('12.04'):
            misc.lightdm_race().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            misc.lightdm_race().describe()
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
            acpi.acpi1().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
            acpi.acpi1().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
            acpi.acpi1().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ratv4'):
        if version == ('7.10'):
            sound.alsa7().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('ratv5'):
        if version == ('7.10'):
            sound.alsa7().describe()
        elif version == ('8.04'):
            sound.alsa8().describe()
        elif version == ('8.10'):
            sound.alsa8().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('sabc1'):
        if version == ('12.04'):
            misc.lightdm_race().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            misc.lightdm_race().describe()
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
            acpi.acpi1().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('sabv2'):
        if version == ('6.06'):
            sound.alsa6().describe()
        elif version == ('6.10'):
            sound.alsa6().describe()
        elif version == ('7.04'):
            sound.alsa6().describe()
            acpi.acpi1().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
            acpi.acpi1().describe()
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            hardy_led.install().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
            acpi.acpi1().describe()
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            hardy_led.install().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('serp3'):
        if version == ('7.04'):
            acpi.acpi1().describe()
            sound.alsa5().describe()
        elif version == ('7.10'):
            if arch == ('x86'):
                sound.alsa5().describe()
                ricoh_cr.card_reader().describe()
            else:
                usplash.gutsy_64_nvidia().describe()
                sound.alsa5().describe()
                ricoh_cr.card_reader().describe()
        elif version == ('8.04'):
            sound.alsa9().describe()
            hardy_led.install().describe()
        elif version == ('8.10'):
            sound.alsa9().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('serp4'):
        if version == ('7.04'):
            acpi.acpi1().describe()
            sound.alsa5().describe()
        elif version == ('7.10'):
            if arch == ('x86'):
                sound.alsa5().describe()
                ricoh_cr.card_reader().describe()
            else:
                usplash.gutsy_64_nvidia().describe()
                sound.alsa5().describe()
                ricoh_cr.card_reader().describe()
        elif version == ('8.04'):
            sound.alsa9().describe()
            hardy_led.install().describe()
        elif version == ('8.10'):
            sound.alsa9().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('serp5'):
        if version == ('8.10'):
            sound.alsa10().describe()
            uvc.camera().describe()
            fprint.install().describe()
            acpi.osiNotWindows().describe()
        elif version == ('9.04'):
            fprint.install().describe()
            misc.linux_backports().describe()
        elif version == ('9.10'):
            fprint.installPackages().describe()
        elif version == ('10.04'):
            fprint.installPackages().describe()
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
            fprint.fingerprintGUI().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            fprint.fingerprintGUI().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('serp6'):
        if version == ('9.10'):
            acpi.os_linux().describe()
            uvc.lemur().describe()
            fprint.installUpek1().describe()
            misc.gnomeThemeRace().describe()
        elif version == ('10.04'):
            acpi.os_linux().describe()
            uvc.lemur().describe()
            fprint.installUpek1().describe()
        elif version == ('10.10'):
            acpi.xhcihcdModule().describe()
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            fprint.fingerprintGUI().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('serp7'):
        if version == ('10.10'):
            fprint.fingerprintGUI().describe()
            acpi.xhcihcdModule().describe()
            misc.gnomeThemeRace().describe()
            acpi.pcie_aspm().describe()
        elif version == ('11.04'):
            acpi.pcie_aspm().describe()
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            fprint.fingerprintGUI().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('star1'):
        if version == ('9.04'):
            sound.alsa12().describe()
            misc.linux_backports().describe()
            acpi.star1().describe()
            hotkey.star1_904().describe()
            misc.wireless8187b().describe()
        elif version == ('9.10'):
            sound.alsa13().describe()
            acpi.star1().describe()
            misc.wireless8187b().describe()
        elif version == ('10.04'):
            sound.alsa13().describe()
            acpi.star1().describe()
            misc.wireless8187b().describe()
        elif version == ('10.10'):
            sound.alsa13().describe()
            acpi.star1().describe()
            misc.wireless8187b().describe()
        elif version == ('11.04'):
            sound.alsa13().describe()
            acpi.star1().describe()
            misc.wireless8187b().describe()
        elif version == ('11.10'):
            sound.alsa13().describe()
            acpi.star1().describe()
            misc.wireless8187b().describe()
        elif version == ('12.04'):
            sound.alsa13().describe()
            acpi.star1().describe()
            misc.wireless8187b().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            sound.alsa13().describe()
            acpi.star1().describe()
            misc.wireless8187b().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('star2'):
        if version == ('10.04'):
            acpi.star2().describe()
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
        elif version == ('12.10'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('star3'):
        if version == ('10.04'):
            sound.alsabackportsLucid().describe()
            acpi.sdCardBug().describe()
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
        elif version == ('12.10'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('star4'):
        if version == ('10.04'):
            sound.alsabackportsLucid().describe()
            acpi.sdCardBug().describe()
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
        elif version == ('12.10'):
            nodrivers = "true"
            return nodrivers
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('star5'):
        if version == ('10.04'):
            sound.alsabackportsLucid().describe()
            acpi.sdCardBug().describe()
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
        elif version == ('12.10'):
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
            misc.gnomeThemeRace().describe()
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('wilp5'):
        if version == ('7.10'):
            if arch == ('x86'):
                nodrivers = "true"
                return nodrivers
            else:
                usplash.gutsy_64_nvidia().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
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
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('wilp8'):
        if version == ('10.10'):
            acpi.xhcihcdModule().describe()
            misc.gnomeThemeRace().describe()
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.10'):
            misc.linux_headers().describe()
        else:
            nodrivers = "true"
            return nodrivers
    elif modelname == ('wilp9'):
        if version == ('12.04'):
            misc.lightdm_race().describe()
        elif version == ('12.10'):
            misc.linux_headers().describe()
            misc.lightdm_race().describe()
        else:
            nodrivers = "true"
            return nodrivers
    else:
        nodrivers = "true"
        return nodrivers
