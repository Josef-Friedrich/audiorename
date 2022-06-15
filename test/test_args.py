"""Test the submodule “args.py”."""

import unittest
import re
import audiorename
import helper


class TestCommandlineInterface(unittest.TestCase):

    def test_help_short(self):
        with self.assertRaises(SystemExit) as cm:
            with helper.Capturing():
                audiorename.execute('-h')
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '0')

    def test_help_long(self):
        with self.assertRaises(SystemExit) as cm:
            with helper.Capturing():
                audiorename.execute('--help')
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '0')

    def test_without_arguments(self):
        with self.assertRaises(SystemExit) as cm:
            with helper.Capturing('stderr'):
                audiorename.execute()
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '2')

    def test_without_mutually_exclusive(self):
        with self.assertRaises(SystemExit) as cm:
            with helper.Capturing('stderr') as output:
                audiorename.execute('--copy', '--move', '.')
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '2')
        self.assertTrue('not allowed with argument' in ' '.join(output))


class TestVersion(unittest.TestCase):

    def test_version(self):
        with self.assertRaises(SystemExit):
            with helper.Capturing() as output:
                audiorename.execute('--version')

        result = re.search('[^ ]* [^ ]*', output[0])
        self.assertTrue(result)


class TestHelp(unittest.TestCase):

    def setUp(self):
        with self.assertRaises(SystemExit):
            with helper.Capturing() as output:
                audiorename.execute('--help')
        self.output = '\n'.join(output)

    def test_tmep(self):
        self.assertTrue('%title{text}' in self.output)

    def test_phrydy(self):
        self.assertTrue('mb_releasegroupid' in self.output)

    # album
    def test_field_ar_classical_album(self):
        self.assertTrue('ar_classical_album' in self.output)

    def test_field_ar_combined_album(self):
        self.assertTrue('ar_combined_album' in self.output)
        self.assertTrue('“album” without' in self.output)

    def test_field_ar_initial_album(self):
        self.assertTrue('ar_initial_album' in self.output)
        self.assertTrue('First character' in self.output)

    # artist
    def test_field_ar_initial_artist(self):
        self.assertTrue('ar_initial_artist' in self.output)
        self.assertTrue('First character' in self.output)

    def test_field_ar_combined_artist(self):
        self.assertTrue('ar_combined_artist' in self.output)
        self.assertTrue('The first available' in self.output)

    def test_field_ar_combined_artist_sort(self):
        self.assertTrue('ar_combined_artist_sort' in self.output)
        self.assertTrue('The first available' in self.output)

    # composer
    def test_field_ar_initial_composer(self):
        self.assertTrue('ar_initial_composer' in self.output)

    def test_field_ar_combined_composer(self):
        self.assertTrue('ar_combined_composer' in self.output)

    def test_field_ar_combined_disctrack(self):
        self.assertTrue('ar_combined_disctrack' in self.output)
        self.assertTrue('Combination of' in self.output)

    def test_field_ar_classical_performer(self):
        self.assertTrue('ar_classical_performer' in self.output)

    def test_field_ar_classical_title(self):
        self.assertTrue('ar_classical_title' in self.output)

    def test_field_ar_classical_track(self):
        self.assertTrue('ar_classical_track' in self.output)

    def test_field_ar_combined_year(self):
        self.assertTrue('ar_combined_year' in self.output)
        self.assertTrue('First “original_year”' in self.output)


