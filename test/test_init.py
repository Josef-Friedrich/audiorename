# -*- coding: utf-8 -*-

"""Test the code in the __init__ file."""

import audiorename
from audiorename import MessageJob
from audiorename import Job
from audiorename.args import ArgsDefault
import unittest
import os
import helper


class TestMessageJob(unittest.TestCase):

    def test_message_job(self):
        tmp = helper.copy_to_tmp(['files', 'album.mp3'])
        with helper.Capturing() as output:
            audiorename.execute(['--dry-run', '--job-info', tmp])
        self.assertEqual(output[0], 'action: dry_run')

    @unittest.skip('Fails with tox')
    def test_unit_color(self):
        message = MessageJob(helper.get_job(color=True))
        with helper.Capturing() as output:
            message.print_output()
        self.assertTrue(u'\x1b' in output[0])

    def test_unit_nocolor(self):
        message = MessageJob(helper.get_job(color=False))
        with helper.Capturing() as output:
            message.print_output()
        self.assertFalse(u'\x1b' in output[0])


class TestJob(unittest.TestCase):

    def setUp(self):
        self.args = ArgsDefault()

    def test_action(self):
        job = Job(self.args)
        self.assertEqual(job.action, u'move')

    def test_action_copy(self):
        job = Job(self.args)
        self.args.copy = True
        self.assertEqual(job.action, u'copy')

    def test_action_dry_run(self):
        job = Job(self.args)
        self.args.dry_run = True
        self.assertEqual(job.action, u'dry_run')

    def test_action_mb_track_listing(self):
        job = Job(self.args)
        self.args.mb_track_listing = True
        self.assertEqual(job.action, u'mb_track_listing')

    def test_action_move(self):
        job = Job(self.args)
        self.args.move = True
        self.assertEqual(job.action, u'move')

    def test_action_work(self):
        job = Job(self.args)
        self.args.work = True
        self.assertEqual(job.action, u'work')

    def test_delete_existing(self):
        self.args.delete_existing = True
        job = Job(self.args)
        self.assertEqual(job.delete_existing, True)

    def test_filter_album_complete(self):
        job = Job(self.args)
        self.args.album_complete = 19
        self.assertEqual(job.filter.album_min, False)
        self.assertEqual(job.filter.album_complete, 19)

    def test_filter_album_min(self):
        job = Job(self.args)
        self.args.album_min = 19
        self.assertEqual(job.filter.album_min, 19)
        self.assertEqual(job.filter.album_complete, False)

    def test_filter_extension(self):
        job = Job(self.args)
        self.args.extension = 'lol'
        self.assertEqual(job.filter.extension, 'lol')

    def test_output_color(self):
        job = Job(self.args)
        self.args.color = True
        self.assertEqual(job.output.color, True)

    def test_output_job_info(self):
        job = Job(self.args)
        self.args.job_info = True
        self.assertEqual(job.output.job_info, True)

    def test_output_verbose(self):
        job = Job(self.args)
        self.args.verbose = True
        self.assertEqual(job.output.verbose, True)

    def test_target(self):
        job = Job(self.args)
        self.args.path = u'.'
        self.assertEqual(job.target, os.getcwd())
        self.args.target = 'test'
        self.assertEqual(job.target, os.path.abspath('test'))
        self.args.source_as_target = True
        self.assertEqual(job.target, os.getcwd())

    def test_shell_friendly(self):
        self.args.shell_friendly = True
        job = Job(self.args)
        self.assertEqual(job.shell_friendly, True)

    def test_skip_if_empty(self):
        self.args.skip_if_empty = True
        job = Job(self.args)
        self.assertEqual(job.skip_if_empty, True)

    def test_source(self):
        self.args.path = u'.'
        job = Job(self.args)
        self.assertEqual(job.source, os.path.abspath(u'.'))


if __name__ == '__main__':
    unittest.main()
