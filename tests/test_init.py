"""Test the code in the __init__ file."""

import audiorename


class TestInit:
    def test_version(self) -> None:
        assert audiorename.__version__
