#! /usr/bin/env python

# Copyright 2013 Bryton Moeller
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.
# club cost estimates by: http://sports.whatitcosts.com/golf-clubs-pg3.htm

golfbag = {"Putter":[0.1,175],"5iron":[0.15,100],"7iron":[0.17,100],"Wood":[0.22,225],"Driver":[0.26,350]}
# filling the golf bag			club                      %off                  price
#									                    insurance

inttrue = False
while(inttrue == False):
	insurancecost = raw_input("How much does your insurance currently cost?:")
	# pre-golfclub cost
	if (isinstance(insurancecost, int)) == False:
		print(insurancecost + ' is not an integer')
	else:
		inttrue = True
# integer checking


clubchoice = raw_input("Which golf club would you like to use to threaten your agent?\n Putter costs 175$ but saves you 10 percent on your insurance.\n5iron costs 100$ but saves you 15 percent on your insurance.\n7iron costs 100$ but saves you 17 percent on your insurance.\nWood costs 225$ but saves you 22 percent on your insurance.\nDriver costs 350$ but saves you 26 percent on your insurance.")
# asks user for club choice and gives info
if(clubchoice != "Putter" or "5iron" or "7iron" or "Wood" or "Driver"):
	print "That's not a valid club choice"
else:
# making sure the user made a valid club choice


	intt2 = False
	while(int2 == False):
		strength = raw_input("how intimidating can you look with a " + golfbag[clubchoice] + "? (1-10): ")
		# gets scaryness data
		if (isinstance(strength, int)) == False:
 	   		print (strength + ' is not an integer')
	   	else:
 	   		int2 = True
# integer checking

	totalcost = insurancecost * (1 - (golfbag[clubchoice][0] + (strength/100)))

