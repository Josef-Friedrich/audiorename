#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import pyexpander

external_definitions = {
	'artist': 'August Högn',
	'title': 'Gloria'
}

string = '$artist -  $title'

parsed = pyexpander.expand(string,
	external_definitions=external_definitions,
	allow_nobracket_vars= True)

print(str(parsed))

