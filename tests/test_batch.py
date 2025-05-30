"""Test the submodule “batchelper.py”."""

import audiorename
from tests import helper


class TestBatch:
    def setup_method(self) -> None:
        self.singles = helper.gen_file_list(
            ["album", "compilation"],
            helper.get_testfile("files"),
        )

        self.album_broken = helper.gen_file_list(
            ["01", "03", "05", "07", "09", "11"],
            helper.get_testfile("files", "album_broken"),
        )

        self.album_broken_all = helper.gen_file_list(
            ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"],
            helper.get_testfile("files", "album_broken"),
        )

        self.album_complete = helper.gen_file_list(
            ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"],
            helper.get_testfile("files", "album_complete"),
        )

        self.album_incomplete = helper.gen_file_list(
            ["01", "02", "04", "05", "06", "07", "09", "10", "11"],
            helper.get_testfile("files", "album_incomplete"),
        )

        self.album_small = helper.gen_file_list(
            ["01", "02", "03", "04", "05"],
            helper.get_testfile("files", "album_small"),
        )

        self.all = (
            self.singles
            + self.album_broken_all
            + self.album_complete
            + self.album_incomplete
            + self.album_small
        )

    def test_single(self) -> None:
        single = helper.get_testfile("files", "album.mp3")
        with helper.Capturing(clean_ansi=True) as output:
            audiorename.execute("--dry-run", "--verbose", single)

        assert [single] == helper.filter_source(output)

    def test_folder_complete(self) -> None:
        with helper.Capturing(clean_ansi=True) as output:
            audiorename.execute("--dry-run", "--verbose", helper.get_testfile("files"))
        assert self.all == helper.filter_source(output)

    def test_folder_sub(self) -> None:
        with helper.Capturing(clean_ansi=True) as output:
            audiorename.execute(
                "--dry-run", "--verbose", helper.get_testfile("files", "album_complete")
            )
        assert self.album_complete == helper.filter_source(output)

    def test_album_min(self) -> None:
        with helper.Capturing(clean_ansi=True) as output:
            audiorename.execute(
                "--dry-run",
                "--verbose",
                "--album-min",
                "7",
                helper.get_testfile("files"),
            )
        assert self.album_complete + self.album_incomplete == helper.filter_source(
            output
        )

    def test_album_min_no_match(self) -> None:
        with helper.Capturing(clean_ansi=True) as output:
            audiorename.execute(
                "--dry-run",
                "--verbose",
                "--album-min",
                "23",
                helper.get_testfile("files"),
            )
        assert [] == helper.filter_source(output)

    def test_album_complete(self) -> None:
        with helper.Capturing(clean_ansi=True) as output:
            audiorename.execute(
                "--dry-run",
                "--verbose",
                "--album-complete",
                helper.get_testfile("files"),
            )
        assert (
            self.singles + self.album_complete + self.album_small
            == helper.filter_source(output)
        )

    def test_filter_all(self) -> None:
        with helper.Capturing(clean_ansi=True) as output:
            audiorename.execute(
                "--dry-run",
                "--verbose",
                "--album-min",
                "7",
                "--album-complete",
                helper.get_testfile("files"),
            )
        assert self.album_complete == helper.filter_source(output)


class TestExtension:
    def setup_method(self) -> None:
        self.test_files = helper.get_testfile("mixed_formats")

    def test_default(self) -> None:
        with helper.Capturing(clean_ansi=True) as output:
            audiorename.execute(
                "--dry-run",
                "--verbose",
                self.test_files,
            )
        assert helper.filter_source(output) == helper.gen_file_list(
            ["01.flac", "02.m4a", "03.mp3"], self.test_files, extension=None
        )

    def test_one(self) -> None:
        with helper.Capturing(clean_ansi=True) as output:
            audiorename.execute(
                "--dry-run", "--verbose", "--extension", "mp3,flac", self.test_files
            )
        assert helper.filter_source(output) == helper.gen_file_list(
            ["01.flac", "03.mp3"], self.test_files, extension=None
        )

    def test_two(self) -> None:
        with helper.Capturing(clean_ansi=True) as output:
            audiorename.execute(
                "--dry-run", "--verbose", "--extension", "mp3", self.test_files
            )
        assert helper.filter_source(output) == helper.gen_file_list(
            ["03.mp3"], self.test_files, extension=None
        )


class TestSkip:
    def setup_method(self) -> None:
        self.file = helper.get_testfile("broken", "binary.mp3")
        with helper.Capturing() as output:
            audiorename.execute("-d", "--verbose", self.file)
        self.output = helper.join(output)

    def test_message(self) -> None:
        assert "Broken file" in self.output

    def test_file_in_message(self) -> None:
        assert "Broken file" in self.output
        assert self.file in self.output

    def test_continuation(self) -> None:
        path = helper.get_testfile("broken")
        with helper.Capturing(clean_ansi=True) as output:
            audiorename.execute("--dry-run", "--verbose", path)
        output = helper.filter_source(output)
        assert output[1]
