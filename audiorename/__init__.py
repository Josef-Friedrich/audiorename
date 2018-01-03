# -*- coding: utf-8 -*-

"""Rename audio files from metadata tags."""

import os
from audiorename.args import parse_args
from .batch import Batch
from ._version import get_versions
from collections import namedtuple

__version__ = get_versions()['version']
del get_versions


class Job(object):
    """Holds informations of one job which can handle multiple files.

    A jobs represents one call of the program on the command line.
    This class unifies and processes the data of the `argparse` call. It groups
    the `argparse` key value pairs into parent proteries. The properties of
    this class can be used to display an overview message of the
    job.
    """

    formats = {}
    """
    default
    compilation
    soundtrack
    """

    def __init__(self, args):
        self._args = args

    @property
    def action(self):
        """
        :return:

        :rtype: string

        * copy
        * dry_run
        * mb_track_listing
        * move

        """
        if self._args.mb_track_listing:
            return u'mb_track_listing'
        elif self._args.dry_run:
            return u'dry_run'
        elif self._args.copy:
            return u'copy'
        elif self._args.move:
            return u'move'
        else:
            return u'move'

    @property
    def filter(self):
        Filter = namedtuple('Filter', [
            'album_complete',
            'album_min',
            'extension'
        ])

        return Filter(
            self._args.album_complete,
            self._args.album_min,
            self._args.extension
        )

    @property
    def output(self):
        Output = namedtuple('Output', [
            'job_info',
            'verbose',
        ])

        return Output(
            self._args.job_info,
            self._args.verbose,
        )

    @property
    def source(self):
        """The source path as a absolute path. Maybe a directory or a file."""
        return os.path.abspath(self._args.source)

    @property
    def target(self):
        """The path of the target path as an absolute path. Is always a
        directory.
        """
        if self._args.source_as_target_dir:
            if os.path.isdir(self.source):
                return os.path.abspath(self.source)
            else:
                return os.path.abspath(os.path.dirname(self.source))
        elif self._args.target_dir:
            return os.path.abspath(self._args.target_dir)
        else:
            return os.getcwd()


class PerFile(object):

    def __init__(self):
        pass


class MessageJob(object):

    def __init__(self, job):
        self.job = job
        self.keys = ['action', 'source', 'target']

    @staticmethod
    def format_key_value(key, value):
        return key + ': ' + value + '\n'

    def print_output(self):
        out = u''
        for key in self.keys:
            out = out + self.format_key_value(key, getattr(self.job, key))

        print(out)


def execute(argv=None):
    """Main function

    :param list argv: The command line arguments specified as a list: e. g
        :code:`['--dry-run', '.']`
    """
    args = parse_args(argv)

    if args.album_min or args.album_complete:
        args.filter = True
    else:
        args.filter = False

    job = Job(args)
    if job.output.job_info:
        message = MessageJob(job)
        message.print_output()
    batch = Batch(args, job)
    batch.execute()
