"""Test the submodule “rename.py”."""

import unittest
import audiorename
from audiorename import audiofile
from audiorename.meta import Meta
import os
import shutil
import tempfile
import helper


class TestClassAction(unittest.TestCase):

    def setUp(self):
        self.action = audiofile.Action(helper.get_job())

    def test_method_delete(self):
        tmp = helper.get_tmp_file_object('files', 'album.mp3')
        self.assertTrue(os.path.exists(tmp.abspath))
        with helper.Capturing() as output:
            self.action.delete(tmp)
        self.assertFalse(os.path.exists(tmp.abspath))
        self.assertTrue('Delete' in helper.join(output))

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_method_metadata_enrich(self):
        tmp = helper.get_tmp_file_object('classical', 'without_work.mp3')
        if not tmp.meta:
            self.fail('The audio file needs a meta property.')
        self.assertEqual(tmp.meta.mb_workid, None)
        with helper.Capturing():
            self.action.metadata(tmp, enrich=True)

        meta = Meta(tmp.abspath)
        self.assertEqual(meta.mb_workid,
                         '6b198406-4fbf-3d61-82db-0b7ef195a7fe')

    def test_method_metadata_remap_classical(self):
        tmp = helper.get_tmp_file_object('classical', 'Schubert_Winterreise',
                                         '01.mp3')

        self.assertEqual(tmp.meta.album, 'Winterreise')
        with helper.Capturing():
            self.action.metadata(tmp, remap=True)

        meta = Meta(tmp.abspath)
        self.assertEqual(meta.album,
                         'Die Winterreise, op. 89, D. 911 '
                         '(Fischer-Dieskau, Moore)')


class TestClassAudioFile(unittest.TestCase):

    def test_existing(self):
        abspath = helper.get_testfile('files', 'album.mp3')
        prefix = helper.dir_cwd
        result = audiofile.AudioFile(abspath, job=helper.get_job(),
                                     prefix=prefix)
        self.assertEqual(result.abspath, abspath)
        self.assertEqual(result.type, 'source')
        self.assertEqual(result.exists, True)
        self.assertEqual(result.extension, 'mp3')
        self.assertEqual(result.meta.path, abspath)
        self.assertEqual(result.short, '[…]test/files/files/album.mp3')
        self.assertEqual(result.prefix, prefix + os.path.sep)


class TestClassMbTrackListing(unittest.TestCase):

    def setUp(self):
        self.mb = audiofile.MBTrackListing()

    def listing(self, album, title, length=123):
        return self.mb.format_audiofile(album, title, length)

    def test_one_call(self):
        result = self.listing('album', 'title')
        self.assertEqual(result, '1. album: title (2:03)')

    def test_two_calls(self):
        self.listing('album', 'title')
        result = self.listing('album', 'title')
        self.assertEqual(result, '2. album: title (2:03)')

    def test_opus(self):
        result = self.listing('album Op.', 'title')
        self.assertEqual(result, '1. album op.: title (2:03)')

    def test_dash(self):
        result = self.listing('album - act', 'title')
        self.assertEqual(result, '1. album act: title (2:03)')


class TestFunctionGetTarget(unittest.TestCase):

    def setUp(self):
        self.extensions = ['flac', 'mp3', 'm4a']
        self.target = helper.get_testfile('quality', 'flac.flac')

    def test_same(self):
        result = audiofile.find_target_path(self.target, self.extensions)
        self.assertEqual(self.target, result)

    def test_different(self):
        target = self.target.replace('.flac', '.mp3')
        result = audiofile.find_target_path(target, self.extensions)
        self.assertEqual(self.target, result)


class TestFunctionBestFormat(unittest.TestCase):
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
        return audiofile.detect_best_format(
            helper.get_meta('quality', source),
            helper.get_meta('quality', target),
            helper.get_job()
        )

    def test_same_quality(self):
        with helper.Capturing() as output:
            result = self.source_target('flac.flac', 'flac.flac')
        self.assertEqual(result, 'target')
        self.assertEqual(
            output[0], 'Best format: Source and target have the same '
            'formats, use target.'
        )

    def test_type_target_better(self):
        with helper.Capturing() as output:
            result = self.source_target('mp3_128.mp3', 'flac.flac')
        self.assertEqual(result, 'target')
        self.assertEqual(
            output[0], 'Best format is “target” because of “type”: '
            '(source: mp3, target: flac)'
        )

    def test_type_source_better(self):
        with helper.Capturing() as output:
            result = self.source_target('flac.flac', 'mp3_128.mp3')
        self.assertEqual(result, 'source')
        self.assertEqual(
            output[0], 'Best format is “source” because of “type”: '
            '(source: flac, target: mp3)'
        )

    def test_bitrate_mp3_source_better(self):
        with helper.Capturing() as output:
            result = self.source_target('mp3_320.mp3', 'mp3_128.mp3')
        self.assertEqual(result, 'source')
        self.assertEqual(
            output[0], 'Best format is “source” because of “bitrate”: '
            '(source: 319999, target: 191995)'
        )

    def test_bitrate_mp3_target_better_2(self):
        with helper.Capturing() as output:
            result = self.source_target('mp3_144.mp3', 'mp3_320.mp3')
        self.assertEqual(result, 'target')
        self.assertEqual(
            output[0], 'Best format is “target” because of “bitrate”: '
            '(source: 86884, target: 319999)'
        )

    def test_bitrate_mp3_source_better_2(self):
        with helper.Capturing() as output:
            result = self.source_target('mp3_320.mp3', 'mp3_144.mp3')
        self.assertEqual(result, 'source')
        self.assertEqual(
            output[0], 'Best format is “source” because of “bitrate”: '
            '(source: 319999, target: 86884)'
        )

    def test_bitrate_m4a_target_better(self):
        with helper.Capturing() as output:
            result = self.source_target('m4a_100.m4a', 'm4a_250.m4a')
        self.assertEqual(result, 'target')
        self.assertEqual(
            output[0], 'Best format is “target” because of “bitrate”: '
            '(source: 198551, target: 235243)'
        )

    def test_bitrate_m4a_source_better(self):
        with helper.Capturing() as output:
            result = self.source_target('m4a_250.m4a', 'm4a_100.m4a')
        self.assertEqual(result, 'source')
        self.assertEqual(
            output[0], 'Best format is “source” because of “bitrate”: '
            '(source: 235243, target: 198551)'
        )


