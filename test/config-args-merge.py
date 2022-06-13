#! /usr/bin/env python3

import argparse

import configparser
from configparser import ConfigParser


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

'''


def parse_args(*argv):
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
        help='Remap some fields to fit better for classical music: \
        “composer” becomes “artist”, “work” becomes “album”, from the \
        “title” the work prefix is removed (“Symphonie No. 9: I. Allegro” \
        -> “I. Allegro”) and “track” becomes the movement number. All \
        overwritten fields are safed in the “comments” field.',
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
        action='store_true',
        default=None
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

    # backup
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

    # field_skip
    parser.add_argument(
        '-s',
        '--field-skip',
        help='Skip renaming if field is empty.',
    )

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
    )

    # extension
    filters.add_argument(
        '-e',
        '--extension',
        help='Extensions to rename.',
    )

    # genre classical
    filters.add_argument(
        '--genre-classical',
        help='List of genres to be classical.',
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
    )

    # format
    format_strings.add_argument(
        '-f',
        '--format',
        metavar='FORMAT_STRING',
        help='The default format string for audio files that are not \
        compilations or compilations. Use metadata fields and functions to \
        build the format string.',
    )

    # soundtrack
    format_strings.add_argument(
        '--soundtrack',
        metavar='FORMAT_STRING',
        help='Format string for a soundtrack audio file. Use metadata fields \
        and functions to build the format string.',
    )

    # no_soundtrack
    format_strings.add_argument(
        '--no-soundtrack',
        action='store_true',
        help='Do not use the format string for soundtracks. Use instead the \
        default format string.',
    )

    # classical
    format_strings.add_argument(
        '--format-classical',
        metavar='FORMAT_STRING',
        help='Format string for classical audio file. Use metadata fields \
        and functions to build the format string.',
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
        action='store_true', default=None,
    )

    output_color.add_argument(
        '--no-color',
        help='Don’t colorize the standard output of the program with ANSI '
             'colors.',
        action='store_true', default=None,
    )

    # debug
    output.add_argument(
        '-b',
        '--debug',
        help='Print debug informations about the single metadata fields.',
        action='store_true', default=None,
    )

    # job_info
    output.add_argument(
        '-j',
        '--job-info',
        help='Display informations about the current job. This informations \
        are printted out before any actions on the audio files are executed.',
        action='store_true', default=None,
    )

    # mb_track_listing
    output.add_argument(
        '-l',
        '--mb-track-listing',
        help='Print track listing for Musicbrainz website: Format: track. \
        title (duration), e. g.: \
          1. He, Zigeuner (1:31) \
          2. Hochgetürmte Rimaflut (1:21)',
        action='store_true', default=None,
    )

    # one_line
    output.add_argument(
        '-o',
        '--one-line',
        help='Display the rename / copy action status on one line instead of \
        two.',
        action='store_true', default=None,
    )

    # stats
    output.add_argument(
        '-T',
        '--stats',
        help='Show statistics at the end of the execution.',
        action='store_true', default=None,
    )

    # verbose
    output.add_argument(
        '-V',
        '--verbose',
        help='Make the command line output more verbose.',
        action='store_true', default=None,
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


args = parse_args()

config = ConfigParser()
config.read('../example-config.ini')


class Config:

    _options = None

    def __init__(self, args: argparse.Namespace, config: ConfigParser,
                 section: str, options: dict):
        self._options = options
        print(config)
        for option, data_type in options.items():
            attr = None
            if getattr(args, option) is not None:
                attr = getattr(args, option)
            elif isinstance(config, ConfigParser):
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


class OutputConfig(Config):
    color = False
    debug = False
    job_info = False
    mb_track_listing = False
    one_line = False
    stats = False
    verbose = True


output = OutputConfig(args, config, 'output', {
    'color': 'boolean',
    'debug': 'boolean',
    'job_info': 'boolean',
    'mb_track_listing': 'boolean',
    'one_line': 'boolean',
    'stats': 'boolean',
    'verbose': 'boolean',
})

output._debug()

print(output.color)
