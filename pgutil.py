#!/usr/bin/env python

import os, sys, glob, getopt, time, string, signal, stat, shutil
import traceback

#import warnings; warnings.simplefilter("ignore");
#import gtk; warnings.simplefilter("default")

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

# ------------------------------------------------------------------------
# Handle command line. Interpret optarray and decorate the class

class Config:

    def __init__(self, optarr):
        self.optarr = optarr

    def comline(self, argv):
        optletters = ""
        for aa in self.optarr:
            if aa[0] in optletters:
                print "Warning: duplicate option", "'" + aa[0] + "'"
            optletters += aa[0]
        #print optletters

        # Create defaults:
        for bb in range(len(self.optarr)):
            if self.optarr[bb][1]:
                # Coerse type
                if type(self.optarr[bb][2]) == type(0):
                    self.__dict__[self.optarr[bb][1]] = int(self.optarr[bb][2])
                if type(self.optarr[bb][2]) == type(""):
                    self.__dict__[self.optarr[bb][1]] = str(self.optarr[bb][2])
        try:
            opts, args = getopt.getopt(argv, optletters)
        except getopt.GetoptError, err:
            print "Invalid option(s) on command line:", err
            return ()

        #print "opts", opts, "args", args
        for aa in opts:
            for bb in range(len(self.optarr)):
                if aa[0][1] == self.optarr[bb][0][0]:
                    #print "match", aa, self.optarr[bb]
                    if len(self.optarr[bb][0]) > 1:
                        #print "arg", self.optarr[bb][1], aa[1]
                        if self.optarr[bb][2] != None:
                            if type(self.optarr[bb][2]) == type(0):
                                self.__dict__[self.optarr[bb][1]] = int(aa[1])
                            if type(self.optarr[bb][2]) == type(""):
                                self.__dict__[self.optarr[bb][1]] = str(aa[1])
                    else:
                        #print "set", self.optarr[bb][1], self.optarr[bb][2]
                        if self.optarr[bb][2] != None:
                            self.__dict__[self.optarr[bb][1]] = 1
                        #print "call", self.optarr[bb][3]
                        if self.optarr[bb][3] != None:
                            self.optarr[bb][3]()
        return args

# ------------------------------------------------------------------------
# Print an exception as the system would print it

def print_exception(xstr):
    cumm = xstr + " "
    a,b,c = sys.exc_info()
    if a != None:
        cumm += str(a) + " " + str(b) + "\n"
        try:
            #cumm += str(traceback.format_tb(c, 10))
            ttt = traceback.extract_tb(c)
            for aa in ttt:
                cumm += "File: " + os.path.basename(aa[0]) + \
                        " Line: " + str(aa[1]) + "\n" +  \
                    "   Context: " + aa[2] + " -> " + aa[3] + "\n"
        except:
            print "Could not print trace stack. ", sys.exc_info()
    print cumm

# ------------------------------------------------------------------------
# Never mind

def cmp(aa, bb):
    aaa = os.path.basename(aa);  bbb = os.path.basename(bb)
    pat = re.compile("[0-9]+")
    ss1 = pat.search(aaa)
    ss2 = pat.search(bbb)

    if(ss1 and ss2):
        aaaa = float(aaa[ss1.start(): ss1.end()])
        bbbb = float(bbb[ss2.start(): ss2.end()])
        #print aaa, bbb, aaaa, bbbb
        if aaaa == bbbb:
            return 0
        elif aaaa < bbbb:
            return -1
        elif aaaa > bbbb:
            return 1
        else:
            #print "crap"
            pass
    else:
        if aaa == bbb:
            return 0
        elif aaa < bbb:
            return -1
        elif aaa > bbb:
            return 1
        else:
            #print "crap"
            pass

# ------------------------------------------------------------------------
# Show a regular message:

def message(strx, title = None, icon = None):

    icon = Gtk.STOCK_INFO
    dialog = Gtk.MessageDialog(None, None,
                   Gtk.MessageType.INFO, Gtk.ButtonsType.CLOSE, strx)


    if title:
        dialog.set_title(title)
    else:
        dialog.set_title("ePub Reader")

    # Close dialog on user response
    dialog.connect("response", lambda d, r: d.destroy())
    dialog.show()

# -----------------------------------------------------------------------
# Sleep just a little, but allow the system to breed

def  usleep(msec):

    got_clock = time.clock() + float(msec) / 1000
    #print got_clock
    while True:
        if time.clock() > got_clock:
            break
        Gtk.main_iteration_do(False)

