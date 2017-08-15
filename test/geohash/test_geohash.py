#! /usr/bin/env python

from __future__ import print_function

import sys, os
import time
from shutil import rmtree
from io import BytesIO

import unittest
from argparse import Namespace
from random import choice, randint, seed
from functools import partial
from datetime import timedelta
from calendar import monthrange
import json

testdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../src')))

import geohash
from geohash import Date

geohash.set_root(os.path.join(testdir, "work", "geohash"))

if sys.version_info[0] == 3:
    basestring = str
    from io import StringIO
    import urllib
    from urllib.parse import urlparse
    from urllib import request
else:
    from cStringIO import StringIO
    import urllib2 as urllib
    request = urllib
    from urlparse import urlparse
    
data = {
      "2008-05-28": {
        "hash_str": "2008-05-28-12542.90", 
        "coord_1": (68.68745, -30.21221), 
        "coord_2": (68.71044, -29.11273), 
        "djia": 12542.90, 
        "glob_hash_str": "2008-05-28-12479.63", 
        "glob_hash": (37.87947, -139.41640), 
        "hash_str_30w": "2008-05-28-12479.63"
      }, 
      "2008-05-27": {
        "hash_str": "2008-05-27-12479.63", 
        "coord_1": (68.20968, -30.10144), 
        "coord_2": (68.12537, -29.57711), 
        "djia": 12479.63, 
        "glob_hash_str": "2008-05-27-12620.90", 
        "glob_hash": (-67.43391, 27.75993), 
        "hash_str_30w": "2008-05-27-12620.90"
      }, 
      "2008-05-26": {
        "hash_str": "2008-05-26-12620.90", 
        "coord_1": (68.67313, -30.60731), 
        "coord_2": (68.67313, -29.60731), 
        "djia": 12620.9, 
        "glob_hash_str": "2008-05-26-12620.90", 
        "glob_hash": (31.16306, 38.63088), 
        "hash_str_30w": "2008-05-26-12620.90"
      }, 
      "2008-05-20": {
        "hash_str": "2008-05-20-13026.04", 
        "coord_1": (68.63099, -30.61895), 
        "coord_2": (68.63099, -29.61895), 
        "djia": 13026.04, 
        "glob_hash_str": "2008-05-20-12985.41", 
        "glob_hash": (-46.71388, -135.48197), 
        "hash_str_30w": "2008-05-20-13026.04"
      }, 
      "2012-02-26": {
        "hash_str": "2012-02-26-12981.20", 
        "coord_1": (68.000047, -30.483719), 
        "coord_2": (68.000047, -29.483719), 
        "djia": 12981.2, 
        "glob_hash_str": "2012-02-26-12981.20", 
        "glob_hash": (-89.99161, -5.86128), 
        "hash_str_30w": "2012-02-26-12981.20"
        }
    }

class TestHandler(request.HTTPHandler, request.HTTPSHandler):
    url_target = urlparse(geohash.URL_DOW).netloc
    def http_open(self, req):
        fract = urlparse(req.get_full_url())
        if self.url_target == fract.netloc:
            date = "-".join(tuple(filter(None, fract.path.split('/')))[-3:])
            if date in data:
                resp = request.addinfourl(BytesIO(str(data[date]["djia"]).encode('utf-8')), "msg", req.get_full_url())
                resp.code = 200
                resp.msg = "OK"
            else:
                resp = request.addinfourl(BytesIO("error\ndata not available yet".encode('utf-8')), "msg", req.get_full_url())
                resp.code = 404
                resp.msg = "Not Found"
        else:
            raise NotImplementedError
        return resp
    https_open = http_open 

test_opener = request.build_opener(TestHandler)
request.install_opener(test_opener)

def make_Date(date_str):
    return Date(*(int(x) for x in date_str.split('-')[:3]))

