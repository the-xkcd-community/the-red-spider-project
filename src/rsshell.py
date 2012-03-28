#!/usr/bin/python

# Copyright 2012 Neil Forrester
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

import os
import sys
import rscall

if __name__ == "__main__":
	rscall.set_red_spider_root()
	os.system(os.getenv('SHELL', 'bash'))
