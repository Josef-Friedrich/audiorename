"""Collect all informations about the current job in a class."""

import os
import time
import typing
import configparser

from .message import Message
from .args import ArgsDefault


class Timer:

    begin: float = 0

    end: float = 0

    def start(self):
        self.begin = time.time()

    def stop(self):
        self.end = time.time()

    def result(self) -> str:
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
            if getattr(job.args, option) is not None:
                attr = getattr(job.args, option)
            elif job.config:
                try:
                    if data_type == 'boolean':
                        attr = job.config.getboolean(section, option)
                    elif data_type == 'integer':
                        attr = job.config.getint(section, option)
                    else:
                        attr = job.config.get(section, option)
                except configparser.NoOptionError:
                    pass

            if attr is not None:
                setattr(self, '_' + option, attr)


class SelectionConfig(Config):

    _source: typing.Optional[str]
    _target: typing.Optional[str]
    _source_as_target: typing.Optional[bool]

    @property
    def source(self) -> str:
        """The source path as an absolute path. It maybe a directory or a
        file."""
        source: str
        if hasattr(self, '_source') and self._source:
            source = self._source
        else:
            source = '.'
        return os.path.abspath(source)

    @property
    def target(self) -> typing.Optional[str]:
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
        if hasattr(self, '_source_as_target') and \
           isinstance(self._source_as_target, bool):
            return self._source_as_target
        return False


MoveAction = typing.Literal['move', 'copy', 'no_rename']
CleaningAction = typing.Literal['backup', 'delete', 'do_nothing']


class RenameConfig(Config):

    _backup_folder: typing.Optional[str]
    _best_format: typing.Optional[bool]
    _dry_run: typing.Optional[bool]
    _move_action: typing.Optional[MoveAction]
    _cleaning_action: typing.Optional[CleaningAction]

    @property
    def backup_folder(self) -> str:
        if hasattr(self, '_backup_folder') and \
                isinstance(self._backup_folder, str):
            return self._backup_folder
        return os.path.join(os.getcwd(), '_audiorename_backups')

    @property
    def best_format(self) -> bool:
        if hasattr(self, '_best_format') and \
                isinstance(self._best_format, bool):
            return self._best_format
        return True

    @property
    def dry_run(self) -> bool:
        if hasattr(self, '_dry_run') and \
                isinstance(self._dry_run, bool):
            return self._dry_run
        return False

    @property
    def move_action(self) -> MoveAction:
        if hasattr(self, '_move_action') and \
                self._move_action in ['move', 'copy', 'no_rename']:
            return self._move_action
        return 'move'

    @property
    def cleaning_action(self) -> CleaningAction:
        if hasattr(self, '_cleaning_action') and \
                self._cleaning_action in ['backup', 'delete', 'do_nothing']:
            return self._cleaning_action
        return 'do_nothing'


class FiltersConfig(Config):

    _album_complete: typing.Optional[bool]
    _album_min: typing.Optional[int]
    _extension: typing.Optional[str]
    _genre_classical: typing.Optional[str]
    _field_skip: typing.Optional[str]

    @property
    def album_complete(self) -> bool:
        if hasattr(self, '_album_complete') and \
                isinstance(self._album_complete, bool):
            return self._album_complete
        return False

    @property
    def album_min(self) -> typing.Optional[int]:
        if hasattr(self, '_album_min') and isinstance(self._album_min, int):
            return self._album_min

    @property
    def extension(self) -> typing.List[str]:
        extension: str
        if hasattr(self, '_extension') and isinstance(self._extension, str):
            extension = self._extension
        else:
            extension = 'mp3,m4a,flac,wma'
        return extension.split(',')

    @property
    def genre_classical(self) -> typing.List[str]:
        genre_classical: str
        if hasattr(self, '_genre_classical') and \
                isinstance(self._genre_classical, str):
            genre_classical = self._genre_classical
        else:
            genre_classical = ','
        return list(
            filter(str.strip,
                   genre_classical.lower().split(',')))

    @property
    def field_skip(self) -> typing.Optional[str]:
        if hasattr(self, '_field_skip') and \
                isinstance(self._field_skip, str):
            return self._field_skip


class TemplateSettingsConfig(Config):

    _classical: typing.Optional[bool]
    _shell_friendly: typing.Optional[bool]
    _no_soundtrack: typing.Optional[bool]

    @property
    def classical(self) -> bool:
        if hasattr(self, '_classical') and isinstance(self._classical, bool):
            return self._classical
        return False

    @property
    def shell_friendly(self) -> bool:
        if hasattr(self, '_shell_friendly') and \
                isinstance(self._shell_friendly, bool):
            return self._shell_friendly
        return False

    @property
    def no_soundtrack(self) -> bool:
        if hasattr(self, '_no_soundtrack') and \
                isinstance(self._no_soundtrack, bool):
            return self._no_soundtrack
        return False


