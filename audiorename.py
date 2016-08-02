#! /usr/bin/env python

import os, sys, argparse, textwrap

from beets.mediafile import MediaFile
from beets.util.functemplate import Template
from beets.library import DefaultTemplateFunctions as Functions

parser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=textwrap.dedent('''\
		Rename audio files from metadata

		Metadata fields:
			- album
			- albumartist
			- artist
			- extension
			- filename
			- title
			- track
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

def rename(values):
	t = Template(args.format)
	f = Functions()
	print(t.substitute(values, f.functions()))

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

def enrich():
	new['_artist'] = pick_artist()
	new['_artistfirstcharacter'] = new['_artist'][0:1].lower()
	new['_tracknumber'] = format_tracknumber()

class Rename(object):

	def __init__(self, path):
		self.media_file = MediaFile(path)
		self.meta = {}
		for key in MediaFile.readable_fields():
			value = getattr(self.media_file, key)
			if value:
				self.meta[key] = value

	def debug(self):
		print(self.meta)

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

