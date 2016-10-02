# -*- coding: utf-8 -*-

__version__ = u'0.0.8'

import os

from audiorename.rename import Rename
from audiorename.args import parser


def do_rename(path, root_path='', args=None):
    if path.lower().endswith((".mp3", ".m4a", ".flac", ".wma")):
        audio = Rename(path, root_path, args)
        audio.execute()


def execute(args=None):
    args = parser.parse_args(args)

    if args.version:
        print('Version: ' + __version__)

    elif os.path.isdir(args.folder):
        for root_path, subdirs, files in os.walk(args.folder):
            for file in files:
                do_rename(file, root_path, args=args)

    else:
        do_rename(args.folder, args=args)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
