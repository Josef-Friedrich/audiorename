#! /usr/bin/env python

from beets import mediafile
from beets.util.functemplate import Template
from beets.library import DefaultTemplateFunctions as Functions

lol = mediafile.MediaFile('/home/jf/ownCloud/mutagen/mp3.mp3')

print(lol.title)

t = Template('iii ${lol}l %upper{iii}')

f = Functions()

values = {
	'lol': 'troll'
}
print(t.substitute(values, f.functions()))