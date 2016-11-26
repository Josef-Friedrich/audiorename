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
        self.assertTrue(h.has(self.album, 'no field'))

    def test_compilation(self):
        self.assertTrue(h.has(self.compilation, 'Dry run'))


class TestClassical(unittest.TestCase):

    def assertDryRun(self, folder, track, test):
        self.assertEqual(h.dry_run([
            '--classical',
            os.path.join(h.dir_test, 'classical', folder, track)
        ]), test)

    m = '/m/Mozart_Wolfgang-Amadeus/'
    h1 = 'Concerto-for-French-Horn-no-1-in-D-major-K-386b'
    h2 = 'Concerto-for-Horn-no-2-in-E-flat-major-K-417'

    def test_mozart_01(self):
        self.assertDryRun(
            'Mozart_Wolfgang-Amadeus__4-Hornkonzerte', '01.mp3',
            self.m + self.h1 + '-KV-412/I-Allegro.mp3'
        )

    def test_mozart_02(self):
        self.assertDryRun(
            'Mozart_Wolfgang-Amadeus__4-Hornkonzerte', '02.mp3',
            self.m + self.h1 +
            '-KV-514-Suessmayr-completion/II-Rondo-Allegro.mp3'
        )

    def test_mozart_03(self):
        self.assertDryRun(
            'Mozart_Wolfgang-Amadeus__4-Hornkonzerte', '03.mp3',
            self.m + self.h2 + '/I-Allegro.mp3'
        )

    def test_mozart_04(self):
        self.assertDryRun(
            'Mozart_Wolfgang-Amadeus__4-Hornkonzerte', '04.mp3',
            self.m + self.h2 + '/II-Andante.mp3'
        )

    s = '/s/Schubert_Franz/'
    w = 'Die-Winterreise-op-89-D-911/'

    def test_schubert_01(self):
        self.assertDryRun(
            'Schubert_Franz__Winterreise-D-911', '01.mp3',
            self.s + self.w + 'Gute-Nacht.mp3'
        )

    def test_schubert_02(self):
        self.assertDryRun(
            'Schubert_Franz__Winterreise-D-911', '02.mp3',
            self.s + self.w + 'Die-Wetterfahne.mp3'
        )

    def test_schubert_03(self):
        self.assertDryRun(
            'Schubert_Franz__Winterreise-D-911', '03.mp3',
            self.s + self.w + 'Gefrorne-Traenen.mp3'
        )

    def test_schubert_04(self):
        self.assertDryRun(
            'Schubert_Franz__Winterreise-D-911', '04.mp3',
            self.s + self.w + 'Erstarrung.mp3'
        )

    t = '/t/Tchaikovsky_Pyotr-Ilyich/'
    l = 'Swan-Lake-op-20/'

    def test_tschaikowski_01(self):
        self.assertDryRun(
            'Tschaikowski__Swan-Lake-op-20', '1-01.mp3',
            self.t + self.l + 'Introduction-Moderato-assai.mp3'
        )

    def test_tschaikowski_02(self):
        self.assertDryRun(
            'Tschaikowski__Swan-Lake-op-20', '1-02.mp3',
            self.t + self.l + 'Act-I-no-1-Scene-Allegro.mp3'
        )

    def test_tschaikowski_03(self):
        self.assertDryRun(
            'Tschaikowski__Swan-Lake-op-20', '1-03.mp3',
            self.t + self.l + 'Act-I-no-2-Valse-Tempo-di.mp3'
        )

    def test_tschaikowski_04(self):
        self.assertDryRun(
            'Tschaikowski__Swan-Lake-op-20', '1-04.mp3',
            self.t + self.l + 'Act-I-no-3-Scene-Allegro.mp3'
        )


if __name__ == '__main__':
    unittest.main()