class TestBasicRename(unittest.TestCase):

    def setUp(self):
        self.tmp_album = helper.copy_to_tmp('files', 'album.mp3')
        with helper.Capturing():
            audiorename.execute(self.tmp_album)
        self.tmp_compilation = helper.copy_to_tmp('files', 'compilation.mp3')
        with helper.Capturing():
            audiorename.execute(self.tmp_compilation)

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
        self.tmp_album = helper.copy_to_tmp('files', 'album.mp3')
        with helper.Capturing():
            audiorename.execute('--copy', self.tmp_album)
        self.tmp_compilation = helper.copy_to_tmp('files', 'compilation.mp3')
        with helper.Capturing():
            audiorename.execute('--copy', self.tmp_compilation)

    def test_album(self):
        with helper.Capturing() as output:
            audiorename.execute(self.tmp_album)
        self.assertTrue('Exists' in helper.join(output))

    def test_compilation(self):
        with helper.Capturing() as output:
            audiorename.execute(self.tmp_compilation)
        self.assertTrue('Exists' in helper.join(output))

    def test_album_already_renamed(self):
        with helper.Capturing():
            audiorename.execute(self.tmp_album)
        with helper.Capturing() as output:
            audiorename.execute(helper.dir_cwd + helper.path_album)

        self.assertTrue('Renamed' in helper.join(output))

    def test_compilation_already_renamed(self):
        with helper.Capturing():
            audiorename.execute(self.tmp_compilation)
        with helper.Capturing() as output:
            audiorename.execute(helper.dir_cwd + helper.path_compilation)

        self.assertTrue('Renamed' in helper.join(output))

    def tearDown(self):
        shutil.rmtree(helper.dir_cwd + '/_compilations/')
        shutil.rmtree(helper.dir_cwd + '/t/')


class TestUnicodeUnittest(unittest.TestCase):

    def setUp(self):
        self.uni = helper.get_testfile('äöü', 'ÅåÆæØø.mp3')
        self.renamed = os.path.join('/_', '►', '$ar_combined_album',
                                    '$ar_combined_disctrack'
                                    '_ÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž.mp3')

    def test_dry_run(self):
        with helper.Capturing() as output:
            audiorename.execute('--one-line', '--dry-run', '--verbose',
                                self.uni)
        self.assertTrue(self.renamed in ' '.join(output))

    def test_rename(self):
        tmp_dir = tempfile.mkdtemp()
        tmp = os.path.join(tmp_dir, 'äöü.mp3')
        shutil.copyfile(self.uni, tmp)
        with helper.Capturing() as output:
            audiorename.execute('--one-line', '--verbose', '--target',
                                tmp_dir, tmp)
        self.assertTrue(self.renamed in ' '.join(output))

    def test_copy(self):
        with helper.Capturing() as output:
            audiorename.execute('--one-line', '--verbose', '--copy',
                                self.uni)
        self.assertTrue(self.renamed in ' '.join(output))

    def tearDown(self):
        try:
            shutil.rmtree(helper.dir_cwd + '/_/')
        except OSError:
            pass


class TestProcessTargetPath(unittest.TestCase):

    def setUp(self):
        meta = helper.get_meta('files', 'album.mp3')
        self.meta = meta.export_dict()

    @staticmethod
    def get_meta(**args):
        meta = helper.get_meta('files', 'album.mp3')
        for key in args:
            setattr(meta, key, args[key])
        return meta.export_dict()

    @staticmethod
    def process(meta, format_string, shell_friendly=True):
        return audiofile.process_target_path(meta, format_string,
                                             shell_friendly)

    def assertTargetPath(self, expected, format_string='$title', **fields):
        if fields:
            meta = self.get_meta(**fields)
        else:
            meta = self.meta
        self.assertEqual(self.process(meta, format_string), expected)

    def test_simple(self):
        result = self.process(self.meta, '$title')
        self.assertEqual(result, 'full')

    def test_unicode(self):
        self.assertTargetPath('aeoeue', title='äöü')

    def test_enddot(self):
        self.assertTargetPath('a', title='a.')

    def test_turned_quotation(self):
        self.assertTargetPath('aa', title='a¿a')


if __name__ == '__main__':
    unittest.main()
