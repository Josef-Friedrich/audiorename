# -*- coding: utf-8 -*-

import argparse
import textwrap

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
Python script to rename audio files from metadata tags.

Metadata fields:

    Ordinary metadata:

    - title
    - artist
    - artist_sort:         The “sort name” of the track artist
                           (e.g., “Beatles, The” or “White, Jack”).
    - artist_credit:       The track-specific artist credit name,
                           which may be a variation of the artist’s
                           “canonical” name.
    - artistsafe:          The first available value of this metatag
                           order: “albumartist” -> “artist” ->
                           “albumartist_credit” -> “artist_credit”
    - artistsafe_sort:     The first available value of this metatag
                           order: “albumartist_sort” ->
                           “artist_sort” -> “artistsafe”
    - artist_initial:      First character in lowercase of
                            “artistsafe_sort”
    - album
    - albumartist:         The artist for the entire album, which
                           may be different from the artists for the
                           individual tracks.
    - albumartist_sort
    - albumartist_credit
    - album_initial:       First character in lowercase of “album”.
    - genre
    - composer
    - grouping
    - year, month, day:    The release date of the specific release.
    - original_year, original_month, original_day:
                           The release date of the original version
                           of the album.
    - year_safe
    - track
    - tracktotal
    - disc
    - disctotal
    - disctrack:           Combination of disc and track in the
                           format: disk-track, e.g. 1-01, 3-099
    - lyrics
    - comments
    - bpm
    - comp:                 Compilation flag.
    - albumtype:            The MusicBrainz album type; the
                            MusicBrainz wiki has a list of type
                            names.
    - label
    - asin
    - catalognum
    - script
    - language
    - country
    - albumstatus
    - media
    - albumdisambig
    - disctitle
    - encoder

    Audio information:

    - length                (in seconds)
    - bitrate               (in kilobits per second, with units:
                            e.g., “192kbps”)
    - format                (e.g., “MP3” or “FLAC”)
    - channels
    - bitdepth              (only available for some formats)
    - samplerate            (in kilohertz, with units: e.g.,
                            “48kHz”)

    MusicBrainz and fingerprint information:

    - mb_trackid
    - mb_albumid
    - mb_artistid
    - mb_albumartistid
    - mb_releasegroupid
    - acoustid_fingerprint
    - acoustid_id


    Template Functions

    - %lower{text}:         Convert “text” to lowercase.
    - %upper{text}:         Convert “text” to UPPERCASE.
    - %title{text}:         Convert “text” to Title Case.
    - %left{text,n}:        Return the first “n” characters of “text”.
    - %right{text,n}:       Return the last “n” characters of “text”.
    - %shorten{text,n}:     Shorten “text” on word boundarys.
    - %if{condition,text} or %if{condition,truetext,falsetext}:
                            If condition is nonempty (or nonzero,
                            if it’s a number), then returns the
                            second argument. Otherwise, returns the
                            third argument if specified (or nothing
                            if falsetext is left off).
    - %delchars{text,chars}:
                            Delete every single character of “chars“
                            in “text”.
    - %deldupchars{text,chars}:
                            Search for duplicate characters and
                            replace with only one occurrance of
                            this characters.
    - %replchars{text,chars,replace}
    - %sanitize{text}:      Delete in most file systems not allowed
                            characters
    - %asciify{text}:       Convert non-ASCII characters to their
                            ASCII equivalents. For example, “café”
                            becomes “cafe”. Uses the mapping
                            provided by the unidecode module.
    - %time{date_time,format,curformat}:
                            Return the date and time in any format
                            accepted by strftime. For example, to
                            get the year some music was added to
                            your library, use %time{$added,%Y}.
    - %first{text}:         Returns the first item, separated by ; .
                            You can use %first{text,count,skip},
                            where count is the number of items
                            (default 1) and skip is number to skip
                            (default 0). You can also use
                            %first{text,count,skip,sep,join} where
                            sep is the separator, like ; or / and
                            join is the text to concatenate the
                            items.
    - %ifdef{field}, %ifdef{field,truetext} or
      %ifdef{field,truetext,falsetext}:
                            If field exists, then return truetext or
                            field (default). Otherwise, returns
                            falsetext. The field should be entered
                            without $.

    '''))

parser.add_argument(
    'folder', help='A folder containing audio files or a audio file')

parser.add_argument(
    '-f',
    '--format',
    help='A format string',
    default='$artist_initial/\
    $artistsafe_sort/\
    %shorten{${album},32}%ifdef{year_safe,_${year_safe}}/\
    ${disctrack}_%shorten{$title,32}'
)

parser.add_argument(
    '-c',
    '--compilation',
    help='Format string for compilations',
    default='_compilations/\
    $album_initial/\
    $album%ifdef{year_safe,_${year_safe}}/\
    ${disctrack}_%shorten{$title,32}'
)

parser.add_argument(
    '-S',
    '--shell-friendly',
    help='Rename audio files “shell friendly”, this means without \
    whitespaces, parentheses etc.',
    action='store_true')

parser.add_argument(
    '-d',
    '--dry-run',
    help='A format string for singeltons',
    action='store_true')

parser.add_argument(
    '-D',
    '--debug',
    help='Show special debug informations: meta, artist, track, year',
    default=False)

parser.add_argument(
    '-e', '--extensions', help='Extensions to rename', default='mp3')

parser.add_argument('-b', '--base-dir', help='Base directory', default='')

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
