mp_uint_t gfx_read(mp_obj_t self, void *buf, mp_uint_t size, int *errcode) {
    return 0;
}

mp_uint_t gfx_write(mp_obj_t self, const byte *buf, mp_uint_t size, int *errcode) {
    auto gfx = getGfx(&self);

    static int32_t last_y_offset = gfx->getCursorY();
    const byte *i = buf;
    gfx->fillRect(gfx->getCursorX(), gfx->getCursorY(), gfx->fontWidth(), gfx->fontHeight(), gfx->getTextStyle().back_rgb888);
    while (i < buf + size) {
        uint8_t c = (uint8_t)utf8_get_char(i);
        i = utf8_next_char(i);
        if (c < 128) {
            if (c >= 0x20 && c <= 0x7e) {
                gfx->write(c);
            } else if (c == '\r') {
                gfx->write(c);
            } else if (c == '\n') {
                gfx->write(c);
                last_y_offset = gfx->getCursorY();
            }
            // Commands below are used by MicroPython in the REPL
            else if (c == '\b') {
                int16_t x_offset = gfx->getCursorX();
                int16_t y_offset = gfx->getCursorY();
                if (x_offset == 0) {
                    x_offset = (int16_t)(gfx->fontWidth() * (gfx->width() / gfx->fontWidth()));
                    y_offset = y_offset - gfx->fontHeight();
                }
                gfx->setCursor(x_offset - gfx->fontWidth(), y_offset);
            } else if (c == 0x1b) {
                if (i[0] == '[') {
                    if (i[1] == 'K') {
                        gfx->fillRect(gfx->getCursorX(), gfx->getCursorY(), gfx->fontWidth(), gfx->fontHeight(), gfx->getTextStyle().back_rgb888);
                        i += 2;
                    } else {
                        // Handle commands of the form \x1b[####D
                        uint16_t n = 0;
                        uint8_t j = 1;
                        for (; j < 6; j++)
                        {
                            if ('0' <= i[j] && i[j] <= '9') {
                                n = n * 10 + (i[j] - '0');
                            } else {
                                c = i[j];
                                break;
                            }
                        }
                        if (c == 'D') {
                            // UP and DOWN KEY
                            if (gfx->getCursorY() > last_y_offset) {
                                do {
                                    gfx->fillRect(0, gfx->getCursorY(), gfx->width(), gfx->fontHeight(), gfx->getTextStyle().back_rgb888);
                                    gfx->setCursor(gfx->getCursorX(), (gfx->getCursorY() - gfx->fontHeight()));
                                } while (gfx->getCursorY() > last_y_offset);
                                gfx->setCursor((gfx->fontWidth() * (gfx->width() / gfx->fontWidth())), last_y_offset);
                            }
                            if (gfx->getCursorY() == last_y_offset) {
                                gfx->fillRect((gfx->fontWidth() * 4), gfx->getCursorY(), (gfx->width() - gfx->fontWidth() * 4), gfx->fontHeight(), gfx->getTextStyle().back_rgb888);
                                gfx->setCursor((gfx->fontWidth() * 4), gfx->getCursorY());
                            }
                        }
                        if (c == 'J') {
                            if (n == 2) {

                            }
                        }
                        if (c == ';') {
                            uint16_t m = 0;
                            for (++j; j < 9; j++)
                            {
                                if ('0' <= i[j] && i[j] <= '9') {
                                    m = m * 10 + (i[j] - '0');
                                } else {
                                    c = i[j];
                                    break;
                                }
                            }
                            if (c == 'H') {

                            }
                        }
                        i += j + 1;
                        continue;
                    }
                }
            }
        }
    }
    gfx->fillRect(gfx->getCursorX(), gfx->getCursorY(), gfx->fontWidth(), gfx->fontHeight(), gfx->getTextStyle().fore_rgb888);
    return i - buf;
}

mp_uint_t gfx_ioctl(mp_obj_t self, mp_uint_t request, uintptr_t arg, int *errcode) {
    return 0;
}
