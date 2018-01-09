# -*- coding: utf-8 -*-

"""Test the submodule “meta.py”."""

from audiorename.meta import Meta
import audiorename.meta as meta

import unittest
import os
import tempfile
import shutil
import helper


def get_meta(path_list):
    return Meta(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                *path_list))


class TestEnrich(unittest.TestCase):

    def setUp(self):
        meta.set_useragent()

    def test_recording_pulp_01(self):
        # ['soundtrack', 'Pulp-Fiction', '01.mp3']
        result = meta.query_mbrainz(
            'recording',
            '0480672d-4d88-4824-a06b-917ff408eabe',
        )
        self.assertEqual(result['id'],
                         u'0480672d-4d88-4824-a06b-917ff408eabe')

    def test_recording_mozart_01(self):
        # ['classical', 'Mozart_Horn-concertos', '01.mp3']
        result = meta.query_mbrainz(
            'recording',
            '7886ad6c-11af-435b-8ec3-bca5711f7728',
        )
        self.assertEqual(result['work-relation-list'][0]['work']['id'],
                         u'21fe0bf0-a040-387c-a39d-369d53c251fe')

    def test_release_pulp_01(self):
        # ['soundtrack', 'Pulp-Fiction', '01.mp3']
        result = meta.query_mbrainz(
            'release',
            'ab81edcb-9525-47cd-8247-db4fa969f525',
        )
        self.assertEqual(result['release-group']['id'],
                         u'1703cd63-9401-33c0-87c6-50c4ba2e0ba8')

    def test_release_mozart_01(self):
        # ['classical', 'Mozart_Horn-concertos', '01.mp3'])
        result = meta.query_mbrainz(
            'release',
            '5ed650c5-0f72-4b79-80a7-c458c869f53e',
        )
        self.assertEqual(result['release-group']['id'],
                         u'e1fa28f0-e56e-395b-82d3-a8de54e8c627')

    def test_work_mozart_zauberfloete_unit(self):
        # recording_id 6a0599ea-5c06-483a-ba66-f3a036da900a
        # work_id eafec51f-47c5-3c66-8c36-a524246c85f8
        # Akt 1: 5adc213f-700a-4435-9e95-831ed720f348
        result = meta.work_recursion('eafec51f-47c5-3c66-8c36-a524246c85f8')
        self.assertEqual(result[0]['id'],
                         'eafec51f-47c5-3c66-8c36-a524246c85f8')
        self.assertEqual(result[1]['id'],
                         '5adc213f-700a-4435-9e95-831ed720f348')
        self.assertEqual(result[2]['id'],
                         'e208c5f5-5d37-3dfc-ac0b-999f207c9e46')


###############################################################################
# Public methods
###############################################################################


class TestExportDict(unittest.TestCase):

    def test_export_dict(self):
        meta = get_meta(['files', 'album.mp3'])

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

    def test_enrich_metadata_meistersinger(self):
        tmp = helper.copy_to_tmp(['classical', 'without_work.mp3'])
        meta = Meta(tmp)
        self.assertEqual(meta.mb_trackid,
                         '00ba1660-4e35-4985-86b2-8b7a3e99b1e5')
        self.assertEqual(meta.mb_workid, None)
        self.assertEqual(meta.work, None)

        meta.enrich_metadata()
        self.assertEqual(meta.mb_workid,
                         '6b198406-4fbf-3d61-82db-0b7ef195a7fe')
        self.assertEqual(meta.work, u'Die Meistersinger von Nürnberg, ' +
                         'WWV 96: Akt I. Vorspiel')
        meta.save()

        finished = Meta(tmp)
        self.assertEqual(finished.mb_workid,
                         '6b198406-4fbf-3d61-82db-0b7ef195a7fe')
        self.assertEqual(finished.work, u'Die Meistersinger von Nürnberg, ' +
                         'WWV 96: Akt I. Vorspiel')
        self.assertEqual(
            finished.mb_workhierarchy_ids,
            u'4d644732-9876-4b0d-9c2c-b6a738d6530e/'
            '73663bd3-392f-45a7-b4ff-e75c01f5926a/'
            '6b198406-4fbf-3d61-82db-0b7ef195a7fe')
        self.assertEqual(
            finished.work_hierarchy,
            u'Die Meistersinger von Nürnberg, WWV 96 -> '
            u'Die Meistersinger von Nürnberg, WWV 96: Akt I -> '
            u'Die Meistersinger von Nürnberg, WWV 96: Akt I. Vorspiel'
        )
        self.assertEqual(finished.releasegroup_types, u'album')

    def test_enrich_metadata_pulp(self):
        tmp = helper.copy_to_tmp(['soundtrack', 'Pulp-Fiction', '01.mp3'])
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
                         u'soundtrack/album/compilation')


