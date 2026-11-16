"""Regress the shared M5UI display setup and allocation-failure cleanup."""
import ast
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "m5stack/libs/m5ui/port.py"


class Buffer:
    def __init__(self, owner, width, height):
        self.owner = owner
        self.width, self.height = width, height
        owner.live.append(self)

    def destroy(self):
        self.owner.live.remove(self)


class Allocator:
    def __init__(self, fail=(), null=False, limit=None):
        self.fail, self.null, self.limit = fail, null, limit
        self.calls, self.live = [], []

    def create(self, width, height, color, stride):
        self.calls.append((width, height))
        assert color == "rgb565" and stride == 0
        used = sum(b.width * b.height * 2 for b in self.live)
        if len(self.calls) in self.fail or (
            self.limit is not None and used + width * height * 2 > self.limit
        ):
            if self.null:
                return None
            raise MemoryError
        return Buffer(self, width, height)


class Driver:
    def set_draw_buffers(self, first, second):
        assert first is not None and second is not None
        self.buffers = first, second

    def __getattr__(self, name):
        return lambda *args: None


class DrawBufferTests(unittest.TestCase):
    def load(self, allocator):
        tree = ast.parse(SOURCE.read_text())
        tree.body = [
            n
            for n in tree.body
            if isinstance(n, ast.FunctionDef) and n.name in ("_create_draw_buffers", "_m5_init")
        ]
        self.collections = []
        self.driver = Driver()
        lv = SimpleNamespace(
            draw_buf_create=allocator.create,
            COLOR_FORMAT=SimpleNamespace(RGB565="rgb565"),
            DISPLAY_RENDER_MODE=SimpleNamespace(PARTIAL=0),
            INDEV_TYPE=SimpleNamespace(POINTER=0),
            display_create=lambda *args: self.driver,
            indev_create=Driver,
            fs_drv_t=Driver,
        )
        context = dict(
            lv=lv,
            gc=SimpleNamespace(collect=lambda: self.collections.append(True)),
            lv_utils=SimpleNamespace(fs_register=lambda *args: None),
            event_loop=lambda: None,
        )
        exec(compile(tree, str(SOURCE), "exec"), context)
        return context

    def test_all_boards_use_actual_display_dimensions(self):
        # No board-name API is exposed: setup must be independent of model IDs.
        for width, height in (
            (320, 240),
            (240, 240),
            (468, 468),
            (1280, 720),
            (800, 480),
            (64, 8),
        ):
            with self.subTest(size=(width, height)):
                alloc = Allocator()
                context = self.load(alloc)
                lcd = SimpleNamespace(lvgl_init=lambda: None, lvgl_flush=None, lvgl_read=None)
                display = SimpleNamespace(width=lambda: width, height=lambda: height)
                m5 = SimpleNamespace(begin=lambda: None, Lcd=lcd, getDisplay=lambda index: display)
                with patch.dict(sys.modules, M5=m5):
                    context["_m5_init"]()
                self.assertEqual(alloc.calls, [(width, height)] * 2)
                self.assertEqual(tuple(alloc.live), self.driver.buffers)

    def test_first_or_second_full_buffer_failure_releases_before_fallback(self):
        for null in (False, True):
            for failure in (1, 2):
                with self.subTest(null=null, failure=failure):
                    alloc = Allocator(fail=(failure,), null=null)
                    context = self.load(alloc)
                    buffers = context["_create_draw_buffers"](320, 240)
                    self.assertEqual([b.height for b in buffers], [10, 10])
                    self.assertEqual(alloc.live, list(buffers))
                    self.assertEqual(len(self.collections), 1)

    def test_limited_heap_does_not_retain_partial_full_buffer(self):
        # One full buffer fits, two do not. Without cleanup even strips won't fit.
        alloc = Allocator(limit=320 * 240 * 2)
        context = self.load(alloc)
        for _ in range(100):
            buffers = context["_create_draw_buffers"](320, 240)
            self.assertEqual([b.height for b in buffers], [10, 10])
            self.assertEqual(len(alloc.live), 2)
            for buffer in buffers:
                buffer.destroy()
            self.assertEqual(alloc.live, [])

    def test_exhausted_fallback_raises_and_releases_all_buffers(self):
        for null in (False, True):
            for failures in ((1, 2), (2, 3), (2, 4)):
                with self.subTest(null=null, failures=failures):
                    alloc = Allocator(fail=failures, null=null)
                    context = self.load(alloc)
                    with self.assertRaises(MemoryError):
                        context["_create_draw_buffers"](320, 240)
                    self.assertEqual(alloc.live, [])


if __name__ == "__main__":
    unittest.main()
