#include "pyhelper.h"
#include "pyreadline.h"

namespace py {

static void (*_call)(void*) = [] (void*) {};

void
call(void *pyobj)
{
    _call(pyobj);
}
}

PYREADLINE_EXPORT void
set_py_funcs(void (*call)(void*))
{
    py::_call = call ? call : [] (void*) {};
}
