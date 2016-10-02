import unittest
import audiorename
import six
import os
import tempfile
import shutil
import sys
if six.PY2:
    from cStringIO import StringIO
else:
    from io import StringIO


default_album = '/t/the album artist/the album_2001/4-02_full.mp3'
default_compilation = '/_compilations/t/the album_2001/4-02_full.mp3'

cwd = os.getcwd()


def tmp_file(test_file):
    orig = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), test_file)
    tmp_dir = tempfile.mkdtemp()
    tmp = os.path.join(tmp_dir, test_file)
    shutil.copyfile(orig, tmp)
    return tmp


def is_file(path):
    """Check if file exists

    ":params list path: Path of the file as a list"
    """
    return os.path.isfile(path)

def has(list, search):
    return any(search in string for string in list)


class Capturing(list):
    def __init__(self, channel='out'):
        self.channel = channel

    def __enter__(self):
        if self.channel == 'out':
            self._pipe = sys.stdout
            sys.stdout = self._stringio = StringIO()
        elif self.channel == 'err':
            self._pipe = sys.stderr
            sys.stderr = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        if self.channel == 'out':
            sys.stdout = self._pipe
        elif self.channel == 'err':
            sys.stderr = self._pipe


class TestCommandlineInterface(unittest.TestCase):

    def test_help_short(self):
        with self.assertRaises(SystemExit) as cm:
            with Capturing():
                audiorename.execute(['-h'])
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '0')

    def test_help_long(self):
        with self.assertRaises(SystemExit) as cm:
            with Capturing():
                audiorename.execute(['--help'])
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '0')

    def test_without_arguments(self):
        with self.assertRaises(SystemExit) as cm:
            with Capturing('err'):
                audiorename.execute()
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '2')


class TestBasicRename(unittest.TestCase):

    def setUp(self):
        self.tmp_album = tmp_file('album.mp3')
        with Capturing():
            audiorename.execute([self.tmp_album])
        self.tmp_compilation = tmp_file('compilation.mp3')
        with Capturing():
            audiorename.execute([self.tmp_compilation])
        self.cwd = os.getcwd()

    def test_album(self):
        self.assertFalse(os.path.isfile(self.tmp_album))
        self.assertTrue(is_file(
            self.cwd + default_album
        ))

    def test_compilation(self):
        self.assertFalse(os.path.isfile(self.tmp_compilation))
        self.assertTrue(is_file(
            self.cwd + default_compilation
        ))

    def tearDown(self):
        shutil.rmtree(self.cwd + '/_compilations/')
        shutil.rmtree(self.cwd + '/t/')


class TestBasicCopy(unittest.TestCase):

    def setUp(self):
        self.tmp_album = tmp_file('album.mp3')
        with Capturing():
            audiorename.execute(['--copy', self.tmp_album])
        self.tmp_compilation = tmp_file('compilation.mp3')
        with Capturing():
            audiorename.execute(['--copy', self.tmp_compilation])
        self.cwd = os.getcwd()

    def test_album(self):
        self.assertTrue(is_file(self.tmp_album))
        self.assertTrue(
            os.path.isfile(
                self.cwd +
                default_album
            )
        )

    def test_compilation(self):
        self.assertTrue(os.path.isfile(self.tmp_compilation))
        self.assertTrue(
            os.path.isfile(
                self.cwd + default_compilation
            )
        )

    def tearDown(self):
        shutil.rmtree(self.cwd + '/_compilations/')
        shutil.rmtree(self.cwd + '/t/')


class TestDryRun(unittest.TestCase):

    def setUp(self):
        self.tmp_album = tmp_file('album.mp3')
        with Capturing() as self.output_album:
            audiorename.execute(['--dry-run', self.tmp_album])

        self.tmp_compilation = tmp_file('compilation.mp3')
        with Capturing() as self.output_compilation:
            audiorename.execute(['--dry-run', self.tmp_compilation])
        self.cwd = os.getcwd()

    def test_output_album(self):
        self.assertTrue(has(self.output_album, 'Dry run'))
        self.assertTrue(has(self.output_album, self.tmp_album))

    def test_output_compilation(self):
        self.assertTrue(has(self.output_compilation, 'Dry run'))
        self.assertTrue(
            has(self.output_compilation, self.tmp_compilation)
        )

    def test_album(self):
        self.assertTrue(is_file(self.tmp_album))
        self.assertFalse(
            os.path.isfile(
                self.cwd +
                '/t/the album artist/the album_2001/4-02_full.mp3'
            )
        )

    def test_compilation(self):
        self.assertTrue(is_file(self.tmp_compilation))
        self.assertFalse(
            os.path.isfile(
                self.cwd + '/_compilations/t/the album_2001/4-02_full.mp3'
            )
        )


class TestTarget(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.tmp_album = tmp_file('album.mp3')
        with Capturing():
            audiorename.execute([
                '--target-dir',
                self.tmp_dir,
                '-f',
                'album',
                self.tmp_album
            ])

        self.tmp_compilation = tmp_file('compilation.mp3')
        with Capturing():
            audiorename.execute([
                '--target-dir',
                self.tmp_dir,
                '-c',
                'compilation',
                self.tmp_compilation
            ])

    def test_album(self):
        self.assertTrue(is_file(self.tmp_dir + '/album.mp3'))

    def test_compilation(self):
        self.assertTrue(is_file(self.tmp_dir + '/compilation.mp3'))

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)


class TestSourceAsTarget(unittest.TestCase):

    def setUp(self):
        self.tmp_album = tmp_file('album.mp3')
        self.dir_album = os.path.dirname(self.tmp_album)
        with Capturing():
            audiorename.execute([
                '--source-as-target-dir',
                '-f',
                'a',
                self.tmp_album
            ])

        self.tmp_compilation = tmp_file('compilation.mp3')
        with Capturing():
            audiorename.execute([
                '--source-as-target-dir',
                '-c',
                'c',
                self.tmp_compilation
            ])

    def test_album(self):
        self.assertTrue(is_file(self.dir_album + '/a.mp3'))


class TestCustomFormats(unittest.TestCase):

    def setUp(self):
        with Capturing():
            audiorename.execute([
                '--format',
                'tmp/$title - $artist',
                tmp_file('album.mp3')
            ])
        with Capturing():
            audiorename.execute([
                '--compilation',
                'tmp/comp_$title - $artist',
                tmp_file('compilation.mp3')
            ])
        self.cwd = os.getcwd()

    def test_format(self):
        self.assertTrue(os.path.isfile(
            self.cwd + '/tmp/full - the artist.mp3'
        ))

    def test_compilation(self):
        self.assertTrue(os.path.isfile(
            self.cwd + '/tmp/comp_full - the artist.mp3'
        ))

    def tearDown(self):
        shutil.rmtree(self.cwd + '/tmp/')


class TestSkipIfEmpty(unittest.TestCase):

    def setUp(self):
        with Capturing() as self.album:
            audiorename.execute([
                '--skip-if-empty',
                'lol',
                tmp_file('album.mp3')
            ])
        with Capturing() as self.compilation:
            audiorename.execute([
                '--skip-if-empty',
                'album',
                '-d',
                '-c',
                '/tmp/c',
                tmp_file('compilation.mp3')
            ])

    def test_album(self):
        self.assertTrue(has(self.album, 'no field'))

    def test_compilation(self):
        self.assertTrue(has(self.compilation, 'Dry run'))


if __name__ == '__main__':
    unittest.main()
