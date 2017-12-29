# -*- coding: utf-8 -*-

"""Test the submodule “batchelper.py”."""

import unittest
import os
import audiorename
import helper


class TestBatch(unittest.TestCase):

    def setUp(self):
        self.singles = helper.gen_file_list(
            ['album', 'compilation'],
            os.path.join(helper.test_files),
        )

        self.album_broken = helper.gen_file_list(
            ['01', '03', '05', '07', '09', '11'],
            os.path.join(helper.test_files, 'album_broken'),
        )

        self.album_broken_all = helper.gen_file_list(
            ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11'],
            os.path.join(helper.test_files, 'album_broken'),
        )

        self.album_complete = helper.gen_file_list(
            ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11'],
            os.path.join(helper.test_files, 'album_complete'),
        )

        self.album_incomplete = helper.gen_file_list(
            ['01', '02', '04', '05', '06', '07', '09', '10', '11'],
            os.path.join(helper.test_files, 'album_incomplete'),
        )

        self.album_small = helper.gen_file_list(
            ['01', '02', '03', '04', '05'],
            os.path.join(helper.test_files, 'album_small'),
        )

        self.all = self.singles + \
            self.album_broken_all +  \
            self.album_complete + \
            self.album_incomplete + \
            self.album_small

    def test_single(self):
        single = os.path.join(helper.test_files, 'album.mp3')
        with helper.Capturing() as output:
            audiorename.execute(['--unittest', single])
        self.assertEqual([single], output)

    def test_folder_complete(self):
        with helper.Capturing() as output:
            audiorename.execute(['--unittest', helper.test_files])
        self.assertEqual(self.all, output)

    def test_folder_sub(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--unittest',
                os.path.join(helper.test_files, 'album_complete')
            ])
        self.assertEqual(self.album_complete, output)

    def test_filter_album_min(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--filter-album-min',
                '7',
                helper.test_files
            ])
        self.assertEqual(self.album_complete + self.album_incomplete, output)

    def test_filter_album_min_no_match(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--filter-album-min',
                '23',
                helper.test_files
            ])
        self.assertEqual([], output)

    def test_filter_album_complete(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--filter-album-complete',
                helper.test_files
            ])
        self.assertEqual(
            self.singles +
            self.album_complete +
            self.album_small,
            output
        )

    def test_filter_all(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--filter-album-min',
                '7',
                '--filter-album-complete',
                helper.test_files
            ])
        self.assertEqual(self.album_complete, output)


class TestExtension(unittest.TestCase):

    def setUp(self):
        self.test_files = os.path.join(helper.dir_test, 'mixed_formats')

    def test_default(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--unittest',
                self.test_files
            ])
        self.assertEqual(
            output,
            helper.gen_file_list(
                ['01.flac', '02.m4a', '03.mp3'],
                self.test_files,
                extension=False
            )
        )

    def test_one(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--extension',
                'mp3,flac',
                self.test_files
            ])
        self.assertEqual(
            output,
            helper.gen_file_list(
                ['01.flac', '03.mp3'],
                self.test_files,
                extension=False
            )
        )

    def test_two(self):
        with helper.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--extension',
                'mp3',
                self.test_files
            ])
        self.assertEqual(
            output,
            helper.gen_file_list(['03.mp3'], self.test_files, extension=False)
        )


class TestSkip(unittest.TestCase):

    def setUp(self):
        self.file = os.path.join(helper.dir_test, 'broken', 'binary.mp3')
        with helper.Capturing() as output:
            audiorename.execute([
                '-d',
                '--verbose',
                self.file
            ])
        self.output = output

    def test_message(self):
        self.assertTrue('Broken file' in self.output[0])

    def test_file_in_message(self):
        self.assertTrue('Broken file' in self.output[0])
        self.assertTrue(self.file in self.output[0])

    def test_continuation(self):
        path = os.path.join(helper.dir_test, 'broken')
        with helper.Capturing() as output:
            audiorename.execute([
                '--unittest',
                path
            ])

        self.assertTrue(output[1])


if __name__ == '__main__':
    unittest.main()
