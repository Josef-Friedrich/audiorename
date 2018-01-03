# -*- coding: utf-8 -*-

"""Create the command line interface using the package “argparse”."""

import argparse
import phrydy
from phrydy import doc as pdoc
from ._version import get_versions
from tmep import doc as tdoc
td = tdoc.Doc()

fields = {
    # album
    'album_classical': {
        'description': 'album_classical',
        'category': 'ordinary',
    },
    'album_clean': {
        'description': '“album” without ” (Disc X)”.',
        'category': 'ordinary',
    },
    'album_initial': {
        'description': 'First character in lowercase of “album_clean”.',
        'category': 'ordinary',
    },
    # artist
    'artist_initial': {
        'description': 'First character in lowercase of “artistsafe_sort”',
        'category': 'ordinary',
    },
    'artistsafe': {
        'description': 'The first available value of this metatag order: ' +
                       '“albumartist” -> “artist” -> “albumartist_credit” '
                       '-> “artist_credit”',
        'category': 'ordinary',
    },
    'artistsafe_sort': {
        'description': 'The first available value of this metatag order: ' +
                       '“albumartist_sort” -> “artist_sort” -> “artistsafe”',
        'category': 'ordinary',
    },
    # composer
    'composer_initial': {
        'description': 'composer_initial',
        'category': 'ordinary',
    },
    'composer_safe': {
        'description': 'composer_safe',
        'category': 'ordinary',
    },
    'disctrack': {
        'description': 'Combination of disc and track in the format: ' +
                       'disk-track, e.g. 1-01, 3-099',
        'category': 'ordinary',
    },
    'performer_classical': {
        'description': 'performer_classical',
        'category': 'ordinary',
    },
    'soundtrack': {
        'description': 'Boolean flag which indicates if the audio file is ' +
        'a soundtrack',
        'category': 'ordinary',
    },
    'title_classical': {
        'description': 'title_classical',
        'category': 'ordinary',
    },
    'track_classical': {
        'description': 'track_classical',
        'category': 'ordinary',
    },
    'year_safe': {
        'description': 'First “original_year” then “year”.',
        'category': 'ordinary',
    },
}
"""Documentation of the extra fields."""


all_fields = pdoc.merge_fields(phrydy.doc.fields, fields)


class ArgsDefault():
    """This is a dummy class. The code only exists to document the return
    value of the :func:`audiorename.args.parse_args`.  It can also be used
    to mock the args object for testing purposes.
    """

    classical = False
    compilation = False
    copy = False
    delete_existing = False
    dry_run = False
    extension = 'mp3,m4a,flac,wma'
    filter_album_complete = False
    filter_album_min = False
    format = False
    mb_track_listing = False
    move = False
    shell_friendly = False
    skip_if_empty = False
    soundtrack = False
    source_as_target_dir = False
    target_dir = ''
    unittest = False
    verbose = False
    work = False


def description():
    """Build the description string."""
    return '''\
    Rename audio files from metadata tags.

    How to specify the target directory?

    1. By the default the audio files are moved or renamed to the parent
       working directory.
    2. Use the option ``-t <folder>`` or ``--target-dir <folder>`` to specifiy
       a target directory.
    3. Use the option ``-a`` or ``--source-as-target-dir`` to copy or rename
       your audio files within the source directory.

    Metadata fields
    ---------------

    ''' + pdoc.get_doc(additional_doc=fields) + '''

    Functions
    ---------

    ''' + td.get()


def parse_args(argv):
    """Parse the command line arguments using the python library `argparse`.

    :param list argv: The command line arguments specified as a list: e. g
        :code:`['--dry-run', '.']`

    :return: Dictionary see :class:`audiorename.args.ArgsDefault`

    .. todo:: Rename arguemnt `path` to `source`
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description()
    )

    parser.add_argument(
        'path',
        help='A folder containing audio files or a audio file'
    )

    ##
    # Options (sorted alphabetically)
    ##

    # skip_if_empty
    parser.add_argument(
        '-s',
        '--skip-if-empty',
        help='Skip renaming of field is empty.',
        default=False
    )

    # unittest
    parser.add_argument(
        '--unittest',
        help='The audio files are not renamed. Debug messages for the unit test \
        are printed out.',
        action='store_true'
    )

    # version
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=get_versions()['version'])
    )

    # verbose
    parser.add_argument(
        '-V',
        '--verbose',
        action='store_true'
    )

    # work
    parser.add_argument(
        '-w',
        '--work',
        help='Fetch the tag fields “work” and “mb_workid” from Musicbrainz \
        and save this fields into the audio file. The audio file must have \
        the tag field “mb_trackid”. The give audio file is not renamed.',
        action='store_true'
    )

###############################################################################
# actions
###############################################################################

    actions = parser.add_argument_group('actions')

    # delete_existing
    actions.add_argument(
        '-D',
        '--delete-existing',
        help='Delete source file if the target file already exists.',
        action='store_true'
    )

    exclusive = actions.add_mutually_exclusive_group()

    # copy
    exclusive.add_argument(
        '-C',
        '--copy',
        help='Copy files instead of rename / move.',
        action='store_true'
    )

    # dry_run
    exclusive.add_argument(
        '-d',
        '--dry-run',
        help='Don’t rename or copy the audio files.',
        action='store_true'
    )

    # move
    exclusive.add_argument(
        '-M',
        '--move',
        help='Move / rename a file. This is the default action. The option \
        can be omitted.',
        action='store_true'
    )

    # mb_track_listing
    exclusive.add_argument(
        '--mb-track-listing',
        help='Print track listing for Musicbrainz website: Format: track. \
        title (duration), e. g.: \
          1. He, Zigeuner (1:31) \
          2. Hochgetürmte Rimaflut (1:21)',
        action='store_true'
    )

###############################################################################
# filters
###############################################################################

    filters = parser.add_argument_group('filters')

    # extension
    filters.add_argument(
        '-e',
        '--extension',
        help='Extensions to rename',
        default='mp3,m4a,flac,wma'
    )

    # filter_album_complete
    filters.add_argument(
        '-F',
        '--filter-album-complete',
        help='Rename only complete albums',
        action='store_true'
    )

    # filter_album_min
    filters.add_argument(
        '-m',
        '--filter-album-min',
        help='Rename only albums containing at least X files.',
        default=False
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
        help='Format string for compilations. Use metadata fields and \
        functions to build the format string.',
        default=False
    )

    # format
    format_strings.add_argument(
        '-f',
        '--format',
        help='The default format string for audio files that are not \
        compilations or compilations. Use metadata fields and functions to \
        build the format string.',
        default=False
    )

    # soundtrack
    format_strings.add_argument(
        '--soundtrack',
        help='Format string for a soundtrack audio file. Use metadata fields \
        and functions to build the format string.',
        default=False
    )

###############################################################################
# target
###############################################################################

    target = parser.add_argument_group('target')

    # source_as_target_dir
    target.add_argument(
        '-a',
        '--source-as-target-dir',
        help='Use specified source folder as target directory',
        action='store_true'
    )

    # target_dir
    target.add_argument(
        '-t',
        '--target-dir',
        help='Target directory',
        default=''
    )

    return parser.parse_args(argv)
