# -*- coding: utf-8 -*-

import unittest
import re
import six
import audiorename
import helper


class TestCommandlineInterface(unittest.TestCase):

    def test_help_short(self):
        with self.assertRaises(SystemExit) as cm:
            with helper.Capturing():
                audiorename.execute(['-h'])
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '0')

    def test_help_long(self):
        with self.assertRaises(SystemExit) as cm:
            with helper.Capturing():
                audiorename.execute(['--help'])
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '0')

    def test_without_arguments(self):
        with self.assertRaises(SystemExit) as cm:
            with helper.Capturing('err'):
                audiorename.execute()
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '2')


class TestVersion(unittest.TestCase):

    def test_version(self):
        with self.assertRaises(SystemExit):
            if six.PY2:
                with helper.Capturing('err') as output:
                    audiorename.execute(['--version'])
            else:
                with helper.Capturing() as output:
                    audiorename.execute(['--version'])

        result = re.search('[^ ]* [^ ]*', output[0])
        self.assertTrue(result)


class TestHelp(unittest.TestCase):

    def setUp(self):
        with self.assertRaises(SystemExit):
            with helper.Capturing() as output:
                audiorename.execute(['--help'])
        self.output = '\n'.join(output)

    def test_tmep(self):
        self.assertTrue('%title{text}' in self.output)

    def test_phrydy(self):
        self.assertTrue('mb_releasegroupid' in self.output)

    # album
    def test_field_album_classical(self):
        self.assertTrue('album_classical' in self.output)

    def test_field_album_clean(self):
        self.assertTrue('album_clean' in self.output)
        self.assertTrue('“album” without' in self.output)

    def test_field_album_initial(self):
        self.assertTrue('album_initial' in self.output)
        self.assertTrue('First character' in self.output)

    # artist
    def test_field_artist_initial(self):
        self.assertTrue('artist_initial' in self.output)
        self.assertTrue('First character' in self.output)

    def test_field_artistsafe(self):
        self.assertTrue('artistsafe' in self.output)
        self.assertTrue('The first available' in self.output)

    def test_field_artistsafe_sort(self):
        self.assertTrue('artistsafe_sort' in self.output)
        self.assertTrue('The first available' in self.output)

    # composer
    def test_field_composer_initial(self):
        self.assertTrue('composer_initial' in self.output)

    def test_field_composer_safe(self):
        self.assertTrue('composer_safe' in self.output)

    def test_field_disctrack(self):
        self.assertTrue('disctrack' in self.output)
        self.assertTrue('Combination of' in self.output)

    def test_field_performer_classical(self):
        self.assertTrue('performer_classical' in self.output)

    def test_field_title_classical(self):
        self.assertTrue('title_classical' in self.output)

    def test_field_track_classical(self):
        self.assertTrue('track_classical' in self.output)

    def test_field_year_safe(self):
        self.assertTrue('year_safe' in self.output)
        self.assertTrue('First “original_year”' in self.output)


class TestArgsDefault(unittest.TestCase):

    def test_defaults(self):
        from audiorename.args import parse_args
        args = parse_args(['.'])
        self.assertEqual(args.path, '.')

        self.assertEqual(args.classical, False)
        self.assertEqual(args.compilation, False)
        self.assertEqual(args.copy, False)
        self.assertEqual(args.delete_existing, False)
        self.assertEqual(args.dry_run, False)
        self.assertEqual(args.extension, 'mp3,m4a,flac,wma')
        self.assertEqual(args.filter_album_complete, False)
        self.assertEqual(args.filter_album_min, False)
        self.assertEqual(args.format, False)
        self.assertEqual(args.mb_track_listing, False)
        self.assertEqual(args.shell_friendly, False)
        self.assertEqual(args.skip_if_empty, False)
        self.assertEqual(args.source_as_target_dir, False)
        self.assertEqual(args.target_dir, '')
        self.assertEqual(args.unittest, False)
        self.assertEqual(args.verbose, False)


if __name__ == '__main__':
    unittest.main()
