# -*- coding: utf-8 -*-
import os
import six

from ansicolor import cyan
from ansicolor import green
from ansicolor import red
from ansicolor import yellow
import shutil

from phrydy import MediaFile
from phrydy import as_string
from tmep import Functions
from tmep import Template

from audiorename.meta import Meta


class Rename(object):
    def __init__(self, file, root_path='', args=None):
        if args:
            self.args = args

        if root_path:
            self.old_file = os.path.join(root_path, file)
        else:
            self.old_file = file

        if self.args.base_dir:
            self.base_dir = args.base_dir
        else:
            self.base_dir = os.getcwd()

        if self.args.folder_as_base_dir:
            self.base_dir = os.path.realpath(root_path)

        self.old_path = os.path.realpath(self.old_file)
        self.extension = self.old_file.split('.')[-1]

        meta = Meta(self.old_path, self.args)
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
        self.new_path = os.path.join(self.base_dir, new)
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

    def debug(self, option):
        def p(tag):
            print(cyan(tag) + u': ' + as_string(self.meta[tag]))

        print('\n' + green('- Debug: ') + red(option, reverse=True) + green(
            ' --------------------------------'))
        print(yellow(self.old_file))

        if option == 'artist':

            p('artist')
            p('albumartist')
            p('artistsafe')
            p('artist_sort')
            p('artist_credit')
            p('albumartist_credit')
            p('albumartist_sort')
            p('artistsafe_sort')

        elif option == 'meta':
            for key, value in self.meta.iteritems():
                if key != 'art' and value:
                    print(cyan(as_string(key)) + ': ' + as_string(value))

        elif option == 'mediafile':
            m = MediaFile(self.old_file)
            for key in MediaFile.readable_fields():
                value = getattr(m, key)
                if key != 'art':
                    print(cyan(key) + ': ' + as_string(value))

        elif option == 'mutagen':
            import mutagen
            m = mutagen.File(self.old_file, easy=True)
            print(m)
            for key, value in m.iteritems():
                print(cyan(key) + ': ' + value[0])

        elif option == 'track':
            p('track')
            p('tracktotal')
            p('disc')
            p('disctotal')
            p('disctrack')

        elif option == 'year':
            p('original_year')
            p('year')
            p('date')

    def rename(self):
        self.generateFilename()
        print('Rename: ' + self.message)
        self.createDir(self.new_path)
        print(self.new_path)
        shutil.move(self.old_path, self.new_path)

    def copy(self):
        self.generateFilename()
        print('Copy: ' + self.message)
        self.createDir(self.new_path)
        shutil.copy2(self.old_path, self.new_path)

    def execute(self):
        if self.args.skip_if_empty and not self.meta[self.args.skip_if_empty]:
            self.skipMessage()
        else:
            if self.args.dry_run:
                self.dryRun()
            elif self.args.debug:
                self.debug(self.args.debug)
            elif self.args.copy:
                self.copy()
            else:
                self.rename()
