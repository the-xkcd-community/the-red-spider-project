#! /usr/bin/env python

from __future__ import print_function

from sys import version_info, exit
import os
import hashlib
import re

import time
import datetime
import argparse
import json
import webbrowser
    

if version_info[0] == 3:
    from urllib.request import urlopen
    from urllib.parse import quote
    basestring = str
    raw_input = input
else:
    from urllib import urlopen, quote


class SomeChoice:
    def __init__(self, hint, *responses):
        self.validation = [hint] + list(responses)
        self.hint = hint

    def __call__(self, check):
        check = check.strip().lower()
        if check in self.validation:
            return self

YES = SomeChoice(
    "y", "ye", "yes", "aye", "affirmative", "roger", "okay", "kay", 
    "sure", "fine", "all right", "certainly", "definitely"
    )
NO = SomeChoice(
    "n", "no", "nope", "nay", "nah", "naw", "hell no", "no way",
    "negative", "absolutely not"
    )
    
GEO_ROOT = os.path.join(os.getenv("RED_SPIDER_ROOT"), "work", "geohash")
DEFAULTS_FILE = os.path.join(GEO_ROOT, "defaults")
CACHE_FILE = os.path.join(GEO_ROOT, "cache")
URL_DOW = r"https://www.google.com/finance/historical?cid=983582&startdate={}&enddate={}"
MAPS = "https://maps.google.com/maps?q={:f},{:f}"
MAPS_LOOKUP = "https://maps.google.com/maps?q={}"

def geohash(latitude, longitude, datedow):
    '''Compute geohash() using the Munroe algorithm.

    >>> geohash(37.421542, -122.085589, b'2005-05-26-10458.68')
    37.857713 -122.544543

    '''
    # http://xkcd.com/426/
    # adapted from antigravity.py
    datedow = datedow.encode("utf-8")
    h = hashlib.md5(datedow).hexdigest()
    p, q = [('%f' % float.fromhex('0.' + x)) for x in (h[:16], h[16:32])]
    return [float("{}{}".format(int(x), y[1:])) for x, y in ((latitude, p), (longitude, q))]

def memoize_to_disk(filename, invalid=set()):
    def decorator(func):
        try:
            with open(filename, "r") as fp:
                cache = json.load(fp)
        except (IOError, ValueError):
            cache = {}
            
        def memoize(*args):
            chk = str(args)
            if chk not in cache:
                ret = func(*args)
                if not ret in invalid:
                    cache[chk] = ret
                    with open(filename, "w") as fp:
                        json.dump(cache, fp)
                return ret
            else:
                return cache[chk]
        return memoize
    return decorator
    
def input_choice(prompt, gate=[YES, NO], timeout=4):
    prod = "/".join([x.hint for x in gate])
    prompt = prompt.format(prod)
    for i in range(timeout):
        inp = raw_input(prompt)
        choice = tuple(filter(None, [chk(inp) for chk in gate]))
        if choice:break
    else:
        print("\n???!")
    return choice[0] if len(choice) == 1 else None

def parse_date(date):
    formats = ("%x", "%Y-{m}-%d","%d-{m}-%Y", "{m}-%d-%Y")
    # deal with date delimiters
    datefract = re.findall("\d+|\w+", date)
    assert len(datefract) == 3
    check_date = "-".join(datefract)
    for check_format in formats:
        for month in {"%m", "%b", "%B"}:
            try:
                return time.strptime(check_date, check_format.format(m=month))
            except:
                pass
    else:
        raise ValueError("Invalid date format.")

def store_defaults(args, filepath):
    if not os.path.exists(os.path.split(filepath)[0]):
        os.makedirs(os.path.split(filepath)[0])
    with open(filepath, "w") as fp:
        json.dump(args.__dict__, fp)

def set_defaults(args, filepath):
    if os.path.exists(filepath) and os.path.isfile(filepath):
        with open(filepath, "r") as fp:
            defaults = json.load(fp)
        for key, value in defaults.items():
            if key in args.__dict__:
                chk = getattr(args, key)
                if not chk and chk != value:
                    print("Default {} = {}".format( key, value ))
                    setattr(args, key, value)
        print()

