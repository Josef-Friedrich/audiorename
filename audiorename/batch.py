# -*- coding: utf-8 -*-

from .rename import do_rename
from .bundler import Bundler
import os

class Batch(object):

    def __init__(self, args):
        self.args = args

    def execute(self):
        if os.path.isdir(self.args.folder):
            if self.args.bundle:
                Bundler(self.args.folder)
            else:
                for root_path, subdirs, files in os.walk(self.args.folder):
                    for file in files:
                        do_rename(file, root_path, args=self.args)

        else:
            do_rename(self.args.folder, args=self.args)
