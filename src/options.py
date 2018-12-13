import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk
from os.path import abspath, dirname, join
from math import pi
import sys
import os
import cairo
from Xlib import X, display ,Xutil
from math import ceil
import cairo
from gi.repository import GdkPixbuf

class optionMenu(gtk.Window):

    # Callback function. Since the signal is notify::active
    # we need the argument 'active'
    def activate_cb(self, button, active):
        # if the button (i.e. the switch) is active, set the title
        # of the window to "Switch Example"
        if button.get_active():
            self.set_title("Switch Example")
        # else, set it to "" (empty string)
        else:
            self.set_title("")



    def comboboxformatChanged(self, widget):
        print("anan")


    def __init__(self):
        gtk.Window.__init__(self )


        self.set_resizable(False)

        self.set_title("Options for AESIR Screenshot Tools! ")
        self.set_size_request(400,200)
        self.set_border_width(3)

        self.notebook = gtk.Notebook()
        self.add(self.notebook)

        self.page1 = gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(gtk.Label('Default Page!'))
        self.notebook.append_page(self.page1, gtk.Label('General'))

        self.page2 = gtk.Box()
        self.page2.set_border_width(10)

        self.notebook.append_page(
            self.page2,
                gtk.Label("Formats")

        )

        self.gtk_gridview = gtk.Grid()
        self.gtk_gridview.set_row_spacing(10)
        self.gtk_gridview.set_column_spacing(20)


        self.combobox_formats_list = gtk.ListStore(int,str)
        self.combobox_formats_list.append([1,"JPG"])
        self.combobox_formats_list.append([2,"PNG"])

        self.combobox_formats_list = gtk.ListStore(int,str)
        self.combobox_formats_list.append([1,"JPG"])
        self.combobox_formats_list.append([2,"PNG"])


        combo=gtk.ComboBox.new_with_model_and_entry( self.combobox_formats_list )
        combo.set_entry_text_column(1)
        combo.set_active(0)

        combo.connect('changed', self.comboboxformatChanged)


        self.label_screenshot_save = gtk.Label("Save screenshot as...")


        self.gtk_gridview.attach(self.label_screenshot_save, 0, 0, 1, 1)
        self.gtk_gridview.attach(combo , 1, 0 , 1, 1)


        self.label_automatic_updates = gtk.CheckButton("Check Updates")
        self.label_shortcut_screenshot = gtk.CheckButton("Take a Screenshot")
        self.label_fast_screenshot = gtk.CheckButton("Take a Fast Screenshot")
        self.label_shortcut_full_screenshot = gtk.CheckButton("Take all of the Screen")

        self.page2.add(self.gtk_gridview)


        # a grid to allocate the widgets
        self.gridview = gtk.Grid()
        self.gridview.set_row_spacing(10)
        self.gridview.set_column_spacing(20)





        # a switch
        self.switch_automatic_updates = gtk.Switch()
        # turned on by default
        self.switch_automatic_updates.set_active(True)


        # connect the signal notify::active emitted by the switch
        # to the callback function activate_cb

        #    LEFT                   TOP
        #    LEFT                   TOP
        self.gridview.attach(self.label_automatic_updates, 0, 0, 1, 1)
        self.gridview.attach(self.switch_automatic_updates, 1, 0 , 1, 1)


        self.text_shortcut_screenshot = gtk.Entry()
        self.text_label_fast_screenshot = gtk.Entry()
        self.text_label_shortcut_full_screenshot = gtk.Entry()

        self.text_shortcut_screenshot.connect("preedit-changed+", self.openKeyDetectiondialog)

        self.text_shortcut_screenshot.set_text("Ctrl + Insert")
        self.text_label_fast_screenshot.set_text("Ctrl + Printscreen")
        self.text_label_shortcut_full_screenshot.set_text("Ctrl + Alt")

        self.gridview.attach(self.label_shortcut_screenshot, 0, 1, 1, 1)
        self.gridview.attach(self.text_shortcut_screenshot, 1, 1, 1, 1)




        self.gridview.attach(self.label_fast_screenshot, 0, 2, 1, 1)
        self.gridview.attach(self.text_label_fast_screenshot, 1, 2, 1, 1)


        self.gridview.attach(self.label_shortcut_full_screenshot, 0, 3, 1, 1)
        self.gridview.attach(self.text_label_shortcut_full_screenshot, 1, 3, 1, 1)


        # add the grid to the window
       # self.add(self.gridview)

        self.shortcutTabs = gtk.Box()
        self.shortcutTabs.add(self.gridview)

        self.notebook.append_page(self.shortcutTabs, gtk.Label('Shortcuts'))

        self.set_position(gtk.WindowPosition.CENTER)
        self.show_all()

    def openKeyDetectiondialog(self):
        print("ha")