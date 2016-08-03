#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, argparse, textwrap

#from beets.mediafile import MediaFile
from mediafile import MediaFile
#from beets.util.functemplate import Template
from functemplate import Template
#from beets.library import DefaultTemplateFunctions as Functions
from functions import Functions

parser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=textwrap.dedent('''\
Rename audio files from metadata

Metadata fields:

	Ordinary metadata:

		- title
		- artist
		- artist_sort:         The “sort name” of the track artist
		                       (e.g., “Beatles, The” or “White, Jack”).
		- artist_credit:       The track-specific artist credit name,
		                       which may be a variation of the artist’s
		                       “canonical” name.
		- album
		- albumartist:         The artist for the entire album, which
		                       may be different from the artists for the
		                       individual tracks.
		- albumartist_sort
		- albumartist_credit
		- genre
		- composer
		- grouping
		- year, month, day:    The release date of the specific release.
		- original_year, original_month, original_day:
		                       The release date of the original version
		                       of the album.
		- track
		- tracktotal
		- disc
		- disctotal
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

		- %lower{text}:         Convert text to lowercase.
		- %upper{text}:         Convert text to UPPERCASE.
		- %title{text}:         Convert text to Title Case.
		- %left{text,n}:        Return the first n characters of text.
		- %right{text,n}:       Return the last n characters of text.
		- %if{condition,text} or %if{condition,truetext,falsetext}:
		                        If condition is nonempty (or nonzero,
		                        if it’s a number), then returns the
		                        second argument. Otherwise, returns the
		                        third argument if specified (or nothing
		                        if falsetext is left off).
		- %asciify{text}:       Convert non-ASCII characters to their
		                        ASCII equivalents. For example, “café”
		                        becomes “cafe”. Uses the mapping
		                        provided by the unidecode module.
		- %aunique{identifiers,disambiguators}:
		                        Provides a unique string to disambiguate.
		- %time{date_time,format}:
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
		- %ifdef{field}, %ifdef{field,truetext} or %ifdef{field,truetext,falsetext}:
		                        If field exists, then return truetext or
		                        field (default). Otherwise, returns
		                        falsetext. The field should be entered
		                        without $.

	'''
	)
)
parser.add_argument('folder', help='A folder containing audio files or a audio file')
parser.add_argument('-f', '--format', help='A format string', default='$artist/$album/$track $title')
parser.add_argument('-c', '--compilation', help='Format string for compilations', default='$artist/$album/$track $title')
parser.add_argument('-s', '--singelton', help='A format string for singletons', default='$artist $track')
parser.add_argument('-d', '--dryrun', help='A format string for singeltons')
parser.add_argument('-e', '--extensions', help='Extensions to rename', default='mp3')

args = parser.parse_args()

def shorten(text, max_size):
    if len(text) <= max_size:
        return text
    return textwrap.wrap(text, max_size)[0]

def pick_artist():
	values = [
		new['albumartistsort'],
		new['albumartist'],
		new['artistsort'],
		new['artist'],
	]

	for value in values:
		if value:
			break

	return value

class Rename(object):

	def __init__(self, path):
		self.media_file = MediaFile(path)
		self.meta = {}
		for key in MediaFile.readable_fields():
			value = getattr(self.media_file, key)
			if value:
				self.meta[key] = value

		t = Template(args.format)
		f = Functions()
		self.new_filename = t.substitute(self.meta, f.functions())

	def debug(self):
		print(self.new_filename)

def execute(path):
	if path.endswith((".mp3", ".m4a", ".flac", ".wma")) == True:
		audio = Rename(path)
		audio.debug()

if __name__ == '__main__':

	if os.path.isdir(args.folder):
		for path, subdirs, files in os.walk(args.folder):
			for file in files:
				execute(os.path.join(path, file))

	else:
		execute(args.folder)

