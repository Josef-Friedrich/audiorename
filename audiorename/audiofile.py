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
import errno

if six.PY2:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')


def create_dir(path):
    path = os.path.dirname(path)

    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def mb_track_listing(album, title, length):
    if hasattr(mb_track_listing, 'counter'):
        mb_track_listing.counter += 1
    else:
        mb_track_listing.counter = 1
    m, s = divmod(length, 60)
    mmss = '{:d}:{:02d}'.format(int(m), int(s))
    output = '{:d}. {:s}: {:s} ({:s})'.format(mb_track_listing.counter, album,
                                              title, mmss)
    output = output.replace('Op.', 'op.')
    output = output.replace('- ', '')
    print(output)


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


def get_target(target, extensions):
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
        target = Functions.tmpl_deldupchars(target)
    return re.sub('\.$', '', target)


class Action(object):

    def __init__(self, job):
        self.job = job
        self.dry_run = job.dry_run

    def backup(self, path):
        if not self.dry_run:
            shutil.move(path, path + '.bak')

    def copy(self, source, target):
        if not self.dry_run:
            shutil.copy2(source, target)

    def delete(self, path):
        if not self.dry_run:
            os.remove(path)

    def move(self, source, target):
        if not self.dry_run:
            shutil.move(source, target)


def rename_actions(source_path, desired_target_path, job):
    """"""

    action = Action(job)

    source = Meta(source_path)

    target_path = get_target(desired_target_path, job.filter.extension)

    if target_path:
        target = Meta(target_path)
        best = best_format(target, source)

    # Actions

    # do nothing
    if source_path == desired_target_path:
        return []

    # delete source
    if job.rename.delete_existing and desired_target_path == target_path:
        action.delete(source_path)

    # delete target
    if job.rename.best_format and best == 'source' and target_path:
        # backup
        if job.rename.cleanup == 'backup':
            action.backup(target_path)
        elif job.rename.cleanup == 'delete':
            action.delete(target_path)

        if job.rename.cleanup:
            target_path = None

    # copy
    if job.rename.move == 'copy' and not target_path:
        action.copy(source_path, desired_target_path)

    # move
    if job.rename.move == 'move' and not target_path:
        action.move(source_path, desired_target_path)


def do_job_on_audiofile(source, job=None):
    def count(key):
        job.stats.counter.count(key)
    skip = False

    source = os.path.realpath(source)
    extension = source.split('.')[-1]
    try:
        meta = Meta(source, job.shell_friendly)

    except phrydy.mediafile.UnreadableFileError:
        skip = True

    message = MessageFile(job, source)

    ##
    # Skips
    ##

    if skip:
        message.process(u'Broken file')
        return

    if job.field_skip and  \
       (
            not hasattr(meta, job.field_skip) or
            not getattr(meta, job.field_skip)
       ):
        message.process(u'No field')
        count('no_field')
        return

    ##
    # Output only
    ##

    if job.output.mb_track_listing:
        mb_track_listing(meta.album, meta.title,
                         meta.length)
        return

    if job.output.debug:
        phrydy.doc.Debug(
            source,
            Meta,
            Meta.fields,
            job.output.color,
        ).output()
        return

    ##
    # Metadata actions
    ##

    if job.metadata_actions.enrich_metadata:
        print('Enrich metadata')
        meta.enrich_metadata()

    if job.metadata_actions.remap_classical:
        print('Remap classical')
        meta.remap_classical()

    if job.metadata_actions.remap_classical or \
            job.metadata_actions.enrich_metadata:
        meta.save()

    ##
    # Rename action
    ##

    if job.rename.move != 'no_rename':

        if meta.soundtrack:
            format_string = job.format.soundtrack
        elif meta.comp:
            format_string = job.format.compilation
        else:
            format_string = job.format.default

        meta_dict = meta.export_dict()

        target = process_target_path(meta_dict, format_string,
                                     job.shell_friendly)
        target = os.path.join(job.target, target + '.' + extension.lower())
        message.target = target
        existing_target = get_target(target, job.filter.extension)

        if job.dry_run:
            message.process(u'Dry run')
            count('dry_run')

        elif not existing_target:
            create_dir(target)
            if job.rename.move == u'copy':
                message.process(u'Copy')
                shutil.copy2(source, target)
            else:
                message.process(u'Rename')
                shutil.move(source, target)
                count('rename')
        elif target == source:
            message.process(u'Renamed')
            count('renamed')
        else:
            message.process(u'Exists')
            count('exists')
            if job.rename.cleanup == 'delete':
                meta_target = Meta(existing_target)
                best_format(meta, meta_target)
                os.remove(source)
                print('Delete existing file: ' + source)
