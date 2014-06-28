#ifndef __PYREADLINE_H
#define __PYREADLINE_H

#include <string.h>
#include <stdlib.h>
#include <locale.h>
#include <string>

#include <readline/readline.h>
#include <readline/history.h>

extern "C" {
#include "readline_api.h"
}

#define PYREADLINE_EXPORT __attribute__((visibility("default")))
#define PYREADLINE_INLINE __attribute__((always_inline)) inline

#endif
