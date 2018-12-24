import gi
import requests
import math
import base64
import threading
import webbrowser
from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf, GLib
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from aesirwebrequest import GoogleSearchUploader
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('AppIndicator3', '0.1')

c = []
d = []

from parameters import CONF_FILE_INSTANCE


class oldSelectionRectangle:
    def __init__(self, e_x, e_y, s_x, s_y, status):
        self.e_x = e_x
        self.e_y = e_y
        self.s_x = s_x
        self.s_y = s_y
        self.is_free = status


from operationMenu import operationMenuDialog as opMenu

from os.path import abspath, dirname, join
from math import pi
import sys
import os
import cairo
from Xlib import X, display, Xutil
from math import ceil
import array

from gi.repository import GObject

a = []
b = []


class selectionOperations:
    SELECTION_SYSTEM_OPEN = 0
    SELECTION_ABORTED = 1
    SELECTION_STARTED = 2
    SELECTION_FINISHED = 3
    SELECTION_DRAWING = 4
    SELECTION_MOVING = 5
    SELECTION_RECTANGLE = 6
    SELECTION_NOTHING = 7
    SELECTION_PENCIL = 8
    SELECTION_REFRESH = 9


class MouseButtons:
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3


class ActiveWindow(gtk.Window):

    def copyClickEvent(self, widget):
        self.operation_menu.saveClipBoard()

    def saveClickEvent(self, widget):
        self.operation_menu.saveScreenShot()

    def clearSelectionClickEvent(self, widget):
        self.operation_flag = selectionOperations.SELECTION_ABORTED
        self.queue_draw()
        self.is_rectangle_selection_completed = False
        return True

    def fullScreenClickEvent(self, widget):
        self.start_position_of_x = 0
        self.start_position_of_y = 0
        self.end_position_of_x = 1366
        self.end_position_of_y = 768
        self.operation_flag = selectionOperations.SELECTION_RECTANGLE
        self.queue_draw()
        self.refactorOperationMenu()
        self.is_rectangle_selection_completed = True

    def exitButtonClickEvent(self, widget):
        self.exitFromActiveWindow()
        return True

    def setActionFromOpMenu(self, action):
        self.operation_flag = action

        return True

    def getActiveScreenMetrics(self):
        # get active root window

        self.active_window = gdk.get_default_root_window()
        # get window height and width using active window

        self.active_window_width = self.active_window.get_width()
        self.active_window_height = self.active_window.get_height()
        print(self.active_window_width)
        return

    def getActiveScreenPixbuf(self):
        # take a pixbuf over active window.
        self.active_window_pixbuf = \
            gdk.pixbuf_get_from_window(self.active_window, 0, 0, self.active_window_width, self.active_window_height)

        return self.active_window_pixbuf

    def initParameters(self):
        # set application parameters to zero for application
        self.start_position_of_x = 0;
        self.start_position_of_y = 0;
        self.end_position_of_x = 0;
        self.end_position_of_y = 0;
        self.old_selection = [0, 0, 0, 0]
        self.rectange_area_size = 0
        self.selection_rectangle_coordinates = [0, 0, 0, 0]
        self.selection_rectangle_x_ycoordinates = [0, 0, 0, 0, 0, 0, 0, 0]
        self.current_mouse_position = [0, 0]

        self.rectangle_slide_mouse_flags = [0, 0, 0, 0]

        self.rectangle_x_coords = []
        self.rectangle_y_coords = []

        self.opMenu_new_x_loc = 0
        self.opMenu_new_y_loc = 0
        self.moving_offset_x = 0
        self.x_rectangle_border_points = []
        self.moving_offset_y = 0

        self.uploadProgressBarWindow = None
        self.selection_rectangle_border_step = 0
        self.x_rectangle_border_size = 0
        self.selection_rectangle_move_start_x = 0
        self.selection_rectangle_move_start_y = 0
        self.selection_rectangle_move_end_x = 0
        self.selection_rectangle_move_end_y = 0
        self.rectangle_offset = 1
        self.is_rectangle_selection_completed = False
        self.is_cursor_in_rectangle_selection_area = False
        self.is_rectangle_moving_completed = True

        self.operation_flag = selectionOperations.SELECTION_SYSTEM_OPEN;

        self.is_draw_continue = False;

    def restoreMousePointer(self):
        gdk_window = self.get_root_window()
        gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.ARROW))

    def ActiveWin_on_key_release_event(self, widget, event, data=None):
        # if escape key pressed
        if event.keyval == gdk.KEY_Escape:
            self.exitFromActiveWindow()

    def initSignalSlots(self):
        self.connect("key-release-event", self.ActiveWin_on_key_release_event)
        self.set_events(gdk.EventMask.POINTER_MOTION_MASK | gdk.EventMask.POINTER_MOTION_HINT_MASK)
        self.connect("motion-notify-event", self.on_button_press)
        self.connect("button-press-event", self.on_button_press)
        self.connect("button-release-event", self.on_button_press)

    def refactorOperationMenu(self):

        if (self.end_position_of_x > self.start_position_of_x):
            self.opMenu_new_x_loc = self.end_position_of_x
        else:
            self.opMenu_new_x_loc = self.start_position_of_x

        if (self.end_position_of_y > self.start_position_of_y):
            self.opMenu_new_y_loc = self.end_position_of_y
        else:
            self.opMenu_new_y_loc = self.start_position_of_y

        self.operation_menu.changePositionOpMenu(self.opMenu_new_x_loc - 4, self.opMenu_new_y_loc - 4)

    def initWindowConfigs(self):

        self.set_border_width(10)
        self.set_position(gtk.WindowPosition.CENTER)
        self.fullscreen()

        self.connect("draw", self.area_draw)

    def uploadSubMenuClickCallback(self, widget, args):


        self.operation_menu.saveScreenShot()
        x = GoogleSearchUploader("http://www.google.com.tr/searchbyimage/upload", "screenshot.png", None)
        x.startupload()

        self.exitFromActiveWindow()

    def initOperationMenu(self):

        # create menu for right click
        self.right_click_menu = gtk.Menu()

        self.upload_submenu = gtk.Menu()

        for item in CONF_FILE_INSTANCE["Servers"]["Sites"]:
            menu_item = gtk.MenuItem(item)

            menu_item.connect('activate', self.uploadSubMenuClickCallback, item)
            menu_item.show()
            self.upload_submenu.append(menu_item)

        self.upload_item = gtk.MenuItem("Upload ")
        self.upload_item.set_submenu(self.upload_submenu)

        self.fullscreen_item = gtk.MenuItem("Full Screen")
        self.copy_item = gtk.MenuItem("Copy Selection")
        self.save_item = gtk.MenuItem("Save Selection")
        self.clear_item = gtk.MenuItem("Clear Selection")
        self.exit_item = gtk.MenuItem("Exit")

        self.copy_item.set_tooltip_text("Copy Selection to ClipBoard!")
        self.save_item.set_tooltip_text("Save Selection to File!")
        self.clear_item.set_tooltip_text("Clear All Selection!")
        self.fullscreen_item.set_tooltip_text("Select all of the current screen!")
        self.exit_item.set_tooltip_text("Exit From Aesir!")

        self.copy_item.connect("activate", self.copyClickEvent)
        self.save_item.connect("activate", self.saveClickEvent)
        self.clear_item.connect("activate", self.clearSelectionClickEvent)
        self.fullscreen_item.connect("activate", self.fullScreenClickEvent)
        self.exit_item.connect("activate", self.exitButtonClickEvent)

        self.right_click_menu.append(self.upload_item)
        self.right_click_menu.append(self.fullscreen_item)
        self.right_click_menu.append(self.copy_item)
        self.right_click_menu.append(self.save_item)
        self.right_click_menu.append(self.clear_item)
        self.right_click_menu.append(self.exit_item)

        self.operation_menu = opMenu(self)
        self.operation_menu.hideOpMenu()

    def __init__(self):
        super(ActiveWindow, self).__init__()

        # prepare window application
        self.initWindowConfigs()
        # init parameters to zero
        self.initParameters()

        self.oldSelectionRectangle = oldSelectionRectangle(0, 0, 0, 0, False)

        # get geometry and active window instance
        self.getActiveScreenMetrics()

        # get screenshot of active window
        self.getActiveScreenPixbuf()
        self.selectionRectanglePixbuf = None
        self.selection_rectangle_status = False
        # connect signal-slot events.
        self.initSignalSlots()

        # init operation menu
        self.initOperationMenu()

        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()

        self.opmenu_rectangle_start_x = 0
        self.opmenu_rectangle_start_y = 0
        self.opmenu_rectangle_end_x = 0
        self.opmenu_rectangle_end_y = 0

        if self.visual != None and self.screen.is_composited():
            self.set_visual(self.visual)

        self.set_app_paintable(True)

        self.show_all()

    def createpaintwidget(self):
        self.widget_start_location = self.end_position_of_x

    def clearScreen(self):
        self.set_visible(False)

    def getSelectedAreaPixbuf(self):
        x0 = self.end_position_of_x
        x1 = self.start_position_of_x
        y0 = self.end_position_of_y
        y1 = self.start_position_of_y

        crr = None

        if (x0 < x1):
            if (y0 < y1):
                crr = GdkPixbuf.Pixbuf.new_subpixbuf(self.active_window_pixbuf, x0, y0, abs(x0 - x1), abs(y0 - y1))
            elif (y0 > y1):
                crr = GdkPixbuf.Pixbuf.new_subpixbuf(self.active_window_pixbuf, x0, y1, abs(x0 - x1), abs(y0 - y1))
        else:
            if (y0 < y1):
                crr = GdkPixbuf.Pixbuf.new_subpixbuf(self.active_window_pixbuf, x1, y0, abs(x0 - x1), abs(y0 - y1))
            elif (y0 > y1):
                crr = GdkPixbuf.Pixbuf.new_subpixbuf(self.active_window_pixbuf, x1, y1, abs(x0 - x1), abs(y0 - y1))

        if (crr != None):
            return crr
        else:
            return None

    def clearSelectedAreaMetrics(self):
        self.end_position_of_x = 0
        self.end_position_of_y = 0
        self.start_position_of_x = 0
        self.start_position_of_y = 0

    def drawSelectionRectangleGridLines(self, cr, offset_x, offset_y):

        self.x_rectangle_border_size = int((abs(self.end_position_of_x - self.start_position_of_x)))
        self.y_rectangle_border_size = int((abs(self.end_position_of_y - self.start_position_of_y)))

        if self.checkBiggestPos(self.start_position_of_x, self.end_position_of_x):
            self.x_rectangle_border_points = [self.start_position_of_x + offset_x,
                                              self.start_position_of_x + int(abs(
                                                  self.end_position_of_x - self.start_position_of_x) / 2) + offset_x,
                                              self.end_position_of_x + offset_x]
        else:
            self.x_rectangle_border_points = [self.end_position_of_x + offset_x,
                                              self.end_position_of_x + int(abs(
                                                  self.end_position_of_x - self.start_position_of_x) / 2) + offset_x,
                                              self.start_position_of_x + offset_x]

        if self.checkBiggestPos(self.start_position_of_y, self.end_position_of_y):
            self.y_rectangle_border_points = [
                self.start_position_of_y + offset_y + int(abs(self.end_position_of_y - self.start_position_of_y) / 2)
            ]

            self.y_rectangle_border_extra_points = [
                self.start_position_of_y,
                self.start_position_of_y + offset_y + int(abs(self.end_position_of_y - self.start_position_of_y) / 2),
                self.start_position_of_y + offset_y + 2 * int(
                    abs(self.end_position_of_y - self.start_position_of_y) / 2)
            ]
        else:
            self.y_rectangle_border_points = [
                self.end_position_of_y + offset_y + int(abs(self.end_position_of_y - self.start_position_of_y) / 2)
            ]
            self.y_rectangle_border_extra_points = [
                self.start_position_of_y,
                self.start_position_of_y + offset_y + int(abs(self.end_position_of_y - self.start_position_of_y) / 2),
                self.start_position_of_y + offset_y + 2 * int(
                    abs(self.end_position_of_y - self.start_position_of_y) / 2)
            ]

        self.selection_rectangle_border_step = 8

        for i in range(1, self.x_rectangle_border_size, self.selection_rectangle_border_step):
            cr.set_source_rgba(0, 0, 0, 1)
            if self.checkBiggestPos(self.start_position_of_x, self.end_position_of_x):
                cr.rectangle(self.start_position_of_x + i + offset_x, self.start_position_of_y + offset_y, 3, 1)
            else:
                cr.rectangle(self.end_position_of_x + i + offset_x, self.start_position_of_y + offset_y, 3, 1)
            cr.fill()

        for i in range(1, self.x_rectangle_border_size, self.selection_rectangle_border_step):
            cr.set_source_rgba(0, 0, 0, 1)
            if self.checkBiggestPos(self.start_position_of_x, self.end_position_of_x):
                cr.rectangle(self.start_position_of_x + i + offset_x, self.end_position_of_y + offset_y, 3, 1)
            else:
                cr.rectangle(self.end_position_of_x + i + offset_x, self.end_position_of_y + offset_y, 3, 1)
            cr.fill()

        for i in range(1, self.y_rectangle_border_size, self.selection_rectangle_border_step):
            cr.set_source_rgba(0, 0, 0, 1)
            if self.checkBiggestPos(self.start_position_of_y, self.end_position_of_y):
                cr.rectangle(self.start_position_of_x + offset_x, self.start_position_of_y + i + offset_y, 1, 3)
            else:
                cr.rectangle(self.start_position_of_x + offset_x, self.end_position_of_y + i + offset_y, 1, 3)
            cr.fill()

        for i in range(1, self.y_rectangle_border_size, self.selection_rectangle_border_step):
            cr.set_source_rgba(0, 0, 0, 1)
            if self.checkBiggestPos(self.start_position_of_y, self.end_position_of_y):
                cr.rectangle(self.end_position_of_x + offset_x, self.start_position_of_y + i + offset_y, 1, 3)
            else:
                cr.rectangle(self.end_position_of_x + offset_x, self.end_position_of_y + i + offset_y, 1, 3)
            cr.fill()

        for i in self.x_rectangle_border_points:
            cr.set_source_rgba(0, 0, 0, 1)

            k = i

            cr.rectangle(k - 2, self.start_position_of_y - 3 + offset_y, 5, 5)
            cr.rectangle(k - 2, self.end_position_of_y - 3 + offset_y, 5, 5)
            cr.fill()

        for i in self.y_rectangle_border_points:
            cr.set_source_rgba(0, 0, 0, 1)

            y_rectangle_start_x_pos = self.start_position_of_x - 3 + offset_x
            y_rectangle_end_x_pos = self.end_position_of_x - 3 + offset_x

            cr.rectangle(y_rectangle_start_x_pos, i - 2, 5, 5)
            cr.rectangle(y_rectangle_end_x_pos, i - 2, 5, 5)
            cr.fill()

    def checkIfSelectionRectangleIsBig(self, start_x, start_y, end_x, end_y):
        if (abs(end_x - start_x) > 1 and abs(end_y - start_y) > 1):
            return True
        else:
            return False

    def printBasePixbuf(self, cairo_instance):

        gdk.cairo_set_source_pixbuf(cairo_instance, self.active_window_pixbuf, 0, 0)
        cairo_instance.paint()
        cairo_instance.set_source_rgba(.2, .2, .2, 0.6)
        cairo_instance.paint()
        gdk.cairo_set_source_pixbuf(cairo_instance, self.active_window_pixbuf, 0, 0)

    def area_draw(self, widget, cr):

        if self.operation_flag == selectionOperations.SELECTION_PENCIL:
            self.printBasePixbuf(cr)

            self.cairoGetPaintColor(cr)

            cr.set_source_rgba(255, 0, 0, 1)
            i = 1
            while i < len(c):
                cr.set_line_width(20)

                cr.move_to(c[i - 1], d[i - 1])

                cr.line_to(c[i], d[i])

                cr.arc(c[i], d[i], 20, 0, 2 * math.pi)
                cr.fill()
                i += 1

            return True

        if self.operation_flag == selectionOperations.SELECTION_SYSTEM_OPEN:
            self.printBasePixbuf(cr)
            cr.set_source_rgb(0, 255, 0.1)

            cr.select_font_face("Times New Roman", cairo.FONT_SLANT_NORMAL,
                                cairo.FONT_WEIGHT_NORMAL)

            cr.set_font_size(16)

            size_of_rectangle = "Alan Seciniz!"

            cr.move_to(self.current_mouse_position[0], self.current_mouse_position[1])

            cr.show_text(size_of_rectangle)

            return True

        elif self.operation_flag == selectionOperations.SELECTION_NOTHING:
            cr.save()
            return True

        if self.operation_flag == selectionOperations.SELECTION_ABORTED:
            self.printBasePixbuf(cr)
            self.operation_menu.hideOpMenu()

            self.clearSelectedAreaMetrics()

            return True

        elif self.operation_flag == selectionOperations.SELECTION_REFRESH:

            self.printBasePixbuf(cr)
            self.start_position_of_x = self.old_selection[2]
            self.start_position_of_y = self.old_selection[3]
            self.end_position_of_x = self.old_selection[0]
            self.end_position_of_y = self.old_selection[1]
            self.opmenu_old_x_pos = self.old_selection[4]
            self.opmenu_old_y_pos = self.old_selection[5]

            cr.rectangle(self.start_position_of_x, self.start_position_of_y,
                         self.end_position_of_x - self.start_position_of_x,
                         self.end_position_of_y - self.start_position_of_y)

            cr.stroke()

            cr.rectangle(self.start_position_of_x + self.rectangle_offset,
                         self.start_position_of_y + self.rectangle_offset,
                         self.end_position_of_x - self.start_position_of_x - 2 * self.rectangle_offset,
                         self.end_position_of_y - self.start_position_of_y - 2 * self.rectangle_offset)

            cr.fill()

            self.drawSelectionRectangleGridLines(cr, self.moving_offset_x, self.moving_offset_y)
            self.refactorOperationMenu()
            # self.operation_menu.appMoveWindow(self.opMenu_new_x_loc,self.opMenu_new_y_loc)


        elif self.operation_flag == selectionOperations.SELECTION_MOVING:

            self.printBasePixbuf(cr)

            cr.rectangle(self.start_position_of_x + self.moving_offset_x,
                         self.start_position_of_y + self.moving_offset_y,
                         self.end_position_of_x - self.start_position_of_x,
                         self.end_position_of_y - self.start_position_of_y)

            cr.stroke()

            cr.rectangle(self.start_position_of_x + self.moving_offset_x + self.rectangle_offset,
                         self.start_position_of_y + self.moving_offset_y + self.rectangle_offset,
                         self.end_position_of_x - self.start_position_of_x - 2 * self.rectangle_offset,
                         self.end_position_of_y - self.start_position_of_y - 2 * self.rectangle_offset)

            cr.fill()

            # move rectangle borders with moving offset
            self.drawSelectionRectangleGridLines(cr, self.moving_offset_x, self.moving_offset_y)
            return True;

        elif self.operation_flag == selectionOperations.SELECTION_FINISHED:

            return True;

        elif self.operation_flag == selectionOperations.SELECTION_RECTANGLE:

            self.rectange_area_x_size = int(abs(self.start_position_of_x - self.end_position_of_x))
            self.rectange_area_y_size = int(abs(self.start_position_of_y - self.end_position_of_y))

            self.rectange_area_size = self.rectange_area_x_size * self.rectange_area_y_size

            if not self.rectange_area_x_size:
                print("hata")
                self.printBasePixbuf(cr)
                return True

            self.printBasePixbuf(cr)

            cr.rectangle(self.start_position_of_x, self.start_position_of_y,
                         self.end_position_of_x - self.start_position_of_x,
                         self.end_position_of_y - self.start_position_of_y)

            cr.stroke()

            cr.rectangle(self.start_position_of_x + self.rectangle_offset,
                         self.start_position_of_y + self.rectangle_offset,
                         self.end_position_of_x - self.start_position_of_x - 2 * self.rectangle_offset,
                         self.end_position_of_y - self.start_position_of_y - 2 * self.rectangle_offset)

            cr.fill()

            cr.set_source_rgb(255, 0.1, 0.1)

            cr.select_font_face("Times New Roman", cairo.FONT_SLANT_NORMAL,
                                cairo.FONT_WEIGHT_NORMAL)

            if (self.start_position_of_x > self.end_position_of_x):
                self.selection_rectangle_coordinates[0] = self.start_position_of_x
                self.selection_rectangle_coordinates[2] = self.end_position_of_x
            else:
                self.selection_rectangle_coordinates[0] = self.end_position_of_x
                self.selection_rectangle_coordinates[2] = self.start_position_of_x

            if (self.start_position_of_y > self.end_position_of_y):
                self.selection_rectangle_coordinates[1] = self.start_position_of_y
                self.selection_rectangle_coordinates[3] = self.end_position_of_y
            else:
                self.selection_rectangle_coordinates[1] = self.end_position_of_y
                self.selection_rectangle_coordinates[3] = self.start_position_of_y

            self.rectangle_x_coords = [self.selection_rectangle_coordinates[0], self.selection_rectangle_coordinates[2]]
            self.rectangle_y_coords = [self.selection_rectangle_coordinates[1], self.selection_rectangle_coordinates[3]]

            self.selection_rectangle_size_font = 16

            if (self.selection_rectangle_size_font < 16):
                self.selection_rectangle_size_font = 16

            cr.set_font_size(16)

            cr.set_source_rgb(0, 0, 50)

            size_of_rectangle = " %d x %d" % (abs(self.end_position_of_x - self.start_position_of_x),
                                              abs(self.end_position_of_y - self.start_position_of_y))

            cr.move_to(self.opMenu_new_x_loc - 75, self.opMenu_new_y_loc - 5)

            cr.show_text(size_of_rectangle)

            self.drawSelectionRectangleGridLines(cr, -1, -1)

        else:
            print("sxc")
            return True

    def checkClickNearOnRectangle(self, current_x, current_y):
        if self.start_position_of_x < current_x and current_x <= self.end_position_of_x:
            if self.start_position_of_y < current_y and current_y <= self.end_position_of_y:
                return True
            else:
                return False

        else:
            return False

    def exitFromActiveWindow(self):
        self.operation_menu.exitFromOpMenu()
        self.destroy()

    def checkBiggestPos(self, start_pos, end_pos):
        if start_pos > end_pos:
            return 0
        elif end_pos > start_pos:
            return 1

    def on_button_press(self, w, e):

        if e.type == gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.LEFT_BUTTON:

            if self.is_rectangle_selection_completed:
                if self.is_cursor_in_rectangle_selection_area:
                    self.is_rectangle_moving_completed = False
                    self.operation_flag = selectionOperations.SELECTION_MOVING



                else:
                    self.is_rectangle_selection_completed = False
                    self.operation_flag = selectionOperations.SELECTION_ABORTED
                    self.queue_draw()

                    oldSelectionRectangle.e_x = self.end_position_of_x
                    oldSelectionRectangle.e_y = self.end_position_of_y
                    oldSelectionRectangle.s_x = self.start_position_of_x
                    oldSelectionRectangle.s_y = self.start_position_of_y

                    self.old_selection = [self.end_position_of_x, self.end_position_of_y,
                                          self.start_position_of_x, self.start_position_of_y, self.opMenu_new_x_loc,
                                          self.opMenu_new_y_loc]

                    oldSelectionRectangle.is_free = True
                    self.start_position_of_x = e.x
                    self.start_position_of_y = e.y
                    self.end_position_of_x = e.x
                    self.end_position_of_y = e.y
                    self.operation_menu.hideOpMenu()
                    self.operation_flag = selectionOperations.SELECTION_RECTANGLE
                    self.queue_draw()

                    return True

            if not self.is_rectangle_selection_completed:
                self.operation_flag = selectionOperations.SELECTION_RECTANGLE

                if self.operation_flag == selectionOperations.SELECTION_RECTANGLE:
                    self.start_position_of_x = e.x
                    self.start_position_of_y = e.y
                    self.end_position_of_x = e.x
                    self.end_position_of_y = e.y

                    self.operation_menu.hideOpMenu()
                    self.queue_draw()
                    return True

            elif self.is_rectangle_selection_completed:

                if (self.is_cursor_in_rectangle_selection_area):
                    self.selection_rectangle_move_start_x = e.x
                    self.selection_rectangle_move_start_y = e.y
                    self.selection_rectangle_move_end_x = e.x
                    self.selection_rectangle_move_end_y = e.y
                    self.operation_menu.hideWindowOpMenu()
                    self.operation_flag = selectionOperations.SELECTION_MOVING
                    return True

            return True

        elif e.type == gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.RIGHT_BUTTON:

            if not self.is_rectangle_selection_completed:

                self.upload_item.set_sensitive(False)
                self.copy_item.set_sensitive(False)
                self.save_item.set_sensitive(False)

            else:

                self.upload_item.set_sensitive(True)
                self.copy_item.set_sensitive(True)
                self.save_item.set_sensitive(True)

            self.right_click_menu.show_all()
            self.right_click_menu.popup(None, None, None, None, 0, gtk.get_current_event_time())
            return True


        elif e.type == gdk.EventType.BUTTON_RELEASE \
                and e.button == MouseButtons.LEFT_BUTTON:

            if self.operation_flag == selectionOperations.SELECTION_MOVING:
                self.is_rectangle_moving_completed = True

                self.start_position_of_x = self.start_position_of_x + self.moving_offset_x
                self.end_position_of_x = self.end_position_of_x + self.moving_offset_x
                self.start_position_of_y = self.start_position_of_y + self.moving_offset_y
                self.end_position_of_y = self.end_position_of_y + self.moving_offset_y

                self.refactorOperationMenu()
                self.operation_menu.showOpMenu()
                self.operation_flag = selectionOperations.SELECTION_RECTANGLE
                self.moving_offset_x = 0
                self.moving_offset_y = 0
                self.queue_draw()
                return True

            if self.operation_flag == selectionOperations.SELECTION_RECTANGLE:
                if not self.is_rectangle_selection_completed:

                    if not self.rectange_area_size:
                        self.operation_flag = selectionOperations.SELECTION_REFRESH
                        self.queue_draw()
                        self.refactorOperationMenu()
                        self.operation_menu.showOpMenu()

                        self.is_rectangle_selection_completed = False
                        return True

                    if self.checkIfSelectionRectangleIsBig(
                            self.start_position_of_x,
                            self.start_position_of_y,
                            self.end_position_of_x,
                            self.end_position_of_y
                    ):
                        self.refactorOperationMenu()
                        self.operation_menu.showOpMenu()
                        self.is_rectangle_selection_completed = True
                        return True

                return True





        elif e.type == gdk.EventType.MOTION_NOTIFY:

            if self.operation_flag == selectionOperations.SELECTION_SYSTEM_OPEN:
                self.current_mouse_position = [e.x, e.y]
                self.queue_draw()

            if not self.is_rectangle_selection_completed:

                if (self.operation_flag == selectionOperations.SELECTION_RECTANGLE):
                    self.end_position_of_x = e.x
                    self.end_position_of_y = e.y
                    if not self.selection_rectangle_status:
                        self.queue_draw()
                    else:
                        return True

                elif (self.operation_flag == selectionOperations.SELECTION_STARTED):
                    print("anan")

            if self.is_rectangle_selection_completed:

                if (self.operation_flag == selectionOperations.SELECTION_MOVING):
                    if not self.is_rectangle_moving_completed:
                        self.selection_rectangle_move_end_x = e.x
                        self.selection_rectangle_move_end_y = e.y

                        self.moving_offset_x = int(
                            abs(self.selection_rectangle_move_end_x - self.selection_rectangle_move_start_x))
                        self.moving_offset_y = int(
                            abs(self.selection_rectangle_move_end_y - self.selection_rectangle_move_start_y))

                        if self.checkBiggestPos(self.selection_rectangle_move_start_x,
                                                self.selection_rectangle_move_end_x):
                            self.moving_offset_x = self.moving_offset_x

                        else:
                            self.moving_offset_x = -self.moving_offset_x

                        if self.checkBiggestPos(self.selection_rectangle_move_start_y,
                                                self.selection_rectangle_move_end_y):
                            self.moving_offset_y = self.moving_offset_y

                        else:
                            self.moving_offset_y = -self.moving_offset_y

                        self.queue_draw()

                if (self.operation_flag == selectionOperations.SELECTION_PENCIL):
                    self.end_position_of_x = e.x
                    self.end_position_of_y = e.y
                    c.append(int(e.x))
                    d.append(int(e.y))
                    self.queue_draw()

            if self.is_rectangle_selection_completed:
                gdk_window = self.get_root_window()

                # for i in self.rectangle_x_coords:
                #   if e.x >= i and e.x < i + 4:

                x_index = 0
                y_index = 0

                for i in self.rectangle_x_coords:
                    x_index = x_index + 1
                    if e.x >= i and e.x < i + 10:
                        for j in self.rectangle_y_coords:
                            y_index = y_index + 1
                            if (e.y >= j and e.y < j + 10):
                                print("a")

                                if x_index == 1:
                                    if y_index == 1:
                                        gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.BOTTOM_RIGHT_CORNER))
                                        self.rectangle_slide_mouse_flags = [1, 0, 0, 0]
                                        return True
                                    else:
                                        gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.TOP_RIGHT_CORNER))
                                        self.rectangle_slide_mouse_flags = [0, 1, 0, 0]
                                        return True
                                elif x_index == 2:
                                    if y_index == 1:
                                        gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.BOTTOM_LEFT_CORNER))
                                        self.rectangle_slide_mouse_flags = [0, 0, 1, 0]
                                        return True
                                    else:
                                        gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.TOP_LEFT_CORNER))
                                        self.rectangle_slide_mouse_flags = [0, 0, 0, 1]
                                        return True
                                else:
                                    print("baban")
                                    self.rectangle_slide_mouse_flags = [0, 0, 0, 0]

                                gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.SIZING))
                                return True

                if self.checkBiggestPos(self.start_position_of_x, self.end_position_of_x):

                    if self.start_position_of_x < e.x and e.x <= self.end_position_of_x:

                        if self.checkBiggestPos(self.start_position_of_y, self.end_position_of_y):
                            if self.start_position_of_y < e.y and e.y <= self.end_position_of_y:
                                gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.HAND1))
                                self.is_cursor_in_rectangle_selection_area = True
                            else:
                                self.is_cursor_in_rectangle_selection_area = False
                                gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.ARROW))

                        else:
                            if self.end_position_of_y < e.y and e.y <= self.start_position_of_y:
                                gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.HAND1))
                                self.is_cursor_in_rectangle_selection_area = True
                            else:
                                self.is_cursor_in_rectangle_selection_area = False
                                gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.ARROW))

                    else:
                        self.is_cursor_in_rectangle_selection_area = False
                        gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.ARROW))


                elif not self.checkBiggestPos(self.start_position_of_x, self.end_position_of_x):

                    if self.end_position_of_x < e.x and e.x <= self.start_position_of_x:

                        if self.checkBiggestPos(self.start_position_of_y, self.end_position_of_y):
                            if self.start_position_of_y < e.y and e.y <= self.end_position_of_y:
                                gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.HAND1))
                                self.is_cursor_in_rectangle_selection_area = True
                            else:
                                self.is_cursor_in_rectangle_selection_area = False
                                gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.ARROW))

                        else:
                            if self.end_position_of_y < e.y and e.y <= self.start_position_of_y:
                                gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.HAND1))
                                self.is_cursor_in_rectangle_selection_area = True
                            else:
                                self.is_cursor_in_rectangle_selection_area = False
                                gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.ARROW))
                    else:
                        self.is_cursor_in_rectangle_selection_area = False
                        gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.ARROW))

                else:
                    self.is_cursor_in_rectangle_selection_area = False
                    gdk_window.set_cursor(gdk.Cursor(gdk.CursorType.ARROW))


def main():
    Aesir = ActiveWindow()
    gtk.main()


if __name__ == "__main__":
    main()
