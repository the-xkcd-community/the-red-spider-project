#! /usr/bin/env python

# Copyright 2013 Wesley Aptekar-Cassels
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

import os, sys

documentedcmds = [["xkcd-fetch", "xkcd-fetch -h"], ["xkcd-search", "xkcd-search -h"], ["level_up", "level_up -h"], ["summon", "summon"], ["fortune", "fortune -h"], ["godel", "godel"], ["random-number", "random-number -h"]] # I'm not sure if this is the best way to do this.  If you have a better idea, please fix it!

if len(sys.argv) == 1:
    print("The following commands are available in your version of The Red Spider Project:")
    for cmd in os.listdir(os.path.join(os.getenv("RED_SPIDER_ROOT"), "bin")):
        print(cmd)
else:
    documented = False
    for cmd in documentedcmds:
        if cmd[0] == sys.argv[1]:
            documented = True
            os.system(cmd[1])
    if not documented:
        try:
            manfile = open(os.path.join(os.getenv("RED_SPIDER_ROOT"), "doc",  sys.argv[1] + '.txt'), 'r')
            print(manfile.read())
        except FileNotFoundError:
            print("Hey you!\n\nI couldn't find any documentation for that command.  I looked in the /doc directory and did '" + sys.argv[1] + " -h', but they didn't help.\nrshelp can no longer help you, but if you master the spectral wolf, he will guide you.  Godspeed.") # http://xkcd.com/461/