def make_datedow(date, dow):
    date = time.strftime("%Y-%m-%d", date)
    if isinstance(dow, basestring):
        dow = float(dow)
    return "{}-{:.2f}".format(date, dow)

def get_date_of_dow(date, coords):
    date = datetime.date(*date[:3])
    if 0 > coords[1] > -30:
        date -= datetime.timedelta(days=1)
    wkday = date.weekday()
    if wkday > 4:
        date -= datetime.timedelta(wkday - 4)
    date = tuple(date.timetuple())
    return date

@memoize_to_disk(CACHE_FILE, invalid={None,})
def get_dow(date):
    try:
        regex = '<td class="lm">.*{}.*{}\n<.+>(.+)'.format(date[2], date[0])
        regex = re.compile(regex)
        time_format = "%Y%m%d"
        enddate = datetime.date(*date[:3])
        startdate = enddate - datetime.timedelta(weeks=1)
        request = URL_DOW.format(*[x.strftime(time_format) for x in (startdate, enddate)])
        req = urlopen(request)
        page = req.read().decode("utf-8")
        req.close()
        dow = float(regex.search(page).groups()[0].replace(",", ""))
        return dow
    except:
        return

def get_location_coords(gen_location):
    re_coords = re.compile(r"\s*(\d+\.?\d*)\s+(\d+\.?\d*)\s*$")
    prompt = "Do you want to use google maps to get your coordinates? ({}): "
    response = input_choice(prompt)
    if response:
        if response is YES:
            webbrowser.open(MAPS_LOOKUP.format( quote(gen_location) ))
        prompt = "[q] to abort. Enter LATITUDE LONGITUDE: "
        while True:
            inp = raw_input(prompt)
            coords = re_coords.match(inp)
            if coords:
                return list(float(x) for x in coords.groups())
            if inp in {"q", "quit"}:
                return
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a geohash based on the Munroe Algorithm.")
    parser.add_argument("-ll", dest="location", 
                        metavar=("LATITUDE", "LONGITUDE"),nargs=2,
                        default=None, type=float)
    parser.add_argument("-l", dest="gen_location", metavar=("LOCATION"),
                        default="", nargs="+")
    parser.add_argument("-t", dest="date", metavar=("DATE"), 
                        default=None)
    parser.add_argument("-d", dest="dow", metavar=("DOW"), 
                        default=None)
    parser.add_argument("-n", "--no-defaults", action="store_true")                    
    parser.add_argument("-s", "--store-defaults", action="store_true")
    parser.add_argument("-cc", "--clear-cache", action="store_true")
    parser.add_argument("-m", "--maps", action="store_true")

    args = parser.parse_args()
    args.gen_location = " ".join(args.gen_location)
    
    if not os.path.exists(GEO_ROOT):
        os.makedirs(GEO_ROOT)
    
    if args.clear_cache:
        try:
            os.remove(CACHE_FILE)
        except OSError:
            pass
        exit()

    if args.no_defaults:
        del args.no_defaults
    else:
        set_defaults(args, DEFAULTS_FILE)
        
    if args.store_defaults:
        del args.store_defaults
        store_defaults(args, DEFAULTS_FILE)

    if not args.location:
        args.location = get_location_coords(args.gen_location)
    
    if args.location:
        assert len(args.location) == 2
        date = parse_date(args.date) if args.date else time.localtime()
        date_of_dow = get_date_of_dow(date, args.location)
        datedow = None
    
        if not args.dow:
            print("Fetching DOW from the web..")
            args.dow = get_dow(date_of_dow)
        
        if args.dow:
            datedow = make_datedow(date_of_dow, args.dow)
            
            print()
            print("Input: {}".format(datedow))
            unpack = args.location + [datedow]
            geo_location = geohash(*unpack)
            print("Output: {}, {}".format(*geo_location))
            if args.maps:
                webbrowser.open(MAPS.format(*geo_location))
        else:
            print("drats!")
    