class TestRemapClassical(unittest.TestCase):

    def setUp(self):
        test_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'classical',
            'Mozart_Horn-concertos', '06.mp3'
        )
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
                                         'major, K. 447: I. Allegro')
        self.assertEqual(
            finished.comments,
            u'Original metadata: title: Horn Concerto No. 3 in E-flat major, '
            'K. 447: I. Allegro; track: 6; artist: Wolfgang Amadeus Mozart; '
            'album: 4 Hornkonzerte (Concertos for Horn and Orchestra); '
        )


###############################################################################
# Properties
###############################################################################


# album_clean
class TestPropertyAlbumClean(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])

    def assertAlbumClean(self, album, compare=u'Lorem ipsum'):
        self.meta.album = album
        self.assertEqual(self.meta.album_clean, compare)

    def test_disc_removal(self):
        self.assertAlbumClean('Lorem ipsum (Disc 1)')
        self.assertAlbumClean('Lorem ipsum(Disc 1)')
        self.assertAlbumClean('Lorem ipsum (Disc)')
        self.assertAlbumClean('Lorem ipsum (Disk 100)')
        self.assertAlbumClean('Lorem ipsum (disk99)')

    def test_empty(self):
        self.assertAlbumClean('', '')

    def test_real_world(self):
        meta = get_meta(['real-world', '_compilations', 't',
                         'The-Greatest-No1s-of-the-80s_1994',
                         '2-09_Respectable.mp3'])
        self.assertEqual(meta.album_clean, u'The Greatest No.1s of the 80s')


# artistsafe (integration)
class TestPropertyArtistSafe(unittest.TestCase):

    def test_artist(self):
        meta = get_meta(['meta', 'artist.mp3'])
        self.assertEqual(meta.artistsafe, u'artist')

    def test_artist_sort(self):
        meta = get_meta(['meta', 'artist_sort.mp3'])
        self.assertEqual(meta.artistsafe_sort, u'artist_sort')

    def test_albumartist(self):
        meta = get_meta(['meta', 'albumartist.mp3'])
        self.assertEqual(meta.artistsafe, u'albumartist')


# artistsafe (unit)
class TestPropertyArtistSafeUnit(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])
        self.meta.albumartist_credit = u''
        self.meta.albumartist_sort = u''
        self.meta.albumartist = u''
        self.meta.artist_credit = u''
        self.meta.artist_sort = u''
        self.meta.artist = u''

    def assertArtistSort(self, key):
        setattr(self.meta, key, key)
        self.assertEqual(self.meta.artistsafe, key)
        self.assertEqual(self.meta.artistsafe_sort, key)

    def test_unkown(self):
        self.assertEqual(self.meta.artistsafe, u'Unknown')
        self.assertEqual(self.meta.artistsafe_sort, u'Unknown')

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
        self.assertEqual(self.meta.artistsafe, 'artist')
        self.assertEqual(self.meta.artistsafe_sort, 'artist_sort')

    def test_albumartist__artist__artist_sort(self):
        self.meta.albumartist = 'albumartist'
        self.meta.artist = 'artist'
        self.meta.artist_sort = 'artist_sort'
        self.assertEqual(self.meta.artistsafe, 'albumartist')
        self.assertEqual(self.meta.artistsafe_sort, 'artist_sort')

    def test_artist__albumartist_sort__artist_sort(self):
        self.meta.albumartist_sort = 'albumartist_sort'
        self.meta.artist = 'artist'
        self.meta.artist_sort = 'artist_sort'
        self.assertEqual(self.meta.artistsafe, 'artist')
        self.assertEqual(self.meta.artistsafe_sort, 'albumartist_sort')

    def test_shell_unfriendly(self):
        self.meta.shell_friendly = False
        self.meta.artist_sort = 'Lastname, Prename'
        self.assertEqual(self.meta.artistsafe_sort, 'Lastname, Prename')

    def test_shell_friendly(self):
        self.meta.shell_friendly = True
        self.meta.artist_sort = 'Lastname, Prename'
        self.assertEqual(self.meta.artistsafe_sort, 'Lastname_Prename')


