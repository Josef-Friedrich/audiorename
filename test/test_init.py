# -*- coding: utf-8 -*-

"""Test the code in the __init__ file."""

from audiorename import Job
from audiorename.args import ArgsDefault
import unittest
import os
import helper
from audiorename import audiofile
import audiorename


class TestClassMessage(unittest.TestCase):

    def setUp(self):
        self.job = helper.get_job()
        self.prefix = helper.dir_cwd
        self.source = audiofile.AudioFile(
            helper.get_testfile('files', 'album.mp3'),
            job=self.job,
            prefix=self.prefix
        )

    @staticmethod
    def get_message(**kwargs):
        return audiorename.Message(helper.get_job(**kwargs))

    def test_attributes(self):
        msg = self.get_message()
        self.assertEqual(msg.color, False)
        self.assertEqual(msg.verbose, False)
        self.assertEqual(msg.one_line, False)
        self.assertEqual(msg.max_field, 20)

    def test_diff(self):
        msg = self.get_message()
        with helper.Capturing() as output:
            msg.diff('title', '', 'full')
        self.assertEqual(output[0], '    title:                “”')
        self.assertEqual(output[1], '                          “full”')

    def test_output_one_line(self):
        msg = self.get_message(one_line=True)
        with helper.Capturing() as output:
            msg.output('   lol     ')
            msg.output('   lol     ')

        self.assertEqual(output[0], 'lol lol ')

    def test_output_multilines(self):
        msg = self.get_message(one_line=False)
        with helper.Capturing() as output:
            msg.output('one')
            msg.output('two')
        self.assertEqual(output[0], 'one')
        self.assertEqual(output[1], 'two')


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
        job = Job(self.args)
        self.args.album_complete = 19
        self.assertEqual(job.filter.album_min, False)
        self.assertEqual(job.filter.album_complete, 19)

    # album_min
    def test_filter_album_min(self):
        job = Job(self.args)
        self.args.album_min = 19
        self.assertEqual(job.filter.album_min, 19)
        self.assertEqual(job.filter.album_complete, False)

    # extension
    def test_filter_extension(self):
        job = Job(self.args)
        self.args.extension = 'lol'
        self.assertEqual(job.filter.extension, ['lol'])

    ##
    # metadata_actions
    ##

    # enrich_metadata
    def test_metadata_actions_enrich_metadata(self):
        job = Job(self.args)
        self.args.enrich_metadata = True
        self.assertEqual(job.metadata_actions.enrich_metadata, True)

    # remap_classical
    def test_metadata_actions_remap_classical(self):
        job = Job(self.args)
        self.args.remap_classical = True
        self.assertEqual(job.metadata_actions.remap_classical, True)

    ##
    # output
    ##

    # color
    def test_output_color(self):
        job = Job(self.args)
        self.args.color = True
        self.assertEqual(job.output.color, True)

    # debug
    def test_output_debug(self):
        job = Job(self.args)
        self.args.debug = True
        self.assertEqual(job.output.debug, True)

    # job_info
    def test_output_job_info(self):
        job = Job(self.args)
        self.args.job_info = True
        self.assertEqual(job.output.job_info, True)

    # mb_track_listing
    def test_output_mb_track_listing(self):
        job = Job(self.args)
        self.args.mb_track_listing = True
        self.assertEqual(job.output.mb_track_listing, True)

    # one_line
    def test_output_one_line(self):
        job = Job(self.args)
        self.args.one_line = True
        self.assertEqual(job.output.one_line, True)

    # stats
    def test_output_stats(self):
        job = Job(self.args)
        self.args.stats = True
        self.assertEqual(job.output.stats, True)

    # verbose
    def test_output_verbose(self):
        job = Job(self.args)
        self.args.verbose = True
        self.assertEqual(job.output.verbose, True)

    ##
    # rename
    ##

    # move default
    def test_rename_move_default(self):
        job = Job(self.args)
        self.assertEqual(job.rename.move, u'move')

    # move copy
    def test_rename_move_copy(self):
        job = Job(self.args)
        self.args.copy = True
        self.assertEqual(job.rename.move, u'copy')

    # move move
    def test_rename_move_move(self):
        job = Job(self.args)
        self.args.move = True
        self.assertEqual(job.rename.move, u'move')

    # move no_rename
    def test_rename_move_no_rename(self):
        job = Job(self.args)
        self.args.no_rename = True
        self.assertEqual(job.rename.move, u'no_rename')

    # best_format
    def test_rename_best_format(self):
        self.args.best_format = True
        job = Job(self.args)
        self.assertEqual(job.rename.best_format, True)

    # backup
    def test_rename_cleanup_backup(self):
        job = Job(self.args)
        self.args.backup = True
        self.assertEqual(job.rename.cleanup, u'backup')

    # delete_existing
    def test_rename_cleanup_delete(self):
        self.args.delete_existing = True
        job = Job(self.args)
        self.assertEqual(job.rename.cleanup, u'delete')

    ##
    # end rename
    ##

    # target
    def test_target(self):
        job = Job(self.args)
        self.args.path = u'.'
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
        self.args.path = u'.'
        job = Job(self.args)
        self.assertEqual(job.source, os.path.abspath(u'.'))


class TestTimer(unittest.TestCase):

    def setUp(self):
        from audiorename import Timer
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
        from audiorename import Counter
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
