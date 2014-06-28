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

/* Readline version >= 5.0 introduced a timestamp field into the history entry
   structure; this needs to be freed to avoid a memory leak.  This version of
   readline also introduced the handy 'free_history_entry' function, which
   takes care of the timestamp. */

PYREADLINE_INLINE static void
_free_history_entry(HIST_ENTRY *entry)
{
    histdata_t data = free_history_entry(entry);
    free(data);
}

PYREADLINE_EXPORT int
remove_history_item(int pos)
{
    if (HIST_ENTRY *entry = remove_history(pos)) {
        _free_history_entry(entry);
        return 1;
    }
    return 0;
}

PYREADLINE_EXPORT int
replace_history_item(int pos, const char *line)
{
    if (HIST_ENTRY *old_entry = replace_history_entry(pos, line, nullptr)) {
        _free_history_entry(old_entry);
        return 1;
    }
    return 0;
}

PYREADLINE_EXPORT const char*
get_history_item(int idx)
{
    if (HIST_ENTRY *hist_ent = history_get(idx)) {
        return hist_ent->line;
    }
    return nullptr;
}

/* XXX It may be possible to replace this with a direct use of history_length
 * instead, but it's not clear whether BSD's libedit keeps history_length up
 * to date. See issue #8065.*/

PYREADLINE_EXPORT int
get_history_length()
{
    HISTORY_STATE *hist_st = history_get_history_state();
    int length = hist_st->length;
    /* the history docs don't say so, but the address of hist_st changes each
       time history_get_history_state is called which makes me think it's
       freshly malloc'd memory...  on the other hand, the address of the last
       line stays the same as long as history isn't extended, so it appears to
       be malloc'd but managed by the history package... */
    free(hist_st);
    return length;
}
