# -*- coding: utf-8 -*-
import os
import six

from ansicolor import green
from ansicolor import red
import shutil

from phrydy import as_string
from tmep import Functions
from tmep import Template

from .meta import Meta

formats = {
    'default': '$artist_initial/' +
    '%shorten{$artistsafe_sort}/' +
    '%shorten{$album}%ifdef{year_safe,_${year_safe}}/' +
    '${disctrack}_%shorten{$title}',
    'compilation': '_compilations/' +
    '$album_initial/' +
    '%shorten{$album}%ifdef{year_safe,_${year_safe}}/' +
    '${disctrack}_%shorten{$title}',
}


class Rename(object):
    def __init__(self, file, args):
        if args:
            self.args = args

        self.old_file = file

        if args.target_dir:
            self.target_dir = args.target_dir
        else:
            self.target_dir = os.getcwd()

        if args.source_as_target_dir:

            if args.is_dir:
                self.target_dir = args.path
            else:
                self.target_dir = os.path.dirname(args.path)

        self.old_path = os.path.realpath(self.old_file)
        self.extension = self.old_file.split('.')[-1]

        meta = Meta(self.old_path, args)
        self.meta = meta.getMeta()

    def generateFilename(self):
        if self.meta['comp']:
            t = Template(as_string(self.args.compilation))
        else:
            t = Template(as_string(self.args.format))
        f = Functions(self.meta)
        new = t.substitute(self.meta, f.functions())
        new = self.postTemplate(new)
        new = f.tmpl_deldupchars(new + '.' + self.extension.lower())
        self.new_path = os.path.join(self.target_dir, new)
        if six.PY2:
            old_path = self.old_path.decode('utf-8')
        else:
            old_path = self.old_path
        self.message = red(old_path) + '\n  -> ' + green(
            self.new_path) + '\n'

    def postTemplate(self, text):
        if isinstance(text, str) or isinstance(text, unicode):
            if self.args.shell_friendly:
                text = Functions.tmpl_asciify(text)
                text = Functions.tmpl_delchars(text, '[]().,!"\'’')
                text = Functions.tmpl_replchars(text, '-', ' ')
        return text

    def createDir(self, path):
        path = os.path.dirname(path)
        import errno
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def skipMessage(self):
        print(
            red('☠ no field ' + self.args.skip_if_empty + ' ☠',
                reverse=True) + ': ' + self.old_file)

    def dryRun(self):
        self.generateFilename()
        print('Dry run: ' + self.message)

    def rename(self):
        """Rename audio files"""
        self.generateFilename()
        print('Rename: ' + self.message)
        self.createDir(self.new_path)
        shutil.move(self.old_path, self.new_path)

    def copy(self):
        """Copy audio files to new path."""
        self.generateFilename()
        print('Copy: ' + self.message)
        self.createDir(self.new_path)
        shutil.copy2(self.old_path, self.new_path)

    def execute(self):
        skip = self.args.skip_if_empty
        if skip and (skip not in self.meta or not self.meta[skip]):
            self.skipMessage()
        else:
            if self.args.dry_run:
                self.dryRun()
            elif self.args.copy:
                self.copy()
            else:
                self.rename()


def do_rename(path, args=None):
    if args.unittest:
        print(os.path.abspath(path))
    else:
        audio = Rename(path, args)
        audio.execute()
