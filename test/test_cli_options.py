# -*- coding: utf-8 -*-

"""Test all command line options."""

import unittest
import audiorename
import os
import shutil
import tempfile
import helper


# --classical
class TestClassical(unittest.TestCase):

    def assertDryRun(self, folder, track, test):
        self.assertEqual(helper.dry_run([
            '--classical',
            helper.get_testfile('classical', folder, track)
        ]), test)

    d = '/d/Debussy_Claude/'
    e = 'Estampes-L-100_[Jean-Claude-Pennetier]'
    p = 'Pour-le-piano-L-95_[Jean-Claude-Pennetier]'

    def test_debussy_01(self):
        self.assertDryRun(
            'Debussy_Estampes-etc', '01.mp3',
            self.d + self.e + '/01_Pagodes_.mp3'
        )

    def test_debussy_02(self):
        self.assertDryRun(
            'Debussy_Estampes-etc', '02.mp3',
            self.d + self.e + '/02_Soiree-dans-Grenade_.mp3'
        )

    def test_debussy_03(self):
        self.assertDryRun(
            'Debussy_Estampes-etc', '03.mp3',
            self.d + self.e + '/03_Jardins-sous-la-pluie_.mp3'
        )

    def test_debussy_04(self):
        self.assertDryRun(
            'Debussy_Estampes-etc', '04.mp3',
            self.d + self.p + '/04_Prelude_.mp3'
        )

    m = '/m/Mozart_Wolfgang-Amadeus/'
    mp1 = u'[OrpChaOrc]'
    mp2 = u'[OrpChaOrc]'
    h1 = 'Concerto-for-French-Horn-no-1-in-D-major-K_' + mp1
    h2 = 'Concerto-for-Horn-no-2-in-E-flat-major-K-417_' + mp2

    def test_mozart_01(self):
        self.assertDryRun(
            'Mozart_Horn-concertos', '01.mp3',
            self.m + self.h1 + '/01_I-Allegro_fa140702.mp3'
        )

    def test_mozart_02(self):
        self.assertDryRun(
            'Mozart_Horn-concertos', '02.mp3',
            self.m + self.h1 +
            '/02_II-Rondo-Allegro_a897e98e.mp3'
        )

    def test_mozart_03(self):
        self.assertDryRun(
            'Mozart_Horn-concertos', '03.mp3',
            self.m + self.h2 + '/03_I-Allegro_d557146b.mp3'
        )

    def test_mozart_04(self):
        self.assertDryRun(
            'Mozart_Horn-concertos', '04.mp3',
            self.m + self.h2 + '/04_II-Andante_001c2df3.mp3'
        )

    s = '/s/Schubert_Franz/'
    w = 'Die-Winterreise-op-89-D-911_[Fischer-Dieskau-Moore]/'

    def test_schubert_01(self):
        self.assertDryRun(
            'Schubert_Winterreise', '01.mp3',
            self.s + self.w + '01_Gute-Nacht_311cb6a3.mp3'
        )

    def test_schubert_02(self):
        self.assertDryRun(
            'Schubert_Winterreise', '02.mp3',
            self.s + self.w + '02_Die-Wetterfahne_5b9644f0.mp3'
        )

    def test_schubert_03(self):
        self.assertDryRun(
            'Schubert_Winterreise', '03.mp3',
            self.s + self.w + '03_Gefrorne-Traenen_4b78f893.mp3'
        )

    def test_schubert_04(self):
        self.assertDryRun(
            'Schubert_Winterreise', '04.mp3',
            self.s + self.w + '04_Erstarrung_63bc8e2a.mp3'
        )

    t = '/t/Tchaikovsky_Pyotr-Ilyich/'
    lake = 'Swan-Lake-op-20_[Svetlanov-StaAcaSym]/'

    def test_tschaikowski_01(self):
        self.assertDryRun(
            'Tschaikowski_Swan-Lake', '1-01.mp3',
            self.t + self.lake +
            '1-01_Introduction-Moderato-assai-Allegro-ma-non-troppo-' +
            'Tempo-I_3f6fc6b3.mp3'
        )

    def test_tschaikowski_02(self):
        self.assertDryRun(
            'Tschaikowski_Swan-Lake', '1-02.mp3',
            self.t + self.lake + '1-02_Act-I-no-1-Scene-Allegro-giusto_' +
            '29413f6c.mp3'
        )

    def test_tschaikowski_03(self):
        self.assertDryRun(
            'Tschaikowski_Swan-Lake', '1-03.mp3',
            self.t + self.lake + '1-03_Act-I-no-2-Valse-Tempo-di-valse_' +
            '5303b318.mp3'
        )

    def test_tschaikowski_04(self):
        self.assertDryRun(
            'Tschaikowski_Swan-Lake', '1-04.mp3',
            self.t + self.lake + '1-04_Act-I-no-3-Scene-Allegro-moderato_' +
            '4d5781a4.mp3'
        )

    wr = '/w/Wagner_Richard/'
    mn = 'Die-Meistersinger-von-Nuernberg_[Karajan-StaDre]/'

    def test_wagner_01(self):
        self.assertDryRun(
            'Wagner_Meistersinger', '01.mp3',
            self.wr + self.mn + '1-01_Vorspiel_313c5f00.mp3'
        )

    def test_wagner_02(self):
        self.assertDryRun(
            'Wagner_Meistersinger', '02.mp3',
            self.wr + self.mn +
            '1-02_Akt-I-Szene-I-Da-zu-dir-der-Heiland-kam-Gemeinde_' +
            'cdd9f298.mp3'
        )

    def test_wagner_03(self):
        self.assertDryRun(
            'Wagner_Meistersinger', '03.mp3',
            self.wr + self.mn + '1-03_Akt-I-Szene-I-Verweilt-Ein-Wort-' +
            'Walther-Eva-Magdalene_adab7b8c.mp3'
        )

    def test_wagner_04(self):
        self.assertDryRun(
            'Wagner_Meistersinger', '04.mp3',
            self.wr + self.mn +
            '1-04_Akt-I-Szene-I-Da-bin-ich-David-Magdalene-Walther-Eva' +
            '_f3f0231f.mp3'
        )


