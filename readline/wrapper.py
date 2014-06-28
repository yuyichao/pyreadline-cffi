# Copyright (C) 2014~2014 by Yichao Yu
# yyc1992@gmail.com

# Addapted from pyrepl.readline:
#   Copyright 2000-2010 Michael Hudson-Doyle <micahel@gmail.com>
#                       Alex Gaynor
#                       Antonio Cuni
#                       Armin Rigo
#                       Holger Krekel
#
#                        All Rights Reserved
#
#
# Permission to use, copy, modify, and distribute this software and
# its documentation for any purpose is hereby granted without fee,
# provided that the above copyright notice appear in all copies and
# that both that copyright notice and this permission notice appear in
# supporting documentation.
#
# THE AUTHOR MICHAEL HUDSON DISCLAIMS ALL WARRANTIES WITH REGARD TO
# THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
# INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
# RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF
# CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import sys
import os
from ._cffi import (_ffi, _lib, _to_cstr, _to_cstr_null, _ffi_pystr)


class _PyPyWrapper(object):
    __slots__ = ('f_in', 'f_out')

    def __init__(self):
        self.f_in = _ffi.cast("FILE*", sys.stdin)
        self.f_out = _ffi.cast("FILE*", sys.stdout)

    def raw_input(self, prompt=''):
        cstr = _lib.py_call_readline(self.f_in, self.f_out, _to_cstr(prompt))
        if cstr == _ffi.NULL:
            raise KeyboardInterrupt
        s = _ffi_pystr(cstr)
        _lib.free(_ffi.cast('void*', cstr))
        if len(s) == 0:
            raise EOFError
        return s

    def _hook(self):
        sys.__raw_input__ = self.raw_input


class _CPythonWrapper(object):
    def __init__(self):
        _ffi.cdef('char *(*PyOS_ReadlineFunctionPointer)'
                  '(FILE*, FILE*, char*);')
        self.__pylib = _ffi.dlopen(None)

    def _hook(self):
        self.__pylib.PyOS_ReadlineFunctionPointer = _lib.py_call_readline


def _create_wrapper():
    try:
        f_in = sys.stdin.fileno()
        f_out = sys.stdout.fileno()
        if not os.isatty(f_in) or not os.isatty(f_out):
            return
    except:
        return

    if '__pypy__' in sys.builtin_module_names:    # PyPy
        wrapper = _PyPyWrapper()
    else:
        wrapper = _CPythonWrapper()

    wrapper._hook()
    return wrapper
