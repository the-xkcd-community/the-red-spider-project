# By Wesley Aptekar-Cassels
# Thanks to Steven Kay


import Image
import random
from bisect import bisect
from subprocess import call


def img2ascii(iimg):
    greyscale = [
                " ",
                " ",
                ".,-",
                "_ivc=!/|\\~",
                "gjez2]/(YL)t[+T7Vf",
                "mdK4ZGbNDXY5P*Q",
                "W8KMA",
                "#%$"
                ]


    zonebounds=[36,72,108,144,180,216,252]


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
    call(["mkdir", "/tmp/vid/"])
    call(["ffmpeg", "-i", vid, "/tmp/vid/image%d.jpg"])

vid2frames(r"vid/vid.mp4")
print img2ascii(r"img.jpg")
