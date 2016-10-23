import unittest
import helper as h


def get_real(path):
    return h.get_meta([h.dir_test, 'real-world'] + path)

def get_meta(token):
    return h.get_meta([h.dir_test, 'meta', token + '.mp3'])


class TestMeta(unittest.TestCase):

    def setUp(self):
        self.meta = get_real([
            'h', 'Hines_Earl', 'Just-Friends_1989', '06_Indian-Summer.mp3'
        ])

    def test_artistsafe(self):
        self.assertEqual(self.meta['artistsafe'], u'Earl Hines')

    def test_artistsafe_sort(self):
        self.assertEqual(self.meta['artistsafe_sort'], u'Hines, Earl')

    def test_year_safe(self):
        self.assertEqual(self.meta['year_safe'], 1989)

    def test_artist_initial(self):
        self.assertEqual(self.meta['artist_initial'], u'h')

    def test_album_initial(self):
        self.assertEqual(self.meta['album_initial'], u'j')



class TestArtistSafe(unittest.TestCase):

    def test_artist(self):
        meta = get_meta('artist')
        self.assertEqual(meta['artistsafe'], u'artist')

    @unittest.skip('not working')
    def test_artist_sort(self):
        meta = get_meta('artist_sort')
        self.assertEqual(meta['artistsafe'], u'artist_sort')


    def test_albumartist(self):
        meta = get_meta('albumartist')
        self.assertEqual(meta['artistsafe'], u'albumartist')


class TestDiskTrack(unittest.TestCase):

    def test_single_disc(self):
        meta = get_real([
            'e', 'Everlast', 'Eat-At-Whiteys_2000', '02_Black-Jesus.mp3'
        ])
        self.assertEqual(meta['disctrack'], u'02')

    def test_double_disk(self):
        meta = get_real([
            '_compilations',
            't',
            'The-Greatest-No1s-of-the-80s_1994',
            '2-09_Respectable.mp3'
        ])
        self.assertEqual(meta['disctrack'], u'2-09')

if __name__ == '__main__':
    unittest.main()
