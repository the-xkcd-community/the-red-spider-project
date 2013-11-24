#! /usr/bin/env python

from __future__ import print_function

import os
import hashlib
import re
from urllib import urlopen

import time
import datetime
import argparse
import json
#~ import webbrowser
    
    
DEFAULTS_FILE = os.path.join(os.getenv("RED_SPIDER_ROOT"), "work", "geohash", "defaults")
URL_DOW = r"https://www.google.com/finance/historical?cid=983582&startdate={}&enddate={}"

def geohash(latitude, longitude, datedow):
    '''Compute geohash() using the Munroe algorithm.

    >>> geohash(37.421542, -122.085589, b'2005-05-26-10458.68')
    37.857713 -122.544543

    '''
    # http://xkcd.com/426/
    # adapted from antigravity.py
    h = hashlib.md5(datedow).hexdigest()
    p, q = [('%f' % float.fromhex('0.' + x)) for x in (h[:16], h[16:32])]
    return [float("{}{}".format(int(x), y[1:])) for x, y in ((latitude, p), (longitude, q))]

def parse_date(date):
    formats = ("%Y-%m-%d","%d-%m-%Y", "%m-%d-%Y")
    # deal with date delimiters
    datefract = re.findall("\d+|\w+", date)
    assert len(datefract) == 3
    check_date = "-".join(datefract)
    for check_format in formats:
        try:
            return time.strptime(check_date, check_format)
        except:
            pass
    else:
        raise ValueError("Invalid date format.")

def store_defaults(args, filepath):
    if not (os.path.exists(filepath) or os.path.isfile(filepath)):
        os.makedirs(os.path.split(filepath)[0])
    with open(filepath, "w") as fp:
        json.dump(args._get_kwargs(), fp)

def set_defaults(args, filepath):
    if os.path.exists(filepath) and os.path.isfile(filepath):
        with open(filepath, "r") as fp:
            defaults = json.load(fp)
        for key, value in defaults:
            if hasattr(args, key):
                if getattr(args, key) != value:
                    print("Default {} = {}".format(key, value , getattr(args, key)))
                    setattr(args, key, value)
        print()

def make_datedow(date, dow):
    date = time.strftime("%Y-%m-%d", date)
    if type(dow) is str or unicode:
        dow = float(dow)
    return "{}-{:.2f}".format(date, dow)

def get_date_of_dow(date, coords):
    date = datetime.date(*date[:3])
    if 0 > coords[1] > -30:
        date -= datetime.timedelta(days=1)
    wkday = date.weekday()
    if wkday > 4:
        date -= datetime.timedelta(wkday - 4)
    date = date.timetuple()
    return date

def get_dow(date):
    try:
        regex = '<td class="lm">.*{}.*{}\n<.+>(.+)'.format(date[2], date[0])
        regex = re.compile(regex)
        time_format = "%Y%m%d"
        enddate = datetime.date(*date[:3])
        startdate = enddate - datetime.timedelta(weeks=1)
        request = URL_DOW.format(*[x.strftime(time_format) for x in (startdate, enddate)])
        req = urlopen(request)
        page = req.read()
        req.close()
        dow = float(regex.search(page).groups()[0].replace(",", ""))
        return dow
    except:
        return

def get_location_coords(gen_location):
    #TODO implement location lookup
    return (37.421542, -122.085589)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a geohash based on the Munroe Algorithm.")
    parser.add_argument("-ll", dest="location", 
                        metavar=("LONGITUDE","LATITUDE"),nargs=2,
                        default=None, type=float)
    parser.add_argument("-l", dest="gen_location", metavar=("LOCATION"),
                        default=None)
    parser.add_argument("-t", dest="date", metavar=("DATE"), 
                        default=None)
    parser.add_argument("-d", dest="dow", metavar=("DOW"), 
                        default=None)
    parser.add_argument("-n", "--no-defaults", action="store_true")                    
    parser.add_argument("-s", "--store-defaults", action="store_true")

    args = parser.parse_args()
    maps = "https://maps.google.com/maps?q={:f},{:f}"
    
    if not args.no_defaults:
        set_defaults(args, DEFAULTS_FILE)
    
    if args.store_defaults:
        del args.store_defaults
        store_defaults(args, DEFAULTS_FILE)

    if not args.location:
        if args.gen_location:
            args.location = get_location_coords(args.gen_location)
        else:
            print("LONGITUDE, LATITUDE and LOCATION aren't set.")
    else:
        assert len(args.location) == 2
    
    date = parse_date(args.date) if args.date else time.localtime()
    date_of_dow = get_date_of_dow(date, args.location)
    datedow = None
    
    if not args.dow:
        print("Fetching DOW from the web..")
        args.dow = get_dow(date_of_dow)
    
    if args.dow:
        datedow = make_datedow(date_of_dow, args.dow)
    else:
        print("drats!")
    
    if args.location and datedow:
        print()
        print("Input: {}".format(datedow))
        unpack = args.location + [datedow]
        geo_location = geohash(*unpack)
        print("Output: {}, {}".format(*geo_location))
