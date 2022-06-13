"""Test the submodule “meta.py”."""

from audiorename.meta import Meta
import audiorename.meta as meta

import unittest
import tempfile
import shutil
import helper
from helper import get_meta
import typing


class TestDictDiff(unittest.TestCase):

    def test_identical(self):
        tmp = helper.get_meta('files', 'album.mp3')
        result = meta.compare_dicts(tmp.export_dict(), tmp.export_dict())
        self.assertEqual(result, [])

    def test_one_diff(self):
        tmp = helper.get_meta('files', 'album.mp3')
        dict1 = tmp.export_dict()
        tmp.title = 'diff'
        dict2 = tmp.export_dict()
        result = meta.compare_dicts(dict1, dict2)
        self.assertEqual(
            result,
            [
                ('ar_classical_title', 'full', 'diff'),
                ('title', 'full', 'diff'),
            ]
        )

    def test_multiple_diffs(self):
        tmp = helper.get_meta('files', 'album.mp3')
        dict1 = tmp.export_dict()
        tmp.artist = 'diff'
        tmp.track = 99
        dict2 = tmp.export_dict()
        result = meta.compare_dicts(dict1, dict2)
        self.assertEqual(
            result,
            [
                ('ar_classical_track', '4-02', '4-99'),
                ('ar_combined_disctrack', '4-02', '4-99'),
                ('artist', 'the artist', 'diff'),
                ('track', '2', '99'),
            ]
        )

    def test_del_attr(self):
        tmp = helper.get_meta('files', 'album.mp3')
        dict1 = tmp.export_dict()
        delattr(tmp, 'title')
        dict2 = tmp.export_dict()
        result = meta.compare_dicts(dict1, dict2)
        self.assertEqual(
            result,
            [
                ('ar_classical_title', 'full', None),
                ('title', 'full', None),
            ]
        )


###############################################################################
# Public methods
###############################################################################


class TestExportDict(unittest.TestCase):

    def test_export_dict(self):
        meta = get_meta('files', 'album.mp3')

        result = meta.export_dict()
        print(result)
        self.assertEqual(result['title'], 'full')


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
@unittest.skipIf(helper.SKIP_QUICK, 'Ignored, as it has to be done quickly.')
@unittest.skipIf(helper.SKIP_API_CALLS,
                 'Ignored if the API is not available.')
class TestEnrichMetadata(unittest.TestCase):

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
        self.assertEqual(meta.work, 'Die Meistersinger von Nürnberg, '
                         'WWV 96: Vorspiel')
        meta.save()

        finished = Meta(tmp)
        self.assertEqual(finished.mb_workid,
                         '6b198406-4fbf-3d61-82db-0b7ef195a7fe')
        self.assertEqual(finished.work, 'Die Meistersinger von Nürnberg, '
                         'WWV 96: Vorspiel')
        self.assertEqual(
            finished.mb_workhierarchy_ids,
            '4d644732-9876-4b0d-9c2c-b6a738d6530e/'
            '6b198406-4fbf-3d61-82db-0b7ef195a7fe')
        self.assertEqual(
            finished.work_hierarchy,
            'Die Meistersinger von Nürnberg, WWV 96 -> '
            'Die Meistersinger von Nürnberg, WWV 96: Vorspiel'
        )
        self.assertEqual(finished.releasegroup_types, 'album')

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
                         'soundtrack/album')


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
            'Original metadata: title: Horn Concerto No. 3 in E-flat major, '
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

    def assertAlbumClean(self, album,
                         compare: typing.Optional[str] = 'Lorem ipsum'):
        self.meta.album = album
        self.assertEqual(self.meta.ar_combined_album, compare)

    def test_disc_removal(self):
        self.assertAlbumClean('Lorem ipsum (Disc 1)')
        self.assertAlbumClean('Lorem ipsum(Disc 1)')
        self.assertAlbumClean('Lorem ipsum (Disc)')
        self.assertAlbumClean('Lorem ipsum (Disk 100)')
        self.assertAlbumClean('Lorem ipsum (disk99)')

    def test_empty(self):
        self.assertAlbumClean('', None)

    def test_real_world(self):
        meta = get_meta('real-world', '_compilations', 't',
                        'The-Greatest-No1s-of-the-80s_1994',
                        '2-09_Respectable.mp3')
        self.assertEqual(meta.ar_combined_album,
                         'The Greatest No.1s of the 80s')


