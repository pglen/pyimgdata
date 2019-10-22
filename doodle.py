#!/usr/bin/env python

import os, sys, getopt, signal, array, time, random, binascii, struct

import cairo, numpy

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf
from gi.repository import Pango

import imagearea

sizex = 30
ttt = 60
lll = 200
period = 8

# --------------------------------------------------------------------
# Implement doodle on top of imgarea
# Make sure you call super(s) as it is in this example

class doodle(imagearea.imgarea):

    def __init__(self, strx):
        imagearea.imgarea.__init__(self);
        self.strx = strx

    def key_press_event(self, win, event):
        #print "doodleimg key_press_event", win, event
        super(doodle, self).key_press_event(win, event)
        pass

    def  area_button(self, win, event):
        #print "doodleimg area_button",  event

        self.grab_focus()
        if event.type == Gdk.EventType.BUTTON_PRESS:
            #print "press", event.x, event.y
            self.penx = 1
            self.event_x = event.x
            self.event_y = event.y

        if event.type == Gdk.EventType.BUTTON_RELEASE:
            #print "relea", event.x, event.y
            self.penx = 0
        super(doodle, self).area_button(win, event)

    # Initialize
    def realize(self, area):

        super(doodle, self).realize(area)
        #print "realize:\n", self.strx

        lll = len(self.strx)
        if lll > 128:
            print "String too long, cutting ", lll
            self.strx = self.strx[:124]

        if lll < 124:
            print "String too short, padding", 124 - lll
            self.strx += " " * (124 - lll)

        self.strx = decorate(self.strx)
        if not check(self.strx):
            print "ERROR checksum does not match"

        bbb = bitify(self.strx)

        # Draw frame
        #self.cr2.set_source_rgba(.7, .7, .7)
        #self.cr2.rectangle( lll, ttt, 30, 30);

        for aa in range(period -1):
            self.cr2.rectangle( lll + aa * 3 * sizex, ttt, sizex, sizex);

        for aa in range(period -1):
            self.cr2.rectangle( lll, ttt + 3 * sizex * aa, sizex, sizex);

        for aa in range(period - 1):
            self.cr2.rectangle( lll + (period -2) * 3 * sizex, ttt + 3 * sizex * aa, sizex, sizex);

        for aa in range(period - 1):
            self.cr2.rectangle( lll + aa * 3 * sizex, ttt + (period-2)* 3 * sizex, sizex, sizex);

        # BIG point

        self.cr2.rectangle( lll + (period-2) * 3 * sizex - sizex/2, ttt + (period-2) * 3 * sizex - sizex/2,
                                    sizex + sizex/2 , sizex + sizex/2);

        self.cr2.fill()

        # Draw data
        #self.cr2.set_source_rgba(.5, .5, .5)

        for aa in range(32):
            for bb in range(32):
                #if random.random() * 2  > 1:
                if bbb[aa + bb * 32]:
                    self.cr2.rectangle( sizex + sizex / 2 +lll + aa * sizex/2, ttt + sizex + sizex/2 + bb * sizex/2,
                                                                                3*sizex/8, 3*sizex/8);
                else:
                    self.cr2.rectangle( sizex + sizex / 2 +lll + aa * sizex/2, ttt + sizex + sizex/2 + bb * sizex/2,
                                                                                 sizex/4, sizex/4);

        self.cr2.fill()

    def decode(self):
        print "Decoding"

        # access surface

        buffx = memoryview(self.surfa.get_data())

        www = self.surfa.get_width()
        hhh = self.surfa.get_height()
        rs  = self.surfa.get_stride()

        '''print type(buffx), dir(buffx), www, hhh, rs
        print "shape", buffx.shape, "is", buffx.itemsize, "ro", buffx.readonly'''

        cnt = 0; old = "";   transient = []; tvalues   = []
        for aaa in range(0, 40, 2):
            startx = (55 + aaa * 2)* rs
            rrr = []; vvv = []
            for aa in range(self.www):

                nnn =  ord(buffx[startx + 4*aa+0])
                nnn += ord(buffx[startx + 4*aa+0])
                nnn += ord(buffx[startx + 4*aa+0])
                nnn /= 3

                if nnn != old:
                    # Get uptick
                    if nnn > old:
                        rrr.append(nnn)
                        vvv.append(aa)
                    old = nnn

            #print "done1", rrr
            #print "done2", vvv

            for aa in range(20):
                buffx[startx + 4*aa+0] = chr(0)
                buffx[startx + 4*aa+1] = chr(0)
                buffx[startx + 4*aa+2] = chr(0)
                buffx[startx + 4*aa+3] = chr(255)

            self.invalidate()
            tvalues.append(vvv)
            transient.append(rrr)
            cnt += 1

        print "pitches"
        for aa in range(len(tvalues)):
            #print "tv", tvalues[aa]
            #print "tr", tvalues[aa]
            arr = tvalues[aa]
            pitch = 0
            if len(arr):
                for bb in range(len(arr) - 1):
                    pitch += arr[bb + 1] - arr[bb]
                print "pp", pitch / (len(arr) - 1),

        print
        self.invalidate()

    def pollute(self):

        buffx = memoryview(self.surfa.get_data())
        rs  = self.surfa.get_stride()

        for aaa in range(200):
            xxx = int(random.random() * (self.www - 4))
            yyy = int(random.random() * (self.hhh - 4))

            for bb in range(24):
                xxx2 = int(random.random() * (12) - 6)
                yyy2 = int(random.random() * (12) - 6)

                buffx[(yyy2+yyy) * rs + (xxx2 + xxx) * 4 + 0] = chr(0)
                buffx[(yyy2+yyy) * rs + (xxx2 + xxx) * 4 + 1] = chr(0)
                buffx[(yyy2+yyy) * rs + (xxx2 + xxx) * 4 + 2] = chr(0)

            self.invalidate()

    # Mouse move
    def area_motion(self, area, event):
        #print "doodleimg area_motion",  event

        if self.penx:
            cr2 = cairo.Context(self.surfa)
            ctx = self.get_style_context()
            fg_color  = ctx.get_color(Gtk.StateFlags.NORMAL)
            cr2.set_source_rgba(*list(fg_color));

            cr2.move_to(self.event_x, self.event_y)
            cr2.line_to(event.x, event.y)
            cr2.stroke()

            #print  event.x, event.y, self.event_x, self.event_y

            rect =   Gdk.Rectangle()
            rect.x = min(self.event_x, event.x) - 1
            rect.y = min(self.event_y, event.y) - 1
            rect.width = abs(self.event_x - event.x) + 2
            rect.height = abs(self.event_y - event.y) + 2

            #print "rect",  rect.x, rect.y, rect.width, rect.height

            self.event_x = event.x
            self.event_y = event.y

            self.invalidate(rect)

        super(doodle, self).area_motion(area, event)
        pass


def checksum(strx):

    sum = 0
    for aa in strx:
        sum += ord(aa)
    return sum


def  decorate(strx):

    sss = binascii.crc32(strx)
    strx += struct.pack("i", sss)
    print "org", sss, len(strx)
    return strx

def check(strx):
    ttt = struct.unpack("i", strx[124:])
    strx2 = strx[:124]
    #print ttt, len(strx2)
    sss2 = binascii.crc32(strx2)
    #print "check", sss2, ttt, len(strx)
    return sss2 == ttt[0]


# Return array of bits

def bitify(strx):

    bbb = []
    # Do bytes
    for aa in range(4):
        for bb in range(32):
            mmm = aa * 32 + bb
            if len(strx) > mmm:
                ddd = ord(strx[mmm:mmm + 1])
            else:
                ddd = 0

            # Do one byte

            xxx = 0x80
            for cc in range(8):
                if xxx & ddd:
                    bbb.append(1)
                else:
                    bbb.append(0)
                xxx = xxx >> 1

    return bbb

