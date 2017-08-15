#! /usr/bin/env python2
from __future__ import print_function

''' setup2.py
Initial setup script for the Red Spider Project, completely rewritten from the
ground up by Lior

Copyright 2012, 2013 Julian Gonggrijp
Copyright 2014       Lior Ramati
Licensed under the Red Spider Project License.
See the License.txt that shipped with your copy of this software for details.

A -q option to make it less verbose would probably be nice. Until we
have a dedicated 'update' command we'll need to run the setup every
time one of the commands has been changed on master.
'''

# TODO: 
#   [ ] Write all the functions
#   [ ] Move various stuff into constants to clean code (maybe)
#   [ ] Rearrange the functions so they appear in a useful manner in the source

import sys
import os, os.path
import subprocess
import argparse

import rsupdate # This is here because i intended to pull the installation functions from a separate update script eventually, so you dont have to run a full setup just to update your project. this is here as a reminder of that.

# List of all functions called by the 3 main functions and a bit about their innards
# [x] get_rsp_src_dir(cl_source=""): returns directory with project source, trying the clarg first. possibly just wrapper for get_dir()
# [x] get_install_dir(cl_dest=""): same as get_rsp_src_dir(), but for an empty folder to install into
# [ ] get_default_pref(cl_default=""): possibly just a wrapper for some choice function. or replaced with a call to said choice function
# [ ] build_sys(build_dir, command): calls command ([dev]build|clean|config) for each file in the build directory
# [ ] add_rc_block(name, rc_data, clash="break"): takes name of block, data, and collision response. break: throw an error, new: overwrite old with new on an item-by-item basis, old: ditto but reversed, clobber: overwrite whole block. also generates rc file if it doesnt exist yet
# [ ] set_default_root(root): sets the default root as defined in the rc file
# [ ] get_rsp_dir(cl_dir=""): same as get_rsp_src_dir() but for an install, not source. Maybe have rc file have a list of all installs, and check against that?
# [ ] get_persist_pref(cl_persist=""): see get_default_pref()
# [ ] for_each_file_do(root, command, fail, subs=True): do command for each file under root, recursively if subs. fail is the behaviour for a failed command(non-zero exit). break immediately? catalog all fails and return the list after? something else i havent thought of yet? maybe shouldnt be a function
# [x] get_dest_dir(cl_dest=""): identical to get_install_dir. probably a different prompt message
# [ ] refactor_prog(root): some sort of function to go through root and correct any issues caused by moving an installation. maybe should take old root too?
# [ ] read_rc_block(name): get the name data block in the rc file
# [ ] remove_rc_block(name): delete the name data block in the rc file
# [ ] update_rc_block(name, data): probably the same as add_rc_block with clash="new"
### [ ] Note: the 4 *_rc_block functions might be imported from some other rc management script
### [ ] Note: possible the way add_rc_block() generates new rc files is with a sub call to gen_rc().
### [x] Note: many of these functions suggest the existance of a get_dir() function that asks the same question over and over until a directory with given contents exists. args would probably be `msg, dir_contents, strict_contents`. msg being the thing to print, dir_contents a list of what needs to be found, and strict_contents a bool indicating if other things can also exist.


# Not convinced this is neccessary, but leaving it here just in case
#def abspath(file):
#    ''' returns an absolute path to file with homefolder are environment
#        variables expanded, and without symlinks '''
#    nouser = os.path.expanduser(file)
#    novars = os.path.expandvars(nouser)
#    nosym = os.path.realpath(nosym)
#    return nosym

def get_rsp_src_dir(cl_source=""):
    ''' Returns the directory with the project's source '''
    
    # Find path the setup script is run from
    run_dir = os.path.dirname(os.path.join(os.getcwd(), sys.argv[0]))
    
    # Initial attempt to find folder. Checks command line arg, then requests
    # source dir, with the ability to default to the run directory
    ### Note: I do an extra half indent for continued lines. I admit this looks odd, and if anyone objects, feel free to change it.
    path = cl_source or raw_input("You have run the setup script from `%s`."+\
      " If this is where I can find the project source, press enter."+\
      " Otherwise tell me where I can?"%run_dir) or run_dir
    
    # Now that we have an initial guess, hand off to get_dir for the hard part
    # and pass the result further up
    return get_dir(path, ['src','install'], "I couldn't find the project"+\
      " source in %(old_path)s. Maybe you misspeled the path or moved it elsewhere?")

