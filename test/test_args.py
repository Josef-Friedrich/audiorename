# -*- coding: utf-8 -*-

import unittest
import re
import six
import audiorename
import helper as h


class TestCommandlineInterface(unittest.TestCase):

    def test_help_short(self):
        with self.assertRaises(SystemExit) as cm:
            with h.Capturing():
                audiorename.execute(['-h'])
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '0')

    def test_help_long(self):
        with self.assertRaises(SystemExit) as cm:
            with h.Capturing():
                audiorename.execute(['--help'])
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '0')

    def test_without_arguments(self):
        with self.assertRaises(SystemExit) as cm:
            with h.Capturing('err'):
                audiorename.execute()
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '2')


class TestVersion(unittest.TestCase):

    def test_version(self):
        with self.assertRaises(SystemExit):
            if six.PY2:
                with h.Capturing('err') as output:
                    audiorename.execute(['--version'])
            else:
                with h.Capturing() as output:
                    audiorename.execute(['--version'])

        result = re.search('[^ ]* [^ ]*', output[0])
        self.assertTrue(result)


class TestHelp(unittest.TestCase):

    def setUp(self):
        with self.assertRaises(SystemExit):
            with h.Capturing() as output:
                audiorename.execute(['--help'])
        self.output = '\n'.join(output)

    def test_tmep(self):
        self.assertTrue('%title{text}' in self.output)

    def test_phrydy(self):
        self.assertTrue('mb_releasegroupid' in self.output)

    # album
    def test_field_album_classical(self):
        self.assertTrue('album_classical' in self.output)

    def test_field_album_clean(self):
        self.assertTrue('album_clean' in self.output)
        self.assertTrue('“album” without' in self.output)

    def test_field_album_initial(self):
        self.assertTrue('album_initial' in self.output)
        self.assertTrue('First character' in self.output)

    # artist
    def test_field_artist_initial(self):
        self.assertTrue('artist_initial' in self.output)
        self.assertTrue('First character' in self.output)

    def test_field_artistsafe(self):
        self.assertTrue('artistsafe' in self.output)
        self.assertTrue('The first available' in self.output)

    def test_field_artistsafe_sort(self):
        self.assertTrue('artistsafe_sort' in self.output)
        self.assertTrue('The first available' in self.output)

    # composer
    def test_field_composer_initial(self):
        self.assertTrue('composer_initial' in self.output)

    def test_field_composer_safe(self):
        self.assertTrue('composer_safe' in self.output)

    def test_field_disctrack(self):
        self.assertTrue('disctrack' in self.output)
        self.assertTrue('Combination of' in self.output)

    def test_field_performer_classical(self):
        self.assertTrue('performer_classical' in self.output)

    def test_field_title_classical(self):
        self.assertTrue('title_classical' in self.output)

    def test_field_track_classical(self):
        self.assertTrue('track_classical' in self.output)

    def test_field_year_safe(self):
        self.assertTrue('year_safe' in self.output)
        self.assertTrue('First “original_year”' in self.output)
