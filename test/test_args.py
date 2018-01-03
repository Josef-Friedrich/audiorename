# -*- coding: utf-8 -*-

"""Test the submodule “args.py”."""

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

    def test_without_mutually_exclusive(self):
        with self.assertRaises(SystemExit) as cm:
            with helper.Capturing('err') as output:
                audiorename.execute(['--copy', '--mb-track-listing', '.'])
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '2')
        self.assertTrue('not allowed with argument' in ' '.join(output))


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

    def setUp(self):
        from audiorename.args import parse_args
        from audiorename.args import ArgsDefault
        self.default = ArgsDefault()
        self.default.source = 'lol'
        self.args = parse_args(['lol'])

    def test_source(self):
        self.assertEqual(self.args.source, 'lol')
        self.assertEqual(self.args.source, self.default.source)

    def test_classical(self):
        self.assertEqual(self.args.classical, False)
        self.assertEqual(self.args.classical, self.default.classical)

    def test_compilation(self):
        self.assertEqual(self.args.compilation, False)
        self.assertEqual(self.args.compilation, self.default.compilation)

    def test_copy(self):
        self.assertEqual(self.args.copy, False)
        self.assertEqual(self.args.copy, self.default.copy)

    def test_delete_existing(self):
        self.assertEqual(self.args.delete_existing, False)
        self.assertEqual(self.args.delete_existing,
                         self.default.delete_existing)

    def test_dry_run(self):
        self.assertEqual(self.args.dry_run, False)
        self.assertEqual(self.args.dry_run, self.default.dry_run)

    def test_extension(self):
        self.assertEqual(self.args.extension, 'mp3,m4a,flac,wma')
        self.assertEqual(self.args.extension, self.default.extension)

    def test_filter_album_complete(self):
        self.assertEqual(self.args.filter_album_complete, False)
        self.assertEqual(self.args.filter_album_complete,
                         self.default.filter_album_complete)

    def test_filter_album_min(self):
        self.assertEqual(self.args.filter_album_min, False)
        self.assertEqual(self.args.filter_album_min,
                         self.default.filter_album_min)

    def test_format(self):
        self.assertEqual(self.args.format, False)
        self.assertEqual(self.args.format, self.default.format)

    def test_job_info(self):
        self.assertEqual(self.args.job_info, False)
        self.assertEqual(self.args.job_info, self.default.job_info)

    def test_mb_track_listing(self):
        self.assertEqual(self.args.mb_track_listing, False)
        self.assertEqual(self.args.mb_track_listing,
                         self.default.mb_track_listing)

    def test_move(self):
        self.assertEqual(self.args.move, False)
        self.assertEqual(self.args.move, self.default.move)

    def test_shell_friendly(self):
        self.assertEqual(self.args.shell_friendly, False)
        self.assertEqual(self.args.shell_friendly, self.default.shell_friendly)

    def test_skip_if_empty(self):
        self.assertEqual(self.args.skip_if_empty, False)
        self.assertEqual(self.args.skip_if_empty, self.default.skip_if_empty)

    def test_soundtrack(self):
        self.assertEqual(self.args.soundtrack, False)
        self.assertEqual(self.args.soundtrack, self.default.soundtrack)

    def test_source_as_target_dir(self):
        self.assertEqual(self.args.source_as_target_dir, False)
        self.assertEqual(self.args.source_as_target_dir,
                         self.default.source_as_target_dir)

    def test_target_dir(self):
        self.assertEqual(self.args.target_dir, '')
        self.assertEqual(self.args.target_dir, self.default.target_dir)

    def test_unittest(self):
        self.assertEqual(self.args.unittest, False)
        self.assertEqual(self.args.unittest, self.default.unittest)

    def test_verbose(self):
        self.assertEqual(self.args.verbose, False)
        self.assertEqual(self.args.verbose, self.default.verbose)

    def test_work(self):
        self.assertEqual(self.args.work, False)
        self.assertEqual(self.args.work, self.default.work)


if __name__ == '__main__':
    unittest.main()
