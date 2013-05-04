# Copyright 2012, 2013 Alex Hammel
# Licensed under the Red Spider Project License.
# See the License.txt that shipped with your copy of this software for details.

from __future__ import print_function
import level_up
import unittest
import glob
import os

test_files = glob.glob(os.path.join("test", "*"))

su_langs = ["Ada", "C", "C#", "C++", "Clojure", "Erlang", "F#",
            "Fortran", "Go", "Haskell", "Java", "JavaScript", "Lisp", "Lua",
            "OCaml", "Pascal", "Perl", "PHP", "Python", "Scheme",
            "Ruby", "Smalltalk"]

line_counts = {x: 2 for x in su_langs}

subdir_line_counts = {x: 2 for x in su_langs}
for lang in ["C","C++","Clojure","C#"]: # In the subfolder
    subdir_line_counts[lang] += 2

test_dir = os.path.abspath("test")

test_score_file = os.path.join("test_score_files", "test_score_file")
my_score_file = os.path.join("test_score_files", "my_score_file")
my_score_file_c = os.path.join("test_score_files", "my_score_file_c")

with open(my_score_file, "w") as f:
    print(os.path.join(os.getcwd(),"test"), file=f)
    print("""Ada 2
C 4
C# 4
C++ 4
Clojure 4
Erlang 2
F# 2
Fortran 2
Go 2
Haskell 2
Java 2
JavaScript 2
Lisp 2
Lua 2
OCaml 2
PHP 2
Pascal 2
Perl 2
Python 2
Ruby 2
Scheme 2
Smalltalk 2""", file=f)


class TestLevelUpFunctions(unittest.TestCase):

    def test_level(self):
        test_cases = [(0, 0),
                      (1, 1),
                      (249, 1),
                      (250, 2),
                      (5000, 6)]
        for score, level in test_cases:
            self.assertEqual(level_up.level(score), level)


    def test_language(self):
        """Tests that the language function correctly deduces the language
        of a source code file from it's extension, or raises a LanguageError
        if the language is unsupported.

        """
        for f in test_files[0]:    # First item is a folder
            self.assertRaises(level_up.LanguageError, level_up.language, f)

        self.assertEqual(set([level_up.language(f) for f in test_files[1:]]),
                         set(su_langs))


    def test_line_count(self):
        """All the files in the test folder have two lines of code and some
        comments.

        """
        self.assertEqual(line_counts,
                         {level_up.language(f): level_up.line_count(f)
                            for f in test_files[1:]})

    def test_get_line_counts(self):
        """Tests that the get_line_counts function works as intended. If there
        are too few lines for a certain language, the function isn't descending
        into subdirectories properly. If there are too many, it isn't ignoring
        hidden folders.

        """
        self.assertEqual(subdir_line_counts, level_up.get_line_counts("./test"))


    def test_get_scores(self):
        """Tests that the get_scores function works as intended: esp. that it
        ignores hidden folders.

        """
        self.assertEqual(level_up.get_scores("test"),
                         {x: subdir_line_counts[x] / level_up.C_EQUIV_KLOC[x]
                             for x in subdir_line_counts})


    def test_update_score_file(self):
        level_up.update_score_file(subdir_line_counts, test_score_file,
                                   head=test_dir)
        machine_score_file = open(test_score_file)
        by_hand_score_file = open(my_score_file)
        self.assertEqual(machine_score_file.readlines(),
                         by_hand_score_file.readlines())
        machine_score_file.close()
        by_hand_score_file.close()

    def test_read_score_file(self):
        self.assertEqual(level_up.read_score_file(my_score_file),
                         (test_dir, subdir_line_counts))

    def test_initialize_score_file(self):
        level_up.initialize_score_file("test_c" ,my_score_file_c)
        self.assertEqual(level_up.read_score_file(my_score_file_c),
                         (os.path.abspath("test_c"), {"C": 5}))

    def test_update_scores(self):
        with open(os.path.join("test_c", "temp.c"), "w") as f:
            for n in range(0,250):
                print("A line of C", file=f)
        level_up.update_scores(my_score_file_c)
        self.assertEqual(level_up.read_score_file(my_score_file_c),
                         (os.path.abspath("test_c"), {"C": 255}))
        os.remove(os.path.join("test_c", "temp.c"))
