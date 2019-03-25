.. image:: http://img.shields.io/pypi/v/audiorename.svg
    :target: https://pypi.python.org/pypi/audiorename
    :alt: This package on the Python Package Index

.. image:: https://travis-ci.org/Josef-Friedrich/audiorename.svg?branch=packaging
    :target: https://travis-ci.org/Josef-Friedrich/audiorename
    :alt: Continuous integration

.. image:: https://readthedocs.org/projects/audiorename/badge/?version=latest
    :target: https://audiorename.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

***********
audiorename
***********

Rename audio files from metadata tags.

Installation
============

From Github
-----------

.. code:: Shell

    git clone git@github.com:Josef-Friedrich/audiorename.git
    cd audiorename
    python setup.py install

From PyPI
---------

.. code:: Shell

    pip install audiorename
    easy_install audiorename

Usage
=====

.. code-block:: text

    usage: audiorenamer [-h] [-d] [-s FIELD_SKIP] [-v] [-E] [-r]
                        [-p BACKUP_FOLDER] [-B] [-C | -M | -n] [-A] [-D] [-F]
                        [-m ALBUM_MIN] [-e EXTENSION] [-k] [-S] [-c FORMAT_STRING]
                        [-f FORMAT_STRING] [--soundtrack FORMAT_STRING] [-K] [-b]
                        [-j] [-l] [-o] [-T] [-V] [-a] [-t TARGET]
                        source
    
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
    
        $acoustid_fingerprint:       Acoustic ID fingerprint
    
        $acoustid_id:                Acoustic ID
    
        $album:                      album
    
        $albumartist:                The artist for the entire album, which may be
                                     different from the artists for the individual
                                     tracks
    
        $albumartist_credit:         albumartist_credit
    
        $albumartist_sort:           albumartist_sort
    
        $albumdisambig:              albumdisambig
    
        $albumstatus:                The status describes how "official" a release
                                     is. Possible values are: official,
                                     promotional, bootleg, pseudo-release
    
        $albumtype:                  The MusicBrainz album type; the MusicBrainz
                                     wiki has a list of type names
    
        $ar_classical_album:         ar_classical_album
    
        $ar_classical_performer:     ar_classical_performer
    
        $ar_classical_title:         ar_classical_title
    
        $ar_classical_track:         ar_classical_track
    
        $ar_combined_album:          “album” without ” (Disc X)”.
    
        $ar_combined_artist:         The first available value of this metatag
                                     order: “albumartist” -> “artist” ->
                                     “albumartist_credit” -> “artist_credit”
    
        $ar_combined_artist_sort:    The first available value of this metatag
                                     order: “albumartist_sort” -> “artist_sort” ->
                                     “ar_combined_artist”
    
        $ar_combined_composer:       ar_combined_composer
    
        $ar_combined_disctrack:      Combination of disc and track in the format:
                                     disk-track, e.g. 1-01, 3-099
    
        $ar_combined_soundtrack:     Boolean flag which indicates if the audio
                                     file is a soundtrack
    
        $ar_combined_work_top:       The work on the top level of a work
                                     hierarchy.
    
        $ar_combined_year:           First “original_year” then “year”.
    
        $ar_initial_album:           First character in lowercase of
                                     “ar_combined_album”.
    
        $ar_initial_artist:          First character in lowercase of
                                     “ar_combined_artist_sort”
    
        $ar_initial_composer:        ar_initial_composer
    
        $arranger:                   arranger
    
        $art:                        art
    
        $artist:                     artist
    
        $artist_credit:              The track-specific artist credit name, which
                                     may be a variation of the artist’s
                                     “canonical” name
    
        $artist_sort:                The “sort name” of the track artist (e.g.,
                                     “Beatles, The” or “White, Jack”)
    
        $asin:                       Amazon Standard Identification Number
    
        $bitdepth:                   only available for some formats
    
        $bitrate:                    in kilobits per second, with units: e.g.,
                                     “192kbps”
    
        $bpm:                        bpm
    
        $catalognum:                 This is a number assigned to the release by
                                     the label which can often be found on the
                                     spine or near the barcode. There may be more
                                     than one, especially when multiple labels are
                                     involved. This is not the ASIN — there is a
                                     relationship for that — nor the label code.
    
        $channels:                   channels
    
        $comments:                   comments
    
        $comp:                       Compilation flag
    
        $composer:                   composer
    
        $composer_sort:              Composer name for sorting.
    
        $country:                    The country the release was issued in.
    
        $date:                       date
    
        $day:                        The release day of the specific release
    
        $disc:                       disc
    
        $disctitle:                  disctitle
    
        $disctotal:                  disctotal
    
        $encoder:                    encoder
    
        $format:                     e.g., “MP3” or “FLAC”
    
        $genre:                      genre
    
        $genres:                     genres
    
        $grouping:                   grouping
    
        $images:                     images
    
        $initial_key:                initial_key
    
        $label:                      The label which issued the release. There may
                                     be more than one.
    
        $language:                   The language a release’s track list is
                                     written in. The possible values are taken
                                     from the ISO 639-3 standard.
    
        $length:                     in seconds
    
        $lyricist:                   lyricist
    
        $lyrics:                     lyrics
    
        $mb_albumartistid:           MusicBrainz album artist ID
    
        $mb_albumid:                 MusicBrainz album ID
    
        $mb_artistid:                MusicBrainz artist ID
    
        $mb_releasegroupid:          MusicBrainz releasegroup ID
    
        $mb_releasetrackid:          MusicBrainz release track ID
    
        $mb_trackid:                 MusicBrainz track ID
    
        $mb_workhierarchy_ids:       All IDs in the work hierarchy. This field
                                     corresponds to the field `work_hierarchy`.
                                     The top level work ID appears first. As
                                     separator a slash (/) is used.Example:
                                     e208c5f5-5d37-3dfc-ac0b-999f207c9e46 /
                                     5adc213f-700a-4435-9e95-831ed720f348 /
                                     eafec51f-47c5-3c66-8c36-a524246c85f8
    
        $mb_workid:                  MusicBrainz work ID
    
        $media:                      media
    
        $month:                      The release month of the specific release
    
        $original_date:              original_date
    
        $original_day:               The release day of the original version of
                                     the album
    
        $original_month:             The release month of the original version of
                                     the album
    
        $original_year:              The release year of the original version of
                                     the album
    
        $r128_album_gain:            An optional gain for album normalization
    
        $r128_track_gain:            An optional gain for track normalization
    
        $releasegroup_types:         This field collects all items in the
                                     MusicBrainz’ API  related to type: `type`,
                                     `primary-type and `secondary-type-list`. Main
                                     usage of this field is to determine in a
                                     secure manner if the release is a soundtrack.
    
        $rg_album_gain:              rg_album_gain
    
        $rg_album_peak:              rg_album_peak
    
        $rg_track_gain:              rg_track_gain
    
        $rg_track_peak:              rg_track_peak
    
        $samplerate:                 in kilohertz, with units: e.g., “48kHz”
    
        $script:                     The script used to write the release’s track
                                     list. The possible values are taken from the
                                     ISO 15924 standard.
    
        $title:                      The title of a audio file.
    
        $track:                      track
    
        $tracktotal:                 tracktotal
    
        $work:                       The Musicbrainzs’ work entity.
    
        $work_hierarchy:             The hierarchy of works: The top level work
                                     appears first. As separator is this string
                                     used: -->. Example: Die Zauberflöte, K. 620
                                     --> Die Zauberflöte, K. 620: Akt I --> Die
                                     Zauberflöte, K. 620: Act I, Scene II. No. 2
                                     Aria "Was hör ...
    
        $year:                       The release year of the specific release
    
    Functions
    =========
    
        alpha
        -----
    
        %alpha{text}
            This function first ASCIIfies the given text, then all non alphabet
            characters are replaced with whitespaces.
    
        alphanum
        --------
    
        %alphanum{text}
            This function first ASCIIfies the given text, then all non alpanumeric
            characters are replaced with whitespaces.
    
        asciify
        -------
    
        %asciify{text}
            Translate non-ASCII characters to their ASCII equivalents. For
            example, “café” becomes “cafe”. Uses the mapping provided by the
            unidecode module.
    
        delchars
        --------
    
        %delchars{text,chars}
            Delete every single character of “chars“ in “text”.
    
        deldupchars
        -----------
    
        %deldupchars{text,chars}
            Search for duplicate characters and replace with only one occurrance
            of this characters.
    
        first
        -----
    
        %first{text} or %first{text,count,skip} or
        %first{text,count,skip,sep,join}
            Returns the first item, separated by ; . You can use
            %first{text,count,skip}, where count is the number of items (default
            1) and skip is number to skip (default 0). You can also use
            %first{text,count,skip,sep,join} where sep is the separator, like ; or
            / and join is the text to concatenate the items.
    
        if
        --
    
        %if{condition,truetext} or %if{condition,truetext,falsetext}
            If condition is nonempty (or nonzero, if it’s a number), then returns
            the second argument. Otherwise, returns the third argument if
            specified (or nothing if falsetext is left off).
    
        ifdef
        -----
    
        %ifdef{field}, %ifdef{field,text} or %ifdef{field,text,falsetext}
            If field exists, then return truetext or field (default). Otherwise,
            returns falsetext. The field should be entered without $.
    
        ifdefempty
        ----------
    
        %ifdefempty{field,text} or %ifdefempty{field,text,falsetext}
            If field exists and is empty, then return truetext. Otherwise, returns
            falsetext. The field should be entered without $.
    
        ifdefnotempty
        -------------
    
        %ifdefnotempty{field,text} or %ifdefnotempty{field,text,falsetext}
            If field is not empty, then return truetext. Otherwise, returns
            falsetext. The field should be entered without $.
    
        initial
        -------
    
        %initial{text}
            Get the first character of a text in lowercase. The text is converted
            to ASCII. All non word characters are erased.
    
        left
        ----
    
        %left{text,n}
            Return the first “n” characters of “text”.
    
        lower
        -----
    
        %lower{text}
            Convert “text” to lowercase.
    
        nowhitespace
        ------------
    
        %nowhitespace{text,replace}
            Replace all whitespace characters with replace. By default: a dash (-)
            %nowhitespace{$track,_}
    
        num
        ---
    
        %num{number,count}
            Pad decimal number with leading zeros.
            %num{$track,3}
    
        replchars
        ---------
    
        %replchars{text,chars,replace}
            Replace the characters “chars” in “text” with “replace”.
            %replchars{text,ex,-} > t--t
    
        right
        -----
    
        %right{text,n}
            Return the last “n” characters of “text”.
    
        sanitize
        --------
    
        %sanitize{text}
            Delete in most file systems not allowed characters.
    
        shorten
        -------
    
        %shorten{text} or %shorten{text,max_size}
            Shorten “text” on word boundarys.
            %shorten{$title,32}
    
        time
        ----
    
        %time{date_time,format,curformat}
            Return the date and time in any format accepted by strftime. For
            example, to get the year some music was added to your library, use
            %time{$added,%Y}.
    
        title
        -----
    
        %title{text}
            Convert “text” to Title Case.
    
        upper
        -----
    
        %upper{text}
            Convert “text” to UPPERCASE.
    
    positional arguments:
      source                A folder containing audio files or a audio file
    
    optional arguments:
      -h, --help            show this help message and exit
      -d, --dry-run         Don’t rename or copy the audio files.
      -s FIELD_SKIP, --field-skip FIELD_SKIP
                            Skip renaming if field is empty.
      -v, --version         show program's version number and exit
    
    metadata actions:
      -E, --enrich-metadata
                            Fetch the tag fields “work” and “mb_workid” from
                            Musicbrainz and save this fields into the audio file.
                            The audio file must have the tag field “mb_trackid”.
                            The give audio file is not renamed.
      -r, --remap-classical
    
    rename:
      -p BACKUP_FOLDER, --backup-folder BACKUP_FOLDER
                            Folder to store the backup files in.
      -B, --best-format     Use the best format. This option only takes effect if
                            the target file already exists. `audiorename` now
                            checks the qualtity of the two audio files (source and
                            target). The tool first examines the format. For
                            example a flac file wins over a mp3 file.
                            `audiorename` then checks the bitrate.
      -D, --delete          Delete files.
    
    rename move actions:
      -C, --copy            Copy files instead of rename / move.
      -M, --move            Move / rename a file. This is the default action. The
                            option can be omitted.
      -n, --no-rename       Don’t rename, move, copy dry run. Do nothing.
    
    rename cleanup actions:
      -A, --backup          Backup audio files instead of delete files
    
    filters:
      -F, --album-complete  Rename only complete albums
      -m ALBUM_MIN, --album-min ALBUM_MIN
                            Rename only albums containing at least X files.
      -e EXTENSION, --extension EXTENSION
                            Extensions to rename
    
    formats:
      -k, --classical       Use the default format for classical music. If you use
                            this option, both parameters (--format and
                            --compilation) have no effect. Classical music is
                            sorted by the lastname of the composer.
      -S, --shell-friendly  Rename audio files “shell friendly”, this means
                            without whitespaces, parentheses etc.
    
    format strings:
      -c FORMAT_STRING, --compilation FORMAT_STRING
                            Format string for compilations. Use metadata fields
                            and functions to build the format string.
      -f FORMAT_STRING, --format FORMAT_STRING
                            The default format string for audio files that are not
                            compilations or compilations. Use metadata fields and
                            functions to build the format string.
      --soundtrack FORMAT_STRING
                            Format string for a soundtrack audio file. Use
                            metadata fields and functions to build the format
                            string.
    
    output:
      -K, --color           Colorize the standard output of the program with ANSI
                            colors.
      -b, --debug           Print debug informations about the single metadata
                            fields.
      -j, --job-info        Display informations about the current job. This
                            informations are printted out before any actions on
                            the audio files are executed.
      -l, --mb-track-listing
                            Print track listing for Musicbrainz website: Format:
                            track. title (duration), e. g.: 1. He, Zigeuner (1:31)
                            2. Hochgetürmte Rimaflut (1:21)
      -o, --one-line        Display the rename / copy action status on one line
                            instead of two.
      -T, --stats           Show statistics at the end of the execution.
      -V, --verbose         Make the command line output more verbose.
    
    target:
      -a, --source-as-target
                            Use specified source folder as target directory
      -t TARGET, --target TARGET
                            Target directory

Development
===========

Test
----

::

    tox


Publish a new version
---------------------

::

    git tag 1.1.1
    git push --tags
    python setup.py sdist upload


Package documentation
---------------------

The package documentation is hosted on
`readthedocs <http://audiorename.readthedocs.io>`_.

Generate the package documentation:

::

    python setup.py build_sphinx
