# -*- coding: utf-8 -*-

"""This module contains all functionality on the level of a single audio file.
"""

import os

import ansicolor
import shutil

import phrydy
from phrydy.utils import as_string
from tmep import Functions
from tmep import Template

from .meta import Meta
import six
import re

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

    @staticmethod
    def color(message):
        if message == u'Rename' or message == u'Copy':
            return u'yellow'
        elif message == u'Renamed':
            return u'green'
        elif message == u'Dry run':
            return u'white'
        elif message == u'Exists' or \
                message == 'No field' or \
                message == u'Broken file':
            return u'red'
        else:
            return u'white'

    def process(self, message):
        indent = 12
        message_processed = message + u':'
        message_processed = message_processed.ljust(indent)
        message_processed = u'[' + message_processed + u']'

        if self.job.output.color:
            color = self.color(message)
            colorize = getattr(ansicolor, color)
            message_processed = colorize(message_processed, reverse=True)

        if self.job.output.one_line:
            connection = u' -> '
        else:
            connection = u'\n' + u'-> '.rjust(indent + 3)

        line1 = message_processed + u' ' + self.source
        if self.target:
            if self.job.output.color:
                target = ansicolor.yellow(self.target)
            else:
                target = self.target
            line2 = connection + target
        else:
            line2 = u''

        print(line1 + line2)


def check_target(target, extensions):
    """Get the path of a existing audio file target. Search for audio files
    with different extensions.
    """
    target = os.path.splitext(target)[0]
    for extension in extensions:
        audio_file = target + '.' + extension
        if os.path.exists(audio_file):
            return audio_file


def best_format(source, target):
    """
    :param source: The metadata object of the source file.
    :type source: audiorename.meta.Meta
    :param target: The metadata object of the target file.
    :type target: audiorename.meta.Meta
    :return: Either the string `source` or the string `target`
    :rtype: string
    """
    def get_highest(dictionary):
        for key, value in sorted(dictionary.items()):
            out = value
        return out

    if source.format == target.format:

        bitrates = {}
        bitrates[source.bitrate] = 'source'
        bitrates[target.bitrate] = 'target'
        return get_highest(bitrates)

    else:

        # All types:
        #
        # 'aac'
        # 'aiff'
        # 'alac': Apple Lossless Audio Codec (losless)
        # 'ape'
        # 'asf'
        # 'dsf'
        # 'flac'
        # 'mp3'
        # 'mpc'
        # 'ogg'
        # 'opus'
        # 'wv': WavPack (losless)

        ranking = {
            'flac': 10,
            'alac': 9,
            'aac': 8,
            'mp3': 5,
            'ogg': 2,
            'wma': 1,
        }

        types = {}
        types[ranking[source.type]] = 'source'
        types[ranking[target.type]] = 'target'
        return get_highest(types)


def process_target_path(meta, format_string, shell_friendly=True):
    template = Template(as_string(format_string))
    functions = Functions(meta)
    target = template.substitute(meta, functions.functions())

    if isinstance(target, str) or isinstance(target, unicode):
        if shell_friendly:
            target = Functions.tmpl_asciify(target)
            target = Functions.tmpl_delchars(target, '().,!"\'’')
            target = Functions.tmpl_replchars(target, '-', ' ')
        # asciify generates new characters which must be sanitzed, e. g.:
        # ¿ -> ?
        target = Functions.tmpl_delchars(target, ':*?"<>|\~&{}')
    return re.sub('\.$', '', target)


def determine_rename_actions(source_path, target_path, delete=False,
                             copy=False):
    """Determine the todo actions without performing them. The main reason for
    not exectuting this actions immediately is the --dry-run option.

    .. code:: Python

        [
            {
                'action': 'delete',
                'path': '/path/to/file.mp3',
            },
            {
                'action': 'copy',
                'source': '/path/to/file.mp3',
                'target': '/path/to/file.mp3',
            },
            {
                'action': 'move',
                'source': '/path/to/file.mp3',
                'target': '/path/to/file.mp3',

            },
        ]

    """
    pass
    # source = Meta(source_path)
    # print(copy)
    #
    # target_path = check_target(target_path, self.job.filter.extension)
    #
    # meta_target = Meta(existing_target)
    # best_format(self.meta, meta_target)


