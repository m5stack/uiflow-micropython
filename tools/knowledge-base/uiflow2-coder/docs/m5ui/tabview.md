
# M5TabView

M5TabView is a widget that can be used to create tabbed views in the user interface.

## MicroPython Example

#### tabview basic

This example creates a tabview.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
tabview0 = None
Tab1 = None
Tab2 = None
label1 = None
label2 = None
label3 = None

def setup():
    global page0, tabview0, Tab1, Tab2, label1, label2, label3

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    tabview0 = m5ui.M5TabView(
        x=0, y=-2, w=320, h=240, bar_size=60, bar_pos=lv.DIR.TOP, parent=page0
    )
    Tab1 = tabview0.add_tab("Tab1")
    Tab2 = tabview0.add_tab("Tab2")
    label1 = m5ui.M5Label("This is label1", x=0, y=0, parent=Tab1)

    page0.screen_load()
    label2 = m5ui.M5Label(
        "Hello World",
        x=0,
        y=0,
        text_c=0xFFCC00,
        bg_c=0x99FF99,
        bg_opa=255,
        font=lv.font_montserrat_24,
        parent=Tab1,
    )
    label3 = m5ui.M5Label("hello M5", x=0, y=0, parent=Tab2)
    label3.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)
    label3.set_text_color(0x6600CC, 255, 0)
    label3.set_bg_color(0x33FF33, 255, 0)

def loop():
    global page0, tabview0, Tab1, Tab2, label1, label2, label3
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## **API**

#### M5TabView

## `M5TabView`
Create a TabView object.

- Parameter `x` (`int`): The x position of the tab view.
- Parameter `y` (`int`): The y position of the tab view.
- Parameter `w` (`int`): The width of the tab view.
- Parameter `h` (`int`): The height of the tab view.
- Parameter `bar_size` (`int`): The size of the tab bar.
- Parameter `bar_pos` (`int`): The position of the tab bar.
- Parameter `parent` (`lv.obj`): The parent object to attach the tab view to. If not specified, the tab view will be attached to the default screen.

    None

```python
from m5ui import M5Label
import lvgl as lv

m5ui.init()
tabview0 = m5ui.M5TabView(x=0, y=-2, w=320, h=240, bar_size=60, bar_pos=lv.DIR.TOP, parent=page0)
```

### `add_tab`
Add a tab to the tab view.

- Parameter `text` (`str`): The text to display on the tab.
- Return type: lv.obj

```python
Tab1 = tabview0.add_tab("Tab1")
Tab2 = tabview0.add_tab("Tab2")
```

### `rename_tab`
Rename a tab in the tab view.

- Parameter `pos` (`int`): The position of the tab to rename.
- Parameter `txt` (`str`): The new text for the tab.

```python
tabview0.rename_tab(0, 'hello M5')
```

### `get_tab_active`

M5Label can be used in TabView. For specific usage, please refer to `m5ui.M5Label <m5ui.M5Label>` Documentation.
