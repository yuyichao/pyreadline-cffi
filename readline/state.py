# Copyright (C) 2014~2014 by Yichao Yu
# yyc1992@gmail.com

"""Readline global state
"""

from ._cffi import _ffi, _lib, _ffi_pystr, _to_cstr

try:
    range = xrange
except NameError:
    pass


class _ReadlineState(object):
    """Readline global state:
    Hooks, completers, current positions.
    """
    __slots__ = ('completion_display_matches_hook', 'startup_hook',
                 'pre_input_hook', 'completer', 'begidx', 'endidx')

    def __init__(self):
        self.completion_display_matches_hook = None
        self.startup_hook = None
        self.pre_input_hook = None
        self.completer = None
        self.begidx = 0
        self.endidx = 0

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
        # We cannot set this hook globally, since it replaces the
        # default completion display.
        if function is None:
            _lib.rl_completion_display_matches_hook = _ffi.NULL
        else:
            _lib.rl_completion_display_matches_hook = \
                _on_completion_display_matches_hook

    def set_startup_hook(self, function):
        """set_startup_hook([function]) -> None
        Set or remove the startup_hook function.
        The function is called with no arguments just
        before readline prints the first prompt."""
        if function is not None and not callable(function):
            raise TypeError("set_startup_hook(func): argument not callable")
        self.startup_hook = function

    def set_pre_input_hook(self, function):
        """set_pre_input_hook([function]) -> None
        Set or remove the pre_input_hook function.
        The function is called with no arguments after the first prompt
        has been printed and just before readline starts reading input
        characters."""
        if function is not None and not callable(function):
            raise TypeError("set_pre_input_hook(func): argument not callable")
        self.pre_input_hook = function

    def set_completer(self, function):
        """set_completer([function]) -> None
        Set or remove the completer function.
        The function is called as function(text, state),
        for state in 0, 1, 2, ..., until it returns a non-string.
        It should return the next possible completion starting with 'text'."""
        if function is not None and not callable(function):
            raise TypeError("set_completer(func): argument not callable")
        self.completer = function

pyrl_state = _ReadlineState()


# C function to call the Python completion_display_matches
@_ffi.callback('rl_compdisp_func_t')
def _on_completion_display_matches_hook(matches, num_matches, max_length):
    hook = pyrl_state.completion_display_matches_hook
    if hook is None:
        return
    try:
        subs = _ffi_pystr(matches[0])
        matches = [_ffi_pystr(matches[i + 1]) for i in range(num_matches)]
        hook(subs, matches, max_length)
    except:
        pass


# C functions to call the Python hooks.
@_ffi.callback('rl_hook_func_t')
def _on_startup_hook():
    try:
        return int(pyrl_state.startup_hook())
    except:
        return 0


@_ffi.callback('rl_hook_func_t')
def _on_pre_input_hook():
    try:
        return int(pyrl_state.pre_input_hook())
    except:
        return 0

_lib.rl_startup_hook = _on_startup_hook
_lib.rl_pre_input_hook = _on_pre_input_hook


# C function to call the Python completer.
@_ffi.callback('rl_compentry_func_t')
def _on_completion(text, state):
    if pyrl_state.completer is None:
        return _ffi.NULL
    _lib.rl_attempted_completion_over = 1
    try:
        r = pyrl_state.completer(_ffi_pystr(text), state)
        return _ffi.NULL if r is None else _lib.strdup(_to_cstr(r))
    except:
        return _ffi.NULL


# A more flexible constructor that saves the "begidx" and "endidx"
# before calling the normal completer */
@_ffi.callback('rl_completion_func_t')
def _flex_complete(text, start, end):
    _lib.rl_completion_append_character = 0
    _lib.rl_completion_suppress_append = 0
    pyrl_state.begidx = start
    pyrl_state.endidx = end
    return _lib.rl_completion_matches(text, _on_completion)

_lib.rl_attempted_completion_function = _flex_complete
