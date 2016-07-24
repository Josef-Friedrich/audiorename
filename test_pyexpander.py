#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import pyexpander

external_def = {
	'artist': 'August Högn',
	'title': 'Gloria'
}

string = '$(artist) -  $(title) $lol()'

extend = """$py(
def lol():
	return lol
)
$extend(lol)
"""

string = extend + string

parsed, obj = pyexpander.expand(string,external_definitions=external_def)

print(parsed)

