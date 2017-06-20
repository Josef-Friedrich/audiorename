# -*- coding: utf-8 -*-

"""Create the command line interface using the package “argparse”."""

import argparse
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

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''\
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
)


parser.add_argument(
    'path',
    help='A folder containing audio files or a audio file'
)

parser.add_argument(
    '-f',
    '--format',
    help='A format string',
    default=False
)

parser.add_argument(
    '-c',
    '--compilation',
    help='Format string for compilations',
    default=False
)

parser.add_argument(
    '-k',
    '--classical',
    help='Use default format for classical music',
    action='store_true'
)

parser.add_argument(
    '-S',
    '--shell-friendly',
    help='Rename audio files “shell friendly”, this means without \
    whitespaces, parentheses etc.',
    action='store_true'
)

parser.add_argument(
    '-d',
    '--dry-run',
    help='Don’t rename or copy the audio files.',
    action='store_true'
)

parser.add_argument(
    '-e',
    '--extension',
    help='Extensions to rename',
    default='mp3,m4a,flac,wma'
)

parser.add_argument(
    '-t',
    '--target-dir',
    help='Target directory',
    default=''
)

parser.add_argument(
    '-s',
    '--skip-if-empty',
    help='Skip renaming of field is empty.',
    default=False
)

parser.add_argument(
    '-a',
    '--source-as-target-dir',
    help='Use specified source folder as target directory',
    action='store_true'
)

parser.add_argument(
    '-C',
    '--copy',
    help='Copy files instead of rename / move.',
    action='store_true'
)

parser.add_argument(
    '-m',
    '--filter-album-min',
    help='Rename only albums containing at least X files.',
    default=False
)

parser.add_argument(
    '-F',
    '--filter-album-complete',
    help='Rename only complete albums',
    action='store_true'
)

parser.add_argument(
    '--unittest',
    help='The audio files are not renamed. Debug messages for the unit test \
    are printed out.',
    action='store_true'
)

parser.add_argument(
    '--mb-track-listing',
    help='Print track listing for Musicbrainz website',
    action='store_true'
)

parser.add_argument(
    '-v',
    '--version',
    action='version',
    version='%(prog)s {version}'.format(version=get_versions()['version'])
)
