from cgitb import enable
from gi.repository import Gtk

from ..entry import Entry

class EntryRow(Gtk.ListBoxRow):

    def __init__(self, entry: Entry):
        super().__init__()
        
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
        self._missing_images_label = Gtk.Label(label='')
        self.set_missing_images_label(entry.images.any_missing())
        entry.images.missing_event.subscribe(self.set_missing_images_label)
        box.pack_end(self._missing_images_label, False, False, 0)

        # Add container to row
        self.add(box)
        self.show_all()
    
    def set_missing_images_label(self, enabled):
        self._missing_images_label.set_label('Missing images' if enabled else '')