"""Test the code in the __init__ file."""

import audiorename


class TestInit:
    def test_version(self):
        assert audiorename.__version__
