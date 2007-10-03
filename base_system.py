#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## /opt/system76/drivers/all/src/base_system.py
## Installs base system applications and settings

import os
import time
import model
import ubuntuversion

## KEEP ALL MODELS IN ALPHABETICAL ORDER

def app_install():
    """
    Install appropriate applications for each model
    """

    today = time.strftime('%Y%m%d_h%Hm%Ms%S')
    modelname = model.determine_model()
    version = ubuntuversion.release()

    # Model Z35FM / System76 Model Darter Ultra
    if modelname == ('daru1'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver gsynaptics i855-crt network-manager-gnome linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnome-bluetooth gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver gsynaptics i855-crt network-manager-gnome linux-restricted-modules-generic linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnome-bluetooth bluetooth gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver gsynaptics i855-crt')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver gsynaptics')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Model MS-1221 / System76 Model Darter Ultra 2
    if modelname == ('daru2'):
        if version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install xserver-xorg-video-intel gnome-bluetooth bluetooth gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver gsynaptics i855-crt')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_new_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver gsynaptics')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Model Z62F / System76 model Gazelle Performance
    elif modelname == ('gazp1'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver gsynaptics i855-crt network-manager-gnome linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install camorama 915resolution gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver gsynaptics i855-crt network-manager-gnome linux-restricted-modules-generic linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install camorama 915resolution gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver gsynaptics i855-crt')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver gsynaptics')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Model S62J / System76 model Gazelle Performance
    elif modelname == ('gazp2'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver gsynaptics network-manager-gnome linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install camorama nvidia-glx gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver gsynaptics network-manager-gnome linux-restricted-modules-generic linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install camorama nvidia-glx gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver gsynaptics')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver gsynaptics')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Model S62JP / System76 model Gazelle Performance
    elif modelname == ('gazp3'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install camorama nvidia-glx grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver gsynaptics network-manager-gnome linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install camorama nvidia-glx gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver gsynaptics network-manager-gnome linux-restricted-modules-generic linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install camorama nvidia-glx gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver gsynaptics')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver gsynaptics')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Model SW1 / System76 model Gazelle Value
    if modelname == ('gazv2'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver gsynaptics i855-crt systemconfigurator network-manager-gnome linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver gsynaptics i855-crt systemconfigurator network-manager-gnome linux-restricted-modules-generic linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver gsynaptics i855-crt')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver gsynaptics')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Model Z62FP / System76 model Gazelle Value
    if modelname == ('gazv3'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver gsynaptics i855-crt systemconfigurator network-manager-gnome linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver gsynaptics i855-crt systemconfigurator network-manager-gnome linux-restricted-modules-generic linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver gsynaptics i855-crt')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver gsynaptics')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Model Z62FM / System76 model Gazelle Value
    if modelname == ('gazv4'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver gsynaptics i855-crt systemconfigurator network-manager-gnome linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver gsynaptics i855-crt systemconfigurator network-manager-gnome linux-restricted-modules-generic linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver gsynaptics i855-crt')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver gsynaptics')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # System76 Model Gazelle Value 5
    if modelname == ('gazv5'):
        if version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install xserver-xorg-video-intel gnome-bluetooth bluetooth gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver i855-crt')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_new_notebook /etc/X11/xorg.conf')
            # Setup Panel and Super_L key
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Model Mini PC / System76 model Koala Performance
    elif modelname == ('koap1'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver systemconfigurator network-manager-gnome')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver systemconfigurator network-manager-gnome linux-restricted-modules-generic')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver gsynaptics i855-crt')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Model S96F / System76 model Pangolin Value
    elif modelname == ('panv2'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver gsynaptics i855-crt systemconfigurator linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver gsynaptics i855-crt systemconfigurator network-manager-gnome linux-restricted-modules-generic linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install 915resolution gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver gsynaptics i855-crt')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver gsynaptics')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # System76 Model Pangolin Value 3
    if modelname == ('panv3'):
        if version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install xserver-xorg-video-intel gnome-bluetooth bluetooth gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver i855-crt')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_new_notebook /etc/X11/xorg.conf')
            # Setup Hotkeys
            os.system("echo setkeycodes e076 221 >> /etc/init.d/bootmisc.sh")
            os.system("echo setkeycodes e075 220 >> /etc/init.d/bootmisc.sh")
            os.system('sudo cp /opt/system76/system76-driver/src/hotkeys/panv3_xmodmap.conf /etc/xmodmap.conf')
            os.system('sudo cp /opt/system76/system76-driver/src/hotkeys/panv3_Default /etc/X11/gdm/PostLogin/Default')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/keybinding_commands/command_10 'rhythmbox'")
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/keybinding_commands/command_11 'totem'")
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/run_command_10 'XF86Music'")
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/run_command_11 'XF86Video'")
            # Setup Panel and Super_L key
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Model V2-AH1 / System76 model Ratel Value
    elif modelname == ('ratv1'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver systemconfigurator network-manager-gnome')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_via_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver systemconfigurator network-manager-gnome linux-restricted-modules-generic')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_via_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_via_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # System76 Model Ratel Value
    elif modelname == ('ratv2'):
        if version == ('6.06'):
            a = os.popen('lspci | grep nV')
            try:
                nvidia = a.readline().strip()
            finally:
                a.close()
            graphics = nvidia[35:41]
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver systemconfigurator network-manager-gnome')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            if graphics == 'nVidia':
                os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
                os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
                os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            else:
                os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_via_desktop /etc/X11/xorg.conf')
        elif version == ('6.10'):
            a = os.popen('lspci | grep nV')
            try:
                nvidia = a.readline().strip()
            finally:
                a.close()
            graphics = nvidia[35:41]
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver systemconfigurator network-manager-gnome linux-restricted-modules-generic')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            if graphics == 'nVidia':
                os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
                os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
                os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            else:
                os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_via_desktop /etc/X11/xorg.conf')
        elif version == ('7.04'):
            a = os.popen('lspci | grep nV')
            try:
                nvidia = a.readline().strip()
            finally:
                a.close()
            graphics = nvidia[35:41]
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            if graphics == 'nVidia':
                os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
                os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
                os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            else:
                os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_via_desktop /etc/X11/xorg.conf')
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # System76 Model Ratel Value
    elif modelname == ('ratv3'):
        if version == ('6.06'):
            a = os.popen('lspci | grep nV')
            try:
                nvidia = a.readline().strip()
            finally:
                a.close()
            graphics = nvidia[35:41]
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver systemconfigurator network-manager-gnome')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            if graphics == 'nVidia':
                os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
                os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
                os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            else:
                os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_via_desktop /etc/X11/xorg.conf')
        elif version == ('6.10'):
            a = os.popen('lspci | grep nV')
            try:
                nvidia = a.readline().strip()
            finally:
                a.close()
            graphics = nvidia[35:41]
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver systemconfigurator network-manager-gnome linux-restricted-modules-generic')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            if graphics == 'nVidia':
                os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
                os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
                os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            else:
                os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_via_desktop /etc/X11/xorg.conf')
        elif version == ('7.04'):
            a = os.popen('lspci | grep nV')
            try:
                nvidia = a.readline().strip()
            finally:
                a.close()
            graphics = nvidia[35:41]
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            if graphics == 'nVidia':
                os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
                os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
                os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            else:
                os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_via_desktop /etc/X11/xorg.conf')
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Model P1-AH1 / System76 model Sable Value
    elif modelname == ('sabv1'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver systemconfigurator network-manager-gnome')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver systemconfigurator network-manager-gnome linux-restricted-modules-generic')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # System76 Model Sable Value & Sable Performance (sabv2/sabv1)
    elif modelname == ('sabv2'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver systemconfigurator network-manager-gnome')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver systemconfigurator network-manager-gnome linux-restricted-modules-generic')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')            
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Model EL80 / System76 model Serval Performance
    elif modelname == ('serp1'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver systemconfigurator linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver systemconfigurator network-manager-gnome linux-restricted-modules-generic linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnome-bluetooth bluetooth nvidia-glx gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # System76 Serval Performace
    # Model EL80 / System76 model Serval Performance
    elif modelname == ('serp2'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver systemconfigurator linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver systemconfigurator network-manager-gnome linux-restricted-modules-generic linux-headers-`uname -r`')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnome-bluetooth bluetooth nvidia-glx gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_notebook /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # System76 Model Serval Performance 3 (serp3)
    if modelname == ('serp3'):
        if version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            # TODO: Nvidia installation and configuration
            #os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            #os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_intel_new_notebook /etc/X11/xorg.conf')
            # Setup Hotkeys
            os.system("echo setkeycodes e076 221 >> /etc/init.d/bootmisc.sh")
            os.system("echo setkeycodes e075 220 >> /etc/init.d/bootmisc.sh")
            os.system('sudo cp /opt/system76/system76-driver/src/hotkeys/panv3_xmodmap.conf /etc/xmodmap.conf')
            os.system('sudo cp /opt/system76/system76-driver/src/hotkeys/panv3_Default /etc/X11/gdm/PostLogin/Default')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/keybinding_commands/command_10 'rhythmbox'")
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/keybinding_commands/command_11 'totem'")
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/run_command_10 'XF86Music'")
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/run_command_11 'XF86Video'")
            # Setup Panel and Super_L key
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Model Wild Dog Performance
    elif modelname == ('wilp1'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver systemconfigurator')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver systemconfigurator')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries linux-restricted-modules-generic')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Wild Dog Professional
    elif modelname == ('wilp2'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver systemconfigurator')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver systemconfigurator')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries linux-restricted-modules-generic')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
    # Wild Dog Professional
    elif modelname == ('wilp3'):
        if version == ('6.06'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_dapper /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx grisbi tomboy beagle beagle-backend-evolution inkscape f-spot system76-driver systemconfigurator')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('6.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_edgy /etc/apt/sources.list')
            os.system('sudo cp -r /opt/system76/system76-driver/src/yanc /opt/')
            os.system('sudo cp /opt/system76/system76-driver/src/yanc.desktop /usr/share/applications/')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash tomboy beagle beagle-backend-evolution inkscape system76-driver systemconfigurator')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries linux-restricted-modules-generic')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.04'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_feisty /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install nvidia-glx gnucash beagle beagle-backend-evolution mozilla-beagle inkscape system76-driver')
            os.system('sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/xorg.conf_nvidia_desktop /etc/X11/xorg.conf')
            os.system('sudo gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --load /opt/system76/system76-driver/src/76-panel-setup.entries')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
        elif version == ('7.10'):
            os.system('sudo cp /etc/apt/sources.list /etc/apt/sources.list_sys76backup_%s' % today)
            os.system('sudo cp /opt/system76/system76-driver/src/sources.list_gutsy /etc/apt/sources.list')
            os.system('sudo apt-get update')
            os.system('sudo apt-get --assume-yes install gnucash system76-driver')
            os.system("gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/metacity/global_keybindings/panel_main_menu 'Super_L'")
                