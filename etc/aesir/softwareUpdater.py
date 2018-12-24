#threading class for thread system
import threading

#urllib for request data from web
import urllib.request

#syslogger class
from syslogger import Syslogger

#static parameters
import parameters as PARAMS

#phyton queue library
import queue


class APP_QUEUE_TYPES:
    SOFTWARE_UPDATE_AVAILABLE = 1
    SOFTWARE_UPDATE_NOT_AVAILABLE = 2

class applicationQueue(object):
    def __init__(self, type, data):
        self.type = type
        self.data = data


thread_queue = queue.Queue()






class softwareUpdater(threading.Thread):


    def __init__(self , url):

        self.logger = Syslogger()

        threading.Thread.__init__(self)
        self.logger.writesyslogFile("thread for software updater started.")
        self.update_url = url

    """
    @summary check new software updates from github link
    @:param self: 
    """
    def checkUpdates(self):
        return self.readRemoteJsonData(self.update_url)

    """
    @:param self:
    """
    def readRemoteJsonData(self, url):
        try:
            response = urllib.request.urlopen(url, timeout = PARAMS.SOFTWARE_UPDATER_TIMEOUT)
            data = response.read()
            self.thread_message = applicationQueue(APP_QUEUE_TYPES.SOFTWARE_UPDATE_AVAILABLE, data)

            thread_queue.put(self.thread_message)

            return True, data.decode('utf-8')

        except urllib.request.URLError as urlexception:
            return False, urlexception

    """
    @:param self:
    """
    def run(self):
        ret, value = self.checkUpdates()
        if ret:
            self.logger.writesyslogFile("remote update file checked.")
        else:
            self.logger.writesyslogFile("error occured while accessing repo" + str(value))

        self.logger.writesyslogFile("thread for software updater finished.")
