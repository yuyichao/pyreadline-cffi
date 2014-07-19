#include "pyreadline.h"
#include <sys/select.h>

PYREADLINE_EXPORT int py_history_length = -1;

PYREADLINE_EXPORT void
py_parse_and_bind(const char *s)
{
    std::string copy = s;
    rl_parse_and_bind(&copy[0]);
}

PYREADLINE_EXPORT int
py_write_history_file(const char *s)
{
    int err = write_history(s);
    if (!err && py_history_length >= 0) {
        history_truncate_file(s, py_history_length);
    }
    return err;
}

// Do not free the string in rl_completer_word_break_characters since
// other libraries (e.g. R) might use statically allocated pointer.
/* All nonalphanums except '.' */
static std::string completer_word_break_characters =
    " \t\n`~!@#$%^&*()-=+[{]}\\|;:'\",<>/?";

PYREADLINE_EXPORT void
py_set_completer_delims(const char *s)
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
py_remove_history_item(int pos)
{
    if (HIST_ENTRY *entry = remove_history(pos)) {
        _free_history_entry(entry);
        return 1;
    }
    return 0;
}

PYREADLINE_EXPORT int
py_replace_history_item(int pos, const char *line)
{
    if (HIST_ENTRY *old_entry = replace_history_entry(pos, line, nullptr)) {
        _free_history_entry(old_entry);
        return 1;
    }
    return 0;
}

PYREADLINE_EXPORT const char*
py_get_history_item(int idx)
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
py_get_history_length()
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

PYREADLINE_EXPORT void
py_setup_readline()
{
    locale_saver saver();

    using_history();
    rl_readline_name = "python";
    /* Force rebind of TAB to insert-tab */
    rl_bind_key('\t', rl_insert);
    /* Bind both ESC-TAB and ESC-ESC to the completion function */
    rl_bind_key_in_map('\t', rl_complete, emacs_meta_keymap);
    rl_bind_key_in_map('\033', rl_complete, emacs_meta_keymap);
    /* Set Python word break characters */
    rl_completer_word_break_characters = &completer_word_break_characters[0];

    /* Initialize (allows .inputrc to override) */
    rl_initialize();
}

static char *completed_input_string;
static void
rlhandler(char *text)
{
    completed_input_string = text;
    rl_callback_handler_remove();
}

static char*
readline_until_enter_or_signal(const char *prompt, int *signal)
{
    char not_done_reading = '\0';
    fd_set selectset;

    *signal = 0;
    rl_catch_signals = 0;

    rl_callback_handler_install(prompt, rlhandler);
    FD_ZERO(&selectset);

    for (completed_input_string = &not_done_reading;
         completed_input_string == &not_done_reading;) {
        int has_input = 0;
        while (!has_input) {
            FD_SET(fileno(rl_instream), &selectset);
            /* select resets selectset if no input was available */
            has_input = select(fileno(rl_instream) + 1, &selectset,
                               nullptr, nullptr, nullptr);
        }

        if (has_input > 0) {
            rl_callback_read_char();
        } else if (errno == EINTR) {
            rl_free_line_state();
            rl_cleanup_after_signal();
            rl_callback_handler_remove();
            *signal = 1;
            completed_input_string = nullptr;
        }
    }

    return completed_input_string;
}

PYREADLINE_EXPORT char*
py_call_readline(FILE *sys_stdin, FILE *sys_stdout, const char *prompt)
{
    locale_saver saver();

    if (!sys_stdin)
        sys_stdin = stdin;
    if (!sys_stdout)
        sys_stdout = stdout;
    if (sys_stdin != rl_instream || sys_stdout != rl_outstream) {
        rl_instream = sys_stdin;
        rl_outstream = sys_stdout;
        rl_prep_terminal(1);
    }

    int signal;
    char *p = readline_until_enter_or_signal(prompt, &signal);
    /* we got an interrupt signal */
    if (signal) {
        return nullptr;
    }

    /* We got an EOF, return a empty string. */
    if (!p) {
        return strdup("");
    }

    /* we have a valid line */
    size_t n = strlen(p);
    if (n > 0) {
        int length = py_get_history_length();
        if (length <= 0 || strcmp(p, history_get(length)->line)) {
            add_history(p);
        }
    }

    p = (char*)realloc(p, n + 2);
    p[n] = '\n';
    p[n + 1] = '\0';
    return p;
}
