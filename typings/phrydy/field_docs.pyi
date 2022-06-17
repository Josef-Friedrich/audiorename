"""
This type stub file was generated by pyright.
"""

import typing
from typing import Any, List, Literal
from typing_extensions import NotRequired

categories = ...
class FieldDoc(typing.TypedDict):
    description: str
    category: Literal['common', 'date', 'audio', 'music_brainz', 'rg', 'r128']
    data_type: NotRequired[Literal['int', 'str', 'float', 'list', 'bool', 'bytes']]
    examples: NotRequired[List[Any]]
    ...


FieldDocCollection = typing.Dict[str, FieldDoc]
fields: FieldDocCollection = ...