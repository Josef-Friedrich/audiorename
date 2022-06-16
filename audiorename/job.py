"""Collect all informations about the current job in a class."""

import os
import time
import typing
import configparser

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


class Config:
    """The class ``Config`` is used to combine the two sources of settings
    (command line arguments and INI configuration file). The command line
    arguments override the values of the configuration file. This class is to
    be inherited by subclasses. Each subclass corresponds to a section of the
    INI configuration file. All settings are saved as private properties with
    leading underscore. The subclass provide  for each private property a
    getter method (@property)"""

    _job: 'Job'

    def __init__(self, job: 'Job', section: str,
                 options: typing.Dict[str, typing.Literal['boolean',
                                                          'integer',
                                                          'string']]):
        self._job = job
        for option, data_type in options.items():
            attr = None
            if getattr(job._args, option) is not None:
                attr = getattr(job._args, option)
            elif job._config:
                try:
                    if data_type == 'boolean':
                        attr = job._config.getboolean(section, option)
                    elif data_type == 'integer':
                        attr = job._config.getint(section, option)
                    else:
                        attr = job._config.get(section, option)
                except configparser.NoOptionError:
                    pass

            if attr is not None:
                setattr(self, '_' + option, attr)


class SelectionConfig(Config):

    @property
    def source(self) -> str:
        """The source path as an absolute path. It maybe a directory or a
        file."""
        source: str
        if hasattr(self, '_source'):
            source = self._source
        else:
            source = '.'
        return os.path.abspath(source)

    @property
    def target(self) -> typing.Union[None, str]:
        """The path of the target as an absolute path. It is always a
        directory.
        """
        target: typing.Union[None, str] = None
        if hasattr(self, '_target'):
            target = self._target

        if self.source_as_target:
            if os.path.isdir(self.source):
                return os.path.abspath(self.source)
            else:
                return os.path.abspath(os.path.dirname(self.source))
        elif target:
            return os.path.abspath(target)
        else:
            return os.getcwd()

    @property
    def source_as_target(self) -> bool:
        if hasattr(self, '_source_as_target'):
            return self._source_as_target
        return False


class RenameConfig(Config):

    @property
    def backup_folder(self) -> str:
        if hasattr(self, '_backup_folder'):
            return self._backup_folder
        return os.path.join(os.getcwd(), '_audiorename_backups')

    @property
    def best_format(self) -> bool:
        if hasattr(self, '_best_format'):
            return self._best_format
        return True

    @property
    def move_action(self) -> typing.Literal['move', 'copy', 'no_rename']:
        if hasattr(self, '_move_action'):
            return self._move_action
        return 'move'

    @property
    def cleaning_action(self) -> typing.Literal['backup', 'delete',
                                                'do_nothing']:
        if hasattr(self, '_cleaning_action'):
            return self._cleaning_action
        return 'do_nothing'


class FiltersConfig(Config):

    @property
    def album_complete(self) -> bool:
        if hasattr(self, '_album_complete'):
            return self._album_complete
        return False

    @property
    def album_min(self) -> typing.Union[int, None]:
        if hasattr(self, '_album_min'):
            return self._album_min

    @property
    def extension(self) -> typing.List[str]:
        extension: str
        if hasattr(self, '_extension'):
            extension = self._extension
        else:
            extension = 'mp3,m4a,flac,wma'
        return extension.split(',')

    @property
    def genre_classical(self) -> typing.List[str]:
        genre_classical: str
        if hasattr(self, '_genre_classical'):
            genre_classical = self._genre_classical
        else:
            genre_classical = ','
        return list(
            filter(str.strip,
                   genre_classical.lower().split(',')))


class TemplateSettingsConfig(Config):

    @property
    def classical(self) -> bool:
        if hasattr(self, '_classical'):
            return self._classical
        return False

    @property
    def shell_friendly(self) -> bool:
        if hasattr(self, '_shell_friendly'):
            return self._shell_friendly
        return False

    @property
    def no_soundtrack(self) -> bool:
        if hasattr(self, '_no_soundtrack'):
            return self._no_soundtrack
        return False


