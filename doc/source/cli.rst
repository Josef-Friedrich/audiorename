Comande line interface
======================

.. code-block:: text

    usage: audiorenamer [-h] [-d] [-s FIELD_SKIP] [-v] [-E] [-r]
                        [-p BACKUP_FOLDER] [-B] [-C | -M | -n] [-A | -D] [-F]
                        [-m ALBUM_MIN] [-e EXTENSION]
                        [--genre-classical GENRE_CLASSICAL] [-k] [-S]
                        [-c FORMAT_STRING] [-f FORMAT_STRING]
                        [--soundtrack FORMAT_STRING]
                        [--format-classical FORMAT_STRING] [-K] [-b] [-j] [-l]
                        [-o] [-T] [-V] [-a] [-t TARGET]
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
                                     Examples: ['86e217b7-d3ad-4493-a9f2-cf71256ace07']
    
        $album:                      album
                                     Examples: ['Help!']
    
        $albumartist:                The artist for the entire album, which may be
                                     different from the artists for the individual
                                     tracks
                                     Examples: ['The Beatles']
    
        $albumartist_credit:         albumartist_credit
    
        $albumartist_sort:           albumartist_sort
                                     Examples: ['Beatles, The']
    
        $albumartists:               albumartists
    
        $albumdisambig:              albumdisambig
    
        $albumstatus:                The status describes how "official" a release
                                     is.
                                     Examples: ['official', 'promotional', 'bootleg', 'pseudo-release']
    
        $albumtype:                  The MusicBrainz album type; the MusicBrainz
                                     wiki has a list of type names
                                     Examples: ['album/soundtrack']
    
        $ar_classical_album:         The field “work” without the movement suffix.
                                     For example: “Horn Concerto: I. Allegro” ->
                                     “Horn Concerto”
    
        $ar_classical_performer:     “ar_performer_short” or “albumartist” without
                                     the composer prefix: “Beethoven; Karajan,
                                     Mutter” -> “Karajan, Mutter”
    
        $ar_classical_title:         The movement title without the parent work
                                     prefix. For example “Horn Concerto: I.
                                     Allegro” -> “I. Allegro”
    
        $ar_classical_track:         If the title contains Roman numbers, then
                                     these are converted to arabic numbers with
                                     leading zeros. If no Roman numbers could be
                                     found, then the field “ar_combined_disctrack”
                                     is used.
    
        $ar_combined_album:          “album” without ” (Disc X)”.
    
        $ar_combined_artist:         The first available value of this metatag
                                     order: “albumartist” -> “artist” ->
                                     “albumartist_credit” -> “artist_credit”
    
        $ar_combined_artist_sort:    The first available value of this metatag
                                     order: “albumartist_sort” -> “artist_sort” ->
                                     “ar_combined_artist”
    
        $ar_combined_composer:       The first not empty field of this field list:
                                     “composer_sort”, “composer”,
                                     “ar_combined_artist”
    
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
    
        $ar_initial_composer:        First character in lowercase of
                                     “ar_combined_composer”. For example “Ludwig
                                     van Beethoven” -> “l”
    
        $arranger:                   arranger
    
        $art:                        art
    
        $artist:                     artist
                                     Examples: ['The Beatles']
    
        $artist_credit:              The track-specific artist credit name, which
                                     may be a variation of the artist’s
                                     “canonical” name
    
        $artist_sort:                The “sort name” of the track artist.
                                     Examples: ['Beatles, The', 'White, Jack']
    
        $artists:                    artists
    
        $asin:                       Amazon Standard Identification Number
                                     Examples: ['B000002UAL']
    
        $barcode:                    There are many different types of barcode,
                                     but the ones usually found on music releases
                                     are two: 1. Universal Product Code (UPC),
                                     which is the original barcode used in North
                                     America. 2. European Article Number (EAN)
                                     Examples: ['5028421931838', '036000291452']
    
        $bitdepth:                   only available for some formats
                                     Examples: [16]
    
        $bitrate:                    in kilobits per second, with units: e.g.,
                                     “192kbps”
                                     Examples: [436523]
    
        $bitrate_mode:               bitrate_mode
    
        $bpm:                        Beats per Minute
    
        $catalognum:                 This is a number assigned to the release by
                                     the label which can often be found on the
                                     spine or near the barcode. There may be more
                                     than one, especially when multiple labels are
                                     involved. This is not the ASIN — there is a
                                     relationship for that — nor the label code.
                                     Examples: ['CDP 7 46439 2']
    
        $channels:                   channels
                                     Examples: [1]
    
        $comments:                   comments
    
        $comp:                       Compilation flag
                                     Examples: [True, False]
    
        $composer:                   The name of the composer.
                                     Examples: ['Ludwig van Beethoven']
    
        $composer_sort:              The composer name for sorting.
                                     Examples: ['Beethoven, Ludwig van']
    
        $copyright:                  copyright
    
        $country:                    The country the release was issued in.
    
        $date:                       date
    
        $day:                        The release day of the specific release
    
        $disc:                       disc
    
        $disctitle:                  disctitle
    
        $disctotal:                  disctotal
    
        $encoder:                    the name of the person or organisation that
                                     encoded the audio file. This field may
                                     contain a copyright message, if the audio
                                     file also is copyrighted by the encoder.
                                     Examples: ['iTunes v7.6.2']
    
        $encoder_info:               encoder_info
    
        $encoder_settings:           encoder_settings
    
        $format:                     e.g., “MP3” or “FLAC”
                                     Examples: ['MP3', 'FLAC']
    
        $genre:                      genre
    
        $genres:                     genres
    
        $grouping:                   grouping
    
        $images:                     images
    
        $initial_key:                The Initial key frame contains the musical
                                     key in which the sound starts. It is
                                     represented as a string with a maximum length
                                     of three characters. The ground keys are
                                     represented with "A","B","C","D","E", "F" and
                                     "G" and halfkeys represented with "b" and
                                     "#". Minor is represented as "m".
                                     Examples: ['Dbm']
    
        $isrc:                       The International Standard Recording Code,
                                     abbreviated to ISRC, is a system of codes
                                     that identify audio and music video
                                     recordings.
                                     Examples: ['CAC118989003', 'ITO101117740']
    
        $label:                      The label which issued the release. There may
                                     be more than one.
                                     Examples: ['Brilliant Classics']
    
        $language:                   The language a release’s track list is
                                     written in. The possible values are taken
                                     from the ISO 639-3 standard.
                                     Examples: ['zxx']
    
        $length:                     in seconds
                                     Examples: [674.4666666666667]
    
        $lyricist:                   lyricist
    
        $lyrics:                     lyrics
    
        $mb_albumartistid:           MusicBrainz album artist ID
                                     Examples: ['1f9df192-a621-4f54-8850-2c5373b7eac9', 'b972f589-fb0e-474e-b64a-803b0364fa75']
    
        $mb_albumartistids:          mb_albumartistids
                                     Examples: [['b972f589-fb0e-474e-b64a-803b0364fa75', 'dea28aa9-1086-4ffa-8739-0ccc759de1ce', 'd2ced2f1-6b58-47cf-ae87-5943e2ab6d99']]
    
        $mb_albumid:                 MusicBrainz album ID
                                     Examples: ['fd6adc77-1489-4a13-9aa0-32951061d92b']
    
        $mb_artistid:                MusicBrainz artist ID
                                     Examples: ['1f9df192-a621-4f54-8850-2c5373b7eac9']
    
        $mb_artistids:               mb_artistids
                                     Examples: [['1f9df192-a621-4f54-8850-2c5373b7eac9']]
    
        $mb_releasegroupid:          MusicBrainz releasegroup ID
                                     Examples: ['f714fd70-aaca-4863-9d0d-2768a53acaeb']
    
        $mb_releasetrackid:          MusicBrainz release track ID
                                     Examples: ['38c8c114-5e3b-484f-8af0-79c47ef9c169']
    
        $mb_trackid:                 MusicBrainz track ID
                                     Examples: ['c390b132-4a44-4e16-bec3-bffbbcaa19aa']
    
        $mb_workhierarchy_ids:       All IDs in the work hierarchy. This field
                                     corresponds to the field `work_hierarchy`.
                                     The top level work ID appears first. A slash
                                     (/) is used as separator.
                                     Examples: ['e208c5f5-5d37-3dfc-ac0b-999f207c9e46 / 5adc213f-700a-4435-9e95-831ed720f348 / eafec51f-47c5-3c66-8c36-a524246c85f8']
    
        $mb_workid:                  MusicBrainz work ID
                                     Examples: ['508ec4b1-9549-38cd-a61e-1f0d120a6118']
    
        $media:                      media
                                     Examples: ['CD']
    
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
    
        $rg_album_gain:              ReplayGain Album Gain, see
                                     https://en.wikipedia.org/wiki/ReplayGain.
    
        $rg_album_peak:              ReplayGain Album Peak, see
                                     https://en.wikipedia.org/wiki/ReplayGain.
    
        $rg_track_gain:              ReplayGain Track Gain, see
                                     https://en.wikipedia.org/wiki/ReplayGain.
                                     Examples: [0.0]
    
        $rg_track_peak:              ReplayGain Track Peak, see
                                     https://en.wikipedia.org/wiki/ReplayGain.
                                     Examples: [0.000244]
    
        $samplerate:                 in kilohertz, with units: e.g., “48kHz”
                                     Examples: [44100]
    
        $script:                     The script used to write the release’s track
                                     list. The possible values are taken from the
                                     ISO 15924 standard.
                                     Examples: ['Latn']
    
        $title:                      The title of a audio file.
                                     Examples: ['32 Variations for Piano in C minor on an Original Theme, WoO 80']
    
        $track:                      The track number.
                                     Examples: [1]
    
        $tracktotal:                 The total track number.
                                     Examples: [12]
    
        $url:                        Uniform Resource Locator.
    
        $work:                       The Musicbrainzs’ work entity.
                                     Examples: ['32 Variations for Piano in C minor on an Original Theme, WoO 80']
    
        $work_hierarchy:             The hierarchy of works: The top level work
                                     appears first. As separator is this string
                                     used: -->.
                                     Examples: ['Die Zauberflöte, K. 620 --> Die Zauberflöte, K. 620: Akt I --> Die Zauberflöte, K. 620: Act I, Scene II. No. 2 Aria "Was hör ...']
    
        $year:                       The release year of the specific release
                                     Examples: [2001]
    
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
      source                A folder containing audio files or a single audio file
    
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
                            example a FLAC file wins over a MP3 file. Then
                            `audiorename` checks the bitrate.
    
    rename move actions:
      -C, --copy            Copy files instead of rename / move.
      -M, --move            Move / rename a file. This is the default action. The
                            option can be omitted.
      -n, --no-rename       Don’t rename, move, copy or perform a dry run. Do
                            nothing.
    
    rename cleaning actions:
      The cleaning actions are only executed if the target file already exists.
    
      -A, --backup          Backup the audio files instead of deleting them. The
                            backup directory can be specified with the --backup-
                            folder option.
      -D, --delete          Delete the audio files instead of creating a backup.
    
    filters:
      -F, --album-complete  Rename only complete albums
      -m ALBUM_MIN, --album-min ALBUM_MIN
                            Rename only albums containing at least X files.
      -e EXTENSION, --extension EXTENSION
                            Extensions to rename
      --genre-classical GENRE_CLASSICAL
                            List of genres to be classical
    
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
      --format-classical FORMAT_STRING
                            Format string for classical audio file. Use metadata
                            fields and functions to build the format string.
    
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
