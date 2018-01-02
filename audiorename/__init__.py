# -*- coding: utf-8 -*-

"""Rename audio files from metadata tags."""

import os
from audiorename.args import parse_args
from .batch import Batch
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions


class Job(object):
    """Holds informations of one job which can handle multiple files.

    Unifies and processes the data of the `argparse` call. The properies of
    this class can be used to display an overview message of the job.
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
        * move: Rename / move the file (default).
        * copy: Copy the source file to the target path.
        """
        if self._args.dry_run:
            return u'dry_run'
        if self._args.copy:
            return u'copy'
        else:
            return u'move'

    @property
    def filter(self):
        out = {}

        if self._args.filter_album_min:
            out['album_min'] = self._args.filter_album_min

        if self._args.filter_album_complete:
            out['album_complete'] = self._args.filter_album_complete
        return out

    @property
    def source(self):
        """The source path as a absolute path. Maybe a directory or a file."""
        return os.path.abspath(self._args.path)

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

    def __init(self):
        pass


def execute(argv=None):
    """Main function

    :param list argv: The command line arguments specified as a list: e. g
        :code:`['--dry-run', '.']`
    """
    args = parse_args(argv)

    if args.filter_album_min or args.filter_album_complete:
        args.filter = True
    else:
        args.filter = False

    job = Job(args)
    batch = Batch(args, job)
    batch.execute()
