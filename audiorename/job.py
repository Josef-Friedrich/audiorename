"""Collect all informations about the current job in a class."""

import os
import time
import typing
import configparser
import argparse

from .message import Message
from .args import ArgsDefault


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


class Statistic:

    counter = Counter()
    timer = Timer()


class DefaultFormat:
    """A class to store the default format strings."""

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


class Format:
    """A class to store the selected or configured format strings. This class
    can be accessed under the attibute format of the Job class."""

    default: str = ''
    """Store the default format string."""

    compilation: str = ''
    """Store the format string for compilations."""

    soundtrack: str = ''
    """Store the format string for soundtracks."""

    classical: str = ''
    """Store the format string for classical music."""

    def __init__(self, args: ArgsDefault):
        defaults = DefaultFormat()

        if args.format:
            defaults.default = args.format

        if args.compilation:
            defaults.compilation = args.compilation

        if args.soundtrack:
            defaults.soundtrack = args.soundtrack

        if args.no_soundtrack:
            defaults.soundtrack = defaults.default

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


class Config:

    _options = None

    def __init__(self, args: argparse.Namespace,
                 config: configparser.ConfigParser,
                 section: str, options: dict):
        self._options = options
        for option, data_type in options.items():
            attr = None
            if getattr(args, option) is not None:
                attr = getattr(args, option)
            elif config:
                try:
                    if data_type == 'boolean':
                        attr = config.getboolean(section, option)
                    elif data_type == 'integer':
                        attr = config.getint(section, option)
                    else:
                        attr = config.get(section, option)
                except configparser.NoOptionError:
                    pass

            if attr is not None:
                setattr(self, option, attr)

    def _debug(self):
        for option, data_type in self._options.items():
            value = getattr(self, option)
            print(option + ' ' + str(value) + ' ' + type(value).__name__)


class SelectionConfig(Config):
    source = '.'
    target = None
    source_as_target = False


class OutputConfig(Config):
    color = True
    debug = False
    job_info = False
    mb_track_listing = False
    one_line = False
    stats = False
    verbose = False


class MetadataActionsConfig(Config):
    enrich_metadata = False
    remap_classical = False


class FilterConfig(Config):
    album_complete = False
    album_min = False
    extension = 'mp3,m4a,flac,wma'
    genre_classical = ','

    def __init__(self, args: argparse.Namespace,
                 config: configparser.ConfigParser,
                 section: str, options: dict):
        super().__init__(args, config, section, options)
        self.genre_classical = list(
            filter(str.strip,
                   self.genre_classical.lower().split(',')))
        self.extension = self.extension.split(',')


class RenameConfig(Config):
    backup_folder = None
    best_format = True
    move_action = 'move'
    cleaning_action = 'do_nothing'

    def __init__(self, args: argparse.Namespace,
                 config: configparser.ConfigParser,
                 section: str, options: dict):
        super().__init__(args, config, section, options)
        if not self.backup_folder:
            self.backup_folder = os.path.join(
                os.getcwd(), '_audiorename_backups')


class Job:
    """Holds informations of one job which can handle multiple files.

    A jobs represents one call of the program on the command line. This class
    unifies and processes the data of the `argparse` and the `configparser`
    call. It groups the `argparse` and the `configparser` key-value pairs into
    parent properties. The properties of this class for example can be used to
    display easily an overview message of the job.
    """

    stats = Statistic()

    _config = None

    cli_output = None

    metadata_actions = None

    rename = None

    filters = None

    selection = None

    def __init__(self, args: ArgsDefault):
        self._args = args
        if args.config is not None:
            self._config = self.__read_config(args.config)

        self.selection = SelectionConfig(
            self._args, self._config,
            'selection', {
                'source': 'string',
                'target': 'string',
                'source_as_target': 'string'
            })

        self.metadata_actions = MetadataActionsConfig(
            self._args, self._config,
            'metadata_actions', {
                'enrich_metadata': 'boolean',
                'remap_classical': 'boolean',
            })

        self.cli_output = OutputConfig(self._args, self._config, 'cli_output',
                                       {
                                           'color': 'boolean',
                                           'debug': 'boolean',
                                           'job_info': 'boolean',
                                           'mb_track_listing': 'boolean',
                                           'one_line': 'boolean',
                                           'stats': 'boolean',
                                           'verbose': 'boolean',
                                       })

        self.filters = FilterConfig(self._args, self._config, 'filters', {
            'album_complete': 'boolean',
            'album_min': 'boolean',
            'extension': 'string',
            'genre_classical': 'string',
        })

        self.rename = RenameConfig(self._args, self._config, 'rename', {
            'backup_folder': 'string',
            'best_format': 'boolean',
            'move_action': 'string',
            'cleaning_action': 'string',
        })

        self.field_skip = args.field_skip
        self.shell_friendly = args.shell_friendly
        self.dry_run = args.dry_run
        self.msg = Message(self)

    def __read_config(self, file_path: str) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(file_path)
        return config

    @property
    def format(self) -> Format:
        return Format(self._args)

    @property
    def source(self) -> str:
        """The source path as an absolute path. It maybe a directory or a
        file."""
        return os.path.abspath(self.selection.source)

    @property
    def target(self) -> str:
        """The path of the target as an absolute path. It is always a
        directory.
        """
        if self.selection.source_as_target:
            if os.path.isdir(self.source):
                return os.path.abspath(self.source)
            else:
                return os.path.abspath(os.path.dirname(self.source))
        elif self.selection.target:
            return os.path.abspath(self.selection.target)
        else:
            return os.getcwd()
