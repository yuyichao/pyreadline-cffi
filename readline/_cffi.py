# Copyright (C) 2014~2014 by Yichao Yu
# yyc1992@gmail.com

from cffi import FFI

import os
from os import path as _path

_ffi = FFI()

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

_ffi.cdef("""
/* Bindable functions */
typedef int rl_command_func_t(int, int);

/* Typedefs for the completion system */
typedef char *rl_compentry_func_t(const char*, int);
typedef char **rl_completion_func_t(const char*, int, int);

typedef char *rl_quote_func_t(char*, int, char*);
typedef char *rl_dequote_func_t(char*, int);

typedef int rl_compignore_func_t(char**);

typedef void rl_compdisp_func_t(char**, int, int);

/* Type for input and pre-read hook functions like rl_event_hook */
typedef int rl_hook_func_t(void);

/* Input function type */
typedef int rl_getc_func_t(FILE*);

/* Generic function that takes a character buffer (which could be the readline
   line buffer) and an index into it (which could be rl_point) and returns
   an int. */
typedef int rl_linebuf_func_t(char*, int);

/* `Generic' function pointer typedefs */
typedef int rl_intfunc_t(int);
typedef int rl_icpfunc_t(char*);
typedef int rl_icppfunc_t(char**);

typedef void rl_voidfunc_t(void);
typedef void rl_vintfunc_t(int);
typedef void rl_vcpfunc_t(char*);
typedef void rl_vcppfunc_t(char**);

typedef char *rl_cpvfunc_t(void);
typedef char *rl_cpifunc_t(int);
typedef char *rl_cpcpfunc_t(char*);
typedef char *rl_cpcppfunc_t(char**);
""")
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


# Remove?
@_ffi.callback('void(void*)')
def _py_call(handle):
    try:
        _ffi.from_handle(handle)()
    except:
        pass

_lib.set_py_funcs(_py_call)
