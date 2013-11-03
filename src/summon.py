#! /usr/bin/env python2
from __future__ import print_function

''' summon.py
A simple wrapper for OS-dependent file launchers.

Copyright 2013 Julian Gonggrijp
Licensed under the Red Spider Project License.
See the License.txt that shipped with your copy of this software for details.
'''

import sys
import subprocess

useshell = False
if sys.platform.startswith('win32'):
    summoning_command = ['start']
    useshell = True
elif sys.platform.startswith('darwin'):
    summoning_command = ['open']
else:  # linux assumed
    summoning_command = ['xdg-open']

def main (argv = None):
    if not argv:
        print(usage_msg)
    else:
        for filename in argv:
            subprocess.call(summoning_command + [filename], shell = useshell)

usage_msg = '''
Call me with a space-separated list of file paths and I'll summon
them for you.
'''

if __name__ == '__main__':
    main(sys.argv[1:])
