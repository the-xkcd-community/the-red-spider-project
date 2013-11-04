#! /usr/bin/env python2

# Copyright 2013 Bryton Moeller
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.
# club cost estimates by: http://sports.whatitcosts.com/golf-clubs-pg3.htm

golfbag = {"Putter":[0.1,175],"5iron":[0.15,100],"7iron":[0.17,100],"Wood":[0.22,225],"Driver":[0.26,350]}
# filling the golf bag          club                      %off                  price
#                                                       insurance

# pre-golfclub cost
errorcheck = False
while(errorcheck == False):
    try:
        errorcheck = True
        insurancecost = abs(int(raw_input("How much does your insurance currently cost?: ")))
    except ValueError:
        print("That's not an integer.")
        errorcheck = False
errorcheck = False
print("Putter costs $175 but saves you 10 percent on insurance.")
print("5iron costs $100 but saves you 15 percent on insurance.")
print("Wood costs $225 but saves you 22 percent on insurance.")
print("7iron costs $100 but saves you 17 percent on insurance.")
print("Driver costs $350 but saves you 26 percent on insurance.")
clubchoice = raw_input("Which golf club would you like to use to threaten your agent?: ")
# asks user for club choice and gives info
validchoice = False
while(validchoice == False):
    if(clubchoice not in ("Putter", "5iron", "7iron", "Wood", "Driver")):
        print("That's not a valid club choice.")
        clubchoice = raw_input("Which golf club would you like to use to threaten your agent?\n")
    else:
        validchoice = True
# making sure the user made a valid club choice
while (errorcheck == False):
    try:
        errorcheck = True
        strength = abs(int(raw_input("How intimidating can you look with a golf club? (1-10): ")))
        # gets scaryness data
    except ValueError:
        print("That's not an integer.")
        errorcheck = False
# integer checking
totalcost = str(insurancecost * (1 - (golfbag[clubchoice][0] + (strength/100))))

print("Your insurance will cost $" + totalcost + ", but you will have to pay $" + str(golfbag[clubchoice][1]) + " to purchase your club.\n")