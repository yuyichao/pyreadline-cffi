# Copyright (C) 2014~2014 by Yichao Yu
# yyc1992@gmail.com

from ._cffi import _ffi, _lib


class _ReadlineState(object):
    __slots__ = ('completion_display_matches_hook', 'startup_hook',
                 'pre_input_hook', 'completer', 'begidx', 'endidx')
    def __init__(self):
        self._clear()

    def _clear(self):
        self.completion_display_matches_hook = None
        self.startup_hook = None
        self.pre_input_hook = None
        self.completer = None
        self.begidx = None
        self.endidx = None

    # Exported functions to specify hook functions in Python
    def set_completion_display_matches_hook(self, function):
        """set_completion_display_matches_hook([function]) -> None
        Set or remove the completion display function.
        The function is called as
          function(substitution, [matches], longest_match_length)
        once each time matches need to be displayed."""
        if function is not None and not callable(function):
            raise TypeError("set_completion_display_matches_hook(func): "
                            "argument not callable")
        self.completion_display_matches_hook = function

state = _ReadlineState()
