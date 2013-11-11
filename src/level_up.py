#!/usr/bin/env python

# Copyright 2012 Alex Hammel
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

from __future__ import print_function
import sys
import os
try:
    from tkinter import *
except:
    from Tkinter import *
import argparse

#
# Some definitions:
#
#   The _line count_ for a language is the number of source lines of code
#     written in that language, not counting comments or blank lines.
#
#   The _score_ for a language is the line count divided by the C-equivalent
#     KLOC scaling factor (see below).
#
#   The _level_ is a rough, unreliable, and entirely humorous reflection of a
#     hacker's ability in a given language, given the combined _score_ of all of
#     the code she or he has written in that language. The analogy is to the
#     concept of a level in role-playing games, where the player character might
#     gain a level in strength after caving in a certain number of goblin
#     skulls. Levels get proportionally harder to attain: it's easier to go from
#     level 2 to level 3 than to go from level 3 to level 4.
#
#   If you're curious about the score required to attain a particular level
#   (cheater), open up a python shell in the level_up directory and do this:
#
#         > import level_up
#         > levels = make_level_generator()
#         > next(levels)
#
#   Repeat the last command until your curiosity is satisfied.
#
#   Complaints to the effect that level_up fails to reflect your 133t ski11z
#   should be redirected to /dev/null
#


# This is the C-equivalent KLOC conversion table. Based on task-controlled
# benchmarks (http://shootout.alioth.debian.org/), it takes about 2300 lines of
# Ada to complete a task that could be accomplished with 1000 lines of C,
# for example. The ridiculous number of significant digits is left in to
# add a little randomness.

C_EQUIV_KLOC = {"Ada": 2.321176,
                "C": 1,
                "C#": 1.250588,
                "C++": 1.694118,
                "Clean": 0.9811765,
                "Clojure": 1.268824,
                "Erlang": 0.9876471,
                "F#": 0.9411765,
                "Fortran": 1.137647,
                "Go": 0.8235294,
                "Haskell": 1.356471,
                "Java": 1.458824,
                "JavaScript": 0.5494118,
                "Lisp": 1.857647,
                "Lua": 0.6529412,
                "Mozart/Oz": 0.6576471,
                "OCaml": 1.022353,
                "Pascal": 1.197647,
                "Perl": 0.5270588,
                "PHP": 0.5682353,
                "Python": 0.7364706,
                "Scheme": 0.9376471,
                "Ruby": 0.4941176,
                "Smalltalk": 0.8682353
                }

# In the comment syntax table, the first element of the triple is the single
# line comment syntax, and the nex two are the multi-line comment opening
# and closing

COMMENT_SYNTAX = {"Ada": ("--", None, None),
                  "C": ("//", "/*", "*/"),
                  "C#": ("//", "/*", "*/"),
                  "C++": ("//", "/*", "*/"),
                  "Clojure": (";", None, None), #Other comment syntaxes are
                                                #supported, but semicolon
                                                #comments seem to be most
                                                #common. Who uses clojure,
                                                #anyway?
                  "Erlang": ("%", None, None),
                  "F#": ("//", "(*", "*)"),
                  "Fortran": ("C", None, None),
                  "Go": ("//", "/*", "*/"),
                  "Haskell": ("--", "{-", "-}"),
                  "Java": ("//", "/*", "*/"),
                  "JavaScript": ("//", "/*", "*/"),
                  "Lisp": (";", "#|", "|#"),
                  "Lua": ("--", "--[[", "--]]"),
                  "OCaml": (None, "(*", "*)"),
                  "Pascal": (None, "(*", "*)"),
                  "Perl": ("#", ("=begin", "=for"), "=cut"),
                  "PHP": ("//", "/*", "*/"),
                  "Python": ("#", None, None),
                  "Scheme": (";", "#|", "|#"),
                  "Ruby": ("#", "=begin", "=end"),
                  "Smalltalk": (None, '"', '"')
                  }

EXTENSIONS = {".adb": "Ada",
              ".c": "C",
              ".cs": "C#",
              ".cpp": "C++",
              ".clj": "Clojure",
              ".erl": "Erlang",
              ".fs": "F#",
              ".f": "Fortran",
              ".go": "Go",
              ".hs": "Haskell",
              ".java": "Java",
              ".js": "JavaScript",
              ".lisp": "Lisp",
              ".lua": "Lua",
              ".ml": "OCaml",
              ".pas": "Pascal",
              ".pl": "Perl",
              ".php": "PHP",
              ".py": "Python",
              ".scm": "Scheme",
              ".rb": "Ruby",
              ".st": "Smalltalk"
              }

SCORE_FILE = os.path.join(os.getenv("RED_SPIDER_ROOT"),
                          "work",
                          "level_up",
                          "scores"
                          )

class LanguageError(ValueError):
    """The exception raised when a language is not supported"""

class LevelUpWindow(Frame):
    """A window displaying a congratulatory message upon a level up event"""

    def create_widgets(self, message, button_text):
        self.TEXT = Label(self)
        self.TEXT["text"] = message

        self.TEXT.pack()


        self.BUTTON = Button(self)
        self.BUTTON["text"] = button_text
        self.BUTTON["command"] = self.quit

        self.BUTTON.pack()

    def __init__(self, master, message="", button_text=""):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets(message, button_text)


def make_level_generator():
    """Yields the number of C-equivalent kLOCs needed to advance to the next
    level.

    """
    xp = 0
    level = 1
    while True:
        yield level, xp
        level += 1
        xp = level * 1000 * (level - 1) / 8


