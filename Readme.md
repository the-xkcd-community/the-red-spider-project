The Red Spider Project
----------------------

[http://the-xkcd-community.github.com/the-red-spider-project]


### Why ###

Because we like to combine our love for the xkcd comic with our love
for coding, and we want to share the experience.


### Who ###

Currently, "we" are mostly members of the [xkcd
forums](http://forums.xkcd.com). However, anyone is welcome to join
in.


### How ###

By keeping an ongoing project to which people can add programs at
will. By "program", we mean *any* program. It may be any size and it
may be written in any programming language, though preferably
portable. Most of the programs in our project will probably be
amusing, interesting, touching or a combination of those, either
because of the source code, because of the output, or both. Likely,
most programs will also be small. Anything is welcome except malware.

We put some emphasis on command line programs. The programs may be
interconnected with basic plumbing. We'll put some guidelines and
infrastructure in place to keep things smooth, as we see the need.
Other than that, it's basically liberty above all things!


### When ###

We started in March 2012. In the first few months we spent most of our
effort on the infrastructure. In July we were treated to some splendid
logo designs and we got a homepage. In December we launched our IRC
channel. In the meanwhile several members have been working on various
subprojects, mostly in short bursts of activity.

In the near future we may expect wiki content, a few big improvements
to the infrastructure, and an overarching role playing game, among
other things.


### What ###

__License__: we have a liberal license which might strongly remind you
of the MIT license (that's not a coincidence). See License.txt for
more information.

__Platform support__: for the time being we just try to make sure
that our stuff runs on the most popular platforms. You'll need to
install some additional software, see Dependencies.md for more
information.

__Testing__: we use the issue tracker from GitHub to ask each other a
favour. See Platforms.md for more information.
**Note**: nothing is thoroughly tested, we just make sure that things
behave as expected under expected conditions.

__Branching__: `master` is our sacred branch. It's supposed to contain
only reasonably well-behaved programs (say: more or less stable,
portable and easy to quit). Nonetheless you're encouraged to merge
often into `master`. Do whatever you want in the other branches, but
please do observe some common rules of sensibility. For example, don't
merge everything into everything.

__Building__: currently we have a crude but effective setup script
that copies executable scripts to the right locations and pre-compiles
Python modules. In the future, we hope to use a more professional
build tool which can do that *and* compile things. Perhaps CMake.

__Directory layout__: we chose `src`, `include`, `doc`, `test`,
`build`, `lib`, `bin`, `config` and `work` (if the names don't tell
you what they're meant for, don't hesitate to ask). Programs will be
pooled enjoyably together unless a single program consists of many
files within the same directory (for some subjective value of "many"),
in which case we'll give it a dedicated subdirectory.

__Programs__: so far concrete work has been done on `rsshell`, which
launches a convenient environment for other Red Spider programs, as
well as on an xkcd comic fetcher, an xkcd comic regex searcher, an
adventure shell and an adventure web browser. More ideas are waiting
to be implemented.

__Communication__: we have our little [thread at the xkcd
forums](http://forums.xkcd.com/viewtopic.php?f=11&t=81969) for
updates, discussion and archaeology, and there's the [issue
tracker](https://github.com/the-xkcd-community/the-red-spider-project/issues).
Some of the many other options are to comment on commits or to write
something on the wiki.


### How to ###

Here's the place to find, submit or edit guidelines, rules of thumb,
suggested procedures, and so on and so forth.

A general rule of thumb: look at what the others do.


#### Obtaining the project ####

Easy. Either download the source tree as a zip file from the GitHub
project page, or install Git (if you don't have it yet) and run the
following command in the directory of your choice:

    git clone git://github.com/the-xkcd-community/the-red-spider-project.git

Alternatively, if you plan to contribute to the project you may create
a GitHub account (if you don't have one yet), fork the project and
clone your fork to your computer instead.


#### Installing the software ####

Run `./setup.py` from the root directory of your copy of the Red
Spider Project (you can leave out the `./` part in Windows). Read what
it says and follow the instructions.


#### Running the software ####

Run the `rsshell` command that you installed with `setup.py`. After
that you can run any program from the `bin` directory by just typing
its name. Alternatively, you may also `cd` to the `src` directory and
execute development versions of the programs in there. Leave the
subshell with `exit`.


#### Creating something of your own ####

Pull in the latest changes to `master`, fork a new branch and hack
away. Take your time, we don't do deadlines. :-)

In source code files, please add something like the following in a
comment at the top:

    Copyright YYYY __authors_of_major_contributions__
    Licensed under the Red Spider Project License.
    See the License.txt that shipped with your copy of this software for details.

    Acknowledgements: X provided idea A, Y provided idea B.
    Minor contributions were made by Z/by several authors;
    please refer to the Authors.txt that shipped with your copy of this software.

Where `YYYY` starts off as the current year and
`__authors_of_major_contributions__` starts off as you, by definition.
More years and authors may be added later. The lines with
acknowledgements are optional, of course.


#### Integrating your stuff with the rest of the project ####

Finally, here's the really exciting stuff. You'll need to do some or
all of the following:

 -  If you wrote anything that should be copied to `bin` or `lib`
    during installation, add it to lists at the top of `setup.py`.
 -  Push your branch to your public fork of the project.
 -  If you edited any Markdown files, check that they render correctly
    on GitHub.
 -  Ask your fellow project participants for their opinions, if
    relevant.
 -  Submit a test request to the issue tracker, for the platforms that
    you couldn't test by yourself. See what happens.
 -  Once your branch works on all platforms, pull in the latest
    changes to `master` and merge your own branch into it. Push that
    to your public fork and request that it be pulled into the main
    repository.
 -  Somebody will probably grant your request.

Once your branch has been fully merged into the master branch, others
can start using your work. Of course, nothing stops you from forking
another branch to add more features in the meanwhile!


#### Editing somebody else's stuff ####

First of all, please check whether the original author is currently
working on it. Next, create a new branch to commit your changes to.

If they're not working on it: edit, have it tested, have it pulled.
Business as usual.

If you're going to cooperate with them: add their public fork as a
remote, have them add your public fork too, discuss, and push/pull
your changes back and forth. Other than that, business as usual.

Otherwise: you're about to create a parallel alternative version, so
be aware that something special will need to be done before you can
merge your changes. Perhaps give your variant of the program a
different name.

Depending on the nature of your contributions, you should probably
either add your name to the copyright notices of the files you edited
or include it in the Authors.txt. For program source files, a guiding
question could be the following: "Did I contribute to the program
logic?"


### Credits ###

Julian coined the idea, qubital set up the GitHub repository, Neil
wrote most of the initial infrastructure code and Joey designed the
logo proposals. Please also refer to the copyright notices in the
source files and to the Authors.txt, which lists all the authors who
decided not to add their name to some file they edited.

Please add your name to the Authors.txt if it isn't in there while it
should.