# --copy
class TestBasicCopy(unittest.TestCase):

    def setUp(self):
        self.tmp_album = helper.copy_to_tmp('files', 'album.mp3')
        with helper.Capturing():
            audiorename.execute(['--copy', self.tmp_album])
        self.tmp_compilation = helper.copy_to_tmp('files', 'compilation.mp3')
        with helper.Capturing():
            audiorename.execute(['--copy', self.tmp_compilation])

    def test_album(self):
        self.assertTrue(helper.is_file(self.tmp_album))
        self.assertTrue(
            os.path.isfile(
                helper.dir_cwd +
                helper.path_album
            )
        )

    def test_compilation(self):
        self.assertTrue(os.path.isfile(self.tmp_compilation))
        self.assertTrue(
            os.path.isfile(
                helper.dir_cwd + helper.path_compilation
            )
        )

    def tearDown(self):
        shutil.rmtree(helper.dir_cwd + '/_compilations/')
        shutil.rmtree(helper.dir_cwd + '/t/')


# --debug
class TestDebug(unittest.TestCase):

    def test_debug(self):
        tmp = helper.get_testfile('files', 'album.mp3')

        with helper.Capturing() as output:
            audiorename.execute([
                '--debug',
                tmp
            ])

        self.assertEqual(output[-1], u'          year_safe: 2001')


