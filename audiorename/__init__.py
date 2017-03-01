# -*- coding: utf-8 -*-

"""Rename audio files from metadata tags."""

import os
from audiorename.args import parser
from .batch import Batch
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions


def execute(args=None):
    args = parser.parse_args(args)
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
