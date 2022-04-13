"""Collect all informations about the current job in a class."""

from audiorename.message import Message
from collections import namedtuple
import os
import time
import typing


class Timer:

    begin = 0

    end = 0

    def start(self):
        self.begin = time.time()

    def stop(self):
        self.end = time.time()

    def result(self):
        return '{:.1f}s'.format(self.end - self.begin)


class Counter:

    def __init__(self):
        self._counters: typing.Dict[str, int] = {}

    def reset(self):
        self._counters = {}

    def count(self, counter: str):
        """Add one to number identified by a string.

        :param counter: A string to identify the counter

        :return: None
        """
        if counter in self._counters:
            self._counters[counter] += 1
        else:
            self._counters[counter] = 1

    def get(self, counter: str) -> int:
        """Get the counter identify by a string.

        :param str counter: A string to identify the counter

        :return: The counter as a number
        :rtype: int
        """

        if counter in self._counters:
            return self._counters[counter]
        else:
            return 0

    def result(self) -> str:
        out: typing.List[str] = []
        for counter, value in sorted(self._counters.items()):
            out.append(counter + '=' + str(value))

        if out:
            return ' '.join(out)
        else:
            return 'Nothing to count!'


class Stats:

    counter = Counter()
    timer = Timer()


class DefaultFormats:

    default = '$ar_initial_artist/' \
              '%shorten{$ar_combined_artist_sort}/' \
              '%shorten{$ar_combined_album}' \
              '%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/' \
              '${ar_combined_disctrack}_%shorten{$title}'

    compilation = '_compilations/' \
                  '$ar_initial_album/' \
                  '%shorten{$ar_combined_album}' \
                  '%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/' \
                  '${ar_combined_disctrack}_%shorten{$title}'

    soundtrack = '_soundtrack/' \
                 '$ar_initial_album/' \
                 '%shorten{$ar_combined_album}' \
                 '%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/' \
                 '${ar_combined_disctrack}_${artist}_%shorten{$title}'

    classical = '$ar_initial_composer/$ar_combined_composer/' \
                '%shorten{$ar_combined_work_top,48}' \
                '_[%shorten{$ar_classical_performer,32}]/' \
                '${ar_combined_disctrack}_%shorten{$ar_classical_title,64}' \
                '%ifdefnotempty{acoustid_id,_%shorten{$acoustid_id,8}}'


class Formats:

    default: str = ''
    compilation: str = ''
    soundtrack: str = ''
    classical: str = ''

    def __init__(self, args):
        defaults = DefaultFormats()

        if args.format:
            defaults.default = args.format

        if args.compilation:
            defaults.compilation = args.compilation

        if args.soundtrack:
            defaults.soundtrack = args.soundtrack

        if args.format_classical:
            defaults.classical = args.format_classical

        self.classical = defaults.classical

        if args.classical:
            self.default = defaults.classical
            self.compilation = defaults.classical
            self.soundtrack = defaults.classical
        else:
            self.default = defaults.default
            self.compilation = defaults.compilation
            self.soundtrack = defaults.soundtrack


class RenameAction:

    def __init__(self, args):
        self._args = args
        self.best_format = args.best_format

    @property
    def backup_folder(self):
        if self._args.backup_folder:
            return self._args.backup_folder
        else:
            return os.path.join(os.getcwd(), '_audiorename_backups')

    @property
    def cleanup(self):
        if self._args.backup:
            return 'backup'
        elif self._args.delete:
            return 'delete'
        else:
            return False

    @property
    def move(self):
        """
        :return:

        :rtype: string

        * copy
        * move
        * no_rename
        """
        if self._args.copy:
            return 'copy'
        elif self._args.move:
            return 'move'
        elif self._args.no_rename:
            return 'no_rename'
        else:
            return 'move'


class Job:
    """Holds informations of one job which can handle multiple files.

    A jobs represents one call of the program on the command line.
    This class unifies and processes the data of the `argparse` call. It groups
    the `argparse` key value pairs into parent properties. The properties of
    this class for example can be used to display easily an overview message of
    the job.
    """

    stats = Stats()

    def __init__(self, args):
        self._args = args

        self.field_skip = args.field_skip
        self.shell_friendly = args.shell_friendly
        self.rename = RenameAction(args)
        self.dry_run = args.dry_run
        self.msg = Message(self)

    @property
    def filter(self):
        Filter = namedtuple('Filter', [
            'album_complete',
            'album_min',
            'extension',
            'genre_classical'
        ])

        return Filter(
            self._args.album_complete,
            self._args.album_min,
            self._args.extension.split(','),
            list(filter(str.strip,
                 self._args.genre_classical.lower().split(',')))
        )

    @property
    def format(self):
        """
        default
        compilation
        soundtrack
        """
        return Formats(self._args)

    @property
    def metadata_actions(self):
        MetadataActions = namedtuple('MetadataAction', [
            'enrich_metadata',
            'remap_classical',
        ])

        return MetadataActions(
            self._args.enrich_metadata,
            self._args.remap_classical,
        )
        pass

    @property
    def output(self):
        Output = namedtuple('Output', [
            'color',
            'debug',
            'job_info',
            'mb_track_listing',
            'one_line',
            'stats',
            'verbose',
        ])

        self._args.color = self._args.no_color is not True

        return Output(
            self._args.color,
            self._args.debug,
            self._args.job_info,
            self._args.mb_track_listing,
            self._args.one_line,
            self._args.stats,
            self._args.verbose,
        )

    @property
    def source(self):
        """The source path as an absolute path. It maybe a directory or a
        file."""
        return os.path.abspath(self._args.source)

    @property
    def target(self):
        """The path of the target as an absolute path. It is always a
        directory.
        """
        if self._args.source_as_target:
            if os.path.isdir(self.source):
                return os.path.abspath(self.source)
            else:
                return os.path.abspath(os.path.dirname(self.source))
        elif self._args.target:
            return os.path.abspath(self._args.target)
        else:
            return os.getcwd()
