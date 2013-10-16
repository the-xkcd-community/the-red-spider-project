#! /usr/bin/env python

# Copyright 2013 Wesley Aptekar-Cassels
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

import os, sys


documentedcmds = []

if len(sys.argv) == 1:
    print("The following commands are available in your version of The Red Spider Project:")
    for cmd in os.listdir(os.path.join(os.getenv("RED_SPIDER_ROOT"), "bin")):
        if not os.name == 'nt': # POSIX Assumed.
            print(cmd)
        else:
            print(cmd.split(".")[0]) # Assuming you won't have commands like "__AUTOEXEC.BAT.MY%20OSX%20DOCUMENTS-INSTALL.EXE.RAR.INI.TAR.DOÇX.PHPHPHP.XHTML.TML.XTL.TXXT.0DAY.HACK.ERS_(1995)_BLURAY_CAM-XVID.EXE.TAR.[SCR].LISP.MSI.LNK.ZDA.GNN.WRBT.OBJ.O.H.SWF.DPKG.APP.ZIP.TAR.TAR.CO.GZ.A.OUT.EXE", this should work.
else:
    backuphelp = False
    try:
        docfile = open(os.path.join(os.getenv("RED_SPIDER_ROOT"), "config", "doc.txt"))
        for cmd in docfile.read().splitlines():
            documentedcmds.append(cmd.split(" ", 1))
    except:
        backuphelp = True
    documented = False
    try:
        manfile = open(os.path.join(os.getenv("RED_SPIDER_ROOT"), "doc", sys.argv[1] + ".txt"), 'r')
        print(manfile.read())
    except FileNotFoundError:
        for cmd in documentedcmds:
            if cmd[0] == sys.argv[1]:
                documented = True
                os.system(cmd[1])
        if not documented:
            if not backuphelp:
                print("Hey you!\n\nI couldn't find any documentation for that command.  I looked in the /doc directory and did '" + sys.argv[1] + " -h', but they didn't help.\nrshelp can no longer help you, but if you master the spectral wolf, he will guide you.  Godspeed.") # http://xkcd.com/461/
            else:
                print("Hey you!\n\nI couldn't find the list of commands that I use to generate help files.  It's a shot in the dark, but the best that I can give you is this:")
                os.system(sys.argv[1] + " -h")
                
