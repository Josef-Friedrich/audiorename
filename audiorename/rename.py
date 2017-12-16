# -*- coding: utf-8 -*-

"""Rename a single audio file."""

import os

import ansicolor
import shutil

from phrydy.mediafile import as_string
from tmep import Functions
from tmep import Template

from .meta import Meta
import six


from difflib import SequenceMatcher

if six.PY2:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

counter = 0


def common_substring(a, b):
    """Find the common substring of two paths at the beginning of the path
    string.

    :param string a: Path string a
    :param string b: Path string b

    :return string: the substring
    """
    match = SequenceMatcher(None, a, b).find_longest_match(0, len(a), 0,
                                                           len(b))

    if match.a == 0:
        return a[match.a: match.a + match.size]
    else:
        return ''


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
            '${disctrack}_%shorten{$title_classical,64}_' + \
            '%shorten{$acoustid_id,8}'


class Rename(object):

    old_path = ''
    """The old file path"""

    new_path = ''
    """The new file path"""

    extension = ''
    """The extension"""

    meta = ''
    """The meta object :class:`audiorename.meta.Meta`"""

    args = ''

    target_dir = ''
    """The target directory"""

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

    def processMessage(self, action=u'Rename', error=False, indent=16,
                       old_path=False, new_path=False, output=u'print'):
        action_processed = action + u':'
        message = action_processed.ljust(indent)
        message = u'[' + message + u']'

        if action == u'Already renamed':
            message = ansicolor.blue(message, reverse=True)
        elif action == u'Dry run':
            message = ansicolor.white(message, reverse=True)
        elif error:
            message = ansicolor.red(message, reverse=True)
        else:
            message = ansicolor.green(message, reverse=True)

        if not old_path:
            old_path = self.old_path

        if not new_path and hasattr(self, 'new_path'):
            new_path = self.new_path

        substring = common_substring(old_path, new_path)

        if substring:
            old_path = old_path.replace(substring, '')
            new_path = new_path.replace(substring, '')

        line1 = message + u' ' + old_path + '\n'
        if new_path:
            line2 = u'-> '.rjust(indent + 3) + ansicolor.yellow(new_path)
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
        m, s = divmod(self.meta['length'], 60)
        mmss = '{:d}:{:02d}'.format(int(m), int(s))
        output = '{:d}. {:s}: {:s} ({:s})'.format(counter, self.meta['album'],
                                                  self.meta['title'], mmss)
        output = output.replace('Op.', 'op.')
        output = output.replace('- ', '')
        print(output)

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
            self.processMessage(action=u'Already renamed', error=False)
        else:
            self.processMessage(action=u'File exits', error=True)

    def execute(self):
        global counter
        counter += 1
        skip = self.args.skip_if_empty
        if not self.meta:
            self.processMessage(action=u'Broken file', error=True)
        elif skip and (skip not in self.meta or not self.meta[skip]):
            self.processMessage(action=u'No field', error=True)
        else:
            if self.args.dry_run:
                self.dryRun()
            elif self.args.mb_track_listing:
                self.mbTrackListing()
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
