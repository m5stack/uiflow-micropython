# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
# SPDX-License-Identifier: MIT


class MouseTransport:
    """Serialize existing USB Mouse reports, retaining button edges while busy."""

    def __init__(self, mouse):
        self.mouse = mouse
        self.queue = []
        self.buttons = 0
        self.connected = False
        self.inflight = False
        self.sent = 0
        self.completed = 0
        self.overflows = 0
        self.send_errors = 0

    def enqueue(self, buttons, dx=0, dy=0, wheel=0):
        if not self.connected:
            return
        if len(self.queue) >= 64:
            self.queue[:] = [[0, 0, 0, 0]]
            self.buttons = 0
            self.overflows += 1
            return
        # Movement can merge only across reports with unchanged button state.
        if self.queue and self.queue[-1][0] == buttons and (dx or dy or wheel):
            item = self.queue[-1]
            item[1] += dx
            item[2] += dy
            item[3] += wheel
        else:
            self.queue.append([buttons, dx, dy, wheel])
        self.buttons = buttons

    def poll(self):
        opened = self.mouse.is_open()
        if not opened:
            self.connected = False
            self.queue.clear()
            self.buttons = 0
            self.inflight = False
            return
        if not self.connected:
            self.connected = True
            self.queue[:] = [[0, 0, 0, 0]]
        if self.mouse.busy():
            return
        if self.inflight:
            self.completed += 1
            self.inflight = False
        if not self.queue:
            return
        item = self.queue[0]
        values = [max(-127, min(127, n)) for n in item[1:]]
        self.mouse.set_buttons(b1=item[0] & 1, b2=(item[0] >> 1) & 1, b3=0)
        self.mouse.set_axes(values[0], values[1])
        self.mouse.set_wheel(values[2])
        # Mouse.send_report() returns None on success in the existing library.
        try:
            if self.mouse.send_report() is False:
                return
        except OSError:
            # A USB reset can invalidate the endpoint between is_open and send.
            self.send_errors += 1
            self.connected = False
            self.queue.clear()
            self.inflight = False
            return
        self.inflight = True
        self.sent += 1
        for i, n in enumerate(values, 1):
            item[i] -= n
        if item[1:] == [0, 0, 0]:
            self.queue.pop(0)


class Touchpad:
    """Single-finger relative movement, tap, hold-to-drag and explicit buttons."""

    def __init__(self, transport, pad, buttons):
        self.tx = transport
        self.pad = pad
        self.rects = buttons
        self.mode = None
        self.previous = (0, 0)
        self.started = 0
        self.travel = 0
        self.dragging = False
        self.repeat_at = 0

    @staticmethod
    def inside(rect, x, y):
        rx, ry, w, h = rect
        return rx <= x < rx + w and ry <= y < ry + h

    def update(self, count, x, y, now):
        if not self.tx.connected:
            self.mode = None
            self.dragging = False
            return
        if count != 1:
            if self.mode == "pad":
                if count == 0 and now - self.started < 250 and self.travel < 12:
                    self.tx.enqueue(1)
                self.tx.enqueue(0)
            elif self.mode in ("left", "right"):
                self.tx.enqueue(0)
            self.mode = None
            self.dragging = False
            return
        if self.mode is None:
            if self.inside(self.pad, x, y):
                self.mode = "pad"
            else:
                self.mode = next(
                    (name for name, rect in self.rects.items() if self.inside(rect, x, y)),
                    "outside",
                )
            self.previous = (x, y)
            self.started = now
            self.travel = 0
            self.repeat_at = now
            if self.mode in ("left", "right"):
                self.tx.enqueue(1 if self.mode == "left" else 2)
        if self.mode == "pad":
            dx, dy = x - self.previous[0], y - self.previous[1]
            self.previous = (x, y)
            self.travel += abs(dx) + abs(dy)
            if not self.dragging and self.travel < 12 and now - self.started >= 450:
                self.dragging = True
                self.tx.enqueue(1)
            if dx or dy:
                self.tx.enqueue(1 if self.dragging else 0, dx, dy)
        elif self.mode in ("up", "down") and now >= self.repeat_at:
            self.tx.enqueue(0, wheel=1 if self.mode == "up" else -1)
            self.repeat_at = now + 150
