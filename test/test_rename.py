# -*- coding: utf-8 -*-

"""Test the submodule “rename.py”."""

import unittest
import audiorename
from audiorename import rename
import os
import shutil
import tempfile
import helper


class TestDetermineRenameActions(unittest.TestCase):

    @staticmethod
    def to_tmp(audio_file):
        return helper.copy_to_tmp(['quality', audio_file])

    @staticmethod
    def determine(target, source, delete, copy):
        return rename.determine_rename_actions(target, source, delete, copy)

    def test_delete_source(self):
        target = self.to_tmp('flac.flac')
        source = self.to_tmp('flac.flac')
        self.determine(target, source, delete=True, copy=False)

    def test_move_source(self):
        pass

    def test_rename_source(self):
        pass

    def test_delete_target(self):
        pass


class TestCheckTarget(unittest.TestCase):

    def setUp(self):
        self.extensions = ['flac', 'mp3', 'm4a']
        self.target = helper.path(['quality', 'flac.flac'])

    def test_same(self):
        result = rename.check_target(self.target, self.extensions)
        self.assertEqual(self.target, result)

    def test_different(self):
        target = self.target.replace('.flac', '.mp3')
        result = rename.check_target(target, self.extensions)
        self.assertEqual(self.target, result)


class TestBestFormat(unittest.TestCase):
    """
    Bitrates

    * flac.flac 301213
    * m4a_100.m4a 198551
    * m4a_250.m4a 235243
    * mp3_128.mp3 191995
    * mp3_144.mp3 86884
    * mp3_320.mp3 319999
    """

    @staticmethod
    def source_target(source, target):
        return rename.best_format(
            helper.get_meta(['quality', source]),
            helper.get_meta(['quality', target]),
        )

    def test_same_quality(self):
        result = self.source_target('flac.flac', 'flac.flac')
        self.assertEqual(result, 'target')

    def test_target_better(self):
        result = self.source_target('mp3_128.mp3', 'flac.flac')
        self.assertEqual(result, 'target')

    def test_source_better(self):
        result = self.source_target('flac.flac', 'mp3_128.mp3')
        self.assertEqual(result, 'source')

    def test_mp3_source_better(self):
        result = self.source_target('mp3_320.mp3', 'mp3_128.mp3')
        self.assertEqual(result, 'source')

    def test_mp3_target_better_2(self):
        result = self.source_target('mp3_144.mp3', 'mp3_320.mp3')
        self.assertEqual(result, 'target')

    def test_mp3_source_better_2(self):
        result = self.source_target('mp3_320.mp3', 'mp3_144.mp3')
        self.assertEqual(result, 'source')

    def test_mp3_target_better(self):
        result = self.source_target('m4a_100.m4a', 'm4a_250.m4a')
        self.assertEqual(result, 'target')

    def test_m4a_target_better(self):
        result = self.source_target('m4a_250.m4a', 'm4a_100.m4a')
        self.assertEqual(result, 'source')


class TestBasicRename(unittest.TestCase):

    def setUp(self):
        self.tmp_album = helper.copy_to_tmp(['files', 'album.mp3'])
        with helper.Capturing():
            audiorename.execute([self.tmp_album])
        self.tmp_compilation = helper.copy_to_tmp(['files', 'compilation.mp3'])
        with helper.Capturing():
            audiorename.execute([self.tmp_compilation])

    def test_album(self):
        self.assertFalse(os.path.isfile(self.tmp_album))
        self.assertTrue(helper.is_file(
            helper.dir_cwd + helper.path_album
        ))

    def test_compilation(self):
        self.assertFalse(os.path.isfile(self.tmp_compilation))
        self.assertTrue(helper.is_file(
            helper.dir_cwd + helper.path_compilation
        ))

    def tearDown(self):
        shutil.rmtree(helper.dir_cwd + '/_compilations/')
        shutil.rmtree(helper.dir_cwd + '/t/')


