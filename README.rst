.. image:: http://img.shields.io/pypi/v/audiorename.svg
    :target: https://pypi.python.org/pypi/audiorename
    :alt: This package on the Python Package Index

.. image:: https://github.com/Josef-Friedrich/audiorename/actions/workflows/test.yml/badge.svg
    :target: https://github.com/Josef-Friedrich/audiorename/actions/workflows/test.yml
    :alt: Tests

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

Examples
========

Please use the ``-d`` (``--dry-run``) option first

Basic example:

.. code:: Shell

    cd my-chaotic-music-collection
    audiorenamer -d .


More advanced example:

.. code:: Shell

    audiorenamer -d -f '$artist/$album/$track $title' --target /mnt/hd/my-organized-music-collection .

Very advanced example:

.. code:: Shell

    audiorenamer -d -f '$ar_initial_artist/%shorten{$ar_combined_artist_sort}/%shorten{$ar_combined_album}%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/${ar_combined_disctrack}_%shorten{$title}' .

Usage
=====

.. code-block:: text

    usage: audiorenamer [-h] [--config CONFIG] [-v] [-t TARGET] [-a]
                        [-p BACKUP_FOLDER] [-B] [-d] [-C | -M | -n] [-A | -D] [-F]
                        [-m ALBUM_MIN] [-e EXTENSION]
                        [--genre-classical GENRE_CLASSICAL] [-s FIELD_SKIP] [-k]
                        [-S] [--no-soundtrack] [-f PATH_TEMPLATE]
                        [-c PATH_TEMPLATE] [--soundtrack PATH_TEMPLATE]
                        [--format-classical PATH_TEMPLATE] [-K | --no-color] [-b]
                        [-j] [-l] [-o] [-T] [-V] [-E] [-r]
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
    
        $albumdisambig:              The disambiguation album field helps to
                                     distinguish between identically named albums.
                                     The album “Weezer” for example has the
                                     disambiguation comments “Red Album” and
                                     “Green Album”.
    
        $albumstatus:                The status describes how "official" a release
                                     is.
                                     Examples: ['official', 'promotional', 'bootleg', 'pseudo-release']
    
        $albumtype:                  The MusicBrainz album type; the MusicBrainz
                                     wiki has a list of type names
                                     Examples: ['album/soundtrack']
    
        $ar_classical_album:         The field “work” without the movement suffix.
                                     For example: “Horn Concerto: I. Allegro” ->
                                     “Horn Concerto”
                                     Examples: ['Horn Concerto', 'Die Meistersinger von Nürnberg']
    
        $ar_classical_performer:     “ar_performer_short” or “albumartist” without
                                     the composer prefix: “Beethoven; Karajan,
                                     Mutter” -> “Karajan, Mutter”
                                     Examples: ['Karajan, Mutter', 'Karajan, StaDre']
    
        $ar_classical_title:         The movement title without the parent work
                                     prefix. For example “Horn Concerto: I.
                                     Allegro” -> “I. Allegro”
                                     Examples: ['I. Allegro', 'Akt III, Szene V. "Morgendlich leuchtend im rosigen Schein" (Walther, Volk, Meister, Sachs, Pogner, Eva)']
    
        $ar_classical_track:         If the title contains Roman numbers, then
                                     these are converted to arabic numbers with
                                     leading zeros. If no Roman numbers could be
                                     found, then the field “ar_combined_disctrack”
                                     is used.
                                     Examples: ['01', '4-08']
    
        $ar_combined_album:          “album” without ” (Disc X)”.
                                     Examples: ['Headlines and Deadlines: The Hits of a-ha', 'Die Meistersinger von Nürnberg']
    
        $ar_combined_artist:         The first available value of this metatag
                                     order: “albumartist” -> “artist” ->
                                     “albumartist_credit” -> “artist_credit”
                                     Examples: ['a-ha', 'Richard Wagner; René Kollo, Helen Donath, ...']
    
        $ar_combined_artist_sort:    The first available value of this metatag
                                     order: “albumartist_sort” -> “artist_sort” ->
                                     “ar_combined_artist”
                                     Examples: ['a-ha', 'Wagner, Richard; Kollo, René, Donath, Helen...']
    
        $ar_combined_composer:       The first not empty field of this field list:
                                     “composer_sort”, “composer”,
                                     “ar_combined_artist”
                                     Examples: ['Beethoven, Ludwig-van', 'Wagner, Richard']
    
        $ar_combined_disctrack:      Combination of disc and track in the format:
                                     disk-track
                                     Examples: ['1-01', '3-099']
    
        $ar_combined_soundtrack:     Boolean flag which indicates if the audio
                                     file is a soundtrack
                                     Examples: [True, False]
    
        $ar_combined_work_top:       The work on the top level of a work
                                     hierarchy.
                                     Examples: ['Horn Concerto: I. Allegro', 'Die Meistersinger von Nürnberg']
    
        $ar_combined_year:           First “original_year” then “year”.
                                     Examples: [1978]
    
        $ar_initial_album:           First character in lowercase of
                                     “ar_combined_album”. Allowed characters:
                                     [a-z, 0, _], 0-9 -> 0, ? -> _. For example
                                     “Help!” -> “h”.
                                     Examples: ['h']
    
        $ar_initial_artist:          First character in lowercase of
                                     “ar_combined_artist_sort”. Allowed
                                     characters: [a-z, 0, _], 0-9 -> 0, ? -> _.
                                     For example “Brendel, Alfred” -> “b”.
                                     Examples: ['b']
    
        $ar_initial_composer:        First character in lowercase of
                                     “ar_combined_composer”. Allowed characters:
                                     [a-z, 0, _], 0-9 -> 0, ? -> _. For example
                                     “Ludwig van Beethoven” -> “l”.
                                     Examples: ['l']
    
        $ar_performer:               Performer names.
                                     Examples: ['Herbert von Karajan, Staatskapelle Dresden']
    
        $ar_performer_raw:           Raw performer names.
                                     Examples: [[['conductor', 'Herbert von Karajan'], ['orchestra', 'Staatskapelle Dresden']]]
    
        $ar_performer_short:         Abbreviated performer names.
                                     Examples: ['Karajan, StaDre']
    
        $arranger:                   A musician who creates arrangements.
    
        $art:                        Legacy album art field.
                                     Examples: [b'\xff\xd8\xff\xe0\x00']
    
        $artist:                     artist
                                     Examples: ['The Beatles']
    
        $artist_credit:              The track-specific artist credit name, which
                                     may be a variation of the artist’s
                                     “canonical” name
    
        $artist_sort:                The “sort name” of the track artist.
                                     Examples: ['Beatles, The', 'White, Jack']
    
        $artists:                    artists
                                     Examples: [['a-ha']]
    
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
                                     Examples: [436523, 256000]
    
        $bitrate_mode:               bitrate_mode
                                     Examples: ['CBR']
    
        $bpm:                        Beats per Minute
    
        $catalognum:                 This is a number assigned to the release by
                                     the label which can often be found on the
                                     spine or near the barcode. There may be more
                                     than one, especially when multiple labels are
                                     involved. This is not the ASIN — there is a
                                     relationship for that — nor the label code.
                                     Examples: ['CDP 7 46439 2']
    
        $channels:                   channels
                                     Examples: [1, 2]
    
        $comments:                   comments
    
        $comp:                       Compilation flag
                                     Examples: [True, False]
    
        $composer:                   The name of the composer.
                                     Examples: ['Ludwig van Beethoven']
    
        $composer_sort:              The composer name for sorting.
                                     Examples: ['Beethoven, Ludwig van']
    
        $copyright:                  copyright
    
        $country:                    The country the release was issued in.
    
        $date:                       The release data of the specific release.
                                     Examples: ['1996-01-01']
    
        $day:                        The release day of the specific release.
    
        $disc:                       disc
                                     Examples: [1]
    
        $disctitle:                  disctitle
    
        $disctotal:                  disctotal
                                     Examples: [1]
    
        $encoder:                    the name of the person or organisation that
                                     encoded the audio file. This field may
                                     contain a copyright message, if the audio
                                     file also is copyrighted by the encoder.
                                     Examples: ['iTunes v7.6.2']
    
        $encoder_info:               encoder_info
                                     Examples: ['LAME 3.92.0+']
    
        $encoder_settings:           encoder_settings
                                     Examples: ['-b 255+']
    
        $format:                     e.g., “MP3” or “FLAC”
                                     Examples: ['MP3', 'FLAC']
    
        $genre:                      genre
    
        $genres:                     genres
    
        $grouping:                   A content group, which is a collection of
                                     media items such as a CD boxed set.
    
        $images:                     images
                                     Examples: [['<mediafile.Image object at 0x7f51fce26b20>']]
    
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
                                     Examples: ['Brilliant Classics', 'wea']
    
        $language:                   The language a release’s track list is
                                     written in. The possible values are taken
                                     from the ISO 639-3 standard.
                                     Examples: ['zxx', 'eng']
    
        $length:                     The length of a recording in seconds.
                                     Examples: [674.4666666666667]
    
        $lyricist:                   The writer of the text or lyrics in the
                                     recording.
    
        $lyrics:                     The lyrics of the song or a text
                                     transcription of other vocal activities.
    
        $mb_albumartistid:           MusicBrainz album artist ID.
                                     Examples: ['1f9df192-a621-4f54-8850-2c5373b7eac9', 'b972f589-fb0e-474e-b64a-803b0364fa75']
    
        $mb_albumartistids:          MusicBrainz album artist IDs as a list.
                                     Examples: [['b972f589-fb0e-474e-b64a-803b0364fa75', 'dea28aa9-1086-4ffa-8739-0ccc759de1ce', 'd2ced2f1-6b58-47cf-ae87-5943e2ab6d99']]
    
        $mb_albumid:                 MusicBrainz album ID.
                                     Examples: ['fd6adc77-1489-4a13-9aa0-32951061d92b']
    
        $mb_artistid:                MusicBrainz artist ID.
                                     Examples: ['1f9df192-a621-4f54-8850-2c5373b7eac9']
    
        $mb_artistids:               MusicBrainz artist IDs as a list.
                                     Examples: [['1f9df192-a621-4f54-8850-2c5373b7eac9']]
    
        $mb_releasegroupid:          MusicBrainz releasegroup ID.
                                     Examples: ['f714fd70-aaca-4863-9d0d-2768a53acaeb']
    
        $mb_releasetrackid:          MusicBrainz release track ID.
                                     Examples: ['38c8c114-5e3b-484f-8af0-79c47ef9c169']
    
        $mb_trackid:                 MusicBrainz track ID.
                                     Examples: ['c390b132-4a44-4e16-bec3-bffbbcaa19aa']
    
        $mb_workhierarchy_ids:       All IDs in the work hierarchy. This field
                                     corresponds to the field `work_hierarchy`.
                                     The top level work ID appears first. A slash
                                     (/) is used as separator.
                                     Examples: ['e208c5f5-5d37-3dfc-ac0b-999f207c9e46 / 5adc213f-700a-4435-9e95-831ed720f348 / eafec51f-47c5-3c66-8c36-a524246c85f8']
    
        $mb_workid:                  MusicBrainz work ID.
                                     Examples: ['508ec4b1-9549-38cd-a61e-1f0d120a6118']
    
        $media:                      A prototypical medium is one of the physical,
                                     separate things you would get when you buy
                                     something in a record store.
                                     Examples: ['CD']
    
        $month:                      The release month of the specific release.
                                     Examples: [11]
    
        $original_date:              The release date of the original version of
                                     the album.
                                     Examples: ['1991-11-04']
    
        $original_day:               The release day of the original version of
                                     the album.
                                     Examples: [4]
    
        $original_month:             The release month of the original version of
                                     the album.
                                     Examples: [11]
    
        $original_year:              The release year of the original version of
                                     the album.
                                     Examples: [1991]
    
        $r128_album_gain:            An optional gain for album normalization. EBU
                                     R 128 is a recommendation for loudness
                                     normalisation and maximum level of audio
                                     signals.
    
        $r128_track_gain:            An optional gain for track normalization. EBU
                                     R 128 is a recommendation for loudness
                                     normalisation and maximum level of audio
                                     signals.
    
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
    
        $samplerate:                 The sample rate as an integer number.
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
    
        $year:                       The release year of the specific release.
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
    
    Configuration file
    ==================
    
        [selection]
        source = /home/user/source
        target = /home/user/target
        source_as_target = False
        
        [rename]
        backup_folder = /tmp/backup
        best_format = True
        dry_run = False
        
        ; see --move, --copy or --no-rename
        ; “move”, “copy” or “no_rename”
        move_action = move
        
        ; see --backup, --delete
        ; “backup”, “delete” or “do_nothing”
        cleaning_action = do_nothing
        
        [filters]
        album_complete = False
        album_min = 7
        extension = mp3,m4a,flac,wma
        genre_classical = Classical music,Opera,Symphony
        field_skip = title
        
        [template_settings]
        classical = False
        shell_friendly = False
        no_soundtrack = False
        
        [path_templates]
        default_template = $ar_initial_artist/%shorten{$ar_combined_artist_sort}/%shorten{$ar_combined_album}%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/${ar_combined_disctrack}_%shorten{$title}
        compilation_template = _compilations/$ar_initial_album/%shorten{$ar_combined_album}%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/${ar_combined_disctrack}_%shorten{$title}
        soundtrack_template = _soundtrack/$ar_initial_album/%shorten{$ar_combined_album}%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/${ar_combined_disctrack}_${artist}_%shorten{$title}
        classical_template = $ar_initial_composer/$ar_combined_composer/%shorten{$ar_combined_work_top,48}_[%shorten{$ar_classical_performer,32}]/${ar_combined_disctrack}_%shorten{$ar_classical_title,64}%ifdefnotempty{acoustid_id,_%shorten{$acoustid_id,8}}
        
        [cli_output]
        ; see --color or --no-color
        color = True
        
        debug = False
        job_info = False
        mb_track_listing = False
        one_line = False
        stats = True
        verbose = False
        
        [metadata_actions]
        enrich_metadata = False
        remap_classical = False
        
    
    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG       Load a configuration file in INI format.
      -v, --version         show program's version number and exit
    
    [selection]:
      The following arguments are intended to select the audio files.
    
      source                A folder containing audio files or a single audio
                            file. If you specify a folder, the program will search
                            for audio files in all subfolders. If you want to
                            rename the audio files in the current working
                            directory, then specify a dot (“.”).
      -t TARGET, --target TARGET
                            Target directory
      -a, --source-as-target
                            Use specified source folder as target directory
    
    [rename]:
      These options configure the actual renaming process.
    
      -p BACKUP_FOLDER, --backup-folder BACKUP_FOLDER
                            Folder to store the backup files in.
      -B, --best-format     Use the best format. This option only takes effect if
                            the target file already exists. `audiorename` now
                            checks the qualtity of the two audio files (source and
                            target). The tool first examines the format. For
                            example a FLAC file wins over a MP3 file. Then
                            `audiorename` checks the bitrate.
      -d, --dry-run         Don’t rename or copy the audio files.
    
    move action:
      -C, --copy            Copy files instead of rename / move.
      -M, --move            Move / rename a file. This is the default action. The
                            option can be omitted.
      -n, --no-rename       Don’t rename, move, copy or perform a dry run. Do
                            nothing.
    
    cleaning action:
      The cleaning actions are only executed if the target file already exists.
    
      -A, --backup          Backup the audio files instead of deleting them. The
                            backup directory can be specified with the --backup-
                            folder option.
      -D, --delete          Delete the audio files instead of creating a backup.
    
    [filters]:
      The following options filter the music files that are renamed according to certain rules.
    
      -F, --album-complete  Rename only complete albums.
      -m ALBUM_MIN, --album-min ALBUM_MIN
                            Rename only albums containing at least X files.
      -e EXTENSION, --extension EXTENSION
                            Extensions to rename.
      --genre-classical GENRE_CLASSICAL
                            List of genres to be classical.
      -s FIELD_SKIP, --field-skip FIELD_SKIP
                            Skip renaming if field is empty.
    
    [template_settings]:
      -k, --classical       Use the default format for classical music. If you use
                            this option, both parameters (--default and
                            --compilation) have no effect. Classical music is
                            sorted by the lastname of the composer.
      -S, --shell-friendly  Rename audio files “shell friendly”, this means
                            without whitespaces, parentheses etc.
      --no-soundtrack       Do not use the path template for soundtracks. Use
                            instead the default path template.
    
    [path_templates]:
      audiorename provides default path templates. You can specify your own path templates using the following options.
    
      -f PATH_TEMPLATE, --default PATH_TEMPLATE, --format PATH_TEMPLATE
                            The default path template for audio files that are not
                            compilations or compilations. Use metadata fields and
                            functions to build the path template.
      -c PATH_TEMPLATE, --compilation PATH_TEMPLATE
                            Path template for compilations. Use metadata fields
                            and functions to build the path template.
      --soundtrack PATH_TEMPLATE
                            Path template for a soundtrack audio file. Use
                            metadata fields and functions to build the path
                            template.
      --format-classical PATH_TEMPLATE
                            Path template for classical audio file. Use metadata
                            fields and functions to build the path template.
    
    [cli_output]:
      This group contains all options that affect the output on the command line interface (cli).
    
      -K, --color           Colorize the standard output of the program with ANSI
                            colors.
      --no-color            Don’t colorize the standard output of the program with
                            ANSI colors.
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
    
    [metadata_actions]:
      -E, --enrich-metadata
                            Fetch the tag fields “work” and “mb_workid” from
                            Musicbrainz and save this fields into the audio file.
                            The audio file must have the tag field “mb_trackid”.
                            The give audio file is not renamed.
      -r, --remap-classical
                            Remap some fields to fit better for classical music:
                            “composer” becomes “artist”, “work” becomes “album”,
                            from the “title” the work prefix is removed
                            (“Symphonie No. 9: I. Allegro” -> “I. Allegro”) and
                            “track” becomes the movement number. All overwritten
                            fields are safed in the “comments” field.
    

