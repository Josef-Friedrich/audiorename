# -*- coding: utf-8 -*-
# This file is part of beets.
# Copyright 2016, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""The core data store and collection logic for beets.
"""
from __future__ import division, absolute_import, print_function

import os
import sys
import time
import textwrap
from unidecode import unidecode

def _int_arg(s):
    """Convert a string argument to an integer for use in a template
    function.  May raise a ValueError.
    """
    return int(s.strip())

class Functions(object):
    """A container class for the default functions provided to path
    templates. These functions are contained in an object to provide
    additional context to the functions -- specifically, the Item being
    evaluated.
    """
    _prefix = 'tmpl_'

    def __init__(self, values=None):
        """Parametrize the functions.
        """
        self.values = values

    def functions(self):
        """Returns a dictionary containing the functions defined in this
        object. The keys are function names (as exposed in templates)
        and the values are Python functions.
        """
        out = {}
        for key in self._func_names:
            out[key[len(self._prefix):]] = getattr(self, key)
        return out

    @staticmethod
    def tmpl_lower(s):
        """Convert a string to lower case."""
        return s.lower()

    @staticmethod
    def tmpl_upper(s):
        """Covert a string to upper case."""
        return s.upper()

    @staticmethod
    def tmpl_title(s):
        """Convert a string to title case."""
        return s.title()

    @staticmethod
    def tmpl_left(s, chars):
        """Get the leftmost characters of a string."""
        return s[0:_int_arg(chars)]

    @staticmethod
    def tmpl_right(s, chars):
        """Get the rightmost characters of a string."""
        return s[-_int_arg(chars):]

    @staticmethod
    def tmpl_shorten(text, max_size):
        max_size = int(max_size)
        if len(text) <= max_size:
            return text
        text = textwrap.wrap(text, max_size)[0]
        import re
        text = re.sub(r'\W+$', '', text)
        return text.strip()

    @staticmethod
    def tmpl_if(condition, trueval, falseval=u''):
        """If ``condition`` is nonempty and nonzero, emit ``trueval``;
        otherwise, emit ``falseval`` (if provided).
        """
        try:
            int_condition = _int_arg(condition)
        except ValueError:
            if condition.lower() == "false":
                return falseval
        else:
            condition = int_condition

        if condition:
            return trueval
        else:
            return falseval

    @staticmethod
    def tmpl_delchars(s, chars):
        for char in chars:
            s = s.replace(char, '')
        return s

    @staticmethod
    def tmpl_deldupchars(s, chars = r'-_\.'):
        import re
        return re.sub(r'([' + chars + r'])\1*', r'\1', s)

    @staticmethod
    def tmpl_replchars(s, replace, chars):
        for char in chars:
            s = s.replace(char, replace)
        return s

    @staticmethod
    def tmpl_sanitize(s):
        for char in ':*?"<>|\/~&{}':
            s = s.replace(char, '')
        return s

    @staticmethod
    def tmpl_asciify(s):
        """Translate non-ASCII characters to their ASCII equivalents.
        """
        ger_umlaute = {'ae': u'ä', 'oe': u'ö', 'ue': u'ü', 'Ae': u'Ä', 'Oe': u'Ö', 'Ue': u'Ü'}
        for replace, search in ger_umlaute.iteritems():
            s = s.replace(search, replace)
        return unidecode(s)

    @staticmethod
    def tmpl_time(s, fmt, cur_fmt):
        """Format a time value using `strftime`.
        """
        return time.strftime(fmt, time.strptime(s, cur_fmt))

    @staticmethod
    def tmpl_first(s, count=1, skip=0, sep=u'; ', join_str=u'; '):
        """ Gets the item(s) from x to y in a string separated by something
        and join then with something

        :param s: the string
        :param count: The number of items included
        :param skip: The number of items skipped
        :param sep: the separator. Usually is '; ' (default) or '/ '
        :param join_str: the string which will join the items, default '; '.
        """
        skip = int(skip)
        count = skip + int(count)
        return join_str.join(s.split(sep)[skip:count])

    def tmpl_ifdef(self, field, trueval=u'', falseval=u''):
        """ If field exists return trueval or the field (default)
        otherwise, emit return falseval (if provided).

        :param field: The name of the field
        :param trueval: The string if the condition is true
        :param falseval: The string if the condition is false
        :return: The string, based on condition
        """
        if field in self.values:
            return trueval
        else:
            return falseval


# Get the name of tmpl_* functions in the above class.
Functions._func_names = \
    [s for s in dir(Functions)
     if s.startswith(Functions._prefix)]