# disctrack (integration)
class TestPropertyDiskTrack(unittest.TestCase):

    def test_single_disc(self):
        meta = get_meta(['real-world', 'e', 'Everlast', 'Eat-At-Whiteys_2000',
                         '02_Black-Jesus.mp3'])
        self.assertEqual(meta.disctrack, u'02')

    def test_double_disk(self):
        meta = get_meta(['real-world', '_compilations', 't',
                         'The-Greatest-No1s-of-the-80s_1994',
                         '2-09_Respectable.mp3'])
        self.assertEqual(meta.disctrack, u'2-09')


# disctrack (unit)
class TestPropertyDiskTrackUnit(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])
        self.meta.track = u''
        self.meta.tracktotal = u''
        self.meta.disc = u''
        self.meta.disctotal = u''

    def test_empty(self):
        self.assertEqual(self.meta.disctrack, u'')

    def test_no_track(self):
        self.meta.disc = '2'
        self.meta.disctotal = '3'
        self.meta.tracktotal = '36'
        self.assertEqual(self.meta.disctrack, u'')

    def test_disc_track(self):
        self.meta.disc = '2'
        self.meta.track = '4'
        self.assertEqual(self.meta.disctrack, u'2-04')

    def test_disk_total_one(self):
        self.meta.disc = '1'
        self.meta.track = '4'
        self.meta.disctotal = '1'
        self.meta.tracktotal = '36'
        self.assertEqual(self.meta.disctrack, u'04')

    def test_all_set(self):
        self.meta.disc = '2'
        self.meta.track = '4'
        self.meta.disctotal = '3'
        self.meta.tracktotal = '36'
        self.assertEqual(self.meta.disctrack, u'2-04')

    def test_zfill_track(self):
        self.meta.track = '4'
        self.meta.tracktotal = '100'
        self.assertEqual(self.meta.disctrack, u'004')

        self.meta.tracktotal = '10'
        self.assertEqual(self.meta.disctrack, u'04')

        self.meta.tracktotal = '5'
        self.assertEqual(self.meta.disctrack, u'04')

    def test_zfill_disc(self):
        self.meta.track = '4'
        self.meta.tracktotal = '10'
        self.meta.disc = '2'
        self.meta.disctotal = '10'
        self.assertEqual(self.meta.disctrack, u'02-04')

        self.meta.disctotal = '100'
        self.assertEqual(self.meta.disctrack, u'002-04')


# performer*
class TestPropertyPerformerDifferentFormats(unittest.TestCase):

    def getMeta(self, extension):
        return get_meta(['performers', 'blank.' + extension])

    def assertPerformer(self, meta):
        raw = meta.performer_raw
        self.assertEqual(raw[0][0], u'conductor')
        self.assertEqual(raw[0][1], u'Fabio Luisi')
        self.assertEqual(raw[1][0], u'orchestra')
        self.assertEqual(raw[1][1], u'Wiener Symphoniker')
        self.assertEqual(raw[2][0], u'soprano vocals')
        self.assertEqual(raw[2][1], u'Elena Filipova')
        self.assertEqual(raw[3][0], u'choir vocals')
        self.assertEqual(raw[3][1], u'Chor der Wiener Volksoper')

        self.assertEqual(meta.performer, u'Fabio Luisi, Wiener ' +
                         u'Symphoniker, Elena Filipova, Chor der Wiener ' +
                         u'Volksoper')
        self.assertEqual(meta.performer_short, u'Luisi, WieSym')

        self.assertEqual(meta.performer_classical, u'Luisi, WieSym')

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
        meta = get_meta(['show-case', 'Beatles_Yesterday.mp3'])
        self.assertEqual(meta.soundtrack, True)

    def test_no_soundtrack(self):
        meta = get_meta(['classical', 'Schubert_Winterreise', '01.mp3'])
        self.assertEqual(meta.soundtrack, False)


