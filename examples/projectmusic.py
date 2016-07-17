#! /usr/bin/env python
#
# Desmond Cox
# April 10, 2008

"""Project Music

Renames audio files based on metadata

Usage: projectmusic.py [options]

Options:
  -d ...,   --directory=...             Specify which directory to work in
                                        (default is the current directory)
  -f ...,   --format=...                Specify the naming format
  -l,       --flatten                   Move all files into the same root
                                        directory
  -r,       --recursive                 Work recursively on the specified
                                        directory
  -t,       --test                      Only display the new file names; nothing
                                        will be renamed
  -h,       --help                      Display this help

Formatting:
  The following information is available to be used in the file name:
  album    artist    title    track

  To specify a file name format, enter the desired format enclosed in quotation
  marks. The words album, artist, title, and track will be replaced by values
  retrieved from the audio file's metadata.

  For example, --format="artist - album [track] title" will rename music files
  with the name format:
  Sample Artist - Sample Album [1] Sample Title

  The following characters are of special importance to the operating system
  and cannot be used in the file name:
  \    /    :    *    ?    "    <    >    |

  (=) is replaced by the directory path separator, so to move files into
  artist and album subdirectories, the following format can be used:
  "artist(=)album(=)track - title"

  If no format is provided, the default format is the same as used in the above
  example.

Examples:
  projectmusic.py                       Renames music files in the current
                                        directory
  projectmusic.py -d /music/path/       Renames music files in /music/path/
  projectmusic.py -f "title -- artist"  Renames music files in the current
                                        directory with the name format:
                                        Sample Title -- Sample Artist.mp3"""

### Imports ###

import time
import re
import os
import sys
import getopt

import mutagen.easyid3
import mutagen.oggvorbis

### Exceptions ###

class FormatError(Exception):
    """
    Exception raised due to improper formatting
    """
    pass

class DirectoryError(Exception):
    """
    Exception raised due to a non-existent directory
    """
    pass

### Definitions ###

def scanDirectory(directory, fileExtList, recursive=False):
    """
    Generate a list of files with the specified extension(s) in the specified
    directory (and its subdirectories, if the recursive option is enabled)
    """
    fileList = []

    for dirPath, dirNames, fileNames in os.walk(directory):
        for name in fileNames:
            if os.path.splitext(name)[1].lower() in fileExtList:
                # lower() is necessary here; otherwise ".MP3" is not considered
                # a valid extension and files will be skipped. The extension's
                # case is preserved when renaming the file, however
                fileList.append(os.path.normcase(os.path.join(dirPath, name)))

        if not recursive:
            break # do not continue to the next "dirPath"

    return fileList

class AudioFile:
    """
    A generic audio file
    """
    def __init__(self, fileName):
        self.fileName = fileName
        self.fileExt = os.path.splitext(fileName)[1].lower()
        self.filePath = os.path.split(fileName)[0] + os.path.sep

        self.data = getattr(self, "parse_%s" % self.fileExt[1:])()
        # call the appropriate method based on the file type

        self.generate()

    def generate(self):
        def lookup(key, default):
            return self.data[key][0] if ( self.data.has_key(key) and
                                          self.data[key][0] ) else default

        self.artist = lookup("artist", "No Artist")
        self.album = lookup("album", "No Album")
        self.title = lookup("title", "No Title")
        self.track = lookup("tracknumber", "0")

        if self.track != "0":
            self.track = self.track.split("/")[0].lstrip("0")

        # In regards to track numbers, self.data["tracknumber"] returns numbers
        # in several different formats: 1, 1/10, 01, or 01/10. Wanting a
        # consistent format, the returned string is split at the "/" and leading
        # zeros are stripped.

    def parse_mp3(self):
        return mutagen.easyid3.EasyID3(self.fileName)

    def parse_ogg(self):
        return mutagen.oggvorbis.Open(self.fileName)

    def rename(self, newFileName, flatten=False):
        def uniqueName(newFileName, count=0):
            """
            Returns a unique name if a file already exists with the supplied
            name
            """
            c = "_(%s)" % str(count) if count else ""
            prefix = directory + os.path.sep if flatten else self.filePath
            testFileName = prefix + newFileName + c + self.fileExt

            if os.path.isfile(testFileName):
                count += 1
                return uniqueName(newFileName, count)

            else:
                return testFileName

        os.renames(self.fileName, uniqueName(newFileName))

        # Note: this function is quite simple at the moment; it does not support
        # multiple file extensions, such as "sample.txt.backup", which would
        # only retain the ".backup" file extension.

    def cleanFileName(self, format):
        """
        Generate a clean file name based on metadata
        """
        rawFileName = format % {"artist": self.artist,
                                "album": self.album,
                                "title": self.title,
                                "track": self.track}

        rawFileName.encode("ascii", "replace")
        # encode is used to override the default encode error-handing mode;
        # which is to raise a UnicodeDecodeError

        cleanFileName = re.sub(restrictedCharPattern, "+", rawFileName)
        # remove restricted filename characters (\, /, :, *, ?, ", <, >, |) from
        # the supplied string

        return cleanFileName.replace("(=)", os.path.sep)