class TestOverwriteProtection(unittest.TestCase):

    def setUp(self):
        self.tmp_album = helper.copy_to_tmp(['files', 'album.mp3'])
        with helper.Capturing():
            audiorename.execute(['--copy', self.tmp_album])
        self.tmp_compilation = helper.copy_to_tmp(['files', 'compilation.mp3'])
        with helper.Capturing():
            audiorename.execute(['--copy', self.tmp_compilation])

    def test_album(self):
        with helper.Capturing() as output:
            audiorename.execute([self.tmp_album])
        self.assertTrue('Exists' in output[0])

    def test_compilation(self):
        with helper.Capturing() as output:
            audiorename.execute([self.tmp_compilation])
        self.assertTrue('Exists' in output[0])

    def test_album_already_renamed(self):
        with helper.Capturing():
            audiorename.execute([self.tmp_album])
        with helper.Capturing() as output:
            audiorename.execute([helper.dir_cwd + helper.path_album])

        self.assertTrue('Renamed' in output[0])

    def test_compilation_already_renamed(self):
        with helper.Capturing():
            audiorename.execute([self.tmp_compilation])
        with helper.Capturing() as output:
            audiorename.execute([helper.dir_cwd + helper.path_compilation])

        self.assertTrue('Renamed' in output[0])

    def tearDown(self):
        shutil.rmtree(helper.dir_cwd + '/_compilations/')
        shutil.rmtree(helper.dir_cwd + '/t/')


class TestMessageFile(unittest.TestCase):

    def setUp(self):
        from audiorename.rename import MessageFile
        self.MessageFile = MessageFile
        self.job = helper.get_job(source='/tmp', source_as_target=True)

    def message(self, **arguments):
        job = helper.get_job(**arguments)
        return self.MessageFile(job, 'source.mp3', 'target.mp3')

    def test_without_target(self):
        message = self.MessageFile(self.job, 'lol.mp3')
        with helper.Capturing() as output:
            message.process(u'lol')
        self.assertTrue('[lol:        ]' in output[0])

    def test_with_target(self):
        message = self.MessageFile(self.job, 'source.mp3', 'target.mp3')
        with helper.Capturing() as output:
            message.process(u'lol')
        self.assertTrue('target.mp3' in output[1])

    def test_one_line(self):
        message = self.message(source='/tmp', one_line=True)
        with helper.Capturing() as output:
            message.process(u'lol')
        self.assertTrue('source.mp3' in output[0])
        self.assertTrue('target.mp3' in output[0])

    def test_two_lines(self):
        message = self.message(source='/tmp', one_line=False)
        with helper.Capturing() as output:
            message.process(u'lol')
        self.assertTrue('source.mp3' in output[0])
        self.assertTrue('target.mp3' in output[1])

    def test_no_color(self):
        message = self.message(source='/tmp', color=False)
        with helper.Capturing() as output:
            message.process(u'lol')
        self.assertTrue('] source.mp3' in output[0])

    @unittest.skip('not working with tox')
    def test_color(self):
        message = self.message(source='/tmp', color=True)
        with helper.Capturing() as output:
            message.process(u'lol')
        self.assertTrue(u']\x1b[0;0m source.mp3' in output[0])


class TestUnicodeUnittest(unittest.TestCase):

    def setUp(self):
        self.uni = os.path.join(helper.dir_test, 'äöü', 'ÅåÆæØø.mp3')
        self.renamed = os.path.join('/►', '►', '_',
                                    '_ÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž.mp3')
        self.indent = '            -> '

    def test_dry_run(self):
        with helper.Capturing() as output:
            audiorename.execute(['--dry-run', self.uni])
        self.assertTrue(self.renamed in output[1])

    def test_rename(self):
        tmp_dir = tempfile.mkdtemp()
        tmp = os.path.join(tmp_dir, 'äöü.mp3')
        shutil.copyfile(self.uni, tmp)
        with helper.Capturing() as output:
            audiorename.execute(['--target', tmp_dir, tmp])
        self.assertTrue(self.renamed in output[1])

    def test_copy(self):
        with helper.Capturing() as output:
            audiorename.execute(['--copy', self.uni])
        self.assertTrue(self.renamed in output[1])
        shutil.rmtree(helper.dir_cwd + '/►/')


if __name__ == '__main__':
    unittest.main()