class TestGeohashFunctions(unittest.TestCase):
    def setUp(self):
        try:
            rmtree(geohash.GEO_ROOT)
        except OSError:
            pass

    tearDown = setUp

    def test_parse_date(self):
        formats = (
                    '%Y-{m}-%d',
                    '%d-{m}-%Y',
                    '%b-%d-%Y', '%B-%d-%Y',
                    '%d-{m}',
                    '%b-%d','%B-%d',
                    '%d'
        )
        def gen_year(y, *args, **kwargs):
            return reduce(lambda x,y:x + y, map(partial(gen_month, y), range(1, 12)) )

        def gen_month(y, m, *args, **kwargs):
            date = Date(y, m, 1)
            ret = list()
            while date.month == m:
                ret.extend(gen_cases(date, *args, **kwargs))
                date = timedelta(1) + date
            return ret
            
        def gen_cases(date, sep="-"):
            date_t = date.timetuple()
            months = {"%m", "%b", "%B"}
            gen_date = lambda f:Date(date_t[0] if '%Y' in f else cur.year, date_t[1] if any(m in f for m in {"%m", "%b", "%B", "{m}"}) else cur.month, date_t[2])
            return [(gen_date(f), time.strftime(f.format(m=m), date_t).replace("-", sep), f) for m in months for f in formats]

        cur = Date(*time.localtime()[:3])
        test_cases = gen_month(2005, 5)
        for chk, date, f in test_cases:
            ret = geohash.parse_date(date)
            self.assertEqual(chk, ret)

    def test_geohash(self):
        precision = 0.0001
        def compare(l1, l2):
            return all(abs(x-y) < precision for x, y in zip(l1, l2))

        for key, val in data.items():
            ret = geohash.geohash(68, -30, val['hash_str'])
            ret_30w = geohash.geohash(68, -29, val['hash_str_30w'])
            self.assertTrue(compare(ret, val['coord_1']))
            self.assertTrue(compare(ret_30w, val['coord_2']))

    def test_globalhash(self):
        precision = 0.001
        def compare(l1, l2):
            return all(abs(x-y) < precision for x, y in zip(l1, l2))

        for key, val in data.items():
            ret = geohash.globalhash(val['glob_hash_str'])
            self.assertTrue(compare(ret, val['glob_hash']))

    def test_get_dow(self):
        def rng_date(year=None, month=None, day=None):
            year = choice(year if year else range(1990, 2100))
            month = choice(month if month else range(1, 13))
            day = choice(day if day else range(1, monthrange(year, month)[1]+1))
            return Date(year, month, day)
            
        for date in data.keys():
            dow = geohash.get_dow( make_Date(date) )
            self.assertEqual(dow, data[date]["djia"])
            
        while True:
            date = rng_date()
            if not str(date) in data:
                break
        sys.stdout = StringIO()
        self.assertFalse(geohash.get_dow(date))
        sys.stdout = sys.__stdout__

    def test_datedow(self):
        def test(date, attr, chk, glob=False):
            d = data[str(date)]
            date_of_dow = geohash.get_date_of_dow(date, d[attr], glob)
            try:
                datedow = geohash.make_datedow(date, data[str(date_of_dow)]['djia'] )
                self.assertEqual(datedow, d[chk])
                print("success")
            except KeyError:
                pass
            
        for date in data.keys():
            d = data[date]
            t = make_Date(date)
            test(t, "coord_1", "hash_str")
            test(t, "coord_2", "hash_str_30w")
            test(t, "coord_1", "glob_hash_str", True)

    def test_defaults(self):
        off = object()
        def build(inp, empty=off):
            x = Namespace()
            for k, v in inp.items():
                setattr(x, k, v if empty is off else empty)
            return x
            
        def test(inp, save=True):
            x = build(inp)
            y = build(inp, None)
            if save:
                geohash.store_defaults(x)
            ret = geohash.set_defaults(y)
            self.assertEqual(y, build(inp))
            self.assertTrue(all(ret[L] == inp[L] for L in ret))

        test({}, False)
        test({"latitude":68, "longitude":30, "json":False})
        test({"latitude":68, "longitude":29, "json":True})
        test({"json":False})
        test({"json":True})

    def test_cache(self):
        def test(chk, clear=False):
            if clear and not randint(0, clear):
                chk = dict()
                geohash.get_dow.cache_clear()
            k = choice(list(data))
            chk[k] = geohash.get_dow( make_Date(k) )
            self.assertEqual(chk, geohash.get_dow.cache)
            try:
                with open(geohash.get_dow.cache_path, "r") as fp:
                    load = json.load(fp)
                    self.assertEqual(chk, load)
            except (IOError):
                pass
            return chk

        #clear on non-existant cache file raises?
        geohash.get_dow.cache_clear()
        chk = {}
        for x in range(100):
            chk = test(chk)
        for x in range(100):
            chk = test(chk, 1)

if __name__ == '__main__':
    unittest.main()
