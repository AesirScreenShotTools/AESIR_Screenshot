import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
import os
from gi.repository import Gtk as gtk , GObject
from gi.repository import Gdk as gdk
import threading
from softwareUpdater import softwareUpdater, applicationQueue
from configurationReader import confReader as confmanager
from softwareUpdater import applicationQueue, thread_queue
from userNotifier import userNotifierData as notifydata, userNotifier, NOTIFIER_TYPES
from aboutMenu import aboutMenu
from options import optionMenu as OptionDialog
import parameters as PARAMS
from threading import Thread
from aesirWindowManager import AesirWindowManager
from activeWindow import ActiveWindow as selectionWindow


import urllib
import json

from aesirWindowManager import AesirWindowManager as AesirWinManager

try:
    #gi repository üzerinden appindicator olarak cagir
    from gi.repository import AppIndicator3 as indicator
    HAS_INDICATOR = True
except:
    #değilse hata ver
    HAS_INDICATOR = False

#used for open web pages directly
import webbrowser

#common configuration file instance
from parameters import CONF_FILE_INSTANCE, ICON_PATH

from common import returnIconPath

class MENUITEMS:
    ITEM_NAME   = 0
    ITEM_FUNC   = 1
    ITEM_SIGNAL = 2
    ITEM_SPLIT  = "="


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
            print("sd")

        if self.versionCompare(CONF_FILE_INSTANCE["version"]) < 0:
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


    def restoreSubWindowsItem(self):
        WindowList = self.WindowManager.getCurrentViewableOpenedWins()

        if len(WindowList) == self.old_windows_size:
            return

        counter = 0
        for old_items in self.windowsSubSystemMenu.get_children():
            GObject.idle_add(self.windowsSubSystemMenu.remove, old_items) # check here if you want to remove this child
            old_items = None

        for WindowName in WindowList:

            item_name = "[" + str(counter) + "] " + WindowName

            if len(WindowName) < 20:
                item_name = "[" + str(counter) + "] " + WindowName
            else:
                item_name = "[" + str(counter) + "] " + WindowName[:20]
            item = gtk.MenuItem(item_name)
            item.connect("activate", self.clickSubWindowsCB, item)
            item.show()
            GObject.idle_add(self.windowsSubSystemMenu.add,item)
            counter = counter + 1
            self.old_windows_size = counter

    def show_seconds(self):
        self.old_windows_size = 0
        while True:
            time.sleep(1)
            if self.is_windows_button_clicked:
                self.timeout_counter = self.timeout_counter + 1
                if self.timeout_counter > 2:
                    self.is_windows_button_clicked = False
                    self.timeout_counter = 0

            else:
               self.restoreSubWindowsItem()

    '''
    @brief aesirIndicatorApp indikatör kütüphanesinin constructoru
    '''
    def __init__(self ):

        #aesir pencere yöneticisi sınıfı olusturuluyor
        self.WindowManager = AesirWindowManager()
        #kullanıcının windows menusune tıkladığını algılamak icin kullanıldı.
        self.is_windows_button_clicked = False
        #aesir uygulamasının mevcut versiyonunu al
        self.current_version = 0#CONF_FILE_INSTANCE["version"]
        #dummy timeout counteri worker thread icinde kullanılıyor
        self.timeout_counter = False
        self.indicator_app_icon = returnIconPath("indicator")
        self.indicator_update_icon = returnIconPath("indicatorwarning")
        self.systemtrayicon = indicator.Indicator.new("aesir",
                                                      self.indicator_app_icon,
                                                      indicator.IndicatorCategory.SYSTEM_SERVICES)

        self.systemtrayicon.set_status(indicator.IndicatorStatus.ACTIVE)
        self.systemtrayicon.set_attention_icon(self.indicator_update_icon)
        self.updateCheck = softwareUpdater(CONF_FILE_INSTANCE["update_link"])
        self.updateCheck.setDaemon(True)
        self.updateCheck.start()
        self.updateCheck.join()
        threading.Timer(PARAMS.SOFTWARE_THREAD_CHECK_TIMEOUT, self.checkSoftwareUpdateResult).start()
        self.indicator_menu = gtk.Menu()
        self.activatorItem = gtk.MenuItem( )
        self.activatorItem.connect("activate", self.OnMiddleClicked)
        self.systemtrayicon.set_secondary_activate_target( self.activatorItem)
        self.indicator_menu.append(self.activatorItem)
        self.indicator_menu_items = []

        for menuItemConfig in CONF_FILE_INSTANCE["IndicatorAPPMenuItems"]:
            item = menuItemConfig.split(MENUITEMS.ITEM_SPLIT)
            itemCallbackName = item[MENUITEMS.ITEM_NAME]
            itemCallbackFunc = item[MENUITEMS.ITEM_FUNC]
            itemCallbackSignal = item[MENUITEMS.ITEM_SIGNAL]
            itemCallbackFuncMethod = getattr(self, itemCallbackFunc)
            menuitemInstance = gtk.MenuItem(itemCallbackName)
            menuitemInstance.connect(itemCallbackSignal, itemCallbackFuncMethod)
            self.indicator_menu.append(menuitemInstance)
            self.indicator_menu_items.append(menuitemInstance)

        self.windowsSubSystemMenu = gtk.Menu()
        self.handler_id_list = []
        self.indicator_menu_items[1].set_submenu(self.windowsSubSystemMenu)
        self.indicator_menu.show_all()
        self.systemtrayicon.set_menu(self.indicator_menu)

        self.workerThread = Thread(target=self.show_seconds)
        self.workerThread.setDaemon(True)
        self.workerThread.start()

    def clickCheckUpdatesCB(self, widget):
        from subprocess import Popen
        import os
        print(os.path.dirname(os.path.realpath(__file__)))
        file = os.path.dirname(os.path.realpath(__file__)) + "/scripts/preupdater.sh"
        file2 = os.path.dirname(os.path.realpath(__file__)) + "/scripts/updater.sh"
        Popen(["/bin/bash", file])
        Popen(["pkexec","/bin/bash", file2])

        print("Soft")
        pass

    def clickFindWindowsCB(self, widget):
        self.is_windows_button_clicked = True

    def clickSubWindowsCB(self, item, widget):

        window_name = item.get_label().split("] ")[1]

        self.WindowManager.getScreenshotOfWindow(window_name)


        return True

    def OnMiddleClicked(notification, signal_text):
        selection_widget = selectionWindow()

    def clickTakeSSCB(self, widget):
        self.selection_widget = selectionWindow()

    def clickOptionsCB(self, widget):
        OptionDialog()
        return True

    def clickAboutCB(self, widget):
        aboutMenuInstance = aboutMenu(self.confFile)

    def clickHelpCB(self, widget):
        webbrowser.open(CONF_FILE_INSTANCE["product_link"])
        return

    def clickExitCB(self, widget):
        gtk.main_quit()