# --delete-existing
class TestDeleteExisting(unittest.TestCase):

    def test_delete_existing(self):
        tmp1 = helper.copy_to_tmp('files', 'album.mp3')
        tmp2 = helper.copy_to_tmp('files', 'album.mp3')

        target = tempfile.mkdtemp()

        self.assertTrue(os.path.isfile(tmp1))
        self.assertTrue(os.path.isfile(tmp2))

        with helper.Capturing() as output1:
            audiorename.execute([
                '--delete-existing',
                '--target',
                target,
                tmp1
            ])

        self.assertTrue('Move' in helper.join(output1))
        self.assertFalse(os.path.isfile(tmp1))
        self.assertTrue(os.path.isfile(tmp2))

        with helper.Capturing() as output2:
            audiorename.execute([
                '--delete-existing',
                '--target',
                target,
                tmp2
            ])

        self.assertTrue('Delete' in helper.join(output2))
        self.assertFalse(os.path.isfile(tmp1))
        self.assertFalse(os.path.isfile(tmp2))


# --dry-run
class TestDryRun(unittest.TestCase):

    def setUp(self):
        self.tmp_album = helper.copy_to_tmp('files', 'album.mp3')
        with helper.Capturing() as self.output_album:
            audiorename.execute(['--dry-run', self.tmp_album])

        self.tmp_compilation = helper.copy_to_tmp('files', 'compilation.mp3')
        with helper.Capturing() as self.output_compilation:
            audiorename.execute(['--dry-run', self.tmp_compilation])

    def test_output_album(self):
        self.assertTrue(helper.has(self.output_album, 'Dry run'))
        self.assertTrue(helper.has(self.output_album, self.tmp_album))

    def test_output_compilation(self):
        self.assertTrue(helper.has(self.output_compilation, 'Dry run'))
        self.assertTrue(
            helper.has(self.output_compilation, self.tmp_compilation)
        )

    def test_album(self):
        self.assertTrue(helper.is_file(self.tmp_album))
        self.assertFalse(
            os.path.isfile(
                helper.dir_cwd +
                helper.path_album
            )
        )

    def test_compilation(self):
        self.assertTrue(helper.is_file(self.tmp_compilation))
        self.assertFalse(
            os.path.isfile(
                helper.dir_cwd + helper.path_compilation
            )
        )


# --enrich-metadata
class TestEnrichMetadata(unittest.TestCase):

    def test_pass(self):
        tmp = helper.copy_to_tmp('classical', 'without_work.mp3')
        from audiorename.meta import Meta

        orig = Meta(tmp)
        self.assertEqual(orig.work, None)

        with helper.Capturing() as output:
            audiorename.execute(['--enrich-metadata', '--no-rename', tmp])

        self.assertTrue('Enrich metadata' in helper.join(output))

        with_work = Meta(tmp)
        self.assertEqual(
            with_work.work,
            u'Die Meistersinger von N\xfcrnberg, WWV 96: Akt I. Vorspiel'
        )


# --field-skip
class TestSkipIfEmpty(unittest.TestCase):

    def setUp(self):
        with helper.Capturing() as self.album:
            audiorename.execute([
                '--field-skip',
                'lol',
                helper.copy_to_tmp('files', 'album.mp3')
            ])
        with helper.Capturing() as self.compilation:
            audiorename.execute([
                '--field-skip',
                'album',
                '-d',
                '-c',
                '/tmp/c',
                helper.copy_to_tmp('files', 'compilation.mp3')
            ])

    def test_album(self):
        self.assertTrue(helper.has(self.album, 'No field'))

    def test_compilation(self):
        self.assertTrue(helper.has(self.compilation, 'Dry run'))


# --format
class TestCustomFormats(unittest.TestCase):

    def setUp(self):
        with helper.Capturing():
            audiorename.execute([
                '--format',
                'tmp/$title - $artist',
                helper.copy_to_tmp('files', 'album.mp3')
            ])
        with helper.Capturing():
            audiorename.execute([
                '--compilation',
                'tmp/comp_$title - $artist',
                helper.copy_to_tmp('files', 'compilation.mp3')
            ])

    def test_format(self):
        self.assertTrue(os.path.isfile(
            helper.dir_cwd + '/tmp/full - the artist.mp3'
        ))

    def test_compilation(self):
        self.assertTrue(os.path.isfile(
            helper.dir_cwd + '/tmp/comp_full - the artist.mp3'
        ))

    def tearDown(self):
        shutil.rmtree(helper.dir_cwd + '/tmp/')


