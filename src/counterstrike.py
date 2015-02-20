#!/usr/bin/env python

# Copyright 2015 Michael Gardner
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

print "Welcome to text-only Counterstrike"
print "Enter \"help\" to view the available commands"
print "You are in a dark, outdoor map."

while True:
	input = raw_input("> ")
	
	if input == "GO NORTH" or input == "GO SOUTH" or input == "GO EAST" or input == "GO WEST":
		print "You have been pwned by a grue."
		break
	elif input == "help":
		print "Available commands:"
		print " - GO NORTH"
		print " - GO SOUTH"
		print " - GO EAST"
		print " - GO WEST"
	else:
		print "Unknown command"