# track_classical
class TestPropertyTrackClassical(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])

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
        self.assertEqual(self.meta.track_classical, compare)

    def test_function(self):
        self.assertTrack('III. Credo', u'03')
        self.assertTrack('III Credo', '4-02')
        self.assertTrack('Credo', '4-02')
        self.meta.track = 123
        self.assertEqual(self.meta.track_classical, '4-123')


# work (integration)
class TestPropertyWork(unittest.TestCase):

    def test_work(self):
        meta = get_meta(['classical', 'Mozart_Horn-concertos', '01.mp3'])
        self.assertEqual(
            meta.work,
            u'Concerto for French Horn no. 1 in D major, ' +
            u'K. 386b / KV 412: I. Allegro'
        )
        self.assertEqual(
            meta.mb_workid,
            u'21fe0bf0-a040-387c-a39d-369d53c251fe'
        )
        self.assertEqual(meta.composer_sort, u'Mozart, Wolfgang Amadeus')


# title_classical
class TestPropertyTitleClassical(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])

    def test_work_title(self):
        self.meta.title = 'work: title'
        self.assertEqual(self.meta.title_classical, 'title')

    def test_work_work_title(self):
        self.meta.title = 'work: work: title'
        self.assertEqual(self.meta.title_classical, 'work: title')

    def test_title(self):
        self.meta.title = 'title'
        self.assertEqual(self.meta.title_classical, 'title')


# year_safe
class TestPropertyYearSafe(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])
        self.meta.year = None
        self.meta.original_year = None

    def test_empty(self):
        self.assertEqual(self.meta.year_safe, '')

    def test_year(self):
        self.meta.year = 1978
        self.assertEqual(self.meta.year_safe, '1978')

    def test_original_year(self):
        self.meta.original_year = 1978
        self.assertEqual(self.meta.year_safe, '1978')

    def test_year__original_year(self):
        self.meta.year = 2016
        self.meta.original_year = 1978
        self.assertEqual(self.meta.year_safe, '1978')


###############################################################################
# Static methods
###############################################################################


class TestStaticMethodInitials(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])

    def test_lowercase(self):
        self.assertEqual(self.meta._initials(u'beethoven'), u'b')

    def test_uppercase(self):
        self.assertEqual(self.meta._initials(u'Beethoven'), u'b')


class TestStaticMethodNormalizePerformer(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])

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
        self.meta = get_meta(['files', 'album.mp3'])

    def test_slash(self):
        self.assertEqual(self.meta._sanitize(u'lol/lol'), u'lollol')

    def test_whitespaces(self):
        self.assertEqual(self.meta._sanitize(u'lol  lol'), u'lol lol')

    def test_list(self):
        self.assertEqual(self.meta._sanitize([]), u'')


class TestStaticMethodShortenPerformer(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])

    def test_performer_shorten(self):
        s = self.meta._shorten_performer(u'Ludwig van Beethoven')
        self.assertEqual(s, u'Lud. van Bee.')

    def test_performer_shorten_option_separator(self):
        s = self.meta._shorten_performer(u'Ludwig van Beethoven',
                                         separator=u'--')
        self.assertEqual(s, u'Lud.--van--Bee.')

    def test_performer_shorten_option_abbreviation(self):
        s = self.meta._shorten_performer(u'Ludwig van Beethoven',
                                         abbreviation=u'_')
        self.assertEqual(s, u'Lud_ van Bee_')

    def test_performer_shorten_option_all(self):
        s = self.meta._shorten_performer(u'Ludwig van Beethoven',
                                         separator=u'',
                                         abbreviation=u'')
        self.assertEqual(s, u'LudvanBee')


class TestStaticMethodUnifyList(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])

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
# All properties
###############################################################################


