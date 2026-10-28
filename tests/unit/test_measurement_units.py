# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import ast
from pathlib import Path
import re
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


ROOT = Path(__file__).resolve().parents[2]


class VoltageUnitsTest(unittest.TestCase):
    def test_adc_millivolts_are_returned_as_input_volts(self):
        path = ROOT / "m5stack/libs/base/dtu_nbiot2_v11.py"
        tree = ast.parse(path.read_text())
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef))
        method = next(node for node in cls.body if getattr(node, "name", None) == "get_voltage")
        namespace = {}
        # Exercise the production method without importing hardware-only modules.
        exec(compile(ast.Module(body=[method], type_ignores=[]), str(path), "exec"), namespace)
        for adc_mv, expected in ((0, 0), (1000, 11), (2000, 22)):
            with self.subTest(adc_mv=adc_mv):
                adc = Mock(return_value=adc_mv)
                device = SimpleNamespace(
                    m5ioe1=SimpleNamespace(read_adc_mv=adc), IOE1_VIN_ADC_PIN=2
                )
                self.assertAlmostEqual(namespace["get_voltage"](device), expected, places=4)
                adc.assert_called_once_with(2)


class SpeakerUnitsTest(unittest.TestCase):
    def test_ratio_boundaries_and_all_volume_round_trips(self):
        path = ROOT / "m5stack/components/M5Unified/mpy_m5spk.cpp"
        source = path.read_text()
        functions = []
        for name in ("spk_setVolumePercentage", "spk_getVolumePercentage"):
            match = re.search(r"    mp_obj_t " + name + r"\([^\n]+\) \{", source)
            self.assertIsNotNone(match, name)
            start = match.start()
            pos = match.end()
            depth = 1
            while depth:
                depth += (source[pos] == "{") - (source[pos] == "}")
                pos += 1
            functions.append(source[start:pos])

        # Compile the actual bindings with only the MicroPython/device boundary mocked.
        harness = (
            r"""
#include <cassert>
#include <cmath>
#include <cstdint>
using mp_obj_t = float;
constexpr mp_obj_t mp_const_none = 0;
float mp_obj_get_float(mp_obj_t obj) { return obj; }
mp_obj_t mp_obj_new_float(float value) { return value; }
struct Speaker {
    uint8_t volume = 0;
    void setVolume(uint8_t value) { volume = value; }
    uint8_t getVolume() { return volume; }
} speaker;
Speaker* getSpk(mp_obj_t*) { return &speaker; }
"""
            + "\n".join(functions)
            + r"""
int main() {
    for (int volume = 0; volume <= 255; ++volume) {
        speaker.setVolume(volume);
        float ratio = spk_getVolumePercentage(0);
        assert(std::fabs(ratio - volume / 255.0f) < 1e-6f);
        spk_setVolumePercentage(0, ratio);
        assert(speaker.volume == volume);
    }
    const float inputs[] = {-1, 0, 0.005f, 0.01f, 0.5f, 0.6f, 1, 1.1f, 100};
    const int expected[] = {0, 0, 1, 2, 127, 153, 255, 255, 255};
    for (unsigned i = 0; i < sizeof(inputs) / sizeof(inputs[0]); ++i) {
        spk_setVolumePercentage(0, inputs[i]);
        assert(speaker.volume == expected[i]);
    }
}
"""
        )
        with tempfile.TemporaryDirectory() as temp:
            executable = str(Path(temp) / "speaker_units")
            subprocess.run(
                [
                    "c++",
                    "-std=c++11",
                    "-Wall",
                    "-Wextra",
                    "-Werror",
                    "-x",
                    "c++",
                    "-o",
                    executable,
                    "-",
                ],
                input=harness,
                text=True,
                check=True,
            )
            subprocess.run([executable], check=True)


if __name__ == "__main__":
    unittest.main()
