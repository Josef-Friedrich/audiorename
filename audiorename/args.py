"""Create the command line interface using the package “argparse”."""

from ._version import get_versions
import argparse
import typing
import phrydy
import tmep
import os

from .utils import indent, read_file

fields: phrydy.field_docs.FieldDocCollection = {
    'ar_classical_album': {
        'description': 'The field “work” without the movement suffix. '
                       'For example: “Horn Concerto: I. Allegro” -> '
                       '“Horn Concerto”',
        'category': 'common',
        'examples': ['Horn Concerto', 'Die Meistersinger von Nürnberg'],
    },
    'ar_classical_performer': {
        'description': '“ar_performer_short” or “albumartist” without the '
                       'composer prefix: “Beethoven; Karajan, Mutter” -> '
                       '“Karajan, Mutter”',
        'category': 'common',
        'examples': ['Karajan, Mutter', 'Karajan, StaDre'],
        'data_type': 'str',
    },
    'ar_classical_title': {
        'description': 'The movement title without the parent work prefix. '
                       'For example “Horn Concerto: I. Allegro” -> '
                       '“I. Allegro”',
        'category': 'common',
        'examples': ['I. Allegro',
                     'Akt III, Szene V. "Morgendlich leuchtend im rosigen '
                     'Schein" (Walther, Volk, Meister, Sachs, Pogner, Eva)'],
        'data_type': 'str',
    },
    'ar_classical_track': {
        'description': 'If the title contains Roman numbers, then these are '
                       'converted to arabic numbers with leading zeros. '
                       'If no Roman numbers could be found, then the field '
                       '“ar_combined_disctrack” is used.',
        'category': 'common',
        'examples': ['01', '4-08'],
        'data_type': 'str',
    },
    'ar_combined_album': {
        'description': '“album” without ” (Disc X)”.',
        'category': 'common',
        'examples': ['Headlines and Deadlines: The Hits of a-ha',
                     'Die Meistersinger von Nürnberg'],
    },
    'ar_combined_artist': {
        'description': 'The first available value of this metatag order: '
                       '“albumartist” -> “artist” -> “albumartist_credit” '
                       '-> “artist_credit”',
        'category': 'common',
        'examples': ['a-ha',
                     'Richard Wagner; René Kollo, Helen Donath, ...'],
        'data_type': 'str',
    },
    'ar_combined_artist_sort': {
        'description': 'The first available value of this metatag order: '
                       '“albumartist_sort” -> “artist_sort” -> '
                       '“ar_combined_artist”',
        'category': 'common',
        'examples': ['a-ha', 'Wagner, Richard; Kollo, René, Donath, Helen...'],
        'data_type': 'str',
    },
    'ar_combined_composer': {
        'description': 'The first not empty field of this field list: '
                       '“composer_sort”, “composer”, “ar_combined_artist”',
        'category': 'common',
        'examples': ['Beethoven, Ludwig-van', 'Wagner, Richard'],
        'data_type': 'str',
    },
    'ar_combined_disctrack': {
        'description': 'Combination of disc and track in the format: '
                       'disk-track',
        'category': 'common',
        'examples': ['1-01', '3-099'],
        'data_type': 'str',
    },
    'ar_combined_soundtrack': {
        'description': 'Boolean flag which indicates if the audio file is '
                       'a soundtrack',
        'category': 'common',
        'examples': [True, False],
        'data_type': 'bool',
    },
    'ar_combined_work_top': {
        'description': 'The work on the top level of a work hierarchy.',
        'category': 'common',
        'examples': ['Horn Concerto: I. Allegro',
                     'Die Meistersinger von Nürnberg'],
        'data_type': 'str',
    },
    'ar_combined_year': {
        'description': 'First “original_year” then “year”.',
        'category': 'common',
        'examples': [1978],
        'data_type': 'int',
    },
    'ar_initial_album': {
        'description': 'First character in lowercase of “ar_combined_album”. '
                       'Allowed characters: [a-z, 0, _], 0-9 -> 0, ? -> _. '
                       'For example “Help!” -> “h”.',
        'category': 'common',
        'examples': ['h'],
    },
    'ar_initial_artist': {
        'description': 'First character in lowercase of '
                       '“ar_combined_artist_sort”. '
                       'Allowed characters: [a-z, 0, _], 0-9 -> 0, ? -> _. '
                       'For example “Brendel, Alfred” -> “b”.',
        'category': 'common',
        'examples': ['b'],
        'data_type': 'str',
    },
    'ar_initial_composer': {
        'description': 'First character in lowercase of '
                       '“ar_combined_composer”. '
                       'Allowed characters: [a-z, 0, _], 0-9 -> 0, ? -> _. '
                       'For example “Ludwig van Beethoven” -> “l”.',
        'category': 'common',
        'examples': ['l'],
        'data_type': 'str',
    },
    'ar_performer': {
        'description': 'Performer names.',
        'category': 'common',
        'examples': ['Herbert von Karajan, Staatskapelle Dresden'],
        'data_type': 'str',
    },
    'ar_performer_raw': {
        'description': 'Raw performer names.',
        'category': 'common',
        'examples': [[['conductor', 'Herbert von Karajan'],
                      ['orchestra', 'Staatskapelle Dresden']]],
        'data_type': 'list',
    },
    'ar_performer_short': {
        'description': 'Abbreviated performer names.',
        'category': 'common',
        'examples': ['Karajan, StaDre'],
        'data_type': 'str',
    },
}
"""Documentation of the extra fields."""

