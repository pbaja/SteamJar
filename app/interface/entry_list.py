from gi.repository import Gtk

from ..games.game_store import GameStore
from .entry_row import EntryRow

class EntryList(Gtk.ScrolledWindow):

    def __init__(self):
        super().__init__()

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(box)

        self.stores = {}
        for store in GameStore:
            
            # Add title
            store_name = store.name.replace('_', ' ').title()
            label = Gtk.Label(label=store_name)
            label.get_style_context().add_class('store-title')
            box.pack_start(label, False, False, 0)

            # Add 'No games' information
            status_label = Gtk.Label(label='No games')
            box.pack_start(status_label, False, False, 5)

            # Add container for entries
            container_box = Gtk.ListBox()
            box.pack_start(container_box, False, False, 5)

            # Save
            self.stores[store] = (container_box, status_label)

    def clear_entries(self):
        for container_box, status_label in self.stores.values():
            status_label.show()
            for child in container_box.get_children():
                container_box.remove(child)

    def add_entries(self, store, entries):
        container_box, status_label = self.stores[store]

        for entry in entries:
            row = EntryRow(entry)
            container_box.add(row)
            
        container_box.show_all()
        status_label.hide()