import unittest
import os
import helper as h


class TestDiskTrack(unittest.TestCase):

    def test_single_disc(self):
        meta = h.get_meta([
            'e', 'Everlast', 'Eat-At-Whiteys_2000', '02_Black-Jesus.mp3'
        ])
        self.assertEqual(meta['disctrack'], u'02')

    def test_double_disk(self):
        meta = h.get_meta([
            '_compilations',
            't',
            'The-Greatest-No1s-of-the-80s_1994',
            '2-09_Respectable.mp3'
        ])
        self.assertEqual(meta['disctrack'], u'2-09')

if __name__ == '__main__':
    unittest.main()