Example configuration file
==========================

Use the ``--config`` option to load a configuration file. The command
line arguments overwrite the corresponding options of the configuration
file.

.. code-block:: Shell

    audiorenamer --config /home/user/my-config.ini

Almost all command line arguments have a corresponding option in the
configuration file. ``audiorename`` implements a basic configuration
language which provides a structure similar to what’s found in Microsoft
Windows `INI
<https://docs.python.org/3/library/configparser.html#supported-ini-file-structure>`_
files:

.. code-block:: ini

    [selection]
    source = /home/user/source
    target = /home/user/target
    source_as_target = False
    
    [rename]
    backup_folder = /tmp/backup
    best_format = True
    dry_run = False
    
    ; see --move, --copy or --no-rename
    ; “move”, “copy” or “no_rename”
    move_action = move
    
    ; see --backup, --delete
    ; “backup”, “delete” or “do_nothing”
    cleaning_action = do_nothing
    
    [filters]
    album_complete = False
    album_min = 7
    extension = mp3,m4a,flac,wma
    genre_classical = Classical music,Opera,Symphony
    field_skip = title
    
    [template_settings]
    classical = False
    shell_friendly = False
    no_soundtrack = False
    
    [path_templates]
    default_template = $ar_initial_artist/%shorten{$ar_combined_artist_sort}/%shorten{$ar_combined_album}%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/${ar_combined_disctrack}_%shorten{$title}
    compilation_template = _compilations/$ar_initial_album/%shorten{$ar_combined_album}%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/${ar_combined_disctrack}_%shorten{$title}
    soundtrack_template = _soundtrack/$ar_initial_album/%shorten{$ar_combined_album}%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/${ar_combined_disctrack}_${artist}_%shorten{$title}
    classical_template = $ar_initial_composer/$ar_combined_composer/%shorten{$ar_combined_work_top,48}_[%shorten{$ar_classical_performer,32}]/${ar_combined_disctrack}_%shorten{$ar_classical_title,64}%ifdefnotempty{acoustid_id,_%shorten{$acoustid_id,8}}
    
    [cli_output]
    ; see --color or --no-color
    color = True
    
    debug = False
    job_info = False
    mb_track_listing = False
    one_line = False
    stats = True
    verbose = False
    
    [metadata_actions]
    enrich_metadata = False
    remap_classical = False
    

