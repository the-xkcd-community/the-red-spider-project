#! /usr/bin/env python

# Copyright 2012 Neil Forrester, Julian Gonggrijp
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

'''
Ideas for future changes (unordered):
 -  use the subprocess module instead of os.system;
 -  add variables like PATH and PYTHONPATH;
 -  use the PATHEXT variable on windows (strip off the file extension on POSIX);
 -  cd to RED_SPIDER_ROOT/work, mkdir if it doesn't exist;
 -  drop rscall, since rsshell can already mimic its behaviour;
 -  show a short info message on launch.
'''

import os
import sys
import rscall

def main (argv = None):
    rscall.set_red_spider_root()
    if argv and len(argv) > 1:                  # behave like rscall
        return os.system(" ".join(argv[1:]))
    if os.name == 'nt':                         # Windows
        return os.system(os.getenv('COMSPEC', 'cmd.exe'))
    else:                                       # POSIX assumed
        return os.system(os.getenv('SHELL', 'bash'))

if __name__ == "__main__":
	sys.exit(main(sys.argv))
