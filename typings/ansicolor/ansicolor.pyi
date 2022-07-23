"""
This type stub file was generated by pyright.
"""

__all__ = [
    "black",
    "blue",
    "cyan",
    "green",
    "magenta",
    "red",
    "white",
    "yellow",
    "colorize",
    "colorize_v2",
    "wrap_string",
    "get_code",
    "get_code_v2",
    "highlight_string",
    "get_highlighter",
    "strip_escapes",
    "justify_formatted",
    "colordiff",
    "set_term_title",
    "write_out",
    "write_err",
    "Colors",
]
_disabled = ...

class Colors:
    """Container class for colors"""

    @classmethod
    def new(cls, colorname): ...
    @classmethod
    def iter(cls): ...

def make_func(color): ...

highlights = ...
highlight_map = ...

def get_highlighter(colorid):
    """
    Map a color index to a highlighting color.

    :param int colorid: The index.
    :rtype: :class:`Colors`
    """
    ...

def get_code(color, bold=..., reverse=...):
    """
    Returns the escape code for styling with the given color,
    in bold and/or reverse.

    :param color: The color to use.
    :type color: :class:`Colors` class
    :param bool bold: Whether to mark up in bold.
    :param bool reverse: Whether to mark up in reverse video.
    :rtype: string
    """
    ...

def get_code_v2(color, bold=..., reverse=..., underline=..., blink=...):
    """
    Returns the escape code for styling with the given color,
    in bold and/or reverse.

    :param color: The color to use.
    :type color: :class:`Colors` class
    :param bool bold: Whether to mark up in bold.
    :param bool underline: Whether to mark up in underline.
    :param bool blink: Whether to mark up in blink.
    :param bool reverse: Whether to mark up in reverse video.
    :rtype: string
    """
    ...

def colorize(s, color, bold=..., reverse=..., start=..., end=...):  # -> str:
    """
    Colorize a string with the color given.

    :param string s: The string to colorize.
    :param color: The color to use.
    :type color: :class:`Colors` class
    :param bool bold: Whether to mark up in bold.
    :param bool reverse: Whether to mark up in reverse video.
    :param int start: Index at which to start coloring.
    :param int end: Index at which to end coloring.
    :rtype: string
    """
    ...

def colorize_v2(
    s, color, bold=..., reverse=..., underline=..., blink=..., start=..., end=...
):  # -> str:
    """
    Colorize a string with the color given.

    :param string s: The string to colorize.
    :param color: The color to use.
    :type color: :class:`Colors` class
    :param bool bold: Whether to mark up in bold.
    :param bool reverse: Whether to mark up in reverse video.
    :param bool blink: Whether to mark up in blink.
    :param bool reverse: Whether to mark up in reverse video.
    :param int start: Index at which to start coloring.
    :param int end: Index at which to end coloring.
    :rtype: string
    """
    ...

def wrap_string(s, pos, color, bold=..., reverse=...):  # -> str:
    """
    Colorize the string up to a position.

    :param string s: The string to colorize.
    :param int pos: The position at which to stop.
    :param color: The color to use.
    :type color: :class:`Colors` class
    :param bool bold: Whether to mark up in bold.
    :param bool reverse: Whether to mark up in reverse video.
    :rtype: string

    .. deprecated:: 0.2.2
       This function has been deprecated in favor of :func:`colorize`.
    """
    ...

def highlight_string(s, *spanlists, **kw):
    """
    Highlight spans in a string using a list of (begin, end) pairs. Each
    list is treated as a layer of highlighting. Up to four layers of
    highlighting are supported.

    :param string s: The string to highlight
    :param list spanlists: A list of tuples on the form ``[(begin, end)*]*``
    :param kw: May include: `bold`, `reverse`, `color`, `colors` and `nocolor`
    :rtype: string

    .. deprecated:: 0.2.3
       The `color` parameter has been deprecated in favor of `colors`.
    """
    ...

def colordiff(x, y, color_x=..., color_y=..., debug=...):
    """
    Formats a diff of two strings using the longest common subsequence by
    highlighting characters that differ between the strings.

    Returns the strings `x` and `y` with highlighting.

    :param string x: The first string.
    :param string y: The second string.
    :param color_x: The color to use for the first string.
    :type color_x: :class:`Colors` class
    :param color_y: The color to use for the second string.
    :type color_y: :class:`Colors` class
    :param bool debug: Whether to print debug output underway.
    :rtype: tuple
    """
    ...

def justify_formatted(s, justify_func, width):
    """
    Justify a formatted string to a width using a function
    (eg. ``string.ljust``).

    :param string s: The formatted string.
    :param justify_func: The justify function.
    :param int width: The width at which to justify.
    :rtype: string
    """
    ...

def strip_escapes(s):  # -> str:
    """
    Strips escapes from the string.

    :param string s: The string.
    :rtype: string
    """
    ...

def set_term_title(s):  # -> None:
    """
    Set the title of a terminal window.

    :param string s: The title.
    """
    ...

def write_to(target, s): ...
def write_out(s):  # -> None:
    """
    Write a string to ``sys.stdout``, strip escapes if output is a pipe.

    :param string s: The title.
    """
    ...

def write_err(s):  # -> None:
    """
    Write a string to ``sys.stderr``, strip escapes if output is a pipe.

    :param string s: The title.
    """
    ...
