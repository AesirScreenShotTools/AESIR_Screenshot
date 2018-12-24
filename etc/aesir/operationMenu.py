import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk
import sys
import requests
import webbrowser
import platform
import subprocess
from PIL import Image
import base64


from common import aesirPathManager


from userNotifier import userNotifierData as notifydata, userNotifier, NOTIFIER_TYPES

from gi.repository import GdkPixbuf

from common import returnIconPath

from parameters import CONF_FILE_INSTANCE


class operationMenuDialog():

    def exitButtonPressed(self, widget):
        self.tryExit()

    def exitFromOpMenu(self):
        self.window.destroy()

    '''
    @summary copy button press callback
    '''

    def copyButtonPressed(self, widget):
        self.s.pulseProgressBar()
        # self.saveClipBoard()

    '''
    @summary save button press callback
    '''

    def saveButton_click_callback(self, widget):

        self.saveScreenShot()

    def getRectanglePixbuf(self, pixbuf):
        self.current_pixbuf = pixbuf

    def tryExit(self):
        self.activeWindow.restoreMousePointer()
        self.activeWindow.clearScreen()
        self.activeWindow.exitFromActiveWindow()

    def saveClipBoard(self):

        self.notifyData = notifydata(CONF_FILE_INSTANCE['ClipboardCopy']["NotifierTitle"],
                                     NOTIFIER_TYPES.CLIPBOARD_COPY,
                                     CONF_FILE_INSTANCE['ClipboardCopy']["NotifierBody"],
                                     CONF_FILE_INSTANCE['ClipboardCopy']["NotifierData"],
                                     CONF_FILE_INSTANCE['ClipboardCopy']["NotifierActions"],
                                     None)

        self.notifyinstance = userNotifier(self.notifyData)

        self.tryExit()

    def saveScreenShot(self):

        selected_pixbuf = self.activeWindow.getSelectedAreaPixbuf( )


        import time
        current_time = time.strftime("_%d_%m_%Y_%H:%M")


        file_path = self.pathManager.returnImageSavePath() + "screenshot" + current_time + ".png"
        if file_path is not None:
            selected_pixbuf.savev(file_path, "png", (), ())

        else:
            selected_pixbuf.savev("screenshot.png", "png", (), ())

        self.notifyData = notifydata(CONF_FILE_INSTANCE['ScrenshotSave']["NotifierTitle"],
                                     NOTIFIER_TYPES.SCREENSHOT_SAVE,
                                     CONF_FILE_INSTANCE['ScrenshotSave']["NotifierBody"],
                                     CONF_FILE_INSTANCE['ScrenshotSave']["NotifierData"],
                                     CONF_FILE_INSTANCE['ScrenshotSave']["NotifierActions"],
                                     str(file_path))

        self.notifyinstance = userNotifier(self.notifyData)
        self.tryExit()

    def opMenu_on_key_release_event(self, widget, event, data=None):

        # if escape key pressed
        if event.keyval == gdk.KEY_Escape:
            # self.tryExit() #try exit
            self.window.destroy()
            return True

        # check if ctrl button pressed
        ctrl = (event.state & gdk.ModifierType.CONTROL_MASK)

        # check which button pressed with ctrl key

        # if ctrl-s or ctrl-S then save
        if ctrl and event.keyval == gdk.KEY_s or event.keyval == gdk.KEY_S:
            self.saveScreenShot()  # save screenshot and exit

        # if ctrl-c or ctrl-C then copy clipboard
        elif ctrl and event.keyval == gdk.KEY_c or event.keyval == gdk.KEY_C:
            self.saveClipBoard()  # save clipboard

        # if ctrl-c or ctrl-C then copy clipboard
        elif ctrl and event.keyval == gdk.KEY_d or event.keyval == gdk.KEY_d:
            self.activeWindow.getSelectedAreaPixbuf()
            img = Image.open("screenshot.png")
            img.show()
            self.tryExit()

    def changePositionOpMenu(self, new_x, new_y):

        self.window.move(new_x - 120, new_y - 110)
        self.showOpMenu()

    def hideOpMenu(self):
        self.window.set_visible(False)

    def showOpMenu(self):
        self.window.show_all()
        self.window.set_visible(True)

    def pencilButtonPressed(self, widget):
        self.activeWindow.setActionFromOpMenu(8)
        return

    def appMoveWindow(self, new_pos_x, new_pos_y):
        print(new_pos_x, new_pos_y)
        self.window.move(new_pos_x, new_pos_y)

    def draw_rectangle_button_callback(self, widget):
        self.activeWindow.setActionFromOpMenu(6, 0, 0)

    # upload button click callback function
    def printerButton_click_callback(self, widget):
        print("printer")
        print(platform.system())
        # Windows / Linux
        if platform.system() == "Windows":
            print("windows systems")
        if platform.system() == "Linux":
            print("lin")
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, 'frame.jpg'])

    def my_callback(self, monitor):
        # Your callback function
        print(monitor.bytes_read)

    # upload button click callback function
    def uploadButton_click_callback(self, widget):
        url = 'https://imgyukle.com/api/1/upload/?key=407289b6f603c950af54fbc79311b9b0'

        params = {'format': 'json'}

        with open('screenshot.png', 'rb') as fd:
            b64data = base64.b64encode(fd.read())

        files2 = {'source': ('screenshot.png', b64data)}
        r = requests.post(url, data=files2, params=params)

        print(r.reason)
        print("upload")

        # upload button click callback function

    def googleSearchButton_click_callback(self, widget):
        print("search")
        filePath = '/tmp/tempaesirgooglesearch.png'

        searchUrl = 'http://www.google.com.tr/searchbyimage/upload'
        self.activeWindow.getSelectedAreaPixbuf().savev(filePath, "png", (), ())
        multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}

        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers['Location']
        webbrowser.open(fetchUrl)
        gtk.main_quit()

    def hideWindowOpMenu(self):
        self.window.hide()

    def __init__(self, activeWindowInstance):

        self.activeWindow = activeWindowInstance

        self.pathManager = aesirPathManager()

        self.window = gtk.Window()
        container = gtk.Fixed()

        self.s = None

        self.drawingContainer = gtk.Fixed()

        self.current_pixbuf = None
        self.exit_button = gtk.Button()

        self.exit_button.set_tooltip_text("Exit")

        self.window.connect("key-release-event", self.opMenu_on_key_release_event)

        self.copy_button = gtk.Button()
        self.copy_button.set_tooltip_text("Copy")

        self.exit_button_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=returnIconPath("opclose"),
            width=15,
            height=15,
            preserve_aspect_ratio=True)

        self.exit_button.set_image(gtk.Image.new_from_pixbuf(self.exit_button_pixbuf))

        self.copy_button_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=returnIconPath("opcopy"),
            width=15,
            height=15,
            preserve_aspect_ratio=True)

        self.copy_button.set_image(gtk.Image.new_from_pixbuf(self.copy_button_pixbuf))

        self.save_button = gtk.Button()

        self.save_button_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=returnIconPath("opsave"),
            width=15,
            height=15,
            preserve_aspect_ratio=True)

        self.save_button.set_image(gtk.Image.new_from_pixbuf(self.save_button_pixbuf))

        self.save_button.set_tooltip_text("Save")

        self.printer_button = gtk.Button()

        self.printer_image_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=returnIconPath("opprinter"),
            width=15,
            height=15,
            preserve_aspect_ratio=True)

        self.printer_button.set_image(gtk.Image.new_from_pixbuf(self.printer_image_pixbuf))
        self.printer_button.set_tooltip_text("Printer")

        # create upload button icon and init sequence
        self.upload_image_button = gtk.Button()

        # create pixbuf from image with special size
        self.upload_image_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=returnIconPath("opcloud"),
            width=15,
            height=15,
            preserve_aspect_ratio=True)
        self.upload_image_button.set_tooltip_text("Upload to Cloud")

        self.upload_image_button.set_image(gtk.Image.new_from_pixbuf(self.upload_image_pixbuf))

        self.google_search_button = gtk.Button()

        self.google_search_image_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=returnIconPath("opgoogle"),
            width=15,
            height=15,
            preserve_aspect_ratio=True)

        self.google_search_button.set_image(gtk.Image.new_from_pixbuf(self.google_search_image_pixbuf))
        self.google_search_button.set_tooltip_text("Search on Google")

        self.draw_rectangle_button = gtk.Button()

        self.draw_rectangle_button_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=returnIconPath("oprectangle"),
            width=15,
            height=15,
            preserve_aspect_ratio=True)

        self.draw_rectangle_button.set_image(gtk.Image.new_from_pixbuf(self.draw_rectangle_button_pixbuf))

        self.select_text_button = gtk.Button()

        self.select_text_button_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=returnIconPath("optext"),
            width=15,
            height=15,
            preserve_aspect_ratio=True)

        self.select_text_button.set_image(gtk.Image.new_from_pixbuf(self.select_text_button_pixbuf))

        self.marker_button = gtk.Button()

        self.marker_button_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=returnIconPath("opmarker"),
            width=15,
            height=15,
            preserve_aspect_ratio=True)

        self.marker_button.set_image(gtk.Image.new_from_pixbuf(self.marker_button_pixbuf))

        self.pencil_button = gtk.Button()

        self.pencil_button_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=returnIconPath("oppencil"),
            width=15,
            height=15,
            preserve_aspect_ratio=True)

        self.pencil_button.set_image(gtk.Image.new_from_pixbuf(self.pencil_button_pixbuf))

        self.line_button = gtk.Button()
        self.line_button.set_tooltip_text("Draw a line")

        self.line_button_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=returnIconPath("opline"),
            width=15,
            height=15,
            preserve_aspect_ratio=True)

        self.line_button.set_image(gtk.Image.new_from_pixbuf(self.line_button_pixbuf))

        self.arrow_button = gtk.Button()
        self.arrow_button.set_tooltip_text("Draw a Arrow")

        self.arrow_button_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=returnIconPath("oparrow"),
            width=15,
            height=15,
            preserve_aspect_ratio=True)

        self.arrow_button.set_image(gtk.Image.new_from_pixbuf(self.arrow_button_pixbuf))

        self.draw_rectangle_button.connect("clicked", self.draw_rectangle_button_callback)
        self.printer_button.connect("clicked", self.printerButton_click_callback)
        self.upload_image_button.connect("clicked", self.uploadButton_click_callback)
        self.google_search_button.connect("clicked", self.googleSearchButton_click_callback)
        self.save_button.connect("clicked", self.saveButton_click_callback)
        self.pencil_button.connect("clicked", self.pencilButtonPressed)
        self.copy_button.connect("clicked", self.copyButtonPressed)
        self.exit_button.connect("clicked", self.exitButtonPressed)

        self.drawingContainer.put(self.arrow_button, 129, 0)
        self.drawingContainer.put(self.line_button, 129, 24)
        self.drawingContainer.put(self.select_text_button, 129, 48)
        self.drawingContainer.put(self.pencil_button, 129, 72)
        self.drawingContainer.put(self.marker_button, 129, 96)
        self.drawingContainer.put(self.draw_rectangle_button, 129, 120)

        self.drawingContainer.put(self.copy_button, 103, 120)
        self.drawingContainer.put(self.exit_button, 129, 120)
        self.drawingContainer.put(self.save_button, 77, 120)
        self.drawingContainer.put(self.printer_button, 52, 120)
        self.drawingContainer.put(self.upload_image_button, 0, 120)
        self.drawingContainer.put(self.google_search_button, 26, 120)

        self.window.add(self.drawingContainer)

        self.window.set_decorated(False)
        self.window.screen = self.window.get_screen()
        self.window.visual = self.window.screen.get_rgba_visual()
        if self.window.visual != None and self.window.screen.is_composited():
            print("yay")
            self.window.set_visual(self.window.visual)

        self.window.set_app_paintable(True)

        self.window.set_keep_above(True)
