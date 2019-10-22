#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os, sys, getopt, signal, string
import random, time, subprocess

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

import doodle

from pgutil import  *

class MainWin():

    def __init__(self, strx = ""):

        self.sssmod = None
        self.window = window = Gtk.Window(Gtk.WindowType.TOPLEVEL)

        self.area = doodle.doodle(strx)

        #area.ct()
        #super(doodle.doodle, area).ct()

        #os.chdir( os.path.dirname(os.getcwd()) )

        window.set_title("pyimgenc UI")
        window.set_position(Gtk.WindowPosition.CENTER)

        #ic = Gtk.Image(); ic.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.BUTTON)
        #window.set_icon(ic.get_pixbuf())

        www = Gdk.Screen.width(); hhh = Gdk.Screen.height();
        #window.set_default_size(6*www/8, 6*hhh/8)
        window.set_default_size(1000, 800)

        #window.set_flags(Gtk.CAN_FOCUS | Gtk.SENSITIVE)

        window.set_events(  Gdk.EventMask.POINTER_MOTION_MASK |
                            Gdk.EventMask.POINTER_MOTION_HINT_MASK |
                            Gdk.EventMask.BUTTON_PRESS_MASK |
                            Gdk.EventMask.BUTTON_RELEASE_MASK |
                            Gdk.EventMask.KEY_PRESS_MASK |
                            Gdk.EventMask.KEY_RELEASE_MASK |
                            Gdk.EventMask.FOCUS_CHANGE_MASK )

        window.connect("destroy", self.OnExit)
        window.connect("key-press-event", self.key_press_event)
        window.connect("button-press-event", self.button_press_event)

        try:
            window.set_icon_from_file("icon.png")
        except:
            pass

        vbox = Gtk.VBox();
        sp33 = Spacer(1)
        vbox.pack_start(sp33, 0, 0, 0)

        hbox = Gtk.HBox();  hbox2 = Gtk.HBox(); hbox3 = Gtk.VBox();

        sp1 = Spacer(1)
        hbox2.pack_start(sp1, 0, 0, False)
        lab3 = Gtk.Label(label="  Enter PassWord: ");
        sp11 = Spacer(1)
        hbox2.pack_start(sp11, 0, 0, False)
        hbox2.pack_start(lab3, 0, 0, False)
        self.entry = Gtk.Entry(); self.entry.set_visibility(False)
        sp12 = Spacer(1)
        hbox2.pack_start(sp12, 0, 0, False)
        hbox2.pack_start(self.entry, 0, 0, 0)

        sp13 = Spacer(1)
        hbox2.pack_start(sp13, 0, 0, False)
        butt3 = Gtk.Button.new_with_mnemonic(" _Reveal ")
        butt3.connect("clicked", self.reveal, window)
        hbox2.pack_start(butt3, 0, 0, False)

        hbox2.pack_start(Spacer(1), 0, 0, False)
        butt3f = Gtk.Button.new_with_mnemonic(" Load _File ")
        butt3f.connect("clicked", self.load, window, 0)
        hbox2.pack_start(butt3f, 0, 0, False)

        sp2 = Spacer(1)
        hbox2.pack_start(sp2, 0, 0, False)
        butt3e = Gtk.Button.new_with_mnemonic(" _Encode ")
        butt3e.connect("clicked", self.encode, window)
        hbox2.pack_start(butt3e, 0, 0, False)

        sp21 = Spacer(1)
        hbox2.pack_start(sp21, 0, 0, False)
        butt3e = Gtk.Button.new_with_mnemonic(" _Decode ")
        butt3e.connect("clicked", self.decode, window)
        hbox2.pack_start(butt3e, 0, 0, False)

        sp21 = Spacer(1)
        hbox2.pack_start(sp21, 0, 0, False)
        butt3e = Gtk.Button.new_with_mnemonic(" _Pollute ")
        butt3e.connect("clicked", self.pollute, window)
        hbox2.pack_start(butt3e, 0, 0, False)

        sp3 = Spacer(1)
        hbox2.pack_start(sp3, 0, 0, False)
        butt2 = Gtk.Button.new_with_mnemonic(" E_xit ")
        butt2.connect("clicked", self.OnExit, window)
        hbox2.pack_start(butt2, 1, 1, True)

        lab4 = Gtk.Label(label="  ");   hbox2.pack_start(lab4, 0,0, False)

        sc1 = Gtk.ScrolledWindow()
        self.text1 = Gtk.TextView();    self.text1.set_wrap_mode(True)
        sc1.add_with_viewport(self.text1)

        hbox5a = Gtk.HBox(); hbox5a.set_spacing(2)
        hbox5a.pack_start(sc1, True, True, True)

        hbox3.pack_start(hbox5a, 0, 0, 0)
        hbox3.pack_start(self.area, True, True, padding = 2)

        lab1 = Gtk.Label(label="");  hbox.pack_start(lab1, True, True, 0)
        lab2 = Gtk.Label(label="");  hbox.pack_start(lab2, True, True, 0)

        vbox.pack_start(sp1, 0,0, False)
        vbox.pack_start(hbox2, 0,0, False)
        sp34 = Spacer(1)
        vbox.pack_start(sp34, 0, 0, 0)

        vbox.pack_start(hbox3, True, True, 0)

        window.add(vbox)
        window.show_all()

    def buttcol(self, idx):

        hbox5v = Gtk.VBox(); hbox5v.set_spacing(2)
        return hbox5v

        window = self.window

        hbox5v.pack_start(Spacer(), True, True, True)
        butt5 = Gtk.Button.new_with_mnemonic(" Load ")
        butt5.connect("clicked", self.load, window, idx)
        hbox5v.pack_start(butt5, 0, 0, 0)

        butt5a = Gtk.Button.new_with_mnemonic(" Copy ")
        butt5a.connect("clicked", self.paste, window, idx)
        hbox5v.pack_start(butt5a, 0, 0, 0)

        butt5b = Gtk.Button.new_with_mnemonic(" Paste ")
        butt5b.connect("clicked", self.copy, window, idx)
        hbox5v.pack_start(butt5b, 0, 0, 0)

        butt5c = Gtk.Button.new_with_mnemonic(" SelAll ")
        butt5c.connect("clicked", self.paste,idx, window, idx)
        hbox5v.pack_start(butt5c, 0, 0, 0)
        hbox5v.pack_start(Spacer(), True, True, True)

        return hbox5v

    def reveal(self, arg1, arg2):
        self.entry.set_visibility(not self.entry.get_visibility())

    # --------------------------------------------------------------------

    def copy(self, win, butt, idx):
        #print("Copy clip")
        clip = Gtk.Clipboard.get_default(Gdk.Display().get_default())
        self.text2.get_buffer().copy_clipboard(clip)

    def paste(self, win, butt, idx):
        clip = Gtk.Clipboard.get_default(Gdk.Display().get_default())
        self.text1.get_buffer().paste_clipboard(clip, None, True)

    # --------------------------------------------------------------------

    def encode(self, win, butt):
        #print ("encode", self.orig)
        ppp = self.entry.get_text()
        if len(ppp) == 0:
            message("Cannot have an empty password.")
            return

        #self.newpass = spemod.genpass(ppp)

        try:
            #if not self.sssmod:
                #self.sssmod =  spemod.spellencode("data/spell.txt")
            pass
        except:
            print ("Cannot load encodeion.")
            raise ValueError("Cannot load dictionary.")

        pppx = []; arrx = []

        buff =  self.text1.get_buffer()
        for ccc in range(buff.get_line_count()):
            iter = buff.get_iter_at_line(ccc)
            iter2 = buff.get_iter_at_line(ccc+1)
            aa = buff.get_text(iter, iter2, False)
            #print ("buff", , "eee")

            #ss = spemod.ascsplit(aa.strip())
            for cc in ss:
                #print("cc=", ("'"+cc+"'", end=" ")
                arrx.append(cc)
            arrx.append("\n")

        self.encr = self.sssmod.enc_dec(True, arrx, self.newpass)

        self.text2.get_buffer().set_text(self.encr)

    def pollute(self, win, butt):
        self.area.pollute()

    def decode(self, win, butt):
        self.area.decode()

    def decrypt(self, win, butt):
        #print ("encode", self.orig)

        #ppp = self.entry.get_text()
        #if len(ppp) == 0:
        #    message("Cannot have an empty password.")
        #    return
        ##self.newpass = spemod.genpass(ppp)

        try:
            if not self.sssmod:
                self.sssmod =  spemod.spellencode("../data/spell.txt")
        except:
            print ("Cannot load encodeion.")
            raise ValueError("Cannot load dictionary.")

        pppx = []; arrx = []

        buff =  self.text2.get_buffer()
        for ccc in range(buff.get_line_count()):
            iter = buff.get_iter_at_line(ccc)
            iter2 = buff.get_iter_at_line(ccc+1)
            aa = buff.get_text(iter, iter2, False)
            #print ("buff", , "eee")

            ss = spemod.ascsplit(aa.strip())
            for cc in ss:
                #print("cc=", ("'"+cc+"'", end=" ")
                arrx.append(cc)
            arrx.append("\n")

        self.encr = self.sssmod.enc_dec(False, arrx, self.newpass)

        self.text3.get_buffer().set_text(self.encr)

    # --------------------------------------------------------------------

    def     done_mac_open_fc(self, win, resp, old):

        #print  ("done_mac_fc", resp)

        # Back to original dir
        #os.chdir(os.path.dirname(old))

        if resp == Gtk.ButtonsType.OK:
            try:
                fname = win.get_filename()
                if not fname:
                    print("Must have filename")
                else:
                    fh = open(fname, "rb")
                    self.orig = fh.read()
                    fh.close()
                    self.text1.get_buffer().set_text(self.orig)

            except:
                print("Cannot load file", sys.exc_info())
        win.destroy()

    def load(self, win, butt, idx):
        #print("Loading file:")

        old = os.getcwd()
        but =   "Cancel", Gtk.ButtonsType.CANCEL, "Load Macro", Gtk.ButtonsType.OK
        fc = Gtk.FileChooserDialog("Load file for encodeion:", None, Gtk.FileChooserAction.OPEN, \
            but)
        #fc.set_current_folder(xfile)
        fc.set_current_folder(old)
        fc.set_default_response(Gtk.ButtonsType.OK)
        fc.connect("response", self.done_mac_open_fc, old)
        fc.run()

    def lookup(self):

        try:
            prog = respath("wn")
            pppx = [prog]
            pppx.append(self.entry.get_text())
            pppx.append("-over")
            out = subprocess.Popen(pppx, stdout=subprocess.PIPE).communicate()[0]
            if out == "":
                self.text1.get_buffer().set_text("No entry or incorrenct spelling")
            else:
                self.text1.get_buffer().set_text(out)

            out = ""
            for aa in "nvar":
                out += "(" + aa + ") "
                pppx = [prog]
                pppx.append(self.entry.get_text())
                pppx.append("-syns" + aa)
                out += subprocess.Popen(pppx, stdout=subprocess.PIPE).communicate()[0]
            self.text2.get_buffer().set_text(out)

            out = ""
            for aa in "nvar":
                out += "(" + aa + ") "
                pppx = [prog]
                pppx.append(self.entry.get_text())
                pppx.append("-ants" + aa)
                out += subprocess.Popen(pppx, stdout=subprocess.PIPE).communicate()[0]
            self.text3.get_buffer().set_text(out)

            out = ""
            for aa in "coorn", "coorv", "hypon", "hypov", "derin", "deriv", \
                    "meron", "holon", "perta", "attrn":
                pppx = [prog]
                pppx.append(self.entry.get_text())
                pppx.append("-" + aa)
                res = subprocess.Popen(pppx, stdout=subprocess.PIPE).communicate()[0]
                if res != "":
                    out += "----------------------------------------------------------- "
                    out += res

            self.text4.get_buffer().set_text(out)

        except:
            print ("Cannot execute", pppx, sys.exc_info())
            self.text1.get_buffer().set_text("Cannot execute 'wn', please install it.")

        self.entry.grab_focus()

    def  OnExit(self, arg, srg2 = None):
        self.exit_all()

    def exit_all(self):
        Gtk.main_quit()

    def key_press_event(self, win, event):
        #print ("key_press_event", win, event)
        pass

    def button_press_event(self, win, event):
        #print ("button_press_event", win, event)
        pass

# Start of program:

if __name__ == '__main__':

    mainwin = MainWin()
    Gtk.main()




