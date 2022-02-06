"""Test the submodule “meta.py”."""

from audiorename.meta import Meta
import audiorename.meta as meta

import unittest
import tempfile
import shutil
import helper
from helper import get_meta


class TestDictDiff(unittest.TestCase):

    def test_identical(self):
        tmp = helper.get_meta('files', 'album.mp3')
        result = meta.dict_diff(tmp.export_dict(), tmp.export_dict())
        self.assertEqual(result, [])

    def test_one_diff(self):
        tmp = helper.get_meta('files', 'album.mp3')
        dict1 = tmp.export_dict()
        tmp.title = 'diff'
        dict2 = tmp.export_dict()
        result = meta.dict_diff(dict1, dict2)
        self.assertEqual(
            result,
            [
                (u'ar_classical_title', 'full', 'diff'),
                (u'title', 'full', 'diff'),
            ]
        )

    def test_multiple_diffs(self):
        tmp = helper.get_meta('files', 'album.mp3')
        dict1 = tmp.export_dict()
        tmp.artist = 'diff'
        tmp.track = 99
        dict2 = tmp.export_dict()
        result = meta.dict_diff(dict1, dict2)
        self.assertEqual(
            result,
            [
                (u'ar_classical_track', '4-02', '4-99'),
                (u'ar_combined_disctrack', '4-02', '4-99'),
                (u'artist', 'the artist', 'diff'),
                (u'track', '2', '99'),
            ]
        )

    def test_del_attr(self):
        tmp = helper.get_meta('files', 'album.mp3')
        dict1 = tmp.export_dict()
        delattr(tmp, 'title')
        dict2 = tmp.export_dict()
        result = meta.dict_diff(dict1, dict2)
        self.assertEqual(
            result,
            [
                (u'ar_classical_title', 'full', u''),
                (u'title', 'full', u''),
            ]
        )


class TestEnrich(unittest.TestCase):

    def setUp(self):
        meta.set_useragent()

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_recording_pulp_01(self):
        # ['soundtrack', 'Pulp-Fiction', '01.mp3']
        result = meta.query_mbrainz(
            'recording',
            '0480672d-4d88-4824-a06b-917ff408eabe',
        )
        self.assertEqual(result['id'],
                         u'0480672d-4d88-4824-a06b-917ff408eabe')

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_recording_mozart_01(self):
        # ['classical', 'Mozart_Horn-concertos', '01.mp3']
        result = meta.query_mbrainz(
            'recording',
            '7886ad6c-11af-435b-8ec3-bca5711f7728',
        )
        self.assertEqual(result['work-relation-list'][0]['work']['id'],
                         u'21fe0bf0-a040-387c-a39d-369d53c251fe')

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_release_pulp_01(self):
        # ['soundtrack', 'Pulp-Fiction', '01.mp3']
        result = meta.query_mbrainz(
            'release',
            'ab81edcb-9525-47cd-8247-db4fa969f525',
        )
        self.assertEqual(result['release-group']['id'],
                         u'1703cd63-9401-33c0-87c6-50c4ba2e0ba8')

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_release_mozart_01(self):
        # ['classical', 'Mozart_Horn-concertos', '01.mp3'])
        result = meta.query_mbrainz(
            'release',
            '5ed650c5-0f72-4b79-80a7-c458c869f53e',
        )
        self.assertEqual(result['release-group']['id'],
                         u'e1fa28f0-e56e-395b-82d3-a8de54e8c627')

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_work_mozart_zauberfloete_unit(self):
        # recording_id 6a0599ea-5c06-483a-ba66-f3a036da900a
        # work_id eafec51f-47c5-3c66-8c36-a524246c85f8
        # Akt 1: 5adc213f-700a-4435-9e95-831ed720f348
        result = meta.work_recursion('eafec51f-47c5-3c66-8c36-a524246c85f8',
                                     [])
        self.assertEqual(result[0]['id'],
                         'eafec51f-47c5-3c66-8c36-a524246c85f8')
        self.assertEqual(result[1]['id'],
                         '5adc213f-700a-4435-9e95-831ed720f348')
        self.assertEqual(result[2]['id'],
                         'e208c5f5-5d37-3dfc-ac0b-999f207c9e46')
        self.assertTrue('artist-relation-list' in result[2])

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_work_kempff_transcription(self):
        # work_id 4fba670e-3b8e-4ddf-a3a6-90817c94d6ce
        result = meta.work_recursion('4fba670e-3b8e-4ddf-a3a6-90817c94d6ce',
                                     [])
        self.assertEqual(result[0]['id'],
                         '4fba670e-3b8e-4ddf-a3a6-90817c94d6ce')
        self.assertEqual(len(result), 1)