class PathTemplatesConfig(Config):
    """A class to store the selected or configured path templates. This class
    can be accessed under the attibute path_templates of the Job class."""

    @property
    def _is_classical(self) -> bool:
        return self._job.template_settings.classical

    @property
    def default(self) -> str:
        """Get the default path template."""
        if self._is_classical:
            return self.format_classical
        if hasattr(self, '_default'):
            return self._default
        return '$ar_initial_artist/' \
            '%shorten{$ar_combined_artist_sort}/' \
            '%shorten{$ar_combined_album}' \
            '%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/' \
            '${ar_combined_disctrack}_%shorten{$title}'

    @property
    def compilation(self) -> str:
        """Get the path template for compilations."""
        if self._is_classical:
            return self.format_classical
        if hasattr(self, '_compilation'):
            return self._compilation
        return '_compilations/' \
            '$ar_initial_album/' \
            '%shorten{$ar_combined_album}' \
            '%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/' \
            '${ar_combined_disctrack}_%shorten{$title}'

    @property
    def soundtrack(self) -> str:
        """Get the path template for soundtracks."""
        if self._is_classical:
            return self.format_classical
        if self._job.template_settings.no_soundtrack:
            return self.default
        if hasattr(self, '_soundtrack'):
            return self._soundtrack
        return '_soundtrack/' \
            '$ar_initial_album/' \
            '%shorten{$ar_combined_album}' \
            '%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/' \
            '${ar_combined_disctrack}_${artist}_%shorten{$title}'

    @property
    def format_classical(self) -> str:
        """Get the path template for classical music."""
        if hasattr(self, '_format_classical'):
            return self._format_classical
        return '$ar_initial_composer/$ar_combined_composer/' \
            '%shorten{$ar_combined_work_top,48}' \
            '_[%shorten{$ar_classical_performer,32}]/' \
            '${ar_combined_disctrack}_%shorten{$ar_classical_title,64}' \
            '%ifdefnotempty{acoustid_id,_%shorten{$acoustid_id,8}}'


class CliOutputConfig(Config):

    @property
    def color(self) -> bool:
        if hasattr(self, '_color'):
            return self._color
        return True

    @property
    def debug(self) -> bool:
        if hasattr(self, '_debug'):
            return self._debug
        return False

    @property
    def job_info(self) -> bool:
        if hasattr(self, '_job_info'):
            return self._job_info
        return False

    @property
    def mb_track_listing(self) -> bool:
        if hasattr(self, '_mb_track_listing'):
            return self._mb_track_listing
        return False

    @property
    def one_line(self) -> bool:
        if hasattr(self, '_one_line'):
            return self._one_line
        return False

    @property
    def stats(self) -> bool:
        if hasattr(self, '_stats'):
            return self._stats
        return False

    @property
    def verbose(self) -> bool:
        if hasattr(self, '_verbose'):
            return self._verbose
        return False


class MetadataActionsConfig(Config):

    @property
    def enrich_metadata(self) -> bool:
        if hasattr(self, '_enrich_metadata'):
            return self._enrich_metadata
        return False

    @property
    def remap_classical(self) -> bool:
        if hasattr(self, '_remap_classical'):
            return self._remap_classical
        return False


class Job:
    """Holds informations of one job which can handle multiple files.

    A jobs represents one call of the program on the command line. This class
    unifies and processes the data of the `argparse` and the `configparser`
    call. It groups the `argparse` and the `configparser` key-value pairs into
    parent properties. The properties of this class for example can be used to
    display easily an overview message of the job.
    """

    stats = Statistic()

    _args: ArgsDefault
    _config: configparser.ConfigParser = None

    def __init__(self, args: ArgsDefault):
        self._args = args
        if args.config is not None:
            self._config = self.__read_config(args.config)

        self.field_skip = args.field_skip
        self.shell_friendly = args.shell_friendly
        self.dry_run = args.dry_run
        self.msg = Message(self)

    def __read_config(self, file_path: str) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(file_path)
        return config

    @property
    def selection(self) -> SelectionConfig:
        return SelectionConfig(self, 'selection', {
            'source': 'string',
            'target': 'string',
            'source_as_target': 'string'
        })

    @property
    def rename(self) -> RenameConfig:
        return RenameConfig(self, 'rename', {
            'backup_folder': 'string',
            'best_format': 'boolean',
            'move_action': 'string',
            'cleaning_action': 'string',
        })

    @property
    def filters(self) -> FiltersConfig:
        return FiltersConfig(self, 'filters', {
            'album_complete': 'boolean',
            'album_min': 'boolean',
            'extension': 'string',
            'genre_classical': 'string',
        })

    @property
    def template_settings(self) -> TemplateSettingsConfig:
        return TemplateSettingsConfig(self, 'template_settings', {
            'classical': 'boolean',
            'shell_friendly': 'boolean',
            'no_soundtrack': 'boolean',
        })

    @property
    def path_templates(self) -> PathTemplatesConfig:
        return PathTemplatesConfig(self, 'path_templates', {
            'default': 'string',
            'compilation': 'string',
            'soundtrack': 'string',
            'format_classical': 'string',
        })

    @property
    def cli_output(self) -> CliOutputConfig:
        return CliOutputConfig(self, 'cli_output', {
            'color': 'boolean',
            'debug': 'boolean',
            'job_info': 'boolean',
            'mb_track_listing': 'boolean',
            'one_line': 'boolean',
            'stats': 'boolean',
            'verbose': 'boolean',
        })

    @property
    def metadata_actions(self) -> MetadataActionsConfig:
        return MetadataActionsConfig(self, 'metadata_actions', {
            'enrich_metadata': 'boolean',
            'remap_classical': 'boolean',
        })
