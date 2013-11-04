#! /usr/bin/env python2

#Copyright 2013 Sanjay Kannan (whaatt)
#Licensed under the Red Spider Project License.
#See the License.txt that shipped with your copy of this software for details.

#standard Python 2.x modules
from urllib2 import *
import sys, codecs, random, shutil

#remember if dependencies are available
#dependencies are lxml, cssselect, and [internet]
depAvailable = True

#attempt to import lxml and cssselect
#attempt to grab Google to test internet
#if not available, default to cache mode

try:
    import cssselect
    from lxml import html
    urlopen('http://google.com')
except:
    depAvailable = False

#return address of cache dir
#if flag = True, get backup copy
def getCacheDir(flag = False):
    spiderRoot = os.getenv('RED_SPIDER_ROOT', '..')
    if not flag: return spiderRoot + '/work/fortune/'
    else: return spiderRoot + '/other/'
    
#handle insufficient dependencies
def noDeps(verbose = False):
    #access dependency flag
    global depAvailable
    
    if not depAvailable:
        if verbose:
            print('You do not have all of the following: lxml, cssselect, internet access.')
            print('Please install or acquire these dependencies to use this feature. Thanks!')
        return True #as in True, we have no dependencies available
    
    return False #as in False, we do have the required dependencies
    
#get a random thread
#fetched from XKCDB
#otherwise from cache

#then, update cache file 
#with new thread

def fetchRandom(url = 'http://www.xkcdb.com/random1'):
    if noDeps(): #access local cache without internet
        with codecs.open(getCacheDir() + 'fortune.txt', 'r', encoding = 'utf-8') as cachefile:
            #get cache file header data
            ids = cachefile.readline().strip().split()
            votes = cachefile.readline().strip().split()
            lineNums = cachefile.readline().strip().split()
            
            #gets array index that will correspond with votes/lineNums
            randomID = random.choice(ids)
            quoteHeadersID = ids.index(randomID)
            
            [upVotes, downVotes] = votes[quoteHeadersID].split(',') #split '3,4' or something into [3,4] to get up/down votes
            [start, end] = [int(i) for i in lineNums[quoteHeadersID].split(',')]
            
            print('Thread #' + randomID + ' fetched from cache file.')
            print('This has ' + upVotes + ' upvotes and ' + downVotes + ' downvotes.\n')
            
        #open new handle, just for safety's sake. overhead is minimal
        with codecs.open(getCacheDir() + 'fortune.txt', 'r', encoding = 'utf-8') as cachefile:
            for num, line in enumerate(cachefile):
                #python shifts line indices down one, so they start at 0
                if start - 1 <= num <= end - 1: #check if line in desired range
                    print line.encode('utf-8', 'ignore').strip()
                    
    else: #if internet and parsing libs are there
        #use urllib2 to get random thread HTML
        response = urlopen(url)
        headers = response.info()
        source = response.read().decode('utf-8', 'ignore')

        #generate HTML tree from source
        tree = html.fromstring(source)

        #code that is similar to genCache()
        #but this only gets the first thread: index = 0
        headerSelect = tree.cssselect('.quotehead')
        header = headerSelect[0].text_content().split()
        id = header[0][1:] #looks like '#123' in HTML output, so strip '#' ---> '123'
        
        votes = header[2][1:-1].replace('+','').replace('-','').replace('/',',') #strip parentheses from '(+3/-1)' ---> '3,1'
        [upVotes, downVotes] = votes.split(',')
        
        quoteSelect = tree.cssselect('.quote')
        quote = quoteSelect[0].text_content().strip()
        
        print('Thread #' + id + ' fetched from XKCDB online.')
        print('This thread will be added to the cache.')
        print('This has ' + upVotes + ' upvotes and ' + downVotes + ' downvotes.\n')
        print quote.encode('utf-8', 'ignore').strip()
        
        #find new start, end positions for cache append
        with open(getCacheDir() + 'fortune.txt') as f:
            for i, l in enumerate(f):
                pass
            start = i + 2 + 1 #add 1 for enumerate
            end = start + quote.count('\n')
        
        with codecs.open(getCacheDir() + 'fortune.txt', 'r', encoding = 'utf-8') as cachefile:
            #create temp file for safety
            with codecs.open(getCacheDir() + 'fortune.txt.bak', 'w', encoding = 'utf-8') as tempfile:
                ids = cachefile.readline().strip() + ' ' + id + '\n'
                votes = cachefile.readline().strip() + ' ' + votes + '\n'
                lineNums = cachefile.readline().strip() + ' ' + str(start) + ',' + str(end) + '\n'
                
                changeFile = ids.strip().split().count(id) #check if thread pre-exists
                if changeFile == 1: #this is the number of id #id in [ids]
                    tempfile.write(ids + votes + lineNums)
                    nextLine = cachefile.readline()
                    
                    #copy everything else
                    while nextLine:
                        tempfile.write(nextLine)
                        nextLine = cachefile.readline()
                        
                    #finally append the new quote
                    tempfile.write('\n\n')
                    tempfile.write(quote)
        
        if changeFile == 1:
            #remove old file, rename new one to fortune
            os.remove(getCacheDir() + 'fortune.txt')
            os.rename(getCacheDir() + 'fortune.txt.bak', getCacheDir() + 'fortune.txt')
    
