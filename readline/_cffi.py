# Copyright (C) 2014~2014 by Yichao Yu
# yyc1992@gmail.com

from cffi import FFI

import os
from os import path as _path

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

_ffi = FFI()
_basedir = _path.dirname(__file__)

with open(_path.join(_basedir, 'readline_api.h')) as f:
    _ffi.cdef(f.read())
_lib = _ffi.dlopen(_path.join(_basedir, '_pyreadline.so'))


def _to_cstr(s):
    if isinstance(s, _unicode):
        return s.encode()
    return s


def _to_cstr_null(s):
    return _ffi.NULL if s is None else _to_cstr(s)


def _handle_ioerr(err):
    if err != 0:
        raise IOError(err, os.strerror(err))
