"""
Gtk UI.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os

import logging

log = logging.getLogger(__name__)

from .firmware import get_ec_version, get_bios_version, run_firmware_updater, get_processed_changelog, needs_update

from . import get_datafile

print(os.environ)

class FirmwareWindow (Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="System76 Firmware Updater")
        self.set_size_request(480, 300)
        self.box = Gtk.VBox()
        self.box.set_margin_top(6)
        self.box.set_margin_left(9)
        self.box.set_margin_right(9)
        self.add(self.box)
        
        self.titlebar = Gtk.HeaderBar()
        self.titlebar.set_show_close_button(True)
        
        image = Gtk.Image()
        image.set_from_file(get_datafile('76icon.svg'))
        image.set_padding(6, 6)
        self.titlebar.set_custom_title(image)
        self.set_titlebar(self.titlebar)
        
        changelog = get_processed_changelog()
        
        self.create_version_ui()
        self.create_update_available_label(changelog['versions'][0]['bios'], changelog['versions'][0]['ec'])
        self.create_changelog_ui(changelog)
        self.create_install_button()
        
    def create_version_ui(self):
        ec = get_ec_version()
        bios = get_bios_version()
        
        self.grid = Gtk.Grid(column_homogeneous=True, column_spacing=10)
        self.grid.set_halign(Gtk.Align.CENTER)
        
        row = 0
        col = 0
        for l in ['Installed', 'Latest']:
            label = Gtk.Label()
            label.set_markup('<b>' + l + '</b>')
            label.set_xalign(0.5)
            self.grid.attach(label, col, row, 2, 1)
            col = col + 2
            
        for col in [0,2]:
            row = 2
            for key, value in [('BIOS', bios), ('EC', ec)]:
                key_label = Gtk.Label('<b>' + key + '</b>', use_markup=True)
                key_label.set_xalign(1)
                value_label = Gtk.Label(value)
                value_label.set_xalign(0)
                self.grid.attach(key_label, col, row, 1, 1)
                self.grid.attach(value_label, col + 1, row, 1, 1)
                row = row + 1
                
        self.box.pack_start(self.grid, False, False, 3)
    
    def create_update_available_label(self, new_bios, new_ec):
        self.note = Gtk.Label("Your computer's firmware is up-to-date.")
        if needs_update(new_bios, new_ec):
            self.note.set_markup("<b>Updates are available for your computer</b>")
        self.note.set_vexpand(False)
        self.box.pack_start(self.note, False, False, 3)
    
    def create_changelog_ui(self, changelog):
        self.changelog_expander = Gtk.Expander()
        self.changelog_expander.set_label('Change history')
        
        scrollwindow = Gtk.ScrolledWindow(min_content_height=100, min_content_width=400)
        scrollwindow.set_vexpand(True)
        
        viewport = Gtk.Viewport(shadow_type=Gtk.ShadowType.IN)
        
        vbox = Gtk.VBox()
        vbox.set_valign(Gtk.Align.START)
        
        row = 0
        for version in changelog['versions']:
            self.changelog_grid = Gtk.Grid(column_spacing=10)
            description_label = Gtk.Label(version['description'])
            description_label.set_xalign(0)
            description_label.set_yalign(0)
            self.changelog_grid.attach(description_label, 3, row, 4, 4)
            for key in ['bios', 'ec', 'me']:
                key_label = Gtk.Label(key)
                key_label.set_xalign(0)
                value_label = Gtk.Label(version[key])
                key_label.set_xalign(1)
                self.changelog_grid.attach(key_label, 0, row, 1, 1)
                self.changelog_grid.attach(value_label, 1, row, 1, 1)
                row = row + 1
            vbox.pack_start(self.changelog_grid, False, False, 3)
            vbox.pack_start(Gtk.Separator(), True, False, 3)
        
        scrollwindow.add(vbox)
        viewport.add(scrollwindow)
        self.changelog_expander.add(viewport)
        self.box.pack_start(self.changelog_expander, True, True, 3)
        
    def create_install_button(self):
        self.button = Gtk.Button("Install Firmware", always_show_image=True)
        image = Gtk.Image()
        image.set_from_file(get_datafile('download-firmware-icon.svg'))
        image.set_padding(6, 6)
        self.button.set_image(image)
        self.button.set_image_position(Gtk.PositionType.TOP)
        self.button.set_size_request(200, 96)
        self.button.set_relief(Gtk.ReliefStyle.NONE)
        self.button.set_valign(Gtk.Align.END)
        
        self.button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        print(self.button.get_style_context().list_classes())
        self.button.connect('clicked', self.run_firmware_updater)
        self.box.pack_start(self.button, False, False, 12)
        
    def run_firmware_updater(self, e):
        self.hide()
        while Gtk.events_pending():
            Gtk.main_iteration()
        run_firmware_updater(True, use_notifications=False)
        os._exit(0)

class UI:
    def __init__(self, args):
        self.window = FirmwareWindow()
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()
        Gtk.main()
