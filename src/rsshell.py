#! /usr/bin/env python2

# Copyright 2012, 2013 Neil Forrester, Julian Gonggrijp
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

'''
Ideas for future changes (unordered):
 -  use the argparse module;
 -  move computation of environment variables to the setup script as
    well, store them in a JSON file in config and let rsshell retrieve
    them.
'''

import os
from os.path import join, exists
import sys
from subprocess import call

def get_red_spider_root():
    red_spider_root = os.getenv('RED_SPIDER_ROOT')
    if not red_spider_root:
        print need_setup_msg
        sys.exit(1)
    return red_spider_root

def set_environment (rs_root):
    bin_dir = join(rs_root, 'bin')
    lib_dir = join(rs_root, 'lib')
    env_prepend('PATH', bin_dir)
    env_prepend('PYTHONPATH', lib_dir)
    if os.name == 'nt':  # Windows
        env_append('PATHEXT', '.py')
    os.putenv('RED_SPIDER_ROOT', rs_root)

def env_prepend (varname, addition):
    os.putenv(varname, os.pathsep.join([addition, os.getenv(varname, '')]))

def env_append (varname, addition):
    os.putenv(varname, os.pathsep.join([os.getenv(varname, ''), addition]))

def main (argv = None):
    root = get_red_spider_root()
    set_environment(root)
    if argv and len(argv) > 1:                  # call the requested program
        result = call('"' + '" "'.join(argv[1:]) + '"', shell = True)
    else:
        prior_location = os.getcwd()
        os.chdir(root)
        print welcome_msg.format(root, os.path.sep, *variable_wrap)
        if os.name == 'nt':                     # Windows
            result = call(os.getenv('COMSPEC', 'cmd.exe'))
        else:                                   # POSIX assumed
            result = call(os.getenv('SHELL', 'bash'))
        os.chdir(prior_location)
    return result

welcome_msg = """
Welcome to the Red Spider shell, your portal into the world of the
Red Spider Project.

RED_SPIDER_ROOT = {0}

You have been teleported there. When you exit the Red Spider shell
you'll be delivered back to your prior location. Call "exit" to make
that happen.
"""

variable_wrap = ('%', '%') if os.name == 'nt' else ('$', '')

need_setup_msg = """
RED_SPIDER_ROOT has not been set. Go run the setup script first.
"""

if __name__ == "__main__":
    sys.exit(main(sys.argv))
