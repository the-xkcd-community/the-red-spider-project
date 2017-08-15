The Red Spider Project
----------------------

https://github.com/the-xkcd-community/the-red-spider-project


### Why ###

Because we like to combine our love for the xkcd comic with our love
for coding, and we want to share the experience.


### How ###

For the impatient: fork the project, then

    git clone git@github.com:yourname/the-red-spider-project.git redspider
    cd redspider
    git remote add upstream git://github.com/the-xkcd-community/the-red-spider-project.git
    git config branch.master.remote upstream
    git config branch.master.merge refs/heads/master
    ./setup.py
    rsshell

The project is like a small, self-contained operating system layered
on top of your actual operating system. People can add programs at
will. It's an open-ended process without deadlines or a final goal and
we're very open-minded. Anyone who wants to contribute can join.


### What ###

When you run `rsshell` it displays a list of available commands. You
can review that list at any time by running `rshelp`. `rshelp <topic>`
will show you documentation for `<topic>` if available. This works for
most commands.

There's always work in progress. If you want to know what is going on
or you want to know what *you* can do, the issue tracker and the wiki
are your places to be.


### Where ###

- [Home page](http://the-xkcd-community.github.com/the-red-spider-project)
- [Issue tracker](https://github.com/the-xkcd-community/the-red-spider-project/issues)
- [Wiki](https://github.com/the-xkcd-community/the-red-spider-project/wiki)
- [IRC channel: #redspider at foonetic.net](irc://irc.foonetic.net/redspider)
- [xkcd forums thread](http://forums.xkcd.com/viewtopic.php?f=11&t=81969)


### When ###

We started in March 2012. In the first few months we spent most of our
effort on the infrastructure. In July we were treated to some splendid
logo designs and we got a homepage. In December we launched our IRC
channel and in March 2013 the wiki took off. The builtin documentation
was introduced in October 2013.


### Who ###

Julian coined the idea, qubital set up the GitHub repository, Neil
wrote most of the initial infrastructure code and Joey designed the
logo proposals. Please also refer to the copyright notices in the
source files and to the Authors.txt, which lists all the authors who
decided not to add their name to some file they edited.