def level(score):
    """Given a value in C-equivalent LOCs, returns the level."""
    if score == 0:
        return 0
    l_gen = make_level_generator()
    while True:
        level, xp = next(l_gen)
        if score < xp:
            return level - 1


def language(filename):
    """Gets the language which the source code file filename was written in
    based on its extension.

    """
    name, ext = os.path.splitext(filename)
    if ext not in EXTENSIONS:
        raise LanguageError ("Error 1: file is not source code or language is"
                             "not supported.")
    return EXTENSIONS[ext]


def line_count(filename):
    """Returns a count of the number of lines in the file, not counting
    comments or blank lines, for supported source code files.

    """
    lang = language(filename)
    comment, begin_block_comment, end_block_comment = COMMENT_SYNTAX[lang]
    count = 0
    is_comment = False
    with open(filename) as source:
        for line in source:
            line = line.strip()
            # Are we in a block comment?
            if begin_block_comment and line.startswith(begin_block_comment):
                if end_block_comment not in line[len(begin_block_comment):]:
                    is_comment = True
            elif is_comment and end_block_comment in line:
                is_comment = False
                line = ''    # so the comment-ending line is not counted

            if comment and line.startswith(comment):
                pass
            elif line and not is_comment:
                count += 1
    return count


def get_line_counts(root_folder):
    """Recurses through the root directory, looking for source files of the
    supported languages. Returns a dictionary of the line counts of all such
    files, less comments and blank lines. Ignores files in hidden directories.

    """
    line_counts = {}
    file_list = []
    for root, sub_folders, files in os.walk(root_folder):
        for folder in sub_folders:
            if folder.startswith("."):
                sub_folders.remove(folder)
        for source_file in files:
            try:
                language(source_file)
            except LanguageError:
                continue
            file_path = os.path.join(root[len(root_folder):], source_file)
            root_folder_path = os.path.abspath(root_folder)
            # Files in subfolders are sometimes given prefixes for some reason:
            if os.path.isabs(file_path):
                file_path = file_path[1:]
            file_list.append(os.path.join(root_folder_path, file_path))

    for source_file in file_list:
        lang = language(source_file)
        line_counts.setdefault(lang, 0)
        line_counts[lang] += line_count(source_file)
    return line_counts


def get_scores(root_folder):
    """Like get_line_counts, only it normalizes the line counts according to the
    C_EQUIV_KLOC table.

    """
    counts = get_line_counts(root_folder)
    return {lang: counts[lang] / C_EQUIV_KLOC[lang] for lang in counts}


def update_score_file(line_counts, score_file, head=""):
    """Writes a table of line counts to the score_file. The head argument will
    typically be used to prepend the default directory to the score file.

    """
    with open(score_file, 'w') as sf:
        print(head, file=sf)
        for lang in sorted(line_counts):
            print(lang, line_counts[lang], file = sf)


def read_score_file(score_file):
    """Reads the counts of lines printed to a score_file by the
     udate_score_file command. Returns a dictionary of language scores.

     """
    line_counts = {}
    with open(score_file) as sf:
        root_dir = sf.readline().strip()
        for line in sf:
            lang, score = line.split()
            score = float(score)
            line_counts[lang] = score
    return (root_dir, line_counts)


def initialize_score_file(root_dir, score_file):
    """Makes a table of line counts in C-equivalent KLOCs and writes it
    to the score_file.

    """
    work_dir = os.path.split(score_file)[0]
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    line_counts = get_line_counts(root_dir)
    for lang in line_counts:
        line_counts[lang] /= C_EQUIV_KLOC[lang]
    update_score_file(line_counts, score_file, head = os.path.abspath(root_dir))


def update_scores(score_file):
    """Gets the current scores from the score file, updates them and raises a
    congratulatory message if a level-up has occured.

    """
    root_folder, old_scores = read_score_file(score_file)
    old_levels = {lang: level(old_scores[lang]) for lang in old_scores}
    new_scores = get_scores(root_folder)
    new_levels = {lang: level(new_scores[lang]) for lang in new_scores}
    congrats = ""

    for lang in sorted(old_levels):
        try:
            if old_levels[lang] < new_levels[lang]:
                congrats += "".join(["You have advanced to level ",
                                     str(new_levels[lang]),
                                     " in ", lang, "!\n"])
        except KeyError:
            pass

    if congrats:
        congrats = "Congratulations!\n\n" + congrats
        root = Tk()
        window = LevelUpWindow(root, message=congrats, button_text="Hooray!")
        root.mainloop()

    update_score_file(new_scores, score_file, head=os.path.abspath(root_folder))


def main():
    parser = argparse.ArgumentParser(description="Track your coding experience")
    parser.add_argument('-i','--initialize', action='store', nargs=1,
                        dest='init',
                        help="Initialize a score file for the specified folder")
    parser.add_argument('-l','--line-counts', action='store', nargs=1,
                        dest='count',
                        help="Show the code line counts for the directory")
    args = parser.parse_args()

    if args.count:
        counts = get_line_counts(args.count[0])
        for lang in sorted(counts):
            print(lang, ": ", counts[lang])
    elif args.init:
        initialize_score_file(args.init[0], SCORE_FILE)
    else:
        try:
            root_dir, scores = read_score_file(SCORE_FILE)
        except IOError:
            print("Score file not found. Call 'level_up -i <directory>' to"
                  " initialize a score folder, or 'level_up -h' for help")
            sys.exit(0)
        update_scores(SCORE_FILE)

if __name__ == '__main__':
    main()
