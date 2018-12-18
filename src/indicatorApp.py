import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
import os
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
import threading
from softwareUpdater import softwareUpdater as updater, applicationQueue
from configurationReader import confReader as confmanager
from softwareUpdater import applicationQueue, thread_queue
from userNotifier import userNotifierData as notifydata, userNotifier, NOTIFIER_TYPES
from aboutMenu import aboutMenu
from options import optionMenu as OptionDialog
import parameters as PARAMS

from windowManager import AesirWindowManager
from activeWindow import ActiveWindow as selectionWindow


try:
    #gi repository üzerinden appindicator olarak cagir
    from gi.repository import AppIndicator3 as indicator
    HAS_INDICATOR = True
except:
    #değilse hata ver
    HAS_INDICATOR = False






import time



class AppIndicator():


    def versionCompare(self, received_version):

        if float(self.current_version) >= float(received_version):
            return -1
        else:
            return 1

    def checkSoftwareUpdateResult(self):

        if thread_queue.qsize() < 1:
            return

        while not thread_queue.empty():
            self.result = thread_queue.get()

        try:
            received_json = self.configurations.parseJson(self.result.data)
        except:
            print(self.result.data)
            print("sd")



        if self.versionCompare(received_json["current_version"]) < 0:
            self.systemtrayicon.set_status(indicator.IndicatorStatus.ACTIVE)

        else:

            self.systemtrayicon.set_status(indicator.IndicatorStatus.ACTIVE)
            self.notifyinstance = userNotifier(self.notifyData)

    def detectWindowsMenu(self, window):
        print("Windows")

    def initSoftwareUpdateNotifierData(self, jsonInstance):

        if(jsonInstance == None):
            return

        try:

            print(jsonInstance)
            self.notifyData = notifydata(jsonInstance['SoftwareUpdater']["NotifierTitle"],
                                         NOTIFIER_TYPES.SOFTWARE_UPDATE,
                                         jsonInstance['SoftwareUpdater']["NotifierBody"],
                                         jsonInstance['SoftwareUpdater']["NotifierData"],
                                         jsonInstance['SoftwareUpdater']["NotifierActions"],None)
        except :
            print(Exception)



    def __init__(self ):

        self.configurations = confmanager("/home/firat/Desktop/AESIR_Screenshot/src/conf.json")
        self.initSoftwareUpdateNotifierData(self.configurations.getConfigFileContext())
        self.confFile = self.configurations.getConfigFileContext()

        self.WindowManager = AesirWindowManager()

        self.active_screen_list  = []




        self.current_version = self.configurations.getJsonValue("version")

        thread = updater(self.configurations.getJsonValue("update_link"))
        thread.start()
        thread.join()

        threading.Timer(PARAMS.SOFTWARE_THREAD_CHECK_TIMEOUT, self.checkSoftwareUpdateResult).start()

        icon_image = os.path.dirname(__file__) + "/icons" + "/systemtray.png"
        icon_image1 = os.path.dirname(__file__) + "/icons" + "/systemtray_update.png"

        print(icon_image)
        if not os.path.isfile(icon_image):
            print("hata")
            icon_image = "/usr/share/unity/icons/panel-shadow.png"

        else:
            print("basa")


        self.systemtrayicon = indicator.Indicator.new("Weather",
                                           icon_image,
                                              indicator.IndicatorCategory.SYSTEM_SERVICES)

        self.systemtrayicon.set_status(indicator.IndicatorStatus.ACTIVE)

        self.systemtrayicon.set_attention_icon(icon_image1)


        self.menu = gtk.Menu()

        item = gtk.MenuItem( )
        item.connect("activate", self.OnMiddleClicked)

        self.systemtrayicon.set_secondary_activate_target( item)

        self.menu.append(item)





        self.Screenshot =  gtk.MenuItem("Take a screenshot")






        self.Options    =  gtk.MenuItem("Options")
        self.About      =  gtk.MenuItem("About...")
        self.Help       =  gtk.MenuItem("Help")
        self.Close      =  gtk.ImageMenuItem("Exit")
        self.Updates    =  gtk.CheckMenuItem("Check Updates")


        self.Screenshot.connect("activate", self.takeScreenshot)




        self.Options.connect("activate", self.openOptionsMenu)

        self.About.connect("activate", self.openAboutMenu)

        self.Help.connect("activate", self.openHelpMenu)

        self.Close.connect("activate", self.openCloseMenu)

        self.menu.append(self.Screenshot)

        self.menu.append(self.Options)
        self.menu.append(self.About)
        self.menu.append(self.Help)
        self.menu.append(self.Updates)
        self.menu.append(self.Close)

        self.menu.show_all()


        self.systemtrayicon.set_menu(self.menu)

    def OnMiddleClicked(notification, signal_text):
        selection_widget = selectionWindow()

    def windowsSubMenuClicked(self, widget):
        pass

    def takeScreenshot(self, widget):


        self.selection_widget = selectionWindow()

    def openOptionsMenu(self, widget):
        OptionDialog()
        return True

    def openAboutMenu(self, widget):
        aboutMenuInstance = aboutMenu(self.confFile)

    def openHelpMenu(self, widget):

        print()

    def openCloseMenu(self, widget):
        gtk.main_quit()


