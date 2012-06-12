# XKCD The Red Spider Project
# Random text generator
# June, 11th 2012
# Author: leo

"""
A random text generator class that takes in a data stream and returns a random stream from the input.
It uses Markov chains, with the property that, granted present state changes are probabilistic, future state depend on current state on,
not depending on the past outcomes (http://en.wikipedia.org/wiki/Markov_chain), the Markov property. This allows for on-the-fly, memoryless
generation of gibberish, which is the objective of this program.
"""

#TODO: Maybe implementing the 'words' list with some keywords, XKCD-related. Also, setup some words to be in the outcome.
#      Expanding the program may be feasible, but still it's too early. Need some ideas.
#-leo, 06/12/2012

#More intensive debugging required

import random
import sys
import os

class textGenerator(object):
  def __init__(self, open_file):
    self.cache = {}
    self.open_file = open_file
    self.words = self.file_to_words()
    self.word_size = len(self.words)
    self.wordDict()

  def file_to_words(self):
    self.open_file.seek(0)
    dataString = self.open_file.read()
    words = dataString.split()
    return words

  def triples(self):
    """ 
    Generates triples from the given data string.
    """
    if len(self.words) < 3: #Nothing to do here.
      return		
    for i in xrange(self.word_size - 2):
      yield (self.words[i], self.words[i+1], self.words[i+2])
			
  def wordDict(self):
    for word1, word2, word3 in self.triples():
      key = (word1, word2)
      if key in self.cache:
        self.cache[key].append(word3)
      else:
        self.cache[key] = [word3]

  def generate_random_text(self, size=15):
    seed = random.randint(0, self.word_size - 3)
    seed_word, next_word = self.words[seed], self.words[seed+1]
    word1, word2 = seed_word, next_word
    gen_words = []
    for i in xrange(size):
      gen_words.append(word1)
      word1, word2 = word2, random.choice(self.cache[(word1, word2)])
      gen_words.append(word2)
    return ' '.join(gen_words)

def _usage():
  print 'Usage: python randomtext.py [PATH/FILE] [NUMBER OF WORDS IN THE OUTPUT] [optional: output file]'

def writeFile(toWrite, path):
  try:
    open(path, 'w').write(toWrite)
  except IOError:
    print toWrite

def main():
  if len(sys.argv) < 3 or len(sys.argv) > 4:
    _usage()
    sys.exit(-1)
  filePath = sys.argv[1]
  if not os.path.exists(filePath):
    raise IOError('Path not found. Are you sure you entered the correct path?\n')
  textWriter = textGenerator(open(filePath, 'r'))
  textSize = int(sys.argv[2])
  while (textSize < 0):
    textSize = int(raw_input('Enter a number > 0 for the words to be generated. '))
  randomText = textWriter.generate_random_text(textSize)
  output = True
  try:
    outputPath = sys.argv[3]
  except IndexError:
    output = False
  if output and os.path.exists(outputPath):
    writeFile(randomText+'\n', outputPath)
  else:
    print randomText
  
main()

