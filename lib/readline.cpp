extern "C" {
#include "readline_api.h"
}

#include <string.h>
#include <stdlib.h>
#include <locale.h>
#include <string>

#define PYREADLINE_EXPORT __attribute__((visibility("default")))
#define PYREADLINE_INLINE __attribute__((always_inline)) inline

#ifdef HAVE_CONFIG_H
#  undef HAVE_CONFIG_H /* Else readline/chardefs.h includes strings.h */
#endif
#include <readline/readline.h>
#include <readline/history.h>

int history_length = -1;

class locale_saver {
    char *m_saved_locale;
    locale_saver(const locale_saver&) = delete;
public:
    PYREADLINE_INLINE
    locale_saver()
        : m_saved_locale(strdup(setlocale(LC_CTYPE, NULL)))
    {
    }
    PYREADLINE_INLINE
    ~locale_saver()
    {
        setlocale(LC_CTYPE, m_saved_locale);
        free(m_saved_locale);
    }
};

#define completion_matches rl_completion_matches
// static void on_completion_display_matches_hook(char **matches, int num_matches,
//                                                int max_length);

// Do not free the string in rl_completer_word_break_characters since
// other libraries (e.g. R) might use statically allocated pointer.
static std::string completer_word_break_characters =
    " \t\n`~!@#$%^&*()-=+[{]}\\|;:'\",<>/?";

void
parse_and_bind(const char *s)
{
    std::string copy = s;
    rl_parse_and_bind(&copy[0]);
}

int
read_init_file(const char *s)
{
    return rl_read_init_file(s);
}

int
read_history_file(const char *s)
{
    return read_history(s);
}

int
write_history_file(const char *s)
{
    int err = write_history(s);
    if (!err && history_length >= 0) {
        history_truncate_file(s, history_length);
    }
    return err;
}
