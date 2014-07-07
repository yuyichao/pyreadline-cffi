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

"""Replace builtin readline functions
"""

import sys
import os
from ._cffi import _ffi, _lib, _to_cstr, _ffi_pystr


class _ReadlineWrapper(object):
    __slots__ = ('f_in', 'f_out')

    def __init__(self):
        self.f_in = _ffi.cast("FILE*", sys.stdin)
        self.f_out = _ffi.cast("FILE*", sys.stdout)

    def _cffi_input(self, prompt):
        cstr = _lib.py_call_readline(self.f_in, self.f_out, _to_cstr(prompt))
        if cstr == _ffi.NULL:
            raise KeyboardInterrupt
        return _ffi.gc(cstr, _lib.free)

    def raw_input(self, prompt=''):
        cstr = self._cffi_input(prompt)
        s = _ffi_pystr(cstr)
        if len(s) == 0:
            raise EOFError
        return s

    def multiline_input(self, more_lines, ps1, ps2, returns_unicode=False):
        """Read an input on possibly multiple lines, asking for more
        lines as long as 'more_lines(unicodetext)' returns an object whose
        boolean value is true.
        """
        # TODO? steal some code from IPython?
        prompt = ps1
        if returns_unicode:
            res = u''
            convert = lambda cstr: _ffi.string(cstr).decode()
        else:
            res = b''
            convert = _ffi.string
        while True:
            line = convert(self._cffi_input(prompt))
            if len(line) == 0:
                if len(res) == 0:
                    raise EOFError
                return res
            res += line[:-1]
            try:
                if not more_lines(res):
                    return res
            except:
                return res
            res += '\n'
            prompt = ps2


class _PyPyWrapper(_ReadlineWrapper):
    def _hook(self):
        sys.__raw_input__ = self.raw_input


class _CPythonWrapper(_ReadlineWrapper):
    def __init__(self):
        _ReadlineWrapper.__init__(self)
        _ffi.cdef('char *(*PyOS_ReadlineFunctionPointer)'
                  '(FILE*, FILE*, char*);')
        self.__pylib = _ffi.dlopen(None)

    def _hook(self):
        self.__pylib.PyOS_ReadlineFunctionPointer = _lib.py_call_readline


def _create_wrapper():
    if '__pypy__' in sys.builtin_module_names:    # PyPy
        wrapper = _PyPyWrapper()
    else:
        wrapper = _CPythonWrapper()

    try:
        f_in = sys.stdin.fileno()
        f_out = sys.stdout.fileno()
        if os.isatty(f_in) and os.isatty(f_out):
            wrapper._hook()
    except:
        pass

    return wrapper
