import gi
from gi.repository import Wnck
from gi.repository import Gdk as Gdk

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Wnck', '3.0')



import Xlib
import Xlib.display
from Xlib import X
from PIL import Image
W,H = 200,200
display = Xlib.display.Display()






class AesirWindowManager:
    def __init__(self):
        self.default_screen = None
        self.number_of_screens = None
        self.active_windows_list = None
        self.getcurrentactivewins()

    def getWindowIDFromString(self, window_name):

        root = display.screen().root

        windowIDs = root.get_full_property(display.intern_atom('_NET_CLIENT_LIST'),
                                           Xlib.X.AnyPropertyType).value

        for windowID in windowIDs:
            window = display.create_resource_object('window', windowID)
            if window_name  in window.get_wm_name():


                window_width = window.get_geometry().width
                window_heigth = window.get_geometry().height
                raw = window.get_image(0, 0, window_width,window_heigth, X.ZPixmap, 0xffffffff)
                image = Image.frombytes("RGB", (window_width , window_heigth), raw.data, "raw", "BGRX")
                image.show()

    def getScreenshotOfWindow(self,window_name):

        if window_name is not None:
            print(window_name)
            self.getWindowIDFromString(window_name)

    def getCurrentViewableOpenedWins(self):
        root = display.screen().root
        windowNames = []

        windowIDs = root.get_full_property(display.intern_atom('_NET_CLIENT_LIST'),
                                           Xlib.X.AnyPropertyType).value
        for windowID in windowIDs:
            window = display.create_resource_object('window', windowID)

            name = window.get_wm_name() # Title

            try:
                data = name.decode()
            except AttributeError:

                prop = window.get_full_property(display.intern_atom('_NET_WM_PID'),
                                                Xlib.X.AnyPropertyType)

                windowNames.append(name)
                continue






        return windowNames

    def getnumberofscreens(self):

        self.default_screen = Gdk.Screen.get_default()

        if self.default_screen is not None:
            self.number_of_screens = Gdk.Screen.get_n_monitors(self.default_screen)

        return self.number_of_screens


    def getcurrentactivewins(self):
        self.active_windows_list = []
        wnck = Wnck.Screen.get_default()
        wnck.force_update()
        for windows in wnck.get_windows():
            self.active_windows_list.append(windows.get_name())
        return self.active_windows_list
