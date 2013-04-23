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
    #Bonobo
    if modelname == ('bonp1'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            sound.alsa6().install()
        elif version == ('7.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            hardy_led.install().install()
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
            misc.linux_headers().install()
        elif version == ('13.04'):
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('bonp2'):
        if version == ('8.04'):
            sound.alsa10().install()
            uvc.camera().install()
            fprint.install().install()
            acpi.osiNotWindows().install()
        elif version == ('8.10'):
            sound.alsa10().install()
            uvc.camera().install()
            fprint.install().install()
            acpi.osiNotWindows().install()
        elif version == ('9.04'):
            fprint.install().install()
            acpi.osiNotWindows().install()
            misc.linux_backports().install()
        elif version == ('9.10'):
            fprint.installPackages().install()
        elif version == ('10.04'):
            fprint.installPackages().install()
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
            misc.linux_headers().install()
        elif version == ('13.04'):
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('bonp3'):
        if version == ('9.10'):
            acpi.os_linux().install()
            fprint.installUpek1().install()
            misc.jme_nic().install()
            misc.rm_aticatalyst().install()
        elif version == ('10.04'):
            fprint.installUpek1().install()
            acpi.os_linux().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('bonp4'):
        if version == ('10.10'):
            acpi.xhcihcdModule().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('bonp5'):
        if version == ('11.04'):
            acpi.pcie_aspm().install()
            sound.audioDevPPA().install()
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            fprint.fingerprintGUI().install()
        elif version == ('13.04'):
            fprint.fingerprintGUI().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('bonx6'):
        if version == ('12.04'):
            fprint.fingerprintGUI().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            fprint.fingerprintGUI().install()
            misc.realtek_rts_bpp().install()
            misc.lightdm_race().install()
            misc.plymouth1080().install()
        elif version == ('13.04'):
            fprint.fingerprintGUI().install()
            misc.plymouth1080().install()
        else:
            nodrivers = "true"
            return nodrivers
    
    #Darter        
    elif modelname == ('daru1'):
        if version == ('6.06'):
            sound.alsa6().install()
        elif version == ('6.10'):
            sound.alsa6().install()
        elif version == ('7.04'):
            misc.piix().install()
            acpi.acpi1().install()
            hotkey.daru1_monitor_switch().install()
        elif version == ('7.10'):
            acpi.acpi3().install()
            hotkey.daru1_monitor_switch().install()
        elif version == ('8.04'):
            acpi.acpi3().install()
            hotkey.daru1_monitor_switch().install()
            hardy_led.install().install()
        elif version == ('8.10'):
            hotkey.daru1_touchpad_switch().install()
        elif version == ('9.04'):
            hotkey.daru1_touchpad_switch().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('daru2'):
        if version == ('7.04'):
            misc.piix2().install()
            acpi.acpi2().install()
            acpi.daru2().install()
            sound.alsa4().install()
        elif version == ('7.10'):
            acpi.acpi3().install()
            acpi.daru2().install()
            sound.alsa4().install()
        elif version == ('8.04'):
            sound.alsa4().install()
            hardy_led.install().install()
        elif version == ('8.10'):
            sound.alsa4().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('daru3'):
        if version == ('8.04'):
            sound.alsa10().install()
            uvc.camera().install()
            fprint.install().install()
        elif version == ('8.10'):
            sound.alsa10().install()
            uvc.camera().install()
            fprint.install().install()
            acpi.acpi4().install()
        elif version == ('9.04'):
            fprint.install().install()
        elif version == ('9.10'):
            fprint.installPackages().install()
        elif version == ('10.04'):
            fprint.installPackages().install()
        elif version == ('10.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            acpi.lemu1().install()
        elif version == ('12.04'):
            fprint.fingerprintGUI().install()
            acpi.lemu1().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            fprint.fingerprintGUI().install()
            acpi.lemu1().install()
        elif version == ('13.04'):
            fprint.fingerprintGUI().install()
            acpi.lemu1().install()
        else:
            nodrivers = "true"
            return nodrivers
    
    #Gazelle        
    elif modelname == ('gazp1'):
        if version == ('6.06'):
            sound.alsa6().install()
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            sound.alsa6().install()
            acpi.acpi1().install()
        elif version == ('7.10'):
            sound.alsa6().install()
            acpi.acpi3().install()
        elif version == ('8.04'):
            hardy_led.install().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('gazp2'):
        if version == ('6.06'):
            sound.alsa6().install()
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            sound.alsa6().install()
            acpi.acpi1().install()
        elif version == ('7.10'):
            sound.alsa6().install()
            acpi.acpi3().install()
        elif version == ('8.04'):
            hardy_led.install().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('gazp3'):
        if version == ('6.06'):
            sound.alsa6().install()
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            sound.alsa6().install()
            acpi.acpi1().install()
        elif version == ('7.10'):
            sound.alsa6().install()
            acpi.acpi3().install()
        elif version == ('8.04'):
            hardy_led.install().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('gazp5'):
        if version == ('7.04'):
            misc.piix2().install()
            sound.alsa5().install()
            uvc.camera().install()
            acpi.acpi1().install()
            ricoh_cr.card_reader().install()
        elif version == ('7.10'):
            sound.alsa5().install()
            acpi.acpi3().install()
            ricoh_cr.card_reader().install()
        elif version == ('8.04'):
            sound.alsa9().install()
            hardy_led.install().install()
        elif version == ('8.10'):
            sound.alsa9().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('gazp6'):
        if version == ('10.10'):
            fprint.fingerprintGUI().install()
            acpi.xhcihcdModule().install()
            misc.gnomeThemeRace().install()
            acpi.pcie_aspm().install()
        elif version == ('11.04'):
            acpi.pcie_aspm().install()
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            fprint.fingerprintGUI().install()
        elif version == ('13.04'):
            fprint.fingerprintGUI().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('gazp7'):
        if version == ('12.04'):
            acpi.lemu1().install()
            misc.realtek_rts_bpp().install()
            misc.lightdm_race().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            acpi.lemu1().install()
            misc.realtek_rts_bpp().install()
            misc.lightdm_race().install()
        elif version == ('13.04'):
            acpi.lemu1().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('gazp8'):
        if version == ('12.04'):
            acpi.lemu1().install()
            misc.realtek_rts_bpp().install()
            misc.lightdm_race().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            acpi.lemu1().install()
            misc.realtek_rts_bpp().install()
            misc.lightdm_race().install()
        elif version == ('13.04'):
            misc.lemu1().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('gazv1'):
        nodrivers = "true"
        return nodrivers
    elif modelname == ('gazv2'):
        if version == ('6.06'):
            sound.alsa6().install()
        elif version == ('6.10'):
            sound.alsa6().install()
        elif version == ('7.04'):
            sound.alsa6().install()
            acpi.acpi1().install()
        elif version == ('7.10'):
            sound.alsa6().install()
            acpi.acpi3().install()
        elif version == ('8.04'):
            hardy_led.install().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('gazv3'):
        if version == ('6.06'):
            sound.alsa6().install()
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            sound.alsa6().install()
            misc.piix().install()
            acpi.acpi2().install()
        elif version == ('7.10'):
            sound.alsa6().install()
            acpi.acpi3().install()
        elif version == ('8.04'):
            hardy_led.install().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('gazv4'):
        if version == ('6.06'):
            sound.alsa6().install()
        elif version == ('6.10'):
            sound.alsa6().install()
        elif version == ('7.04'):
            sound.alsa6().install()
            misc.piix().install()
            acpi.acpi2().install()
        elif version == ('7.10'):
            sound.alsa6().install()
            acpi.acpi3().install()
        elif version == ('8.04'):
            hardy_led.install().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('gazv5'):
        if version == ('7.04'):
            misc.piix2().install()
            sound.alsa5().install()
            uvc.camera().install()
            acpi.acpi1().install()
            ricoh_cr.card_reader().install()
        elif version == ('7.10'):
            sound.alsa5().install()
            ricoh_cr.card_reader().install()
        elif version == ('8.04'):
            sound.alsa9().install()
            hardy_led.install().install()
        elif version == ('8.10'):
            sound.alsa9().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('gazu1'):
        if version == ('8.04'):
            sound.alsa10().install()
            uvc.camera().install()
            uvc.quirks().install()
            fprint.install().install()
        elif version == ('8.10'):
            sound.alsa10().install()
            uvc.quirks().install()
            fprint.install().install()
        elif version == ('9.04'):
            uvc.quirks().install()
            fprint.install().install()
        elif version == ('9.10'):
            uvc.quirks().install()
            fprint.installPackages().install()
        elif version == ('10.04'):
            uvc.quirks().install()
            fprint.installPackages().install()
        elif version == ('10.10'):
            uvc.quirks().install()
        elif version == ('11.04'):
            uvc.quirks().install()
        elif version == ('11.10'):
            uvc.quirks().install()
        elif version == ('12.04'):
            uvc.quirks().install()
            fprint.fingerprintGUI().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            uvc.quirks().install()
            fprint.fingerprintGUI().install()
        elif version == ('13.04'):
            fprint.fingerprintGUI().install()
            uvc.quirks().install()
        else:
            nodrivers = "true"
            return nodrivers
    
    #Koala        
    elif modelname == ('koap1'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            acpi.acpi1().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
    
    #Lemur        
    elif modelname == ('lemu1'):
        if version == ('9.04'):
            uvc.lemur().install()
            acpi.lemu1().install()
        elif version == ('9.10'):
            uvc.lemur().install()
            acpi.lemu1().install()
            misc.jme_nic().install()
        elif version == ('10.04'):
            uvc.lemur().install()
            acpi.lemu1().install()
        elif version == ('10.10'):
            acpi.lemu1().install()
        elif version == ('11.04'):
            acpi.lemu1().install()
        elif version == ('11.10'):
            acpi.lemu1().install()
        elif version == ('12.04'):
            acpi.lemu1().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            acpi.lemu1().install()
        elif version == ('13.04'):
            fprint.fingerprintGUI().install()
            acpi.lemu1().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('lemu2'):
        if version == ('10.04'):
            uvc.lemur().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('lemu3'):
        if version == ('11.04'):
            acpi.lemu1().install()
        elif version == ('11.10'):
            acpi.lemu1().install()
        elif version == ('12.04'):
            acpi.lemu1().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            acpi.lemu1().install()
        elif version == ('13.04'):
            acpi.lemu1().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('lemu4'):
        if version == ('11.10'):
            acpi.lemu1().install()
            misc.realtek_rts_bpp().install()
        elif version == ('12.04'):
            acpi.lemu1().install()
            misc.realtek_rts_bpp().install()
            misc.lightdm_race().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            acpi.lemu1().install()
            misc.realtek_rts_bpp().install()
            misc.lightdm_race().install()
        elif version == ('13.04'):
            acpi.lemu1().install()
        else:
            nodrivers = "true"
            return nodrivers
    
    #Leopard        
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('leox2'):
        if version == ('10.10'):
            acpi.xhcihcdModule().install()
            misc.gnomeThemeRace().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('leox3'):
        if version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            misc.lightdm_race().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            misc.lightdm_race().install()
        else:
            nodrivers = "true"
            return nodrivers
    
    #Meerkat        
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
            misc.linux_headers().install()
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
            misc.linux_headers().install()
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
            misc.linux_headers().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    #Non-System76
    elif modelname == ('nonsystem76'):
        nodrivers = "true"
        return nodrivers
        
    #Pangolin
    elif modelname == ('panp4i'):
        if version == ('8.04'):
            uvc.camera().install()
            sound.alsa11().install()
        elif version == ('8.10'):
            uvc.camera().install()
            sound.alsa10().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('panp4n'):
        if version == ('8.04'):
            uvc.camera().install()
            fprint.install().install()
            sound.alsa11().install()
        elif version == ('8.10'):
            uvc.camera().install()
            fprint.install().install()
            sound.alsa10().install()
        elif version == ('9.04'):
            fprint.install().install()
            misc.linux_backports().install()
        elif version == ('9.10'):
            fprint.installPackages().install()
        elif version == ('10.04'):
            fprint.installPackages().install()
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
            fprint.fingerprintGUI().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            fprint.fingerprintGUI().install()
        elif version == ('13.04'):
            fprint.fingerprintGUI().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('panp5'):
        if version == ('8.04'):
            uvc.camera().install()
            fprint.install().install()
            sound.alsa11().install()
        elif version == ('8.10'):
            uvc.camera().install()
            fprint.install().install()
            sound.alsa10().install()
        elif version == ('9.04'):
            fprint.install().install()
            misc.linux_backports().install()
        elif version == ('9.10'):
            fprint.installPackages().install()
        elif version == ('10.04'):
            fprint.installPackages().install()
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
            fprint.fingerprintGUI().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            fprint.fingerprintGUI().install()
        elif version == ('13.04'):
            fprint.fingerprintGUI().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('panp6'):
        if version == ('8.04'):
            uvc.camera().install()
            fprint.install().install()
            sound.alsa11().install()
        elif version == ('8.10'):
            uvc.camera().install()
            fprint.install().install()
            sound.alsa10().install()
        elif version == ('9.04'):
            fprint.install().install()
            misc.linux_backports().install()
        elif version == ('9.10'):
            fprint.installPackages().install()
        elif version == ('10.04'):
            fprint.installPackages().install()
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
            fprint.fingerprintGUI().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            fprint.fingerprintGUI().install()
        elif version == ('13.04'):
            fprint.fingerprintGUI().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('panp7'):
        if version == ('9.10'):
            acpi.os_linux().install()
            fprint.installUpek1().install()
            misc.jme_nic().install()
            misc.rm_aticatalyst().install()
        elif version == ('10.04'):
            acpi.os_linux().install()
            fprint.installUpek1().install()
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
            fprint.fingerprintGUI().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            fprint.fingerprintGUI().install()
        elif version == ('13.04'):
            fprint.fingerprintGUI().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('panp8'):
        if version == ('11.04'):
            acpi.lemu1().install()
            misc.elantech().install()
        elif version == ('11.10'):
            acpi.lemu1().install()
        elif version == ('12.04'):
            acpi.lemu1().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            acpi.lemu1().install()
        elif version == ('13.04'):
            acpi.lemu1().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('panp9'):
        if version == ('11.10'):
            acpi.lemu1().install()
            misc.realtek_rts_bpp().install()
        elif version == ('12.04'):
            acpi.lemu1().install()
            misc.realtek_rts_bpp().install()
            misc.lightdm_race().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            acpi.lemu1().install()
            misc.realtek_rts_bpp().install()
            misc.lightdm_race().install()
        elif version == ('13.04'):
            acpi.lemu1().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('panv2'):
        if version == ('6.06'):
            sound.alsa6().install()
        elif version == ('6.10'):
            sound.alsa6().install()
        elif version == ('7.04'):
            sound.alsa6().install()
            acpi.acpi1().install()
        elif version == ('7.10'):
            sound.alsa6().install()
        elif version == ('8.04'):
            hardy_led.install().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('panv3'):
        if version == ('7.04'):
            misc.piix2().install()
            sound.alsa5().install()
            acpi.acpi1().install()
            ricoh_cr.card_reader().install()
        elif version == ('7.10'):
            sound.alsa5().install()
            ricoh_cr.card_reader().install()
        elif version == ('8.04'):
            sound.alsa9().install()
            hardy_led.install().install()
        elif version == ('8.10'):
            sound.alsa9().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    #Ratel
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
            misc.linux_headers().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('ratp1'):
        if version == ('12.04'):
            misc.lightdm_race().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            misc.lightdm_race().install()
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
            acpi.acpi1().install()
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
            misc.linux_headers().install()
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
            acpi.acpi1().install()
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
            misc.linux_headers().install()
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
            acpi.acpi1().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('ratv4'):
        if version == ('7.10'):
            sound.alsa7().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('ratv5'):
        if version == ('7.10'):
            sound.alsa7().install()
        elif version == ('8.04'):
            sound.alsa8().install()
        elif version == ('8.10'):
            sound.alsa8().install()
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
            misc.linux_headers().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    #Sable
    elif modelname == ('sabc1'):
        if version == ('12.04'):
            misc.lightdm_race().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            misc.lightdm_race().install()
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
            acpi.acpi1().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('sabv2'):
        if version == ('6.06'):
            sound.alsa6().install()
        elif version == ('6.10'):
            sound.alsa6().install()
        elif version == ('7.04'):
            sound.alsa6().install()
            acpi.acpi1().install()
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
            misc.linux_headers().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    #Serval
    elif modelname == ('serp1'):
        if version == ('6.06'):
            nodrivers = "true"
            return nodrivers
        elif version == ('6.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('7.04'):
            acpi.acpi1().install()
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            hardy_led.install().install()
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
            misc.linux_headers().install()
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
            acpi.acpi1().install()
        elif version == ('7.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('8.04'):
            hardy_led.install().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('serp3'):
        if version == ('7.04'):
            acpi.acpi1().install()
            sound.alsa5().install()
        elif version == ('7.10'):
            if arch == ('x86'):
                sound.alsa5().install()
                ricoh_cr.card_reader().install()
            else:
                usplash.gutsy_64_nvidia().install()
                sound.alsa5().install()
                ricoh_cr.card_reader().install()
        elif version == ('8.04'):
            sound.alsa9().install()
            hardy_led.install().install()
        elif version == ('8.10'):
            sound.alsa9().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('serp4'):
        if version == ('7.04'):
            acpi.acpi1().install()
            sound.alsa5().install()
        elif version == ('7.10'):
            if arch == ('x86'):
                sound.alsa5().install()
                ricoh_cr.card_reader().install()
            else:
                usplash.gutsy_64_nvidia().install()
                sound.alsa5().install()
                ricoh_cr.card_reader().install()
        elif version == ('8.04'):
            sound.alsa9().install()
            hardy_led.install().install()
        elif version == ('8.10'):
            sound.alsa9().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('serp5'):
        if version == ('8.10'):
            sound.alsa10().install()
            uvc.camera().install()
            fprint.install().install()
            acpi.osiNotWindows().install()
        elif version == ('9.04'):
            fprint.install().install()
            misc.linux_backports().install()
        elif version == ('9.10'):
            fprint.installPackages().install()
        elif version == ('10.04'):
            fprint.installPackages().install()
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
            fprint.fingerprintGUI().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            fprint.fingerprintGUI().install()
        elif version == ('13.04'):
            fprint.fingerprintGUI().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('serp6'):
        if version == ('9.10'):
            acpi.os_linux().install()
            uvc.lemur().install()
            fprint.installUpek1().install()
            misc.gnomeThemeRace().install()
        elif version == ('10.04'):
            acpi.os_linux().install()
            uvc.lemur().install()
            fprint.installUpek1().install()
        elif version == ('10.10'):
            acpi.xhcihcdModule().install()
        elif version == ('11.04'):
            nodrivers = "true"
            return nodrivers
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            fprint.fingerprintGUI().install()
        elif version == ('13.04'):
            fprint.fingerprintGUI().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('serp7'):
        if version == ('10.10'):
            fprint.fingerprintGUI().install()
            acpi.xhcihcdModule().install()
            misc.gnomeThemeRace().install()
            acpi.pcie_aspm().install()
        elif version == ('11.04'):
            acpi.pcie_aspm().install()
        elif version == ('11.10'):
            nodrivers = "true"
            return nodrivers
        elif version == ('12.04'):
            fprint.fingerprintGUI().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            fprint.fingerprintGUI().install()
        elif version == ('13.04'):
            fprint.fingerprintGUI().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    #Starling
    elif modelname == ('star1'):
        if version == ('9.04'):
            sound.alsa12().install()
            misc.linux_backports().install()
            acpi.star1().install()
            hotkey.star1_904().install()
            misc.wireless8187b().install()
        elif version == ('9.10'):
            sound.alsa13().install()
            acpi.star1().install()
            misc.wireless8187b().install()
        elif version == ('10.04'):
            sound.alsa13().install()
            acpi.star1().install()
            misc.wireless8187b().install()
        elif version == ('10.10'):
            sound.alsa13().install()
            acpi.star1().install()
            misc.wireless8187b().install()
        elif version == ('11.04'):
            sound.alsa13().install()
            acpi.star1().install()
            misc.wireless8187b().install()
        elif version == ('11.10'):
            sound.alsa13().install()
            acpi.star1().install()
            misc.wireless8187b().install()
        elif version == ('12.04'):
            sound.alsa13().install()
            acpi.star1().install()
            misc.wireless8187b().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            sound.alsa13().install()
            acpi.star1().install()
            misc.wireless8187b().install()
        elif version == ('13.04'):
            misc.linux_headers().install()
            sound.alsa13().install()
            acpi.star1().install()
            misc.wireless8187b().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('star2'):
        if version == ('10.04'):
            acpi.star2().install()
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
            sound.alsabackportsLucid().install()
            acpi.sdCardBug().install()
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
            sound.alsabackportsLucid().install()
            acpi.sdCardBug().install()
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
            sound.alsabackportsLucid().install()
            acpi.sdCardBug().install()
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
            
    #Wildebeest
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
            misc.gnomeThemeRace().install()
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
            misc.linux_headers().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    #Wild Dog
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
            misc.linux_headers().install()
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
            misc.linux_headers().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('wilp5'):
        if version == ('7.10'):
            if arch == ('x86'):
                nodrivers = "true"
                return nodrivers
            else:
                usplash.gutsy_64_nvidia().install()
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
            misc.linux_headers().install()
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
            misc.linux_headers().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('wilp8'):
        if version == ('10.10'):
            acpi.xhcihcdModule().install()
            misc.gnomeThemeRace().install()
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
            misc.linux_headers().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    elif modelname == ('wilp9'):
        if version == ('12.04'):
            misc.lightdm_race().install()
        elif version == ('12.10'):
            misc.linux_headers().install()
            misc.lightdm_race().install()
        else:
            nodrivers = "true"
            return nodrivers
            
    else:
        nodrivers = "true"
        return nodrivers
