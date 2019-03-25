"""Envoke the exectutable from the command line."""

import unittest
import subprocess


class TestExectutable(unittest.TestCase):

    @staticmethod
    def call(shell_string):
        ar = subprocess.Popen(shell_string, shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        ar.wait()
        return ar

    @staticmethod
    def first_line(ar):
        return ar.stdout.readlines()[0].decode('utf-8')

    def test_without_arguments(self):
        ar = self.call('audiorenamer')
        self.assertTrue('usage: audiorenamer' in self.first_line(ar))
        self.assertEqual(ar.returncode, 2)

    def test_version(self):
        ar = self.call('audiorenamer --version')
        self.assertTrue('audiorenamer' in self.first_line(ar))
        self.assertEqual(ar.returncode, 0)

    def test_help(self):
        ar = self.call('audiorenamer --help')
        self.assertTrue('usage: audiorenamer' in self.first_line(ar))
        self.assertEqual(ar.returncode, 0)

    def test_unkown(self):
        ar = self.call('audioreamer --help')
        self.assertFalse('usage: audiorenamer' in self.first_line(ar))
        self.assertEqual(ar.returncode, 127)


if __name__ == '__main__':
    unittest.main()
