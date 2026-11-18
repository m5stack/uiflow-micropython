"""Exercise ESP-IDF cache recovery and the public Actions environment contract."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]


class IdSetupTest(unittest.TestCase):
    def run_setup(self, *, cached, environment=False, install_exit=0, repetitions=1):
        with tempfile.TemporaryDirectory(prefix="idf-cache-test-") as directory:
            work = Path(directory)
            tools = work / "bin"
            tools.mkdir()
            installer = work / "installer.sh"
            installer.write_text(
                '#!/bin/bash\n'
                'echo install >> "$TEST_TRACE"\n'
                'if [ "$TEST_INSTALL_EXIT" != 0 ]; then exit "$TEST_INSTALL_EXIT"; fi\n'
                'mkdir -p "$TEST_PYTHON_ENV/bin"\n'
                'touch "$TEST_PYTHON_ENV/bin/python"\n'
            )
            installer.chmod(0o755)
            git = tools / "git"
            git.write_text(
                '#!/bin/bash\n'
                'echo "git $*" >> "$TEST_TRACE"\n'
                'case "$*" in\n'
                '  "-C esp-idf describe --tags") echo v5.5.5 ;;\n'
                '  "clone --depth 1 --branch v5.5.5 https://github.com/espressif/esp-idf.git")\n'
                '    mkdir esp-idf; cp "$TEST_INSTALLER" esp-idf/install.sh ;;\n'
                '  "-C esp-idf submodule update --init --depth 1") ;;\n'
                '  *) echo "Unexpected git invocation: $*" >&2; exit 99 ;;\n'
                'esac\n'
            )
            git.chmod(0o755)
            if cached:
                sdk = work / "esp-idf"
                sdk.mkdir()
                (sdk / "install.sh").write_bytes(installer.read_bytes())
                (sdk / "install.sh").chmod(0o755)
            python_env = work / "python-env"
            if environment:
                (python_env / "bin").mkdir(parents=True)
                (python_env / "bin/python").touch()
            trace = work / "trace"
            env = dict(os.environ, PATH=str(tools) + os.pathsep + os.environ["PATH"],
                       TEST_INSTALLER=str(installer), TEST_TRACE=str(trace),
                       TEST_PYTHON_ENV=str(python_env), TEST_INSTALL_EXIT=str(install_exit))
            result = subprocess.run(
                ["bash", "-e", "-c", 'source "$1"\n' + "ci_esp32_idf555_setup\n" * repetitions,
                 "ci-cache-test", str(ROOT / "tools/ci.sh")],
                cwd=work, env=env, capture_output=True, text=True, check=False,
            )
            return result, trace.read_text().splitlines(), (python_env / "bin/python").exists()

    def test_cached_sdk_repairs_missing_python_environment(self):
        result, trace, environment = self.run_setup(cached=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(environment)
        self.assertIn("install", trace)
        self.assertFalse(any("clone" in command for command in trace))

    def test_valid_cache_can_be_checked_repeatedly(self):
        result, trace, environment = self.run_setup(cached=True, environment=True, repetitions=2)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(environment)
        self.assertEqual(trace.count("install"), 2)
        self.assertFalse(any("clone" in command for command in trace))

    def test_empty_cache_installs_sdk_submodules_and_environment(self):
        result, trace, environment = self.run_setup(cached=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(environment)
        self.assertTrue(any(command.startswith("git clone") for command in trace))
        update = trace.index("git -C esp-idf submodule update --init --depth 1")
        self.assertLess(update, trace.index("install"))

    def test_cached_environment_install_failure_is_reported(self):
        result, trace, environment = self.run_setup(cached=True, install_exit=17)
        self.assertEqual(result.returncode, 17)
        self.assertFalse(environment)
        self.assertEqual(trace[-1], "install")

    def test_empty_cache_install_failure_is_reported(self):
        result, trace, environment = self.run_setup(cached=False, install_exit=19)
        self.assertEqual(result.returncode, 19)
        self.assertFalse(environment)
        self.assertEqual(trace[-1], "install")


class WorkflowEnvironmentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = yaml.safe_load((ROOT / ".github/workflows/build-firmware.yml").read_text())

    def test_every_job_selects_python_before_restoring_compatible_cache(self):
        keys = []
        for name, job in self.workflow["jobs"].items():
            with self.subTest(job=name):
                self.assertEqual(job["runs-on"], "ubuntu-24.04")
                steps = job["steps"]
                python = next(i for i, step in enumerate(steps)
                              if step.get("uses", "").startswith("actions/setup-python@"))
                cache = next(i for i, step in enumerate(steps)
                             if step.get("uses", "").startswith("actions/cache@"))
                self.assertLess(python, cache)
                self.assertEqual(steps[python]["with"]["python-version"], "3.11")
                key = steps[cache]["with"]["key"]
                self.assertIn("runner.os", key)
                self.assertIn("runner.arch", key)
                self.assertIn("ubuntu24.04-idf-v5.5.5", key)
                self.assertIn("steps.python.outputs.python-version", key)
                keys.append(key)
        self.assertEqual(len(set(keys)), 1)

    def test_every_job_runs_sdk_setup_on_cache_hits_and_misses(self):
        for name, job in self.workflow["jobs"].items():
            with self.subTest(job=name):
                steps = job["steps"]
                installer = next(i for i, step in enumerate(steps)
                                 if "ci_esp32_idf555_setup" in step.get("run", ""))
                exporter = next(i for i, step in enumerate(steps)
                                if "source esp-idf/export.sh" in step.get("run", ""))
                self.assertLessEqual(installer, exporter)
                self.assertNotIn("if", steps[installer])
                run = steps[installer]["run"]
                if installer == exporter:
                    self.assertLess(run.index("ci_esp32_idf555_setup"), run.index("source esp-idf/export.sh"))


if __name__ == "__main__":
    unittest.main()
