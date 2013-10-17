#! /usr/bin/env python

#Geico
#By Bryton Moeller

#club cost estimates by:http://sports.whatitcosts.com/golf-clubs-pg3.htm

golfbag = {"Putter":[0.1,175],"5iron":[0.15,100],"7iron":[0.17,100],"Wood":[0.22,225],"Driver":[0.26,350]}
#filling the golf bag			club                      %off                  price
#									                    insurence

inttrue = False
while(inttrue == False):
	insurencecost = raw_input("How much does your insurence currently cost?:");
	if (isinstance(insurencecost, int)) == False:
    		print (insurencecost, 'is not an integer');
    	else:
    		inttrue = True
#interger checking


clubchoice = raw_input("Which golf club would you like to use to threaten your agent?\n Putter costs 175$ but saves you 10 percent on your insurence.\n5iron costs 100$ but saves you 15 percent on your insurence.\n7iron costs 100$ but saves you 17 percent on your insurence.\nWood costs 225$ but saves you 22 percent on your insurence.\nDriver costs 350$ but saves you 26 percent on your insurence.")
#asks user for club choice and gives info
if(clubchoice != "Putter" or "5iron" or "7iron" or "Wood" or "Driver"):
		print "thats not a valis club choice"
else:
#making sure the user made a valid club chioce


	intt2 = False
	while(int2 == False):
		strength = raw_input("how scary do you look with a " + golfbag[clubchoice] + "? (1-10):");
		#gets scaryness data
		if (isinstance(strength, int)) == False:
 	   		print (strength, 'is not an integer');
 	   	else:
 	   		int2 = True
#interger checking


	totalcost = insurencecost * (1 - (golfbag[clubchoice][0] + (strength/100)))

print "your insurence will cost" + totalcost + "$, but you will have to pay" + golfbag[clubchoice][1] + "$ to purchace your club.\n"