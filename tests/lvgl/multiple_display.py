# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# multipl display example
import sys
import M5
import lvgl as lv

M5.begin()

# lvgl init
M5.Lcd.lvgl_init()

# create a display 0 buffer
disp_buf0 = lv.disp_draw_buf_t()
buf1_0 = bytearray(M5.getDisplay(0).width() * 10)
disp_buf0.init(buf1_0, None, len(buf1_0) // lv.color_t.__SIZE__)

# register display 0 driver
disp_drv_0 = lv.disp_drv_t()
disp_drv_0.init()
disp_drv_0.draw_buf = disp_buf0
disp_drv_0.flush_cb = M5.Lcd.lvgl_flush
disp_drv_0.hor_res = M5.getDisplay(0).width()
disp_drv_0.ver_res = M5.getDisplay(0).height()
disp_drv_0.user_data = {"display_index": 0}
disp0 = disp_drv_0.register()

# create a display 1 buffer
disp_buf1 = lv.disp_draw_buf_t()
buf1_1 = bytearray(M5.getDisplay(1).width() * 10)
disp_buf1.init(buf1_1, None, len(buf1_1) // lv.color_t.__SIZE__)

# register display 1 driver
disp_drv_1 = lv.disp_drv_t()
disp_drv_1.init()
disp_drv_1.draw_buf = disp_buf1
disp_drv_1.flush_cb = M5.Lcd.lvgl_flush
disp_drv_1.hor_res = M5.getDisplay(1).width()
disp_drv_1.ver_res = M5.getDisplay(1).height()
disp_drv_1.user_data = {"display_index": 1}
disp1 = disp_drv_1.register()

# set default display to screen 0
lv.disp_t.set_default(disp0)
scr0 = lv.obj()
# create button widget on screen 0
btn0 = lv.btn(scr0)
btn0.align(lv.ALIGN.CENTER, 0, -50)
label0 = lv.label(btn0)
label0.set_text("LVGL Screen 0")
lv.scr_load(scr0)

# set default display to screen 1
lv.disp_t.set_default(disp1)
scr1 = lv.obj()
# create button widget on screen 1
btn1 = lv.btn(scr1)
btn1.align(lv.ALIGN.CENTER, 0, -50)
label1 = lv.label(btn1)
label1.set_text("LVGL Screen 1")
lv.scr_load(scr1)

# touch driver init
indev_drv = lv.indev_drv_t()
indev_drv.init()
indev_drv.disp = disp0  # input device assigned to display 0
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = M5.Lcd.lvgl_read
indev = indev_drv.register()

# Create an image from the jpg file
try:
    with open("res/img/uiflow.jpg", "rb") as f:
        jpg_data = f.read()
except:
    print("Could not find uiflow.jpg")
    sys.exit()

img_cogwheel_argb = lv.img_dsc_t({"data_size": len(jpg_data), "data": jpg_data})

# show image on screen 0
img0 = lv.img(scr0)
img0.set_src(img_cogwheel_argb)
img0.align(lv.ALIGN.CENTER, 0, 0)

# show image on screen 1
img1 = lv.img(scr1)
img1.set_src(img_cogwheel_argb)
img1.align(lv.ALIGN.CENTER, 0, 0)
