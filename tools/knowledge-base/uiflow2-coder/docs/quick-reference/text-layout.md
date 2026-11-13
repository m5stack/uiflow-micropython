# Text Layout Without Clipping

## Measure with the Rendering API

Read the logical screen width and height after setting the board-appropriate
rotation. A 135 x 240 portrait screen becomes 240 x 135 in landscape; fixed
coordinates from one orientation do not fit the other. For rectangular
screens, reserve margins and require `x + text_width <= width` and
`y + font_height <= height`. On a round screen, use an inset rectangle
whose corners lie inside the visible circle.

For `M5.Lcd` / M5GFX, use `textWidth(text, font)` and `fontHeight(font)`
with exactly the font used to draw. Account for text size, datum and padding;
the reference examples below use size 1 and the top-left datum. For
`m5ui` labels use LVGL's layout and fonts instead of M5GFX font objects.

## Choose Overflow Behavior

- **Shorten:** Keep a useful prefix and append `...` only after measuring
  the complete result. Preserve essential status/error details elsewhere.
- **Wrap:** Set an explicit available width, allow multiple lines and
  recompute height after changing the text. Wrapping alone does not ensure
  the label fits vertically.
- **Reduce font size:** Choose an available, readable smaller font and measure
  again. Do not shrink essential status text below a readable size just to
  retain decoration.

Do this again for changing values, not only the initial placeholder. A label
that fits `OK` may not fit `RFID2 absent (0x28)`.

## 135 x 240 and 320 x 240 References

This standalone M5GFX example fits long text to the current logical screen.
Use it on a 135 x 240 portrait display or a 320 x 240 landscape display;
the same measured layout handles both. It also handles a 240 x 135 landscape
screen without placing a status line below its bottom edge.

```python
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
```

The 135 x 240 and 320 x 240 layouts use 8-pixel margins, leaving 119 and
304 pixels of text width. Long text is shortened to fit. Show the full
message on a detail page when needed, and skip lines that cannot fit
vertically.

## M5UI Label Width and Height

`M5Label` has no constructor `w` or `h` parameters. Its initial size
follows content. Call `set_width()` after creating it. For full text use
`lv.label.LONG_MODE.WRAP` with content height; for a compact summary use
`DOTS` and a fixed height. `CLIP` hides overflow; `SCROLL` and
`SCROLL_CIRCULAR` reveal it over time. Select deliberately, rather than
assuming a fixed-width label always shows every character.

```python
import m5ui
import lvgl as lv

m5ui.init()
page = m5ui.M5Page(bg_c=0x101820)
page.screen_load()
page.update_layout()
margin = 8
status = m5ui.M5Label(
    "RFID2 absent (0x28)", x=margin, y=20,
    font=lv.font_montserrat_14, text_c=0xFFFFFF, parent=page,
)
status.set_width(page.get_content_width() - 2 * margin)
status.set_long_mode(lv.label.LONG_MODE.WRAP)
status.set_height(lv.SIZE_CONTENT)
status.update_layout()
if status.get_y() + status.get_height() > page.get_content_height() - margin:
    # A real application can move full text to a detail/scrollable page.
    status.set_height(20)
    status.set_long_mode(lv.label.LONG_MODE.DOTS)
```
For a round screen choose a narrower safe area before applying this example.
After `set_text()` call `update_layout()` before measuring height or
positioning the next widget. Parent bounds, padding and scroll position also
affect visibility; being within the panel's dimensions is necessary but not
sufficient when the parent is smaller.
