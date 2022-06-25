"""Envoke the exectutable from the command line."""
from __future__ import annotations  # For ar: Popen
import unittest
import subprocess
from subprocess import Popen


class TestExectutable(unittest.TestCase):

    @staticmethod
    def call(shell_string: str):
        ar = Popen(shell_string, shell=True, stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT)
        ar.wait()
        return ar

    @staticmethod
    def first_line(ar: Popen[bytes]) -> str:
        if ar.stdout:
            return ar.stdout.readlines()[0].decode('utf-8')
        else:
            raise Exception('Could not find first line')

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
