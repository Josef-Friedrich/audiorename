import unittest
import re
import audiorename
import six
import os
import shutil
import tempfile
import sys
import helper as h
if six.PY2:
    from cStringIO import StringIO
else:
    from io import StringIO


path_album = '/t/the album artist/the album_2001/4-02_full.mp3'
path_compilation = '/_compilations/t/the album_2001/4-02_full.mp3'

test_path = os.path.dirname(os.path.abspath(__file__))

test_files = os.path.join(test_path, 'files')
cwd = os.getcwd()


class TestCommandlineInterface(unittest.TestCase):

    def test_help_short(self):
        with self.assertRaises(SystemExit) as cm:
            with h.Capturing():
                audiorename.execute(['-h'])
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '0')

    def test_help_long(self):
        with self.assertRaises(SystemExit) as cm:
            with h.Capturing():
                audiorename.execute(['--help'])
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '0')

    def test_without_arguments(self):
        with self.assertRaises(SystemExit) as cm:
            with h.Capturing('err'):
                audiorename.execute()
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '2')


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
            cwd + path_album
        ))

    def test_compilation(self):
        self.assertFalse(os.path.isfile(self.tmp_compilation))
        self.assertTrue(h.is_file(
            cwd + path_compilation
        ))

    def tearDown(self):
        shutil.rmtree(cwd + '/_compilations/')
        shutil.rmtree(cwd + '/t/')


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
                cwd +
                path_album
            )
        )

    def test_compilation(self):
        self.assertTrue(os.path.isfile(self.tmp_compilation))
        self.assertTrue(
            os.path.isfile(
                cwd + path_compilation
            )
        )

    def tearDown(self):
        shutil.rmtree(cwd + '/_compilations/')
        shutil.rmtree(cwd + '/t/')


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
                cwd +
                path_album
            )
        )

    def test_compilation(self):
        self.assertTrue(h.is_file(self.tmp_compilation))
        self.assertFalse(
            os.path.isfile(
                cwd + path_compilation
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
            cwd + '/tmp/full - the artist.mp3'
        ))

    def test_compilation(self):
        self.assertTrue(os.path.isfile(
            cwd + '/tmp/comp_full - the artist.mp3'
        ))

    def tearDown(self):
        shutil.rmtree(cwd + '/tmp/')


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


class TestVersion(unittest.TestCase):

    def test_version(self):
        with self.assertRaises(SystemExit):
            if six.PY2:
                with h.Capturing('err') as output:
                    audiorename.execute(['--version'])
            else:
                with h.Capturing() as output:
                    audiorename.execute(['--version'])

        result = re.search('[^ ]* [^ ]*', output[0])
        self.assertTrue(result)


class TestBatch(unittest.TestCase):

    def setUp(self):
        self.singles = h.gen_file_list(
            ['album', 'compilation'],
            os.path.join(test_files),
        )

        self.album_broken = h.gen_file_list(
            ['01', '03', '05', '07', '09', '11'],
            os.path.join(test_files, 'album_broken'),
        )

        self.album_broken_all = h.gen_file_list(
            ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11'],
            os.path.join(test_files, 'album_broken'),
        )

        self.album_complete = h.gen_file_list(
            ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11'],
            os.path.join(test_files, 'album_complete'),
        )

        self.album_incomplete = h.gen_file_list(
            ['01', '02', '04', '05', '06', '07', '09', '10', '11'],
            os.path.join(test_files, 'album_incomplete'),
        )

        self.album_small = h.gen_file_list(
            ['01', '02', '03', '04', '05'],
            os.path.join(test_files, 'album_small'),
        )

        self.all = self.singles + \
            self.album_broken_all +  \
            self.album_complete + \
            self.album_incomplete + \
            self.album_small

    def test_single(self):
        single = os.path.join(test_files, 'album.mp3')
        with h.Capturing() as output:
            audiorename.execute(['--unittest', single])
        self.assertEqual([single], output)

    def test_folder_complete(self):
        with h.Capturing() as output:
            audiorename.execute(['--unittest', test_files])
        self.assertEqual(self.all, output)

    def test_folder_sub(self):
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                os.path.join(test_files, 'album_complete')
            ])
        self.assertEqual(self.album_complete, output)

    def test_filter_album_min(self):
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--filter-album-min',
                '7',
                test_files
            ])
        self.assertEqual(self.album_complete + self.album_incomplete, output)

    def test_filter_album_min_no_match(self):
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--filter-album-min',
                '23',
                test_files
            ])
        self.assertEqual([], output)

    def test_filter_album_complete(self):
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--filter-album-complete',
                test_files
            ])
        self.assertEqual(
            self.singles +
            self.album_complete +
            self.album_small,
            output
        )

    def test_filter_all(self):
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--filter-album-min',
                '7',
                '--filter-album-complete',
                test_files
            ])
        self.assertEqual(self.album_complete, output)


class TestExtension(unittest.TestCase):

    def setUp(self):
        self.test_files = os.path.join(test_path, 'mixed_formats')

    def test_default(self):
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                self.test_files
            ])
        self.assertEqual(
            output,
            h.gen_file_list(
                ['01.flac', '02.m4a', '03.mp3'],
                self.test_files,
                extension=False
            )
        )

    def test_one(self):
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--extension',
                'mp3,flac',
                self.test_files
            ])
        self.assertEqual(
            output,
            h.gen_file_list(
                ['01.flac', '03.mp3'],
                self.test_files,
                extension=False
            )
        )

    def test_two(self):
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--extension',
                'mp3',
                self.test_files
            ])
        self.assertEqual(
            output,
            h.gen_file_list(['03.mp3'], self.test_files, extension=False)
        )


class TestHelp(unittest.TestCase):

    def setUp(self):
        with self.assertRaises(SystemExit):
            with h.Capturing() as output:
                audiorename.execute(['--help'])
        self.output = '\n'.join(output)

    def test_tmep(self):
        self.assertTrue('%title{text}' in self.output)

    def test_phrydy(self):
        self.assertTrue('mb_releasegroupid' in self.output)


class TestSkip(unittest.TestCase):

    def setUp(self):
        self.file = os.path.join(test_path, 'broken', 'binary.mp3')
        with h.Capturing() as output:
            audiorename.execute([
                '-d',
                self.file
            ])
        self.output = output

    def test_message(self):
        self.assertTrue('!!! SKIPPED [broken file] !!!' in self.output[0])

    def test_file_in_message(self):
        self.assertTrue('!!! SKIPPED [broken file] !!!' in self.output[0])
        self.assertTrue(self.file in self.output[0])

    def test_continuation(self):
        path = os.path.join(test_path, 'broken')
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                path
            ])

        self.assertTrue(output[1])


if __name__ == '__main__':
    unittest.main()
