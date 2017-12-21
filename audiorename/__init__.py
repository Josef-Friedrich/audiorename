# -*- coding: utf-8 -*-

"""Rename audio files from metadata tags."""

import os
from audiorename.args import parse_args
from .batch import Batch
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions


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
