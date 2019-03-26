"""This module contains all functionality on the level of a single audio file.
"""

from __future__ import print_function
from audiorename.meta import Meta, dict_diff
from phrydy.utils import as_string
from tmep import Functions
from tmep import Template
import errno
import os
import phrydy
import re
import shutil


class AudioFile(object):
    """
    :param path: The path string of the audio file.
    :param string file_type: Either “source” or “target”.
    :param string prefix: The path prefix of the audio file, for example the
        base folder of your music collection. Used to shorten the path strings
        in the progress messaging.
    :param job: The `job` object.
    :type job: audiorename.job.Job
    """
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


def get_target(target, extensions):
    """Get the path of a existing audio file target. Search for audio files
    with different extensions.
    """
    target = os.path.splitext(target)[0]
    for extension in extensions:
        audio_file = target + '.' + extension
        if os.path.exists(audio_file):
            return audio_file


def best_format(source, target, job):
    """
    :param source: The metadata object of the source file.
    :type source: audiorename.meta.Meta
    :param target: The metadata object of the target file.
    :type target: audiorename.meta.Meta
    :return: Either the string `source` or the string `target`
    :param job: The `job` object.
    :type job: audiorename.job.Job
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
        best = get_highest(bitrates)
        job.msg.best_format(best, 'bitrate', source, target)
        return best

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
        best = get_highest(types)
        job.msg.best_format(best, 'type', source, target)
        return best


def process_target_path(meta, format_string, shell_friendly=True):
    """
    :param dict meta: The to a dictionary converted attributes of a
        meta object :class:`audiorename.meta.Meta`.
    :param string format_string:
    :param boolean shell_friendly:
    """
    template = Template(as_string(format_string))
    functions = Functions(meta)
    target = template.substitute(meta, functions.functions())

    if isinstance(target, str):
        if shell_friendly:
            target = Functions.tmpl_asciify(target)
            target = Functions.tmpl_delchars(target, '().,!"\'’')
            target = Functions.tmpl_replchars(target, '-', ' ')
        # asciify generates new characters which must be sanitzed, e. g.:
        # ¿ -> ?
        target = Functions.tmpl_delchars(target, ':*?"<>|\\~&{}')
        target = Functions.tmpl_deldupchars(target)
    return re.sub(r'\.$', '', target)


class Action(object):
    """
    :param job: The `job` object.
    :type job: audiorename.job.Job
    """

    def __init__(self, job):
        self.job = job
        self.dry_run = job.dry_run

    def count(self, counter_name):
        self.job.stats.counter.count(counter_name)

    def cleanup(self, audio_file):
        if self.job.rename.cleanup == 'backup':
            self.backup(audio_file)
        elif self.job.rename.cleanup == 'delete':
            self.delete(audio_file)

    def backup(self, audio_file):
        backup_file = AudioFile(
            os.path.join(
                self.job.rename.backup_folder,
                os.path.basename(audio_file.abspath)
            ), file_type='target'
        )

        self.job.msg.action_two_path('Backup', audio_file, backup_file)
        self.count('backup')
        if not self.dry_run:
            self.create_dir(backup_file)
            shutil.move(audio_file.abspath, backup_file.abspath)

    def copy(self, source, target):
        self.job.msg.action_two_path('Copy', source, target)
        self.count('copy')
        if not self.dry_run:
            self.create_dir(target)
            shutil.copy2(source.abspath, target.abspath)

    def create_dir(self, audio_file):
        path = os.path.dirname(audio_file.abspath)

        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def delete(self, audio_file):
        self.job.msg.action_one_path('Delete', audio_file)
        self.count('delete')
        if not self.dry_run:
            os.remove(audio_file.abspath)

    def move(self, source, target):
        self.job.msg.action_two_path('Move', source, target)
        self.count('move')
        if not self.dry_run:
            self.create_dir(target)
            shutil.move(source.abspath, target.abspath)

    def metadata(self, audio_file, enrich=False, remap=False):
        pre = audio_file.meta.export_dict(sanitize=False)

        def single_action(audio_file, method_name, message):
            pre = audio_file.meta.export_dict(sanitize=False)
            method = getattr(audio_file.meta, method_name)
            method()
            post = audio_file.meta.export_dict(sanitize=False)
            diff = dict_diff(pre, post)
            if diff:
                self.count(method_name)
            self.job.msg.output(message)
            for change in diff:
                self.job.msg.diff(change[0], change[1], change[2])

        if enrich:
            single_action(audio_file, 'enrich_metadata', 'Enrich metadata')
        if remap:
            single_action(audio_file, 'remap_classical', 'Remap classical')

        post = audio_file.meta.export_dict(sanitize=False)
        diff = dict_diff(pre, post)

        if not self.dry_run and diff:
            audio_file.meta.save()


def do_job_on_audiofile(source, job=None):
    """
    :param job: The `job` object.
    :type job: audiorename.job.Job
    """
    def count(key):
        job.stats.counter.count(key)
    skip = False

    action = Action(job)

    source = AudioFile(source, prefix=os.getcwd(), file_type='source', job=job)
    if not job.output.mb_track_listing:
        job.msg.next_file(source)

    if not source.meta:
        skip = True

    ##
    # Skips
    ##

    if skip:
        job.msg.status(u'Broken file', status='error')
        count('broken_file')
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
        phrydy.doc.print_debug(
            source.abspath,
            Meta,
            Meta.fields,
            job.output.color,
        )
        return

    if job.field_skip and (not hasattr(source.meta,
       job.field_skip) or not getattr(source.meta, job.field_skip)):
        job.msg.status(u'No field', status='error')
        count('no_field')
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

        if source.meta.ar_combined_soundtrack:
            format_string = job.format.soundtrack
        elif source.meta.comp:
            format_string = job.format.compilation
        else:
            format_string = job.format.default

        meta_dict = source.meta.export_dict()

        desired_target_path = process_target_path(meta_dict, format_string,
                                                  job.shell_friendly)
        desired_target_path = os.path.join(
            job.target,
            desired_target_path + '.' + source.extension
        )

        desired_target = AudioFile(desired_target_path, prefix=job.target,
                                   file_type='target', job=job)

        # Do nothing
        if source.abspath == desired_target.abspath:
            job.msg.status('Renamed', status='ok')
            count('renamed')
            return

        # Search existing target
        target = False
        target_path = get_target(desired_target.abspath, job.filter.extension)
        if target_path:
            target = AudioFile(target_path, prefix=job.target,
                               file_type='target', job=job)

        # Both file exist
        if target:
            best = best_format(source.meta, target.meta, job)

            if job.rename.cleanup:

                # delete source
                if not job.rename.best_format or \
                   (job.rename.best_format and best == 'target'):
                    action.cleanup(source)

                # delete target
                if job.rename.best_format and best == 'source':
                    action.cleanup(target)

                    # Unset target object to trigger copy or move actions.
                    target = None

        if target:
            job.msg.status('Exists', status='error')

        # copy
        elif job.rename.move == 'copy':
            action.copy(source, desired_target)

        # move
        elif job.rename.move == 'move':
            action.move(source, desired_target)
