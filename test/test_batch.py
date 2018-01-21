# -*- coding: utf-8 -*-

"""Test the submodule “batchelper.py”."""

import unittest
import audiorename
import helper


class TestBatch(unittest.TestCase):

    def setUp(self):
        self.singles = helper.gen_file_list(
            ['album', 'compilation'],
            helper.get_testfile('files'),
        )

        self.album_broken = helper.gen_file_list(
            ['01', '03', '05', '07', '09', '11'],
            helper.get_testfile('files', 'album_broken'),
        )

        self.album_broken_all = helper.gen_file_list(
            ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11'],
            helper.get_testfile('files', 'album_broken'),
        )

        self.album_complete = helper.gen_file_list(
            ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11'],
            helper.get_testfile('files', 'album_complete'),
        )

        self.album_incomplete = helper.gen_file_list(
            ['01', '02', '04', '05', '06', '07', '09', '10', '11'],
            helper.get_testfile('files', 'album_incomplete'),
        )

        self.album_small = helper.gen_file_list(
            ['01', '02', '03', '04', '05'],
            helper.get_testfile('files', 'album_small'),
        )

        self.all = self.singles + \
            self.album_broken_all +  \
            self.album_complete + \
            self.album_incomplete + \
            self.album_small

    def test_single(self):
        single = helper.get_testfile('files', 'album.mp3')
        with helper.Capturing() as output:
            audiorename.execute(['--dry-run', '--verbose', single])
        self.assertEqual([single], helper.filter_source(output))

    def test_folder_complete(self):
        with helper.Capturing() as output:
            audiorename.execute(['--dry-run', '--verbose',
                                helper.get_testfile('files')])
        self.assertEqual(self.all, helper.filter_source(output))

    def test_folder_sub(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--dry-run', '--verbose',
                helper.get_testfile('files', 'album_complete')
            ])
        self.assertEqual(self.album_complete, helper.filter_source(output))

    def test_album_min(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--dry-run', '--verbose',
                '--album-min',
                '7',
                helper.get_testfile('files')
            ])
        self.assertEqual(self.album_complete + self.album_incomplete,
                         helper.filter_source(output))

    def test_album_min_no_match(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--dry-run', '--verbose',
                '--album-min',
                '23',
                helper.get_testfile('files')
            ])
        self.assertEqual([], helper.filter_source(output))

    def test_album_complete(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--dry-run', '--verbose',
                '--album-complete',
                helper.get_testfile('files')
            ])
        self.assertEqual(
            self.singles +
            self.album_complete +
            self.album_small,
            helper.filter_source(output)
        )

    def test_filter_all(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--dry-run', '--verbose',
                '--album-min',
                '7',
                '--album-complete',
                helper.get_testfile('files')
            ])
        self.assertEqual(self.album_complete, helper.filter_source(output))


class TestExtension(unittest.TestCase):

    def setUp(self):
        self.test_files = helper.get_testfile('mixed_formats')

    def test_default(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--dry-run', '--verbose',
                self.test_files,
            ])
        self.assertEqual(
            helper.filter_source(output),
            helper.gen_file_list(
                ['01.flac', '02.m4a', '03.mp3'],
                self.test_files,
                extension=False
            )
        )

    def test_one(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--dry-run', '--verbose',
                '--extension',
                'mp3,flac',
                self.test_files
            ])
        self.assertEqual(
            helper.filter_source(output),
            helper.gen_file_list(
                ['01.flac', '03.mp3'],
                self.test_files,
                extension=False
            )
        )

    def test_two(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--dry-run', '--verbose',
                '--extension',
                'mp3',
                self.test_files
            ])
        self.assertEqual(
            helper.filter_source(output),
            helper.gen_file_list(['03.mp3'], self.test_files,
                                 extension=False)
        )


class TestSkip(unittest.TestCase):

    def setUp(self):
        self.file = helper.get_testfile('broken', 'binary.mp3')
        with helper.Capturing() as output:
            audiorename.execute([
                '-d',
                '--verbose',
                self.file
            ])
        self.output = helper.join(output)

    def test_message(self):
        self.assertTrue('Broken file' in self.output)

    def test_file_in_message(self):
        self.assertTrue('Broken file' in self.output)
        self.assertTrue(self.file in self.output)

    def test_continuation(self):
        path = helper.get_testfile('broken')
        with helper.Capturing() as output:
            audiorename.execute([
                '--dry-run', '--verbose',
                path
            ])
        output = helper.filter_source(output)
        self.assertTrue(output[1])


if __name__ == '__main__':
    unittest.main()