all_fields = phrydy.doc_generator.merge_fields(
    phrydy.field_docs.fields, fields)


class ArgsDefault:
    """To document the return value of the :func:`audiorename.args.parse_args`.
    It can also be used to mock the args object for testing purposes.
    """

    # default
    config: typing.Optional[str] = None

    # [selection]
    source: typing.Optional[str] = None
    source_as_target: typing.Optional[bool] = None
    target: typing.Optional[str] = None

    # [rename]
    backup_folder: typing.Optional[str] = None
    best_format: typing.Optional[bool] = None
    dry_run: typing.Optional[bool] = None
    move_action: typing.Union[
        typing.Literal['move', 'copy', 'no_rename'], None] = None
    cleaning_action: typing.Union[typing.Literal['backup', 'delete',
                                                 'do_nothing'], None] = None

    # [filters]
    album_complete: typing.Optional[bool] = None
    album_min: typing.Optional[int] = None
    extension: typing.Optional[str] = None
    genre_classical: typing.Optional[str] = None
    field_skip: typing.Optional[str] = None

    # [template_settings]
    classical: typing.Optional[bool] = None
    shell_friendly: typing.Optional[bool] = None
    no_soundtrack: typing.Optional[bool] = None

    # [path_templates]
    default_template: typing.Optional[str] = None
    soundtrack_template: typing.Optional[str] = None
    compilation_template: typing.Optional[str] = None
    classical_template: typing.Optional[str] = None

    # [cli_output]
    color: typing.Optional[bool] = None
    debug: typing.Optional[bool] = None
    job_info: typing.Optional[bool] = None
    mb_track_listing: typing.Optional[bool] = None
    one_line: typing.Optional[bool] = None
    stats: typing.Optional[bool] = None
    verbose: typing.Optional[bool] = None

    # [metadata_actions]
    enrich_metadata: typing.Optional[bool] = None
    remap_classical: typing.Optional[bool] = None

    def __init__(self, **kwargs: typing.Any):
        for k, v in kwargs.items():
            setattr(self, k, v)


def read_configuration_file() -> str:
    content = read_file(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'example-config.ini'))
    return indent(content)


def description() -> str:
    """Build the description string."""
    return '''\
    Rename audio files from metadata tags.

    How to specify the target directory?

    1. By the default the audio files are moved or renamed to the parent
       working directory.
    2. Use the option ``-t <folder>`` or ``--target <folder>`` to specifiy
       a target directory.
    3. Use the option ``-a`` or ``--source-as-target`` to copy or rename
       your audio files within the source directory.

Metadata fields
===============

''' + phrydy.format_fields_as_txt(additional_fields=fields, color=True,
                                  field_prefix='$') + '''

Functions
=========

''' + tmep.doc.Doc().get() + '''

Configuration file
==================

''' + read_configuration_file()


def parse_args(argv: typing.List[str]) -> ArgsDefault:
    """Parse the command line arguments using the python library `argparse`.

    :param list argv: The command line arguments specified as a list: e. g
        :code:`['--dry-run', '.']`

    :return: Dictionary see :class:`audiorename.args.ArgsDefault`
    """

    if not argv:
        argv = None

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description()
    )

    ##
    # Options without section. These options have no equivalent in the
    # configuration file
    ##

    # config
    parser.add_argument(
        '--config',
        help='Load a configuration file in INI format.',
        default=None,
    )

    # version
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=get_versions()['version'])
    )


