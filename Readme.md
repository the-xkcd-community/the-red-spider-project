The Red Spider Project
----------------------

[http://the-xkcd-community.github.com/the-red-spider-project]


### Why ###

Because we like to combine our love for the xkcd comic with our love
for coding, and we want to share the experience.


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


### What ###

__Branching__: `master` is our sacred branch. It's supposed to contain
only reasonably well-behaved programs (say: more or less stable,
portable and easy to quit). Nonetheless you're encouraged to merge
often into `master`. Do whatever you want in the other branches, but
please do observe some common rules of sensibility. For example, don't
merge everything into everything.

__Directory layout__: we chose `src`, `include`, `doc`, `test`,
`build`, `lib`, `bin`, `config` and `work` (if the names don't tell
you what they're meant for, don't hesitate to ask). Programs will be
pooled enjoyably together unless a single program consists of many
files within the same directory (for some subjective value of "many"),
in which case we'll give it a dedicated subdirectory.


### How to ###

A general rule of thumb: look at what the others do.


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


### When ###

We started in March 2012. In the first few months we spent most of our
effort on the infrastructure. In July we were treated to some splendid
logo designs and we got a homepage. In December we launched our IRC
channel. In the meanwhile several members have been working on various
subprojects, mostly in short bursts of activity.

In the near future we may expect wiki content, a few big improvements
to the infrastructure, and an overarching role playing game, among
other things.


### Who ###

Julian coined the idea, qubital set up the GitHub repository, Neil
wrote most of the initial infrastructure code and Joey designed the
logo proposals. Please also refer to the copyright notices in the
source files and to the Authors.txt, which lists all the authors who
decided not to add their name to some file they edited.
