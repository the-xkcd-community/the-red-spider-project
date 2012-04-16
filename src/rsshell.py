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
 -  show a short info message on launch.
'''

import os
import sys

def find_red_spider_root():
    this_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    parent, subdir = os.path.split(this_path)
    if subdir == 'bin' or subdir == 'src':
        return parent
    else:
        return this_path

red_spider_root = find_red_spider_root()

def set_red_spider_root():
	global red_spider_root
	if os.name == 'nt':  # Windows
	    config_path = os.getenv('APPDATA') + '\\xkcdRedSpider\\config.txt'
	else:                # POSIX assumed
	    config_path = os.getenv('HOME') + '/.config/xkcdRedSpider'
	config_path = os.path.normpath(config_path)
	if os.path.exists(config_path):
	    config = open(config_path)
	    red_spider_root = config.readline()
	    config.close()
	os.putenv('RED_SPIDER_ROOT', red_spider_root)
	print('RED_SPIDER_ROOT =', red_spider_root)

def main (argv = None):
    set_red_spider_root()
    if argv and len(argv) > 1:                  # call the requested program
        return os.system(" ".join(argv[1:]))
    if os.name == 'nt':                         # Windows
        return os.system(os.getenv('COMSPEC', 'cmd.exe'))
    else:                                       # POSIX assumed
        return os.system(os.getenv('SHELL', 'bash'))

if __name__ == "__main__":
	sys.exit(main(sys.argv))
