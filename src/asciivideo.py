# By Wesley Aptekar-Cassels
# Thanks to Steven Kay for img2ascii.


import Image
import random
import os
import time
import sys
from bisect import bisect
from subprocess import call


def img2ascii(iimg):

    greyscale = [
                "@",
                "#",
                "8",
                "Z",
                "3",
                "+",
                "=",
                "-",
                ":",
                ".",
                " "
                ]

    zonebounds=[25, 50, 75, 100, 125, 150, 175, 200, 225, 250]


    im=Image.open(iimg)
    im=im.resize((160, 75),Image.BILINEAR)
    im=im.convert("L") 

    str=""
    for y in range(0,im.size[1]):
        for x in range(0,im.size[0]):
            lum=255-im.getpixel((x,y))
            row=bisect(zonebounds,lum)
            possibles=greyscale[row]
            str=str+possibles[random.randint(0,len(possibles)-1)]
        str=str+"\n"

    return str

def vid2frames(vid):
    call(["rm", "-r", "/tmp/vid/"]) # Cleanup
    call(["mkdir", "/tmp/vid/"]) # Fuck windows.  Hey, MS, nobody cares about you!  At least I don't, but my opinion counts as everybody, right?  right?
    call(["ffmpeg", "-i", vid, "-r", "10", "/tmp/vid/image%d.jpg"]) #@TODO: allow customizing -r via sys.argv (m. lib?)

vid2frames(sys.argv[1])

nxtframe = ""

for imgfile in os.listdir(r"/tmp/vid/")[::-1]:
    print nxtframe
    nxtframe = img2ascii("/tmp/vid/" + imgfile)
    time.sleep(0.01) #@TODO: Make fps shit work
    call(["clear"])  # My hands are typing stuff and I shouldnt be operating a keyboard with this little sleep.  HAAAAAAAAAAAAAAAANNNNNNDDDSSSS!
    time.sleep(6/10) # Replace 10 w/ the value of the -r option.

###########
# Cleanup #
###########

call(["rm", "-R", "/tmp/vid"])