def get_dir(path, dir_contents, msg, strict=False):
    ''' This function checks if path contains dir_contents (exclusively if 
        strict is set), repeatedly asking msg until it gets a valid dir if path
        isn't one. msg may contain `%(old_path)s` to indicate that the last path
        should be inserted here in the string. '''
        # TODO: Maybe increase complexity for subcontents (dir contains foo/bar)
        # if so, do we make strict a two-part variable for separate main and 
        # subfolder control?
    # Select the function to be used for contents check (identical/contains)
    check_f = set(dir_contents).__eq__ if strict else set(dir_contents).issubset
    
    # Contents check
    while not check_f(set(os.listdir(path)):
        # request new path
        path = raw_input(msg % {'old_path':path})
    
    # We have a valid directory!
    return path

def get_install_dir(cl_dest=""):
    ''' Returns the directory into which the project should be installed.'''
    
    # Initial attempt to find the directory. Checks command line arg first, then
    # requests an empty directory
    path = cl_dest or raw_input("Where should I install the project?")
    
    # Hand off to get_dir for the hard part.
    return get_dir(path, [], "That folder isn't empty! Please give me an "+\
      "empty one!", strict=True)

def get_dest_dir(cl_dest=""):
    ''' Returns the directory into which the project should be moved.'''
    
    # Initial attempt to find the directory. Checks command line arg first, then
    # requests the directory with ability to default to the current directory
    path = cl_dest or raw_input("Where should I move the project to? You are"+\
      " running the script from %s. Press enter if I should move it here, or"+\
      " another location if you'd prefer it there.") or os.getcwd()
    
    # Hand off to get_dir for the hard part
    return get_dir(path, [], "That folder isn't empty! Please give me an "+\
      "empty one!", strict=True)

def main():
    ''' main is in charge of reading command line arguments, discerning the run
        mode, and passing the command line args to the run mode's main function. '''
    
    print("Hello! welcome to the red spider project management script!")
    
    # Build command line argument list
    parser = argparse.ArgumentParser(description="Red Spider Install Manager",
                                     usage="%(prog)s [-m|-i [-d]|-u]",
                                     epilog="These flags are provided for convenience. If left unsupplied, the program will request them during execution")
    # Mode args
    # If more modes are added, they should get a command line option here
    # Required: action='store_const', dest='action', and const=<function name>
    # The function is the mode's "main()" and accepts the parsed args object
    ### Brainstorm: maybe set const to a string with the function's name and pull from vars()?
    parser.add_argument('-m','--move', action='store_const', dest='action',
                        const=move, help="Move an installation from source to dest")
    parser.add_argument('-u','--uninstall', action='store_const', dest='action',
                        const=uninstall, help="Uninstall the project at source")
    parser.add_argument('-i','--install', action='store_const', dest='action',
                        const=install, help="Install the a copy of the project in source to dest")
    
    # Behaviour args
    # We need an negative option for this to differentiate between "no dont default" and "I'm not using the command line interface"
    parser.add_argument('-d','--default','--make-default', action='store_true',
                        help="For use with -m and -i. Makes the new project rsshell's default")
    parser.add_argument('--dev', action='store_true', help=argparse.SUPPRESS)
    
    # Location args
    parser.add_argument('--source', metavar="folder", action='store',
                        help="The source folder. See -m,-u, and -i for usage")
    parser.add_argument('--dest','--destination', metavar="folder", action='store',
                        help="The Destination folder. Unused by -u. See -m, and -i for usage.")
    
    # Get command line args
    args = parser.parse_args()
    
    # Function to call gets stored here by the parser,
    # and it accepts the parsed args object as input
    if 'action' in args and args.action is not None: args.action(args)
    # If the action wasn't given on the command line, get it interactively
    else: get_action()(args)

def install(clargs):
    ''' install is the "main" function in charge of creating a new installation of the project.
        clargs is the args object the command line parser returns, and is used as a starting point
        for the various flags and paths needed to install the red spider project '''
    
    # Get options
    source = get_rsp_src_dir(clargs.source)
    # There should probably be some effort made to make sure dest is always the
    # same if its pointing to the same location.
    dest = get_install_dir(clargs.dest)
    default = get_default_pref(clargs.default)
    
    if source is not dest:
        pass
        # TODO: If the project is being installed into the folder it was unzipped into
        # things become signifficantly simpler. In the case that it is not, certain
        # things have to happen to allow for the successful construction of the project.
    
    # Install the thing!
    build_sys(pass) # TODO: figure out how this function was intended to work
    
    # Currently, I'm not sure what data would go in the install's rc section
    # but I'm leaving the function call in just in case
    try:
        add_rc_block(dest, data, clash="break")
    except LookupError: # LookupError should maybe be replaced with a custom error?
        print "Something has gone terribly wrong! There is already a section"+\
          " in the rc file for this location! Please attempt to fix this and"+\
          " then run the setup script again."
          sys.exit()
    
    # If we decide to make the rc file aware of all installations, that should
    # also happen around here
    if default:
        set_default_root(dest)
    
    # TODO: Make sure a copy of rsshell is in the user's bin folder, and whatever
    # madness is supposed to happen on windows.
    # Alternative idea: place a launch script instead that would call a specific
    # install's own rsshell to allow multiple installs to use separate versions.

def uninstall(clargs):
    ''' uninstall is the "main" function in charge of removing an old installation of the project.
        clargs is the args object the command line parser returns, and is used as a starting point
        for the various flags and paths needed to uninstall the red spider project '''
    # TODO: write function body
    # function calls:
    # get_rsp_dir - obtain root of installation to uninstall
    # get_persist_pref - should i keep rc settings for the install?
    # for_each_file_do - delete all the files
    # get_rsp_dir - obtain root of alternative default root
    # set_default_root - set the default root in the rc file
    pass

def move(clargs):
    ''' move is the "main" function in charge of migrating an installation of the project.
        clargs is the args object the command line parser returns, and is used as a starting point
        for the various flags and paths needed to move the red spider project '''
    # TODO: write function body
    # function calls:
    # get_rsp_dir - obtain root of installation to move
    # get_dest_dir - obtain dir to move root to
    # get_default_pref - set this as default installation? y/n
    # for_each_file_do - move all the files
    # refactor_prog - goes through new root and corrects anything broken by the move
    # read_rc_block - get data about old install point from rc file
    # remove_rc_block - delete data about old install point from rc file
    # add_rc_block - reinsert the data for the new install point into rc file
    ### Note: the last 3 functions maybe should just be a block of code.
    ### Incentive for adding them is that together with update_rc_block they
    ### could be used for a --update mode which would modify rc file data.
    ### Alternatively, a separate script could be used for that. Although even
    ### then, we could include that script here and call the script's functions
    ### from move()...
    pass