class PathTemplatesConfig(Config):
    """A class to store the selected or configured path templates. This class
    can be accessed under the attibute path_templates of the Job class."""

    _default_template: typing.Optional[str]
    _compilation_template: typing.Optional[str]
    _soundtrack_template: typing.Optional[str]
    _classical_template: typing.Optional[str]

    @property
    def _is_classical(self) -> bool:
        return self._job.template_settings.classical

    @property
    def default(self) -> str:
        """Get the default path template."""
        if self._is_classical:
            return self.classical
        if hasattr(self, '_default_template') and \
                isinstance(self._default_template, str):
            return self._default_template
        return '$ar_initial_artist/' \
            '%shorten{$ar_combined_artist_sort}/' \
            '%shorten{$ar_combined_album}' \
            '%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/' \
            '${ar_combined_disctrack}_%shorten{$title}'

    @property
    def compilation(self) -> str:
        """Get the path template for compilations."""
        if self._is_classical:
            return self.classical
        if hasattr(self, '_compilation_template') and \
                isinstance(self._compilation_template, str):
            return self._compilation_template
        return '_compilations/' \
            '$ar_initial_album/' \
            '%shorten{$ar_combined_album}' \
            '%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/' \
            '${ar_combined_disctrack}_%shorten{$title}'

    @property
    def soundtrack(self) -> str:
        """Get the path template for soundtracks."""
        if self._is_classical:
            return self.classical
        if self._job.template_settings.no_soundtrack:
            return self.default
        if hasattr(self, '_soundtrack_template') and \
                isinstance(self._soundtrack_template, str):
            return self._soundtrack_template
        return '_soundtrack/' \
            '$ar_initial_album/' \
            '%shorten{$ar_combined_album}' \
            '%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/' \
            '${ar_combined_disctrack}_${artist}_%shorten{$title}'

    @property
    def classical(self) -> str:
        """Get the path template for classical music."""
        if hasattr(self, '_classical_template') and \
                isinstance(self._classical_template, str):
            return self._classical_template
        return '$ar_initial_composer/$ar_combined_composer/' \
            '%shorten{$ar_combined_work_top,48}' \
            '_[%shorten{$ar_classical_performer,32}]/' \
            '${ar_combined_disctrack}_%shorten{$ar_classical_title,64}' \
            '%ifdefnotempty{acoustid_id,_%shorten{$acoustid_id,8}}'


class CliOutputConfig(Config):

    _color: typing.Optional[bool]
    _debug: typing.Optional[bool]
    _job_info: typing.Optional[bool]
    _mb_track_listing: typing.Optional[bool]
    _one_line: typing.Optional[bool]
    _stats: typing.Optional[bool]
    _verbose: typing.Optional[bool]

    @property
    def color(self) -> bool:
        if hasattr(self, '_color') and isinstance(self._color, bool):
            return self._color
        return True

    @property
    def debug(self) -> bool:
        if hasattr(self, '_debug') and isinstance(self._debug, bool):
            return self._debug
        return False

    @property
    def job_info(self) -> bool:
        if hasattr(self, '_job_info') and isinstance(self._job_info, bool):
            return self._job_info
        return False

    @property
    def mb_track_listing(self) -> bool:
        if hasattr(self, '_mb_track_listing') and \
           isinstance(self._mb_track_listing, bool):
            return self._mb_track_listing
        return False

    @property
    def one_line(self) -> bool:
        if hasattr(self, '_one_line') and isinstance(self._one_line, bool):
            return self._one_line
        return False

    @property
    def stats(self) -> bool:
        if hasattr(self, '_stats') and isinstance(self._stats, bool):
            return self._stats
        return False

    @property
    def verbose(self) -> bool:
        if hasattr(self, '_verbose') and isinstance(self._verbose, bool):
            return self._verbose
        return False


class MetadataActionsConfig(Config):

    _enrich_metadata: typing.Optional[bool]
    _remap_classical: typing.Optional[bool]

    @property
    def enrich_metadata(self) -> bool:
        if hasattr(self, '_enrich_metadata') and \
                isinstance(self._enrich_metadata, bool):
            return self._enrich_metadata
        return False

    @property
    def remap_classical(self) -> bool:
        if hasattr(self, '_remap_classical') and \
                isinstance(self._remap_classical, bool):
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

    args: ArgsDefault
    config: typing.Optional[configparser.ConfigParser] = None

    def __init__(self, args: ArgsDefault):
        self.args = args
        if args.config is not None:
            self.config = self.__read_config(args.config)

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
            'source_as_target': 'boolean'
        })

    @property
    def rename(self) -> RenameConfig:
        return RenameConfig(self, 'rename', {
            'backup_folder': 'string',
            'best_format': 'boolean',
            'dry_run': 'boolean',
            'move_action': 'string',
            'cleaning_action': 'string',
        })

    @property
    def filters(self) -> FiltersConfig:
        return FiltersConfig(self, 'filters', {
            'album_complete': 'boolean',
            'album_min': 'integer',
            'extension': 'string',
            'genre_classical': 'string',
            'field_skip': 'string'
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
            'default_template': 'string',
            'compilation_template': 'string',
            'soundtrack_template': 'string',
            'classical_template': 'string',
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
