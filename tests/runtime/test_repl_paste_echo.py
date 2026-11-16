"""Exercise production friendly REPL paste loops with host I/O mocks."""
import argparse
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def function(source, signature):
    start = re.search(re.escape(signature) + r"\([^;]*?\)\s*\{", source).start()
    return source[start : source.index("\n}", start) + 2]


PRELUDE = r"""
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define CHAR_CTRL_A 1
#define CHAR_CTRL_B 2
#define CHAR_CTRL_C 3
#define CHAR_CTRL_D 4
#define CHAR_CTRL_E 5
#define PYEXEC_FORCED_EXIT 256
#define MICROPY_BANNER_NAME_AND_VERSION "test"
#define MICROPY_BANNER_MACHINE "host"
#define MICROPY_PY_BUILTINS_HELP 0
#define EXEC_FLAG_ALLOW_DEBUGGING 2
#define EXEC_FLAG_IS_REPL 4
#define EXEC_FLAG_SOURCE_IS_VSTR 16
#define MP_STATE_THREAD(x) (x)
#define MP_STATE_VM(x) (x)
typedef int mp_parse_input_kind_t;
enum { MP_PARSE_SINGLE_INPUT, MP_PARSE_FILE_INPUT };
enum { PYEXEC_MODE_FRIENDLY_REPL, PYEXEC_MODE_RAW_REPL };
static int pyexec_mode_kind, gc_lock_depth;
typedef struct { char buf[512]; size_t len; } vstr_t;
static vstr_t event_line, *repl_line = &event_line;
static char output[8192];
static size_t output_len, input_pos;
static bool silent, cancel_paste, exception;
static unsigned reads, executed;
static const char command[] = "print('paste test')\r";
static bool pyexec_friendly_repl_silent_paste(void) { return silent; }
static void mp_hal_stdout_tx_strn(const char *s, size_t n) {
    assert(output_len + n < sizeof(output));
    memcpy(output + output_len, s, n); output_len += n; output[output_len] = 0;
}
static void mp_hal_stdout_tx_str(const char *s) { mp_hal_stdout_tx_strn(s, strlen(s)); }
static void vstr_init(vstr_t *v, size_t size) { (void)size; v->len = 0; v->buf[0] = 0; }
static void vstr_clear(vstr_t *v) { vstr_init(v, 0); }
static void vstr_reset(vstr_t *v) { vstr_init(v, 0); }
static void vstr_add_byte(vstr_t *v, int c) { assert(v->len + 1 < sizeof(v->buf)); v->buf[v->len++] = c; v->buf[v->len] = 0; }
static size_t vstr_len(vstr_t *v) { return v->len; }
static char *vstr_null_terminated_str(vstr_t *v) { return v->buf; }
static void mp_hal_stdio_mode_raw(void) {}
static void mp_hal_stdio_mode_orig(void) {}
static const char *mp_repl_get_ps1(void) { return ">>> "; }
static const char *mp_repl_get_ps2(void) { return "... "; }
static bool mp_repl_continue_with_input(const char *s) { (void)s; return false; }
static int readline(vstr_t *v, const char *prompt) {
    (void)v; mp_hal_stdout_tx_str(prompt); return reads++ == 0 ? CHAR_CTRL_E : CHAR_CTRL_D;
}
static int readline_process_char(int c) { return c; }
static void readline_init(vstr_t *v, const char *prompt) { (void)v; mp_hal_stdout_tx_str(prompt); }
static void readline_note_newline(const char *prompt) { (void)prompt; }
static int mp_hal_stdin_rx_chr(void) {
    assert(input_pos <= strlen(command));
    if (input_pos == strlen(command)) { ++input_pos; return cancel_paste ? CHAR_CTRL_C : CHAR_CTRL_D; }
    return command[input_pos++];
}
static int parse_compile_execute(const void *source, int kind, int flags) {
    (void)flags; assert(kind == MP_PARSE_FILE_INPUT);
    const vstr_t *v = source;
    assert(strcmp(v->buf, command) == 0); ++executed;
    silent = false; // the real VM claims its ticket before user output
    mp_hal_stdout_tx_str(exception ? "Traceback: ValueError\r\n" : "PROGRAM_OUTPUT\r\n");
    return 0;
}
static int pyexec_raw_repl_process_char(int c) { (void)c; abort(); }
"""

CASES = r"""
int main(void) {
    for (int quiet = 0; quiet < 2; ++quiet) {
        for (int error = 0; error < 2; ++error) {
            for (int cancel = 0; cancel < 2; ++cancel) {
                output_len = input_pos = reads = executed = 0; output[0] = 0;
                silent = quiet; exception = error; cancel_paste = cancel;
#if EVENT_DRIVEN
                memset(&repl, 0, sizeof(repl)); vstr_init(repl_line, 32);
                assert(pyexec_friendly_repl_process_char(CHAR_CTRL_E) == 0);
                for (size_t i = 0; i < strlen(command); ++i) {
                    assert(pyexec_friendly_repl_process_char(command[i]) == 0);
                }
                assert(pyexec_friendly_repl_process_char(cancel ? CHAR_CTRL_C : CHAR_CTRL_D) == 0);
                assert(!repl.paste_mode);
#else
                assert(pyexec_friendly_repl() == PYEXEC_FORCED_EXIT);
#endif
                assert(executed == (unsigned)!cancel);
                assert((strstr(output, "=== ") != NULL) == !quiet);
                assert((strstr(output, "paste mode;") != NULL) == !quiet);
                assert((strstr(output, "print('paste test')") != NULL) == !quiet);
                assert((strstr(output, "PROGRAM_OUTPUT") != NULL) == (!cancel && !error));
                assert((strstr(output, "Traceback: ValueError") != NULL) == (!cancel && error));
            }
        }
    }
    puts("PASS: normal/silent paste, program output, exceptions and cancellation");
    return 0;
}
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sanitize", action="store_true")
    args = parser.parse_args()
    source = (ROOT / "micropython/shared/runtime/pyexec.c").read_text()
    for event in (False, True):
        parts = [PRELUDE]
        if event:
            start = source.index("typedef struct _repl_t")
            parts.append(source[start : source.index("repl_t repl;", start) + len("repl_t repl;")])
            parts.append(function(source, "static int pyexec_friendly_repl_process_char"))
        else:
            parts.append(function(source, "int pyexec_friendly_repl"))
        parts.append(CASES)
        with tempfile.TemporaryDirectory(prefix="repl-echo-") as tmp:
            test = Path(tmp) / "test.c"
            test.write_text("\n".join(parts))
            cmd = [
                "cc",
                "-std=c11",
                "-Wall",
                "-Wextra",
                "-Werror",
                "-Wno-unused-function",
                "-Wno-unused-variable",
                "-g",
                f"-DEVENT_DRIVEN={int(event)}",
            ]
            if args.sanitize:
                cmd += ["-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
            binary = Path(tmp) / "test"
            subprocess.run(cmd + [str(test), "-o", str(binary)], check=True)
            subprocess.run([str(binary)], check=True)


if __name__ == "__main__":
    main()
