This document lists the platforms that should be supported, and
outlines how to have them supported.


### Target platforms ###

Anything on branch `master` should be stable and support at least the
following platforms:

 -  Windows with cmd.exe (tested on Windows 7);
 -  Mac OS X with bash (tested on 10.6);
 -  Linux with bash (tested on Fedora 16).

Exceptions are possible, please discuss such cases with the others.

Other platforms might work too, we just don't take effort to ensure
that. For example PowerShell on Windows works, though inconveniently.

More platform support can be added if testers are available. Let us
know if you want to test for a new platform.


### Ensuring that your program supports these platforms ###

When you think it's time to merge your stuff into master, [submit an
issue to the main project on
GitHub](https://github.com/the-xkcd-community/the-red-spider-project/issues).
Tell us where we can find your branch and which platforms still need
to be tested. Also make sure that it's clear *how* to perform the
testing. When your branch appears all clear, merge it into your own
master branch and submit a pull request.


### Reporting failing platform support ###

If you find that something on the master branch doesn't support your
platform while it should, please submit an issue.
