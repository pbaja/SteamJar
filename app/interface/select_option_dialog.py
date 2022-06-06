from gi.repository import Gtk

class SelectOptionDialog(Gtk.Dialog):
    def __init__(self, parent, values=[], title="Select option", message="Select an option:", label_func=None):
        super().__init__(title=title, transient_for=parent, flags=Gtk.DialogFlags.MODAL)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Add label
        label = Gtk.Label(label=message)
        box.pack_start(label, False, False, 5)

        # Add user list
        self._listbox = Gtk.ListBox()
        for value in values:
            row = Gtk.ListBoxRow()
            row.__value = value

            msg = str(value)
            if label_func != None:
                msg = label_func(value)
            label = Gtk.Label(msg)

            row.add(label)
            self._listbox.add(row)
        box.pack_start(self._listbox, True, True, 5)

        self.get_content_area().add(box)

    def get_selected_value(self):
        return self._listbox.get_selected_row().__value