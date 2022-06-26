from typing import TypedDict


Version = TypedDict('Version', {
    'version': str,
    'full-revisionid': str,
    'dirty': bool,
    'error': str,
    'date': str
})


def get_versions() -> Version: ...