class TestAllPropertiesHines(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['real-world', 'h', 'Hines_Earl',
                              'Just-Friends_1989', '06_Indian-Summer.mp3'])

    def test_album_classical(self):
        self.assertEqual(self.meta.album_classical, u'')

    def test_album_clean(self):
        self.assertEqual(self.meta.album_clean, u'Just Friends')

    def test_album_initial(self):
        self.assertEqual(self.meta.album_initial, u'j')

    def test_artist_initial(self):
        self.assertEqual(self.meta.artist_initial, u'h')

    def test_artistsafe(self):
        self.assertEqual(self.meta.artistsafe, u'Earl Hines')

    def test_artistsafe_sort(self):
        self.assertEqual(self.meta.artistsafe_sort, u'Hines, Earl')

    def test_composer_initial(self):
        self.assertEqual(self.meta.composer_initial, u'e')

    def test_composer_safe(self):
        self.assertEqual(self.meta.composer_safe, u'Earl Hines')

    def test_disctrack(self):
        self.assertEqual(self.meta.disctrack, u'06')

    def test_performer(self):
        self.assertEqual(self.meta.performer, u'')

    def test_performer_classical(self):
        self.assertEqual(self.meta.performer_classical, u'Earl Hines')

    def test_performer_raw(self):
        self.assertEqual(self.meta.performer_raw, [])

    def test_performer_short(self):
        self.assertEqual(self.meta.performer_short, u'')

    def test_title_classical(self):
        self.assertEqual(self.meta.title_classical, u'Indian Summer')

    def test_track_classical(self):
        self.assertEqual(self.meta.track_classical, u'06')

    def test_year_safe(self):
        self.assertEqual(self.meta.year_safe, '1989')


class TestAllPropertiesWagner(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['classical', 'Wagner_Meistersinger', '01.mp3'])

    def test_album_classical(self):
        self.assertEqual(self.meta.album_classical,
                         u'Die Meistersinger von Nürnberg')

    def test_album_clean(self):
        self.assertEqual(self.meta.album_clean,
                         u'Die Meistersinger von Nürnberg')

    def test_album_initial(self):
        self.assertEqual(self.meta.album_initial, u'd')

    def test_artist_initial(self):
        self.assertEqual(self.meta.artist_initial, u'w')

    def test_artistsafe(self):
        self.assertEqual(
            self.meta.artistsafe,
            u'Richard Wagner; René Kollo, Helen Donath, Theo Adam, Geraint ' +
            'Evans, Peter Schreier, Ruth Hesse, Karl Ridderbusch, Chor der ' +
            'Staatsoper Dresden, MDR Rundfunkchor Leipzig, Staatskapelle ' +
            'Dresden, Herbert von Karajan')

    def test_artistsafe_sort(self):
        self.assertEqual(
            self.meta.artistsafe_sort,
            u'Wagner, Richard; Kollo, René, Donath, Helen, Adam, Theo, Evans, '
            'Geraint, Schreier, Peter, Hesse, Ruth, Ridderbusch, Karl, Chor '
            'der Staatsoper Dresden, MDR Rundfunkchor Leipzig, Staatskapelle '
            'Dresden, Karajan, Herbert von')

    def test_composer_initial(self):
        self.assertEqual(self.meta.composer_initial, u'w')

    def test_composer_safe(self):
        self.assertEqual(self.meta.composer_safe, u'Wagner, Richard')

    def test_disctrack(self):
        self.assertEqual(self.meta.disctrack, u'1-01')

    def test_performer(self):
        self.assertEqual(self.meta.performer,
                         u'Herbert von Karajan, Staatskapelle Dresden')

    def test_performer_classical(self):
        self.assertEqual(self.meta.performer_classical,
                         u'Karajan, StaDre')

    def test_performer_raw(self):
        self.assertEqual(self.meta.performer_raw,
                         [
                             [u'conductor', u'Herbert von Karajan'],
                             [u'orchestra', u'Staatskapelle Dresden']
                         ])

    def test_performer_short(self):
        self.assertEqual(self.meta.performer_short,
                         u'Karajan, StaDre')

    def test_title_classical(self):
        self.assertEqual(self.meta.title_classical, 'Vorspiel')

    def test_track_classical(self):
        self.assertEqual(self.meta.track_classical, '1-01')

    def test_year_safe(self):
        self.assertEqual(self.meta.year_safe, '1971')