# --job-info
class TestJobInfo(unittest.TestCase):

    def test_dry_run(self):
        with helper.Capturing() as output:
            audiorename.execute(['--dry-run', '--job-info',
                                helper.get_testfile('mixed_formats')])

        output = str(output)
        self.assertTrue('Versions: ' in output)
        self.assertTrue('audiorename=' in output)
        self.assertTrue('phrydy=' in output)
        self.assertTrue('tmep=' in output)
        self.assertTrue('Source: ' in output)
        self.assertTrue('Target: ' in output)


# --mb-track-listing
class TestMbTrackListing(unittest.TestCase):

    def mb_track_listing(self, folder, track):
        with helper.Capturing() as output:
            audiorename.execute([
                '--mb-track-listing',
                helper.get_testfile('classical', folder, track)
            ])
        return output[0]

    def test_debussy(self):
        audiorename.audiofile.counter = 0
        self.assertEqual(self.mb_track_listing('Debussy_Estampes-etc',
                         '01.mp3'),
                         '1. Estampes/Images/Pour le Piano: Estampes: ' +
                         'Pagodes (0:00)')

    def test_schubert(self):
        self.assertEqual(self.mb_track_listing('Schubert_Winterreise',
                         '01.mp3'),
                         '1. Winterreise: Winterreise, D. 911: Gute Nacht ' +
                         '(0:00)')

    def test_folder(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--mb-track-listing',
                helper.get_testfile('classical', 'Schubert_Winterreise')
            ])

        self.assertEqual(
            output[0],
            '1. Winterreise: Winterreise, D. 911: Gute Nacht (0:00)'
        )

        self.assertEqual(
            output[23],
            '24. Winterreise: Winterreise, D. 911: Der Leiermann (0:00)'
        )


# --soundtrack
class TestSoundtrack(unittest.TestCase):

    def assertDryRun(self, folder, track, test):
        self.assertEqual(helper.dry_run([
            '--soundtrack',
            '$album_initial/' +
            '%shorten{$album_clean}' +
            '%ifdef{year_safe,_${year_safe}}/' +
            '${disctrack}_${artist}_%shorten{$title}',
            helper.get_testfile('soundtrack', folder, track)
        ]), test)

    def test_pulp_01(self):
        self.assertDryRun(
            'Pulp-Fiction', '01.mp3',
            '/p/Pulp-Fiction_1994/01_[dialogue]_Pumpkin-and-Honey-Bunny.mp3'
        )

    def test_pulp_02(self):
        self.assertDryRun(
            'Pulp-Fiction', '02.mp3',
            '/p/Pulp-Fiction_1994/02_Dick-Dale-and-His-Del-Tones_Misirlou.mp3'
        )

    def test_pulp_03(self):
        self.assertDryRun(
            'Pulp-Fiction', '03.mp3',
            '/p/Pulp-Fiction_1994/03_Kool-The-Gang_Jungle-Boogie.mp3'
        )

    def test_pulp_04(self):
        self.assertDryRun(
            'Pulp-Fiction', '04.mp3',
            '/p/Pulp-Fiction_1994/' +
            '04_[dialogue]_Royale-With-Cheese-dialogue.mp3'
        )

    def test_pulp_05(self):
        self.assertDryRun(
            'Pulp-Fiction', '05.mp3',
            '/p/Pulp-Fiction_1994/' +
            '05_The-Brothers-Johnson_Strawberry-Letter-23.mp3'
        )

    def test_pulp_06(self):
        self.assertDryRun(
            'Pulp-Fiction', '06.mp3',
            '/p/Pulp-Fiction_1994/' +
            '06_[dialogue]_Ezekiel-2517-dialogue-Samuel-L.mp3'
        )

    def test_pulp_07(self):
        self.assertDryRun(
            'Pulp-Fiction', '07.mp3',
            '/p/Pulp-Fiction_1994/07_Al-Green_Lets-Stay-Together.mp3'
        )

    def test_pulp_08(self):
        self.assertDryRun(
            'Pulp-Fiction', '08.mp3',
            '/p/Pulp-Fiction_1994/08_The-Tornadoes_Bustin-Surfboards.mp3'
        )

    def test_pulp_09(self):
        self.assertDryRun(
            'Pulp-Fiction', '09.mp3',
            '/p/Pulp-Fiction_1994/09_The-Centurions_Bullwinkle-Part-II.mp3'
        )

    def test_pulp_10(self):
        self.assertDryRun(
            'Pulp-Fiction', '10.mp3',
            '/p/Pulp-Fiction_1994/' +
            '10_Dusty-Springfield_Son-of-a-Preacher-Man.mp3'
        )