###############################################################################
# Public methods
###############################################################################


class TestExportDict(unittest.TestCase):

    def test_export_dict(self):
        meta = get_meta('files', 'album.mp3')

        result = meta.export_dict()
        self.assertEqual(result['title'], u'full')


# Test file:
# test/classical/without_work.mp3
#
# Same as without work:
# test/classical/Wagner_Meistersinger/01.mp3
#
# mb_trackid:
#   00ba1660-4e35-4985-86b2-8b7a3e99b1e5
#
# mb_workid:
#   6b198406-4fbf-3d61-82db-0b7ef195a7fe
#
# work:
#  Die Meistersinger von Nürnberg, WWV 96: Akt I. Vorspiel
class TestEnrichMetadata(unittest.TestCase):

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_enrich_metadata_meistersinger(self):
        tmp = helper.copy_to_tmp('classical', 'without_work.mp3')
        meta = Meta(tmp)
        self.assertEqual(meta.mb_trackid,
                         '00ba1660-4e35-4985-86b2-8b7a3e99b1e5')
        self.assertEqual(meta.mb_workid, None)
        self.assertEqual(meta.work, None)

        meta.enrich_metadata()
        self.assertEqual(meta.mb_workid,
                         '6b198406-4fbf-3d61-82db-0b7ef195a7fe')
        self.assertEqual(meta.work, u'Die Meistersinger von Nürnberg, '
                         'WWV 96: Vorspiel')
        meta.save()

        finished = Meta(tmp)
        self.assertEqual(finished.mb_workid,
                         '6b198406-4fbf-3d61-82db-0b7ef195a7fe')
        self.assertEqual(finished.work, u'Die Meistersinger von Nürnberg, '
                         'WWV 96: Vorspiel')
        self.assertEqual(
            finished.mb_workhierarchy_ids,
            u'4d644732-9876-4b0d-9c2c-b6a738d6530e/'
            u'6b198406-4fbf-3d61-82db-0b7ef195a7fe')
        self.assertEqual(
            finished.work_hierarchy,
            u'Die Meistersinger von Nürnberg, WWV 96 -> '
            u'Die Meistersinger von Nürnberg, WWV 96: Vorspiel'
        )
        self.assertEqual(finished.releasegroup_types, u'album')

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_enrich_metadata_pulp(self):
        tmp = helper.copy_to_tmp('soundtrack', 'Pulp-Fiction', '01.mp3')
        meta = Meta(tmp)
        self.assertEqual(meta.mb_trackid,
                         '0480672d-4d88-4824-a06b-917ff408eabe')
        self.assertEqual(meta.mb_workid, None)
        self.assertEqual(meta.work, None)

        meta.enrich_metadata()
        self.assertEqual(meta.mb_workid, None)
        self.assertEqual(meta.work, None)
        meta.save()

        finished = Meta(tmp)
        self.assertEqual(finished.mb_workid, None)
        self.assertEqual(finished.work, None)
        self.assertEqual(finished.mb_workhierarchy_ids, None)
        self.assertEqual(finished.work_hierarchy, None)
        self.assertEqual(finished.releasegroup_types,
                         u'soundtrack/album')


class TestRemapClassical(unittest.TestCase):

    def setUp(self):
        test_file = helper.get_testfile('classical', 'Mozart_Horn-concertos',
                                        '06.mp3')
        self.tmp_file = tempfile.mktemp()
        shutil.copy2(test_file, self.tmp_file)
        self.meta = Meta(self.tmp_file)

    def test_remap_classical(self):
        self.assertEqual(self.meta.title, 'Horn Concerto No. 3 in E-flat '
                         'major, K. 447: I. Allegro')
        self.assertEqual(self.meta.track, 6)
        self.assertEqual(self.meta.artist, 'Wolfgang Amadeus Mozart')
        self.assertEqual(self.meta.album, '4 Hornkonzerte (Concertos for Horn '
                                          'and Orchestra)')
        self.assertEqual(self.meta.comments, 'Orpheus Chamber Orchestra, '
                                             'David Jolley, William Purvis')

        self.meta.remap_classical()
        self.meta.save()

        finished = Meta(self.tmp_file)

        self.assertEqual(finished.title, 'I. Allegro')
        self.assertEqual(finished.track, 1)
        self.assertEqual(finished.artist, 'Wolfgang Amadeus Mozart')
        self.assertEqual(finished.album, 'Concerto for Horn no. 3 in E-flat '
                                         'major, K. 447 (OrpChaOrc)')
        self.assertEqual(
            finished.comments,
            u'Original metadata: title: Horn Concerto No. 3 in E-flat major, '
            'K. 447: I. Allegro; track: 6; artist: Wolfgang Amadeus Mozart; '
            'album: 4 Hornkonzerte (Concertos for Horn and Orchestra); '
        )


