#! /usr/bin/env python

# Copyright 2013 Wesley Aptekar-Cassels
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

import os, sys


documentedcmds = []

if len(sys.argv) == 1:
    print("The following commands are available in your version of The Red Spider Project:")
    for cmd in os.listdir(os.path.join(os.getenv("RED_SPIDER_ROOT"), "bin")):
        print(cmd)
else:
    try:
        docfile = open(os.path.join(os.getenv("RED_SPIDER_ROOT"), "config", "doc.txt"))
        for cmd in docfile.read().splitlines():
            documentedcmds.append(cmd.split(" ", 1))
    except:
        print("Hey you!\n\nI couldn't find the list of commands that I use to generate help files.  It's a shot in the dark, but the best that I can give you is this:")
        os.system(sys.argv[1] + " -h")  # This might be a bad idea if the user does "rshelp rshelp"...
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
            print("Hey you!\n\nI couldn't find any documentation for that command.  I looked in the /doc directory and did '" + sys.argv[1] + " -h', but they didn't help.\nrshelp can no longer help you, but if you master the spectral wolf, he will guide you.  Godspeed.") # http://xkcd.com/461/
