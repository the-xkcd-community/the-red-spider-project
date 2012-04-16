#! /usr/bin/env python
from __future__ import print_function

__doc__ = ''' setup.py
Initial setup script for the Red Spider Project

Copyright 2012 Julian Gonggrijp
Licensed under the Red Spider Project License.
See the License.txt that shipped with your copy of this software for details.
'''

from future_builtins import zip, map
import os
from os.path import exists, join, split, splitext
import shutil
import py_compile
import sys
sys.path.append('./src')
import rsshell

executable_scripts = 'json-parse.py xkcd-fetch.py xkcd-search.py'.split()

python_modules = 'src/xkcd-fetch.py'.split()

def main ( ):
    print(welcome_msg)
    red_spider_root = verify_root()
    save_user_config(red_spider_root)
    build_dir = join(red_spider_root, 'build')
    # existence of the build dir is the natural indicator of a previous install
    user_pref = raw_input(
        reinstall_choice_msg if exists(build_dir) else new_install_choice_msg
    )
    if (user_pref.find('y') != -1 or user_pref.find('Y') != -1):
        install(red_spider_root)
    print(farewell_msg)

def verify_root ( ):
    root_path = rsshell.red_spider_root
    user_path = raw_input(root_guess_msg.format(root_path))
    if user_path:
        user_path = os.path.abspath(os.path.expanduser(user_path))
        while not exists(user_path):
            user_path = raw_input(user_path_fail_msg.format(user_path))
            user_path = os.path.abspath(user_path)
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

def save_user_config (rs_root):
    if os.name == 'nt':  # Windows
        config_folder = join(os.getenv('APPDATA'), 'xkcdRedSpider')
        config_file = join(config_folder, 'config.txt')
    else:                # POSIX assumed
        config_folder = join(os.getenv('HOME'), '.config')
        config_file = join(config_folder, 'xkcdRedSpider')
    # We could go fancy and use JSON to store the external
    # configuration, but simple plaintext will do for the time being.
    # Afterall, we're storing only one string!
    if not exists(config_folder):
        os.mkdir(config_folder)
    config_handle = open(config_file, 'w')
    config_handle.write(rs_root)  # no line ending; probably important
    config_handle.close()
    print(config_file_stored_msg.format(config_file))

def install (rs_root):
    # invariant: rs_root exists and is read/writeable
    src_dir = join(rs_root, 'src')
    bin_dir = join(rs_root, 'bin')
    install_rsshell(src_dir, bin_dir)  # creates the dirs if they don't exist
    lib_dir = join(rs_root, 'lib')
    if not exists(lib_dir):
        os.mkdir(lib_dir)
    build_dir = join(rs_root, 'build')
    if not exists(build_dir):
        os.mkdir(build_dir)
    # Installing from within Python works fine as long as we only need to copy
    # some files, but this will become unmanageable if we also have to compile
    # C++, Haskell, etcetera.
    # So in the future the part below should be taken care of by some external
    # build tool, called from here.
    print(install_patience_msg)
    if os.name == 'nt':  # Windows
        install_scripts(    src_dir, bin_dir,
                            executable_scripts, executable_scripts  )
    else:                # POSIX assumed
        install_scripts(    src_dir, bin_dir, executable_scripts,
                            map(lambda x: splitext(x)[0], executable_scripts)
                        )
    install_python_modules(rs_root, lib_dir, python_modules)
    # add more of such steps if that's feasible and no build system is available

def install_rsshell (src_dir, bin_dir):
    if not exists(src_dir):
        print(no_src_panic_msg)
        sys.exit(1)
    if not exists(bin_dir):
        os.mkdir(bin_dir)
    fname = 'rsshell.py'
    src_file = join(src_dir, fname)
    if not exists(src_file):
        print(no_rsshell_warning_msg.format(join('src', fname)))
        return
    if os.name != 'nt':  # POSIX assumed
        fname = splitext(fname)[0]
    bin_file = join(bin_dir, fname)
    shutil.copy2(src_file, bin_file)
    if os.name == 'nt':  # Windows
        if os.getenv('PATHEXT', '').find('.py') != -1:
            # Python commands can be run without typing the file extension,
            # like on POSIX with a shebang and the executable bit ON
            fname = splitext(fname)[0]
            bin_file = splitext(bin_file)[0]
    print(rsshell_install_success_msg.format(bin_file, fname))

def install_scripts (src_dir, bin_dir, src_names, bin_names):
    # if the program reaches this point, src_dir and bin_dir exist for sure
    for src_name, bin_name in zip(src_names, bin_names):
        src_file = join(src_dir, src_name)
        if not exists(src_file):
            print(script_not_found_msg.format(src_name))
        else:
            shutil.copy2(src_file, join(bin_dir, bin_name))

def install_python_modules (rs_root, lib_dir, modules):
    # if the program reaches this point, lib_dir exists for sure
    # ideally the modules in lib should be optimized, but we can fix that later
    for module in modules:
        dir, module_name = module.split('/')
        source_file = join(rs_root, dir, module_name)
        if not exists(source_file):
            print(script_not_found_msg.format(join(dir, module_name)))
        else:
            target_file = join(lib_dir, module_name + 'c')
            py_compile.compile(source_file, target_file)

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

config_file_stored_msg = """
I stored the path to {0} ."""

reinstall_choice_msg = """
It seems that you have run the installer before.
Would you like me to reinstall everything anyway? (y/n) --> """

new_install_choice_msg = """
I think you haven't run the installer before (at least not in this
root). Would you like me to do it now? (y/n) --> """

no_src_panic_msg = """
Oh my. There is no 'src' subdirectory within the root?!
Please come back when you've checked that everything is in its
proper place!
"""

no_rsshell_warning_msg = """
Warning: I couldn't find '{0}' in the root.
I'll skip the installation of rsshell."""

rsshell_install_success_msg = """
Hey, listen up. I've installed rsshell for you.
From now on you can run it from
{0} .
It will launch a subshell with some convenient environment variables
that the other programs rely on. If you want you can copy or move it
to some place where your shell can always find it (i.e. in your PATH)
so you can always get there by just punching '{1}' into your leopard."""

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
