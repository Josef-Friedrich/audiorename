"""Test the code in the __init__ file."""

import unittest

import audiorename


class TestInit(unittest.TestCase):
    def test_version(self):
        self.assertTrue(audiorename.__version__)


if __name__ == "__main__":
    unittest.main()
