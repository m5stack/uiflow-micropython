import time
import M5


def fit_line(display, text, font, available):
    if display.textWidth(text, font) <= available:
        return text
    suffix = "..."
    if display.textWidth(suffix, font) > available:
        return ""
    while text and display.textWidth(text + suffix, font) > available:
        text = text[:-1]
    return text + suffix


def draw_messages(messages):
    display = M5.Lcd
    # Set rotation for your board before calling this function.
    display.setTextSize(1)
    # drawString uses the default top-left text datum.
    display.setTextColor(0xFFFFFF, 0x101820)
    display.fillScreen(0x101820)
    width, height = display.width(), display.height()
    font = display.FONTS.DejaVu12
    margin, gap = 8, 6
    line_height = display.fontHeight(font)
    y = margin
    for message in messages:
        if y + line_height > height - margin:
            break
        text = fit_line(display, message, font, width - 2 * margin)
        x = (width - display.textWidth(text, font)) // 2
        display.drawString(text, x, y, font)
        y += line_height + gap


def setup():
    M5.begin()
    messages = (
        "PHONE CAMERA -> STICK",
        "CANVA CLICKER",
        "USB: PLUG IN",
        "RFID2 absent (0x28)",
        "Uptime: 123456 seconds",
    )
    draw_messages(messages)


if __name__ == "__main__":
    setup()
    while True:
        M5.update()
        time.sleep_ms(20)