#get a specific thread
#fetched from XKCDB
#or search the cache
#if    nonexistent, say so

def fetchID(id, urlBase = 'http://www.xkcdb.com/'):
    #validate thread ID
    try:
        id = int(id)
        if id < 1:
            print('An invalid thread ID was passed as an argument.')
            print('Please try again with a different thread ID.')
            return False
    except:
        print('An invalid thread ID was passed as an argument.')
        print('Please try again with a different thread ID.')
        return False
        
    if noDeps(): #access local cache without internet
        with codecs.open(getCacheDir() + 'fortune.txt', 'r', encoding = 'utf-8') as cachefile:
            #get cache file header data
            ids = cachefile.readline().strip().split()
            votes = cachefile.readline().strip().split()
            lineNums = cachefile.readline().strip().split()
            
            #gets array index that will correspond with votes/lineNums
            try: #check if ID exists
                threadID = str(id)
                quoteHeadersID = ids.index(threadID)
            except:
                print('A thread ID that is not cached was passed as an argument.')
                print('Please try again with a different thread ID.')
                return False
            
            [upVotes, downVotes] = votes[quoteHeadersID].split(',') #split '3,4' or something into [3,4] to get up/down votes
            [start, end] = [int(i) for i in lineNums[quoteHeadersID].split(',')]
            
            print('Thread #' + threadID + ' fetched from cache file.')
            print('This has ' + upVotes + ' upvotes and ' + downVotes + ' downvotes.\n')
            
        #open new handle, just for safety's sake. overhead is minimal
        with codecs.open(getCacheDir() + 'fortune.txt', 'r', encoding = 'utf-8') as cachefile:
            for num, line in enumerate(cachefile):
                #python shifts line indices down one, so they start at 0
                if start - 1 <= num <= end - 1: #check if line in desired range
                    print line.encode('utf-8', 'ignore').strip() #print lines of thread
                    
    else: #if internet and parsing libs are there
        #use urllib2 to get specific thread HTML
        response = urlopen(urlBase + str(id))
        headers = response.info()
        source = response.read().decode('utf-8', 'ignore')
        
        #hacky way to determine whether a quote exists online
        #this is the string that is displayed for '404s' on XKCDB
        if 'No quotes were found with that ID or containing that string.' in source:
            print('A thread ID that does not exist was passed as an argument.')
            print('Please try again with a different thread ID.')
            return False
        
        #generate HTML tree from source
        tree = html.fromstring(source)

        #code that is similar to genCache()
        #but this only gets the first thread: index = 0
        headerSelect = tree.cssselect('.quotehead')
        header = headerSelect[0].text_content().split()
        
        #id gets reassigned here, only because I was copying code. no harm done, just an assignment
        id = header[0][1:] #looks like '#123' in HTML output, so strip '#' ---> '123'
        
        votes = header[2][1:-1].replace('+','').replace('-','').replace('/',',') #strip parentheses from '(+3/-1)' ---> '3,1'
        [upVotes, downVotes] = votes.split(',')
        
        quoteSelect = tree.cssselect('.quote')
        quote = quoteSelect[0].text_content().strip()
        
        print('Thread #' + id + ' fetched from XKCDB online.')
        print('This thread will be added to the cache.')
        print('This has ' + upVotes + ' upvotes and ' + downVotes + ' downvotes.\n')
        print quote.encode('utf-8', 'ignore').strip()
        
        #find new start, end positions for cache append
        with open(getCacheDir() + 'fortune.txt') as f:
            for i, l in enumerate(f):
                pass
            start = i + 2 + 1 #add 1 for enumerate
            end = start + quote.count('\n')
        
        with codecs.open(getCacheDir() + 'fortune.txt', 'r', encoding = 'utf-8') as cachefile:
            #create temp file for safety
            with codecs.open(getCacheDir() + 'fortune.txt.bak', 'w', encoding = 'utf-8') as tempfile:
                ids = cachefile.readline().strip() + ' ' + id + '\n'
                votes = cachefile.readline().strip() + ' ' + votes + '\n'
                lineNums = cachefile.readline().strip() + ' ' + str(start) + ',' + str(end) + '\n'
                
                changeFile = ids.strip().split().count(id) #check if thread pre-exists
                if changeFile == 1: #this is the number of id #id in [ids]
                    tempfile.write(ids + votes + lineNums)
                    nextLine = cachefile.readline()
                    
                    #copy everything else
                    while nextLine:
                        tempfile.write(nextLine)
                        nextLine = cachefile.readline()
                        
                    #finally append the new quote
                    tempfile.write('\n\n')
                    tempfile.write(quote)
        
        if changeFile == 1:
            #remove old file, rename new one to fortune
            os.remove(getCacheDir() + 'fortune.txt')
            os.rename(getCacheDir() + 'fortune.txt.bak', getCacheDir() + 'fortune.txt')
    
