# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# https://www.displayfuture.com/Display/datasheet/controller/SH1107.pdf

from micropython import const
from framebuf import FrameBuffer, MONO_VLSB, MONO_HMSB, MONO_HLSB

SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_DCDC_MODE = const(0xAD)
SET_MEM_MODE = const(0x20)
SET_PAGE_ADDR = const(0xB0)
SET_COL_LO_ADDR = const(0x00)
SET_COL_HI_ADDR = const(0x10)
SET_DISP_START_LINE = const(0xDC)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)

TEST_CHUNK = const(8)


class SH1107(FrameBuffer):
    def __init__(self, width, height, external_vcc):
        self.external_vcc = external_vcc
        if width == 128 and height == 64:
            self.page_mode = False
        elif (width == 64 and height == 128) or (width == 128 and height == 128):
            self.page_mode = True
        else:
            raise ValueError
        self.width = width
        self.height = height
        self.pages = self.height // 8
        self.line_bytes = self.width // 8
        size = self.width * self.height // 8
        self.curr_buffer = bytearray(b"\x00" * size)  # self.fill(0)
        self.prev_buffer = bytearray(b"\xff" * size)  # force full refresh
        super().__init__(
            self.curr_buffer, self.width, self.height, MONO_VLSB if self.page_mode else MONO_HMSB
        )
        self.init_display()
        self.fill(0)
        self.show()
        try:
            self.image(27, 0, "/flash/img/m5stack.pbm")
            self.show()
        except:
            pass

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00,  # off
            # address setting
            # 0x00 = page, 0x01 = vertical
            SET_MEM_MODE | (0x00 if self.page_mode else 0x01),
            # resolution and layout
            SET_DISP_START_LINE,
            0x00,
            SET_SEG_REMAP | 0x00,  # 0x01 rotate 180 deg
            # 0x08 rotate 180 deg
            SET_COM_OUT_DIR | (0x00 if self.page_mode else 0x08),
            SET_MUX_RATIO,
            0x7F,  # always this?
            # offseted for 64 x 128 (Aliexpress 0.96")
            SET_DISP_OFFSET,
            0x60 if self.width != self.height else 0x00,
            # timing and driving scheme
            SET_DISP_CLK_DIV,
            0x50,
            SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL,
            0x35,  # 0.77 * Vcc
            SET_DCDC_MODE,
            0x81,  # on, 0.6 * switch freq
            # display
            SET_CONTRAST,
            0x80,  # very low to avoid uneven background
            SET_ENTIRE_ON | 0x00,  # output follows RAM contents, not entire on
            SET_NORM_INV | 0x00,  # 0x00 = not inverted, 0x01 = inverted
        ):
            self.write_cmd(cmd)
        # buffers are initialized as if self.fill(0) was called
        self.show()
        self.poweron()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def image(self, x, y, filename):
        with open(filename, "rb") as f:
            f.readline()
            f.readline()
            width, height = [int(v) for v in f.readline().split()]
            data = bytearray(f.read())
        image = FrameBuffer(data, width, height, MONO_HLSB)
        self.blit(image, x, y)

    def show(self):
        if self.page_mode:
            self.show_page_mode()
        else:
            self.show_vert_mode()
        self.prev_buffer[:] = self.curr_buffer

    def show_page_mode(self):
        for page in range(self.pages):
            noffs = page * self.width
            for col1, col2 in self.test_modified(noffs, self.width):
                c = col1 - noffs
                self.write_cmd(SET_PAGE_ADDR | page)
                self.write_cmd(SET_COL_LO_ADDR | (c & 0x0F))
                self.write_cmd(SET_COL_HI_ADDR | ((c & 0x70) >> 4))
                self.write_data(self.curr_buffer[col1:col2])
                # print('Write offsets {} : {}, col: {}'.format(col1, col2, c))

    def show_vert_mode(self):
        for col in range(self.height):
            noffs = col * self.line_bytes
            for page1, page2 in self.test_modified(noffs, self.line_bytes):
                self.write_cmd(SET_PAGE_ADDR | (page1 - noffs))
                self.write_cmd(SET_COL_LO_ADDR | (col & 0x0F))
                self.write_cmd(SET_COL_HI_ADDR | ((col & 0x70) >> 4))
                self.write_data(self.curr_buffer[page1:page2])
                # print('Write offsets {} : {}, page: {}'.format(page1, page2, page1 - noffs))

    def test_modified(self, offs, width):
        ptr = offs
        width += offs
        while ptr < width:
            # skip unmodified chunks
            while (
                ptr < width
                and self.curr_buffer[ptr : ptr + TEST_CHUNK]
                == self.prev_buffer[ptr : ptr + TEST_CHUNK]
            ):
                ptr += TEST_CHUNK

            if ptr < width:
                first = ptr
                ptr += TEST_CHUNK
                # find modified chunks
                while (
                    ptr < width
                    and self.curr_buffer[ptr : ptr + TEST_CHUNK]
                    != self.prev_buffer[ptr : ptr + TEST_CHUNK]
                ):
                    ptr += TEST_CHUNK

                yield first, ptr
                ptr += TEST_CHUNK


class SH1107_I2C(SH1107):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.i2c_addr = addr
        self.temp = bytearray(2)
        self.write_list = [b"\x40", None]  # Co=0, D/C#=1
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.i2c_addr, self.temp)

    def write_data(self, buf):
        self.write_list[1] = buf
        self.i2c.writevto(self.i2c_addr, self.write_list)
