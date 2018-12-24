from gi.repository import Gtk, GObject
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from gi.repository import Gdk as Gdk
import requests
import webbrowser
import gi
import base64
import threading
gi.require_version('Gtk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Wnck', '3.0')

class progressBarWidget(Gtk.Window):
    def __init__(self, title):
        Gtk.Window.__init__(self, title=title)

    def showProgressDialog(self):
        self.show_all()

class aesirProgressBar(Gtk.ProgressBar):
    def __init__(self, data_byte):
        Gtk.ProgressBar.__init__(self)
        self.max_size = data_byte

    def progress_timeout(self, widget):
        self.props.text = ''
        self.props.show_text = True
        widget.progress_bar.set_text("Error!")
        return True

    def getBytesLengthofFile(self):
            return self.max_size

    def setRemainingBytesofFile(self, new_value):
        self.remaining_size = self.max_size - new_value
        self.changeValueofProgressBar(self.scaleFractionValue(self.remaining_size))

    def getRemainingBytesofFile(self):
        return self.remaining_size

    def scaleFractionValue(self, value):
        return 1 * (self.remaining_size / self.max_size)

    def changeValueofProgressBar(self, new_value):
        self.set_fraction(1 - new_value)

    def pulseProgressBar(self):
        self.pulse()


class GoogleSearchUploader:
    def __init__(self, url, filepath, is_widget):
        self.url = url
        self.filepath = filepath
        self.is_widget = is_widget
        self.data_length = None
        self.data = None

    def startupload(self):

        if self.url is None:
            return 1

        if self.filepath is None:
            return 2

        with open(self.filepath, 'rb') as fd:
            self.data = base64.b64encode(fd.read())

        if self.data is None:
            return 3

        self.remaining_byte = 0
        self.data_length = len(self.data) + 216
        self.progress_bar = aesirProgressBar(len(self.data) + 216)

        if self.is_widget is None:
            Gdk.threads_init()
            self.widget = progressBarWidget("Upload Operation Dialog")
            self.initWidgets()

        self.googlesearchquery()

    def uploadmonitorcallback(self, monitor):
        self.timer = GObject.timeout_add (10000, self.progress_bar.progress_timeout, self)
        step = round(100*(monitor.bytes_read/self.data_length))
        GObject.idle_add(self.progress_step.set_text, "%" + str(step))
        self.progress_bar.setRemainingBytesofFile(monitor.bytes_read)


    def clientworkerfunc(self):
        requirements = MultipartEncoder(
            fields={'format': 'json',
                    'source': self.data}
        )
        m = MultipartEncoderMonitor(requirements, self.uploadmonitorcallback)
        response = requests.post('https://imgyukle.com/api/1/upload/?key=407289b6f603c950af54fbc79311b9b0', data = m,
                                 headers={'Content-Type': m.content_type})

        try:
            self.url = response.json()["image"]["url"]
        except Exception as e:
            return str(e)

        if self.is_widget is None:
            GObject.source_remove(self.timer)
            Gdk.threads_enter()
            self.horizontal_box.pack_start(self.url_text, expand=True, fill=True, padding=0)
            GObject.idle_add(self.open_button.set_sensitive, self.url)
            GObject.idle_add(self.widget.set_title,"Upload Finished!")
            GObject.idle_add(self.copy_button.set_sensitive, self.url)
            GObject.idle_add(self.url_text.set_text, self.url)
            GObject.idle_add(self.url_text.select_region,0,len(self.url))
            Gdk.threads_leave()
        else:
            return self.url

    def googlesearchquery(self):
        clientHandler = threading.Thread(target=self.clientworkerfunc)
        clientHandler.setDaemon(True)
        clientHandler.start()

    def openurl(self, widget):
        webbrowser.open(self.url)
        self.widget.destroy()

    def copyurl(self, widget):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(self.url, len(self.url))
        self.widget.destroy()

    def initWidgets(self):

        self.widget.set_position(Gtk.WindowPosition.CENTER)
        self.widget.set_keep_above(True)
        self.vertical_box = Gtk.VBox()
        self.horizontal_box = Gtk.HBox()
        self.open_button = Gtk.Button("Open")
        self.copy_button = Gtk.Button("Copy")
        self.progress_step = Gtk.Label()
        self.url_text = Gtk.Entry()
        self.url_text.show()
        self.progress_step.set_text("%0")
        self.open_button.connect("clicked", self.openurl)
        self.copy_button.connect("clicked", self.copyurl)
        self.open_button.show()
        self.open_button.set_sensitive(False)
        self.copy_button.set_sensitive(False)
        self.horizontal_box.pack_start(self.progress_bar, expand=True, fill=True, padding=0)
        self.horizontal_box.pack_start(self.progress_step, expand=True, fill=True, padding=1)
        self.horizontal_box.pack_start(self.open_button, expand=True, fill=True, padding=0)
        self.horizontal_box.pack_start(self.copy_button, expand=True, fill=True, padding=0)
        self.vertical_box.add(self.horizontal_box)
        self.timer = GObject.timeout_add (10000, self.progress_bar.progress_timeout, self)
        self.widget.add(self.vertical_box)
        self.widget.show_all()
