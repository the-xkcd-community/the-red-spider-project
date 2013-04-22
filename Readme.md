The Red Spider Project
----------------------

[http://the-xkcd-community.github.com/the-red-spider-project]


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

The project is like a small, self-contained operating system layered on top of your actual operating system. People can add programs at will. It's an open-ended process without deadlines or a final goal and we're very open-minded.


### What ###

When you run `rsshell` the following commands are available to you.

- `xkcd-fetch`: Manages an offline xkcd comic database for you. Run
  with `-h` for help.
- `xkcd-search`: Searches the database from `xkcd-fetch` for keywords.
  Run with `-h` for help.
- `json-parse`: Manually inspect JSON files. Undocumented.

The following commands are expected to be added soon:

- `level_up`: An RPG-style lines-of-code counter which pops up a
  "level up" message when you pass a milestone in a programming
  language.
- `summon`: A generic file/URL launcher which can handle any file type
  your underlying system supports.


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
