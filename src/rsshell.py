#! /usr/bin/env python2

# Copyright 2012 Neil Forrester, Julian Gonggrijp
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

'''
Ideas for future changes (unordered):
 -  use the subprocess module instead of os.system;
 -  cd to RED_SPIDER_ROOT/work, mkdir if it doesn't exist;
 -  move find_red_spider_root to setup.py and make rsshell fully depend
    on the config file;
 -  show a short info message on launch (more than just the root and
    'call exit if you want your normal shell back').
'''

import os
from os.path import join, exists
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
	if exists(config_path):  # most reliable way to find the root
	    config = open(config_path)
	    red_spider_root = config.readline()
	    config.close()
	os.putenv('RED_SPIDER_ROOT', red_spider_root)
	print 'RED_SPIDER_ROOT =', red_spider_root

def set_environment():
    set_red_spider_root()
    bin_dir = join(red_spider_root, 'bin')
    lib_dir = join(red_spider_root, 'lib')
    env_prepend('PATH', bin_dir)
    env_prepend('PYTHONPATH', lib_dir)
    if os.name == 'nt':  # Windows
        env_append('PATHEXT', '.py')

def env_prepend (varname, addition):
    os.putenv(varname, os.pathsep.join([addition, os.getenv(varname, '')]))

def env_append (varname, addition):
    os.putenv(varname, os.pathsep.join([os.getenv(varname, ''), addition]))

def main (argv = None):
    set_environment()
    if argv and len(argv) > 1:                  # call the requested program
        return os.system(" ".join(argv[1:]))
    print 'Call "exit" if you want to return to your normal shell'
    if os.name == 'nt':                         # Windows
        return os.system(os.getenv('COMSPEC', 'cmd.exe'))
    else:                                       # POSIX assumed
        return os.system(os.getenv('SHELL', 'bash'))

if __name__ == "__main__":
	sys.exit(main(sys.argv))
