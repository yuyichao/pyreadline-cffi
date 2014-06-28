// API for cffi

extern int history_length;

void parse_and_bind(const char *s);
int read_init_file(const char *s);
int read_history_file(const char *s);
int write_history_file(const char *s);
void set_py_funcs(void (*)(void*));
