#include "readline_api.h"

#include <stddef.h>
#include <setjmp.h>
#include <signal.h>
#include <errno.h>
#include <sys/time.h>
#include <locale.h>
#include <string>

#ifdef HAVE_CONFIG_H
#  undef HAVE_CONFIG_H /* Else readline/chardefs.h includes strings.h */
#endif
#include <readline/readline.h>
#include <readline/history.h>

class locale_saver {
    char *m_saved_locale;
public:
    locale_saver()
        : m_saved_locale(strdup(setlocale(LC_CTYPE, NULL)))
    {
    }
    ~locale_saver()
    {
        setlocale(LC_CTYPE, m_saved_locale);
        free(m_saved_locale);
    }
};

#define completion_matches rl_completion_matches
static void on_completion_display_matches_hook(char **matches, int num_matches,
                                               int max_length);

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
