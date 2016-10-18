import unittest
import os
from audiorename import meta


dir_test = os.path.dirname(os.path.abspath(__file__))
dir_real_world = os.path.join(dir_test, 'real-world')


def get(path):
    path_list = [dir_test, 'real-world'] + path
    return os.path.join(*path_list)


def get_meta(path):
    m = meta.Meta(get(path))
    return m.getMeta()


class TestDiskTrack(unittest.TestCase):

    def test_single_disc(self):
        meta = get_meta([
            'e', 'Everlast', 'Eat-At-Whiteys_2000', '02_Black-Jesus.mp3'
        ])
        self.assertEqual(meta['disctrack'], u'02')

    def test_double_disk(self):
        meta = get_meta([
            '_compilations',
            't',
            'The-Greatest-No1s-of-the-80s_1994',
            '2-09_Respectable.mp3'
        ])
        self.assertEqual(meta['disctrack'], u'2-09')

if __name__ == '__main__':
    unittest.main()