###############################################################################
# Properties
###############################################################################


# ar_combined_album
class TestPropertyAlbumClean(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def assertAlbumClean(self, album, compare=u'Lorem ipsum'):
        self.meta.album = album
        self.assertEqual(self.meta.ar_combined_album, compare)

    def test_disc_removal(self):
        self.assertAlbumClean('Lorem ipsum (Disc 1)')
        self.assertAlbumClean('Lorem ipsum(Disc 1)')
        self.assertAlbumClean('Lorem ipsum (Disc)')
        self.assertAlbumClean('Lorem ipsum (Disk 100)')
        self.assertAlbumClean('Lorem ipsum (disk99)')

    def test_empty(self):
        self.assertAlbumClean('', '')

    def test_real_world(self):
        meta = get_meta('real-world', '_compilations', 't',
                        'The-Greatest-No1s-of-the-80s_1994',
                        '2-09_Respectable.mp3')
        self.assertEqual(meta.ar_combined_album,
                         u'The Greatest No.1s of the 80s')


# ar_combined_artist (integration)
class TestPropertyArtistSafe(unittest.TestCase):

    def test_artist(self):
        meta = get_meta('meta', 'artist.mp3')
        self.assertEqual(meta.ar_combined_artist, u'artist')

    def test_artist_sort(self):
        meta = get_meta('meta', 'artist_sort.mp3')
        self.assertEqual(meta.ar_combined_artist_sort, u'artist_sort')

    def test_albumartist(self):
        meta = get_meta('meta', 'albumartist.mp3')
        self.assertEqual(meta.ar_combined_artist, u'albumartist')


# ar_combined_artist (unit)
class TestPropertyArtistSafeUnit(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')
        self.meta.albumartist_credit = u''
        self.meta.albumartist_sort = u''
        self.meta.albumartist = u''
        self.meta.artist_credit = u''
        self.meta.artist_sort = u''
        self.meta.artist = u''

    def assertArtistSort(self, key):
        setattr(self.meta, key, key)
        self.assertEqual(self.meta.ar_combined_artist, key)
        self.assertEqual(self.meta.ar_combined_artist_sort, key)

    def test_unkown(self):
        self.assertEqual(self.meta.ar_combined_artist, u'Unknown')
        self.assertEqual(self.meta.ar_combined_artist_sort, u'Unknown')

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
        self.meta.artist = 'artist'
        self.meta.artist_sort = 'artist_sort'
        self.assertEqual(self.meta.ar_combined_artist, 'artist')
        self.assertEqual(self.meta.ar_combined_artist_sort, 'artist_sort')

    def test_albumartist__artist__artist_sort(self):
        self.meta.albumartist = 'albumartist'
        self.meta.artist = 'artist'
        self.meta.artist_sort = 'artist_sort'
        self.assertEqual(self.meta.ar_combined_artist, 'albumartist')
        self.assertEqual(self.meta.ar_combined_artist_sort, 'artist_sort')

    def test_artist__albumartist_sort__artist_sort(self):
        self.meta.albumartist_sort = 'albumartist_sort'
        self.meta.artist = 'artist'
        self.meta.artist_sort = 'artist_sort'
        self.assertEqual(self.meta.ar_combined_artist, 'artist')
        self.assertEqual(self.meta.ar_combined_artist_sort, 'albumartist_sort')

    def test_shell_unfriendly(self):
        self.meta.shell_friendly = False
        self.meta.artist_sort = 'Lastname, Prename'
        self.assertEqual(self.meta.ar_combined_artist_sort,
                         'Lastname, Prename')

    def test_shell_friendly(self):
        self.meta.shell_friendly = True
        self.meta.artist_sort = 'Lastname, Prename'
        self.assertEqual(self.meta.ar_combined_artist_sort, 'Lastname_Prename')


# ar_combined_disctrack (integration)
class TestPropertyDiskTrack(unittest.TestCase):

    def test_single_disc(self):
        meta = get_meta('real-world', 'e', 'Everlast', 'Eat-At-Whiteys_2000',
                        '02_Black-Jesus.mp3')
        self.assertEqual(meta.ar_combined_disctrack, u'02')

    def test_double_disk(self):
        meta = get_meta('real-world', '_compilations', 't',
                        'The-Greatest-No1s-of-the-80s_1994',
                        '2-09_Respectable.mp3')
        self.assertEqual(meta.ar_combined_disctrack, u'2-09')


# ar_combined_disctrack (unit)
class TestPropertyDiskTrackUnit(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')
        self.meta.track = u''
        self.meta.tracktotal = u''
        self.meta.disc = u''
        self.meta.disctotal = u''

    def test_empty(self):
        self.assertEqual(self.meta.ar_combined_disctrack, u'')

    def test_no_track(self):
        self.meta.disc = '2'
        self.meta.disctotal = '3'
        self.meta.tracktotal = '36'
        self.assertEqual(self.meta.ar_combined_disctrack, u'')

    def test_disc_track(self):
        self.meta.disc = '2'
        self.meta.track = '4'
        self.assertEqual(self.meta.ar_combined_disctrack, u'2-04')

    def test_disk_total_one(self):
        self.meta.disc = '1'
        self.meta.track = '4'
        self.meta.disctotal = '1'
        self.meta.tracktotal = '36'
        self.assertEqual(self.meta.ar_combined_disctrack, u'04')

    def test_all_set(self):
        self.meta.disc = '2'
        self.meta.track = '4'
        self.meta.disctotal = '3'
        self.meta.tracktotal = '36'
        self.assertEqual(self.meta.ar_combined_disctrack, u'2-04')

    def test_zfill_track(self):
        self.meta.track = '4'
        self.meta.tracktotal = '100'
        self.assertEqual(self.meta.ar_combined_disctrack, u'004')

        self.meta.tracktotal = '10'
        self.assertEqual(self.meta.ar_combined_disctrack, u'04')

        self.meta.tracktotal = '5'
        self.assertEqual(self.meta.ar_combined_disctrack, u'04')

    def test_zfill_disc(self):
        self.meta.track = '4'
        self.meta.tracktotal = '10'
        self.meta.disc = '2'
        self.meta.disctotal = '10'
        self.assertEqual(self.meta.ar_combined_disctrack, u'02-04')

        self.meta.disctotal = '100'
        self.assertEqual(self.meta.ar_combined_disctrack, u'002-04')


# ar_performer*
class TestPropertyPerformerDifferentFormats(unittest.TestCase):

    def getMeta(self, extension):
        return get_meta('performers', 'blank.' + extension)

    def assertPerformer(self, meta):
        raw = meta.ar_performer_raw
        self.assertEqual(raw[0][0], u'conductor')
        self.assertEqual(raw[0][1], u'Fabio Luisi')
        self.assertEqual(raw[1][0], u'orchestra')
        self.assertEqual(raw[1][1], u'Wiener Symphoniker')
        self.assertEqual(raw[2][0], u'soprano vocals')
        self.assertEqual(raw[2][1], u'Elena Filipova')
        self.assertEqual(raw[3][0], u'choir vocals')
        self.assertEqual(raw[3][1], u'Chor der Wiener Volksoper')

        self.assertEqual(meta.ar_performer, u'Fabio Luisi, Wiener '
                         u'Symphoniker, Elena Filipova, Chor der Wiener '
                         u'Volksoper')
        self.assertEqual(meta.ar_performer_short, u'Luisi, WieSym')

        self.assertEqual(meta.ar_classical_performer, u'Luisi, WieSym')

    def test_flac(self):
        meta = self.getMeta('flac')
        self.assertPerformer(meta)

    def test_mp3(self):
        meta = self.getMeta('mp3')
        self.assertPerformer(meta)

    def test_ogg(self):
        meta = self.getMeta('ogg')
        self.assertPerformer(meta)


# soundtrack
class TestPropertySoundtrack(unittest.TestCase):

    def test_soundtrack(self):
        # albumtype -> bootleg
        # meta = get_meta(['soundtrack', 'Pulp-Fiction', '01.mp3'])
        meta = get_meta('show-case', 'Beatles_Yesterday.mp3')
        self.assertEqual(meta.ar_combined_soundtrack, True)

    def test_no_soundtrack(self):
        meta = get_meta('classical', 'Schubert_Winterreise', '01.mp3')
        self.assertEqual(meta.ar_combined_soundtrack, False)


# ar_classical_track
class TestPropertyTrackClassical(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def assertRoman(self, roman, arabic):
        self.assertEqual(self.meta._roman_to_int(roman), arabic)

    def test_roman_to_int(self):
        self.assertRoman('I', 1)
        self.assertRoman('II', 2)
        self.assertRoman('III', 3)
        self.assertRoman('IV', 4)
        self.assertRoman('V', 5)
        self.assertRoman('VI', 6)
        self.assertRoman('VII', 7)
        self.assertRoman('VIII', 8)
        self.assertRoman('IX', 9)
        self.assertRoman('X', 10)
        self.assertRoman('XI', 11)
        self.assertRoman('XII', 12)

    def assertTrack(self, title, compare):
        self.meta.title = title
        self.assertEqual(self.meta.ar_classical_track, compare)

    def test_function(self):
        self.assertTrack('III. Credo', u'03')
        self.assertTrack('III Credo', '4-02')
        self.assertTrack('Credo', '4-02')
        self.meta.track = 123
        self.assertEqual(self.meta.ar_classical_track, '4-123')


# work (integration)
class TestPropertyWork(unittest.TestCase):

    def test_work(self):
        meta = get_meta('classical', 'Mozart_Horn-concertos', '01.mp3')
        self.assertEqual(
            meta.work,
            u'Concerto for French Horn no. 1 in D major, '
            u'K. 386b / KV 412: I. Allegro'
        )
        self.assertEqual(
            meta.mb_workid,
            u'21fe0bf0-a040-387c-a39d-369d53c251fe'
        )
        self.assertEqual(meta.composer_sort, u'Mozart, Wolfgang Amadeus')


# ar_combined_work_top
class TestPropertyWorkTop(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def test_none(self):
        self.assertEqual(self.meta.ar_combined_work_top, None)

    def test_mutliple(self):
        self.meta.work_hierarchy = 'top -> work'
        self.assertEqual(self.meta.ar_combined_work_top, u'top')

    def test_single(self):
        self.meta.work_hierarchy = 'top'
        self.assertEqual(self.meta.ar_combined_work_top, u'top')

    def test_work_colon(self):
        self.meta.work = 'work: test'
        self.assertEqual(self.meta.ar_combined_work_top, u'work')

    def test_work(self):
        self.meta.work = 'work'
        self.assertEqual(self.meta.ar_combined_work_top, u'work')


# ar_classical_title
class TestPropertyTitleClassical(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def test_work_title(self):
        self.meta.title = 'work: title'
        self.assertEqual(self.meta.ar_classical_title, 'title')

    def test_work_work_title(self):
        self.meta.title = 'work: work: title'
        self.assertEqual(self.meta.ar_classical_title, 'work: title')

    def test_title(self):
        self.meta.title = 'title'
        self.assertEqual(self.meta.ar_classical_title, 'title')


# ar_combined_year
class TestPropertyYearSafe(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')
        self.meta.year = None
        self.meta.original_year = None

    def test_empty(self):
        self.assertEqual(self.meta.ar_combined_year, None)

    def test_year(self):
        self.meta.year = 1978
        self.assertEqual(self.meta.ar_combined_year, 1978)

    def test_original_year(self):
        self.meta.original_year = 1978
        self.assertEqual(self.meta.ar_combined_year, 1978)

    def test_year__original_year(self):
        self.meta.year = 2016
        self.meta.original_year = 1978
        self.assertEqual(self.meta.ar_combined_year, 1978)


###############################################################################
# Static methods
###############################################################################


class TestStaticMethodInitials(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def test_lowercase(self):
        self.assertEqual(self.meta._initials(u'beethoven'), u'b')

    def test_uppercase(self):
        self.assertEqual(self.meta._initials(u'Beethoven'), u'b')


class TestStaticMethodNormalizePerformer(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def test_unit_normalize_performer(self):
        out = self.meta._normalize_performer([u'John Lennon (vocals)',
                                             u'Ringo Starr (drums)'])
        self.assertEqual(out[0][0], u'vocals')
        self.assertEqual(out[0][1], u'John Lennon')
        self.assertEqual(out[1][0], u'drums')
        self.assertEqual(out[1][1], u'Ringo Starr')

    def test_unit_normalize_performer_string(self):
        out = self.meta._normalize_performer(u'Ludwig van Beethoven')
        self.assertEqual(out, [])


class TestStaticMethodSanitize(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def test_slash(self):
        self.assertEqual(self.meta._sanitize(u'lol/lol'), u'lollol')

    def test_whitespaces(self):
        self.assertEqual(self.meta._sanitize(u'lol  lol'), u'lol lol')

    def test_list(self):
        self.assertEqual(self.meta._sanitize([]), u'')


class TestStaticMethodShortenPerformer(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def test_ar_performer_shorten(self):
        s = self.meta._shorten_performer(u'Ludwig van Beethoven')
        self.assertEqual(s, u'Lud. van Bee.')

    def test_ar_performer_shorten_option_separator(self):
        s = self.meta._shorten_performer(u'Ludwig van Beethoven',
                                         separator=u'--')
        self.assertEqual(s, u'Lud.--van--Bee.')

    def test_ar_performer_shorten_option_abbreviation(self):
        s = self.meta._shorten_performer(u'Ludwig van Beethoven',
                                         abbreviation=u'_')
        self.assertEqual(s, u'Lud_ van Bee_')

    def test_ar_performer_shorten_option_all(self):
        s = self.meta._shorten_performer(u'Ludwig van Beethoven',
                                         separator=u'',
                                         abbreviation=u'')
        self.assertEqual(s, u'LudvanBee')


class TestStaticMethodUnifyList(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def test_unify_numbers(self):
        seq = self.meta._unify_list([1, 1, 2, 2, 1, 1, 3])
        self.assertEqual(seq, [1, 2, 3])

    def test_unify_list(self):
        seq = self.meta._unify_list([
            [u'conductor', u'Herbert von Karajan'],
            [u'orchestra', u'Staatskapelle Dresden'],
            [u'orchestra', u'Staatskapelle Dresden']
        ])

        self.assertEqual(seq, [
            [u'conductor', u'Herbert von Karajan'],
            [u'orchestra', u'Staatskapelle Dresden']
        ])


###############################################################################
# Class methods
###############################################################################

all_fields = [
    'acoustid_fingerprint',
    'acoustid_id',
    'album',
    'albumartist_credit',
    'albumartist_sort',
    'albumartist',
    'albumdisambig',
    'albumstatus',
    'albumtype',
    'ar_classical_album',
    'ar_classical_performer',
    'ar_classical_title',
    'ar_classical_track',
    'ar_combined_album',
    'ar_combined_artist_sort',
    'ar_combined_artist',
    'ar_combined_composer',
    'ar_combined_disctrack',
    'ar_combined_soundtrack',
    'ar_combined_work_top',
    'ar_combined_year',
    'ar_initial_album',
    'ar_initial_artist',
    'ar_initial_composer',
    'arranger',
    'art',
    'artist_credit',
    'artist_sort',
    'artist',
    'asin',
    'bitdepth',
    'bitrate',
    'bpm',
    'catalognum',
    'channels',
    'comments',
    'comp',
    'composer_sort',
    'composer',
    'country',
    'date',
    'day',
    'disc',
    'disctitle',
    'disctotal',
    'encoder',
    'format',
    'genre',
    'genres',
    'grouping',
    'images',
    'initial_key',
    'label',
    'language',
    'length',
    'lyricist',
    'lyrics',
    'mb_albumartistid',
    'mb_albumid',
    'mb_artistid',
    'mb_releasegroupid',
    'mb_releasetrackid',
    'mb_trackid',
    'mb_workhierarchy_ids',
    'mb_workid',
    'media',
    'month',
    'original_date',
    'original_day',
    'original_month',
    'original_year',
    'ar_performer_raw',
    'ar_performer_short',
    'ar_performer',
    'r128_album_gain',
    'r128_track_gain',
    'releasegroup_types',
    'rg_album_gain',
    'rg_album_peak',
    'rg_track_gain',
    'rg_track_peak',
    'samplerate',
    'script',
    'title',
    'track',
    'tracktotal',
    'work_hierarchy',
    'work',
    'year',
]


class TestFields(unittest.TestCase):

    def test_fields_phrydy(self):
        fields = Meta.fields()
        for field in Meta.fields_phrydy():
            self.assertIn(field, fields)

    def test_fields_audiorename(self):
        fields = Meta.fields()
        for field in Meta.fields_audiorename():
            self.assertIn(field, fields)

    def test_fields(self):
        for field in Meta.fields():
            self.assertIn(field, all_fields)

    def test_fields_sorted(self):
        for field in Meta.fields_sorted():
            self.assertIn(field, all_fields)


###############################################################################
# All properties
###############################################################################


class TestAllPropertiesHines(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('real-world', 'h', 'Hines_Earl',
                             'Just-Friends_1989', '06_Indian-Summer.mp3')

    def test_ar_classical_album(self):
        self.assertEqual(self.meta.ar_classical_album, u'')

    def test_ar_combined_album(self):
        self.assertEqual(self.meta.ar_combined_album, u'Just Friends')

    def test_ar_initial_album(self):
        self.assertEqual(self.meta.ar_initial_album, u'j')

    def test_ar_initial_artist(self):
        self.assertEqual(self.meta.ar_initial_artist, u'h')

    def test_ar_combined_artist(self):
        self.assertEqual(self.meta.ar_combined_artist, u'Earl Hines')

    def test_ar_combined_artist_sort(self):
        self.assertEqual(self.meta.ar_combined_artist_sort, u'Hines, Earl')

    def test_ar_initial_composer(self):
        self.assertEqual(self.meta.ar_initial_composer, u'e')

    def test_ar_combined_composer(self):
        self.assertEqual(self.meta.ar_combined_composer, u'Earl Hines')

    def test_ar_combined_disctrack(self):
        self.assertEqual(self.meta.ar_combined_disctrack, u'06')

    def test_ar_performer(self):
        self.assertEqual(self.meta.ar_performer, u'')

    def test_ar_classical_performer(self):
        self.assertEqual(self.meta.ar_classical_performer, u'Earl Hines')

    def test_ar_performer_raw(self):
        self.assertEqual(self.meta.ar_performer_raw, [])

    def test_ar_performer_short(self):
        self.assertEqual(self.meta.ar_performer_short, u'')

    def test_ar_classical_title(self):
        self.assertEqual(self.meta.ar_classical_title, u'Indian Summer')

    def test_ar_classical_track(self):
        self.assertEqual(self.meta.ar_classical_track, u'06')

    def test_ar_combined_year(self):
        self.assertEqual(self.meta.ar_combined_year, 1989)


class TestAllPropertiesWagner(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('classical', 'Wagner_Meistersinger', '01.mp3')

    def test_ar_classical_album(self):
        self.assertEqual(self.meta.ar_classical_album,
                         u'Die Meistersinger von Nürnberg')

    def test_ar_combined_album(self):
        self.assertEqual(self.meta.ar_combined_album,
                         u'Die Meistersinger von Nürnberg')

    def test_ar_initial_album(self):
        self.assertEqual(self.meta.ar_initial_album, u'd')

    def test_ar_initial_artist(self):
        self.assertEqual(self.meta.ar_initial_artist, u'w')

    def test_ar_combined_artist(self):
        self.assertEqual(
            self.meta.ar_combined_artist,
            u'Richard Wagner; René Kollo, Helen Donath, Theo Adam, Geraint '
            'Evans, Peter Schreier, Ruth Hesse, Karl Ridderbusch, Chor der '
            'Staatsoper Dresden, MDR Rundfunkchor Leipzig, Staatskapelle '
            'Dresden, Herbert von Karajan')

    def test_ar_combined_artist_sort(self):
        self.assertEqual(
            self.meta.ar_combined_artist_sort,
            u'Wagner, Richard; Kollo, René, Donath, Helen, Adam, Theo, Evans, '
            'Geraint, Schreier, Peter, Hesse, Ruth, Ridderbusch, Karl, Chor '
            'der Staatsoper Dresden, MDR Rundfunkchor Leipzig, Staatskapelle '
            'Dresden, Karajan, Herbert von')

    def test_ar_initial_composer(self):
        self.assertEqual(self.meta.ar_initial_composer, u'w')

    def test_ar_combined_composer(self):
        self.assertEqual(self.meta.ar_combined_composer, u'Wagner, Richard')

    def test_ar_combined_disctrack(self):
        self.assertEqual(self.meta.ar_combined_disctrack, u'1-01')

    def test_ar_performer(self):
        self.assertEqual(self.meta.ar_performer,
                         u'Herbert von Karajan, Staatskapelle Dresden')

    def test_ar_classical_performer(self):
        self.assertEqual(self.meta.ar_classical_performer,
                         u'Karajan, StaDre')

    def test_ar_performer_raw(self):
        self.assertEqual(self.meta.ar_performer_raw,
                         [
                             [u'conductor', u'Herbert von Karajan'],
                             [u'orchestra', u'Staatskapelle Dresden']
                         ])

    def test_ar_performer_short(self):
        self.assertEqual(self.meta.ar_performer_short,
                         u'Karajan, StaDre')

    def test_ar_classical_title(self):
        self.assertEqual(self.meta.ar_classical_title, 'Vorspiel')

    def test_ar_classical_track(self):
        self.assertEqual(self.meta.ar_classical_track, '1-01')

    def test_ar_combined_year(self):
        self.assertEqual(self.meta.ar_combined_year, 1971)


class TestClassical(unittest.TestCase):

    def setUp(self):
        self.mozart = get_meta('classical', 'Mozart_Horn-concertos',
                               '01.mp3')
        self.mozart2 = get_meta('classical', 'Mozart_Horn-concertos',
                                '02.mp3')
        self.schubert = get_meta('classical', 'Schubert_Winterreise',
                                 '01.mp3')
        self.tschaikowski = get_meta('classical', 'Tschaikowski_Swan-Lake',
                                     '1-01.mp3')
        self.wagner = get_meta('classical', 'Wagner_Meistersinger', '01.mp3')

    # ar_classical_album
    def test_ar_classical_album_mozart(self):
        self.assertEqual(
            self.mozart.ar_classical_album,
            u'Concerto for French Horn no. 1 in D major, K. 386b / KV 412'
        )

    def test_ar_classical_album_schubert(self):
        self.assertEqual(
            self.schubert.ar_classical_album,
            u'Die Winterreise, op. 89, D. 911'
        )

    def test_ar_classical_album_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.ar_classical_album,
            u'Swan Lake, op. 20'
        )

    def test_ar_classical_album_wagner(self):
        self.assertEqual(
            self.wagner.ar_classical_album,
            u'Die Meistersinger von N\xfcrnberg'
        )

    # ar_initial_composer
    def test_ar_initial_composer_mozart(self):
        self.assertEqual(self.mozart.ar_initial_composer, u'm')

    def test_ar_initial_composer_schubert(self):
        self.assertEqual(self.schubert.ar_initial_composer, u's')

    def test_ar_initial_composer_tschaikowski(self):
        self.assertEqual(self.tschaikowski.ar_initial_composer, u't')

    def test_ar_initial_composer_wagner(self):
        self.assertEqual(self.wagner.ar_initial_composer, u'w')

    # ar_combined_composer
    def test_ar_combined_composer_mozart(self):
        self.assertEqual(
            self.mozart.ar_combined_composer,
            u'Mozart, Wolfgang Amadeus'
        )

    def test_ar_combined_composer_mozart2(self):
        self.assertEqual(
            self.mozart2.ar_combined_composer,
            u'Mozart, Wolfgang Amadeus'
        )

    def test_ar_combined_composer_schubert(self):
        self.assertEqual(
            self.schubert.ar_combined_composer,
            u'Schubert, Franz'
        )

    def test_ar_combined_composer_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.ar_combined_composer,
            u'Tchaikovsky, Pyotr Ilyich'
        )

    def test_ar_combined_composer_wagner(self):
        self.assertEqual(
            self.wagner.ar_combined_composer,
            u'Wagner, Richard'
        )

    # composer_sort
    def test_composer_sort_mozart(self):
        self.assertEqual(
            self.mozart.composer_sort,
            u'Mozart, Wolfgang Amadeus'
        )

    def test_composer_sort_schubert(self):
        self.assertEqual(
            self.schubert.composer_sort,
            u'Schubert, Franz'
        )

    def test_composer_sort_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.composer_sort,
            u'Tchaikovsky, Pyotr Ilyich'
        )

    def test_composer_sort_wagner(self):
        self.assertEqual(
            self.wagner.composer_sort,
            u'Wagner, Richard'
        )

    # ar_classical_performer
    def test_ar_classical_performer_mozart(self):
        self.assertEqual(
            self.mozart.ar_classical_performer,
            u'OrpChaOrc'
        )

    def test_ar_classical_performer_schubert(self):
        self.assertEqual(
            self.schubert.ar_classical_performer,
            u'Fischer-Dieskau, Moore'
        )

    def test_ar_classical_performer_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.ar_classical_performer,
            u'Svetlanov, StaAcaSym'
        )

    def test_ar_classical_performer_wagner(self):
        self.assertEqual(
            self.wagner.ar_classical_performer,
            u'Karajan, StaDre'
        )

    # ar_classical_title
    def test_ar_classical_title_mozart(self):
        self.assertEqual(self.mozart.ar_classical_title, u'I. Allegro')

    def test_ar_classical_title_schubert(self):
        self.assertEqual(
            self.schubert.ar_classical_title, u'Gute Nacht')

    def test_ar_classical_title_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.ar_classical_title,
            u'Introduction. Moderato assai - Allegro, ma non troppo - Tempo I'
        )

    def test_ar_classical_title_wagner(self):
        self.assertEqual(
            self.wagner.ar_classical_title, u'Vorspiel')

    # ar_classical_track
    def test_ar_classical_track_mozart(self):
        self.assertEqual(self.mozart.ar_classical_track, u'01')

    def test_ar_classical_track_schubert(self):
        self.assertEqual(self.schubert.ar_classical_track, u'01')

    def test_ar_classical_track_tschaikowski(self):
        self.assertEqual(self.tschaikowski.ar_classical_track, u'1-01')

    def test_ar_classical_track_wagner(self):
        self.assertEqual(self.wagner.ar_classical_track, u'1-01')


if __name__ == '__main__':
    unittest.main()
