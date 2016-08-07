#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, argparse, textwrap

#from beets.mediafile import MediaFile
from mediafile import MediaFile
from mediafile import as_string
#from beets.util.functemplate import Template
from functemplate import Template
#from beets.library import DefaultTemplateFunctions as Functions
from functions import Functions

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
		- %ifdef{field}, %ifdef{field,truetext} or %ifdef{field,truetext,falsetext}:
		                        If field exists, then return truetext or
		                        field (default). Otherwise, returns
		                        falsetext. The field should be entered
		                        without $.

	'''
	)
)

parser.add_argument('folder',
	help='A folder containing audio files or a audio file')

parser.add_argument('-f', '--format',
	help='A format string',
	default='$artist_initial/$artistsafe_sort/$album/${disctrack}_%shorten{$title,32}')

parser.add_argument('-c', '--compilation',
	help='Format string for compilations',
	default='_compilations/$album_initial/$album/${disctrack}_%shorten{$title,32}')

parser.add_argument('-s', '--singelton',
	help='A format string for singletons',
	default='$artist $track')

parser.add_argument('-S', '--shell-friendly',
	help='Rename audio files “shell friendly”, this means without whitespaces, parentheses etc.',
	action='store_true')

parser.add_argument('-d', '--dry-run',
	help='A format string for singeltons',
	action='store_true')

parser.add_argument('-e', '--extensions',
	help='Extensions to rename',
	default='mp3')

parser.add_argument('-b', '--base-dir',
	help='Base directory',
	default='')

parser.add_argument('-a', '--folder-as-base-dir',
	help='Use specified folder as base directory',
	action='store_true')

parser.add_argument('-C', '--copy',
	help='Copy files instead of rename / move.',
	action='store_true')

parser.add_argument('-m', '--meta',
	help='Show meta tags for debugging purposes.',
	action='store_true')

args = parser.parse_args()

class Meta(object):

	def __init__(self, path):
		self.media_file = MediaFile(path)
		self.m = {}
		for key in MediaFile.readable_fields():
			value = getattr(self.media_file, key)
			if key != 'art':
				if value:
					if isinstance(value, str) or isinstance(value, unicode):
						if args.shell_friendly:
							value = Functions.tmpl_asciify(value)
							value = Functions.tmpl_delchars(value, '().,')
							value = Functions.tmpl_replchars(value, '-', ' ')
							value = Functions.tmpl_sanitize(value)
						else:
							self.m[key] = Functions.tmpl_sanitize(value)
				else:
					value = ''
				self.m[key] = value
		self.discTrack()
		self.artistSafe()
		self.initials()

	def discTrack(self):
		if self.m['disctotal'] > 9:
			disk = str(self.m['disc']).zfill(2)
		else:
			disk = str(self.m['disc'])

		if self.m['tracktotal'] > 99:
			track = str(self.m['track']).zfill(3)
		else:
			track = str(self.m['track']).zfill(2)

		if self.m['disc']:
			self.m['disctrack'] = disk + '-' + track
		else:
			self.m['disctrack'] = track

	def artistSafe(self):
		if self.m['albumartist_sort']:
			self.m['artistsafe_sort'] = self.m['albumartist_sort']
		elif self.m['artist_sort']:
			self.m['artistsafe_sort'] = self.m['artist_sort']

		if self.m['albumartist']:
			self.m['artistsafe'] = self.m['albumartist']
		elif self.m['artist']:
			self.m['artistsafe'] = self.m['artist']
		elif self.m['albumartist_credit']:
			self.m['artistsafe'] = self.m['albumartist_credit']
		elif self.m['artist_credit']:
			self.m['artistsafe'] = self.m['artist_credit']

		if not 'artistsafe_sort' in self.m and 'artistsafe' in self.m:
			self.m['artistsafe_sort'] = self.m['artistsafe']
		else:
			self.m['artistsafe_sort'] = 'Unknown'

	def initials(self):
		self.m['artist_initial'] = self.m['artistsafe_sort'][0:1].lower()
		self.m['album_initial'] = self.m['album'][0:1].lower()

	def getMeta(self):
		return self.m

class Rename(object):

	def __init__(self, file, root_path = ''):
		if root_path:
			self.old_file = os.path.join(root_path, file)
		else:
			self.old_file = file

		if args.base_dir:
			self.base_dir = args.base_dir
		else:
			self.base_dir = os.getcwd()

		if args.folder_as_base_dir:
			self.base_dir = os.path.realpath(root_path)

		self.old_path = os.path.realpath(self.old_file)
		self.extension = self.old_file.split('.')[-1]

		meta = Meta(self.old_path)
		self.meta = meta.getMeta()
		if self.meta['comp']:
			t = Template(as_string(args.compilation))
		else:
			t = Template(as_string(args.format))
		f = Functions()
		self.new_filename = t.substitute(self.meta, f.functions())

		self.new_path = os.path.join(self.base_dir, self.new_filename + '.' + self.extension)
		self.message = self.old_path.decode('utf-8') + '\n  -> ' + self.new_path + '\n'

	def createDir(self, path):
		path = os.path.dirname(path)
		import errno
		try:
			os.makedirs(path)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

	def debug(self):
		print('Dry run: ' + self.message)

	def debugMeta(self):
		for key, value in self.meta.iteritems():
			if key != 'art' and value:
				print(as_string(key) + ': ' + as_string(value))

	def rename(self):
		print('Rename: ' + self.message)
		self.createDir(self.new_path)
		os.rename(self.old_path, self.new_path)

	def copy(self):
		print('Copy: ' + self.message)
		import shutil
		self.createDir(self.new_path)
		shutil.copy2(self.old_path, self.new_path)

def execute(path, root_path = ''):
	if path.endswith((".mp3", ".m4a", ".flac", ".wma")) == True:
		audio = Rename(path, root_path)
		if args.dry_run:
			audio.debug()
		elif args.meta:
			audio.debugMeta()
		elif args.copy:
			audio.copy()
		else:
			audio.rename()

if __name__ == '__main__':

	if os.path.isdir(args.folder):
		for root_path, subdirs, files in os.walk(args.folder):
			for file in files:
				execute(file, root_path)

	else:
		execute(args.folder)

