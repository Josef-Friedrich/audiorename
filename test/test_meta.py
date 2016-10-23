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


class TestArtistSafeUnit(unittest.TestCase):

    def setUp(self):
        from audiorename import meta
        self.meta = meta.Meta()

        self.m = {
            'albumartist_credit': u'',
            'albumartist_sort': u'',
            'albumartist': u'',
            'artist_credit': u'',
            'artist_sort': u'',
            'artist': u'',
        }

    def assertArtistSort(self, key):
        self.m[key] = key
        safe, sort = self.meta.artistSafe(self.m)
        self.assertEqual(safe, key)
        self.assertEqual(sort, key)

    def test_albumartist_credit(self):
        self.assertArtistSort('albumartist_credit')

    def test_albumartist_sort(self):
        self.assertArtistSort('albumartist_sort')

    def test_albumartist(self):
        self.assertArtistSort('albumartist')

    def test_artist_credit(self):
        self.assertArtistSort('artist_credit')

    def test_artist_sort(self):
        self.assertArtistSort('artist_sort')

    def test_artist(self):
        self.assertArtistSort('artist')


class TestArtistSafe(unittest.TestCase):

    def test_artist(self):
        meta = get_meta('artist')
        self.assertEqual(meta['artistsafe'], u'artist')

    def test_artist_sort(self):
        meta = get_meta('artist_sort')
        self.assertEqual(meta['artistsafe_sort'], u'artist_sort')

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
