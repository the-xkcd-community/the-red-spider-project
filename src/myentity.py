#! /usr/bin/env python2
# Copyright 2013 PM 2Ring
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

''' My HTML entity translator
'''

import re

#Dictionary to convert HTML entities to ASCII
entityASCIItable = {
    'quot'  : '\x22', 'amp'   : '\x26', 'lt'    : '\x3c', 'gt'    : '\x3e', 
    'nbsp'  : '\xa0', 'iexcl' : '\xa1', 'cent'  : '\xa2', 'pound' : '\xa3', 
    'curren': '\xa4', 'yen'   : '\xa5', 'brvbar': '\xa6', 'sect'  : '\xa7', 
    'uml'   : '\xa8', 'copy'  : '\xa9', 'ordf'  : '\xaa', 'laquo' : '\xab', 
    'not'   : '\xac', 'shy'   : '\xad', 'reg'   : '\xae', 'macr'  : '\xaf', 
    'deg'   : '\xb0', 'plusmn': '\xb1', 'sup2'  : '\xb2', 'sup3'  : '\xb3', 
    'acute' : '\xb4', 'micro' : '\xb5', 'para'  : '\xb6', 'middot': '\xb7', 
    'cedil' : '\xb8', 'sup1'  : '\xb9', 'ordm'  : '\xba', 'raquo' : '\xbb', 
    'frac14': '\xbc', 'frac12': '\xbd', 'frac34': '\xbe', 'iquest': '\xbf', 
    'Agrave': '\xc0', 'Aacute': '\xc1', 'Acirc' : '\xc2', 'Atilde': '\xc3', 
    'Auml'  : '\xc4', 'Aring' : '\xc5', 'AElig' : '\xc6', 'Ccedil': '\xc7', 
    'Egrave': '\xc8', 'Eacute': '\xc9', 'Ecirc' : '\xca', 'Euml'  : '\xcb', 
    'Igrave': '\xcc', 'Iacute': '\xcd', 'Icirc' : '\xce', 'Iuml'  : '\xcf', 
    'ETH'   : '\xd0', 'Ntilde': '\xd1', 'Ograve': '\xd2', 'Oacute': '\xd3', 
    'Ocirc' : '\xd4', 'Otilde': '\xd5', 'Ouml'  : '\xd6', 'times' : '\xd7', 
    'Oslash': '\xd8', 'Ugrave': '\xd9', 'Uacute': '\xda', 'Ucirc' : '\xdb', 
    'Uuml'  : '\xdc', 'Yacute': '\xdd', 'THORN' : '\xde', 'szlig' : '\xdf', 
    'agrave': '\xe0', 'aacute': '\xe1', 'acirc' : '\xe2', 'atilde': '\xe3', 
    'auml'  : '\xe4', 'aring' : '\xe5', 'aelig' : '\xe6', 'ccedil': '\xe7', 
    'egrave': '\xe8', 'eacute': '\xe9', 'ecirc' : '\xea', 'euml'  : '\xeb', 
    'igrave': '\xec', 'iacute': '\xed', 'icirc' : '\xee', 'iuml'  : '\xef', 
    'eth'   : '\xf0', 'ntilde': '\xf1', 'ograve': '\xf2', 'oacute': '\xf3', 
    'ocirc' : '\xf4', 'otilde': '\xf5', 'ouml'  : '\xf6', 'divide': '\xf7', 
    'oslash': '\xf8', 'ugrave': '\xf9', 'uacute': '\xfa', 'ucirc' : '\xfb', 
    'uuml'  : '\xfc', 'yacute': '\xfd', 'thorn' : '\xfe', 'yuml'  : '\xff' 
}

pentity = re.compile(r'&(?:(\w+?)|#(\d+?));')

def xlateEntity(matchobj):
    full, name, num = matchobj.group(0, 1, 2)
    if name:
        return entityASCIItable.get(name, full)
    else:
        #Numeric entity
        i = int(num)
        if i <= 255:
            return chr(i)
        else:
            return full


def entityToASCII(s):
    return pentity.sub(xlateEntity, s) 


def main():
    #Simple stdio HTML entity translator
    import sys, readline
    
    while True:
        try:
            s = raw_input()
            print entityToASCII(s)
        except EOFError:
            break


if __name__ == '__main__':  
  main()
