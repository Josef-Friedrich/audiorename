"""Test the code in the __init__ file."""

from typing import Any

from audiorename import audiofile
from audiorename.message import Message
from tests import helper


class TestClassMessage:
    def setup_method(self) -> None:
        self.job = helper.get_job()
        self.prefix = helper.dir_cwd
        self.source = audiofile.AudioFile(
            helper.get_testfile("files", "album.mp3"), job=self.job, prefix=self.prefix
        )

    @staticmethod
    def get_message(**kwargs: Any) -> Message:
        return Message(helper.get_job(**kwargs))

    def test_attributes(self) -> None:
        msg = self.get_message()
        assert msg.color is True
        assert msg.verbose is False
        assert msg.one_line is False
        assert msg.max_field == 23

    def test_diff(self) -> None:
        msg = self.get_message()
        with helper.Capturing(clean_ansi=True) as output:
            msg.diff("title", "", "full")
        assert output[0] == "    title:                   “”"
        assert output[1] == "                             “full”"

    def test_output_one_line(self) -> None:
        msg = self.get_message(one_line=True)
        with helper.Capturing() as output:
            msg.output("   lol     ")
            msg.output("   lol     ")

        assert output[0] == "lol lol "

    def test_output_multilines(self) -> None:
        msg = self.get_message(one_line=False)
        with helper.Capturing() as output:
            msg.output("one")
            msg.output("two")
        assert output[0] == "one"
        assert output[1] == "two"
