# -*- coding: utf-8 -*-

"""Rename audio files from metadata tags."""

import os
from audiorename.args import parse_args
from .batch import Batch
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions


class Job(object):

    """Holds informations of one job which can handle multiple files."""

    source = u''
    """The source path. May be a directory or a file."""

    target = u''

    formats = {}
    """
    default
    compilation
    soundtrack
    """

    action = u''
    """
    rename/move (default)
    copy
    """

    filters = []
    """Filters"""

    def __init__(self, args):
        pass


class PerFile(object):

    def __init(self):
        pass


def execute(argv=None):
    """Main function

    :param list argv: The command line arguments specified as a list: e. g
        :code:`['--dry-run', '.']`
    """
    args = parse_args(argv)
    args.path = os.path.abspath(args.path)
    if os.path.isdir(args.path):
        args.is_dir = True
    else:
        args.is_dir = False

    if args.filter_album_min or args.filter_album_complete:
        args.filter = True
    else:
        args.filter = False

    batch = Batch(args)
    batch.execute()
