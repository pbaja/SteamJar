from gi.repository import Gtk

from .entry_row import EntryRow


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

        # Add scrollable list box
        self._entries_listbox = Gtk.ListBox()
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self._entries_listbox)
        self.pack_start(scrolled_window, True, True, 10)

    def clear_entries(self):
        for child in self._entries_listbox.get_children():
            self._entries_listbox.remove(child)

    def add_entries(self, entries):
        for entry in entries:
            row = EntryRow(entry)
            self._entries_listbox.add(row)
        self._entries_listbox.show_all()

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
