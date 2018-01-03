# -*- coding: utf-8 -*-

"""Test the code in the __init__ file."""

import audiorename
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


class TestJob(unittest.TestCase):

    def setUp(self):
        self.args = ArgsDefault()

    def test_property_action(self):
        job = Job(self.args)
        self.assertEqual(job.action, u'move')

    def test_property_action_copy(self):
        job = Job(self.args)
        self.args.copy = True
        self.assertEqual(job.action, u'copy')

    def test_property_action_dry_run(self):
        job = Job(self.args)
        self.args.dry_run = True
        self.assertEqual(job.action, u'dry_run')

    def test_property_action_mb_track_listing(self):
        job = Job(self.args)
        self.args.mb_track_listing = True
        self.assertEqual(job.action, u'mb_track_listing')

    def test_property_action_move(self):
        job = Job(self.args)
        self.args.move = True
        self.assertEqual(job.action, u'move')

    def test_property_source(self):
        self.args.path = u'.'
        job = Job(self.args)
        self.assertEqual(job.source, os.path.abspath(u'.'))

    def test_property_filter_album_complete(self):
        job = Job(self.args)
        self.args.album_complete = 19
        self.assertEqual(job.filter.album_min, False)
        self.assertEqual(job.filter.album_complete, 19)

    def test_property_filter_album_min(self):
        job = Job(self.args)
        self.args.album_min = 19
        self.assertEqual(job.filter.album_min, 19)
        self.assertEqual(job.filter.album_complete, False)

    def test_property_filter_extension(self):
        job = Job(self.args)
        self.args.extension = 'lol'
        self.assertEqual(job.filter.extension, 'lol')

    def test_property_target(self):
        job = Job(self.args)
        self.args.path = u'.'
        self.assertEqual(job.target, os.getcwd())
        self.args.target_dir = 'test'
        self.assertEqual(job.target, os.path.abspath('test'))
        self.args.source_as_target_dir = True
        self.assertEqual(job.target, os.getcwd())


if __name__ == '__main__':
    unittest.main()