# ar_combined_artist (integration)
class TestPropertyArtistSafe(unittest.TestCase):

    def test_artist(self):
        meta = get_meta('meta', 'artist.mp3')
        self.assertEqual(meta.ar_combined_artist, 'artist')

    def test_artist_sort(self):
        meta = get_meta('meta', 'artist_sort.mp3')
        self.assertEqual(meta.ar_combined_artist_sort, 'artist_sort')

    def test_albumartist(self):
        meta = get_meta('meta', 'albumartist.mp3')
        self.assertEqual(meta.ar_combined_artist, 'albumartist')


# ar_combined_artist (unit)
class TestPropertyArtistSafeUnit(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')
        self.meta.albumartist_credit = ''
        self.meta.albumartist_sort = ''
        self.meta.albumartist = ''
        self.meta.artist_credit = ''
        self.meta.artist_sort = ''
        self.meta.artist = ''

    def assertArtistSort(self, key):
        setattr(self.meta, key, key)
        self.assertEqual(self.meta.ar_combined_artist, key)
        self.assertEqual(self.meta.ar_combined_artist_sort, key)

    def test_unkown(self):
        self.assertEqual(self.meta.ar_combined_artist, 'Unknown')
        self.assertEqual(self.meta.ar_combined_artist_sort, 'Unknown')

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
        self.assertEqual(meta.ar_combined_disctrack, '02')

    def test_double_disk(self):
        meta = get_meta('real-world', '_compilations', 't',
                        'The-Greatest-No1s-of-the-80s_1994',
                        '2-09_Respectable.mp3')
        self.assertEqual(meta.ar_combined_disctrack, '2-09')


# ar_combined_disctrack (unit)
class TestPropertyDiskTrackUnit(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')
        self.meta.track = ''
        self.meta.tracktotal = ''
        self.meta.disc = ''
        self.meta.disctotal = ''

    def test_empty(self):
        self.assertEqual(self.meta.ar_combined_disctrack, None)

    def test_no_track(self):
        self.meta.disc = '2'
        self.meta.disctotal = '3'
        self.meta.tracktotal = '36'
        self.assertEqual(self.meta.ar_combined_disctrack, None)

    def test_disc_track(self):
        self.meta.disc = '2'
        self.meta.track = '4'
        self.assertEqual(self.meta.ar_combined_disctrack, '2-04')

    def test_disk_total_one(self):
        self.meta.disc = '1'
        self.meta.track = '4'
        self.meta.disctotal = '1'
        self.meta.tracktotal = '36'
        self.assertEqual(self.meta.ar_combined_disctrack, '04')

    def test_all_set(self):
        self.meta.disc = '2'
        self.meta.track = '4'
        self.meta.disctotal = '3'
        self.meta.tracktotal = '36'
        self.assertEqual(self.meta.ar_combined_disctrack, '2-04')

    def test_zfill_track(self):
        self.meta.track = '4'
        self.meta.tracktotal = '100'
        self.assertEqual(self.meta.ar_combined_disctrack, '004')

        self.meta.tracktotal = '10'
        self.assertEqual(self.meta.ar_combined_disctrack, '04')

        self.meta.tracktotal = '5'
        self.assertEqual(self.meta.ar_combined_disctrack, '04')

    def test_zfill_disc(self):
        self.meta.track = '4'
        self.meta.tracktotal = '10'
        self.meta.disc = '2'
        self.meta.disctotal = '10'
        self.assertEqual(self.meta.ar_combined_disctrack, '02-04')

        self.meta.disctotal = '100'
        self.assertEqual(self.meta.ar_combined_disctrack, '002-04')


# ar_performer*
class TestPropertyPerformerDifferentFormats(unittest.TestCase):

    def getMeta(self, extension):
        return get_meta('performers', 'blank.' + extension)

    def assertPerformer(self, meta):
        raw = meta.ar_performer_raw
        self.assertEqual(raw[0][0], 'conductor')
        self.assertEqual(raw[0][1], 'Fabio Luisi')
        self.assertEqual(raw[1][0], 'orchestra')
        self.assertEqual(raw[1][1], 'Wiener Symphoniker')
        self.assertEqual(raw[2][0], 'soprano vocals')
        self.assertEqual(raw[2][1], 'Elena Filipova')
        self.assertEqual(raw[3][0], 'choir vocals')
        self.assertEqual(raw[3][1], 'Chor der Wiener Volksoper')

        self.assertEqual(meta.ar_performer, 'Fabio Luisi, Wiener '
                         'Symphoniker, Elena Filipova, Chor der Wiener '
                         'Volksoper')
        self.assertEqual(meta.ar_performer_short, 'Luisi, WieSym')

        self.assertEqual(meta.ar_classical_performer, 'Luisi, WieSym')

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
        self.assertTrack('III. Credo', '03')
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
            'Concerto for French Horn no. 1 in D major, '
            'K. 386b / KV 412: I. Allegro'
        )
        self.assertEqual(
            meta.mb_workid,
            '21fe0bf0-a040-387c-a39d-369d53c251fe'
        )
        self.assertEqual(meta.composer_sort, 'Mozart, Wolfgang Amadeus')


# ar_combined_work_top
class TestPropertyWorkTop(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def test_none(self):
        self.assertEqual(self.meta.ar_combined_work_top, None)

    def test_mutliple(self):
        self.meta.work_hierarchy = 'top -> work'
        self.assertEqual(self.meta.ar_combined_work_top, 'top')

    def test_single(self):
        self.meta.work_hierarchy = 'top'
        self.assertEqual(self.meta.ar_combined_work_top, 'top')

    def test_work_colon(self):
        self.meta.work = 'work: test'
        self.assertEqual(self.meta.ar_combined_work_top, 'work')

    def test_work(self):
        self.meta.work = 'work'
        self.assertEqual(self.meta.ar_combined_work_top, 'work')


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
        self.assertEqual(self.meta._find_initials('beethoven'), 'b')

    def test_uppercase(self):
        self.assertEqual(self.meta._find_initials('Beethoven'), 'b')


class TestStaticMethodNormalizePerformer(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def test_unit_normalize_performer(self):
        out = self.meta._normalize_performer(['John Lennon (vocals)',
                                             'Ringo Starr (drums)'])
        self.assertEqual(out[0][0], 'vocals')
        self.assertEqual(out[0][1], 'John Lennon')
        self.assertEqual(out[1][0], 'drums')
        self.assertEqual(out[1][1], 'Ringo Starr')

    def test_unit_normalize_performer_string(self):
        out = self.meta._normalize_performer('Ludwig van Beethoven')
        self.assertEqual(out, [])


class TestStaticMethodSanitize(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def test_slash(self):
        self.assertEqual(self.meta._sanitize('lol/lol'), 'lollol')

    def test_whitespaces(self):
        self.assertEqual(self.meta._sanitize('lol  lol'), 'lol lol')

    def test_list(self):
        self.assertEqual(self.meta._sanitize([]), '')


class TestStaticMethodShortenPerformer(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def test_ar_performer_shorten(self):
        s = self.meta._shorten_performer('Ludwig van Beethoven')
        self.assertEqual(s, 'Lud. van Bee.')

    def test_ar_performer_shorten_option_separator(self):
        s = self.meta._shorten_performer('Ludwig van Beethoven',
                                         separator='--')
        self.assertEqual(s, 'Lud.--van--Bee.')

    def test_ar_performer_shorten_option_abbreviation(self):
        s = self.meta._shorten_performer('Ludwig van Beethoven',
                                         abbreviation='_')
        self.assertEqual(s, 'Lud_ van Bee_')

    def test_ar_performer_shorten_option_all(self):
        s = self.meta._shorten_performer('Ludwig van Beethoven',
                                         separator='',
                                         abbreviation='')
        self.assertEqual(s, 'LudvanBee')


class TestStaticMethodUnifyList(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('files', 'album.mp3')

    def test_unify_numbers(self):
        seq = self.meta._unify_list([1, 1, 2, 2, 1, 1, 3])
        self.assertEqual(seq, [1, 2, 3])

    def test_unify_list(self):
        seq = self.meta._unify_list([
            ['conductor', 'Herbert von Karajan'],
            ['orchestra', 'Staatskapelle Dresden'],
            ['orchestra', 'Staatskapelle Dresden']
        ])

        self.assertEqual(seq, [
            ['conductor', 'Herbert von Karajan'],
            ['orchestra', 'Staatskapelle Dresden']
        ])


###############################################################################
# Class methods
###############################################################################


all_fields = [
    # acoustid_fingerprint: None
    # acoustid_id         : None
    # album               : the album
    # albumartist         : the album artist
    # albumartist_credit  : None
    # albumartist_sort    : None
    # albumartists        : []
    # albumdisambig       : None
    # albumstatus         : None
    # albumtype           : None
    'acoustid_fingerprint',
    'acoustid_id',
    'album',
    'albumartist_credit',
    'albumartist_sort',
    'albumartist',
    'albumartists',
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
    'ar_performer_raw',
    'ar_performer_short',
    'ar_performer',
    # arranger            : None
    # art                 : None
    # artist              : the artist
    # artist_credit       : None
    # artist_sort         : None
    # artists             : []
    # asin                : None
    'arranger',
    'art',
    'artist_credit',
    'artist_sort',
    'artist',
    'artists',
    'asin',
    # barcode             : None
    # bitdepth            : 0
    # bitrate             : 80000
    # bitrate_mode        :
    # bpm                 : 6
    'barcode',
    'bitdepth',
    'bitrate_mode',
    'bitrate',
    'bpm',
    # catalognum          : None
    # channels            : 1
    # comments            : the comments
    # comp                : True
    # composer            : the composer
    # composer_sort       : None
    # copyright           : None
    # country             : None
    'catalognum',
    'channels',
    'comments',
    'comp',
    'composer_sort',
    'composer',
    'copyright',
    'country',
    # date                : 2001-01-01
    # day                 : None
    # disc                : 4
    # disctitle           : None
    # disctotal           : 5
    'date',
    'day',
    'disc',
    'disctitle',
    'disctotal',
    # encoder             : iTunes v7.6.2
    # encoder_info        :
    # encoder_settings    :
    'encoder',
    'encoder_info',
    'encoder_settings',
    # format              : MP3
    'format',
    # genre               : the genre
    # genres              : ['the genre']
    # grouping            : the grouping
    'genre',
    'genres',
    'grouping',
    # images              : []
    # initial_key         : None
    # isrc                : None
    'images',
    'initial_key',
    'isrc',
    # label               : the label
    # language            : None
    # length              : 1.071
    # lyricist            : None
    # lyrics              : the lyrics
    'label',
    'language',
    'length',
    'lyricist',
    'lyrics',
    # mb_albumartistid    : None
    # mb_albumartistids   : []
    # mb_albumid          : 9e873859-8aa4-4790-b985-5a953e8ef628
    # mb_artistid         : 7cf0ea9d-86b9-4dad-ba9e-2355a64899ea
    # mb_artistids        : ['7cf0ea9d-86b9-4dad-ba9e-2355a64899ea']
    # mb_releasegroupid   : None
    # mb_releasetrackid   : c29f3a57-b439-46fd-a2e2-93776b1371e0
    # mb_trackid          : 8b882575-08a5-4452-a7a7-cbb8a1531f9e
    # mb_workhierarchy_ids: None
    # mb_workid           : None
    # media               : None
    # month               : None
    'mb_albumartistid',
    'mb_albumartistids',
    'mb_albumid',
    'mb_artistid',
    'mb_artistids',
    'mb_releasegroupid',
    'mb_releasetrackid',
    'mb_trackid',
    'mb_workhierarchy_ids',
    'mb_workid',
    'media',
    'month',
    # original_date       : None
    # original_day        : None
    # original_month      : None
    # original_year       : None
    'original_date',
    'original_day',
    'original_month',
    'original_year',
    # r128_album_gain     : None
    # r128_track_gain     : None
    # releasegroup_types  : None
    # rg_album_gain       : None
    # rg_album_peak       : None
    # rg_track_gain       : 0.0
    # rg_track_peak       : 0.000244
    'r128_album_gain',
    'r128_track_gain',
    'releasegroup_types',
    'rg_album_gain',
    'rg_album_peak',
    'rg_track_gain',
    'rg_track_peak',
    # samplerate          : 44100
    # script              : None
    'samplerate',
    'script',
    # title               : full
    # track               : 2
    # tracktotal          : 3
    'title',
    'track',
    'tracktotal',
    # url                 : None
    'url',
    # work                : None
    # work_hierarchy      : None
    'work_hierarchy',
    'work',
    # year                : 2001
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
        self.assertEqual(self.meta.ar_classical_album, None)

    def test_ar_combined_album(self):
        self.assertEqual(self.meta.ar_combined_album, 'Just Friends')

    def test_ar_initial_album(self):
        self.assertEqual(self.meta.ar_initial_album, 'j')

    def test_ar_initial_artist(self):
        self.assertEqual(self.meta.ar_initial_artist, 'h')

    def test_ar_combined_artist(self):
        self.assertEqual(self.meta.ar_combined_artist, 'Earl Hines')

    def test_ar_combined_artist_sort(self):
        self.assertEqual(self.meta.ar_combined_artist_sort, 'Hines, Earl')

    def test_ar_initial_composer(self):
        self.assertEqual(self.meta.ar_initial_composer, 'e')

    def test_ar_combined_composer(self):
        self.assertEqual(self.meta.ar_combined_composer, 'Earl Hines')

    def test_ar_combined_disctrack(self):
        self.assertEqual(self.meta.ar_combined_disctrack, '06')

    def test_ar_performer(self):
        self.assertEqual(self.meta.ar_performer, '')

    def test_ar_classical_performer(self):
        self.assertEqual(self.meta.ar_classical_performer, 'Earl Hines')

    def test_ar_performer_raw(self):
        self.assertEqual(self.meta.ar_performer_raw, [])

    def test_ar_performer_short(self):
        self.assertEqual(self.meta.ar_performer_short, '')

    def test_ar_classical_title(self):
        self.assertEqual(self.meta.ar_classical_title, 'Indian Summer')

    def test_ar_classical_track(self):
        self.assertEqual(self.meta.ar_classical_track, '06')

    def test_ar_combined_year(self):
        self.assertEqual(self.meta.ar_combined_year, 1989)


class TestAllPropertiesWagner(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta('classical', 'Wagner_Meistersinger', '01.mp3')

    def test_ar_classical_album(self):
        self.assertEqual(self.meta.ar_classical_album,
                         'Die Meistersinger von Nürnberg')

    def test_ar_combined_album(self):
        self.assertEqual(self.meta.ar_combined_album,
                         'Die Meistersinger von Nürnberg')

    def test_ar_initial_album(self):
        self.assertEqual(self.meta.ar_initial_album, 'd')

    def test_ar_initial_artist(self):
        self.assertEqual(self.meta.ar_initial_artist, 'w')

    def test_ar_combined_artist(self):
        self.assertEqual(
            self.meta.ar_combined_artist,
            'Richard Wagner; René Kollo, Helen Donath, Theo Adam, Geraint '
            'Evans, Peter Schreier, Ruth Hesse, Karl Ridderbusch, Chor der '
            'Staatsoper Dresden, MDR Rundfunkchor Leipzig, Staatskapelle '
            'Dresden, Herbert von Karajan')

    def test_ar_combined_artist_sort(self):
        self.assertEqual(
            self.meta.ar_combined_artist_sort,
            'Wagner, Richard; Kollo, René, Donath, Helen, Adam, Theo, Evans, '
            'Geraint, Schreier, Peter, Hesse, Ruth, Ridderbusch, Karl, Chor '
            'der Staatsoper Dresden, MDR Rundfunkchor Leipzig, Staatskapelle '
            'Dresden, Karajan, Herbert von')

    def test_ar_initial_composer(self):
        self.assertEqual(self.meta.ar_initial_composer, 'w')

    def test_ar_combined_composer(self):
        self.assertEqual(self.meta.ar_combined_composer, 'Wagner, Richard')

    def test_ar_combined_disctrack(self):
        self.assertEqual(self.meta.ar_combined_disctrack, '1-01')

    def test_ar_performer(self):
        self.assertEqual(self.meta.ar_performer,
                         'Herbert von Karajan, Staatskapelle Dresden')

    def test_ar_classical_performer(self):
        self.assertEqual(self.meta.ar_classical_performer,
                         'Karajan, StaDre')

    def test_ar_performer_raw(self):
        self.assertEqual(self.meta.ar_performer_raw,
                         [
                             ['conductor', 'Herbert von Karajan'],
                             ['orchestra', 'Staatskapelle Dresden']
                         ])

    def test_ar_performer_short(self):
        self.assertEqual(self.meta.ar_performer_short,
                         'Karajan, StaDre')

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
            'Concerto for French Horn no. 1 in D major, K. 386b / KV 412'
        )

    def test_ar_classical_album_schubert(self):
        self.assertEqual(
            self.schubert.ar_classical_album,
            'Die Winterreise, op. 89, D. 911'
        )

    def test_ar_classical_album_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.ar_classical_album,
            'Swan Lake, op. 20'
        )

    def test_ar_classical_album_wagner(self):
        self.assertEqual(
            self.wagner.ar_classical_album,
            'Die Meistersinger von N\xfcrnberg'
        )

    # ar_initial_composer
    def test_ar_initial_composer_mozart(self):
        self.assertEqual(self.mozart.ar_initial_composer, 'm')

    def test_ar_initial_composer_schubert(self):
        self.assertEqual(self.schubert.ar_initial_composer, 's')

    def test_ar_initial_composer_tschaikowski(self):
        self.assertEqual(self.tschaikowski.ar_initial_composer, 't')

    def test_ar_initial_composer_wagner(self):
        self.assertEqual(self.wagner.ar_initial_composer, 'w')

    # ar_combined_composer
    def test_ar_combined_composer_mozart(self):
        self.assertEqual(
            self.mozart.ar_combined_composer,
            'Mozart, Wolfgang Amadeus'
        )

    def test_ar_combined_composer_mozart2(self):
        self.assertEqual(
            self.mozart2.ar_combined_composer,
            'Mozart, Wolfgang Amadeus'
        )

    def test_ar_combined_composer_schubert(self):
        self.assertEqual(
            self.schubert.ar_combined_composer,
            'Schubert, Franz'
        )

    def test_ar_combined_composer_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.ar_combined_composer,
            'Tchaikovsky, Pyotr Ilyich'
        )

    def test_ar_combined_composer_wagner(self):
        self.assertEqual(
            self.wagner.ar_combined_composer,
            'Wagner, Richard'
        )

    # composer_sort
    def test_composer_sort_mozart(self):
        self.assertEqual(
            self.mozart.composer_sort,
            'Mozart, Wolfgang Amadeus'
        )

    def test_composer_sort_schubert(self):
        self.assertEqual(
            self.schubert.composer_sort,
            'Schubert, Franz'
        )

    def test_composer_sort_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.composer_sort,
            'Tchaikovsky, Pyotr Ilyich'
        )

    def test_composer_sort_wagner(self):
        self.assertEqual(
            self.wagner.composer_sort,
            'Wagner, Richard'
        )

    # ar_classical_performer
    def test_ar_classical_performer_mozart(self):
        self.assertEqual(
            self.mozart.ar_classical_performer,
            'OrpChaOrc'
        )

    def test_ar_classical_performer_schubert(self):
        self.assertEqual(
            self.schubert.ar_classical_performer,
            'Fischer-Dieskau, Moore'
        )

    def test_ar_classical_performer_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.ar_classical_performer,
            'Svetlanov, StaAcaSym'
        )

    def test_ar_classical_performer_wagner(self):
        self.assertEqual(
            self.wagner.ar_classical_performer,
            'Karajan, StaDre'
        )

    # ar_classical_title
    def test_ar_classical_title_mozart(self):
        self.assertEqual(self.mozart.ar_classical_title, 'I. Allegro')

    def test_ar_classical_title_schubert(self):
        self.assertEqual(
            self.schubert.ar_classical_title, 'Gute Nacht')

    def test_ar_classical_title_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.ar_classical_title,
            'Introduction. Moderato assai - Allegro, ma non troppo - Tempo I'
        )

    def test_ar_classical_title_wagner(self):
        self.assertEqual(
            self.wagner.ar_classical_title, 'Vorspiel')

    # ar_classical_track
    def test_ar_classical_track_mozart(self):
        self.assertEqual(self.mozart.ar_classical_track, '01')

    def test_ar_classical_track_schubert(self):
        self.assertEqual(self.schubert.ar_classical_track, '01')

    def test_ar_classical_track_tschaikowski(self):
        self.assertEqual(self.tschaikowski.ar_classical_track, '1-01')

    def test_ar_classical_track_wagner(self):
        self.assertEqual(self.wagner.ar_classical_track, '1-01')


if __name__ == '__main__':
    unittest.main()