# --source-as-target
class TestSourceAsTarget(unittest.TestCase):

    def setUp(self):
        self.tmp_album = helper.copy_to_tmp('files', 'album.mp3')
        self.dir_album = os.path.dirname(self.tmp_album)
        with helper.Capturing():
            audiorename.execute([
                '--source-as-target',
                '-f',
                'a',
                self.tmp_album
            ])

        self.tmp_compilation = helper.copy_to_tmp('files', 'compilation.mp3')
        with helper.Capturing():
            audiorename.execute([
                '--source-as-target',
                '-c',
                'c',
                self.tmp_compilation
            ])

    def test_album(self):
        self.assertTrue(helper.is_file(self.dir_album + '/a.mp3'))


# --stats
class TestStats(unittest.TestCase):

    def test_dry_run(self):
        with helper.Capturing() as output:
            audiorename.execute(['--dry-run', '--stats',
                                helper.get_testfile('mixed_formats')])

        self.assertTrue('Execution time:' in helper.join(output))
        self.assertTrue('Counter:' in helper.join(output))


# --target
class TestTarget(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.tmp_album = helper.copy_to_tmp('files', 'album.mp3')
        with helper.Capturing():
            audiorename.execute([
                '--target',
                self.tmp_dir,
                '-f',
                'album',
                self.tmp_album
            ])

        self.tmp_compilation = helper.copy_to_tmp('files', 'compilation.mp3')
        with helper.Capturing():
            audiorename.execute([
                '--target',
                self.tmp_dir,
                '-c',
                'compilation',
                self.tmp_compilation
            ])

    def test_album(self):
        self.assertTrue(helper.is_file(self.tmp_dir + '/album.mp3'))

    def test_compilation(self):
        self.assertTrue(helper.is_file(self.tmp_dir + '/compilation.mp3'))

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)


# --verbose
class TestVerbose(unittest.TestCase):

    def test_verbose(self):
        tmp = helper.copy_to_tmp('files', 'album.mp3')

        target = tempfile.mkdtemp()

        with helper.Capturing() as output:
            audiorename.execute([
                '--copy',
                '--verbose',
                '--target',
                target,
                tmp
            ])

        # '[Copy:       ] /tmp/tmpisugl3hp/album.mp3'
        # '            -> /tmp/tmpcwqxsfgx/t/the album artist/the
        # album_2001/4-02_full.mp3']

        self.assertTrue(target in helper.join(output))

    def test_non_verbose(self):
        tmp = helper.copy_to_tmp('files', 'album.mp3')

        target = tempfile.mkdtemp()

        with helper.Capturing() as output:
            audiorename.execute([
                '--copy',
                '--target',
                target,
                tmp
            ])
        # '[Copy:       ] /tmp/tmpycwB06/album.mp3'
        # '            -> /t/the album artist/the album_2001/4-02_full.mp3'

        self.assertFalse(target in output[1])


if __name__ == '__main__':
    unittest.main()
