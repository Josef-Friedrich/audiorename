"""Test the code in the __init__ file."""

import unittest
import helper
from audiorename import audiofile
from audiorename.message import Message
from typing import Any


class TestClassMessage(unittest.TestCase):

    def setUp(self):
        self.job = helper.get_job()
        self.prefix = helper.dir_cwd
        self.source = audiofile.AudioFile(
            helper.get_testfile('files', 'album.mp3'),
            job=self.job,
            prefix=self.prefix
        )

    @staticmethod
    def get_message(**kwargs: Any) -> Message:
        return Message(helper.get_job(**kwargs))

    def test_attributes(self):
        msg = self.get_message()
        self.assertEqual(msg.color, True)
        self.assertEqual(msg.verbose, False)
        self.assertEqual(msg.one_line, False)
        self.assertEqual(msg.max_field, 23)

    def test_diff(self):
        msg = self.get_message()
        with helper.Capturing() as output:
            msg.diff('title', '', 'full')
        self.assertEqual(output[0], '    title:                   “”')
        self.assertEqual(output[1], '                             “full”')

    def test_output_one_line(self):
        msg = self.get_message(one_line=True)
        with helper.Capturing() as output:
            msg.output('   lol     ')
            msg.output('   lol     ')

        self.assertEqual(output[0], 'lol lol ')

    def test_output_multilines(self):
        msg = self.get_message(one_line=False)
        with helper.Capturing() as output:
            msg.output('one')
            msg.output('two')
        self.assertEqual(output[0], 'one')
        self.assertEqual(output[1], 'two')


if __name__ == '__main__':
    unittest.main()