Metadata fields
===============


.. list-table:: Fields documentation
   :widths: 20 10 50 20
   :header-rows: 1

   * - Field name
     - Category
     - Description
     - Examples
   * - acoustid_fingerprint
     - music_brainz
     - Acoustic ID fingerprint
     - 
   * - acoustid_id
     - music_brainz
     - Acoustic ID
     - ``86e217b7-d3ad-4493-a9f2-cf71256ace07``
   * - album
     - common
     - album
     - ``Help!``
   * - albumartist
     - common
     - The artist for the entire album, which may be different from the artists for the individual tracks
     - ``The Beatles``
   * - albumartist_credit
     - common
     - albumartist_credit
     - 
   * - albumartist_sort
     - common
     - albumartist_sort
     - ``Beatles, The``
   * - albumartists
     - common
     - albumartists
     - 
   * - albumdisambig
     - common
     - The disambiguation album field helps to distinguish between identically named albums. The album “Weezer” for example has the disambiguation comments “Red Album” and “Green Album”.
     - 
   * - albumstatus
     - common
     - The status describes how "official" a release is.
     - ``official``, ``promotional``, ``bootleg``, ``pseudo-release``
   * - albumtype
     - common
     - The MusicBrainz album type; the MusicBrainz wiki has a list of type names
     - ``album/soundtrack``
   * - ar_classical_album
     - common
     - The field “work” without the movement suffix. For example: “Horn Concerto: I. Allegro” -> “Horn Concerto”
     - ``Horn Concerto``, ``Die Meistersinger von Nürnberg``
   * - ar_classical_performer
     - common
     - “ar_performer_short” or “albumartist” without the composer prefix: “Beethoven; Karajan, Mutter” -> “Karajan, Mutter”
     - ``Karajan, Mutter``, ``Karajan, StaDre``
   * - ar_classical_title
     - common
     - The movement title without the parent work prefix. For example “Horn Concerto: I. Allegro” -> “I. Allegro”
     - ``I. Allegro``, ``Akt III, Szene V. "Morgendlich leuchtend im rosigen Schein" (Walther, Volk, Meister, Sachs, Pogner, Eva)``
   * - ar_classical_track
     - common
     - If the title contains Roman numbers, then these are converted to arabic numbers with leading zeros. If no Roman numbers could be found, then the field “ar_combined_disctrack” is used.
     - ``01``, ``4-08``
   * - ar_combined_album
     - common
     - “album” without ” (Disc X)”.
     - ``Headlines and Deadlines: The Hits of a-ha``, ``Die Meistersinger von Nürnberg``
   * - ar_combined_artist
     - common
     - The first available value of this metatag order: “albumartist” -> “artist” -> “albumartist_credit” -> “artist_credit”
     - ``a-ha``, ``Richard Wagner; René Kollo, Helen Donath, ...``
   * - ar_combined_artist_sort
     - common
     - The first available value of this metatag order: “albumartist_sort” -> “artist_sort” -> “ar_combined_artist”
     - ``a-ha``, ``Wagner, Richard; Kollo, René, Donath, Helen...``
   * - ar_combined_composer
     - common
     - The first not empty field of this field list: “composer_sort”, “composer”, “ar_combined_artist”
     - ``Beethoven, Ludwig-van``, ``Wagner, Richard``
   * - ar_combined_disctrack
     - common
     - Combination of disc and track in the format: disk-track
     - ``1-01``, ``3-099``
   * - ar_combined_soundtrack
     - common
     - Boolean flag which indicates if the audio file is a soundtrack
     - ``True``, ``False``
   * - ar_combined_work_top
     - common
     - The work on the top level of a work hierarchy.
     - ``Horn Concerto: I. Allegro``, ``Die Meistersinger von Nürnberg``
   * - ar_combined_year
     - common
     - First “original_year” then “year”.
     - ``1978``
   * - ar_initial_album
     - common
     - First character in lowercase of “ar_combined_album”. Allowed characters: [a-z, 0, _], 0-9 -> 0, ? -> _. For example “Help!” -> “h”.
     - ``h``
   * - ar_initial_artist
     - common
     - First character in lowercase of “ar_combined_artist_sort”. Allowed characters: [a-z, 0, _], 0-9 -> 0, ? -> _. For example “Brendel, Alfred” -> “b”.
     - ``b``
   * - ar_initial_composer
     - common
     - First character in lowercase of “ar_combined_composer”. Allowed characters: [a-z, 0, _], 0-9 -> 0, ? -> _. For example “Ludwig van Beethoven” -> “l”.
     - ``l``
   * - ar_performer
     - common
     - Performer names.
     - ``Herbert von Karajan, Staatskapelle Dresden``
   * - ar_performer_raw
     - common
     - Raw performer names.
     - ``[['conductor', 'Herbert von Karajan'], ['orchestra', 'Staatskapelle Dresden']]``
   * - ar_performer_short
     - common
     - Abbreviated performer names.
     - ``Karajan, StaDre``
   * - arranger
     - common
     - A musician who creates arrangements.
     - 
   * - art
     - common
     - Legacy album art field.
     - ``b'\xff\xd8\xff\xe0\x00'``
   * - artist
     - common
     - artist
     - ``The Beatles``
   * - artist_credit
     - common
     - The track-specific artist credit name, which may be a variation of the artist’s “canonical” name
     - 
   * - artist_sort
     - common
     - The “sort name” of the track artist.
     - ``Beatles, The``, ``White, Jack``
   * - artists
     - common
     - artists
     - ``['a-ha']``
   * - asin
     - common
     - Amazon Standard Identification Number
     - ``B000002UAL``
   * - barcode
     - common
     - There are many different types of barcode, but the ones usually found on music releases are two: 1. Universal Product Code (UPC), which is the original barcode used in North America. 2. European Article Number (EAN)
     - ``5028421931838``, ``036000291452``
   * - bitdepth
     - audio
     - only available for some formats
     - ``16``
   * - bitrate
     - audio
     - in kilobits per second, with units: e.g., “192kbps”
     - ``436523``, ``256000``
   * - bitrate_mode
     - common
     - bitrate_mode
     - ``CBR``
   * - bpm
     - common
     - Beats per Minute
     - 
   * - catalognum
     - common
     - This is a number assigned to the release by the label which can often be found on the spine or near the barcode. There may be more than one, especially when multiple labels are involved. This is not the ASIN — there is a relationship for that — nor the label code.
     - ``CDP 7 46439 2``
   * - channels
     - audio
     - channels
     - ``1``, ``2``
   * - comments
     - common
     - comments
     - 
   * - comp
     - common
     - Compilation flag
     - ``True``, ``False``
   * - composer
     - common
     - The name of the composer.
     - ``Ludwig van Beethoven``
   * - composer_sort
     - common
     - The composer name for sorting.
     - ``Beethoven, Ludwig van``
   * - copyright
     - common
     - copyright
     - 
   * - country
     - common
     - The country the release was issued in.
     - 
   * - date
     - date
     - The release data of the specific release.
     - ``1996-01-01``
   * - day
     - date
     - The release day of the specific release.
     - 
   * - disc
     - common
     - disc
     - ``1``
   * - disctitle
     - common
     - disctitle
     - 
   * - disctotal
     - common
     - disctotal
     - ``1``
   * - encoder
     - common
     - the name of the person or organisation that encoded the audio file. This field may contain a copyright message, if the audio file also is copyrighted by the encoder.
     - ``iTunes v7.6.2``
   * - encoder_info
     - common
     - encoder_info
     - ``LAME 3.92.0+``
   * - encoder_settings
     - common
     - encoder_settings
     - ``-b 255+``
   * - format
     - audio
     - e.g., “MP3” or “FLAC”
     - ``MP3``, ``FLAC``
   * - genre
     - common
     - genre
     - 
   * - genres
     - common
     - genres
     - 
   * - grouping
     - common
     - A content group, which is a collection of media items such as a CD boxed set.
     - 
   * - images
     - common
     - images
     - ``['<mediafile.Image object at 0x7f51fce26b20>']``
   * - initial_key
     - common
     - The Initial key frame contains the musical key in which the sound starts. It is represented as a string with a maximum length of three characters. The ground keys are represented with "A","B","C","D","E", "F" and "G" and halfkeys represented with "b" and "#". Minor is represented as "m".
     - ``Dbm``
   * - isrc
     - common
     - The International Standard Recording Code, abbreviated to ISRC, is a system of codes that identify audio and music video recordings.
     - ``CAC118989003``, ``ITO101117740``
   * - label
     - common
     - The label which issued the release. There may be more than one.
     - ``Brilliant Classics``, ``wea``
   * - language
     - common
     - The language a release’s track list is written in. The possible values are taken from the ISO 639-3 standard.
     - ``zxx``, ``eng``
   * - length
     - audio
     - The length of a recording in seconds.
     - ``674.4666666666667``
   * - lyricist
     - common
     - The writer of the text or lyrics in the recording.
     - 
   * - lyrics
     - common
     - The lyrics of the song or a text transcription of other vocal activities.
     - 
   * - mb_albumartistid
     - music_brainz
     - MusicBrainz album artist ID.
     - ``1f9df192-a621-4f54-8850-2c5373b7eac9``, ``b972f589-fb0e-474e-b64a-803b0364fa75``
   * - mb_albumartistids
     - music_brainz
     - MusicBrainz album artist IDs as a list.
     - ``['b972f589-fb0e-474e-b64a-803b0364fa75', 'dea28aa9-1086-4ffa-8739-0ccc759de1ce', 'd2ced2f1-6b58-47cf-ae87-5943e2ab6d99']``
   * - mb_albumid
     - music_brainz
     - MusicBrainz album ID.
     - ``fd6adc77-1489-4a13-9aa0-32951061d92b``
   * - mb_artistid
     - music_brainz
     - MusicBrainz artist ID.
     - ``1f9df192-a621-4f54-8850-2c5373b7eac9``
   * - mb_artistids
     - music_brainz
     - MusicBrainz artist IDs as a list.
     - ``['1f9df192-a621-4f54-8850-2c5373b7eac9']``
   * - mb_releasegroupid
     - music_brainz
     - MusicBrainz releasegroup ID.
     - ``f714fd70-aaca-4863-9d0d-2768a53acaeb``
   * - mb_releasetrackid
     - music_brainz
     - MusicBrainz release track ID.
     - ``38c8c114-5e3b-484f-8af0-79c47ef9c169``
   * - mb_trackid
     - music_brainz
     - MusicBrainz track ID.
     - ``c390b132-4a44-4e16-bec3-bffbbcaa19aa``
   * - mb_workhierarchy_ids
     - music_brainz
     - All IDs in the work hierarchy. This field corresponds to the field `work_hierarchy`. The top level work ID appears first. A slash (/) is used as separator.
     - ``e208c5f5-5d37-3dfc-ac0b-999f207c9e46 / 5adc213f-700a-4435-9e95-831ed720f348 / eafec51f-47c5-3c66-8c36-a524246c85f8``
   * - mb_workid
     - music_brainz
     - MusicBrainz work ID.
     - ``508ec4b1-9549-38cd-a61e-1f0d120a6118``
   * - media
     - common
     - A prototypical medium is one of the physical, separate things you would get when you buy something in a record store.
     - ``CD``
   * - month
     - date
     - The release month of the specific release.
     - ``11``
   * - original_date
     - date
     - The release date of the original version of the album.
     - ``1991-11-04``
   * - original_day
     - date
     - The release day of the original version of the album.
     - ``4``
   * - original_month
     - date
     - The release month of the original version of the album.
     - ``11``
   * - original_year
     - date
     - The release year of the original version of the album.
     - ``1991``
   * - r128_album_gain
     - r128
     - An optional gain for album normalization. EBU R 128 is a recommendation for loudness normalisation and maximum level of audio signals.
     - 
   * - r128_track_gain
     - r128
     - An optional gain for track normalization. EBU R 128 is a recommendation for loudness normalisation and maximum level of audio signals.
     - 
   * - releasegroup_types
     - music_brainz
     - This field collects all items in the MusicBrainz’ API  related to type: `type`, `primary-type and `secondary-type-list`. Main usage of this field is to determine in a secure manner if the release is a soundtrack.
     - 
   * - rg_album_gain
     - rg
     - ReplayGain Album Gain, see https://en.wikipedia.org/wiki/ReplayGain.
     - 
   * - rg_album_peak
     - rg
     - ReplayGain Album Peak, see https://en.wikipedia.org/wiki/ReplayGain.
     - 
   * - rg_track_gain
     - rg
     - ReplayGain Track Gain, see https://en.wikipedia.org/wiki/ReplayGain.
     - ``0.0``
   * - rg_track_peak
     - rg
     - ReplayGain Track Peak, see https://en.wikipedia.org/wiki/ReplayGain.
     - ``0.000244``
   * - samplerate
     - audio
     - The sample rate as an integer number.
     - ``44100``
   * - script
     - common
     - The script used to write the release’s track list. The possible values are taken from the ISO 15924 standard.
     - ``Latn``
   * - title
     - common
     - The title of a audio file.
     - ``32 Variations for Piano in C minor on an Original Theme, WoO 80``
   * - track
     - common
     - The track number.
     - ``1``
   * - tracktotal
     - common
     - The total track number.
     - ``12``
   * - url
     - common
     - Uniform Resource Locator.
     - 
   * - work
     - common
     - The Musicbrainzs’ work entity.
     - ``32 Variations for Piano in C minor on an Original Theme, WoO 80``
   * - work_hierarchy
     - music_brainz
     - The hierarchy of works: The top level work appears first. As separator is this string used: -->.
     - ``Die Zauberflöte, K. 620 --> Die Zauberflöte, K. 620: Akt I --> Die Zauberflöte, K. 620: Act I, Scene II. No. 2 Aria "Was hör ...``
   * - year
     - date
     - The release year of the specific release.
     - ``2001``


Development
===========

Test
----

::

    pyenv local 3.6.13 3.7.10 3.9.2
    pip install tox tox-pyenv
    tox

Run a single test

::

    tox -e quick -- -s test test_job.TestJobWithConfigParser.test_source


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
