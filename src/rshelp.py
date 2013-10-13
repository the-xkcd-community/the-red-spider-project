#! /usr/bin/env python

import os

print("The following commands are available in your version of The Red Spider Project:")
for cmd in os.listdir(os.path.dirname(os.path.realpath(__file__))):
    print(cmd)
