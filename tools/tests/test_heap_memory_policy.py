"""Exercise the prepared ESP32 port policy with and without detected PSRAM."""

import pathlib
import shutil
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


class HeapMemoryPolicyTest(unittest.TestCase):
    def test_runtime_capabilities(self):
        compiler = shutil.which("cc")
        self.assertIsNotNone(compiler)
        port = (ROOT / "micropython/ports/esp32/mpconfigport.h").read_text()
        policy = port[port.index("#ifndef MICROPY_GC_INITIAL_HEAP_SIZE") : port.index("// emitters")]
        gc = (ROOT / "micropython/py/gc.c").read_text()
        start = gc.index("    #ifdef MICROPY_GC_SPLIT_HEAP_MAX_GROWTH")
        stop = gc.index("\n\n    mp_state_mem_area_t *new_heap", start)
        growth = gc[start:stop]
        targets = ("ESP32", "ESP32S2", "ESP32S3", "ESP32C2", "ESP32C3", "ESP32C5", "ESP32C6", "ESP32C61", "ESP32P4")
        with tempfile.TemporaryDirectory() as directory:
            directory = pathlib.Path(directory)
            source = directory / "policy.c"
            executable = directory / "policy"
            for target in targets:
                for configured in (0, 1):
                    for override in (False, True):
                        with self.subTest(target=target, configured=configured, override=override):
                            initial = 56 * 1024 if target == "ESP32" else 64 * 1024
                            if target == "ESP32C2":
                                initial = 36 * 1024
                            prefix = ""
                            if override:
                                prefix = "#define MICROPY_GC_INITIAL_HEAP_SIZE (128 * 1024)\n#define MICROPY_GC_SPLIT_HEAP_MAX_GROWTH (12 * 1024)\n"
                            program = """#include <assert.h>
#include <stdint.h>
#include <stddef.h>
#define MALLOC_CAP_SPIRAM 1
#define MALLOC_CAP_8BIT 2
#define MIN(a,b) ((a) < (b) ? (a) : (b))
#define MAX(a,b) ((a) > (b) ? (a) : (b))
size_t external_bytes;
size_t heap_caps_get_total_size(unsigned caps) { assert(caps == 3); return external_bytes; }
""" + prefix + policy + """
size_t allocate_area(size_t total_heap, size_t needed, size_t avail) {
""" + growth + """
return to_alloc;
}
int main(void) {
external_bytes = 0;
"""
                            if override:
                                program += "assert(MICROPY_GC_INITIAL_HEAP_SIZE == 128 * 1024);\nassert(allocate_area(65536, 3000, 100000) == 12288);\n"
                            else:
                                program += "assert(MICROPY_GC_INITIAL_HEAP_SIZE == 36 * 1024);\nassert(allocate_area(65536, 3000, 100000) == 3000);\n"
                            program += "assert(allocate_area(65536, 20000, 100000) == 20000);\nassert(allocate_area(65536, 20000, 15000) == 15000);\nexternal_bytes = 8 * 1024 * 1024;\n"
                            if override:
                                program += "assert(MICROPY_GC_INITIAL_HEAP_SIZE == 128 * 1024);\nassert(allocate_area(65536, 3000, 100000) == 12288);\n"
                            else:
                                program += f"assert(MICROPY_GC_INITIAL_HEAP_SIZE == {initial});\nassert(allocate_area(65536, 3000, 100000) == 65536);\n"
                            program += "return 0;\n}\n"
                            source.write_text(program)
                            subprocess.run([compiler, "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", f"-DCONFIG_IDF_TARGET_{target}=1", f"-DCONFIG_SPIRAM={configured}", str(source), "-o", str(executable)], check=True, capture_output=True)
                            subprocess.run([str(executable)], check=True)


if __name__ == "__main__":
    unittest.main()
