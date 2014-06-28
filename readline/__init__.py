# Copyright (C) 2014~2014 by Yichao Yu
# yyc1992@gmail.com

from ._cffi import _ffi, _lib
import os

try:
    # 2to3 friendly
    _unicode = eval('unicode')
    _ffi_pystr = _ffi.string
except:
    _unicode = str
    _bytes = bytes
    def _ffi_pystr(s):
        return _ffi.string(s).decode()
else:
    try:
        _bytes = bytes
    except:
        _bytes = str


def _to_cstr(s):
    if isinstance(s, _unicode):
        return s.encode()
    return s


def _handle_ioerr(err):
    if err != 0:
        raise IOError(err, os.strerror(err))


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
    err = _lib.read_init_file(_ffi.NULL if filename is None
                              else _to_cstr(filename))
    _handle_ioerr(err)