class TestArgsDefault(unittest.TestCase):

    def setUp(self):
        from audiorename.args import parse_args
        from audiorename.args import ArgsDefault
        self.default = ArgsDefault()
        self.default.source = 'lol'
        self.args = parse_args(['lol'])

    # positional arguments
    def test_source(self):
        self.assertEqual(self.args.source, 'lol')
        self.assertEqual(self.args.source, self.default.source)

    # optional arguments
    def test_album_complete(self):
        self.assertEqual(self.args.album_complete, None)
        self.assertEqual(self.args.album_complete, self.default.album_complete)

    def test_album_min(self):
        self.assertEqual(self.args.album_min, None)
        self.assertEqual(self.args.album_min, self.default.album_min)

    def test_cleaning_action(self):
        self.assertEqual(self.args.cleaning_action, None)
        self.assertEqual(self.args.cleaning_action,
                         self.default.cleaning_action)

    def test_backup_folder(self):
        self.assertEqual(self.args.backup_folder, None)
        self.assertEqual(self.args.backup_folder, self.default.backup_folder)

    def test_best_format(self):
        self.assertEqual(self.args.best_format, None)
        self.assertEqual(self.args.best_format, self.default.best_format)

    def test_classical(self):
        self.assertEqual(self.args.classical, None)
        self.assertEqual(self.args.classical, self.default.classical)

    def test_color(self):
        self.assertEqual(self.args.color, None)
        self.assertEqual(self.args.color, self.default.color)

    def test_compilation(self):
        self.assertEqual(self.args.compilation, None)
        self.assertEqual(self.args.compilation, self.default.compilation)

    def test_debug(self):
        self.assertEqual(self.args.debug, None)
        self.assertEqual(self.args.debug, self.default.debug)

    def test_dry_run(self):
        self.assertEqual(self.args.dry_run, None)
        self.assertEqual(self.args.dry_run, self.default.dry_run)

    def test_enrich_metadata(self):
        self.assertEqual(self.args.enrich_metadata, None)
        self.assertEqual(self.args.enrich_metadata,
                         self.default.enrich_metadata)

    def test_extension(self):
        self.assertEqual(self.args.extension, None)
        self.assertEqual(self.args.extension, self.default.extension)

    def test_field_skip(self):
        self.assertEqual(self.args.field_skip, None)
        self.assertEqual(self.args.field_skip, self.default.field_skip)

    def test_format(self):
        self.assertEqual(self.args.format, None)
        self.assertEqual(self.args.format, self.default.format)

    def test_format_classical(self):
        self.assertEqual(self.args.format_classical, None)
        self.assertEqual(self.args.format_classical,
                         self.default.format_classical)

    def test_job_info(self):
        self.assertEqual(self.args.job_info, None)
        self.assertEqual(self.args.job_info, self.default.job_info)

    def test_mb_track_listing(self):
        self.assertEqual(self.args.mb_track_listing, None)
        self.assertEqual(self.args.mb_track_listing,
                         self.default.mb_track_listing)

    def test_move_action(self):
        self.assertEqual(self.args.move_action, None)
        self.assertEqual(self.args.move_action, self.default.move_action)

    def test_one_line(self):
        self.assertEqual(self.args.one_line, None)
        self.assertEqual(self.args.one_line, self.default.one_line)

    def test_remap_classical(self):
        self.assertEqual(self.args.remap_classical, None)
        self.assertEqual(self.args.remap_classical,
                         self.default.remap_classical)

    def test_shell_friendly(self):
        self.assertEqual(self.args.shell_friendly, None)
        self.assertEqual(self.args.shell_friendly, self.default.shell_friendly)

    def test_soundtrack(self):
        self.assertEqual(self.args.soundtrack, None)
        self.assertEqual(self.args.soundtrack, self.default.soundtrack)

    def test_source_as_target(self):
        self.assertEqual(self.args.source_as_target, None)
        self.assertEqual(self.args.source_as_target,
                         self.default.source_as_target)

    def test_target(self):
        self.assertEqual(self.args.target, None)
        self.assertEqual(self.args.target, self.default.target)

    def test_stats(self):
        self.assertEqual(self.args.stats, None)
        self.assertEqual(self.args.stats, self.default.stats)

    def test_verbose(self):
        self.assertEqual(self.args.verbose, None)
        self.assertEqual(self.args.verbose, self.default.verbose)


if __name__ == '__main__':
    unittest.main()
