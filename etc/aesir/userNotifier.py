#using gi for notify library
import gi
import subprocess
import sys
from subprocess import call
import os


NOTIFY_NAME = 'Notify'  #name of the notifier library
NOTIFY_VERSION = '0.7'  #version of the current notify library

#set required version of notify
gi.require_version(NOTIFY_NAME, NOTIFY_VERSION)

#from gi repository get Notify library
from gi.repository import Notify as notify

#used for operations like try-catch
import traceback

#import Image Library for multi screenshot
from PIL import Image

#class for notifier types used in AESIR
class NOTIFIER_TYPES:
    SOFTWARE_UPDATE = 1    # software update notifer
    SCREENSHOT_SAVE = 2    # screenshot saved notifier
    CLIPBOARD_COPY  = 3    # clipboard copy notifier





'''
@summary Data structure used in notifier object
'''
class userNotifierData(object):
    def __init__(self, title, type, body, data, actions, argument):
        self.title = title  #title for notifier object
        self.type = type    #type of notifier object
        self.data = data    #message of notifier object
        self.body = body    #body header of notifier object
        self.actionlist = actions #callback functions of notifier object
        self.argument = argument #extra arguments from caller object

'''
@summary User notifier callback system using Notifier From gi
'''
class userNotifier():


    def openImage(self, path):
        imageViewerFromCommandLine = {'linux':'eog',
                                      'win32':'explorer',
                                      'darwin':'open'}[sys.platform]
        subprocess.run([imageViewerFromCommandLine, path])

    #get arguments from caller object and fill them
    def __init__(self, notifierData):

        #get type
        self.type = notifierData.type

        #get argument
        self.argument = notifierData.argument

        #try to run notifier app
        try:

            #init notifier subsytem with title.
            notify.init(notifierData.title)

            #is that software updater notifier?
            if(self.type == NOTIFIER_TYPES.SOFTWARE_UPDATE):

                notifierData.body = notifierData.body

            #is that screenshot save notifier?
            if(self.type == NOTIFIER_TYPES.SCREENSHOT_SAVE):
                notifierData.body = notifierData.body + notifierData.argument

            #is that clipboard copy notifier?
            if(self.type == NOTIFIER_TYPES.CLIPBOARD_COPY):
                notifierData.body = notifierData.body

            #if we are here, we call notifier system
            self.notification = notify.Notification.new(notifierData.title, notifierData.body)

            #if argument have action
            if notifierData.actionlist != None:

                self.callback_name = notifierData.actionlist
                self.callback_data = notifierData.data
                #declare callback functions
                self.notification.add_action\
                (
                    self.callback_name, #callback signal name
                    self.callback_data, #action title
                    self.notifier_callback_func, #callback function
                    None
                )

            #finally, show the notifier
            self.notification.show()

        #if error occurred, print
        except Exception:
            traceback.print_exc()

    '''
    @summary Notifer subsytem callback function 
    '''
    def notifier_callback_func(self, notification, signal_text, e):

        #if Aesir Software Updater Notifier
        if self.type == NOTIFIER_TYPES.SOFTWARE_UPDATE:
            file = os.path.dirname(os.path.realpath(__file__)) + "/preupdater.sh"
            call(["pkexec","bash", file])
        #if Aesir Clipboard copy Notifier
        elif self.type == NOTIFIER_TYPES.CLIPBOARD_COPY:
            print("Upload ")

        #if Aesir Screenshot save Notifier
        elif self.type == NOTIFIER_TYPES.SCREENSHOT_SAVE:
            self.openImage(self.argument)