#generate the cache file
#overwrites old cache file
#get top 1000 threads

def genCache(numPages = 20, urlBase = 'http://www.xkcdb.com/top?page='):
    #get result of dep check
    if noDeps(True): return False
    
    #validate number of pages
    try:
        numPages = int(numPages)
        if numPages < 1:
            print('An invalid number of pages was passed as an argument.')
            print('Please try again with a different number of pages.')
            return False
        if numPages > 100:
            print('Caching currently supports a maximum of 100 pages.')
            print('Please try again with a different number of pages.')
            return False
    except:
        print('An invalid number of pages was passed as an argument.')
        print('Please try again with a different number of pages.')
        return False
            
    #informational messages
    print('Starting cache of threads.')
    print('Caching a total of ' + str(numPages) + ' pages.')
    print('All threads sourced from XKCDB.\n')

    #these arrays' indices
    #will correspond with each other
    ids, votes, quotes, lineNums = [], [], [], []

    #the start/end line positions will be stored in the cache file
    #so we can access an individual thread without opening the whole cache
    
    #line 1 is for IDs (space delimited)
    #line 2 is for up/down votes (space delimited)
    #line 3 is for line numbers (space delimited)
    #line 4 is a blank line
    #line 5-end is each thread/quote, each followed by a newline char
    
    #as such, we start with 5
    lineNo = 5 
    
    for page in range(1, numPages + 1): #numPages pages
        #use urllib2 to get top page HTML
        #add page to urlBase for top threads
        #there should be fifty threads/page
        response = urlopen(urlBase + str(page))
        headers = response.info()
        source = response.read().decode('utf-8', 'ignore')

        #generate HTML tree from source
        tree = html.fromstring(source)

        headerSelect = tree.cssselect('.quotehead')
        headers = [header.text_content().split() for header in headerSelect]
        ids += [header[0][1:] for header in headers] #looks like '#123' in HTML output, so strip '#' ---> '123'
        votes += [header[2][1:-1].replace('+','').replace('-','').replace('/',',') for header in headers] #strip parentheses from '(+3/-1)' ---> '3,1'
        
        quoteSelect = tree.cssselect('.quote')
        newQuotes = [quote.text_content().strip() for quote in quoteSelect]
        quotes += newQuotes
        
        #do line number arithmetic
        for quote in newQuotes:
            newLines = quote.count('\n')
            lineNums.append(str(lineNo) + ',' + str(lineNo + newLines)) #format is '5,7' for a thread on lines 5-7
            lineNo += newLines + 2 #update lineNo to new start position
            
        #log to console so users know what's going on if this takes a while
        print('Page ' + str(page) + ' of top threads was downloaded. (' + str(page * 50) + '/' + str(numPages * 50) + ')')
    
    #create work/fortune if it doesn't already exist, to avoid an error
    if not os.path.isdir(getCacheDir()): os.makedirs(getCacheDir())
    
    with codecs.open(getCacheDir() + 'fortune.txt', 'w', encoding = 'utf-8') as outfile:
        #separator
        print ''
        
        #write header info to top lines
        #see format spec above
        outfile.write(' '.join(ids) + '\n')
        outfile.write(' '.join(votes) + '\n')
        outfile.write(' '.join(lineNums))
        
        #write newline, newline, quote, newline, newline, quote, etc..
        for quote in quotes:
            outfile.write('\n\n' + quote)
        
        print('Old cache file overwritten, if it existed.')
        print('Quotes successfully cached. Enjoy!')
    
    #great success
    return True