# -----------------------------------------------------------------------
# Call func with all processes, func called with stat as its argument
# Function may return True to stop iteration

def withps(func, opt = None):

    ret = False
    dl = os.listdir("/proc")
    for aa in dl:
        fname = "/proc/" + aa + "/stat"
        if os.path.isfile(fname):
            ff = open(fname, "r").read().split()
            ret = func(ff, opt)
        if ret:
            break
    return ret

# ------------------------------------------------------------------------
# Find

def find(self):

    head = "Find in text"

    dialog = Gtk.Dialog(head,
                   None,
                   Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                    Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
    dialog.set_default_response(Gtk.ResponseType.ACCEPT)

    try:
        dialog.set_icon_from_file("epub.png")
    except:
        print "Cannot load find dialog icon", sys.exc_info()

    self.dialog = dialog

    # Spacers
    label1 = Gtk.Label(label="   ");  label2 = Gtk.Label(label="   ")
    label3 = Gtk.Label(label="   ");  label4 = Gtk.Label(label="   ")
    label5 = Gtk.Label(label="   ");  label6 = Gtk.Label(label="   ")
    label7 = Gtk.Label(label="   ");  label8 = Gtk.Label(label="   ")

    warnings.simplefilter("ignore")
    entry = Gtk.Entry();
    warnings.simplefilter("default")
    entry.set_text(self.oldfind)

    entry.set_activates_default(True)

    dialog.vbox.pack_start(label4, True, True, 0)

    hbox2 = Gtk.HBox()
    hbox2.pack_start(label6, False)
    hbox2.pack_start(entry, True, True, 0)
    hbox2.pack_start(label7, False)

    dialog.vbox.pack_start(hbox2, True, True, 0)

    dialog.checkbox = Gtk.CheckButton("Search _Backwards")
    dialog.checkbox2 = Gtk.CheckButton("Case In_sensitive")
    dialog.vbox.pack_start(label5, True, True, 0)

    hbox = Gtk.HBox()
    #hbox.pack_start(label1, True, True, 0);  hbox.pack_start(dialog.checkbox, True, True, 0)
    #hbox.pack_start(label2, True, True, 0);  hbox.pack_start(dialog.checkbox2, True, True, 0)
    hbox.pack_start(label3, True, True, 0);
    dialog.vbox.pack_start(hbox, True, True, 0)
    dialog.vbox.pack_start(label8, True, True, 0)

    label32 = Gtk.Label(label="   ");  label33 = Gtk.Label(label="   ")
    label34 = Gtk.Label(label="   ");  label35 = Gtk.Label(label="   ")

    hbox4 = Gtk.HBox()

    hbox4.pack_start(label32, True, True, 0);
    dialog.vbox.pack_start(hbox4, True, True, 0)

    dialog.show_all()
    response = dialog.run()
    self.srctxt = entry.get_text()

    dialog.destroy()

    if response != Gtk.ResponseType.ACCEPT:
        return None

    return self.srctxt, dialog.checkbox.get_active(), \
                dialog.checkbox2.get_active()

# ------------------------------------------------------------------------
# Count lead spaces

def leadspace(strx):
    cnt = 0;
    for aa in range(len(strx)):
        bb = strx[aa]
        if bb == " ":
            cnt += 1
        elif bb == "\t":
            cnt += 1
        elif bb == "\r":
            cnt += 1
        elif bb == "\n":
            cnt += 1
        else:
            break
    return cnt


def message2(strx):

        dialog = Gtk.MessageDialog(None, None,
            Gtk.ButtonsType.NONE , Gtk.ButtonsType.CLOSE,
            'Message: \n\n%s' % (strx) )
        # Close dialog on user response
        dialog.connect ("response", lambda d, r: d.destroy())
        dialog.show()

# ------------------------------------------------------------------------
# Resolve path name

def respath(fname):

    try:
        ppp = string.split(os.environ['PATH'], os.pathsep)
        for aa in ppp:
            ttt = aa + os.sep + fname
            if os.path.isfile(str(ttt)):
                return ttt
    except:
        print ("Cannot resolve path", fname, sys.exc_info())
    return None

# ------------------------------------------------------------------------
# An N pixel vertical spacer. Default to 5.

class Spacer(Gtk.Label):

    def __init__(self, sp = 5):
        GObject.GObject.__init__(self)
        #sp *= 1000
        #self.set_markup("<span  size=\"" + str(sp) + "\"> </span>")
        self.set_text(" " * sp)

# ------------------------------------------------------------------------






