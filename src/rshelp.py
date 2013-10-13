#! /usr/bin/env python

# Copyright 2013 Wesley Aptekar-Cassels
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

import os

print("The following commands are available in your version of The Red Spider Project:")
for cmd in os.listdir(os.path.dirname(os.path.realpath(__file__))):
    print(cmd)
