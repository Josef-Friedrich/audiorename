#! /usr/bin/env python

import os, sys, argparse, textwrap

from beets import mediafile
from beets.util.functemplate import Template
from beets.library import DefaultTemplateFunctions as Functions

parser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=textwrap.dedent('''\
		Rename music files from metadata

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
parser.add_argument('folder', help='A folder containing music')

args = parser.parse_args()

def load(path):
	audio = mediafile.MediaFile(path)
	print(audio.title)

def shorten(text, max_size):
    if len(text) <= max_size:
        return text
    return textwrap.wrap(text, max_size)[0]

def format_tracknumber():
	pos = new['tracknumber'].find('/')
	if pos:
		track = new['tracknumber'][:pos]
	else:
		track = new['tracknumber']

	return track.zfill(2)

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


for path, subdirs, files in os.walk(args.folder):
	for audio_file in files:
		if audio_file.endswith((".mp3", ".m4a", ".flac", ".wma")) == True:
			load(os.path.join(path, audio_file))



