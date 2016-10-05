# -*- coding: utf-8 -*-


import os
from audiorename.rename import Rename
from audiorename.args import parser
from .bundler import Bundler
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions


def do_rename(path, root_path='', args=None):
    if path.lower().endswith((".mp3", ".m4a", ".flac", ".wma")):
        audio = Rename(path, root_path, args)
        audio.execute()


def execute(args=None):
    args = parser.parse_args(args)

    if os.path.isdir(args.folder):
        if args.bundle:
            Bundler(args.folder)
        else:
            for root_path, subdirs, files in os.walk(args.folder):
                for file in files:
                    do_rename(file, root_path, args=args)

    else:
        do_rename(args.folder, args=args)
