"""Test the submodule “args.py”."""

import re

import pytest

import audiorename
from tests import helper

with pytest.raises(ValueError) as exc_info:
    raise ValueError("value must be 42")

assert exc_info.type is ValueError

assert exc_info.value.args[0] == "value must be 42"


class TestCommandlineInterface:
    def test_help_short(self) -> None:
        with pytest.raises(SystemExit) as exc_info:
            with helper.Capturing():
                audiorename.execute("-h")
        assert exc_info.value.code == 0

    def test_help_long(self) -> None:
        with pytest.raises(SystemExit) as exc_info:
            with helper.Capturing():
                audiorename.execute("--help")
        assert exc_info.value.code == 0

    def test_without_arguments(self) -> None:
        with pytest.raises(SystemExit) as exc_info:
            with helper.Capturing("stderr"):
                audiorename.execute()
        assert exc_info.value.code == 2

    def test_without_mutually_exclusive(self) -> None:
        with pytest.raises(SystemExit) as exc_info:
            with helper.Capturing("stderr") as output:
                audiorename.execute("--copy", "--move", ".")
        assert exc_info.value.code == 2
        assert "not allowed with argument" in " ".join(output)


class TestVersion:
    def test_version(self) -> None:
        with pytest.raises(SystemExit):
            with helper.Capturing() as output:
                audiorename.execute("--version")

        result = re.search("[^ ]* [^ ]*", output[0])
        assert result


class TestHelp:
    def setup_method(self) -> None:
        with pytest.raises(SystemExit):
            with helper.Capturing() as output:
                audiorename.execute("--help")
        self.output = "\n".join(output)

    def test_tmep(self) -> None:
        assert "%title{text}" in self.output

    def test_phrydy(self) -> None:
        assert "mb_releasegroupid" in self.output

    # album
    def test_field_ar_classical_album(self) -> None:
        assert "ar_classical_album" in self.output

    def test_field_ar_combined_album(self) -> None:
        assert "ar_combined_album" in self.output
        assert "“album” without" in self.output

    def test_field_ar_initial_album(self) -> None:
        assert "ar_initial_album" in self.output
        assert "First character" in self.output

    # artist
    def test_field_ar_initial_artist(self) -> None:
        assert "ar_initial_artist" in self.output
        assert "First character" in self.output

    def test_field_ar_combined_artist(self) -> None:
        assert "ar_combined_artist" in self.output
        assert "The first non-empty value" in self.output

    def test_field_ar_combined_artist_sort(self) -> None:
        assert "ar_combined_artist_sort" in self.output
        assert "The first non-empty value" in self.output

    # composer
    def test_field_ar_initial_composer(self) -> None:
        assert "ar_initial_composer" in self.output

    def test_field_ar_combined_composer(self) -> None:
        assert "ar_combined_composer" in self.output

    def test_field_ar_combined_disctrack(self) -> None:
        assert "ar_combined_disctrack" in self.output
        assert "Combination of" in self.output

    def test_field_ar_classical_performer(self) -> None:
        assert "ar_classical_performer" in self.output

    def test_field_ar_classical_title(self) -> None:
        assert "ar_classical_title" in self.output

    def test_field_ar_classical_track(self) -> None:
        assert "ar_classical_track" in self.output

    def test_field_ar_combined_year(self) -> None:
        assert "ar_combined_year" in self.output
        assert "First “original_year”" in self.output


class TestArgsDefault:
    def setup_method(self):
        from audiorename.args import ArgsDefault, parse_args

        self.default = ArgsDefault()
        self.default.source = "lol"
        self.args = parse_args(["lol"])

    # positional arguments
    def test_source(self):
        assert self.args.source == "lol"
        assert self.args.source == self.default.source

    # optional arguments
    def test_album_complete(self):
        assert self.args.album_complete is None
        assert self.args.album_complete == self.default.album_complete

    def test_album_min(self):
        assert self.args.album_min is None
        assert self.args.album_min == self.default.album_min

    def test_cleaning_action(self):
        assert self.args.cleaning_action is None
        assert self.args.cleaning_action == self.default.cleaning_action

    def test_backup_folder(self):
        assert self.args.backup_folder is None
        assert self.args.backup_folder == self.default.backup_folder

    def test_best_format(self):
        assert self.args.best_format is None
        assert self.args.best_format == self.default.best_format

    def test_classical(self):
        assert self.args.classical is None
        assert self.args.classical == self.default.classical

    def test_color(self):
        assert self.args.color is None
        assert self.args.color == self.default.color

    def test_compilation(self):
        assert self.args.compilation_template is None
        assert self.args.compilation_template == self.default.compilation_template

    def test_debug(self):
        assert self.args.debug is None
        assert self.args.debug == self.default.debug

    def test_dry_run(self):
        assert self.args.dry_run is None
        assert self.args.dry_run == self.default.dry_run

    def test_enrich_metadata(self):
        assert self.args.enrich_metadata is None
        assert self.args.enrich_metadata == self.default.enrich_metadata

    def test_extension(self):
        assert self.args.extension is None
        assert self.args.extension == self.default.extension

    def test_field_skip(self):
        assert self.args.field_skip is None
        assert self.args.field_skip == self.default.field_skip

    def test_format(self):
        assert self.args.default_template is None
        assert self.args.default_template == self.default.default_template

    def test_format_classical(self):
        assert self.args.classical_template is None
        assert self.args.classical_template == self.default.classical_template

    def test_job_info(self):
        assert self.args.job_info is None
        assert self.args.job_info == self.default.job_info

    def test_mb_track_listing(self):
        assert self.args.mb_track_listing is None
        assert self.args.mb_track_listing == self.default.mb_track_listing

    def test_move_action(self):
        assert self.args.move_action is None
        assert self.args.move_action == self.default.move_action

    def test_one_line(self):
        assert self.args.one_line is None
        assert self.args.one_line == self.default.one_line

    def test_remap_classical(self):
        assert self.args.remap_classical is None
        assert self.args.remap_classical == self.default.remap_classical

    def test_shell_friendly(self):
        assert self.args.shell_friendly is None
        assert self.args.shell_friendly == self.default.shell_friendly

    def test_soundtrack(self):
        assert self.args.soundtrack_template is None
        assert self.args.soundtrack_template == self.default.soundtrack_template

    def test_source_as_target(self):
        assert self.args.source_as_target is None
        assert self.args.source_as_target == self.default.source_as_target

    def test_target(self):
        assert self.args.target is None
        assert self.args.target == self.default.target

    def test_stats(self):
        assert self.args.stats is None
        assert self.args.stats == self.default.stats

    def test_verbose(self):
        assert self.args.verbose is None
        assert self.args.verbose == self.default.verbose
