#!/usr/bin/env python3

import unittest
from one_zoom.find_in_file import get_matches

def chunks_from_string(s, chunk_size):
    for i in range(0, len(s), chunk_size):
        yield s[i:i+chunk_size]

'''
Unit test for find_in_file.get_matches
'''
class TestGetMatches(unittest.TestCase):

    def run_get_matches(self, regex, window_size):
        s = "abcdefghijklmnopqrstuvwxyz" * 3
        iter = chunks_from_string(s, 26)

        return list(get_matches(iter, regex, window_size))

    def test_no_match(self):
        self.assertEqual(
            self.run_get_matches("123", 2),
            []
        )

    # Matches in the middle of the chunks
    def test_middle_string(self):
        self.assertEqual(
            self.run_get_matches("ijk", 2),
            [(8, 'ghijklm'), (34, 'ghijklm'), (60, 'ghijklm')]
        )

    # Matches at the start of the chunks
    def test_start_string(self):
        self.assertEqual(
            self.run_get_matches("ab", 3),
            [(0, 'abcde'), (26, 'xyzabcde'), (52, 'xyzabcde')]
        )

        self.assertEqual(
            self.run_get_matches("bc", 3),
            [(1, 'abcdef'), (27, 'yzabcdef'), (53, 'yzabcdef')]
        )

    # Matches at the end of the chunks
    def test_end_string(self):
        self.assertEqual(
            self.run_get_matches("yz", 3),
            [(24, 'vwxyzabc'), (50, 'vwxyzabc'), (76, 'vwxyz')]
        )

        self.assertEqual(
            self.run_get_matches("xy", 3),
            [(23, 'uvwxyzab'), (49, 'uvwxyzab'), (75, 'uvwxyz')]
        )

    # Matches overlapping two chunks
    def test_overlap_string(self):
        self.assertEqual(
            self.run_get_matches("za", 3),
            [(25, 'wxyzabcd'), (51, 'wxyzabcd')]
        )

        self.assertEqual(
            self.run_get_matches("yzab", 3),
            [(24, 'vwxyzabcde'), (50, 'vwxyzabcde')]
        )

        self.assertEqual(
            self.run_get_matches("zabcdefgh", 3),
            [(25, 'wxyzabcdefghijk'), (51, 'wxyzabcdefghijk')]
        )

        self.assertEqual(
            self.run_get_matches("vwxyza", 3),
            [(21, 'stuvwxyzabcd'), (47, 'stuvwxyzabcd')]
        )

        self.assertEqual(
            self.run_get_matches("vwxyza", 0),
            [(21, 'vwxyza'), (47, 'vwxyza')]
        )
