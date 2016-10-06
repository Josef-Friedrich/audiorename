# -*- coding: utf-8 -*-


import os
from audiorename.rename import Rename
from audiorename.args import parser
from .bundler import Bundler
from .batch import Batch
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions


def execute(args=None):
    args = parser.parse_args(args)

    batch = Batch(args)
    batch.execute()
