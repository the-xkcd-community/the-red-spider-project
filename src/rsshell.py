#! /usr/bin/env python

# Copyright 2012 Neil Forrester, Julian Gonggrijp
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

'''
Ideas for future changes (unordered):
 -  use the subprocess module instead of os.system;
 -  cd to RED_SPIDER_ROOT/work, mkdir if it doesn't exist;
 -  use the argparse module;
 -  move computation of environment variables to the setup script as
    well, store them in a JSON file in config and let rsshell retrieve
    them;
 -  show a short info message on launch (more than just the root and
    'call exit if you want your normal shell back').
'''

import os
from os.path import join, exists
import sys

def get_red_spider_root():
    red_spider_root = os.getenv('RED_SPIDER_ROOT')
    if not red_spider_root:
        print need_setup_msg
        sys.exit(1)
    return red_spider_root

def set_environment():
    rs_root = get_red_spider_root()
    bin_dir = join(rs_root, 'bin')
    lib_dir = join(rs_root, 'lib')
    env_prepend('PATH', bin_dir)
    env_prepend('PYTHONPATH', lib_dir)
    if os.name == 'nt':  # Windows
        env_append('PATHEXT', '.py')
    os.putenv('RED_SPIDER_ROOT', rs_root)
    print 'RED_SPIDER_ROOT =', rs_root

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

need_setup_msg = """
RED_SPIDER_ROOT has not been set. Go run the setup script first.
"""

if __name__ == "__main__":
    sys.exit(main(sys.argv))
