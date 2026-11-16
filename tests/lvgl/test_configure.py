"""Run the actual LVGL CMake configuration against generated-file states."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
BINDINGS = ROOT / "m5stack/cmodules/lv_binding_micropython/micropython.cmake"


class ConfigureTests(unittest.TestCase):
    def test_generated_binding_lifecycle(self):
        with tempfile.TemporaryDirectory(prefix="lvgl-config-") as directory:
            project = Path(directory) / "source"
            build = Path(directory) / "build"
            project.mkdir()
            build.mkdir()
            (project / "bindings").mkdir()
            (project / "consumer").mkdir()
            (project / "CMakeLists.txt").write_text(
                "cmake_minimum_required(VERSION 3.16)\n"
                "project(LVGLConfigureRegression LANGUAGES C)\n"
                "add_subdirectory(bindings)\n"
                "add_subdirectory(consumer)\n"
            )
            (project / "bindings/CMakeLists.txt").write_text(
                "add_library(usermod INTERFACE)\n"
                f'include("{BINDINGS}")\n'
                'add_custom_target(generate_bindings DEPENDS "${LV_MP}")\n'
            )
            (project / "consumer/CMakeLists.txt").write_text(
                'add_library(consumer STATIC "${CMAKE_BINARY_DIR}/lv_mp.c")\n'
            )

            def configure():
                result = subprocess.run(
                    ["cmake", "-G", "Ninja", "-S", str(project), "-B", str(build)],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                self.assertEqual(result.returncode, 0, result.stdout)

            output = build / "lv_mp.c"
            preprocessed = build / "lv_mp.c.pp"
            preprocessed.write_text("stale preprocessing")
            configure()
            self.assertEqual(output.read_bytes(), b"")
            self.assertFalse(preprocessed.exists())
            generated = b"/* Valid generated bindings must survive reconfiguration. */\n"
            output.write_bytes(generated)
            preprocessed.write_text("valid preprocessing")
            timestamp = output.stat().st_mtime_ns
            for _ in range(2):
                configure()
                self.assertEqual(output.read_bytes(), generated)
                self.assertEqual(output.stat().st_mtime_ns, timestamp)
                self.assertEqual(preprocessed.read_text(), "valid preprocessing")
            output.write_bytes(b"")
            configure()
            self.assertEqual(output.read_bytes(), b"")
            self.assertFalse(
                preprocessed.exists(), "Invalidate preprocessing to force binding regeneration"
            )
            result = subprocess.run(
                ["ninja", "-C", str(build), "-n", "generate_bindings"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("LV_BINDINGS CPP", result.stdout)
            self.assertIn("LV_BINDINGS GEN MPY", result.stdout)


if __name__ == "__main__":
    unittest.main()