#create fortune file from copy that ships with Red Spider on first run
#if backup copy has been deleted, issue a warning message
#create the necessary directories, like work/fortune
    
def setupCache():
    try:
        with open(getCacheDir() + 'fortune.txt') as file: pass
        
    except IOError:
        print('No fortune cache file found in the appropriate directory!')
        print('I will attempt to copy one from the backup location.')
        
        try:
            if not os.path.isdir(getCacheDir()): os.makedirs(getCacheDir())
            shutil.copy(getCacheDir(True) + 'fortune.txt', getCacheDir())
            print('The backup cache file was succcessfully copied!\n')
            
        except IOError, OSError:
            print('\nThe cache copy was tragically unsuccessful.')
            print('It is possible that the backup does not exist.')
            print('Please run \'fortune cache\' now to create cache.\n')
            return False
    
    return True
    
def main(argv = None):
    #blank line for good measure
    print ''
        
    if not argv:
        if not setupCache(): return False
        fetchRandom() #default behavior is to fetch random thread
        
    elif argv[0].lower() == 'fetch':
        if not setupCache(): return False
        try: fetchID(argv[1]) #for commands like 'fortune fetch 148', fetch the specified thread by ID
        except IndexError: fetchRandom() #fetch is alias for no parameter, e.g. 'fortune fetch' is the same as 'fortune'
    
    elif argv[0].lower() == 'cache':
        try: genCache(argv[1]) #cache argv[1] number of pages (50 threads/page) from XKCDB, e.g. 'fortune cache 30' for 1500 threads
        except IndexError: genCache() #just cache first 20 pages, which is one thousand threads, e.g. 'fortune cache'
        
    else:
        print helpMessage #all other args, including 'fortune help' default to this
        
    #another blank line
    print ''

helpMessage = '''This is the help message for the fortune command.
You are seeing this because you typed help or a nonexistent command.
The following are some of the parameters you can use with fortune.

fortune --> Grabs a random #xkcd thread from your cache file or XKCDB.
fortune fetch --> An alias of fortune, for consistency's sake.
fortune fetch ID --> Fetch the given thread by ID.
fortune cache --> Grab 20 pages worth of fortunes from XKCDB, for cache.
fortune cache pages --> Cache the given number of pages from XKCDB.

If you are seeing Python error messages, your fortune file is corrupted.
Fear not, you may simply run 'fortune cache' to generate a new cache.
Otherwise, you may simply download a new copy from GitHub.'''

if __name__ == '__main__':
    main(sys.argv[1:])