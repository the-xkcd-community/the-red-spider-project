#! /usr/bin/env python2
from __future__ import print_function

''' setup.py
Initial setup script for the Red Spider Project

Copyright 2012, 2013 Julian Gonggrijp
Licensed under the Red Spider Project License.
See the License.txt that shipped with your copy of this software for details.


A -q option to make it less verbous would probably be nice. Until we
have a dedicated 'update' command we'll need to run the setup every
time one of the commands has been changed on master.
'''

from future_builtins import zip, map
import os
from os.path import exists, join, split, splitext, abspath, expanduser
from shutil import copy2
import py_compile
import sys
import stat

bin_dir     = 'bin'
extbin_dir  = 'extbin'  # stands for 'external binaries'
lib_dir     = 'lib'
build_dir   = 'build'
src_dir     = 'src'
inc_dir     = 'include'
cfg_dir     = 'config'
work_dir    = 'work'

documented_cmds = [["xkcd-fetch",    "xkcd-fetch --help"],
                   ["xkcd-search",   "xkcd-search --help"],
                   ["level_up",      "level_up --help"],
                   ["summon",        "summon"],
                   ["fortune",       "fortune --help"],
                   ["godel",         "godel"],
                   ["random-number", "random-number --help"],
                   ["randomtext",    "randomtext"]]

executable_scripts = [  'json-parse.py', 'xkcd-fetch.py', 'xkcd-search.py',
                        'level_up.py', 'summon.py', 'fortune.py', 'godel.py',
                        'random-number.py', 'rshelp.py', 'Geico.py', 'randomtext.py' ]

python_modules = 'src/xkcd-fetch.py src/level_up.py'.split()

def main ( ):
    print(welcome_msg)
    red_spider_root = verify_root()
    extend_user_env('RED_SPIDER_ROOT', red_spider_root, 'o')
    os.chdir(red_spider_root)
    # existence of the build dir is the natural indicator of a previous install
    user_pref = raw_input(
        reinstall_choice_msg if exists(build_dir) else new_install_choice_msg
    )
    if 'y' in user_pref or 'Y' in user_pref:
        install()
    print(farewell_msg)

def verify_root ( ):
    root_path = os.path.dirname(abspath(sys.argv[0]))
    user_path = raw_input(root_guess_msg.format(root_path))
    if user_path:
        user_path = abspath(expanduser(user_path))
        while not exists(user_path):
            user_path = raw_input(user_path_fail_msg.format(user_path))
            user_path = abspath(expanduser(user_path))
        print(user_path_end_msg.format(user_path))
        # if we want to go paranoid:
        # check_rs_root_contents(user_path)
        root_path = user_path
    if not os.access(root_path, os.R_OK | os.W_OK):
        print(root_rw_fail_message)
        sys.exit(2)
    return root_path

def check_rs_root_contents (candidate_path):
    # insert checks for directory contents if you want
    pass

def extend_user_env (name, value, mode):
    '''Add 'value' to 'name' in the user's environment settings that
    are loaded at login. This function writes to HKEY_CURRENT_USER in
    the Registry on Windows and to ~/.profile on unixy systems. 'mode'
    determines what to do with any pre-existing value:
     a  append the new value to the old
     p  prepend the new value to the old
     o  overwrite the old value with the new

    You should only write values to the user environment that are
    normally stored as strings, i.e. REG_SZ or REG_EXPAND_SZ in the
    Windows registry.'''
    if mode not in ('a', 'o', 'p'):
        raise ValueError("mode must be 'a', 'o' or 'p'")
    if os.name == 'nt':
        extend_user_env_windows(name, value, mode)
    else:
        extend_user_env_posix(name, value, mode)

def extend_user_env_windows (name, value, mode):
    '''NEVER call this function directly.
    Use the safer and platform-neutral 'extend_user_env' instead.'''
    # !! We're messing with the Windows Registry here, edit with care !!
    import _winreg
    from _winreg import OpenKey, QueryValueEx, SetValueEx, CloseKey
    user_env = OpenKey( _winreg.HKEY_CURRENT_USER, 'Environment',
                        0, _winreg.KEY_ALL_ACCESS                   )
    try:
        old_value, old_value_type = QueryValueEx(user_env, name)
        assert old_value_type in (_winreg.REG_SZ, _winreg.REG_EXPAND_SZ)
    except WindowsError:
        old_value, old_value_type = '', _winreg.REG_SZ
    if not old_value or mode == 'o':
        new_value = value
    elif mode == 'a':
        new_value = os.pathsep.join((old_value, value))
    else: # mode == 'p'
        new_value = os.pathsep.join((value, old_value))
    if old_value_type == _winreg.REG_SZ and value.find('%') != -1:
        new_value_type = _winreg.REG_EXPAND_SZ
    else:
        new_value_type = old_value_type
    SetValueEx(user_env, name, 0, new_value_type, new_value)
    CloseKey(user_env)

def extend_user_env_posix (name, value, mode):
    '''NEVER call this function directly.
    Use the safer and platform-neutral 'extend_user_env' instead.'''
    # It's sloppy to just append another export statement, but it
    # works for the time being.
    profile = open(expanduser('~/.profile'), 'a')
    if mode == 'a':
        profile.write('\nexport {0}=${0}:{1}\n'.format(name, value))
    elif mode == 'p':
        profile.write('\nexport {0}={1}:${0}\n'.format(name, value))
    else: # mode == 'o'
        profile.write('\nexport {0}={1}\n'.format(name, value))
    profile.close()

