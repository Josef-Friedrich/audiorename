.. image:: http://img.shields.io/pypi/v/audiorename.svg
    :target: https://pypi.python.org/pypi/audiorename

.. image:: https://travis-ci.org/Josef-Friedrich/audiorename.svg?branch=packaging
    :target: https://travis-ci.org/Josef-Friedrich/audiorename


.. code-block:: none


    usage: audiorenamer [-h] [-f FORMAT] [-c COMPILATION] [-S] [-d]
                        [-e EXTENSIONS] [-t TARGET_DIR] [-s SKIP_IF_EMPTY] [-a]
                        [-C] [-m FILTER_ALBUM_MIN] [-F] [--unittest] [-v]
                        path
    
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
    
        $lyrics:               lyrics
    
        $disctitle:            disctitle
    
        $month:                The release month of the specific
                               release
    
        $channels:             channels
    
        $disc:                 disc
    
        $mb_trackid:           MusicBrainz track ID
    
        $composer:             composer
    
        $albumartist_sort:     albumartist_sort
    
        $bitdepth:             only available for some formats
    
        $title:                title
    
        $mb_albumid:           MusicBrainz album ID
    
        $acoustid_fingerprint:    Acoustic ID fingerprint
    
        $mb_releasegroupid:    MusicBrainz releasegroup  ID
    
        $albumartist_credit:    albumartist_credit
    
        $acoustid_id:          Acoustic ID
    
        $format:               e.g., “MP3” or “FLAC”
    
        $encoder:              encoder
    
        $day:                  The release day of the specific
                               release
    
        $original_year:        The release year of the original
                               version of the album
    
        $tracktotal:           tracktotal
    
        $artist:               artist
    
        $mb_albumartistid:     MusicBrainz album artist ID
    
        $bpm:                  bpm
    
        $artist_credit:        The track-specific artist credit
                               name,  which may be a variation
                               of the artist’s “canonical”
                               name
    
        $grouping:             grouping
    
        $disctotal:            disctotal
    
        $albumstatus:          The status describes how
                               "official" a release is. Possible
                               values are: official,
                               promotional, bootleg, pseudo-
                               release
    
        $original_day:         The release day of the original
                               version of the album
    
        $albumartist:          The artist for the entire album,
                               which may be different from the
                               artists for the individual tracks
    
        $year:                 The release year of the specific
                               release
    
        $albumdisambig:        albumdisambig
    
        $samplerate:           in kilohertz, with units: e.g.,
                               “48kHz”
    
        $album:                album
    
        $asin:                 Amazon Standard Identification
                               Number
    
        $media:                media
    
        $artist_sort:          The “sort name” of the track
                               artist (e.g., “Beatles, The”
                               or “White, Jack”)
    
        $comments:             comments
    
        $label:                The label which issued the
                               release. There may be more than
                               one.
    
        $catalognum:           This is a number assigned to the
                               release by the label which can
                               often be found on the spine or
                               near the barcode. There may be
                               more than one, especially when
                               multiple labels are involved.
                               This is not the ASIN — there is
                               a relationship for that — nor
                               the label code.
    
        $original_month:       The release month of the original
                               version of the album
    
        $mb_artistid:          MusicBrainz artist ID
    
        $track:                track
    
        $comp:                 Compilation flag
    
        $genre:                genre
    
        $bitrate:              in kilobits per second, with
                               units: e.g., “192kbps”
    
        $language:             The language a release’s track
                               list is written in. The possible
                               values are taken from the ISO
                               639-3 standard.
    
        $country:              The country the release was
                               issued in.
    
        $script:               The script used to write the
                               release’s track list. The
                               possible values are taken from
                               the ISO 15924 standard.
    
        $length:               in seconds
    
        $albumtype:            The MusicBrainz album type; the
                               MusicBrainz wiki has a list of
                               type names
    
    Functions
    ---------
    
    asciify
    %asciify{text}
    Translate non-ASCII characters to their ASCII equivalents. For example, “café” becomes “cafe”. Uses the mapping provided by the unidecode module.
    
    delchars
    %delchars{text,chars}
    Delete every single character of “chars“ in “text”.
    
    deldupchars
    %deldupchars{text,chars}
    Search for duplicate characters and replace with only one occurrance of this characters.
    
    first
    %first{text}
    Returns the first item, separated by ; . You can use %first{text,count,skip}, where count is the number of items (default 1) and skip is number to skip (default 0). You can also use %first{text,count,skip,sep,join} where sep is the separator, like ; or / and join is the text to concatenate the items.
    
    if
    %if{condition,text} or %if{condition,truetext,falsetext}
    If condition is nonempty (or nonzero, if it’s a number), then returns the second argument. Otherwise, returns the third argument if specified (or nothing if falsetext is left off).
    
    ifdef
    %ifdef{field}, %ifdef{field,truetext} or %ifdef{field,truetext,falsetext}
    If field exists, then return truetext or field (default). Otherwise, returns falsetext. The field should be entered without $.
    
    left
    %left{text,n}
    Return the first “n” characters of “text”.
    
    lower
    %lower{text}
    Convert “text” to lowercase.
    
    replchars
    %replchars{text,chars,replace}
    
    right
    %right{text,n}
    Return the last “n” characters of “text”.
    
    sanitize
    %sanitize{text}
     Delete in most file systems not allowed characters.
    
    shorten
    %shorten{text, max_size}
    Shorten “text” on word boundarys.
    %shorten{$title, 32}
    
    time
    %time{date_time,format,curformat}
    Return the date and time in any format accepted by strftime. For example, to get the year some music was added to your library, use %time{$added,%Y}.
    
    title
    %title{text}
    Convert “text” to Title Case.
    
    upper
    Convert “text” to UPPERCASE.
    
    positional arguments:
      path                  A folder containing audio files or a audio file
    
    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            A format string
      -c COMPILATION, --compilation COMPILATION
                            Format string for compilations
      -S, --shell-friendly  Rename audio files “shell friendly”, this means
                            without whitespaces, parentheses etc.
      -d, --dry-run         Don’t rename or copy the audio files.
      -e EXTENSIONS, --extensions EXTENSIONS
                            Extensions to rename
      -t TARGET_DIR, --target-dir TARGET_DIR
                            Target directory
      -s SKIP_IF_EMPTY, --skip-if-empty SKIP_IF_EMPTY
                            Skip renaming of field is empty.
      -a, --source-as-target-dir
                            Use specified source folder as target directory
      -C, --copy            Copy files instead of rename / move.
      -m FILTER_ALBUM_MIN, --filter-album-min FILTER_ALBUM_MIN
                            Rename only albums containing at least X files.
      -F, --filter-album-complete
                            Rename only complete albums
      --unittest            The audio files are not renamed. Debug messages for
                            the unit test are printed out.
      -v, --version         show program's version number and exit
