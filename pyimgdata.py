#!/usr/bin/env python

# ------------------------------------------------------------------------
# Voice recognition

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, binascii

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from pgutil import  *
from mainwin import  *

# ------------------------------------------------------------------------
# Globals

version = "0.00"

# ------------------------------------------------------------------------

def phelp():

    print
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options] [filename]"
    print
    print "Options:    -d level  - Debug level 0-10"
    print "            -p        - Port to use (default: 9999)"
    print "            -r        - Randomize"
    print "            -v        - Verbose"
    print "            -V        - Version"
    print "            -q        - Quiet"
    print "            -h        - Help"
    print
    sys.exit(0)

# ------------------------------------------------------------------------
def pversion():
    print os.path.basename(sys.argv[0]), "Version", version
    sys.exit(0)

    # option, var_name, initial_val, function
optarr = \
    ["d:",  "pgdebug",  0,      None],      \
    ["p:",  "port",     9999,   None],      \
    ["v",   "verbose",  0,      None],      \
    ["r",   "randx",    0,      None],      \
    ["q",   "quiet",    0,      None],      \
    ["t",   "test",     "x",    None],      \
    ["V",   None,       None,   pversion],  \
    ["h",   None,       None,   phelp]      \

conf = Config(optarr)

if __name__ == '__main__':

    global mw
    args = conf.comline(sys.argv[1:])

    strz = string.letters + string.digits # + string.punctuation

    strx = ""
    if conf.randx:
        for aa in range(124):
            idx = int(random.random() * len(strz))
            strx += strz[idx]
    else:
        if len(args) == 0:
            print("Usage: pyimgdata filename")
            sys.exit(0)
        fp = open(args[0], "r")
        strx = fp.read()
        fp.close()

    mw = MainWin(strx)
    Gtk.main()

    sys.exit(0)

# EOF
