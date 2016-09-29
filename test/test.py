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


def tmp_file(test_file):
    orig = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), test_file)
    tmp_dir = tempfile.mkdtemp()
    tmp = os.path.join(tmp_dir, test_file)
    shutil.copyfile(orig, tmp)
    return tmp


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
        audiorename.execute([self.tmp_album])
        self.tmp_compilation = tmp_file('compilation.mp3')
        audiorename.execute([self.tmp_compilation])
        self.cwd = os.getcwd()

    def test_rename_album(self):
        self.assertFalse(os.path.isfile(self.tmp_album))
        self.assertTrue(os.path.isfile(self.cwd + '/t/the album artist/the album_2001/4-02_full.mp3'))

    def test_rename_compilation(self):
        self.assertFalse(os.path.isfile(self.tmp_compilation))
        self.assertTrue(os.path.isfile(self.cwd + '/_compilations/t/the album_2001/4-02_full.mp3'))


class TestBasicCopy(unittest.TestCase):

    def setUp(self):
        self.tmp_album = tmp_file('album.mp3')
        audiorename.execute(['--copy', self.tmp_album])
        self.tmp_compilation = tmp_file('compilation.mp3')
        audiorename.execute(['--copy', self.tmp_compilation])
        self.cwd = os.getcwd()

    def test_rename_album(self):
        self.assertTrue(os.path.isfile(self.tmp_album))
        self.assertTrue(os.path.isfile(self.cwd + '/t/the album artist/the album_2001/4-02_full.mp3'))

    def test_rename_compilation(self):
        self.assertTrue(os.path.isfile(self.tmp_compilation))
        self.assertTrue(os.path.isfile(self.cwd + '/_compilations/t/the album_2001/4-02_full.mp3'))


class TestCustomFormats(unittest.TestCase):

    def setUp(self):
        audiorename.execute(['--format', 'tmp/$title - $artist', tmp_file('album.mp3')])
        audiorename.execute(['--compilation', 'tmp/comp_$title - $artist', tmp_file('compilation.mp3')])
        self.cwd = os.getcwd()

    def test_format(self):
        self.assertTrue(os.path.isfile(self.cwd + '/tmp/full - the artist.mp3'))

    def test_compilation(self):
        self.assertTrue(os.path.isfile(self.cwd + '/tmp/comp_full - the artist.mp3'))


if __name__ == '__main__':
    unittest.main()
