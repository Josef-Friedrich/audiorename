"""This module contains all functionality on the level of a single audio file.
"""

import errno
import os
import re
import shutil
import traceback
import typing

import phrydy
from tmep import Functions, Template

from .job import Job
from .meta import Meta, compare_dicts


DestinationType = typing.Literal['source', 'target']


class AudioFile:
    """
    :param path: The path string of the audio file.
    :param job: The current `job` object.
    :param string file_type: Either “source” or “target”.
    :param string prefix: The path prefix of the audio file, for example the
        base folder of your music collection. Used to shorten the path strings
        in the progress messaging.
    """

    def __init__(self, path: str, job: Job,
                 file_type: DestinationType = 'source',
                 prefix=None):
        self.__path = path
        self.type = file_type
        self.job = job
        self.__prefix = prefix
        self.shorten_symbol = '[…]'

    @property
    def shell_friendly(self):
        if not self.job:
            return True
        else:
            return self.job.template_settings.shell_friendly

    @property
    def meta(self) -> typing.Optional[Meta]:
        if self.exists:
            try:
                return Meta(self.abspath, self.shell_friendly)
            except Exception as e:
                tb = traceback.TracebackException.from_exception(e)
                print(''.join(tb.stack.format()))

    @property
    def abspath(self) -> str:
        """The absolute path of the audio file."""
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
    def extension(self) -> str:
        """The file extension of the audio file."""
        return self.abspath.split('.')[-1].lower()

    @property
    def short(self) -> str:
        if self.prefix:
            short = self.abspath.replace(self.prefix, '')
        else:
            short = os.path.basename(self.abspath)

        return self.shorten_symbol + short

    @property
    def filename(self) -> str:
        """The file name of the audio file."""
        return os.path.basename(self.abspath)

    @property
    def dir_and_file(self) -> str:
        """The parent directory name and the file name."""
        path_segments = self.abspath.split(os.path.sep)
        return os.path.sep.join(path_segments[-2:])


class MBTrackListing:

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


def find_target_path(target: str,
                     extensions: typing.List[str]) -> typing.Optional[str]:
    """Get the path of a existing audio file target. Search for audio files
    with different extensions.
    """
    target = os.path.splitext(target)[0]
    for extension in extensions:
        audio_file = target + '.' + extension
        if os.path.exists(audio_file):
            return audio_file


def detect_best_format(source: Meta, target: Meta,
                       job: Job) -> DestinationType:
    """
    :param source: The metadata object of the source file.
    :param target: The metadata object of the target file.
    :param job: The `job` object.

    :return: Either the string `source` or the string `target`
    """
    def get_highest(dictionary: typing.Dict[typing.Any, DestinationType]
                    ) -> DestinationType:
        out: DestinationType = 'target'
        for _, value in sorted(dictionary.items()):
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
        types[ranking[source.type] if source.type in ranking else 0] = 'source'
        types[ranking[target.type] if target.type in ranking else 0] = 'target'
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
    template = Template(format_string)
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


