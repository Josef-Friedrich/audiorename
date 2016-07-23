#! /usr/bin/env python3

import mutagen, os, sys, argparse, textwrap

old = {}
new = {}

parser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=textwrap.dedent('''\
		Rename music files from metadata

		Metadata fields:
			- artist
			- title
			- extension
			- filename
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

def normalize(audio_file):
	global new
	new = {}
	new['extension'] = extension = audio_file.split('.')[-1]
	new['filename'] = os.path.basename(audio_file)

	global old
	old = mutagen.File(audio_file, easy=True)

	if extension == 'wma':
		print(old)
		# Author
		map('artist', 'WM/ARTISTS')
		map('artist', 'Author')
		map('album', 'WM/AlbumTitle')
		map('track', 'WM/TrackNumber')
		#WM/Year
		#WM/Composer
		#WM/ArtistSortOrder
		map('title', 'Title')
	elif extension == 'mp3' or extension == 'm4a' or extension == 'flac':
		#print(old)
		map('artist')
		map('albumartist')
		map('title')
		map('album')
		map('track', 'tracknumber')

for path, subdirs, files in os.walk(args.folder):
	for audio_file in files:
		if audio_file.endswith((".mp3", ".m4a", ".flac", ".wma")) == True:
			normalize(os.path.join(path, audio_file))
			print(new)
			print(new['artist'] + ' ' + new['title'])


