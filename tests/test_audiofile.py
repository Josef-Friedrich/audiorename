"""Test the submodule “rename.py”."""

import os
import shutil
import tempfile

import pytest

import audiorename
from audiorename import audiofile
from audiorename.meta import Meta
from tests import helper


class TestClassAction:
    def setup_method(self) -> None:
        self.action = audiofile.Action(helper.get_job())

    def test_method_delete(self) -> None:
        tmp = helper.get_tmp_file_object("files", "album.mp3")
        assert os.path.exists(tmp.abspath)
        with helper.Capturing() as output:
            self.action.delete(tmp)
        assert not os.path.exists(tmp.abspath)
        assert "Delete" in helper.join(output)

    @pytest.mark.skipif(
        helper.SKIP_QUICK, reason="Ignored, as it has to be done quickly."
    )
    @pytest.mark.skipif(
        helper.skip_api_calls, reason="Ignored if the API is not available."
    )
    def test_method_metadata_enrich(self) -> None:
        tmp = helper.get_tmp_file_object("classical", "without_work.mp3")
        if not tmp.meta:
            pytest.fail("The audio file needs a meta property.")
        assert tmp.meta.mb_workid is None
        with helper.Capturing():
            self.action.metadata(tmp, enrich=True)

        meta = Meta(tmp.abspath)
        assert meta.mb_workid == "6b198406-4fbf-3d61-82db-0b7ef195a7fe"

    def test_method_metadata_remap_classical(self) -> None:
        tmp = helper.get_tmp_file_object("classical", "Schubert_Winterreise", "01.mp3")

        assert tmp.meta.album == "Winterreise"
        with helper.Capturing():
            self.action.metadata(tmp, remap=True)

        meta = Meta(tmp.abspath)
        assert meta.album == "Die Winterreise, op. 89, D. 911 (Fischer-Dieskau, Moore)"


class TestClassAudioFile:
    def test_existing(self) -> None:
        abspath = helper.get_testfile("files", "album.mp3")
        prefix = helper.dir_cwd
        result = audiofile.AudioFile(abspath, job=helper.get_job(), prefix=prefix)
        assert result.abspath == abspath
        assert result.type == "source"
        assert result.exists is True
        assert result.extension == "mp3"
        assert result.meta.path == abspath
        assert result.short == "[…]tests/files/files/album.mp3"
        assert result.prefix == prefix + os.path.sep


class TestClassMbTrackListing:
    def setup_method(self) -> None:
        self.mb = audiofile.MBTrackListing()

    def listing(self, album: str, title: str, length: int = 123) -> str:
        return self.mb.format_audiofile(album, title, length)

    def test_one_call(self) -> None:
        result = self.listing("album", "title")
        assert result == "1. album: title (2:03)"

    def test_two_calls(self) -> None:
        self.listing("album", "title")
        result = self.listing("album", "title")
        assert result == "2. album: title (2:03)"

    def test_opus(self) -> None:
        result = self.listing("album Op.", "title")
        assert result == "1. album op.: title (2:03)"

    def test_dash(self) -> None:
        result = self.listing("album - act", "title")
        assert result == "1. album act: title (2:03)"


class TestFunctionGetTarget:
    def setup_method(self) -> None:
        self.extensions = ["flac", "mp3", "m4a"]
        self.target = helper.get_testfile("quality", "flac.flac")

    def test_same(self) -> None:
        result = audiofile.find_target_path(self.target, self.extensions)
        assert self.target == result

    def test_different(self) -> None:
        target = self.target.replace(".flac", ".mp3")
        result = audiofile.find_target_path(target, self.extensions)
        assert self.target == result


class TestFunctionBestFormat:
    """
    Bitrates

    * flac.flac 301213
    * m4a_100.m4a 198551
    * m4a_250.m4a 235243
    * mp3_128.mp3 191995
    * mp3_144.mp3 86884
    * mp3_320.mp3 319999
    """

    @staticmethod
    def source_target(source: str, target: str):
        return audiofile.detect_best_format(
            helper.get_meta("quality", source),
            helper.get_meta("quality", target),
            helper.get_job(),
        )

    def test_same_quality(self) -> None:
        with helper.Capturing() as output:
            result = self.source_target("flac.flac", "flac.flac")
        assert result == "target"
        assert (
            output[0] == "Best format: Source and target have the same "
            "formats, use target."
        )

    def test_type_target_better(self) -> None:
        with helper.Capturing() as output:
            result = self.source_target("mp3_128.mp3", "flac.flac")
        assert result == "target"
        assert (
            output[0] == "Best format is “target” because of “type”: "
            "(source: mp3, target: flac)"
        )

    def test_type_source_better(self) -> None:
        with helper.Capturing() as output:
            result = self.source_target("flac.flac", "mp3_128.mp3")
        assert result == "source"
        assert (
            output[0] == "Best format is “source” because of “type”: "
            "(source: flac, target: mp3)"
        )

    def test_bitrate_mp3_source_better(self) -> None:
        with helper.Capturing() as output:
            result = self.source_target("mp3_320.mp3", "mp3_128.mp3")
        assert result == "source"
        assert (
            output[0] == "Best format is “source” because of “bitrate”: "
            "(source: 319999, target: 191995)"
        )

    def test_bitrate_mp3_target_better_2(self) -> None:
        with helper.Capturing() as output:
            result = self.source_target("mp3_144.mp3", "mp3_320.mp3")
        assert result == "target"
        assert (
            output[0] == "Best format is “target” because of “bitrate”: "
            "(source: 86884, target: 319999)"
        )

    def test_bitrate_mp3_source_better_2(self) -> None:
        with helper.Capturing() as output:
            result = self.source_target("mp3_320.mp3", "mp3_144.mp3")
        assert result == "source"
        assert (
            output[0] == "Best format is “source” because of “bitrate”: "
            "(source: 319999, target: 86884)"
        )

    def test_bitrate_m4a_target_better(self) -> None:
        with helper.Capturing() as output:
            result = self.source_target("m4a_100.m4a", "m4a_250.m4a")
        assert result == "target"
        assert (
            output[0] == "Best format is “target” because of “bitrate”: "
            "(source: 198551, target: 235243)"
        )

    def test_bitrate_m4a_source_better(self) -> None:
        with helper.Capturing() as output:
            result = self.source_target("m4a_250.m4a", "m4a_100.m4a")
        assert result == "source"
        assert (
            output[0] == "Best format is “source” because of “bitrate”: "
            "(source: 235243, target: 198551)"
        )


