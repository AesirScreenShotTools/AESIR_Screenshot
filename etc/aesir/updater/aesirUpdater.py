import sys

from threading import Thread

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
import os
from gi.repository import Gtk, Gdk

import time
from gi.repository import GObject

from subprocess import Popen,call


class aesirGUIUpdaterNotifier(Gtk.Window):

    def workerThreadFunc(self):
        ## If file exists, delete it ##
        myfile = "/tmp/aesirupdater/log"
        if os.path.isfile(myfile):
            print("")
        else:    ## Show an error ##
            print("Error: %s file not found" % myfile)
            Gtk.main_quit()
        while 1:
            time.sleep(0.4)

            self.logFile = open("/tmp/aesirupdater/log", "r")
            context = self.logFile.readline()
            context = context[:len(context) -1 ]
            print(context)
            self.logFile.close()

            if context is not None:
                GObject.idle_add(self.image.set_from_file, str(context))
                GObject.idle_add(self.statusLabel.set_text, str(context))


    def __init__(self):
        super(aesirGUIUpdaterNotifier, self).__init__()
        self.image = Gtk.Image()
        self.image.set_from_file("prepare")
        self.set_icon_from_file("logo.png")
        self.set_title("Aesir Updater")
        self.statusLabel = Gtk.Label("Aesir-SS Updater")
        self.logFile = None
        vbox = Gtk.VBox()
        vbox.add(self.image)
        vbox.add(self.statusLabel)
        self.add(vbox)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(200, 200)
        self.set_keep_above(True)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()


        self.workerThread = Thread(target=self.workerThreadFunc)
        self.workerThread.setDaemon(True)
        self.workerThread.start()

        args = ['gnome-terminal', '--' , 'tail', '-f', '/tmp/aesirupdater/logfile.txt']
        call(args)
        Gtk.main()

if __name__ == "__main__":
    updater = aesirGUIUpdaterNotifier()
