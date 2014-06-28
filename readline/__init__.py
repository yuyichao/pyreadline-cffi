# Copyright (C) 2014~2014 by Yichao Yu
# yyc1992@gmail.com

from ._cffi import _ffi, _lib

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
