'''
ASCII Art maker
A (very simple) class for creating an ASCII string
Picks a random image in a given directory and generates an ASCII art from it.
Takes in .jpg, .jpeg, .bmp and .png image files.
Author: leo
Date: 06/12/2012
'''

#TODO: Clean up the code. Maybe split it into two different files (the class and the I/O functionality).
#      Also, try to change the output size according to the environment.

from PIL import Image
import random
from bisect import bisect
import os
import sys


#Size (in pixels) of the output image. I think that making
#these variables to adapt to some environment will be implementation dependable.
#Will try to make a UNIX/POSIX one afterwards.
#leo

_HEIGHT = 160
_WIDTH = 65

# The following strings represent
# 10 tonal ranges, from lighter to darker, so that they
# are the greyscale.
# The greyscale was picked from: http://local.wasp.uwa.edu.au/~pbourke/dataformats/asciiart/

greyscale = [
            " ",
            "@",
            ":",
            "-",
            "=",
            "+",
            "*",
            "#",
            "%",
            "."
            ]

# There are 10 luminosity bands, of equal sizes. They can be changed accordingly;
# for instance, to boost contrast.

zonebounds=[25, 50, 75, 100, 125, 150, 175, 200, 225, 250]

class AsciiGenerator(object):
  #This assumes that correct path checking was done previously.
  #May want to change the panic mode and not exiting like this.

  def __init__(self, imagePath):
    try:
      self.image = Image.open(imagePath)
    except IOError:
      print 'Could not open image. Are you sure you entered the correct path?\n'
      sys.exit(-1)
    self.image = self.image.resize((_HEIGHT, _WIDTH),Image.BILINEAR)
    self.image = self.image.convert("L") # convert to mono

  def __str__(self):
    asciiString = ''
    for height in xrange(0, self.image.size[1]):
      for width in xrange(0, self.image.size[0]):
        lum = 255 - self.image.getpixel((width, height))
        row = bisect(zonebounds, lum)
        try:
         possibles = greyscale[row]
        except IndexError:
         continue
        asciiString = asciiString + possibles[random.randint(0, len(possibles) - 1)]
      asciiString = asciiString + '\n'
    return asciiString

def isImage(extension):
  #Seems a kludge. Maybe there is a cleaner, more pythonic way of checking the extension.
  if extension == '.bmp' or extension == '.jpg' or extension == '.jpeg' \
     or extension == '.png':
    return True
  return False

def chooseRandomImage(imageList):
  size = len(imageList)
  return imageList[random.randint(0, size - 1)]

def _usage():
  print 'Usage: python randomascii.py [SOURCE FOLDER]'

def generateImageList(targetDirectory):
  dir_list = os.listdir(targetDirectory)
  imageList = []
  for file_target in dir_list:
    fileName, fileExtension = os.path.splitext(os.path.join(targetDirectory, file_target))
    if isImage(fileExtension):
      imageList.append( fileName+fileExtension )
  if not imageList:
    print 'Found no images in the target directory %(directory)s' % {'directory':targetDirectory}
    print 'Supported format for images are .png, .bmp, .jpg and .jpeg'
    sys.exit(-1)
  return imageList

def main():
  if len(sys.argv) != 2:
    _usage()
    sys.exit(-1)
  curr_dir = sys.argv[1]
  while not os.path.exists(curr_dir):
    curr_dir = raw_input('Path not found. Please, try again: ')
  imageList = generateImageList(curr_dir)
  imageToPrint = chooseRandomImage(imageList)
  print imageToPrint
  asciiString = AsciiGenerator(imageToPrint)
  if asciiString:
    print asciiString
  
main()
