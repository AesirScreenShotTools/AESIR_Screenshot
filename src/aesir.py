
#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Wnck', '3.0')
from gi.repository import Gtk, Gdk
import sys






































import sys
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Wnck', '3.0')
from gi.repository import Gdk as gdk
from gi.repository import Wnck

from gi.repository import Gtk as gtk
from indicatorApp import AppIndicator
from configurationReader import confReader as confmanager
from activeWindow import ActiveWindow as selectionWindow


class AesirStartArguments:
    START_FROM_HOTKEY    = 1
    START_FROM_SYSTEMD   = 2

class AesirHotkeyFunctions:
    AESIR_SCREENSHOT         = 1
    AESIR_MULTI_SCREENSHOT   = 2
from Xlib.display import Display as display

from aesirwebrequest import GoogleSearchUploader

def main():

    aesir_system_mode = AesirStartArguments.START_FROM_SYSTEMD

    print(sys.argv)

    if(len(sys.argv) > 1):
        aesir_system_mode = int(sys.argv[1])

    if aesir_system_mode == AesirStartArguments.START_FROM_SYSTEMD:

        confmanager("/home/firat/Desktop/AESIR_Screenshot/src/conf.json")
        indicator = AppIndicator()
        gtk.main()

    elif aesir_system_mode == AesirStartArguments.START_FROM_HOTKEY:
        selection_widget = selectionWindow()
        gtk.main()

    print("cikis")

if __name__ == "__main__":
    main()