class Rename(object):
    """Rename one file"""

    def __init__(self, source, job):
        self.skip = False
        self.job = job

        self.source = os.path.realpath(source)
        self.extension = self.source.split('.')[-1]
        try:
            self.meta = Meta(self.source, self.job.shell_friendly)

        except phrydy.mediafile.UnreadableFileError:
            self.skip = True

        self.message = MessageFile(job, self.source)

    def count(self, key):
        self.job.stats.counter.count(key)

    def generate_filename(self):
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
        new = self.post_template(new)
        new = f.tmpl_deldupchars(new + '.' + self.extension.lower())
        self.new_file = new
        self.target = os.path.join(self.job.target, new)
        self.message.target = self.target

    def post_template(self, text):
        if isinstance(text, str) or isinstance(text, unicode):
            if self.job.shell_friendly:
                text = Functions.tmpl_asciify(text)
                text = Functions.tmpl_delchars(text, '().,!"\'’')
                text = Functions.tmpl_replchars(text, '-', ' ')
            # asciify generates new characters which must be sanitzed, e. g.:
            # ¿ -> ?
            text = Functions.tmpl_delchars(text, ':*?"<>|\~&{}')
        return text

    def create_dir(self, path):
        path = os.path.dirname(path)
        import errno
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def mb_track_listing(self):
        m, s = divmod(self.meta.length, 60)
        mmss = '{:d}:{:02d}'.format(int(m), int(s))
        output = '{:d}. {:s}: {:s} ({:s})'.format(counter, self.meta.album,
                                                  self.meta.title, mmss)
        output = output.replace('Op.', 'op.')
        output = output.replace('- ', '')
        print(output)

    def execute(self):
        """
        .. todo:: Rethink `fetch work`
        """
        global counter
        counter += 1

        ##
        # Skips
        ##

        if self.skip:
            self.message.process(u'Broken file')
            return

        if self.job.field_skip and  \
           (
                not hasattr(self.meta, self.job.field_skip) or
                not getattr(self.meta, self.job.field_skip)
           ):
            self.message.process(u'No field')
            self.count('no_field')
            return

        ##
        # Output only
        ##

        if self.job.output.mb_track_listing:
            self.mb_track_listing()
            return

        if self.job.output.debug:
            phrydy.doc.Debug(
                self.source,
                Meta,
                Meta.fields,
                self.job.output.color,
            ).output()
            return

        ##
        # Metadata actions
        ##

        if self.job.metadata_actions.enrich_metadata:
            print('Enrich metadata')
            self.meta.enrich_metadata()

        if self.job.metadata_actions.remap_classical:
            print('Remap classical')
            self.meta.remap_classical()

        if self.job.metadata_actions.remap_classical or \
                self.job.metadata_actions.enrich_metadata:
            self.meta.save()

        ##
        # Rename action
        ##

        if self.job.rename_action != 'no_rename':
            self.generate_filename()

            existing_target = check_target(self.target,
                                           self.job.filter.extension)

            if self.job.rename_action == u'dry_run':
                self.message.process(u'Dry run')
                self.count('dry_run')

            elif not existing_target:
                self.create_dir(self.target)
                if self.job.rename_action == u'copy':
                    self.message.process(u'Copy')
                    shutil.copy2(self.source, self.target)
                else:
                    self.message.process(u'Rename')
                    shutil.move(self.source, self.target)
                    self.count('rename')
            elif self.target == self.source:
                self.message.process(u'Renamed')
                self.count('renamed')
            else:
                self.message.process(u'Exists')
                self.count('exists')
                if self.job.delete_existing:
                    meta_target = Meta(existing_target)
                    best_format(self.meta, meta_target)
                    os.remove(self.source)
                    print('Delete existing file: ' + self.source)


def do_rename(path, job=None):
    audio = Rename(path, job)
    audio.execute()