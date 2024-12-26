# NeoPixel driver for MicroPython
# MIT license; Copyright (c) 2016 Damien P. George, 2021 Jim Mussared
# Copyright (c) 2024 M5Stack Technology CO LTD

from machine import bitstream, Pin


class NeoPixel:
    """
    note:
        en: NeoPixel is a class to control WS2812 and similar LED strips using a single pin. It allows setting individual
            LED colors, filling the strip with a color, and adjusting brightness.

    details:
        link: https://docs.m5stack.com/en/unit/neopixel
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/neopixel/neopixel_01.webp
        category: Unit

    example:
        - ../../../examples/unit/neopixel/neopixel_cores3_example.py

    m5f2:
        - unit/neopixel/neopixel_cores3_example.m5f2
    """

    ORDER = (1, 0, 2, 3)

    def __init__(self, pin: Pin, n: int, bpp: int = 3, timing: int = 1) -> None:
        """
        note:
            en: Initialize the NeoPixel object with the specified pin, number of LEDs, bytes per pixel (bpp), and timing.

        params:
            pin:
                note: The Pin object used to control the NeoPixel strip.
            n:
                note: The number of LEDs in the strip.
            bpp:
                note: The number of bytes per pixel (3 for RGB, 4 for RGBW). Default is 3.
            timing:
                note: The timing for signal transmission, can be 1 for 800kHz or 0 for 400kHz, or custom timing in ns. Default is 1.
        """
        self.pin = pin
        self.n = n
        self.bpp = bpp
        self.buf = bytearray(n * bpp)
        self.pin.init(pin.OUT)
        self.timing = (
            ((400, 850, 800, 450) if timing else (800, 1700, 1600, 900))
            if isinstance(timing, int)
            else timing
        )

    def __len__(self) -> int:
        """
        note:
            en: Return the number of LEDs in the NeoPixel strip.

        params:
            note:
        """
        return self.n

    def __setitem__(self, i: int, v: int) -> None:
        """
        note:
            en: Set the color of the LED at the specified index using the provided RGB values.

        params:
            i:
                note: The index of the LED to set.
            v:
                note: A tuple containing the RGB values for the LED.
        """
        offset = i * self.bpp
        for i in range(self.bpp):
            self.buf[offset + self.ORDER[i]] = v[i]

    def __getitem__(self, i: int) -> tuple:
        """
        note:
            en: Get the color of the LED at the specified index as an RGB tuple.

        params:
            i:
                note: The index of the LED to get.

        returns:
            note: A tuple containing the RGB values of the LED.
        """
        offset = i * self.bpp
        return tuple(self.buf[offset + self.ORDER[i]] for i in range(self.bpp))

    def fill(self, v: int) -> None:
        """
        note:
            en: Fill the entire NeoPixel strip with the specified color.

        params:
            v:
                note: A tuple containing the RGB (or RGBW) values to fill the strip with.
        """
        b = self.buf
        l = len(self.buf)
        bpp = self.bpp
        for i in range(bpp):
            c = v[i]
            j = self.ORDER[i]
            while j < l:
                b[j] = c
                j += bpp

    def write(self) -> None:
        """
        note:
            en: Write the current buffer to the NeoPixel strip to update the LED colors.
        """
        bitstream(self.pin, 0, self.timing, self.buf)

    def color_to_rgb(self, c: int) -> tuple:
        """
        note:
            en: Convert a color value (in the form R << 16 | G << 8 | B) to an RGB tuple.

        params:
            c:
                note: The color value in the form R << 16 | G << 8 | B.

        returns:
            note: A tuple containing the RGB values.
        """
        v = []
        v.append(int(((c >> 16) & 0xFF) * self.br))  # R
        v.append(int(((c >> 8) & 0xFF) * self.br))  # G
        v.append(int(((c >> 0) & 0xFF) * self.br))  # B
        return tuple(v)

    def color_to_wrgb(self, c: int) -> tuple:
        """
        note:
            en: Convert a color value (in the form W << 24 | R << 16 | G << 8 | B) to a WRGB tuple.

        params:
            c:
                note: The color value in the form W << 24 | R << 16 | G << 8 | B.

        returns:
            note: A tuple containing the WRGB values.
        """
        v = []
        v.append(int(((c >> 16) & 0xFF) * self.br))  # R
        v.append(int(((c >> 8) & 0xFF) * self.br))  # G
        v.append(int(((c >> 0) & 0xFF) * self.br))  # B
        v.append(int(((c >> 24) & 0xFF) * self.br))  # W
        return tuple(v)

    def set_color(self, i, c: int) -> None:
        """
        note:
            en: Set the color of the LED at the specified index.

        params:
            i:
                note: The index of the LED to set.
            c:
                note: The color value to set the LED to (in RGB or RGBW format).
        """
        offset = i * self.bpp
        v = None
        if self.bpp == 3:
            v = self.color_to_rgb(c)
        elif self.bpp == 4:
            v = self.color_to_wrgb(c)
        for i in range(self.bpp):
            self.buf[offset + self.ORDER[i]] = v[i]
        self.write()

    def fill_color(self, c: int) -> None:
        """
        note:
            en: Fill the entire NeoPixel strip with the specified color.

        params:
            c:
                note: The color value to fill the strip with (in RGB or RGBW format).
        """
        v = None
        if self.bpp == 3:
            v = self.color_to_rgb(c)
        elif self.bpp == 4:
            v = self.color_to_wrgb(c)
        self.fill(v)
        self.write()

    def set_brightness(self, br: int) -> None:
        """
        note:
            en: Set the brightness for the NeoPixel strip.

        params:
            br:
                note: The brightness level as a percentage (0-100).
        """
        b = self.buf
        self.br = br / 100.0
        for i in range(len(self.buf)):
            self.buf[i] = int(b[i] * self.br)
        self.write()
