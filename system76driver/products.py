# system76-driver: Universal driver for System76 computers
# Copyright (C) 2005-2016 System76, Inc.
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
Map model name to list of driver actions.
"""

from . import actions


PRODUCTS = {
    # Adder
    'addw1': {
        'name': 'Adder WS',
        'drivers': [
            actions.blacklist_nvidia_i2c,
        ],
    },
    'addw2': {
        'name': 'Adder WS',
        'drivers': [
            actions.blacklist_nvidia_i2c,
        ],
    },

    # Bonobo:
    'bonp1': {
        'name': 'Bonobo Performance',
        'drivers': [],
    },
    'bonp2': {
        'name': 'Bonobo Performance',
        'drivers': [],
    },
    'bonp3': {
        'name': 'Bonobo Performance',
        'drivers': [],
    },
    'bonp4': {
        'name': 'Bonobo Professional',
        'drivers': [],
    },
    'bonp5': {
        'name': 'Bonobo Professional',
        'drivers': [],
    },
    'bonx6': {
        'name': 'Bonobo Extreme',
        'drivers': [
            actions.plymouth1080,
            actions.wifi_pm_disable,
        ],
    },
    'bonx7': {
        'name': 'Bonobo Extreme',
        'drivers': [
            #actions.plymouth1080,  # Causes problems with nvidia-313-updates
            actions.wifi_pm_disable,
        ],
    },
    'bonx8': {
        'name': 'Bonobo Extreme',
        'drivers': [
            actions.wifi_pm_disable,
        ],
    },
    'bonw9': {
        'name': 'Bonobo WS',
        'drivers': [],
    },
    'bonw10': {
        'name': 'Bonobo WS',
        'drivers': [
            actions.remove_gfxpayload_text,
        ],
    },
    'bonw11': {
        'name': 'Bonobo WS',
        'drivers': [
            actions.remove_backlight_vendor,
            actions.gfxpayload_text,
            actions.dac_fixup,
            actions.pulseaudio_hp_spdif_desc,
            actions.hidpi_scaling,
        ],
    },
    'bonw12': {
        'name': 'Bonobo WS',
        'drivers': [
            actions.remove_backlight_vendor,
            actions.dac_fixup,
            actions.pulseaudio_hp_spdif_desc,
            actions.hidpi_scaling,
        ],
    },
    'bonw13': {
        'name': 'Bonobo WS',
        'drivers': [
            actions.remove_backlight_vendor,
            actions.dac_fixup,
            actions.pulseaudio_hp_spdif_desc,
            actions.hidpi_scaling,
            actions.nvreg_enablebacklighthandler,
        ],
    },
    'bonw14': {
        'name': 'Bonobo WS',
        'drivers': [],
    },

    # Darter:
    'daru1': {
        'name': 'Darter Ultra',
        'drivers': [],
    },
    'daru2': {
        'name': 'Darter Ultra',
        'drivers': [],
    },
    'daru3': {
        'name': 'Darter Ultra',
        'drivers': [],
    },
    'daru4': {
        'name': 'Darter UltraTouch',
        'drivers': [
            actions.wifi_pm_disable,
            actions.hdmi_hotplug_fix,
            actions.backlight_vendor,
            actions.internal_mic_gain,
        ],
    },
    'darp5': {
        'name': 'Darter Pro',
        'drivers': [
            actions.headset_darp_fixup,
        ],
    },
    'darp6': {
        'name': 'Darter Pro',
        'drivers': [
            actions.headset_darp_fixup,
        ],
    },
    'darp7': {
        'name': 'Darter Pro',
        'drivers': [],
    },

    # Galago:
    'galu1': {
        'name': 'Galago UltraPro',
        'drivers': [
            actions.wifi_pm_disable,
            actions.internal_mic_gain,
            actions.hdmi_hotplug_fix,
        ],
    },
    'galp2': {
        'name': 'Galago Pro',
        'drivers': [
            actions.internal_mic_gain,
            actions.hidpi_scaling,
	    ],
    },
    'galp3': {
        'name': 'Galago Pro',
        'drivers': [
            actions.internal_mic_gain,
            actions.hidpi_scaling,
	    ],
    },
    'galp3-b': {
        'name': 'Galago Pro',
        'drivers': [
            actions.internal_mic_gain,
            actions.energystar_gsettings_override,
            actions.energystar_wakeonlan,
	    ],
    },
    'galp3-c': {
        'name': 'Galago Pro',
        'drivers': [],
    },
    'galp4': {
        'name': 'Galago Pro',
        'drivers': [],
    },
    'galp5': {
        'name': 'Galago Pro',
        'drivers': [
            actions.remove_nvidia_dynamic_power_one,
        ],
    },

    # Gazelle:
    'gazp1': {
        'name': 'Gazelle Performance',
        'drivers': [],
    },
    'gazp2': {
        'name': 'Gazelle Performance',
        'drivers': [],
    },
    'gazp3': {
        'name': 'Gazelle Performance',
        'drivers': [],
    },
    'gazp5': {
        'name': 'Gazelle Value with nVidia and Camera',
        'drivers': [],
    },
    'gazp6': {
        'name': 'Gazelle Professional',
        'drivers': [],
    },
    'gazp7': {
        'name': 'Gazelle Professional',
        'drivers': [
            actions.wifi_pm_disable,
        ],
    },
    'gazp8': {
        'name': 'Gazelle Professional',
        'drivers': [
            actions.lemu1,
            actions.wifi_pm_disable,
        ],
    },
    'gazp9': {
        'name': 'Gazelle Professional',
        'drivers': [
            actions.wifi_pm_disable,
            actions.hdmi_hotplug_fix,
            actions.backlight_vendor,  # Still needed for some early BIOS
        ],
    },
    'gazp9b': {
        'name': 'Gazelle Professional',
        'drivers': [
            actions.wifi_pm_disable,
            actions.hdmi_hotplug_fix,
            actions.remove_backlight_vendor,
            actions.internal_mic_gain,  # Only for gazp9b
        ],
    },
    'gazp9c': {
        'name': 'Gazelle Pro',
        'drivers': [
            actions.wifi_pm_disable,
            actions.hdmi_hotplug_fix,
            actions.internal_mic_gain,  # Only for gazp9b/gazp9c
        ],
    },
    'gaze10': {
        'name': 'Gazelle',
        'drivers': [
            actions.internal_mic_gain,
            actions.backlight_vendor,
        ],
    },
    'gaze11': {
        'name': 'Gazelle',
        'drivers': [
            actions.internal_mic_gain,
            actions.backlight_vendor,
        ],
    },
    'gaze12': {
        'name': 'Gazelle',
        'drivers': [
            actions.internal_mic_gain,
	],
    },
    'gaze13': {
        'name': 'Gazelle',
        'drivers': [
            actions.internal_mic_gain,
	],
    },
    'gaze14': {
        'name': 'Gazelle',
        'drivers': [
            actions.blacklist_nvidia_i2c,
            actions.i8042_nomux,
        ],
    },
    'gaze15': {
        'name': 'Gazelle',
        'drivers': [
            actions.blacklist_nvidia_i2c,
            actions.i8042_nomux,
        ],
    },
    'gaze16-3050': {
        'name': 'Gazelle',
        'drivers': [
            actions.blacklist_nvidia_i2c,
        ],
    },
    'gaze16-3060': {
        'name': 'Gazelle',
        'drivers': [
            actions.blacklist_nvidia_i2c,
        ],
    },
    'gaze16-3060-b': {
        'name': 'Gazelle',
        'drivers': [
            actions.blacklist_nvidia_i2c,
        ],
    },
    'gazu1': {
        'name': 'Gazelle Ultra',
        'drivers': [
            actions.uvcquirks,
        ],
    },
    'gazv1': {
        'name': 'Gazelle Value',
        'drivers': [],
    },
    'gazv2': {
        'name': 'Gazelle Value',
        'drivers': [],
    },
    'gazv3': {
        'name': 'Gazelle Value',
        'drivers': [],
    },
    'gazv4': {
        'name': 'Gazelle Value',
        'drivers': [],
    },
    'gazv5': {
        'name': 'Gazelle Value',
        'drivers': [],
    },

    # Koala:
    'koap1': {
        'name': 'Koala Performance',
        'drivers': [],
    },

    # Kudu:
    'kudp1': {
        'name': 'Kudu Professional',
        'drivers': [
            actions.wifi_pm_disable,
            actions.hdmi_hotplug_fix,
        ],
    },
    'kudp1b': {
        'name': 'Kudu Professional',
        'drivers': [
            actions.wifi_pm_disable,
            actions.hdmi_hotplug_fix,
            actions.internal_mic_gain,  # Only for kudp1b
        ],
    },
    'kudp1c': {
        'name': 'Kudu Pro',
        'drivers': [
            actions.wifi_pm_disable,
            actions.hdmi_hotplug_fix,
            actions.internal_mic_gain,  # Only for kudp1b/kudp1c
        ],
    },
    'kudu2': {
        'name': 'Kudu',
        'drivers': [
            actions.internal_mic_gain,
            actions.backlight_vendor,
        ],
    },
    'kudu3': {
        'name': 'Kudu',
        'drivers': [
            actions.internal_mic_gain,
            actions.backlight_vendor,
        ],
    },
    'kudu4': {
        'name': 'Kudu',
        'drivers': [
            actions.internal_mic_gain,
        ],
    },
    'kudu5': {
        'name': 'Kudu',
        'drivers': [
            actions.internal_mic_gain,
        ],
    },
    'kudu6': {
        'name': 'Kudu',
        'drivers': [],
    },

    # Lemur:
    'lemu1': {
        'name': 'Lemur UltraThin',
        'drivers': [],
    },
    'lemu2': {
        'name': 'Lemur UltraThin',
        'drivers': [],
    },
    'lemu3': {
        'name': 'Lemur Ultra',
        'drivers': [],
    },
    'lemu4': {
        'name': 'Lemur Ultra',
        'drivers': [
            actions.wifi_pm_disable,
            actions.lemu1,
        ],
    },
    'lemu5': {
        'name': 'Lemur',
        'drivers': [
            actions.backlight_vendor,
            actions.internal_mic_gain,
            actions.wifi_pm_disable,
            actions.hdmi_hotplug_fix,
        ],
    },
    'lemu6': {
        'name': 'Lemur',
        'drivers': [
            actions.internal_mic_gain,
        ],
    },
    'lemu7': {
        'name': 'Lemur',
        'drivers': [
            actions.internal_mic_gain,
        ],
    },
    'lemu8': {
        'name': 'Lemur',
        'drivers': [
            actions.internal_mic_gain,
        ],
    },
    'lemp9': {
        'name': 'Lemur Pro',
        'drivers': [
            actions.intel_idle_max_cstate_4
        ],
    },
    'lemp10': {
        'name': 'Lemur Pro',
        'drivers': [],
    },

    # Leopard:
    'leo1': {
        'name': 'Leopard Extreme',
        'drivers': [],
    },
    'leox2': {
        'name': 'Leopard Extreme',
        'drivers': [],
    },
    'leox3': {
        'name': 'Leopard Extreme',
        'drivers': [],
    },
    'leox4': {
        'name': 'Leopard Extreme',
        'drivers': [],
    },
    'leox5': {
        'name': 'Leopard Extreme',
        'drivers': [],
    },
    'leow6': {
        'name': 'Leopard WS',
        'drivers': [],
    },
    'leow7': {
        'name': 'Leopard WS',
        'drivers': [],
    },
    'leow8': {
        'name': 'Leopard WS',
        'drivers': [],
    },
    'leow9': {
        'name': 'Leopard WS',
        'drivers': [],
    },
    'leow9-b': {
        'name': 'Leopard WS',
        'drivers': [],
    },
    'leow9-w': {
        'name': 'Leopard WS',
        'drivers': [],
    },

    # Meerkat:
    'meec1': {
        'name': 'Meerkat Compact',
        'drivers': [],
    },
    'ment1': {
        'name': 'Meerkat NetTop',
        'drivers': [],
    },
    'ment2': {
        'name': 'Meerkat Ion NetTop',
        'drivers': [],
    },
    'ment3': {
        'name': 'Meerkat NetTop',
        'drivers': [],
    },
    'ment5': {
        'name': 'Meerkat Ion NetTop',
        'drivers': [],
    },
    'meer1': {
        'name': 'Meerkat',
        'drivers': [
            actions.disable_pm_async,
        ],
    },
    'meer2': {
        'name': 'Meerkat',
        'drivers': [],
    },
    'meer3': {
        'name': 'Meerkat',
        'drivers': [
            actions.headset_meer3_fixup,
        ],
    },
    'meer4': {
        'name': 'Meerkat',
        'drivers': [],
    },
    'meer5': {
        'name': 'Meerkat',
        'drivers': [
            actions.headset_meer5_fixup,
            actions.meer5_audio_hdajackretask,
        ],
    },
    'meer6': {
        'name': 'Meerkat',
        'drivers': [
            actions.displayport1_force_enable_audio,
        ],
    },

    # Oryx:
    'orxp1': {
        'name': 'Oryx Pro',
        'drivers': [
            actions.remove_gfxpayload_text,
            actions.nvreg_enablebacklighthandler,
        ],
    },
    'oryp2': {
        'name': 'Oryx Pro',
        'drivers': [
            actions.remove_backlight_vendor,
            actions.i8042_reset_nomux,
            actions.hidpi_scaling,
            actions.nvreg_enablebacklighthandler,
        ],
    },
    'oryp2-ess': {
        'name': 'Oryx Pro',
        'drivers': [
            actions.remove_backlight_vendor,
            actions.i8042_reset_nomux,
            actions.dac_fixup,
            actions.pulseaudio_hp_spdif_desc,
            actions.hidpi_scaling,
        ],
    },
    'oryp3': {
        'name': 'Oryx Pro',
        'drivers': [
            actions.remove_backlight_vendor,
            actions.hidpi_scaling,
            actions.nvreg_enablebacklighthandler,
        ],
    },
    'oryp3-ess': {
        'name': 'Oryx Pro',
        'drivers': [
            actions.remove_backlight_vendor,
            actions.dac_fixup,
            actions.pulseaudio_hp_spdif_desc,
            actions.hidpi_scaling,
        ],
    },
    'oryp3-b': {
        'name': 'Oryx Pro',
        'drivers': [
            actions.remove_backlight_vendor,
            actions.hidpi_scaling,
        ],
    },
    'oryp4': {
        'name': 'Oryx Pro',
        'drivers': [
            actions.hidpi_scaling,
            actions.limit_tdp,
        ],
    },
    'oryp4-b': {
        'name': 'Oryx Pro',
        'drivers': [
            actions.hidpi_scaling,
            actions.remove_switch_internal_speakers,
        ],
    },
    'oryp5': {
        'name': 'Oryx Pro',
        'drivers': [
            actions.hda_probe_mask,
            actions.blacklist_nvidia_i2c,
        ],
    },
    'oryp6': {
        'name': 'Oryx Pro',
        'drivers': [
            actions.blacklist_nvidia_i2c,
            actions.i915_initramfs,
        ],
    },
    'oryp7': {
        'name': 'Oryx Pro',
        'drivers': [
            actions.blacklist_nvidia_i2c,
            actions.i915_initramfs,
        ],
    },
    'oryp8': {
        'name': 'Oryx Pro',
        'drivers': [
            actions.blacklist_nvidia_i2c,
            actions.i915_initramfs,
        ],
    },

    # Pangolin:
    'panp4i': {
        'name': 'Pangolin Performance',
        'drivers': [],
    },
    'panp4n': {
        'name': 'Pangolin Performance',
        'drivers': [],
    },
    'panp5': {
        'name': 'Pangolin Performance',
        'drivers': [],
    },
    'panp6': {
        'name': 'Pangolin Performance',
        'drivers': [],
    },
    'panp7': {
        'name': 'Pangolin Performance',
        'drivers': [
            actions.radeon_dpm,
        ],
    },
    'panp8': {
        'name': 'Pangolin Performance',
        'drivers': [],
    },
    'panp9': {
        'name': 'Pangolin Performance',
        'drivers': [
            actions.wifi_pm_disable,
            actions.lemu1,
        ],
    },
    'pang10': {
        'name': 'Pangolin',
        'drivers': [
            actions.pang10_nvme_fix,
        ],
    },
    'pang11': {
        'name': 'Pangolin',
        'drivers': [
            actions.i8042_nomux,
        ],
    },
    #'panv1': {'name': 'Pangolin Value'},  # FIXME: Not in model.py
    'panv2': {
        'name': 'Pangolin Value',
        'drivers': [],
    },
    'panv3': {
        'name': 'Pangolin Value',
        'drivers': [],
    },

    # Ratel:
    'ratp1': {
        'name': 'Ratel Performance',
        'drivers': [],
    },
    'ratp2': {
        'name': 'Ratel Performance',
        'drivers': [],
    },
    'ratp3': {
        'name': 'Ratel Performance',
        'drivers': [],
    },
    'ratp4': {
        'name': 'Ratel Performance',
        'drivers': [],
    },
    'ratp5': {
        'name': 'Ratel Pro',
        'drivers': [],
    },
    'ratu1': {
        'name': 'Ratel Ultra',
        'drivers': [],
    },
    'ratu2': {
        'name': 'Ratel Ultra',
        'drivers': [],
    },
    'ratv1': {
        'name': 'Ratel Value',
        'drivers': [],
    },
    'ratv2': {
        'name': 'Ratel Value',
        'drivers': [],
    },
    'ratv3': {
        'name': 'Ratel Value',
        'drivers': [],
    },
    'ratv4': {
        'name': 'Ratel Value',
        'drivers': [],
    },
    'ratv5': {
        'name': 'Ratel Value',
        'drivers': [],
    },
    'ratv6': {
        'name': 'Ratel Value',
        'drivers': [],
    },

    # Sable:
    'sabc1': {
        'name': 'Sable Complete',
        'drivers': [],
    },
    'sabc2': {
        'name': 'Sable Complete',
        'drivers': [],
    },
    'sabc3': {
        'name': 'Sable Complete',
        'drivers': [],
    },
    'sabl4': {
        'name': 'Sable',
        'drivers': [],
    },
    'sabl5': {
        'name': 'Sable',
        'drivers': [],
    },
    'sabl6': {
        'name': 'Sable',
        'drivers': [],
    },
    'sabt1': {
        'name': 'Sable Touch',
        'drivers': [],
    },
    'sabt2': {
        'name': 'Sable Touch',
        'drivers': [],
    },
    'sabt3': {
        'name': 'Sable Touch',
        'drivers': [],
    },
    'sabv1': {
        'name': 'Sable Series',
        'drivers': [],
    },
    'sabv2': {
        'name': 'Sable Series',
        'drivers': [],
    },
    'sabv3': {
        'name': 'Sable Series',
        'drivers': [],
    },

    # Serval:
    'serp1': {
        'name': 'Serval Performance',
        'drivers': [],
    },
    'serp2': {
        'name': 'Serval Performance',
        'drivers': [],
    },
    'serp3': {
        'name': 'Serval Performance',
        'drivers': [],
    },
    'serp4': {
        'name': 'Serval Performance',
        'drivers': [],
    },
    'serp5': {
        'name': 'Serval Professional',
        'drivers': [],
    },
    'serp6': {
        'name': 'Serval Professional',
        'drivers': [],
    },
    'serp7': {
        'name': 'Serval Professional',
        'drivers': [],
    },
    'serw8-15': {
        'name': 'Serval WS',
        'drivers': [],
    },
    'serw8-17': {
        'name': 'Serval WS',
        'drivers': [],
    },
    'serw8-17g': {
        'name': 'Serval WS',
        'drivers': [],
    },
    'serw9': {
        'name': 'Serval WS',
        'drivers': [
            actions.remove_gfxpayload_text,
        ],
    },
    'serw10': {
        'name': 'Serval WS',
        'drivers': [
            actions.remove_backlight_vendor,
            actions.dac_fixup,
            actions.pulseaudio_hp_spdif_desc,
            actions.hidpi_scaling,
        ],
    },
    'serw11': {
        'name': 'Serval WS',
        'drivers': [
            actions.remove_backlight_vendor,
            actions.dac_fixup,
            actions.pulseaudio_hp_spdif_desc,
            actions.hidpi_scaling,
            actions.nvreg_enablebacklighthandler,
        ],
    },
    'serw11-b': {
        'name': 'Serval WS',
        'drivers': [
            actions.remove_backlight_vendor,
            actions.dac_fixup,
            actions.pulseaudio_hp_spdif_desc,
            actions.hidpi_scaling,
            actions.nvreg_enablebacklighthandler,
        ],
    },
    'serw12': {
        'name': 'Serval WS',
        'drivers': [
            actions.firefox_framerate144,
            actions.firefox_unsetwebrender,
            actions.nvidia_forcefullcompositionpipeline,
            actions.i8042_nomux,
        ],
    },

    # Silverback:
    'silw1': {
        'name': 'Silverback WS',
        'drivers': [],
    },
    'silw2': {
        'name': 'Silverback WS',
        'drivers': [],
    },
    'silw3': {
        'name': 'Silverback WS',
        'drivers': [],
    },

    # Starling:
    'star1': {
        'name': 'Starling NetBook',
        'drivers': [],
    },
    'star2': {
        'name': 'Starling EduBook',
        'drivers': [],
    },
    'star3': {
        'name': 'Starling NetBook',
        'drivers': [],
    },
    'star4': {
        'name': 'Starling NetBook',
        'drivers': [],
    },
    'star5': {
        'name': 'Starling NetBook',
        'drivers': [],
    },

    #Thelio:
    'thelio-b1': {
        'name': 'Thelio',
        'drivers': [],
    },
    'thelio-b2': {
        'name': 'Thelio',
        'drivers': [],
    },
    'thelio-r1': {
        'name': 'Thelio',
        'drivers': [],
    },
    'thelio-r2': {
        'name': 'Thelio',
        'drivers': [
            actions.hda_disable_power_save,
        ],
    },
    'thelio-major-b1': {
        'name': 'Thelio Major',
        'drivers': [],
    },
    'thelio-major-b1.1': {
        'name': 'Thelio Major',
        'drivers': [],
    },
    'thelio-major-b2': {
        'name': 'Thelio Major',
        'drivers': [],
    },
    'thelio-major-b3': {
        'name': 'Thelio Major',
        'drivers': [],
    },
    'thelio-major-r1': {
        'name': 'Thelio Major',
        'drivers': [],
    },
    'thelio-major-r2': {
        'name': 'Thelio Major',
        'drivers': [
            actions.usb_audio_ignore_ctl_error,
            actions.remove_usb_audio_load_microphone,
            actions.remove_usb_audio_load_spdif,
        ],
    },
    'thelio-major-r2.1': {
        'name': 'Thelio Major',
        'drivers': [
            actions.usb_audio_ignore_ctl_error,
            actions.remove_usb_audio_load_microphone,
            actions.remove_usb_audio_load_spdif,
        ],
    },
    'thelio-massive-b1': {
        'name': 'Thelio Massive',
        'drivers': [],
    },
    'thelio-mega-b1': {
        'name': 'Thelio Mega',
        'drivers': [],
    },
    'thelio-mega-r1': {
        'name': 'Thelio Mega',
        'drivers': [
            actions.usb_audio_ignore_ctl_error,
            actions.remove_usb_audio_load_microphone,
            actions.remove_usb_audio_load_spdif,
        ],
    },
    'thelio-mega-r1.1': {
        'name': 'Thelio Mega',
        'drivers': [
            actions.usb_audio_ignore_ctl_error,
            actions.remove_usb_audio_load_microphone,
            actions.remove_usb_audio_load_spdif,
        ],
    },
    'thelio-mira-b1': {
        'name': 'Thelio Mira',
        'drivers': [
            actions.integrated_11th_gen_intel_fix,
        ],
    },
    'thelio-mira-r1': {
        'name': 'Thelio Mira',
        'drivers': [],
    },

    # Wildebeest:
    'wilb1': {
        'name': 'Wildebeest Performance',
        'drivers': [],
    },
    'wilb2': {
        'name': 'Wildebeest Performance',
        'drivers': [],
    },

    # Wild Dog:
    'wilp1': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp2': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp3': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp5': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp6': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp7': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp8': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp9': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp10': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp11': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp12': {
        'name': 'Wild Dog Pro',
        'drivers': [],
    },
    'wilp13': {
        'name': 'Wild Dog Pro',
        'drivers': [],
    },
    'wilp14': {
        'name': 'Wild Dog Pro',
        'drivers': [],
    },
}
