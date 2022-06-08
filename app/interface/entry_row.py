from cgitb import enable
from gi.repository import Gtk

from ..entry import Entry
from .. import utils

class EntryRow(Gtk.ListBoxRow):

    def __init__(self, entry: Entry):
        super().__init__(selectable=False, activatable=False)
        
        # Create container
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
        # Add label
        self._label = Gtk.Label(entry.shortcut.app_name)
        box.pack_start(self._label, False, False, 0)

        # Add switch
        self._switch = Gtk.Switch()
        self._switch.set_active(entry.enabled)
        self._switch.connect("state-set", lambda _, enable: entry.set_enabled(enable))
        entry.enabled_event.subscribe(self._switch.set_active)
        box.pack_end(self._switch, False, False, 0)

        # Add 'Missing images' label
        self._status_label = Gtk.Label(label='Missing images')
        self.set_status('Missing images' if entry.images.any_missing() else '')
        entry.images.missing_event.subscribe(lambda e: self.set_status('Missing images' if e else ''))
        entry.images.status_event.subscribe(self.set_status)
        box.pack_end(self._status_label, False, False, 0)

        # Add container to row
        self.add(box)
        self.show_all()
    
    def set_status(self, status):
        self._status_label.set_label(status)
        utils.flush_gtk()