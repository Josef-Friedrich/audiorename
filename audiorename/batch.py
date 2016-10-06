# -*- coding: utf-8 -*-

from .rename import do_rename
from .bundler import Bundler
import os

class Batch(object):

    def __init__(self, args):
        self.args = args

    def execute(self):
        if os.path.isdir(self.args.path):
            if self.args.bundle:
                Bundler(self.args.path)
            else:
                for path, dirs, files in os.walk(self.args.path):
                    for file_name in files:
                        do_rename(os.path.join(path, file_name), args=self.args)

        else:
            do_rename(self.args.path, args=self.args)
