from re import S
from gi.repository import Gtk

from .entry_row import EntryRow
from .entry_list import EntryList
from ..games.game_store import GameStore

class MainView(Gtk.Box):

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        # Add buttons
        buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.pack_start(buttons_box, False, False, 5)

        self._reload_button = Gtk.Button(label="Refresh games")
        buttons_box.pack_start(self._reload_button, True, False, 5)

        self._enable_all_button = Gtk.Button(label="Enable all")
        buttons_box.pack_start(self._enable_all_button, True, False, 5)
        
        self._download_button = Gtk.Button(label="Download images")
        buttons_box.pack_start(self._download_button, True, False, 5)

        self._save_button = Gtk.Button(label="Save changes")
        buttons_box.pack_start(self._save_button, True, False, 5)

        # Add entry list
        self._entry_list = EntryList()
        self.pack_start(self._entry_list, True, True, 10)

    def clear_entries(self):
        self._entry_list.clear_entries()

    def add_entries(self, entries):
        stores = {}
        for e in entries:
            s = e.game.store if e.game is not None else GameStore.UNKNOWN
            entry_list = stores.setdefault(s, [])
            entry_list.append(e)
        for store, entry in stores.items():
            self._entry_list.add_entries(store, entry)

    def set_buttons_enabled(self, enabled):
        self._reload_button.set_sensitive(enabled)
        self._enable_all_button.set_sensitive(enabled)
        self._download_button.set_sensitive(enabled)
        self._save_button.set_sensitive(enabled)

    def on_reload_clicked(self, callback):
        self._reload_button.connect("clicked", lambda _: callback())

    def on_enable_all_clicked(self, callback):
        self._enable_all_button.connect("clicked", lambda _: callback())

    def on_download_clicked(self, callback):
        self._download_button.connect("clicked", lambda _: callback())

    def on_save_clicked(self, callback):
        self._save_button.connect("clicked", lambda _: callback())
