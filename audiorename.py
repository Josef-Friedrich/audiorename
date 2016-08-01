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
parser.add_argument('folder', help='A folder containing music')
parser.add_argument('-f', '--format', help='A format string', default='$artist $track $title')

args = parser.parse_args()

def convert_object_to_dict(obj):
	values = {}
	for key in MediaFile.readable_fields():
		value = getattr(obj, key)
		if value:
			values[key] = value
	return values

def load(path):
	audio = MediaFile(path)
	values = convert_object_to_dict(audio)
	return values

def rename(values):
	t = Template(args.format)
	f = Functions()
	print(t.substitute(values, f.functions()))


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
			values = load(os.path.join(path, audio_file))
			rename(values)







