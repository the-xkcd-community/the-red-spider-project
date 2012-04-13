#!/usr/bin/env python

# Copyright 2012 Neil Forrester
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

import json
import sys

if __name__ == "__main__":
	for line in map(lambda json_dict: json_dict[sys.argv[1]], map(json.loads, sys.stdin.readlines())):
		print line
