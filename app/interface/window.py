import sys, logging
from pathlib import Path
from gi.repository import Gtk, Gdk

from .main_view import MainView
from ..version import VERSION_STR


class Window(Gtk.Window):
    def __init__(self):

        # Setup window
        super().__init__(title=f'SteamJar v{VERSION_STR}')
        self.connect("destroy", self.on_close)
        self.set_default_size(500, 650)

        # Setup style
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Load css
        path = Path(sys.argv[0]).parent / 'assets' / 'style.css'
        if path.exists():
            with path.open('rb') as file:
                provider.load_from_data(file.read())
        else:
            logging.warn('Failed to load GUI style file')

        # Add main view
        self.view = MainView()
        self.add(self.view)

    def on_close(self, _):
        Gtk.main_quit()