# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import math


def hsv_to_rgb(hue: int = 0, sat: int = 0, val: int = 0) -> int:
    h = max(0, min(360, hue)) / 360.0
    s = max(0, min(100, sat)) / 100.0
    v = max(0, min(100, val)) / 100.0

    if s == 0:
        r = g = b = v
    else:
        h *= 6.0
        sector = math.floor(h)
        frac = h - sector
        p = v * (1 - s)
        q = v * (1 - s * frac)
        t = v * (1 - s * (1 - frac))

        r, g, b = [
            (v, t, p),
            (q, v, p),
            (p, v, t),
            (p, q, v),
            (t, p, v),
            (v, p, q),
        ][int(sector % 6)]

    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return (r << 16) | (g << 8) | b
