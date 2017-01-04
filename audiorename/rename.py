# -*- coding: utf-8 -*-

"""Rename a single audio file."""

import os
import six

from ansicolor import green
from ansicolor import red
from ansicolor import yellow
import shutil

from phrydy.mediafile import as_string
from tmep import Functions
from tmep import Template

from .meta import Meta


def default_formats(classical=False, compilation=False):
    if not classical and not compilation:
        return '$artist_initial/' + \
            '%shorten{$artistsafe_sort}/' +  \
            '%shorten{$album_clean}%ifdef{year_safe,_${year_safe}}/' +  \
            '${disctrack}_%shorten{$title}'
    elif not classical and compilation:
        return '_compilations/' +  \
            '$album_initial/' +  \
            '%shorten{$album_clean}%ifdef{year_safe,_${year_safe}}/' +  \
            '${disctrack}_%shorten{$title}'
    elif classical:
        return '$composer_initial/$composer_safe/' +  \
            '%shorten{$album_classical,48}' + \
            '_[%shorten{$performer_classical,32}]/' +  \
            '${disctrack}_%shorten{$title_classical,64}_%shorten{$acoustid_id,8}'


class Rename(object):
    def __init__(self, old_file=False, args=False):
        if args:
            self.args = args

        if old_file:
            self.old_file = old_file

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

            meta = Meta(self.old_path, args.shell_friendly)
            self.meta = meta.getMeta()

    def generateFilename(self):
        if self.meta['comp'] and self.args.compilation:
            format_string = self.args.compilation
        elif not self.meta['comp'] and self.args.format:
            format_string = self.args.format
        else:
            format_string = default_formats(self.args.classical,
                                            self.meta['comp'])

        t = Template(as_string(format_string))
        f = Functions(self.meta)
        new = t.substitute(self.meta, f.functions())
        new = self.postTemplate(new)
        new = f.tmpl_deldupchars(new + '.' + self.extension.lower())
        self.new_path = os.path.join(self.target_dir, new)

    def postTemplate(self, text):
        if isinstance(text, str) or isinstance(text, unicode):
            if self.args.shell_friendly:
                text = Functions.tmpl_asciify(text)
                text = Functions.tmpl_delchars(text, '().,!"\'’')
                text = Functions.tmpl_replchars(text, '-', ' ')
            # asciify generates new characters which must be sanitzed, e. g.:
            # ¿ -> ?
            text = Functions.tmpl_delchars(text, ':*?"<>|\~&{}')
        return text

    def createDir(self, path):
        path = os.path.dirname(path)
        import errno
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def processMessage(self, action=u'Rename', message_type=u'Success',
                       indent=15, old_path=False, new_path=False,
                       output=u'print'):

        if not old_path:
            old_path = self.old_path

        if six.PY2:
            old_path = old_path.decode('utf-8')

        if not new_path and hasattr(self, 'new_path'):
            new_path = self.new_path

        message = action.ljust(indent)
        message = u'[' + message + u']:'

        if message_type == u'Error':
            message = red(message, reverse=True)
            if new_path:
                new_path = red(new_path)
        elif message_type == u'Success':
            message = green(message, reverse=True)
            new_path = green(new_path)
        elif message_type == u'Warning':
            message = yellow(message, reverse=True)
            new_path = yellow(new_path)

        line1 = message + u' ' + old_path + u'\n'
        if new_path:
            line2 = u'-> '.rjust(indent + 4) + green(new_path)
        else:
            line2 = u''

        out = line1 + line2

        if output == u'print':
            print(out)
        else:
            return out

    def dryRun(self):
        self.generateFilename()
        self.processMessage(action=u'Dry run')

    def action(self, copy=False):
        """Copy audio files to new path."""
        self.generateFilename()
        if not os.path.exists(self.new_path):
            self.createDir(self.new_path)
            if copy:
                self.processMessage(action=u'Copy')
                shutil.copy2(self.old_path, self.new_path)
            else:
                self.processMessage(action=u'Rename')
                shutil.move(self.old_path, self.new_path)
        elif self.new_path == self.old_path:
            self.processMessage(action=u'Already renamed',
                                message_type=u'Warning')
        else:
            self.processMessage(action=u'File exits', message_type=u'Error')

    def execute(self):
        skip = self.args.skip_if_empty
        if not self.meta:
            self.processMessage(action=u'Broken file', message_type=u'Error')
        elif skip and (skip not in self.meta or not self.meta[skip]):
            self.processMessage(action=u'No field', message_type=u'Error')
        else:
            if self.args.dry_run:
                self.dryRun()
            elif self.args.copy:
                self.action(copy=True)
            else:
                self.action()


def do_rename(path, args=None):
    if args.unittest:
        print(os.path.abspath(path))
    else:
        audio = Rename(path, args)
        audio.execute()
