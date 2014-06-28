# Copyright (C) 2014~2014 by Yichao Yu
# yyc1992@gmail.com

"""
Importing this module enables command line editing using GNU readline.
"""

from ._cffi import _ffi, _lib, _to_cstr, _to_cstr_null, _handle_ioerr
from .state import state as _state


# Exported function to send one line to readline's init file parser
def parse_and_bind(s):
    """parse_and_bind(string) -> None
    Parse and execute single line of a readline init file."""
    _lib.parse_and_bind(_to_cstr(s))


# Exported function to parse a readline init file
def read_init_file(filename=None):
    """read_init_file([filename]) -> None
    Parse a readline initialization file.
    The default filename is the last filename used."""
    err = _lib.read_init_file(_to_cstr_null(filename))
    _handle_ioerr(err)


# Exported function to load a readline history file
def read_history_file(filename=None):
    """read_history_file([filename]) -> None
    Load a readline history file.
    The default filename is ~/.history."""
    err = _lib.read_history_file(_to_cstr_null(filename))
    _handle_ioerr(err)


# Exported function to save a readline history file
def write_history_file(filename=None):
    """write_history_file([filename]) -> None
    Save a readline history file.
    The default filename is ~/.history."""
    err = _lib.write_history_file(_to_cstr_null(filename))
    _handle_ioerr(err)


# Set history length
def set_history_length(length):
    """set_history_length(length) -> None
    set the maximal number of items which will be written to
    the history file. A negative length is used to inhibit
    history truncation."""
    _lib.history_length = length


# Get history length
def get_history_length():
    """get_history_length() -> int
    return the maximum number of items that will be written to
    the history file."""
    return _lib.history_length

# Exported functions to specify hook functions in Python
set_completion_display_matches_hook = \
    _state.set_completion_display_matches_hook
set_startup_hook = _state.set_startup_hook
set_pre_input_hook = _state.set_pre_input_hook


# Get the completion type for the scope of the tab-completion
def get_completion_type():
    """get_completion_type() -> int
    Get the type of completion being attempted."""
    return _lib.rl_completion_type


# Get the beginning index for the scope of the tab-completion
def get_begidx():
    """get_begidx() -> int
    get the beginning index of the readline tab-completion scope"""
    return _state.begidx


# Get the ending index for the scope of the tab-completion
def get_endidx():
    """get_endidx() -> int
    get the ending index of the readline tab-completion scope"""
    return _state.endidx


# Set the tab-completion word-delimiters that readline uses
def set_completer_delims(string):
    """set_completer_delims(string) -> None
    set the readline word delimiters for tab-completion"""
    _lib.set_completer_delims(_to_cstr(string))


def remove_history_item(pos):
    """remove_history_item(pos) -> None
    remove history item given by its position"""
    pos = int(pos)
    if pos < 0:
        raise ValueError("History index cannot be negative")
    if not _lib.remove_history_item(pos):
        raise ValueError("No history item at position %d" % pos)


def replace_history_item(pos, line):
    """replace_history_item(pos, line) -> None
    replaces history item given by its position with contents of line"""
    pos = int(pos)
    if pos < 0:
        raise ValueError("History index cannot be negative")
    if not _lib.replace_history_item(pos, _to_cstr(line)):
        raise ValueError("No history item at position %d" % pos)


# Add a line to the history buffer
def add_history(string):
    """add_history(string) -> None
    add a line to the history buffer"""
    _lib.add_history(_to_cstr(string))


# Get the tab-completion word-delimiters that readline uses
def get_completer_delims():
    """get_completer_delims() -> string
    get the readline word delimiters for tab-completion"""
    return _ffi_pystr(_lib.rl_completer_word_break_characters)


# Exported function to specify a word completer in Python

# Set the completer function
set_completer = _state.set_completer


# Get the completer function
def get_completer():
    """get_completer() -> function\n
    Returns current completer function."""
    return _state.completer