class TestBasicRename:
    def setup_method(self) -> None:
        self.tmp_album = helper.copy_to_tmp("files", "album.mp3")
        with helper.Capturing():
            audiorename.execute(self.tmp_album)
        self.tmp_compilation = helper.copy_to_tmp("files", "compilation.mp3")
        with helper.Capturing():
            audiorename.execute(self.tmp_compilation)

    def test_album(self) -> None:
        assert not os.path.isfile(self.tmp_album)
        assert helper.is_file(helper.dir_cwd + helper.path_album)

    def test_compilation(self) -> None:
        assert not os.path.isfile(self.tmp_compilation)
        assert helper.is_file(helper.dir_cwd + helper.path_compilation)

    def teardown_method(self) -> None:
        shutil.rmtree(helper.dir_cwd + "/_compilations/")
        shutil.rmtree(helper.dir_cwd + "/t/")


class TestOverwriteProtection:
    def setup_method(self) -> None:
        self.tmp_album = helper.copy_to_tmp("files", "album.mp3")
        with helper.Capturing():
            audiorename.execute("--copy", self.tmp_album)
        self.tmp_compilation = helper.copy_to_tmp("files", "compilation.mp3")
        with helper.Capturing():
            audiorename.execute("--copy", self.tmp_compilation)

    def test_album(self) -> None:
        with helper.Capturing() as output:
            audiorename.execute(self.tmp_album)
        assert "Exists" in helper.join(output)

    def test_compilation(self) -> None:
        with helper.Capturing() as output:
            audiorename.execute(self.tmp_compilation)
        assert "Exists" in helper.join(output)

    def test_album_already_renamed(self) -> None:
        with helper.Capturing():
            audiorename.execute(self.tmp_album)
        with helper.Capturing() as output:
            audiorename.execute(helper.dir_cwd + helper.path_album)

        assert "Renamed" in helper.join(output)

    def test_compilation_already_renamed(self) -> None:
        with helper.Capturing():
            audiorename.execute(self.tmp_compilation)
        with helper.Capturing() as output:
            audiorename.execute(helper.dir_cwd + helper.path_compilation)

        assert "Renamed" in helper.join(output)

    def teardown_method(self) -> None:
        shutil.rmtree(helper.dir_cwd + "/_compilations/")
        shutil.rmtree(helper.dir_cwd + "/t/")


class TestUnicodeUnittest:
    def setup_method(self) -> None:
        self.uni = helper.get_testfile("äöü", "ÅåÆæØø.mp3")
        self.renamed = os.path.join(
            "/_",
            "►",
            "$ar_combined_album",
            "$ar_combined_disctrack_ÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž.mp3",
        )

    def test_dry_run(self) -> None:
        with helper.Capturing() as output:
            audiorename.execute("--one-line", "--dry-run", "--verbose", self.uni)
        assert self.renamed in " ".join(output)

    def test_rename(self) -> None:
        tmp_dir = tempfile.mkdtemp()
        tmp = os.path.join(tmp_dir, "äöü.mp3")
        shutil.copyfile(self.uni, tmp)
        with helper.Capturing() as output:
            audiorename.execute("--one-line", "--verbose", "--target", tmp_dir, tmp)
        assert self.renamed in " ".join(output)

    def test_copy(self) -> None:
        with helper.Capturing() as output:
            audiorename.execute("--one-line", "--verbose", "--copy", self.uni)
        assert self.renamed in " ".join(output)

    def teardown_method(self) -> None:
        try:
            shutil.rmtree(helper.dir_cwd + "/_/")
        except OSError:
            pass


class TestProcessTargetPath:
    def setup_method(self) -> None:
        meta = helper.get_meta("files", "album.mp3")
        self.meta = meta.export_dict()

    @staticmethod
    def get_meta(**args):
        meta = helper.get_meta("files", "album.mp3")
        for key in args:
            setattr(meta, key, args[key])
        return meta.export_dict()

    @staticmethod
    def process(meta: str, format_string: str, shell_friendly: bool = True) -> str:
        return audiofile.process_target_path(meta, format_string, shell_friendly)

    def assert_target_path(
        self, expected: str, format_string: str = "$title", **fields
    ):
        if fields:
            meta = self.get_meta(**fields)
        else:
            meta = self.meta
        assert self.process(meta, format_string) == expected

    def test_simple(self) -> None:
        result = self.process(self.meta, "$title")
        assert result == "full"

    def test_unicode(self) -> None:
        self.assert_target_path("aeoeue", title="äöü")

    def test_enddot(self) -> None:
        self.assert_target_path("a", title="a.")

    def test_turned_quotation(self) -> None:
        self.assert_target_path("aa", title="a¿a")
