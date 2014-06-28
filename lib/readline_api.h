// API for cffi

extern int history_length;
extern rl_compdisp_func_t *rl_completion_display_matches_hook;
extern rl_hook_func_t *rl_startup_hook;
extern rl_hook_func_t *rl_pre_input_hook;
extern int rl_completion_type;
extern char *rl_completer_word_break_characters;
extern char *rl_line_buffer;
extern int rl_attempted_completion_over;
extern int rl_completion_append_character;
extern int rl_completion_suppress_append;
extern rl_completion_func_t *rl_attempted_completion_function;

void parse_and_bind(const char *s);
int rl_read_init_file(const char*);
int read_history(const char*);
int write_history_file(const char *s);
void set_py_funcs(void (*)(void*));
void set_completer_delims(const char *s);
int remove_history_item(int pos);
int replace_history_item(int pos, const char *line);
void add_history(const char*);
const char *get_history_item(int i);
int get_history_length();
void clear_history();
int rl_insert_text(const char*);
void rl_redisplay();
char *strdup(const char*);
char **rl_completion_matches(const char*, rl_compentry_func_t*);
void setup_readline();