class TestClassical(unittest.TestCase):

    def setUp(self):
        self.mozart = get_meta(['classical', 'Mozart_Horn-concertos',
                               '01.mp3'])
        self.mozart2 = get_meta(['classical', 'Mozart_Horn-concertos',
                                '02.mp3'])
        self.schubert = get_meta(['classical', 'Schubert_Winterreise',
                                 '01.mp3'])
        self.tschaikowski = get_meta(['classical', 'Tschaikowski_Swan-Lake',
                                     '1-01.mp3'])
        self.wagner = get_meta(['classical', 'Wagner_Meistersinger', '01.mp3'])

    # album_classical
    def test_album_classical_mozart(self):
        self.assertEqual(
            self.mozart.album_classical,
            u'Concerto for French Horn no. 1 in D major, K. 386b / KV 412'
        )

    def test_album_classical_schubert(self):
        self.assertEqual(
            self.schubert.album_classical,
            u'Die Winterreise, op. 89, D. 911'
        )

    def test_album_classical_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.album_classical,
            u'Swan Lake, op. 20'
        )

    def test_album_classical_wagner(self):
        self.assertEqual(
            self.wagner.album_classical,
            u'Die Meistersinger von N\xfcrnberg'
        )

    # composer_initial
    def test_composer_initial_mozart(self):
        self.assertEqual(self.mozart.composer_initial, u'm')

    def test_composer_initial_schubert(self):
        self.assertEqual(self.schubert.composer_initial, u's')

    def test_composer_initial_tschaikowski(self):
        self.assertEqual(self.tschaikowski.composer_initial, u't')

    def test_composer_initial_wagner(self):
        self.assertEqual(self.wagner.composer_initial, u'w')

    # composer_safe
    def test_composer_safe_mozart(self):
        self.assertEqual(
            self.mozart.composer_safe,
            u'Mozart, Wolfgang Amadeus'
        )

    def test_composer_safe_mozart2(self):
        self.assertEqual(
            self.mozart2.composer_safe,
            u'Mozart, Wolfgang Amadeus'
        )

    def test_composer_safe_schubert(self):
        self.assertEqual(
            self.schubert.composer_safe,
            u'Schubert, Franz'
        )

    def test_composer_safe_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.composer_safe,
            u'Tchaikovsky, Pyotr Ilyich'
        )

    def test_composer_safe_wagner(self):
        self.assertEqual(
            self.wagner.composer_safe,
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

    # performer_classical
    def test_performer_classical_mozart(self):
        self.assertEqual(
            self.mozart.performer_classical,
            u'OrpChaOrc'
        )

    def test_performer_classical_schubert(self):
        self.assertEqual(
            self.schubert.performer_classical,
            u'Fischer-Dieskau, Moore'
        )

    def test_performer_classical_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.performer_classical,
            u'Svetlanov, StaAcaSym'
        )

    def test_performer_classical_wagner(self):
        self.assertEqual(
            self.wagner.performer_classical,
            u'Karajan, StaDre'
        )

    # title_classical
    def test_title_classical_mozart(self):
        self.assertEqual(self.mozart.title_classical, u'I. Allegro')

    def test_title_classical_schubert(self):
        self.assertEqual(
            self.schubert.title_classical, u'Gute Nacht')

    def test_title_classical_tschaikowski(self):
        self.assertEqual(
            self.tschaikowski.title_classical,
            u'Introduction. Moderato assai - Allegro, ma non troppo - Tempo I'
        )

    def test_title_classical_wagner(self):
        self.assertEqual(
            self.wagner.title_classical, u'Vorspiel')

    # track_classical
    def test_track_classical_mozart(self):
        self.assertEqual(self.mozart.track_classical, u'01')

    def test_track_classical_schubert(self):
        self.assertEqual(self.schubert.track_classical, u'01')

    def test_track_classical_tschaikowski(self):
        self.assertEqual(self.tschaikowski.track_classical, u'1-01')

    def test_track_classical_wagner(self):
        self.assertEqual(self.wagner.track_classical, u'1-01')


if __name__ == '__main__':
    unittest.main()
