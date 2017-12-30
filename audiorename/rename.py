# -*- coding: utf-8 -*-

"""Rename a single audio file."""

import os

import ansicolor
import shutil

import phrydy
from phrydy.utils import as_string
from tmep import Functions
from tmep import Template

from .meta import Meta
import six

if six.PY2:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

counter = 0


def default_formats(classical=False, compilation=False):
    """Provide default format string formats

    :param bool classical: True if the audio file is a classical piece.
    :param bool compilation: True if the aufio file is a member of
        a compilation.

    :return: The formatted string
    :rtype: string
    """
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
            '${disctrack}_%shorten{$title_classical,64}_' + \
            '%shorten{$acoustid_id,8}'


class Rename(object):
    """Rename one file"""

    old_path = ''
    """The absolute path of the old file."""

    old_file = ''
    """The input path of the old file."""

    new_path = ''
    """The absolute path of the new file."""

    new_file = ''
    """The path inside the target directory of the new file."""

    extension = ''
    """The extension"""

    meta = ''
    """The meta object :class:`audiorename.meta.Meta`"""

    args = ''

    target_dir = ''
    """The target directory"""

    cwd = os.getcwd()
    """The path of the current working directory"""

    def __init__(self, old_file=False, args=False):
        self.skip = False

        if args:
            self.args = args

        if old_file:
            self.old_file = old_file

            if self.args.target_dir:
                self.target_dir = self.args.target_dir
            else:
                self.target_dir = self.cwd

            if self.args.source_as_target_dir:

                if self.args.is_dir:
                    self.target_dir = args.path
                else:
                    self.target_dir = os.path.dirname(args.path)

            self.old_path = os.path.realpath(self.old_file)
            self.extension = self.old_file.split('.')[-1]
            try:
                self.meta = Meta(self.old_path, self.args)

            except phrydy.mediafile.UnreadableFileError:
                self.skip = True

    def generateFilename(self):
        if self.meta.comp and self.args.compilation:
            format_string = self.args.compilation
        elif not self.meta.comp and self.args.format:
            format_string = self.args.format
        else:
            format_string = default_formats(self.args.classical,
                                            self.meta.comp)

        meta_dict = self.meta.export_dict()

        t = Template(as_string(format_string))
        f = Functions(meta_dict)
        new = t.substitute(meta_dict, f.functions())
        new = self.postTemplate(new)
        new = f.tmpl_deldupchars(new + '.' + self.extension.lower())
        self.new_file = new
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

    def processMessage(self, action=u'Rename', error=False, indent=12,
                       old_path=False, new_path=False, output=u'print'):
        action_processed = action + u':'
        message = action_processed.ljust(indent)
        message = u'[' + message + u']'

        if action == u'Rename' or action == u'Copy':
            message = ansicolor.yellow(message, reverse=True)
        elif action == u'Renamed':
            message = ansicolor.green(message, reverse=True)
        elif action == u'Dry run':
            message = ansicolor.white(message, reverse=True)
        elif error:
            message = ansicolor.red(message, reverse=True)
        else:
            message = ansicolor.white(message, reverse=True)

        if not old_path and hasattr(self, 'old_path'):
            output_old = self.old_path
        else:
            output_old = old_path

        if not new_path and hasattr(self, 'new_path'):
            output_new = self.new_path
        else:
            output_new = new_path

        if not self.args.verbose:
            if output_old and hasattr(self, 'cwd') and len(self.cwd) > 1:
                output_old = output_old.replace(self.cwd, '')
            if output_new and len(self.target_dir) > 1:
                output_new = output_new.replace(self.target_dir, '')

        line1 = message + u' ' + output_old + '\n'
        if output_new:
            line2 = u'-> '.rjust(indent + 3) + ansicolor.yellow(output_new)
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

    def mbTrackListing(self):
        m, s = divmod(self.meta.length, 60)
        mmss = '{:d}:{:02d}'.format(int(m), int(s))
        output = '{:d}. {:s}: {:s} ({:s})'.format(counter, self.meta.album,
                                                  self.meta.title, mmss)
        output = output.replace('Op.', 'op.')
        output = output.replace('- ', '')
        print(output)

    def fetch_work(self):
        self.meta.fetch_work()
        self.meta.save()
        self.processMessage(action=u'Get work')

    def action(self, copy=False):
        """Rename or copy to new path

        :param bool copy: Copy file

        :return: None
        """
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
            self.processMessage(action=u'Renamed', error=False)
        else:
            self.processMessage(action=u'Exists', error=True)
            if self.args.delete_existing:
                os.remove(self.old_path)
                print('Delete existing file: ' + self.old_path)

    def execute(self):
        global counter
        counter += 1
        skip = self.args.skip_if_empty
        if not self.meta:
            self.processMessage(action=u'Broken file', error=True)
        elif skip and (not hasattr(self.meta, skip) or not
                       getattr(self.meta, skip)):
            self.processMessage(action=u'No field', error=True)
        else:
            if self.args.dry_run:
                self.dryRun()
            elif self.args.mb_track_listing:
                self.mbTrackListing()
            elif self.args.copy:
                self.action(copy=True)
            elif self.args.work:
                self.fetch_work()
            else:
                self.action()


def do_rename(path, args=None):
    if args.unittest:
        print(os.path.abspath(path))
    else:
        audio = Rename(path, args)
        audio.execute()
