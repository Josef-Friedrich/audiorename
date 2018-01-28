# -*- coding: utf-8 -*-

"""Test the integration of the python package “tmep”."""

import unittest
import helper


class TestFunctions(unittest.TestCase):

    @unittest.skip('Work to do')
    def test_ifdefempty(self):
        out = helper.call_bin('--dry-run', '--format',
                              '%ifdefempty{xxx,_empty_,_notempty_}',
                              helper.copy_to_tmp('files', 'album.mp3'))
        self.assertTrue('_empty_' in str(out))


if __name__ == '__main__':
    unittest.main()