def install ( ):
    # invariant: RED_SPIDER_ROOT is the working directory and is read/writeable
    install_rsshell()
    for dir in (bin_dir, lib_dir, build_dir, cfg_dir, work_dir):
        if not exists(dir):
            os.mkdir(dir)
    install_docs(documented_cmds)
    # Installing from within Python works fine as long as we only need to copy
    # some files, but this will become unmanageable if we also have to compile
    # C++, Haskell, etcetera.
    # So in the future the part below should be taken care of by some external
    # build tool, called from here.
    print(install_patience_msg)
    if os.name == 'nt':  # Windows
        install_scripts(executable_scripts, executable_scripts)
    else:                # POSIX assumed
        install_scripts(    executable_scripts,
                            map(lambda x: splitext(x)[0], executable_scripts)
                        )
    install_python_modules(python_modules)
    # add more of such steps if that's feasible and no build system is available

def install_rsshell ( ):
    if not exists(src_dir):
        print(no_src_panic_msg)
        sys.exit(1)
    fname = 'rsshell.py'
    src_file = join(src_dir, fname)
    if not exists(src_file):
        print(no_rsshell_warning_msg.format(join('src', fname)))
        return
    if os.name != 'nt':  # POSIX assumed
        fname = splitext(fname)[0]
    if not exists(extbin_dir):
        os.mkdir(extbin_dir)
        # assumption: if it doesn't exist it also isn't in the PATH
        extend_user_env('PATH', abspath(extbin_dir), 'a')
    bin_file = join(extbin_dir, fname)
    copy2(src_file, bin_file)
    if os.name == 'nt' and '.py' not in os.getenv('PATHEXT'):
        fwd = open(splitext(bin_file)[0] + '.cmd', 'w')
        fwd.write(windows_rsshell_forward_script.format(abspath(bin_file)))
        fwd.close()
    print(rsshell_install_success_msg.format(bin_file))

def install_scripts (src_names, bin_names):
    # if the program reaches this point, src_dir and bin_dir exist for sure
    for src_name, bin_name in zip(src_names, bin_names):
        src_file = join(src_dir, src_name)
        if not exists(src_file):
            print(script_not_found_msg.format(src_name))
        else:
            bin_file = join(bin_dir, bin_name)
            copy2(src_file, bin_file)
            if not os.access(bin_file, os.X_OK):
                from stat import S_IXUSR, S_IXGRP, S_IXOTH
                mode = os.stat(bin_file).st_mode
                os.chmod(bin_file, mode | S_IXUSR | S_IXGRP | S_IXOTH)

def install_python_modules (modules):
    # if the program reaches this point, lib_dir exists for sure
    # ideally the modules in lib should be optimized, but we can fix that later
    for module in modules:
        dir, module_name = module.split('/')
        source_file = join(dir, module_name)
        # note: on Windows, join(dir, module_name) != module
        if not exists(source_file):
            print(script_not_found_msg.format(source_file))
        else:
            target_file = join(lib_dir, module_name + 'c')
            py_compile.compile(source_file, target_file)

def install_docs (docs):
    docfile = open('config/doc.txt', 'w')
    for cmd in documented_cmds:
        docfile.write(cmd[0] + " " + cmd[1] + "\n")

windows_rsshell_forward_script = """
@echo off
start "rsshell" /b /wait {0} %*
"""

welcome_msg = """
Hi. I'll setup the Red Spider Project for you."""

root_guess_msg = """
I'm guessing that {0}
is the root directory of your copy of the Red Spider Project.

If I'm wrong please enter the correct path, otherwise just hit enter.
--> """

user_path_fail_msg = """
Sorry, I can't open {0} .
Care to try again?
--> """

user_path_end_msg = """
Using {0}
as the root directory."""

root_rw_fail_msg = """
Damn. I don't have sufficient permissions to use that path.
That ends it, then.
"""

reinstall_choice_msg = """
It seems that you have run the installer before.
Would you like me to reinstall everything anyway? (y/n) --> """

new_install_choice_msg = """
I think you haven't run the installer before (at least not in this
root). Would you like me to do it now? (y/n) --> """

no_src_panic_msg = """
Oh my. There is no '{0}' subdirectory within the root?!
Please come back when you've checked that everything is in its
proper place!
""".format(src_dir)

no_rsshell_warning_msg = """
Warning: I couldn't find '{0}' in the root.
I'll skip the installation of rsshell."""

rsshell_install_success_msg = """
Hey, listen up. I've installed rsshell for you in {0} .
I also added it to your PATH, so from your next logon onwards you can
run it by just punching 'rsshell' into your leopard. It will launch a
subshell with some convenient environment variables that the other
programs rely on.

In addition the root has been saved to RED_SPIDER_ROOT, so after your
next logon that one will be permanently available as well.

Note for unixy systems: opening a new terminal window might count as a
new logon. If you run me often, you may want to clean up ~/.profile
once in a while..."""

install_patience_msg = """
Please wait while I install the rest..."""

script_not_found_msg = """I can't find {0} so I'll skip it."""

farewell_msg = """
We're done! But wait, don't walk away yet.
This is important: if you ever decide to move the Red Spider Project
to another directory, you'll have to run me again or otherwise my dear
friend rsshell might choke and call you an inconsiderate boor.
Just kidding! But seriously, do come back to me if you ever move the
project to somewhere else.
"""

if __name__ == '__main__':
    main()

# Not used anymore, but kept here for future reference. ;-)"
winreg_path_unexpected_type_msg = """
Uhoh. Your 'Environment' setting in the Registry is of type {0},
which is not what I expected. I'll try my best to bring this to a good
end, but don't be surprised if velociraptors jump out of your fridge
tomorrow."""
