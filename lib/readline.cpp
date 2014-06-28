#include "pyreadline.h"

PYREADLINE_EXPORT int history_length = -1;

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

PYREADLINE_EXPORT void
parse_and_bind(const char *s)
{
    std::string copy = s;
    rl_parse_and_bind(&copy[0]);
}

PYREADLINE_EXPORT int
read_init_file(const char *s)
{
    return rl_read_init_file(s);
}

PYREADLINE_EXPORT int
read_history_file(const char *s)
{
    return read_history(s);
}

PYREADLINE_EXPORT int
write_history_file(const char *s)
{
    int err = write_history(s);
    if (!err && history_length >= 0) {
        history_truncate_file(s, history_length);
    }
    return err;
}

// Do not free the string in rl_completer_word_break_characters since
// other libraries (e.g. R) might use statically allocated pointer.
static std::string completer_word_break_characters =
    " \t\n`~!@#$%^&*()-=+[{]}\\|;:'\",<>/?";

PYREADLINE_EXPORT void
set_completer_delims(const char *s)
{
    /* Keep a reference to the allocated memory in the module state in case
       some other module modifies rl_completer_word_break_characters
       (see issue #17289). */
    completer_word_break_characters = s;
    rl_completer_word_break_characters = &completer_word_break_characters[0];
}
