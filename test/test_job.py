"""Test the code in the __init__ file."""

from audiorename.job import Job, Timer, Counter
from audiorename.args import ArgsDefault
import unittest
import os


class TestJob(unittest.TestCase):

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
        self.args.album_complete = 19
        job = Job(self.args)
        self.assertEqual(job.filter.album_min, None)
        self.assertEqual(job.filter.album_complete, 19)

    # album_min
    def test_filter_album_min(self):
        self.args.album_min = 19
        job = Job(self.args)
        self.assertEqual(job.filter.album_min, 19)
        self.assertEqual(job.filter.album_complete, None)

    # extension
    def test_filter_extension(self):
        self.args.extension = 'lol'
        job = Job(self.args)
        self.assertEqual(job.filter.extension, ['lol'])

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
        self.assertEqual(job.output.color, True)

    # debug
    def test_output_debug(self):
        self.args.debug = True
        job = Job(self.args)
        self.assertEqual(job.output.debug, True)

    # job_info
    def test_output_job_info(self):
        self.args.job_info = True
        job = Job(self.args)
        self.assertEqual(job.output.job_info, True)

    # mb_track_listing
    def test_output_mb_track_listing(self):
        self.args.mb_track_listing = True
        job = Job(self.args)
        self.assertEqual(job.output.mb_track_listing, True)

    # one_line
    def test_output_one_line(self):
        self.args.one_line = True
        job = Job(self.args)
        self.assertEqual(job.output.one_line, True)

    # stats
    def test_output_stats(self):
        self.args.stats = True
        job = Job(self.args)
        self.assertEqual(job.output.stats, True)

    # verbose
    def test_output_verbose(self):
        self.args.verbose = True
        job = Job(self.args)
        self.assertEqual(job.output.verbose, True)

    ##
    # rename
    ##

    # move default
    def test_rename_move_default(self):
        job = Job(self.args)
        self.assertEqual(job.rename.move, 'move')

    # move copy
    def test_rename_move_copy(self):
        self.args.copy = True
        job = Job(self.args)
        self.assertEqual(job.rename.move, 'copy')

    # move move
    def test_rename_move_move(self):
        self.args.move = True
        job = Job(self.args)
        self.assertEqual(job.rename.move, 'move')

    # move no_rename
    def test_rename_move_no_rename(self):
        self.args.no_rename = True
        job = Job(self.args)
        self.assertEqual(job.rename.move, 'no_rename')

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
        self.args.backup = True
        job = Job(self.args)
        self.assertEqual(job.rename.cleanup, 'backup')

    # delete
    def test_rename_cleanup_delete(self):
        self.args.delete = True
        job = Job(self.args)
        self.assertEqual(job.rename.cleanup, 'delete')

    ##
    # end rename
    ##

    # target
    def test_target(self):
        job = Job(self.args)
        self.args.path = '.'
        self.assertEqual(job.target, os.getcwd())
        self.args.target = 'test'
        self.assertEqual(job.target, os.path.abspath('test'))
        self.args.source_as_target = True
        self.assertEqual(job.target, os.getcwd())

    # shell_friendly
    def test_shell_friendly(self):
        self.args.shell_friendly = True
        job = Job(self.args)
        self.assertEqual(job.shell_friendly, True)

    # field_skip
    def test_field_skip(self):
        self.args.field_skip = True
        job = Job(self.args)
        self.assertEqual(job.field_skip, True)

    # source
    def test_source(self):
        self.args.path = '.'
        job = Job(self.args)
        self.assertEqual(job.source, os.path.abspath('.'))


class TestTimer(unittest.TestCase):

    def setUp(self):
        self.timer = Timer()

    def get_result(self, begin, end):
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
