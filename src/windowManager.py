import gi
from gi.repository import Wnck
from gi.repository import Gdk as Gdk

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Wnck', '3.0')


class AesirWindowManager:
    def __init__(self):
        self.default_screen = None
        self.number_of_screens = None
        self.active_windows_list = None
        self.getcurrentactivewins()

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
