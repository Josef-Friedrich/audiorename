import unittest
import os
import audiorename
import helper as h


class TestBatch(unittest.TestCase):

    def setUp(self):
        self.singles = h.gen_file_list(
            ['album', 'compilation'],
            os.path.join(h.test_files),
        )

        self.album_broken = h.gen_file_list(
            ['01', '03', '05', '07', '09', '11'],
            os.path.join(h.test_files, 'album_broken'),
        )

        self.album_broken_all = h.gen_file_list(
            ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11'],
            os.path.join(h.test_files, 'album_broken'),
        )

        self.album_complete = h.gen_file_list(
            ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11'],
            os.path.join(h.test_files, 'album_complete'),
        )

        self.album_incomplete = h.gen_file_list(
            ['01', '02', '04', '05', '06', '07', '09', '10', '11'],
            os.path.join(h.test_files, 'album_incomplete'),
        )

        self.album_small = h.gen_file_list(
            ['01', '02', '03', '04', '05'],
            os.path.join(h.test_files, 'album_small'),
        )

        self.all = self.singles + \
            self.album_broken_all +  \
            self.album_complete + \
            self.album_incomplete + \
            self.album_small

    def test_single(self):
        single = os.path.join(h.test_files, 'album.mp3')
        with h.Capturing() as output:
            audiorename.execute(['--unittest', single])
        self.assertEqual([single], output)

    def test_folder_complete(self):
        with h.Capturing() as output:
            audiorename.execute(['--unittest', h.test_files])
        self.assertEqual(self.all, output)

    def test_folder_sub(self):
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                os.path.join(h.test_files, 'album_complete')
            ])
        self.assertEqual(self.album_complete, output)

    def test_filter_album_min(self):
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--filter-album-min',
                '7',
                h.test_files
            ])
        self.assertEqual(self.album_complete + self.album_incomplete, output)

    def test_filter_album_min_no_match(self):
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--filter-album-min',
                '23',
                h.test_files
            ])
        self.assertEqual([], output)

    def test_filter_album_complete(self):
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                '--filter-album-complete',
                h.test_files
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
                h.test_files
            ])
        self.assertEqual(self.album_complete, output)


class TestExtension(unittest.TestCase):

    def setUp(self):
        self.test_files = os.path.join(h.dir_test, 'mixed_formats')

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


class TestSkip(unittest.TestCase):

    def setUp(self):
        self.file = os.path.join(h.dir_test, 'broken', 'binary.mp3')
        with h.Capturing() as output:
            audiorename.execute([
                '-d',
                self.file
            ])
        self.output = output

    def test_message(self):
        self.assertTrue('Broken file' in self.output[0])

    def test_file_in_message(self):
        self.assertTrue('Broken file' in self.output[0])
        self.assertTrue(self.file in self.output[0])

    def test_continuation(self):
        path = os.path.join(h.dir_test, 'broken')
        with h.Capturing() as output:
            audiorename.execute([
                '--unittest',
                path
            ])

        self.assertTrue(output[1])
