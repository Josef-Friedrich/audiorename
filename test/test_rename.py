# -*- coding: utf-8 -*-

import unittest
import audiorename
import os
import shutil
import tempfile
import helper as h


class TestBasicRename(unittest.TestCase):

    def setUp(self):
        self.tmp_album = h.tmp_file('album.mp3')
        with h.Capturing():
            audiorename.execute([self.tmp_album])
        self.tmp_compilation = h.tmp_file('compilation.mp3')
        with h.Capturing():
            audiorename.execute([self.tmp_compilation])

    def test_album(self):
        self.assertFalse(os.path.isfile(self.tmp_album))
        self.assertTrue(h.is_file(
            h.dir_cwd + h.path_album
        ))

    def test_compilation(self):
        self.assertFalse(os.path.isfile(self.tmp_compilation))
        self.assertTrue(h.is_file(
            h.dir_cwd + h.path_compilation
        ))

    def tearDown(self):
        shutil.rmtree(h.dir_cwd + '/_compilations/')
        shutil.rmtree(h.dir_cwd + '/t/')


class TestBasicCopy(unittest.TestCase):

    def setUp(self):
        self.tmp_album = h.tmp_file('album.mp3')
        with h.Capturing():
            audiorename.execute(['--copy', self.tmp_album])
        self.tmp_compilation = h.tmp_file('compilation.mp3')
        with h.Capturing():
            audiorename.execute(['--copy', self.tmp_compilation])

    def test_album(self):
        self.assertTrue(h.is_file(self.tmp_album))
        self.assertTrue(
            os.path.isfile(
                h.dir_cwd +
                h.path_album
            )
        )

    def test_compilation(self):
        self.assertTrue(os.path.isfile(self.tmp_compilation))
        self.assertTrue(
            os.path.isfile(
                h.dir_cwd + h.path_compilation
            )
        )

    def tearDown(self):
        shutil.rmtree(h.dir_cwd + '/_compilations/')
        shutil.rmtree(h.dir_cwd + '/t/')


class TestOverwriteProtection(unittest.TestCase):

    def setUp(self):
        self.tmp_album = h.tmp_file('album.mp3')
        with h.Capturing():
            audiorename.execute(['--copy', self.tmp_album])
        self.tmp_compilation = h.tmp_file('compilation.mp3')
        with h.Capturing():
            audiorename.execute(['--copy', self.tmp_compilation])

    def test_album(self):
        with h.Capturing() as output:
            audiorename.execute([self.tmp_album])
        self.assertTrue('File exits' in output[0])

    def test_compilation(self):
        with h.Capturing() as output:
            audiorename.execute([self.tmp_compilation])
        self.assertTrue('File exits' in output[0])

    def test_album_already_renamed(self):
        with h.Capturing():
            audiorename.execute([self.tmp_album])
        with h.Capturing() as output:
            audiorename.execute([h.dir_cwd + h.path_album])

        self.assertTrue('Already renamed' in output[0])

    def test_compilation_already_renamed(self):
        with h.Capturing():
            audiorename.execute([self.tmp_compilation])
        with h.Capturing() as output:
            audiorename.execute([h.dir_cwd + h.path_compilation])

        self.assertTrue('Already renamed' in output[0])

    def tearDown(self):
        shutil.rmtree(h.dir_cwd + '/_compilations/')
        shutil.rmtree(h.dir_cwd + '/t/')


class TestDryRun(unittest.TestCase):

    def setUp(self):
        self.tmp_album = h.tmp_file('album.mp3')
        with h.Capturing() as self.output_album:
            audiorename.execute(['--dry-run', self.tmp_album])

        self.tmp_compilation = h.tmp_file('compilation.mp3')
        with h.Capturing() as self.output_compilation:
            audiorename.execute(['--dry-run', self.tmp_compilation])

    def test_output_album(self):
        self.assertTrue(h.has(self.output_album, 'Dry run'))
        self.assertTrue(h.has(self.output_album, self.tmp_album))

    def test_output_compilation(self):
        self.assertTrue(h.has(self.output_compilation, 'Dry run'))
        self.assertTrue(
            h.has(self.output_compilation, self.tmp_compilation)
        )

    def test_album(self):
        self.assertTrue(h.is_file(self.tmp_album))
        self.assertFalse(
            os.path.isfile(
                h.dir_cwd +
                h.path_album
            )
        )

    def test_compilation(self):
        self.assertTrue(h.is_file(self.tmp_compilation))
        self.assertFalse(
            os.path.isfile(
                h.dir_cwd + h.path_compilation
            )
        )


class TestTarget(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.tmp_album = h.tmp_file('album.mp3')
        with h.Capturing():
            audiorename.execute([
                '--target-dir',
                self.tmp_dir,
                '-f',
                'album',
                self.tmp_album
            ])

        self.tmp_compilation = h.tmp_file('compilation.mp3')
        with h.Capturing():
            audiorename.execute([
                '--target-dir',
                self.tmp_dir,
                '-c',
                'compilation',
                self.tmp_compilation
            ])

    def test_album(self):
        self.assertTrue(h.is_file(self.tmp_dir + '/album.mp3'))

    def test_compilation(self):
        self.assertTrue(h.is_file(self.tmp_dir + '/compilation.mp3'))

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)


