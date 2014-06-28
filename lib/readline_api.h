// API for cffi

extern int history_length;
extern rl_compdisp_func_t *rl_completion_display_matches_hook;
extern rl_hook_func_t *rl_startup_hook;
extern rl_hook_func_t *rl_pre_input_hook;
extern int rl_completion_type;

void parse_and_bind(const char *s);
int read_init_file(const char *s);
int read_history_file(const char *s);
int write_history_file(const char *s);
void set_py_funcs(void (*)(void*));
