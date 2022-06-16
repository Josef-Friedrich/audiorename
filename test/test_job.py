"""Test the file job.py."""

from audiorename.job import Job, Timer, Counter
from audiorename.args import ArgsDefault
import unittest
import os
import helper


class TestJobWithArgParser(unittest.TestCase):

    def setUp(self):
        self.args = ArgsDefault()

    # dry_run
    def test_rename_action_dry_run(self):
        self.args.dry_run = True
        job = Job(self.args)
        self.assertEqual(job.dry_run, True)

    ##
    # filter
    ##

    # album_complete
    def test_filter_album_complete(self):
        self.args.album_complete = True
        job = Job(self.args)
        self.assertEqual(job.filters.album_min, None)
        self.assertEqual(job.filters.album_complete, True)

    # album_min
    def test_filter_album_min(self):
        self.args.album_min = 19
        job = Job(self.args)
        self.assertEqual(job.filters.album_min, 19)
        self.assertEqual(job.filters.album_complete, False)

    # extension
    def test_filter_extension(self):
        self.args.extension = 'lol'
        job = Job(self.args)
        self.assertEqual(job.filters.extension, ['lol'])

    ##
    # metadata_actions
    ##

    # enrich_metadata
    def test_metadata_actions_enrich_metadata(self):
        self.args.enrich_metadata = True
        job = Job(self.args)
        self.assertEqual(job.metadata_actions.enrich_metadata, True)

    # remap_classical
    def test_metadata_actions_remap_classical(self):
        self.args.remap_classical = True
        job = Job(self.args)
        self.assertEqual(job.metadata_actions.remap_classical, True)

    ##
    # output
    ##

    # color
    def test_output_color(self):
        self.args.color = True
        job = Job(self.args)
        self.assertEqual(job.cli_output.color, True)

    # debug
    def test_output_debug(self):
        self.args.debug = True
        job = Job(self.args)
        self.assertEqual(job.cli_output.debug, True)

    # job_info
    def test_output_job_info(self):
        self.args.job_info = True
        job = Job(self.args)
        self.assertEqual(job.cli_output.job_info, True)

    # mb_track_listing
    def test_output_mb_track_listing(self):
        self.args.mb_track_listing = True
        job = Job(self.args)
        self.assertEqual(job.cli_output.mb_track_listing, True)

    # one_line
    def test_output_one_line(self):
        self.args.one_line = True
        job = Job(self.args)
        self.assertEqual(job.cli_output.one_line, True)

    # stats
    def test_output_stats(self):
        self.args.stats = True
        job = Job(self.args)
        self.assertEqual(job.cli_output.stats, True)

    # verbose
    def test_output_verbose(self):
        self.args.verbose = True
        job = Job(self.args)
        self.assertEqual(job.cli_output.verbose, True)

    ##
    # rename
    ##

    # move_action default
    def test_rename_move_action_default(self):
        job = Job(self.args)
        self.assertEqual(job.rename.move_action, 'move')

    # move_action set value
    def test_rename_move_action_set(self):
        self.args.move_action = 'copy'
        job = Job(self.args)
        self.assertEqual(job.rename.move_action, 'copy')

    # best_format
    def test_rename_best_format(self):
        self.args.best_format = True
        job = Job(self.args)
        self.assertEqual(job.rename.best_format, True)

    # backup_folder
    def test_rename_backup_folder(self):
        self.args.backup_folder = '/tmp'
        job = Job(self.args)
        self.assertEqual(job.rename.backup_folder, '/tmp')

    # backup
    def test_rename_cleanup_backup(self):
        self.args.cleaning_action = 'backup'
        job = Job(self.args)
        self.assertEqual(job.rename.cleaning_action, 'backup')

    ##
    # end rename
    ##

    # target
    def test_target(self):
        self.args.path = '.'
        job = Job(self.args)
        self.assertEqual(job.selection.target, os.getcwd())

        self.args.target = 'test'
        job = Job(self.args)
        self.assertEqual(job.selection.target, os.path.abspath('test'))

        self.args.source_as_target = True
        job = Job(self.args)
        self.assertEqual(job.selection.target, os.getcwd())

    # shell_friendly
    def test_shell_friendly(self):
        self.args.shell_friendly = True
        job = Job(self.args)
        self.assertEqual(job.template_settings.shell_friendly, True)

    # field_skip
    def test_field_skip(self):
        self.args.field_skip = 'album'
        job = Job(self.args)
        self.assertEqual(job.filters.field_skip, 'album')

    # source
    def test_source(self):
        self.args.path = '.'
        job = Job(self.args)
        self.assertEqual(job.selection.source, os.path.abspath('.'))


class TestJobWithConfigParser(unittest.TestCase):

    def get_job(self, *config_file: str) -> Job:
        args = ArgsDefault()
        args.config = helper.get_testfile(*config_file)
        return Job(args)

    def test_section_selection(self):
        job = self.get_job('config', 'all-true.ini')
        self.assertEqual(job.selection.source, '/tmp')
        self.assertEqual(job.selection.target, '/tmp')
        self.assertEqual(job.selection.source_as_target, True)


class TestTimer(unittest.TestCase):

    def setUp(self):
        self.timer = Timer()

    def get_result(self, begin: float, end: float) -> str:
        self.timer.begin = begin
        self.timer.end = end
        return self.timer.result()

    def test_method_start(self):
        self.timer.start()
        self.assertTrue(self.timer.begin > 0)

    def test_method_stop(self):
        self.timer.stop()
        self.assertTrue(self.timer.end > 0)

    def test_method_result(self):
        self.assertEqual(self.get_result(10.3475, 14.594), '4.2s')

    def test_method_result_large(self):
        self.assertEqual(self.get_result(10, 145), '135.0s')

    def test_method_result_small(self):
        self.assertEqual(self.get_result(10.00001, 10.00002), '0.0s')


class TestCounter(unittest.TestCase):

    def setUp(self):
        self.counter = Counter()

    def test_reset(self):
        self.counter.count('lol')
        self.counter.reset()
        self.assertEqual(self.counter.get('lol'), 0)

    def test_count(self):
        self.counter.count('rename')
        self.assertEqual(self.counter.get('rename'), 1)
        self.counter.count('rename')
        self.assertEqual(self.counter.get('rename'), 2)

    def test_result(self):
        self.counter.count('rename')
        self.assertEqual(self.counter.result(),
                         'rename=1')

        self.counter.count('no_field')
        self.assertEqual(self.counter.result(),
                         'no_field=1 rename=1')


if __name__ == '__main__':
    unittest.main()
