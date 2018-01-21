# -*- coding: utf-8 -*-

"""This module contains all functionality on the level of a single audio file.
"""

from __future__ import print_function

import os

import ansicolor
import shutil

import phrydy
from phrydy.utils import as_string
from tmep import Functions
from tmep import Template

from .args import all_fields
from .meta import Meta, dict_diff
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


class AudioFile(object):

    def __init__(self, path=None, file_type='source', prefix=None, job=None):
        self.__path = path
        self.type = file_type
        self.job = job
        self.__prefix = prefix
        self.shorten_symbol = '[…]'

        if not self.job:
            shell_friendly = True
        else:
            shell_friendly = self.job.shell_friendly
        if self.exists:
            try:
                self.meta = Meta(self.abspath, shell_friendly)

            except phrydy.mediafile.UnreadableFileError:
                self.meta = False

    @property
    def abspath(self):
        return os.path.abspath(self.__path)

    @property
    def prefix(self):
        if self.__prefix and len(self.__prefix) > 1:
            if self.__prefix[-1] != os.path.sep:
                return self.__prefix + os.path.sep
            else:
                return self.__prefix

    @property
    def exists(self):
        return os.path.exists(self.abspath)

    @property
    def extension(self):
        return self.abspath.split('.')[-1].lower()

    @property
    def short(self):
        if self.prefix:
            short = self.abspath.replace(self.prefix, '')
        else:
            short = os.path.basename(self.abspath)

        return self.shorten_symbol + short

    @property
    def filename(self):
        return os.path.basename(self.abspath)

    @property
    def dir_and_file(self):
        path_segments = self.abspath.split(os.path.sep)
        return os.path.sep.join(path_segments[-2:])


class MBTrackListing(object):

    def __init__(self):
        self.counter = 0

    def format_audiofile(self, album, title, length):
        self.counter += 1

        m, s = divmod(length, 60)
        mmss = '{:d}:{:02d}'.format(int(m), int(s))
        output = '{:d}. {:s}: {:s} ({:s})'.format(self.counter, album,
                                                  title, mmss)
        output = output.replace('Op.', 'op.')
        return output.replace('- ', '')


mb_track_listing = MBTrackListing()