###############################################################################
# [selection]
###############################################################################

    selection = parser.add_argument_group(
        title='[selection]',
        description='The following arguments are intended to select the audio '
        'files.'
    )

    # source
    selection.add_argument(
        'source',
        help='A folder containing audio files or a single audio file. If you '
        'specify a folder, the program will search for audio files in all '
        'subfolders. If you want to rename the audio files in the current '
        'working directory, then specify a dot (“.”).'
    )

    # target
    selection.add_argument(
        '-t',
        '--target',
        help='Target directory',
        default=None,
    )

    # source_as_target
    selection.add_argument(
        '-a',
        '--source-as-target',
        help='Use specified source folder as target directory',
        action='store_true',
        default=None,
    )


###############################################################################
# Rename
###############################################################################

    rename = parser.add_argument_group(
        title='[rename]',
        description='These options configure the actual renaming process.'
    )

    # backup_folder
    rename.add_argument(
        '-p',
        '--backup-folder',
        help='Folder to store the backup files in.',
        default=None
    )

    # best_format
    rename.add_argument(
        '-B',
        '--best-format',
        help='Use the best format. This option only takes effect if the \
        target file already exists. `audiorename` now checks the qualtity of \
        the two audio files (source and target). The tool first examines the \
        format. For example a FLAC file wins over a MP3 file. Then \
        `audiorename` checks the bitrate.',
        action='store_true',
        default=None,
    )

    # dry_run
    rename.add_argument(
        '-d',
        '--dry-run',
        help='Don’t rename or copy the audio files.',
        action='store_true',
        default=None,
    )

##
# Move actions
##

    rename_move = parser.add_argument_group('move action')
    exclusive_rename_move = rename_move.add_mutually_exclusive_group()

    # move_action: copy
    exclusive_rename_move.add_argument(
        '-C',
        '--copy',
        dest='move_action',
        help='Copy files instead of rename / move.',
        action='store_const',
        const='copy',
    )

    # move_action: move
    exclusive_rename_move.add_argument(
        '-M',
        '--move',
        dest='move_action',
        help='Move / rename a file. This is the default action. The option \
        can be omitted.',
        action='store_const',
        const='move',
    )

    # move_action: no_rename
    exclusive_rename_move.add_argument(
        '-n',
        '--no-rename',
        dest='move_action',
        help='Don’t rename, move, copy or perform a dry run. Do nothing.',
        action='store_const',
        const='no_rename',
    )

##
# Cleaning actions
##

    rename_cleaning = parser.add_argument_group(
        title='cleaning action',
        description='The cleaning actions are only executed if the target '
        'file already exists.'
    )
    exclusive_rename_cleaning = rename_cleaning.add_mutually_exclusive_group()

    # cleaning_action: backup
    exclusive_rename_cleaning.add_argument(
        '-A',
        '--backup',
        dest='cleaning_action',
        help='Backup the audio files instead of deleting them. The backup \
        directory can be specified with the --backup-folder option.',
        action='store_const',
        const='backup',
    )

    # cleaning_action: delete
    exclusive_rename_cleaning.add_argument(
        '-D',
        '--delete',
        dest='cleaning_action',
        help='Delete the audio files instead of creating a backup.',
        action='store_const',
        const='delete',
    )

###############################################################################
# filters
###############################################################################

    filters = parser.add_argument_group(
        title='[filters]',
        description='The following options filter the music files that are '
        'renamed according to certain rules.'
    )

    # album_complete
    filters.add_argument(
        '-F',
        '--album-complete',
        help='Rename only complete albums.',
        action='store_true',
        default=None,
    )

    # album_min
    filters.add_argument(
        '-m',
        '--album-min',
        type=int,
        help='Rename only albums containing at least X files.',
        default=None
    )

    # extension
    filters.add_argument(
        '-e',
        '--extension',
        help='Extensions to rename.',
        default=None
    )

    # genre classical
    filters.add_argument(
        '--genre-classical',
        help='List of genres to be classical.',
        default=','
    )

    # field_skip
    filters.add_argument(
        '-s',
        '--field-skip',
        help='Skip renaming if field is empty.',
        default=None
    )

###############################################################################
# formats
###############################################################################

    template_settings = parser.add_argument_group('[template_settings]')

    # classical
    template_settings.add_argument(
        '-k',
        '--classical',
        help='Use the default format for classical music. If you use this \
        option, both parameters (--default and --compilation) have no \
        effect. Classical music is sorted by the lastname of the composer.',
        action='store_true',
        default=None,
    )

    # shell_friendly
    template_settings.add_argument(
        '-S',
        '--shell-friendly',
        help='Rename audio files “shell friendly”, this means without \
        whitespaces, parentheses etc.',
        action='store_true',
        default=None,
    )

    # no_soundtrack
    template_settings.add_argument(
        '--no-soundtrack',
        action='store_true',
        help='Do not use the path template for soundtracks. Use instead the \
        default path template.',
        default=None,
    )

