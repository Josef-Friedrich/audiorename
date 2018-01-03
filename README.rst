.. image:: http://img.shields.io/pypi/v/audiorename.svg
    :target: https://pypi.python.org/pypi/audiorename

.. image:: https://travis-ci.org/Josef-Friedrich/audiorename.svg?branch=packaging
    :target: https://travis-ci.org/Josef-Friedrich/audiorename

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

    usage: audiorenamer [-h] [-k] [-c COMPILATION] [-C] [-D] [-d] [-e EXTENSION]
                        [-F] [-m album_min] [-f FORMAT]
                        [--mb-track-listing] [-S] [-s SKIP_IF_EMPTY] [-a]
                        [-t TARGET_DIR] [--unittest] [-v] [-V] [-w]
                        path
    
        Rename audio files from metadata tags.
    
        How to specify the target directory?
    
        1. By the default the audio files are moved or renamed to the parent
           working directory.
        2. Use the option ``-t <folder>`` or ``--target-dir <folder>`` to specifiy
           a target directory.
        3. Use the option ``-a`` or ``--source-as-target`` to copy or rename
           your audio files within the source directory.
    
        Metadata fields
        ---------------
    
            $acoustid_fingerprint:    Acoustic ID fingerprint
    
        $acoustid_id:          Acoustic ID
    
        $album:                album
    
        $album_classical:      album_classical
    
        $album_clean:          “album” without ” (Disc
                               X)”.
    
        $album_initial:        First character in lowercase of
                               “album_clean”.
    
        $albumartist:          The artist for the entire album,
                               which may be different from the
                               artists for the individual tracks
    
        $albumartist_credit:    albumartist_credit
    
        $albumartist_sort:     albumartist_sort
    
        $albumdisambig:        albumdisambig
    
        $albumstatus:          The status describes how
                               "official" a release is. Possible
                               values are: official,
                               promotional, bootleg, pseudo-
                               release
    
        $albumtype:            The MusicBrainz album type; the
                               MusicBrainz wiki has a list of
                               type names
    
        $arranger:             arranger
    
        $art:                  art
    
        $artist:               artist
    
        $artist_credit:        The track-specific artist credit
                               name, which may be a variation of
                               the artist’s “canonical”
                               name
    
        $artist_initial:       First character in lowercase of
                               “artistsafe_sort”
    
        $artist_sort:          The “sort name” of the track
                               artist (e.g., “Beatles, The”
                               or “White, Jack”)
    
        $artistsafe:           The first available value of this
                               metatag order: “albumartist”
                               -> “artist” ->
                               “albumartist_credit” ->
                               “artist_credit”
    
        $artistsafe_sort:      The first available value of this
                               metatag order:
                               “albumartist_sort” ->
                               “artist_sort” ->
                               “artistsafe”
    
        $asin:                 Amazon Standard Identification
                               Number
    
        $bitdepth:             only available for some formats
    
        $bitrate:              in kilobits per second, with
                               units: e.g., “192kbps”
    
        $bpm:                  bpm
    
        $catalognum:           This is a number assigned to the
                               release by the label which can
                               often be found on the spine or
                               near the barcode. There may be
                               more than one, especially when
                               multiple labels are involved.
                               This is not the ASIN — there is
                               a relationship for that — nor
                               the label code.
    
        $channels:             channels
    
        $comments:             comments
    
        $comp:                 Compilation flag
    
        $composer:             composer
    
        $composer_initial:     composer_initial
    
        $composer_safe:        composer_safe
    
        $composer_sort:        Composer name for sorting.
    
        $country:              The country the release was
                               issued in.
    
        $date:                 date
    
        $day:                  The release day of the specific
                               release
    
        $disc:                 disc
    
        $disctitle:            disctitle
    
        $disctotal:            disctotal
    
        $disctrack:            Combination of disc and track in
                               the format: disk-track, e.g.
                               1-01, 3-099
    
        $encoder:              encoder
    
        $format:               e.g., “MP3” or “FLAC”
    
        $genre:                genre
    
        $genres:               genres
    
        $grouping:             grouping
    
        $images:               images
    
        $initial_key:          initial_key
    
        $label:                The label which issued the
                               release. There may be more than
                               one.
    
        $language:             The language a release’s track
                               list is written in. The possible
                               values are taken from the ISO
                               639-3 standard.
    
        $length:               in seconds
    
        $lyricist:             lyricist
    
        $lyrics:               lyrics
    
        $mb_albumartistid:     MusicBrainz album artist ID
    
        $mb_albumid:           MusicBrainz album ID
    
        $mb_artistid:          MusicBrainz artist ID
    
        $mb_releasegroupid:    MusicBrainz releasegroup ID
    
        $mb_trackid:           MusicBrainz track ID
    
        $mb_workid:            MusicBrainz work ID
    
        $media:                media
    
        $month:                The release month of the specific
                               release
    
        $original_date:        original_date
    
        $original_day:         The release day of the original
                               version of the album
    
        $original_month:       The release month of the original
                               version of the album
    
        $original_year:        The release year of the original
                               version of the album
    
        $performer_classical:    performer_classical
    
        $r128_album_gain:      An optional gain for album
                               normalization
    
        $r128_track_gain:      An optional gain for track
                               normalization
    
        $rg_album_gain:        rg_album_gain
    
        $rg_album_peak:        rg_album_peak
    
        $rg_track_gain:        rg_track_gain
    
        $rg_track_peak:        rg_track_peak
    
        $samplerate:           in kilohertz, with units: e.g.,
                               “48kHz”
    
        $script:               The script used to write the
                               release’s track list. The
                               possible values are taken from
                               the ISO 15924 standard.
    
        $title:                The title of a audio file.
    
        $title_classical:      title_classical
    
        $track:                track
    
        $track_classical:      track_classical
    
        $tracktotal:           tracktotal
    
        $work:                 The Musicbrainzs’ work entity.
    
        $year:                 The release year of the specific
                               release
    
        $year_safe:            First “original_year” then
                               “year”.
    
        Functions
        ---------
    
            asciify
        -------
    
        %asciify{text}
            Translate non-ASCII characters to their ASCII
            equivalents. For example, “café” becomes “cafe”. Uses
            the mapping             provided by the unidecode module.
    
        delchars
        --------
    
        %delchars{text,chars}
            Delete every single character of “chars“ in “text”.
    
        deldupchars
        -----------
    
        %deldupchars{text,chars}
            Search for duplicate characters and replace with only
            one occurrance of this characters.
    
        first
        -----
    
        %first{text}
            Returns the first item, separated by ; . You can use
            %first{text,count,skip}, where count is the number of items
            (default 1) and skip is number to skip (default 0). You can also
            use %first{text,count,skip,sep,join} where sep is the separator,
            like ; or / and join is the text to concatenate the items.
    
        if
        --
    
        %if{condition,truetext} or             %if{condition,truetext,falsetext}
            If condition is nonempty (or nonzero, if it’s a
            number), then returns the second argument. Otherwise, returns
            the             third argument if specified (or nothing if
            falsetext is left off).
    
        ifdef
        -----
    
        %ifdef{field}, %ifdef{field,text} or
        %ifdef{field,text,falsetext}
            If field exists, then return truetext or field
            (default). Otherwise, returns falsetext. The field should be
            entered without $.
    
        left
        ----
    
        %left{text,n}
            Return the first “n” characters of “text”.
    
        lower
        -----
    
        %lower{text}
            Convert “text” to lowercase.
    
        num
        ---
    
        %num{number, count}
            Pad decimal number with leading zeros.
            %num{$track, 3}
    
        replchars
        ---------
    
        %replchars{text,chars,replace}
    
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
    
        %shorten{text} or %shorten{text, max_size}
            Shorten “text” on word boundarys.
            %shorten{$title, 32}
    
        time
        ----
    
        %time{date_time,format,curformat}
            Return the date and time in any format accepted by
            strftime. For example, to get the year some music was added to
            your library, use %time{$added,%Y}.
    
        title
        -----
    
        %title{text}
            Convert “text” to Title Case.
    
        upper
        -----
    
            Convert “text” to UPPERCASE.
    
    positional arguments:
      path                  A folder containing audio files or a audio file
    
    optional arguments:
      -h, --help            show this help message and exit
      -k, --classical       Use default format for classical music
      -c COMPILATION, --compilation COMPILATION
                            Format string for compilations
      -C, --copy            Copy files instead of rename / move.
      -D, --delete-existing
                            Delete source file if the target file already exists.
      -d, --dry-run         Don’t rename or copy the audio files.
      -e EXTENSION, --extension EXTENSION
                            Extensions to rename
      -F, --album-complete
                            Rename only complete albums
      -m album_min, --album-min album_min
                            Rename only albums containing at least X files.
      -f FORMAT, --format FORMAT
                            A format string
      --mb-track-listing    Print track listing for Musicbrainz website: Format:
                            track. title (duration), e. g.: 1. He, Zigeuner (1:31)
                            2. Hochgetürmte Rimaflut (1:21)
      -S, --shell-friendly  Rename audio files “shell friendly”, this means
                            without whitespaces, parentheses etc.
      -s SKIP_IF_EMPTY, --skip-if-empty SKIP_IF_EMPTY
                            Skip renaming of field is empty.
      -a, --source-as-target
                            Use specified source folder as target directory
      -t TARGET_DIR, --target-dir TARGET_DIR
                            Target directory
      --unittest            The audio files are not renamed. Debug messages for
                            the unit test are printed out.
      -v, --version         show program's version number and exit
      -V, --verbose
      -w, --work            Fetch the tag fields “work” and “mb_workid”
                            from Musicbrainz and save this fields into the audio
                            file. The audio file must have the tag field
                            “mb_trackid”. The give audio file is not renamed.


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
