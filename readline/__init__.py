# Copyright (C) 2014~2014 by Yichao Yu
# yyc1992@gmail.com

from ._cffi import _ffi, _lib, _to_cstr, _to_cstr_null, _handle_ioerr


class _ReadlineState(object):
    __slots__ = ('completion_display_matches_hook', 'startup_hook',
                 'pre_input_hook', 'completer', 'begidx', 'endidx')
    def _clear(self):
        self.completion_display_matches_hook = None
        self.startup_hook = None
        self.pre_input_hook = None
        self.completer = None
        self.begidx = None
        self.endidx = None

_readline_state = _ReadlineState()


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
