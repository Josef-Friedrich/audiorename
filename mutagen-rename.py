#! /usr/bin/env python3

import mutagen, os, sys, argparse, textwrap

old = {}
new = {}

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

def map(new_field, old_field=False):
	if not old_field:
		old_field = new_field
	if old_field in old:
		new[new_field] = str(old[old_field][0])
	else:
		new[new_field] = ''

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

def re_map(audio_file):
	global new
	new = {}
	new['extension'] = extension = audio_file.split('.')[-1]
	new['filename'] = os.path.basename(audio_file)

	global old
	old = mutagen.File(audio_file, easy=True)

	if extension == 'wma':
		#print(old)
		map('album', 'WM/AlbumTitle')
		map('albumartist', 'WM/AlbumArtist')
		map('albumartistsort', 'WM/AlbumArtistSortOrder')
		map('artist', 'Author')
		map('artist', 'WM/ARTISTS')
		map('artistsort', 'WM/ArtistSortOrder')
		map('title', 'Title')
		map('track', 'WM/TrackNumber')
	elif extension == 'mp3' or extension == 'm4a' or extension == 'flac':
		#print(old)
		map('album')
		map('albumartist')
		map('albumartistsort')
		map('artist')
		map('artistsort')
		map('title')
		map('tracknumber')
		map('discnumber')

def enrich():
	new['_artist'] = pick_artist()
	new['_artistfirstcharacter'] = new['_artist'][0:1].lower()
	new['_tracknumber'] = format_tracknumber()


for path, subdirs, files in os.walk(args.folder):
	for audio_file in files:
		if audio_file.endswith((".mp3", ".m4a", ".flac", ".wma")) == True:
			re_map(os.path.join(path, audio_file))
			enrich()
			#print(new['extension'] + ': ' + new['artistsort'])
			format_string = new['_artistfirstcharacter'] + \
				'/' + \
				new['_artist'] + \
				'/' + \
				new['album'] + \
				'/' + \
				new['_tracknumber'] + \
				'_' + \
				new['title']

			print(format_string)


