# Copyright (C) 2014~2014 by Yichao Yu
# yyc1992@gmail.com

from cffi import FFI
from os import path as _path

_ffi = FFI()
_basedir = _path.dirname(__file__)


def _get_api_header():
    with open(_path.join(_basedir, 'readline_api.h')) as f:
        return f.read()

_ffi.cdef(_get_api_header())
_lib = _ffi.dlopen(_path.join(_basedir, '_pyreadline.so'))
