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
            h.cwd + h.path_album
        ))

    def test_compilation(self):
        self.assertFalse(os.path.isfile(self.tmp_compilation))
        self.assertTrue(h.is_file(
            h.cwd + h.path_compilation
        ))

    def tearDown(self):
        shutil.rmtree(h.cwd + '/_compilations/')
        shutil.rmtree(h.cwd + '/t/')


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
                h.cwd +
                h.path_album
            )
        )

    def test_compilation(self):
        self.assertTrue(os.path.isfile(self.tmp_compilation))
        self.assertTrue(
            os.path.isfile(
                h.cwd + h.path_compilation
            )
        )

    def tearDown(self):
        shutil.rmtree(h.cwd + '/_compilations/')
        shutil.rmtree(h.cwd + '/t/')


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
                h.cwd +
                h.path_album
            )
        )

    def test_compilation(self):
        self.assertTrue(h.is_file(self.tmp_compilation))
        self.assertFalse(
            os.path.isfile(
                h.cwd + h.path_compilation
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
            h.cwd + '/tmp/full - the artist.mp3'
        ))

    def test_compilation(self):
        self.assertTrue(os.path.isfile(
            h.cwd + '/tmp/comp_full - the artist.mp3'
        ))

    def tearDown(self):
        shutil.rmtree(h.cwd + '/tmp/')


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


if __name__ == '__main__':
    unittest.main()
