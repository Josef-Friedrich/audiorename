#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, argparse, textwrap, mutagen

from ansicolor import cyan
from ansicolor import green
from ansicolor import red
from ansicolor import yellow

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
	default='$artist_initial/$artistsafe_sort/%shorten{${album},32}%ifdef{year_safe,_${year_safe}}/${disctrack}_%shorten{$title,32}')

parser.add_argument('-c', '--compilation',
	help='Format string for compilations',
	default='_compilations/$album_initial/$album%ifdef{year_safe,_${year_safe}}/${disctrack}_%shorten{$title,32}')

parser.add_argument('-S', '--shell-friendly',
	help='Rename audio files “shell friendly”, this means without whitespaces, parentheses etc.',
	action='store_true')

parser.add_argument('-d', '--dry-run',
	help='A format string for singeltons',
	action='store_true')

parser.add_argument('-D', '--debug',
	help='Show special debug informations: meta, artist, track, year',
	default=False)

parser.add_argument('-e', '--extensions',
	help='Extensions to rename',
	default='mp3')

parser.add_argument('-b', '--base-dir',
	help='Base directory',
	default='')

parser.add_argument('-s', '--skip-if-empty',
	help='Skip renaming of field is empty.',
	default=False)

parser.add_argument('-a', '--folder-as-base-dir',
	help='Use specified folder as base directory',
	action='store_true')

parser.add_argument('-C', '--copy',
	help='Copy files instead of rename / move.',
	action='store_true')

args = parser.parse_args()

class Meta(object):

	def __init__(self, path):
		self.media_file = MediaFile(path)
		self.m = {}
		for key in MediaFile.readable_fields():
			value = getattr(self.media_file, key)
			if key != 'art':
				if not value:
					value = ''
				elif isinstance(value, str) or isinstance(value, unicode):
					value = Functions.tmpl_sanitize(value)
				self.m[key] = value
		self.discTrack()
		self.artistSafe()
		self.yearSafe()
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

		if self.m['disc'] and self.m['disctotal'] > 1:
			self.m['disctrack'] = disk + '-' + track
		else:
			self.m['disctrack'] = track

	def artistSafe(self):
		safe_sort = ''
		safe = ''
		if self.m['albumartist_sort']:
			safe_sort = self.m['albumartist_sort']
		elif self.m['artist_sort']:
			safe_sort = self.m['artist_sort']

		if self.m['albumartist']:
			safe = self.m['albumartist']
		elif self.m['artist']:
			safe = self.m['artist']
		elif self.m['albumartist_credit']:
			safe = self.m['albumartist_credit']
		elif self.m['artist_credit']:
			safe = self.m['artist_credit']

		if not safe_sort:
			if safe:
				safe_sort = safe
			else:
				safe_sort = 'Unknown'

		if args.shell_friendly:
			safe_sort = safe_sort.replace(', ', '_')

		self.m['artistsafe'] = safe
		self.m['artistsafe_sort'] = safe_sort


	def yearSafe(self):
		if self.m['original_year']:
			value = self.m['original_year']
		elif self.m['year']:
			value = self.m['year']
		else:
			value = ''
		self.m['year_safe'] = value

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

	def generateFilename(self):
		if self.meta['comp']:
			t = Template(as_string(args.compilation))
		else:
			t = Template(as_string(args.format))
		f = Functions(self.meta)
		new = t.substitute(self.meta, f.functions())
		new = self.postTemplate(new);
		new = f.tmpl_deldupchars(new + '.' + self.extension.lower())
		self.new_path = os.path.join(self.base_dir, new)
		self.message = red(self.old_path.decode('utf-8')) + '\n  -> ' + green(self.new_path) + '\n'

	def postTemplate(self, text):
		if isinstance(text, str) or isinstance(text, unicode):
			if args.shell_friendly:
				text = Functions.tmpl_asciify(text)
				text = Functions.tmpl_delchars(text, '[]().,!"\'’')
				text = Functions.tmpl_replchars(text, '-', ' ')
		return text

	def createDir(self, path):
		path = os.path.dirname(path)
		import errno
		try:
			os.makedirs(path)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

	def skipMessage(self):
		print(red('☠ no field ' + args.skip_if_empty + ' ☠', reverse=True) + ': ' + self.old_file)

	def dryRun(self):
		self.generateFilename()
		print('Dry run: ' + self.message)

	def debug(self, option):
		def p(tag):
			print(cyan(tag) + u': ' + as_string(self.meta[tag]))
		print('\n' + green('- Debug: ') + red(option, reverse=True) + green(' --------------------------------'))
		print(yellow(self.old_file))

		if option == 'artist':

			p('artist')
			p('albumartist')
			p('artistsafe')
			p('artist_sort')
			p('artist_credit')
			p('albumartist_credit')
			p('albumartist_sort')
			p('artistsafe_sort')

		elif option == 'meta':
			for key, value in self.meta.iteritems():
				if key != 'art' and value:
					print(cyan(as_string(key)) + ': ' + as_string(value))

		elif option == 'mediafile':
			m = MediaFile(self.old_file)
			for key in MediaFile.readable_fields():
				value = getattr(m, key)
				if key != 'art':
					print(cyan(key) + ': ' + as_string(value))

		elif option == 'mutagen':
			m = mutagen.File(self.old_file, easy=True)
			print(m)
			for key, value in m.iteritems():
				print(cyan(key) + ': ' + value[0])

		elif option == 'track':
			p('track')
			p('tracktotal')
			p('disc')
			p('disctotal')
			p('disctrack')

		elif option == 'year':
			p('original_year')
			p('year')
			p('date')

	def rename(self):
		self.generateFilename()
		print('Rename: ' + self.message)
		self.createDir(self.new_path)
		os.rename(self.old_path, self.new_path)

	def copy(self):
		self.generateFilename()
		print('Copy: ' + self.message)
		import shutil
		self.createDir(self.new_path)
		shutil.copy2(self.old_path, self.new_path)

	def execute(self):
		if args.skip_if_empty and not self.meta[args.skip_if_empty]:
			self.skipMessage()
		else:
			if args.dry_run:
				self.dryRun()
			elif args.debug:
				self.debug(args.debug)
			elif args.copy:
				self.copy()
			else:
				self.rename()

def execute(path, root_path = ''):
	if path.lower().endswith((".mp3", ".m4a", ".flac", ".wma")) == True:
		audio = Rename(path, root_path)
		audio.execute()

if __name__ == '__main__':

	if os.path.isdir(args.folder):
		for root_path, subdirs, files in os.walk(args.folder):
			for file in files:
				execute(file, root_path)

	else:
		execute(args.folder)

