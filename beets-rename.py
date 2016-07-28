#! /usr/bin/env python

from beets import mediafile
from beets.util.functemplate import Template

lol = mediafile.MediaFile('/home/jf/ownCloud/mutagen/mp3.mp3')

print(lol.title)


t = Template('iii ${lol}l iii')


values = {
	'lol': 'troll'
}
print(t.substitute(values))