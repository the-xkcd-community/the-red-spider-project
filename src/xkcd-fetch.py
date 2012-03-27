#!/usr/bin/python

from urllib import urlretrieve
import re
import argparse
from time import sleep
import os
import sys
import codecs
import htmlentitydefs

def file_exists(filename):
	try:
		os.stat(filename)
		return True
	except OSError as ex:
		if ex.errno == 2:
			return False
		else:
			raise ex

def sleep_if_necessary():
	global first_cache_miss
	if not(first_cache_miss):
		sleep(args.sleep_time)
	first_cache_miss = False

def remove_escapes(string):
	def remove_one(match):
		ref = match.group(0)
		if ref[:2] == "&#":
			if ref[:3] == "&#x":
				return unichr(int(ref[3:-1], 16))
			else:
				return unichr(int(ref[2:-1]))
		else:
			ref = unichr(htmlentitydefs.name2codepoint[ref[1:-1]])
		return ref
	return re.sub("&#?\w+;", remove_one, string)

class Comic:
	def write_comic(self, lines):
		lines.append(repr(self.number))
		lines.append(self.comic_title)
		lines.append(self.image_name)
		lines.append(self.title_text)
		lines.append(self.date)
		lines.append('<transcript>')
		lines.append(self.transcript)
		lines.append('</transcript>')
		lines.append('')

def read_comic(lines):
	comic = Comic()
	comic.number = int(lines.pop(0))
	comic.comic_title = lines.pop(0).rstrip()
	comic.image_name = lines.pop(0).rstrip()
	comic.title_text = lines.pop(0).rstrip()
	comic.date = lines.pop(0).rstrip()
	assert '<transcript>' == lines.pop(0).rstrip()

	line = lines.pop(0).rstrip()
	comic.transcript = ''
	while line != '</transcript>':
		comic.transcript = comic.transcript + '\n' + line
		line = lines.pop(0).rstrip()
	comic.transcript = comic.transcript[1:] # strip the leading \n

	lines.pop(0)
	if file_exists(cache_path + '/' + comic.image_name):
		return comic
	else:
		return None

def download_comic(comics, comic_number):
	sleep_if_necessary()

	url = 'http://www.xkcd.com'
	url = url + '/' + repr(comic_number)

	scratch_filename = cache_path + '/raw.html'
	urlretrieve(url, scratch_filename)
	raw = codecs.open(scratch_filename, 'r', 'utf-8')
	raw_html = raw.read()
	raw.close()
	os.remove(scratch_filename)

	comic_line_match = re.search(comic_line, raw_html)
	permalink_line_match = re.search(permalink_line, raw_html)
	transcript_line_match = re.search(transcript_line, raw_html)

	if not(comic_line_match) or not(permalink_line_match):
		return None
	
	assert comic_number == int(permalink_line_match.group(1))

	comics[comic_number].image_name = comic_line_match.group(1)
	comics[comic_number].title_text = remove_escapes(comic_line_match.group(2))

	if transcript_line_match:
		comics[comic_number].transcript = remove_escapes(transcript_line_match.group(1))

	image_path = cache_path + '/' + comics[comic_number].image_name
	if not file_exists(image_path):
		urlretrieve('http://imgs.xkcd.com/comics/' + comics[comic_number].image_name, image_path)

	assert file_exists(image_path)

def read_cache():
	comic_data_file = codecs.open(comic_data_path, 'r', 'utf-8')
	comic_data_lines = comic_data_file.readlines()
	comic_data_file.close()

	comics = {}

	while len(comic_data_lines) > 0:
		comic = read_comic(comic_data_lines)
		if comic:
			comics[comic.number] = comic

	return comics

def write_cache(comics):
	comic_data_lines = []
	for num in sorted(comics.keys()):
		comics[num].write_comic(comic_data_lines)

	comic_data_file = codecs.open(comic_data_path, 'w', 'utf-8')
	for line in comic_data_lines:
		comic_data_file.write(line + '\n')
	comic_data_file.close()

def fetch(comics, comic_number):
	if comic_number == 0: # a comic number of 0 indicates the most recent comic
		download_archive(comics)
		comic_number = max(comics.keys())
	if not(comic_number in comics):
		download_archive(comics)
		if not(comic_number in comics):
			return None
	if comics[comic_number].image_name == '':
		download_comic(comics, comic_number)
	return comics[comic_number]

def download_archive(comics):
	sleep_if_necessary()

	url = 'http://www.xkcd.com/archive'

	scratch_filename = cache_path + '/raw.html'
	urlretrieve(url, scratch_filename)
	raw = codecs.open(scratch_filename, 'r', 'utf-8')
	raw_html = raw.read()
	raw.close()
	os.remove(scratch_filename)

	while True:
		archive_line_match = re.search(archive_line, raw_html)

		if not(archive_line_match):
			break

		num = int(archive_line_match.group(1))
		if not(num in comics.keys()):
			comics[num] = Comic()
			comics[num].number = num
			comics[num].date = archive_line_match.group(2)
			comics[num].comic_title = archive_line_match.group(3)
			comics[num].image_name = ''
			comics[num].title_text = ''
			comics[num].transcript = ''

		raw_html = raw_html[archive_line_match.end():]

parser = argparse.ArgumentParser(description = 'Downloads, caches, and returns xkcd comics')
parser.add_argument('-s', '--sleep-time',
                    metavar = 'TIME',
                    default = 1.0,
                    type = float,
                    help = 'Time (in seconds) to sleep between fetches in order to respect the server. Defaults to 1.0 seconds.')
parser.add_argument('comic_nums',
                    metavar = 'N',
                    type = int,
                    nargs = '*',
                    help = 'Comic number to download. Defaults to the most recent comic. Ignored if -a specified')

args = parser.parse_args()

work_path = '../work'
cache_path = work_path + '/xkcd-fetch'
comic_data_path = cache_path + '/comic-data.txt'

first_cache_miss = True

if not file_exists(work_path):
	os.mkdir(work_path)
if not file_exists(cache_path):
	os.mkdir(cache_path)
if not file_exists(comic_data_path):
	comic_data_file = codecs.open(comic_data_path, 'w', 'utf-8')
	comic_data_file.write('')
	comic_data_file.close()

comic_line = re.compile('^[^\n]*<img src="http://imgs\.xkcd\.com/comics/(\S*)" title="([^\n]*)" alt="([^\n]*)" />[^\n]*$', re.MULTILINE);
permalink_line = re.compile('^[^\n]*<h3>Permanent link to this comic: http://xkcd\.com/(\d+)/</h3>[^\n]*$', re.MULTILINE);
transcript_line = re.compile('^[^\n]*<div id="transcript" style="display: none">(.*?)</div>[^\n]*$', re.MULTILINE | re.DOTALL);
archive_line = re.compile('^[^\n]*<a href="/(\d+)/" title="(\d{4,4}-\d{1,2}-\d{1,2})">([^\n]*)</a><br/>[^\n]*$', re.MULTILINE);

comics = read_cache()

if len(args.comic_nums) > 0:
	fetch(comics, args.comic_nums[0])
	for num in args.comic_nums[1:]:
		fetch(comics, num)
else:
	fetch(comics, 0) # a comic number of 0 indicates the most recent comic

write_cache(comics)
