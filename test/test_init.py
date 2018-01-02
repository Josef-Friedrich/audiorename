# -*- coding: utf-8 -*-

"""Test the code in the __init__ file."""

from audiorename import Job
from audiorename.args import ArgsDefault
import unittest
import os


class TestJob(unittest.TestCase):

    def setUp(self):
        self.args = ArgsDefault()

    def test_property_action(self):
        job = Job(self.args)
        self.assertEqual(job.action, u'move')
        self.args.copy = True
        self.assertEqual(job.action, u'copy')
        self.args.dry_run = True
        self.assertEqual(job.action, u'dry_run')

    def test_property_source(self):
        self.args.path = u'.'
        job = Job(self.args)
        self.assertEqual(job.source, os.path.abspath(u'.'))

    def test_property_filter(self):
        job = Job(self.args)
        self.assertEqual(job.filter, {})

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
