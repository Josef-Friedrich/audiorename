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


class MessageFile(object):
    """Print out message on file level, foreach file to rename or to copy.

    :param string job: A instance of the class
        :class:`audiorename.Job`
    :param string source: The source file
    :param string target: The target file
    """

    def __init__(self, job, source, target=None):
        self.job = job
        self._source = source
        if target:
            self._target = target
        self.verbose = job.output.verbose

    @property
    def source(self):
        cwd = os.getcwd()
        if not self.verbose and len(cwd) > 1:
            return self._source.replace(cwd, '')
        else:
            return self._source

    @property
    def target(self):
        if not hasattr(self, '_target'):
            return ''
        if not self.verbose and len(self.job.target) > 1:
            return self._target.replace(self.job.target, '')
        else:
            return self._target

    @target.setter
    def target(self, value):
        self._target = value

    def process(self, action=u'Rename', error=False):
        indent = 12
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

        line1 = message + u' ' + self.source
        if self.target:
            line2 = u'\n' + u'-> '.rjust(indent + 3) + \
                ansicolor.yellow(self.target)
        else:
            line2 = u''

        out = line1 + line2

        print(out)


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

    target = ''
    """The target directory"""

    cwd = os.getcwd()
    """The path of the current working directory"""

    def __init__(self, old_file=False, job=False):
        self.skip = False

        if job:
            self.job = job

        if old_file:
            self.old_file = old_file

            self.old_path = os.path.realpath(self.old_file)
            self.extension = self.old_file.split('.')[-1]
            try:
                self.meta = Meta(self.old_path, self.job.shell_friendly)

            except phrydy.mediafile.UnreadableFileError:
                self.skip = True

        self.message = MessageFile(job, self.old_path)

    def generateFilename(self):
        if self.meta.soundtrack:
            format_string = self.job.format.soundtrack
        elif self.meta.comp:
            format_string = self.job.format.compilation
        else:
            format_string = self.job.format.default

        meta_dict = self.meta.export_dict()

        t = Template(as_string(format_string))
        f = Functions(meta_dict)
        new = t.substitute(meta_dict, f.functions())
        new = self.postTemplate(new)
        new = f.tmpl_deldupchars(new + '.' + self.extension.lower())
        self.new_file = new
        self.new_path = os.path.join(self.job.target, new)
        self.message.target = self.new_path

    def postTemplate(self, text):
        if isinstance(text, str) or isinstance(text, unicode):
            if self.job.shell_friendly:
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

    def dryRun(self):
        self.generateFilename()
        self.message.process(action=u'Dry run')

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
        self.message.process(action=u'Get work')

    def action(self, copy=False):
        """Rename or copy to new path

        :param bool copy: Copy file

        :return: None
        """
        self.generateFilename()
        if not os.path.exists(self.new_path):
            self.createDir(self.new_path)
            if copy:
                self.message.process(action=u'Copy')
                shutil.copy2(self.old_path, self.new_path)
            else:
                self.message.process(action=u'Rename')
                shutil.move(self.old_path, self.new_path)
        elif self.new_path == self.old_path:
            self.message.process(action=u'Renamed', error=False)
        else:
            self.message.process(action=u'Exists', error=True)
            if self.job.delete_existing:
                os.remove(self.old_path)
                print('Delete existing file: ' + self.old_path)

    def execute(self):
        """
        .. todo:: Rethink `fetch work`
        """
        global counter
        counter += 1
        skip = self.job.skip_if_empty
        if not self.meta:
            self.message.process(action=u'Broken file', error=True)
        elif skip and (not hasattr(self.meta, skip) or not
                       getattr(self.meta, skip)):
            self.message.process(action=u'No field', error=True)
        else:
            if self.job.action == u'dry_run':
                self.dryRun()
            elif self.job.action == u'mb_track_listing':
                self.mbTrackListing()
            elif self.job.action == u'copy':
                self.action(copy=True)
            elif self.job.action == u'work':
                self.fetch_work()
            else:
                self.action()


def do_rename(path, job=None):
    audio = Rename(path, job)
    audio.execute()
