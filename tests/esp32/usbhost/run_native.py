#!/usr/bin/env python3
"""Test the native HID backend with POSIX queue/task substitutes and sanitizers.

This tests application lifecycle, errors, and parsing. It cannot test USB hardware,
the actual ESP-IDF host driver, or physical hotplug timing.
"""

import os
from pathlib import Path
import shlex
import subprocess
import tempfile

TEST = Path(__file__).resolve().parent
MODULE = TEST.parents[2] / "m5stack/cmodules/usbhost"

with tempfile.TemporaryDirectory(prefix="uiflow-usbhost-") as temporary:
    output = Path(temporary)
    for header in (
        "freertos/FreeRTOS.h",
        "freertos/event_groups.h",
        "freertos/queue.h",
        "freertos/task.h",
        "esp_err.h",
        "esp_log.h",
        "usb/usb_host.h",
        "usb/hid_host.h",
        "usb/uvc_host.h",
        "esp_heap_caps.h",
    ):
        p = output / header
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('#include "fakes.h"\n')
    binary = output / "test_native"
    command = shlex.split(os.environ.get("CC", "cc")) + [
        "-std=c11",
        "-g",
        "-Wall",
        "-Wextra",
        "-Werror",
        "-Wno-unused-parameter",
        "-fsanitize=address,undefined",
        "-fno-omit-frame-pointer",
        "-pthread",
        "-I" + str(output),
        "-I" + str(TEST),
        "-I" + str(MODULE),
        str(TEST / "test_native.c"),
        str(MODULE / "hid_report.c"),
        "-o",
        str(binary),
    ]
    subprocess.run(command, check=True)
    subprocess.run([str(binary)], check=True)
    print(
        "PASS: HID reports, startup failures, unplug, queue overflow, cleanup/retry, HID/UVC ownership, retained frames, disconnect/retry and 200 lifecycle cycles (ASan/UBSan)"
    )
