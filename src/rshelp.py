#! /usr/bin/env python

# Copyright 2013 Wesley Aptekar-Cassels
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

import os, sys

if len(sys.argv) == 1:
    print("The following commands are available in your version of The Red Spider Project:")
    for cmd in os.listdir(os.path.join(os.getenv("RED_SPIDER_ROOT"), "bin")):
        print(cmd)
else:
    manfile = open(os.path.join(os.getenv("RED_SPIDER_ROOT"), "doc",  sys.argv[1] + '.txt'), 'r')
    print(manfile.read())
