# -*- coding: utf-8 -*-

"""Test the submodule “rename.py”."""

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
        self.assertTrue('Exits' in output[0])

    def test_compilation(self):
        with h.Capturing() as output:
            audiorename.execute([self.tmp_compilation])
        self.assertTrue('Exits' in output[0])

    def test_album_already_renamed(self):
        with h.Capturing():
            audiorename.execute([self.tmp_album])
        with h.Capturing() as output:
            audiorename.execute([h.dir_cwd + h.path_album])

        self.assertTrue('Renamed' in output[0])

    def test_compilation_already_renamed(self):
        with h.Capturing():
            audiorename.execute([self.tmp_compilation])
        with h.Capturing() as output:
            audiorename.execute([h.dir_cwd + h.path_compilation])

        self.assertTrue('Renamed' in output[0])

    def tearDown(self):
        shutil.rmtree(h.dir_cwd + '/_compilations/')
        shutil.rmtree(h.dir_cwd + '/t/')


class TestMessageUnittest(unittest.TestCase):

    def setUp(self):
        from audiorename.rename import Rename
        from audiorename.args import ArgsDefault
        args_default = ArgsDefault()
        self.r = Rename(False, args_default)

    def test_message(self):
        out = self.r.processMessage(action=u'lol', old_path=u'old',
                                    new_path=u'new', output=u'return')
        self.assertTrue('[lol:        ]' in out)
        self.assertTrue('new' in out)


class TestUnicodeUnittest(unittest.TestCase):

    def setUp(self):
        self.uni = os.path.join(h.dir_test, 'äöü', 'ÅåÆæØø.mp3')
        self.renamed = os.path.join('/►', '►', '_',
                                    '_ÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž.mp3')
        self.indent = '            -> '

    def test_dry_run(self):
        with h.Capturing() as output:
            audiorename.execute([
                '--dry-run',
                self.uni
            ])
        self.assertEqual(output[1],
                         self.indent + self.renamed)

    def test_rename(self):
        tmp_dir = tempfile.mkdtemp()
        tmp = os.path.join(tmp_dir, 'äöü.mp3')
        shutil.copyfile(self.uni, tmp)
        with h.Capturing() as output:
            audiorename.execute(['--target-dir', tmp_dir, tmp])

        self.assertEqual(output[1],
                         self.indent + self.renamed)

    def test_copy(self):
        with h.Capturing() as output:
            audiorename.execute(['--copy', self.uni])

        self.assertEqual(output[1],
                         self.indent + self.renamed)
        shutil.rmtree(h.dir_cwd + '/►/')


if __name__ == '__main__':
    unittest.main()
