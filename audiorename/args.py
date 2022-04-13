"""Create the command line interface using the package “argparse”."""

from ._version import get_versions
import argparse
import phrydy
import tmep

fields: phrydy.FieldDocCollection = {
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
        'description': 'First character in lowercase of “ar_combined_album”.',
        'category': 'common',
        'examples': ['h'],
    },
    'ar_initial_artist': {
        'description': 'First character in lowercase of '
                       '“ar_combined_artist_sort”',
        'category': 'common',
        'examples': ['b'],
        'data_type': 'str',
    },
    'ar_initial_composer': {
        'description': 'First character in lowercase of '
                       '“ar_combined_composer”. '
                       'For example “Ludwig van Beethoven” -> “l”',
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

all_fields = phrydy.merge_fields(phrydy.fields, fields)


class ArgsDefault():
    """This is a dummy class. The code only exists to document the return
    value of the :func:`audiorename.args.parse_args`.  It can also be used
    to mock the args object for testing purposes.
    """

    album_complete = False
    album_min = False
    backup = False
    backup_folder = False
    best_format = False
    classical = False
    color = False
    no_color = False
    compilation = False
    copy = False
    debug = False
    delete = False
    dry_run = False
    enrich_metadata = False
    extension = 'mp3,m4a,flac,wma'
    genre_classical = ','
    field_skip = False
    format = False
    job_info = False
    mb_track_listing = False
    move = False
    no_rename = False
    one_line = False
    remap_classical = False
    format_classical = False
    shell_friendly = False
    soundtrack = False
    source = '.'
    source_as_target = False
    stats = False
    target = ''
    verbose = False


def description():
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

''' + tmep.doc.Doc().get()


def parse_args(argv):
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

    parser.add_argument(
        'source',
        help='A folder containing audio files or a single audio file'
    )

    ##
    # Options (sorted alphabetically)
    ##

    # dry_run
    parser.add_argument(
        '-d',
        '--dry-run',
        help='Don’t rename or copy the audio files.',
        action='store_true'
    )

    # field_skip
    parser.add_argument(
        '-s',
        '--field-skip',
        help='Skip renaming if field is empty.',
        default=False
    )

    # version
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=get_versions()['version'])
    )

###############################################################################
# Metadata actions
###############################################################################

    metadata_actions = parser.add_argument_group('metadata actions')

    # enrich_metadata
    metadata_actions.add_argument(
        '-E',
        '--enrich-metadata',
        help='Fetch the tag fields “work” and “mb_workid” from Musicbrainz \
        and save this fields into the audio file. The audio file must have \
        the tag field “mb_trackid”. The give audio file is not renamed.',
        action='store_true'
    )

    # remap_classical
    metadata_actions.add_argument(
        '-r',
        '--remap-classical',
        help='',
        action='store_true'
    )

###############################################################################
# Rename
###############################################################################

    rename = parser.add_argument_group('rename')

    # backup_folder
    rename.add_argument(
        '-p',
        '--backup-folder',
        help='Folder to store the backup files in.',
        default=False
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
        action='store_true'
    )

##
# Move actions
##

    rename_move = parser.add_argument_group('rename move actions')
    exclusive_rename_move = rename_move.add_mutually_exclusive_group()

    # copy
    exclusive_rename_move.add_argument(
        '-C',
        '--copy',
        help='Copy files instead of rename / move.',
        action='store_true'
    )

    # move
    exclusive_rename_move.add_argument(
        '-M',
        '--move',
        help='Move / rename a file. This is the default action. The option \
        can be omitted.',
        action='store_true'
    )

    # no_rename
    exclusive_rename_move.add_argument(
        '-n',
        '--no-rename',
        help='Don’t rename, move, copy or perform a dry run. Do nothing.',
        action='store_true'
    )

##
# Cleaning actions
##

    rename_cleaning = parser.add_argument_group(
        title='rename cleaning actions',
        description='The cleaning actions are only executed if the target '
        'file already exists.'
    )
    exclusive_rename_cleaning = rename_cleaning.add_mutually_exclusive_group()

    # --backup
    exclusive_rename_cleaning.add_argument(
        '-A',
        '--backup',
        help='Backup the audio files instead of deleting them. The backup \
        directory can be specified with the --backup-folder option.',
        action='store_true'
    )

    # delete
    exclusive_rename_cleaning.add_argument(
        '-D',
        '--delete',
        help='Delete the audio files instead of creating a backup.',
        action='store_true'
    )

###############################################################################
# filters
###############################################################################

    filters = parser.add_argument_group('filters')

    # album_complete
    filters.add_argument(
        '-F',
        '--album-complete',
        help='Rename only complete albums.',
        action='store_true'
    )

    # album_min
    filters.add_argument(
        '-m',
        '--album-min',
        help='Rename only albums containing at least X files.',
        default=False
    )

    # extension
    filters.add_argument(
        '-e',
        '--extension',
        help='Extensions to rename.',
        default='mp3,m4a,flac,wma'
    )

    # genre classical
    filters.add_argument(
        '--genre-classical',
        help='List of genres to be classical.',
        default=','
    )

###############################################################################
# formats
###############################################################################

    formats = parser.add_argument_group('formats')

    # classical
    formats.add_argument(
        '-k',
        '--classical',
        help='Use the default format for classical music. If you use this \
        option, both parameters (--format and --compilation) have no \
        effect. Classical music is sorted by the lastname of the composer.',
        action='store_true'
    )

    # shell_friendly
    formats.add_argument(
        '-S',
        '--shell-friendly',
        help='Rename audio files “shell friendly”, this means without \
        whitespaces, parentheses etc.',
        action='store_true'
    )

###############################################################################
# formats_strings
###############################################################################

    format_strings = parser.add_argument_group('format strings')

    # compilation
    format_strings.add_argument(
        '-c',
        '--compilation',
        metavar='FORMAT_STRING',
        help='Format string for compilations. Use metadata fields and \
        functions to build the format string.',
        default=False
    )

    # format
    format_strings.add_argument(
        '-f',
        '--format',
        metavar='FORMAT_STRING',
        help='The default format string for audio files that are not \
        compilations or compilations. Use metadata fields and functions to \
        build the format string.',
        default=False
    )

    # soundtrack
    format_strings.add_argument(
        '--soundtrack',
        metavar='FORMAT_STRING',
        help='Format string for a soundtrack audio file. Use metadata fields \
        and functions to build the format string.',
        default=False
    )
    # classical
    format_strings.add_argument(
        '--format-classical',
        metavar='FORMAT_STRING',
        help='Format string for classical audio file. Use metadata fields \
        and functions to build the format string.',
        default=False
    )
###############################################################################
# output
###############################################################################

    output = parser.add_argument_group('output')

    output_color = output.add_mutually_exclusive_group()

    # color
    output_color.add_argument(
        '-K',
        '--color',
        help='Colorize the standard output of the program with ANSI colors.',
        action='store_true'
    )

    output_color.add_argument(
        '--no-color',
        help='Don’t colorize the standard output of the program with ANSI '
             'colors.',
        action='store_true'
    )

    # debug
    output.add_argument(
        '-b',
        '--debug',
        help='Print debug informations about the single metadata fields.',
        action='store_true'
    )

    # job_info
    output.add_argument(
        '-j',
        '--job-info',
        help='Display informations about the current job. This informations \
        are printted out before any actions on the audio files are executed.',
        action='store_true'
    )

    # mb_track_listing
    output.add_argument(
        '-l',
        '--mb-track-listing',
        help='Print track listing for Musicbrainz website: Format: track. \
        title (duration), e. g.: \
          1. He, Zigeuner (1:31) \
          2. Hochgetürmte Rimaflut (1:21)',
        action='store_true'
    )

    # one_line
    output.add_argument(
        '-o',
        '--one-line',
        help='Display the rename / copy action status on one line instead of \
        two.',
        action='store_true'
    )

    # stats
    output.add_argument(
        '-T',
        '--stats',
        help='Show statistics at the end of the execution.',
        action='store_true'
    )

    # verbose
    output.add_argument(
        '-V',
        '--verbose',
        help='Make the command line output more verbose.',
        action='store_true'
    )

###############################################################################
# target
###############################################################################

    target = parser.add_argument_group('target')

    # source_as_target
    target.add_argument(
        '-a',
        '--source-as-target',
        help='Use specified source folder as target directory',
        action='store_true'
    )

    # target
    target.add_argument(
        '-t',
        '--target',
        help='Target directory',
        default=''
    )

    return parser.parse_args(argv)