class Message(object):
    """Print messages on the command line interface.

    :param job: The `job` object
    :type job: audiorename.Job
    """

    def __init__(self, job):
        self.color = job.output.color
        self.verbose = job.output.verbose
        self.one_line = job.output.one_line
        self.max_field = self.max_fields_length()
        self.indent_width = 4

    @staticmethod
    def max_fields_length():
        return phrydy.doc.get_max_field_length(all_fields)

    def output(self, text=''):
        if self.one_line:
            print(text.strip(), end=' ')
        else:
            print(text)

    def template_indent(self, level=1):
        return (' ' * self.indent_width) * level

    def template_path(self, audio_file):
        if self.verbose:
            path = audio_file.abspath
        else:
            path = audio_file.short

        if self.color:
            if audio_file.type == 'source':
                path = ansicolor.magenta(path)
            else:
                path = ansicolor.yellow(path)

        return path

    def next_file(self, audio_file):
        print()
        if self.verbose:
            path = audio_file.abspath
        else:
            path = audio_file.dir_and_file
        if self.color:
            path = ansicolor.blue(path, reverse=True)
        self.output(path)

    def action_one_path(self, message, audio_file):
        self.output(self.template_indent(1) + message)
        self.output(self.template_indent(2) + self.template_path(audio_file))
        self.output()

    def action_two_path(self, message, source, target):
        self.output(self.template_indent(1) + message)
        self.output(self.template_indent(2) + self.template_path(source))
        self.output(self.template_indent(2) + 'to')
        self.output(self.template_indent(2) + self.template_path(target))
        self.output()

    def diff(self, key, value1, value2):
        key_width = self.max_field + 2
        value2_indent = self.indent_width + key_width
        key += ':'

        def quote(value):
            return '“' + value + '”'

        value1 = quote(value1)
        value2 = quote(value2)
        self.output(' ' * self.indent_width + key.ljust(self.max_field + 2)
                    + value1)
        self.output(' ' * value2_indent + value2)


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
        self.msg = Message(job)

    def backup(self, audio_file):
        backup_file = AudioFile(audio_file.abspath + '.bak', type='target')
        self.msg.action_two_path('Backup', audio_file, backup_file)
        if not self.dry_run:
            shutil.move(audio_file.abspath, backup_file.abspath)

    def copy(self, source, target):
        self.msg.action_two_path('Copy', source, target)
        if not self.dry_run:
            shutil.copy2(source.abspath, target.abspath)

    def delete(self, audio_file):
        self.msg.action_one_path('Delete', audio_file)
        if not self.dry_run:
            os.remove(audio_file.abspath)

    def move(self, source, target):
        self.msg.action_two_path('Move', source, target)
        if not self.dry_run:
            shutil.move(source.abspath, target.abspath)

    def metadata(self, audio_file, enrich=False, remap=False):
        pre = audio_file.meta.export_dict()

        def single_action(audio_file, method_name, message):
            pre = audio_file.meta.export_dict()
            method = getattr(audio_file.meta, method_name)
            method()
            post = audio_file.meta.export_dict()
            diff = dict_diff(pre, post)
            self.msg.output(message)
            for change in diff:
                self.msg.diff(change[0], change[1], change[2])

        if enrich:
            single_action(audio_file, 'enrich_metadata', 'Enrich metadata')
        if remap:
            single_action(audio_file, 'remap_classical', 'Remap classical')

        post = audio_file.meta.export_dict()
        diff = dict_diff(pre, post)

        if not self.dry_run and len(diff) > 0:
            audio_file.meta.save()


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

    action = Action(job)
    msg = Message(job)

    source = AudioFile(source, prefix=os.getcwd(), file_type='source', job=job)
    msg.next_file(source)

    if not source.meta:
        skip = True

    ##
    # Skips
    ##

    if skip:
        msg.output(u'Broken file')
        return

    if job.field_skip and  \
       (
            not hasattr(source.meta, job.field_skip) or
            not getattr(source.meta, job.field_skip)
       ):
        msg.output(u'No field')
        count('no_field')
        return

    ##
    # Output only
    ##

    if job.output.mb_track_listing:
        print(mb_track_listing.format_audiofile(source.meta.album,
                                                source.meta.title,
                                                source.meta.length))
        return

    if job.output.debug:
        phrydy.doc.Debug(
            source.abspath,
            Meta,
            Meta.fields,
            job.output.color,
        ).output()
        return

    ##
    # Metadata actions
    ##

    if job.metadata_actions.remap_classical or \
            job.metadata_actions.enrich_metadata:
        action.metadata(
            source,
            job.metadata_actions.enrich_metadata,
            job.metadata_actions.remap_classical
        )

    ##
    # Rename action
    ##

    if job.rename.move != 'no_rename':

        if source.meta.soundtrack:
            format_string = job.format.soundtrack
        elif source.meta.comp:
            format_string = job.format.compilation
        else:
            format_string = job.format.default

        meta_dict = source.meta.export_dict()

        target = process_target_path(meta_dict, format_string,
                                     job.shell_friendly)

        target = AudioFile(os.path.join(job.target,
                           target + '.' + source.extension),
                           prefix=job.target, file_type='target', job=job)

        existing_target = get_target(target.abspath, job.filter.extension)

        if not existing_target:
            create_dir(target.abspath)
            if job.rename.move == u'copy':
                action.copy(source, target)
            else:
                action.move(source, target)
        elif target.abspath == source.abspath:
            msg.output(u'Renamed')
            count('renamed')
        else:
            msg.output(u'Exists')
            count('exists')
            if job.rename.cleanup == 'delete':
                meta_target = Meta(existing_target)
                best_format(source.meta, meta_target)
                action.delete(source)
