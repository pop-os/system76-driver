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
Gtk UI.
"""

import distro
import threading
from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk

from . import __version__, get_datafile
from .util import create_logs
from .actions import ActionRunner


GLib.threads_init()


class UI:
    def __init__(self, model, product, args):
        assert isinstance(model, str)
        assert product is None or isinstance(product, dict)
        assert isinstance(args.dry, bool)
        self.thread = None
        self.model = model
        self.product = product
        self.args = args
        self.builder = Gtk.Builder()
        self.builder.add_from_file(get_datafile('gtk3.glade'))
        self.window = self.builder.get_object('mainWindow')
        self.notify_icon = self.builder.get_object('notifyImage')
        self.notify_text = self.builder.get_object('notifyLabel')
        self.details = self.builder.get_object('detailsText')
        self.builder.get_object('sysModel').set_text(model)
        self.builder.get_object('ubuntuVersion').set_text(
            '{} {} ({})'.format(*distro.linux_distribution())
        )
        self.builder.get_object('driverVersion').set_text(__version__)

        self.builder.connect_signals({
            'onDeleteWindow': Gtk.main_quit,
            'onCloseClicked': Gtk.main_quit,
            'onInstallClicked': self.onInstallClicked,
            'onRestoreClicked': self.onRestoreClicked,
            'onCreateClicked': self.onCreateClicked,
            'onAboutClicked': self.onAboutClicked,
        })

        self.buttons = dict(
            (key, self.builder.get_object(key))
            for key in ['driverInstall', 'driverRestore', 'driverCreate']
        )
        self.enabled = {
            'driverInstall': False,
            'driverRestore': False,
            'driverCreate': False,
        }
        self.set_sensitive(False)

        if product:
            name = product['name']
        else:
            name = _('Non System76 Product')
            self.set_notify('gtk-dialog-error',
                _('Not a System76 product, nothing to do!')
            )
        self.builder.get_object('sysName').set_text(name)

    def prepare_action_runner(self):
        self.enabled['driverCreate'] = True
        self.action_runner = ActionRunner(self.product['drivers'])
        if not self.action_runner.actions:
            msg = _('All of the drivers for this system are provided by Ubuntu.')
            self.set_notify('gtk-ok', msg)
            self.details.set_text(msg)
        else:
            lines = []
            for action in self.action_runner.actions:
                template = ('+ {}' if action.isneeded else '* {}')
                lines.append(template.format(action.description))
            self.details.set_text('\n'.join(lines))
            if self.action_runner.needed:
                self.enabled['driverInstall'] = True
                self.enabled['driverRestore'] = True
            else:
                msg = _('All drivers have been applied, nothing to do.')
                self.set_notify('gtk-ok', msg)
        self.set_sensitive(True)

    def set_sensitive(self, sensitive):
        for (key, button) in self.buttons.items():
            button.set_sensitive(sensitive and self.enabled[key])

    def set_notify(self, icon, text):
        self.notify_text.show()
        self.notify_icon.show()
        self.notify_text.set_text(text)
        self.notify_icon.set_from_stock(icon, 4)

    def run(self):
        self.window.show()
        if self.product:
            GLib.idle_add(self.prepare_action_runner)
        Gtk.main()

    def worker_thread(self, actions):
        for msg in self.action_runner.run_iter():
            print(msg)
        GLib.idle_add(self.on_worker_complete)

    def on_worker_complete(self):
        self.thread.join()
        self.thread = None
        self.set_notify('gtk-apply',
            'Installation is complete! Please reboot for changes to take effect.'
        )
        self.set_sensitive(True)

    def start_worker(self):
        if self.thread is None:
            self.set_sensitive(False)
            self.set_notify('gtk-execute',
                _('Now installing drivers. This may take a while...')
            )
            self.thread = threading.Thread(
                target=self.worker_thread,
                args=(self.product['drivers'],),
                daemon=True,
            )
            self.thread.start()

    def onInstallClicked(self, button):
        print('onInstallClicked')
        self.start_worker()

    def onRestoreClicked(self, button):
        print('onRestoreClicked')
        self.start_worker()

    def create_worker(self):
        tgz = create_logs(self.args.home)
        GLib.idle_add(self.on_create_complete, tgz)

    def on_create_complete(self, tgz):
        self.thread.join()
        self.thread = None
        self.set_sensitive(True)
        self.set_notify('gtk-ok',
            _('A log file (system76-logs.tgz) was created in your home folder.\nPlease send it to support via www.system76.com/support')
        )

    def onCreateClicked(self, button):
        if self.thread is None:
            self.set_sensitive(False)
            self.set_notify('gtk-execute', _('Creating logs...'))
            self.thread = threading.Thread(
                target=self.create_worker,
                daemon=True,
            )
            self.thread.start()

    def onAboutClicked(self, button):
        aboutDialog = self.builder.get_object('aboutDialog')
        aboutDialog.set_version(__version__)
        aboutDialog.run()
        aboutDialog.hide()