class Action:
    """
    :param job: The `job` object.
    :type job: audiorename.job.Job
    """

    def __init__(self, job):
        self.job = job
        self.dry_run = job.rename.dry_run

    def count(self, counter_name):
        self.job.stats.counter.count(counter_name)

    def cleanup(self, audio_file):
        if self.job.rename.cleaning_action == 'backup':
            self.backup(audio_file)
        elif self.job.rename.cleaning_action == 'delete':
            self.delete(audio_file)

    def backup(self, audio_file):
        backup_file = AudioFile(
            os.path.join(
                self.job.rename.backup_folder,
                os.path.basename(audio_file.abspath)
            ), job=self.job, file_type='target'
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

    def metadata(self, audio_file: AudioFile, enrich: bool = False,
                 remap: bool = False) -> None:
        if not audio_file.meta:
            raise Exception('The given audio file has no meta property.')
        meta = audio_file.meta
        pre = meta.export_dict(sanitize=False)

        def single_action(meta: Meta,
                          method_name: typing.Literal['enrich_metadata',
                                                      'remap_classical'],
                          message: str):
            pre = meta.export_dict(sanitize=False)
            method = getattr(meta, method_name)
            method()
            post = meta.export_dict(sanitize=False)
            diff = compare_dicts(pre, post)
            if diff:
                self.count(method_name)
            self.job.msg.output(message)
            for change in diff:
                self.job.msg.diff(change[0], change[1], change[2])

        if enrich:
            single_action(meta, 'enrich_metadata', 'Enrich metadata')
        if remap:
            single_action(meta, 'remap_classical', 'Remap classical')

        post = meta.export_dict(sanitize=False)
        diff = compare_dicts(pre, post)

        if not self.dry_run and diff:
            meta.save()


def do_job_on_audiofile(source_path: str, job: Job):
    def count(key):
        job.stats.counter.count(key)
    skip = False

    action = Action(job)

    source = AudioFile(source_path, job=job, prefix=os.getcwd(),
                       file_type='source')
    if not job.cli_output.mb_track_listing:
        job.msg.next_file(source)

    if not source.meta:
        skip = True

    ##
    # Skips
    ##

    if skip:
        job.msg.status('Broken file', status='error')
        count('broken_file')
        return

    ##
    # Output only
    ##

    if not source.meta:
        raise Exception('source.meta must not be empty.')

    if job.cli_output.mb_track_listing:
        print(mb_track_listing.format_audiofile(source.meta.album,
                                                source.meta.title,
                                                source.meta.length))
        return

    if job.cli_output.debug:
        phrydy.print_debug(
            source.abspath,
            Meta,
            Meta.fields,
            job.cli_output.color,
        )
        return

    if job.filters.field_skip and (not hasattr(source.meta,
       job.filters.field_skip) or not getattr(source.meta,
       job.filters.field_skip)):
        job.msg.status('No field', status='error')
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

    if source.meta.genre is not None and \
       getattr(source.meta, "genre", "").lower() in \
       job.filters.genre_classical:

        if not job.metadata_actions.remap_classical:
            action.metadata(
                source,
                job.metadata_actions.enrich_metadata,
                True
            )

    ##
    # Rename action
    ##

    if job.rename.move_action != 'no_rename':

        if source.meta.genre is not None and \
           getattr(source.meta, "genre", "").lower() \
           in job.filters.genre_classical:
            format_string = job.path_templates.classical
        elif source.meta.ar_combined_soundtrack:
            if job.args.no_soundtrack and source.meta.comp:
                format_string = job.path_templates.compilation
            else:
                format_string = job.path_templates.soundtrack
        elif source.meta.comp:
            format_string = job.path_templates.compilation
        else:
            format_string = job.path_templates.default

        meta_dict = source.meta.export_dict()

        desired_target_path = process_target_path(
            meta_dict, format_string,
            job.template_settings.shell_friendly
        )

        # Remove the leading path separator to prevent the audio files from
        # ending up in a folder other than the target folder.
        desired_target_path = re.sub(r'^' + os.path.sep + r'+', '',
                                     desired_target_path)
        desired_target_path = os.path.join(
            job.selection.target,
            desired_target_path + '.' + source.extension
        )

        desired_target = AudioFile(desired_target_path, job=job,
                                   prefix=job.selection.target,
                                   file_type='target')

        # Do nothing
        if source.abspath == desired_target.abspath:
            job.msg.status('Renamed', status='ok')
            count('renamed')
            return

        # Search existing target
        target = False
        target_path = find_target_path(desired_target.abspath,
                                       job.filters.extension)
        if target_path:
            target = AudioFile(target_path, job=job,
                               prefix=job.selection.target,
                               file_type='target')

        # Both file exist
        if target:
            if not target.meta:
                raise Exception('target.meta must not be empty.')
            best = detect_best_format(source.meta, target.meta, job)

            if job.rename.cleaning_action:

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
        elif job.rename.move_action == 'copy':
            action.copy(source, desired_target)

        # move
        elif job.rename.move_action == 'move':
            action.move(source, desired_target)