### Main ###

def main(argv):
    global directory
    directory = os.getcwd()
    format = "%(artist)s - %(album)s [%(track)s] %(title)s"
    flatten = False
    recursive = False
    test = False

    def verifyFormat(format):
        """
        Verify the supplied filename format
        """
        if re.search(restrictedCharPattern, format):
            raise FormatError, "supplied format contains restricted characters"

        if not re.search(formatPattern, format):
            raise FormatError, "supplied format does not contain any metadata keys"
            # the supplied format must contain at least one of "artist",
            # "album", "title", or "track", or all files will be named
            # identically

        format = format.replace("artist", "%(artist)s")
        format = format.replace("album", "%(album)s")
        format = format.replace("title", "%(title)s")
        format = format.replace("track", "%(track)s")
        return format

    def verifyDirectory(directory):
        """
        Verify the supplied directory path
        """
        if os.path.isdir(directory):
            return os.path.abspath(directory)

        else:
            raise DirectoryError, "supplied directory cannot be found"

    def usage():
        print __doc__

    try:
        opts, args = getopt.getopt(argv, "d:f:hlrt", ["directory=",
                                                      "format=",
                                                      "help",
                                                      "flatten",
                                                      "recursive",
                                                      "test"])

    except getopt.error, error:
        usage()
        print "\n***Error: %s***" % error
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()

        elif opt in ("-f", "--format"):
            try:
                format = verifyFormat(arg)

            except FormatError, error:
                print "\n***Error: %s***" % error
                sys.exit(2)

        elif opt in ("-d", "--directory"):
            try:
                directory = verifyDirectory(arg)

            except DirectoryError, error:
                print "\n***Error: %s***" % error
                sys.exit(3)

        elif opt in ("-l", "--flatten"):
            flatten = True

        elif opt in ("-r", "--recursive"):
            recursive = True

        elif opt in ("-t", "--test"):
            test = True

    work(directory, format, flatten, recursive, test)

def safety(message):
    print "\n***Attention: %s***" % message
    safety = raw_input("Enter 'ok' to continue (any other response will abort): ")

    if safety.lower().strip() != "ok":
        print "\n***Attention: aborting***"
        sys.exit()

def work(directory, format, flatten, recursive, test):
    fileList = scanDirectory(directory, [".mp3", ".ogg"], recursive)

    try:
        if test:
            safety("testing mode; nothing will be renamed")

            print "\n***Attention: starting***"

            for f in fileList:
                current = AudioFile(f)
                print current.cleanFileName(format)

        else:
            count = 0
            total = len(fileList)
            safety("all audio files in %s will be renamed" % directory)

            print "\n***Attention: starting***"
            start = time.time()

            for f in fileList:
                count += 1
                current = AudioFile(f)
                current.rename(current.cleanFileName(format), flatten)
                message = "Renamed %d of %d" % (count, total)
                sys.stdout.write("\r" + message)

            print "\n%d files renamed in %f seconds" % (len(fileList),
                                                        time.time() - start)

    except StandardError:
        print "\n***Error: %s***" % f
        raise

if __name__ == "__main__":
    restrictedCharPattern = re.compile('[\\\\/:\*\?"<>\|]')
    formatPattern = re.compile('artist|album|title|track')

    main(sys.argv[1:])