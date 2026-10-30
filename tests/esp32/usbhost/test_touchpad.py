"""Report sequencing and gesture regressions for the combined Tab5 USB demo."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "examples/hardware/usbhost"))
from tab5_mouse_transport import MouseTransport, Touchpad


class Mouse:
    def __init__(self):
        self.opened = True
        self.pending = False
        self.reports = []

    def is_open(self):
        return self.opened

    def busy(self):
        return self.pending

    def set_buttons(self, b1, b2, b3):
        self.buttons = b1 | (b2 << 1) | (b3 << 2)

    def set_axes(self, x, y):
        self.x, self.y = x, y

    def set_wheel(self, wheel):
        self.wheel = wheel

    def send_report(self):
        assert not self.pending
        self.reports.append((self.buttons, self.x, self.y, self.wheel))
        self.pending = True
        # Existing Mouse.send_report returns None after successful submission.


class Tests(unittest.TestCase):
    def setUp(self):
        self.mouse = Mouse()
        self.tx = MouseTransport(self.mouse)
        self.tx.poll()
        self.drain()
        self.mouse.reports.clear()
        self.pad = Touchpad(self.tx, (0, 0, 100, 100), {"right": (110, 0, 30, 30)})

    def drain(self):
        for _ in range(100):
            self.mouse.pending = False
            self.tx.poll()
            if not self.tx.queue and not self.tx.inflight:
                return
        self.fail("reports failed to drain")

    def test_click_edges_survive_busy_endpoint(self):
        self.mouse.pending = True
        self.tx.enqueue(1)
        self.tx.enqueue(0)
        self.tx.poll()
        self.assertEqual(self.mouse.reports, [])
        self.drain()
        self.assertEqual(self.mouse.reports, [(1, 0, 0, 0), (0, 0, 0, 0)])

    def test_large_movement_is_split_without_losing_distance(self):
        self.tx.enqueue(1, 400, -260, 5)
        self.tx.enqueue(0)
        self.drain()
        self.assertEqual(sum(r[1] for r in self.mouse.reports), 400)
        self.assertEqual(sum(r[2] for r in self.mouse.reports), -260)
        self.assertEqual(sum(r[3] for r in self.mouse.reports), 5)
        self.assertEqual(self.mouse.reports[-1], (0, 0, 0, 0))
        self.assertTrue(all(abs(n) <= 127 for r in self.mouse.reports for n in r[1:]))

    def test_disconnect_discards_clicks_and_reconnect_releases(self):
        self.tx.enqueue(1)
        self.mouse.opened = False
        self.tx.poll()
        self.mouse.opened = True
        self.drain()
        self.assertEqual(self.mouse.reports, [(0, 0, 0, 0)])

    def test_tap_emits_press_and_release_once(self):
        self.pad.update(0, 0, 0, 0)
        self.pad.update(1, 20, 20, 10)
        self.pad.update(0, 20, 20, 100)
        self.pad.update(0, 20, 20, 120)
        self.drain()
        self.assertEqual(self.mouse.reports, [(1, 0, 0, 0), (0, 0, 0, 0)])

    def test_movement_does_not_generate_tap_click(self):
        self.pad.update(1, 20, 20, 0)
        self.pad.update(1, 45, 20, 50)
        self.pad.update(0, 45, 20, 100)
        self.drain()
        self.assertFalse(any(r[0] for r in self.mouse.reports))

    def test_hold_drag_and_multitouch_release(self):
        self.pad.update(1, 20, 20, 0)
        self.pad.update(1, 20, 20, 450)
        self.pad.update(1, 40, 30, 500)
        self.pad.update(2, 40, 30, 510)
        self.drain()
        self.assertEqual(self.mouse.reports[-1], (0, 0, 0, 0))
        self.assertTrue(any(r[0] == 1 and r[1] == 20 for r in self.mouse.reports))

    def test_explicit_right_button_releases_outside_button(self):
        self.pad.update(1, 120, 10, 0)
        self.pad.update(1, 180, 80, 50)
        self.pad.update(0, 180, 80, 60)
        self.drain()
        self.assertEqual(self.mouse.reports, [(2, 0, 0, 0), (0, 0, 0, 0)])

    def test_queue_overflow_keeps_a_release_report(self):
        for i in range(65):
            self.tx.enqueue(i % 2)
        self.drain()
        self.assertEqual(self.tx.overflows, 1)
        self.assertEqual(self.mouse.reports[-1], (0, 0, 0, 0))


if __name__ == "__main__":
    unittest.main()
