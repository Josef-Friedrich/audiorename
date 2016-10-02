# -*- coding: utf-8 -*-

import argparse
import textwrap

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
Rename audio files from metadata tags.

How to specify the target directory?

1. By the default the audio files are moved or renamed to the parent
   working directory.
2. Use the option ``-t <folder>`` or ``--target-dir <folder>`` to specifiy
   a target directory.
3. Use the option ``-a`` or ``--source-as-target-dir`` to copy or rename
   your audio files within the source directory.'''))

parser.add_argument(
    'folder',
    help='A folder containing audio files or a audio file'
)

parser.add_argument(
    '-f',
    '--format',
    help='A format string',
    default='$artist_initial/' +
    '$artistsafe_sort/' +
    '%shorten{${album},32}%ifdef{year_safe,_${year_safe}}/' +
    '${disctrack}_%shorten{$title,32}'
)

parser.add_argument(
    '-c',
    '--compilation',
    help='Format string for compilations',
    default='_compilations/' +
    '$album_initial/' +
    '$album%ifdef{year_safe,_${year_safe}}/' +
    '${disctrack}_%shorten{$title,32}'
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
    '--extensions',
    help='Extensions to rename',
    default='mp3'
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
