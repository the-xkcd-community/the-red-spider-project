#!/usr/bin/python

# Copyright 2012 Neil Forrester
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.


import re
import argparse
import os
import sys
import codecs
xf = __import__('xkcd-fetch')

if __name__ == "__main__":
	# set up command line arguments
	parser = argparse.ArgumentParser(description = 'Searches cached xkcd comics, will not download new ones.')
	parser.add_argument('regex',
	                    metavar = 'REGEX',
	                    help = 'A python regular expression')
	args = parser.parse_args()

	# if files don't exist, exit
	if not os.path.exists(xf.comic_data_path):
		sys.stderr.write("No comic data found.\n" +
		                 "Is RED_SPIDER_ROOT set?\n" +
		                 "Have you run xkcd-fetch yet?\n")
		sys.exit(1)

	regex = re.compile(args.regex)

	# read the cache from the file
	comics = xf.read_cache()

	# search the comics
	for num in comics.keys():
		if any(map(regex.search, [comics[num].comic_title,
		                          comics[num].title_text,
		                          comics[num].transcript,
		                          comics[num].news])):
			print num
