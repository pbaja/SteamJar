from gi.repository import Gtk

def suff(count):
    return 's' if count > 1 else ''

def flush_gtk():
    # This is bad. We should use signals and threading instead. Someday ;]
    while Gtk.events_pending():
        Gtk.main_iteration()