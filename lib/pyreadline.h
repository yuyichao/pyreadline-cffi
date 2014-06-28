#ifndef __PYREADLINE_H
#define __PYREADLINE_H

extern "C" {
#include "readline_api.h"
}

#include <string.h>
#include <stdlib.h>
#include <locale.h>
#include <string>

#define PYREADLINE_EXPORT __attribute__((visibility("default")))
#define PYREADLINE_INLINE __attribute__((always_inline)) inline

#endif
