# -*- coding: utf-8 -*-

"""Test the integration of the python package “tmep”."""

import unittest
import helper


class TestFunctions(unittest.TestCase):

    def test_ifdefempty_empty_existent_field(self):
        out = helper.call_bin('--dry-run', '--format',
                              '%ifdefempty{mb_workid,_empty_,_notempty_}',
                              helper.get_testfile('files', 'album.mp3'))
        self.assertTrue('_empty_' in str(out))

    def test_ifdefempty_empty_nonexistent_field(self):
        out = helper.call_bin('--dry-run', '--format',
                              '%ifdefempty{xxx,_empty_,_notempty_}',
                              helper.get_testfile('files', 'album.mp3'))
        self.assertTrue('_empty_' in str(out))

    def test_ifdefempty_notempty(self):
        out = helper.call_bin('--dry-run', '--format',
                              '%ifdefempty{title,_empty_,_notempty_}',
                              helper.get_testfile('files', 'album.mp3'))
        self.assertTrue('_notempty_' in str(out))


if __name__ == '__main__':
    unittest.main()
