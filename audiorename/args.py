"""Create the command line interface using the package “argparse”."""

from audiorename._version import get_versions
import argparse
import phrydy
import tmep

fields = {
    # album
    'ar_classical_album': {
        'description': 'ar_classical_album',
        'category': 'ordinary',
    },
    'ar_combined_album': {
        'description': '“album” without ” (Disc X)”.',
        'category': 'ordinary',
    },
    'ar_initial_album': {
        'description': 'First character in lowercase of “ar_combined_album”.',
        'category': 'ordinary',
    },
    # artist
    'ar_initial_artist': {
        'description': 'First character in lowercase of '
                       '“ar_combined_artist_sort”',
        'category': 'ordinary',
    },
    'ar_combined_artist': {
        'description': 'The first available value of this metatag order: '
                       '“albumartist” -> “artist” -> “albumartist_credit” '
                       '-> “artist_credit”',
        'category': 'ordinary',
    },
    'ar_combined_artist_sort': {
        'description': 'The first available value of this metatag order: '
                       '“albumartist_sort” -> “artist_sort” -> '
                       '“ar_combined_artist”',
        'category': 'ordinary',
    },
    # composer
    'ar_initial_composer': {
        'description': 'ar_initial_composer',
        'category': 'ordinary',
    },
    'ar_combined_composer': {
        'description': 'ar_combined_composer',
        'category': 'ordinary',
    },
    'ar_combined_disctrack': {
        'description': 'Combination of disc and track in the format: '
                       'disk-track, e.g. 1-01, 3-099',
        'category': 'ordinary',
    },
    'ar_classical_performer': {
        'description': 'ar_classical_performer',
        'category': 'ordinary',
    },
    'ar_combined_soundtrack': {
        'description': 'Boolean flag which indicates if the audio file is '
        'a soundtrack',
        'category': 'ordinary',
    },
    'ar_classical_title': {
        'description': 'ar_classical_title',
        'category': 'ordinary',
    },
    'ar_classical_track': {
        'description': 'ar_classical_track',
        'category': 'ordinary',
    },
    'ar_combined_year': {
        'description': 'First “original_year” then “year”.',
        'category': 'ordinary',
    },
    'ar_combined_work_top': {
        'description': 'The work on the top level of a work hierarchy.',
        'category': 'ordinary',
    },
}
"""Documentation of the extra fields."""

all_fields = phrydy.doc.merge_fields(phrydy.doc.fields, fields)


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
    compilation = False
    copy = False
    debug = False
    delete = False
    dry_run = False
    enrich_metadata = False
    extension = 'mp3,m4a,flac,wma'
    field_skip = False
    format = False
    job_info = False
    mb_track_listing = False
    move = False
    no_rename = False
    one_line = False
    remap_classical = False
    shell_friendly = False
    soundtrack = False
    source = u'.'
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

''' + phrydy.doc.get_doc(additional_doc=fields) + '''

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
        help='A folder containing audio files or a audio file'
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
        format. For example a flac file wins over a mp3 file. `audiorename`\
        then checks the bitrate.',
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
        help='Don’t rename, move, copy dry run. Do nothing.',
        action='store_true'
    )

##
# Cleanup actions
##

    rename_cleanup = parser.add_argument_group('rename cleanup actions')
    exclusive_rename_cleanup = rename_cleanup.add_mutually_exclusive_group()

    # --backup
    exclusive_rename_cleanup.add_argument(
        '-A',
        '--backup',
        help='Backup audio files instead of delete files',
        action='store_true'
    )

    # delete
    rename.add_argument(
        '-D',
        '--delete',
        help='Delete files.',
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
        help='Rename only complete albums',
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
        help='Extensions to rename',
        default='mp3,m4a,flac,wma'
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

###############################################################################
# output
###############################################################################

    output = parser.add_argument_group('output')

    # color
    output.add_argument(
        '-K',
        '--color',
        help='Colorize the standard output of the program with ANSI colors.',
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
