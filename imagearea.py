#!/usr/bin/env python

import os, sys, getopt, signal, array, time, random

import cairo
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf
from gi.repository import Pango

gi.require_version('PangoCairo', '1.0')
from gi.repository import PangoCairo

DIVIDER     = 32                    # How many divisions

# --------------------------------------------------------------------
# Class to instantiate a window so we can use it simply

class imgarea(Gtk.DrawingArea):

    def __init__(self, wwww = 500, hhhh = 500):

        GObject.GObject.__init__(self);

        self.cnt = 0
        self.divider = DIVIDER;
        self.wwww = wwww; self.hhhh = hhhh
        self.set_size_request(wwww, hhhh)

        self.annote = []; self.aframe = []; self.atext = []
        self.mag = False
        self.event_x = self.event_y = 0

        self.penx = 0
        # Our font
        fsize = 14
        fname = "Monospace"
        self._setfont(fname, fsize)

        self.set_events(  Gdk.EventMask.POINTER_MOTION_MASK |
                            Gdk.EventMask.POINTER_MOTION_HINT_MASK |
                            Gdk.EventMask.BUTTON_PRESS_MASK |
                            Gdk.EventMask.BUTTON_RELEASE_MASK |
                            Gdk.EventMask.KEY_PRESS_MASK |
                            Gdk.EventMask.KEY_RELEASE_MASK |
                            Gdk.EventMask.FOCUS_CHANGE_MASK )

        self.set_can_focus(True)

        self.connect("key-press-event", self.key_press_event)
        self.connect("button-press-event", self.area_button)
        self.connect("button-release-event", self.area_button)
        self.connect("draw", self.draw)
        self.connect("realize", self.realize)
        self.connect("motion-notify-event", self.area_motion)

    def realize(self, area):

        #print ("realize", area)
        self.hhh = self.get_height();  self.www = self.get_width()

        #self.pb = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, self.www , self.hhh)
        #self.surfa = Gdk.cairo_surface_create_from_pixbuf( self.pb, 0, self.get_window())

        self.xxx = bytearray(self.www * self.hhh * 4);

        self.buff = array.array("B", self.xxx)
        self.surfa = cairo.ImageSurface.create_for_data(self.buff, cairo.Format.RGB24, self.www , self.hhh)

        self.cr2 = cairo.Context(self.surfa)
        ctx = self.get_style_context()
        fg_color  = ctx.get_color(Gtk.StateFlags.NORMAL)
        bg_color = ctx.get_background_color(Gtk.StateFlags.NORMAL)

        #print("fg colors RGB:", fg_color.red, fg_color.green, fg_color.blue)
        #print("bg colors RGB:", bg_color.red, bg_color.green, bg_color.blue)

        # Paint white, ignore system BG
        self.cr2.set_source_rgba(255, 255, 255)
        #cr2.set_source_rgba(fg_color.red * 255, fg_color.green * 255, fg_color.blue * 255)
        #cr2.set_source_rgba(bg_color.red * 255, bg_color.green * 255, bg_color.blue * 255)

        self.cr2.rectangle( 0, 0, self.www, self.hhh);
        self.cr2.fill()

        # Pre set for drawing
        self.cr2.set_source_rgba(*list(fg_color));
        self.layout = PangoCairo.create_layout(self.cr2)
        self.layout.set_font_description(self.fd)

        #text2 = "Doodle Pad base class"
        #self.layout.set_text(text2, len(text2))
        #xx, yy = self.layout.get_pixel_size()
        #self.cr2.move_to(self.www / 2 - xx / 2  , 4)
        #PangoCairo.show_layout(self.cr2, self.layout)


    def area_motion(self, area, event):
        pass

    def get_size(self):
        rect = self.get_allocation()
        return rect.width, rect.height

    def get_height(self):
        rect = self.get_allocation()
        return rect.height

    def get_width(self):
        rect = self.get_allocation()
        return rect.width

    # Paint the
    def draw(self, widget, cr):
        cr.set_source_surface(self.surfa)
        cr.paint()
        return

    def _setfont(self, fam, size):

        self.fd = Pango.FontDescription()
        self.fd.set_family(fam)
        self.fd.set_size(size * Pango.SCALE);
        self.pangolayout = self.create_pango_layout("a")
        self.pangolayout.set_font_description(self.fd)

        # Get Pango steps
        self.surfax, self.cyy = self.pangolayout.get_pixel_size()

        # Get Pango tabs
        self.tabarr = Pango.TabArray(80, False)

        self.pangolayout.set_tabs(self.tabarr)
        ts = self.pangolayout.get_tabs()


    def invalidate(self, rect = None):
        if rect == None:
            self.queue_draw()
        else:
            #print "Invalidate:", rect.x, rect.y, rect.width, rect.height
            self.queue_draw_area(rect.x, rect.y, \
                            rect.width, rect.height)

    # --------------------------------------------------------------------
    def  area_button(self, win, event):
        self.invalidate()

    # --------------------------------------------------------------------
    def key_press_event(self, win, event):

        #print "img key_press_event", win, event

        if event.get_state() & Gdk.ModifierType.MOD1_MASK:
            if event.keyval == Gdk.KEY_x or event.keyval == Gdk.KEY_X:
                sys.exit(0)

        if event.keyval == Gdk.KEY_Escape:
            self.mag = False
            self.invalidate()

    #def ct(self):
    #    print "in imgarea"




