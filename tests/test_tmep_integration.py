"""Test the integration of the python package “tmep”."""

from tests import helper


class TestFunctions:
    def test_ifdefempty_empty_existent_field(self) -> None:
        out = helper.call_bin(
            "--dry-run",
            "--format",
            "%ifdefempty{mb_workid,_empty_,_notempty_}",
            helper.get_testfile("files", "album.mp3"),
        )
        assert "_empty_" in str(out)

    def test_ifdefempty_empty_nonexistent_field(self) -> None:
        out = helper.call_bin(
            "--dry-run",
            "--format",
            "%ifdefempty{xxx,_empty_,_notempty_}",
            helper.get_testfile("files", "album.mp3"),
        )
        assert "_empty_" in str(out)

    def test_ifdefempty_notempty(self) -> None:
        out = helper.call_bin(
            "--dry-run",
            "--format",
            "%ifdefempty{title,_empty_,_notempty_}",
            helper.get_testfile("files", "album.mp3"),
        )
        assert "_notempty_" in str(out)