class TestSourceAsTarget(unittest.TestCase):

    def setUp(self):
        self.tmp_album = h.tmp_file('album.mp3')
        self.dir_album = os.path.dirname(self.tmp_album)
        with h.Capturing():
            audiorename.execute([
                '--source-as-target-dir',
                '-f',
                'a',
                self.tmp_album
            ])

        self.tmp_compilation = h.tmp_file('compilation.mp3')
        with h.Capturing():
            audiorename.execute([
                '--source-as-target-dir',
                '-c',
                'c',
                self.tmp_compilation
            ])

    def test_album(self):
        self.assertTrue(h.is_file(self.dir_album + '/a.mp3'))


class TestCustomFormats(unittest.TestCase):

    def setUp(self):
        with h.Capturing():
            audiorename.execute([
                '--format',
                'tmp/$title - $artist',
                h.tmp_file('album.mp3')
            ])
        with h.Capturing():
            audiorename.execute([
                '--compilation',
                'tmp/comp_$title - $artist',
                h.tmp_file('compilation.mp3')
            ])

    def test_format(self):
        self.assertTrue(os.path.isfile(
            h.dir_cwd + '/tmp/full - the artist.mp3'
        ))

    def test_compilation(self):
        self.assertTrue(os.path.isfile(
            h.dir_cwd + '/tmp/comp_full - the artist.mp3'
        ))

    def tearDown(self):
        shutil.rmtree(h.dir_cwd + '/tmp/')


class TestSkipIfEmpty(unittest.TestCase):

    def setUp(self):
        with h.Capturing() as self.album:
            audiorename.execute([
                '--skip-if-empty',
                'lol',
                h.tmp_file('album.mp3')
            ])
        with h.Capturing() as self.compilation:
            audiorename.execute([
                '--skip-if-empty',
                'album',
                '-d',
                '-c',
                '/tmp/c',
                h.tmp_file('compilation.mp3')
            ])

    def test_album(self):
        self.assertTrue(h.has(self.album, 'No field'))

    def test_compilation(self):
        self.assertTrue(h.has(self.compilation, 'Dry run'))


class TestClassical(unittest.TestCase):

    def assertDryRun(self, folder, track, test):
        self.assertEqual(h.dry_run([
            '--classical',
            os.path.join(h.dir_test, 'classical', folder, track)
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
    mp1 = u'[OrpChaOrc-Jolley]'
    mp2 = u'[OrpChaOrc-Purvis]'
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
    l = 'Swan-Lake-op-20_[Svetlanov-StaAcaSym]/'

    def test_tschaikowski_01(self):
        self.assertDryRun(
            'Tschaikowski_Swan-Lake', '1-01.mp3',
            self.t + self.l +
            '1-01_Introduction-Moderato-assai-Allegro-ma-non-troppo-' +
            'Tempo-I_3f6fc6b3.mp3'
        )

    def test_tschaikowski_02(self):
        self.assertDryRun(
            'Tschaikowski_Swan-Lake', '1-02.mp3',
            self.t + self.l + '1-02_Act-I-no-1-Scene-Allegro-giusto_29413f6c.mp3'
        )

    def test_tschaikowski_03(self):
        self.assertDryRun(
            'Tschaikowski_Swan-Lake', '1-03.mp3',
            self.t + self.l + '1-03_Act-I-no-2-Valse-Tempo-di-valse_5303b318.mp3'
        )

    def test_tschaikowski_04(self):
        self.assertDryRun(
            'Tschaikowski_Swan-Lake', '1-04.mp3',
            self.t + self.l + '1-04_Act-I-no-3-Scene-Allegro-moderato_4d5781a4.mp3'
        )

    wr = '/w/Wagner_Richard/'
    mn = 'Die-Meistersinger-von-Nuernberg_[Karajan-StaDre-StaDre]/'

    def test_wagner_01(self):
        self.assertDryRun(
            'Wagner_Meistersinger', '01.mp3',
            self.wr + self.mn + '1-01_Vorspiel_313c5f00.mp3'
        )

    def test_wagner_02(self):
        self.assertDryRun(
            'Wagner_Meistersinger', '02.mp3',
            self.wr + self.mn +
            '1-02_Akt-I-Szene-I-Da-zu-dir-der-Heiland-kam-Gemeinde_cdd9f298.mp3'
        )

    def test_wagner_03(self):
        self.assertDryRun(
            'Wagner_Meistersinger', '03.mp3',
            self.wr + self.mn +
            '1-03_Akt-I-Szene-I-Verweilt-Ein-Wort-Walther-Eva-Magdalene_adab7b8c.mp3'
        )

    def test_wagner_04(self):
        self.assertDryRun(
            'Wagner_Meistersinger', '04.mp3',
            self.wr + self.mn +
            '1-04_Akt-I-Szene-I-Da-bin-ich-David-Magdalene-Walther-Eva_f3f0231f.mp3'
        )


class TestMessageUnittest(unittest.TestCase):

    def setUp(self):
        from audiorename.rename import Rename
        self.r = Rename()

    def test_message(self):
        out = self.r.processMessage(action=u'lol', old_path=u'old',
                                    new_path=u'new', output=u'return')
        self.assertEqual(out, u'[lol:        ] old\n            -> new')


if __name__ == '__main__':
    unittest.main()
