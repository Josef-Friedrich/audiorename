# -*- coding: utf-8 -*-

import argparse
import textwrap

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
Rename audio files from metadata tags.



    '''))

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
    '-b',
    '--base-dir',
    help='Base directory',
    default=''
)

parser.add_argument(
    '-s',
    '--skip-if-empty',
    help='Skip renaming of field is empty.',
    default=False)

parser.add_argument(
    '-a',
    '--folder-as-base-dir',
    help='Use specified folder as base directory',
    action='store_true')

parser.add_argument(
    '-C',
    '--copy',
    help='Copy files instead of rename / move.',
    action='store_true')
