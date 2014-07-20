#! /usr/bin/env python2
# Copyright 2013 PM 2Ring
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

''' phpBB forum thread fetch

Fetch data from a range of pages of a phpBB forum thread 
and save the author, time & contents of each post as (extended) ASCII.

Created as XKCDthreadfetch by PM 2Ring, 2013.5.13
Generalised & modified to handle posts with quotes, 2013.8.25
'''

import sys, getopt, re, urllib
from myentity import entityToASCII

#Regex patterns for thread data extraction
ptitle = re.compile(r'id="page-body">.*?<h2><a.*?>(.*?)</a></h2>', re.S)

pauthortime = re.compile(r'<p class="author">.*>(.*)</a>(?:by <strong>)?(.*)</strong> &raquo; (.*) </p>')
pcontent = re.compile(r'<div class="content">')
pprofile = re.compile(r'<dl class="postprofile"')

pbr = re.compile(r'<br />')
ptags = re.compile(r'<.*?>')
#pspan = re.compile(r'<span.*?>|</span>', re.S)
pdivend = re.compile(r'</div>')
pblockstart = re.compile(r'<blockquote.*?>')
pblockend = re.compile(r'</blockquote>')
psig = re.compile(r'<div id="[^"]*?" class="signature">', re.S)

pwhite = re.compile(r'\n[ ]+\n')
pblanklines = re.compile(r'\n{3,}')


#Convert some pesky UTF-8 sequences to an ASCII equivalent
putf8 = re.compile('\xe2\x80(.)')
UTFtable = {
    '\x93': '-',
    '\x94': '--',
    '\x99': "'",
    '\x9c': '"',
    '\x9d': '"',
    '\xa6': '...'
}


def xlateUTF8(matchobj):
    return UTFtable.get(matchobj.group(1), '?')


def UTF8ToASCII(s):
    return putf8.sub(xlateUTF8, s) 


def DoPage(baseurl, start, ofile, dotitle):
    url = '%s&start=%d' % (baseurl, start)
    #url = 'test.html'

    sys.stderr.write(" Fetching '%s' " % url)
    f = urllib.urlopen(url)
    data = f.read()
    f.close()
    
    #f = open('test.html', 'w')
    #f.write(data)
    #f.close
    #return

    #Get thread title
    a = ptitle.search(data)
    title = a.group(1)
    title = entityToASCII(title)
    sys.stderr.write(' Title: [%s]\r' % title)
    if dotitle:
        ofile.write('\n  Thread: \xe2\x80\x9c%s\xe2\x80\x9d\n\n' % title)    

    count = start
    while True:
        #Get Author's name and post time
        a = pauthortime.search(data)
        if not a:
            break
        
        author = a.group(1) + a.group(2)
        time = a.group(3)
        ofile.write('%d: %s at %s\n\n' % (count, entityToASCII(author), time))
        data = data[a.end():]
        
        #print >>sys.stderr, "%2d: [%s] [%s]" % (count, author, time)
        #print a.group(0), '\n'
        
        #Find start & end of post contents
        cstart = pcontent.search(data).end()
        cend = pprofile.search(data).start()
        content = data[cstart:cend]
        data = data[cend:]
        
        #Remove post signature, if found
        a = psig.search(content)
        if a:
            content = content[:a.start()]

        #print >>sys.stderr, "Contents:[%s]\n" % content

        #Replace HTML linebreaks with linefeeds
        content = pbr.sub('\n', content)
       
        #Replace blockquote tags with braces
        content = pblockstart.sub('\n{', content)
        content = pblockend.sub('}\n', content)
        
        #### Maybe preserve <a> & <img> data...
        
        #Replace </div> tags with linefeeds
        #content = pdivend.sub('\n', content)
        
        #Strip out any remaining HTML tags
        content = ptags.sub('', content)
        
        #Replace HTML entities
        content = entityToASCII(content)
        
        #Replace those pesky UTF-8 sequences
        #content = UTF8ToASCII(content)
        
        content = content.replace('\t', ' ')
        content = content.replace('\r', '')
        
        #Remove spaces from otherwise blank lines
        content = pwhite.sub('\n\n', content)
        
        #Reduce multiple newlines down to two
        content = pblanklines.sub('\n\n', content)
        
        #content = content.encode('string-escape')
        #content = content.decode('ascii','ignore')
        
        ofile.write('%s\n' % content)
        count += 1
        
 
def main():
    #args
    oname = None        #Output filename
    baseurl = None      #Base URL of thread
    lopage = 1
    hipage = None
    pagesize = 40       #Number of posts per page = 40 for xkcd

    def usage(msg=None):
        s = msg!=None and '\x1b[31m%s\x1b[0m\n\n' % msg or ''
        s += '''Fetch and save data from a range of pages of a phpBB forum thread 

\x1b[1mUsage\x1b[0m
%s [-h] -u [-s] [-e] [-p] [-o]

\x1b[1mOptions\x1b[0m
-o output file name
-u base URL
-s start page number
-e end page number
-p posts per page

You must put the URL string in quotes to prevent the shell from interpreting the embedded ampersands. Eg,
'http://forums.xkcd.com/viewtopic.php?f=14&t=6989'

The default start page is 1, the default end page is the start page.
The default page size is %d.

If no output file name is given, output goes to stdout.
'''
        print >>sys.stderr, s % (sys.argv[0], pagesize)
        raise SystemExit, msg!=None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:u:s:e:p:")
    except getopt.GetoptError, e:
        usage(e.msg)

    for o, a in opts:
        if o == "-h": usage(None)
        elif o == "-o": oname = a
        elif o == "-u": baseurl = a
        elif o == "-s": lopage = int(a)
        elif o == "-e": hipage = int(a)
        elif o == "-p": pagesize = int(a)
    
    if hipage == None: 
        hipage = lopage
    
    print >>sys.stderr, "oname: '%s'\nurl: '%s'\nlopage: %d\nhipage: %d\npagesize: %d\n" % (oname, baseurl, lopage, hipage, pagesize)
    
    #Convert page numbers to message numbers
    lonum = (lopage - 1) * pagesize
    hinum = (hipage) * pagesize

    if oname:
        ofile = open(oname, 'wt')
    else:
        ofile = sys.stdout

    dotitle = True
    for i in xrange(lonum, hinum, pagesize):
        DoPage(baseurl, i, ofile, dotitle)
        dotitle = False
    sys.stderr.write('\n')
        
    if oname:
        ofile.close()
    

if __name__ == '__main__':  
  main()