###############################################################################
# path_templates
###############################################################################

    path_templates = parser.add_argument_group(
        title='[path_templates]',
        description='audiorename provides default path templates. '
        'You can specify your own path templates using the following options.',
    )

    # default_template
    path_templates.add_argument(
        '-f',
        '--default',
        '--format',
        metavar='PATH_TEMPLATE',
        dest='default_template',
        help='The default path template for audio files that are not \
        compilations or compilations. Use metadata fields and functions to \
        build the path template.',
        default=None,
    )

    # compilation_template
    path_templates.add_argument(
        '-c',
        '--compilation',
        metavar='PATH_TEMPLATE',
        dest='compilation_template',
        help='Path template for compilations. Use metadata fields and \
        functions to build the path template.',
        default=None,
    )

    # soundtrack_template
    path_templates.add_argument(
        '--soundtrack',
        metavar='PATH_TEMPLATE',
        dest='soundtrack_template',
        help='Path template for a soundtrack audio file. Use metadata fields \
        and functions to build the path template.',
        default=None,
    )

    # classical_template
    path_templates.add_argument(
        '--format-classical',
        metavar='PATH_TEMPLATE',
        dest='classical_template',
        help='Path template for classical audio file. Use metadata fields \
        and functions to build the path template.',
        default=None,
    )

###############################################################################
# cli_output
###############################################################################

    cli_output = parser.add_argument_group(
        title='[cli_output]',
        description='This group contains all options that affect the output '
        'on the command line interface (cli).')

    output_color = cli_output.add_mutually_exclusive_group()

    # color
    output_color.add_argument(
        '-K',
        '--color',
        help='Colorize the standard output of the program with ANSI colors.',
        action='store_true',
        default=None,
    )

    output_color.add_argument(
        '--no-color',
        help='Don’t colorize the standard output of the program with ANSI '
             'colors.',
        action='store_false',
        dest='color',
        default=None,
    )

    # debug
    cli_output.add_argument(
        '-b',
        '--debug',
        help='Print debug informations about the single metadata fields.',
        action='store_true',
        default=None,
    )

    # job_info
    cli_output.add_argument(
        '-j',
        '--job-info',
        help='Display informations about the current job. This informations \
        are printted out before any actions on the audio files are executed.',
        action='store_true',
        default=None,
    )

    # mb_track_listing
    cli_output.add_argument(
        '-l',
        '--mb-track-listing',
        help='Print track listing for Musicbrainz website: Format: track. \
        title (duration), e. g.: \
          1. He, Zigeuner (1:31) \
          2. Hochgetürmte Rimaflut (1:21)',
        action='store_true',
        default=None,
    )

    # one_line
    cli_output.add_argument(
        '-o',
        '--one-line',
        help='Display the rename / copy action status on one line instead of \
        two.',
        action='store_true',
        default=None,
    )

    # stats
    cli_output.add_argument(
        '-T',
        '--stats',
        help='Show statistics at the end of the execution.',
        action='store_true',
        default=None,
    )

    # verbose
    cli_output.add_argument(
        '-V',
        '--verbose',
        help='Make the command line output more verbose.',
        action='store_true',
        default=None,
    )

###############################################################################
# Metadata actions
###############################################################################

    metadata_actions = parser.add_argument_group('[metadata_actions]')

    # enrich_metadata
    metadata_actions.add_argument(
        '-E',
        '--enrich-metadata',
        help='Fetch the tag fields “work” and “mb_workid” from Musicbrainz \
        and save this fields into the audio file. The audio file must have \
        the tag field “mb_trackid”. The give audio file is not renamed.',
        action='store_true',
        default=None,
    )

    # remap_classical
    metadata_actions.add_argument(
        '-r',
        '--remap-classical',
        help='Remap some fields to fit better for classical music: \
        “composer” becomes “artist”, “work” becomes “album”, from the \
        “title” the work prefix is removed (“Symphonie No. 9: I. Allegro” \
        -> “I. Allegro”) and “track” becomes the movement number. All \
        overwritten fields are safed in the “comments” field.',
        action='store_true',
        default=None,
    )

    return parser.parse_args(argv)
