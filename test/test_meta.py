import unittest
import helper as h


def get_real(path):
    return h.get_meta([h.dir_test, 'real-world'] + path)


def get_classical(path):
    return h.get_meta([h.dir_test, 'classical'] + path)


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

    def test_unkown(self):
        safe, sort = self.meta.artistSafe(self.m)
        self.assertEqual(safe, 'Unknown')
        self.assertEqual(sort, 'Unknown')

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

    def test_artist__artist_sort(self):
        self.m['artist'] = 'artist'
        self.m['artist_sort'] = 'artist_sort'
        safe, sort = self.meta.artistSafe(self.m)
        self.assertEqual(safe, 'artist')
        self.assertEqual(sort, 'artist_sort')

    def test_albumartist__artist__artist_sort(self):
        self.m['albumartist'] = 'albumartist'
        self.m['artist'] = 'artist'
        self.m['artist_sort'] = 'artist_sort'
        safe, sort = self.meta.artistSafe(self.m)
        self.assertEqual(safe, 'albumartist')
        self.assertEqual(sort, 'artist_sort')

    def test_artist__albumartist_sort__artist_sort(self):
        self.m['albumartist_sort'] = 'albumartist_sort'
        self.m['artist'] = 'artist'
        self.m['artist_sort'] = 'artist_sort'
        safe, sort = self.meta.artistSafe(self.m)
        self.assertEqual(safe, 'artist')
        self.assertEqual(sort, 'albumartist_sort')

    def test_shell_unfriendly(self):
        self.meta.shell_friendly = False
        self.m['artist_sort'] = 'Lastname, Prename'
        safe, sort = self.meta.artistSafe(self.m)
        self.assertEqual(sort, 'Lastname, Prename')

    def test_shell_friendly(self):
        self.meta.shell_friendly = True
        self.m['artist_sort'] = 'Lastname, Prename'
        safe, sort = self.meta.artistSafe(self.m)
        self.assertEqual(sort, 'Lastname_Prename')


class TestYearSafeUnit(unittest.TestCase):

    def setUp(self):
        from audiorename import meta
        self.meta = meta.Meta()

        self.m = {
            'year': u'',
            'original_year': u'',
        }

    def test_empty(self):
        self.assertEqual(self.meta.yearSafe(self.m), '')

    def test_year(self):
        self.m['year'] = '1978'
        self.assertEqual(self.meta.yearSafe(self.m), '1978')

    def test_original_year(self):
        self.m['original_year'] = '1978'
        self.assertEqual(self.meta.yearSafe(self.m), '1978')

    def test_year__original_year(self):
        self.m['year'] = '2016'
        self.m['original_year'] = '1978'
        self.assertEqual(self.meta.yearSafe(self.m), '1978')


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


class TestDiskTrackUnit(unittest.TestCase):

    def setUp(self):
        from audiorename import meta
        self.meta = meta.Meta()

        self.m = {
            'track': u'',
            'tracktotal': u'',
            'disc': u'',
            'disctotal': u'',
        }

    def test_empty(self):
        self.assertEqual(self.meta.discTrack(self.m), u'')

    def test_no_track(self):
        self.m['disc'] = '2'
        self.m['disctotal'] = '3'
        self.m['tracktotal'] = '36'
        self.assertEqual(self.meta.discTrack(self.m), u'')

    def test_disc_track(self):
        self.m['disc'] = '2'
        self.m['track'] = '4'
        self.assertEqual(self.meta.discTrack(self.m), u'2-04')

    def test_disk_total_one(self):
        self.m['disc'] = '1'
        self.m['track'] = '4'
        self.m['disctotal'] = '1'
        self.m['tracktotal'] = '36'
        self.assertEqual(self.meta.discTrack(self.m), u'04')

    def test_all_set(self):
        self.m['disc'] = '2'
        self.m['track'] = '4'
        self.m['disctotal'] = '3'
        self.m['tracktotal'] = '36'
        self.assertEqual(self.meta.discTrack(self.m), u'2-04')

    def test_zfill_track(self):
        self.m['track'] = '4'
        self.m['tracktotal'] = '100'
        self.assertEqual(self.meta.discTrack(self.m), u'004')

        self.m['tracktotal'] = '10'
        self.assertEqual(self.meta.discTrack(self.m), u'04')

        self.m['tracktotal'] = '5'
        self.assertEqual(self.meta.discTrack(self.m), u'04')

    def test_zfill_disc(self):
        self.m['track'] = '4'
        self.m['tracktotal'] = '10'
        self.m['disc'] = '2'
        self.m['disctotal'] = '10'
        self.assertEqual(self.meta.discTrack(self.m), u'02-04')

        self.m['disctotal'] = '100'
        self.assertEqual(self.meta.discTrack(self.m), u'002-04')


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


class TestAlbumClean(unittest.TestCase):

    def setUp(self):
        from audiorename import meta
        self.meta = meta.Meta()

    def assertAlbumClean(self, album, compare=u'Lorem ipsum'):
        self.assertEqual(self.meta.albumClean(album), compare)

    def test_disc_removal(self):
        self.assertAlbumClean('Lorem ipsum (Disc 1)')
        self.assertAlbumClean('Lorem ipsum(Disc 1)')
        self.assertAlbumClean('Lorem ipsum (Disc)')
        self.assertAlbumClean('Lorem ipsum (Disk 100)')
        self.assertAlbumClean('Lorem ipsum (disk99)')

    def test_empty(self):
        self.assertAlbumClean('', '')

    def test_real_world(self):
        meta = get_real([
            '_compilations',
            't',
            'The-Greatest-No1s-of-the-80s_1994',
            '2-09_Respectable.mp3'
        ])
        self.assertEqual(meta['album_clean'], u'The Greatest No.1s of the 80s')


class TestWork(unittest.TestCase):

    def test_work(self):
        meta = get_classical([
            'Mozart_Wolfgang-Amadeus__4-Hornkonzerte',
            '01.mp3'
        ])
        self.assertEqual(
            meta['work'],
            u'Concerto for French Horn no. 1 in D major, ' +
            u'K. 386b  KV 412 I. Allegro'
        )
        self.assertEqual(
            meta['mb_workid'],
            u'21fe0bf0-a040-387c-a39d-369d53c251fe'
        )
        self.assertEqual(
            meta['composer_sort'],
            u'Mozart, Wolfgang Amadeus'
        )


class TestClassicalUnit(unittest.TestCase):

    def setUp(self):
        from audiorename import meta
        self.meta = meta.Meta()

    def test_classical_title(self):
        self.assertEqual(self.meta.classicalTitle('work: title'), 'title')
        self.assertEqual(self.meta.classicalTitle('work: work: title'), 'work: title')
        self.assertEqual(self.meta.classicalTitle('title'), 'title')

if __name__ == '__main__':
    unittest.main()
