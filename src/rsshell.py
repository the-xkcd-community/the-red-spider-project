#!/usr/bin/python

# Copyright 2012 Neil Forrester
# See License.txt

import os
import sys
import rscall

if __name__ == "__main__":
	rscall.set_red_spider_root()
	os.system(os.getenv('SHELL', 'bash'))
