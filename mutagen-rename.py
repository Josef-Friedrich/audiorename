#! /usr/bin/env python3

import mutagen, os, sys, argparse

from mutagen.asf import ASFUnicodeAttribute

parser = argparse.ArgumentParser(description='Rename music files.')
parser.add_argument('folder', help='A folder containing music')

args = parser.parse_args()

def normalize(audio_file):
	metadata = {}
	metadata['extension'] = extension = audio_file.split('.')[-1]
	metadata['filename'] = os.path.basename(audio_file)

	m = mutagen.File(audio_file, easy=True)

	if extension == 'wma':
		metadata['artist'] = str(m['WM/ARTISTS'][0])
	elif extension == 'mp3' or extension == 'm4a':
	if 'title' in m:
		metadata['title'] = m['title']
	if 'artist' in m:
		metadata['artist'] = m['artist']
	return metadata

for path, subdirs, files in os.walk(args.folder):
	for audio_file in files:
		if audio_file.endswith((".mp3", ".m4a", ".flac", ".wma")) == True:
			metadata = normalize(os.path.join(path, audio_file))
			print(metadata)


