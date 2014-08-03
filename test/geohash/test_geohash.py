#! /usr/bin/env python

from __future__ import print_function

import sys, os
import time
import unittest
from functools import partial
from datetime import timedelta
from datetime import date as Date
import json

testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../src')))

import geohash

if sys.version_info[0] == 3:
    basestring = str

data = {
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

class TestGeohashFunctions(unittest.TestCase):

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
        test_cases = gen_month(2005,5)
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

    
if __name__ == '__main__':
    unittest.main()
