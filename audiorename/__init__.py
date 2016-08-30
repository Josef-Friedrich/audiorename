# -*- coding: utf-8 -*-
import os

from rename import Rename
from args import parser

def do_rename(path, root_path='', args=None):
	if path.lower().endswith((".mp3", ".m4a", ".flac", ".wma")) == True:
		audio = Rename(path, root_path, args)
		audio.execute()

def execute():
	args = parser.parse_args()

	if os.path.isdir(args.folder):
		for root_path, subdirs, files in os.walk(args.folder):
			for file in files:
				do_rename(file, root_path, args=args)

	else:
		do_rename(args.folder, args=args)
