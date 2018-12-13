import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk
import cairo
from gi.repository import GdkPixbuf
import os
import webbrowser

class aboutMenu(gtk.Window):

    def exitMenu(self, event,l):
        self.destroy()

    def __init__(self, conf_file):
        gtk.Window.__init__(self )
        self.set_title("AESIR Screenshoot Tools")
        self.set_position(gtk.WindowPosition.CENTER)
        self.set_size_request(350,200)

        self.logo_area = gtk.DrawingArea()


        self.set_resizable(False)
        self.logo_area.connect("draw", self.area_draw)


        self.anan = gtk.Fixed()


        label= gtk.Label()
        label2 = gtk.Label()

        label2.set_markup('Development: <a href="https://github.com/muratdemirtas/aesir">Github Page</a>')


        label.set_markup('Support: <a href="http://www.embedded-tips.com">embedded-tips.com</a>')
        label.connect('activate-link', self.hashtag_handler)


        self.quit_button = gtk.Button("Quit")
        self.quit_button.set_size_request(50,30)
        self.quit_button.show()

        self.quit_button.connect("button-press-event", self.exitMenu )

        self.window_height = 350
        self.window_weight = 300


        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            os.getcwd() + "/" + conf_file["icons"]["folder"] + "/" + conf_file["icons"]["icons"]["aboutlogo"], 100,100)

        self.logo_area.set_size_request(350,180)


        self.anan.put(self.logo_area, 0, 0)
        self.anan.put(self.quit_button, 300, 150)
        self.anan.put(label,10,170)
        self.anan.put(label2,10,150)
        self.add(self.anan)





        self.show_all()

    def hashtag_handler(self,label, uri):
        print(uri)
        webbrowser.open_new_tab(uri)

        return True

    def area_draw(self, widget, cr):


        cr.set_line_width(1)
        cr.set_source_rgb(255 , 255 , 255)
        cr.rectangle(0, 0, self.window_height, self.window_weight-150)
        cr.fill()


        cr.set_source_rgb(192 , 192 , 192)
        cr.rectangle(200, 200, self.window_height , 250)
        #cr.fill()

        cr.set_source_rgb(0 , 0, 0)
        cr.select_font_face("Times New Roman", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(15)

        cr.move_to(10, 30)
        cr.show_text("AESIR Screenshot Tools")

        cr.select_font_face("Times New Roman", cairo.FONT_SLANT_ITALIC,
                            cairo.FONT_WEIGHT_BOLD)

        cr.set_source_rgb(0 , 0, 250)
        cr.move_to(10, 60)
        cr.show_text("Open Source Screen Capture Tool")


        cr.set_font_size(15)
        cr.set_source_rgb(0 , 0, 250)
        cr.move_to(10, 140)
        cr.show_text("V1.0.0 Alpha Nightly")

        gdk.cairo_set_source_pixbuf(cr, self.pixbuf, 240, 10)

        cr.paint()

