# multipl display example
import sys
import M5
import lvgl as lv

M5.begin()

# lvgl init
M5.Lcd.lvgl_init()

# init function update in lvgl9. ref: https://github.com/lvgl/lvgl/issues/4011 
# lv_disp_t * disp = lv_disp_create(hor_res, ver_res)
# lv_disp_set_flush_cb(disp, flush_cb);
# lv_disp_set_draw_buffers(disp, buf1, buf2, buf_size_in_bytes, mode);

# create display 0
disp0 = lv.disp_create(M5.getDisplay(0).width(), M5.getDisplay(0).height())
disp0.set_flush_cb(M5.Lcd.lvgl_flush)
buf1_0 = bytearray(M5.getDisplay(0).width() * 10 * lv.color_t.__SIZE__)
disp0.set_draw_buffers(buf1_0, None, len(buf1_0), lv.DISP_RENDER_MODE.PARTIAL)
disp0.set_user_data({"display_index": 0})

# create display 1
disp1 = lv.disp_create(M5.getDisplay(1).width(), M5.getDisplay(1).height())
disp1.set_flush_cb(M5.Lcd.lvgl_flush)
buf1_1 = bytearray(M5.getDisplay(1).width() * 10 * lv.color_t.__SIZE__)
disp1.set_draw_buffers(buf1_1, None, len(buf1_1), lv.DISP_RENDER_MODE.PARTIAL)
disp1.set_user_data({"display_index": 1})

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
# init function update in lvgl9. ref: https://github.com/lvgl/lvgl/issues/4011 
# lv_indev_t * indev = lv_indev_create();
# lv_indev_set_type(indev, LV_INDEV_TYPE_...);
# lv_indev_set_read_cb(indev, read_cb);
indev_drv = lv.indev_create()
indev_drv.set_disp(disp0)  # input device assigned to display 0
indev_drv.set_type(lv.INDEV_TYPE.POINTER)
indev_drv.set_read_cb(M5.Lcd.lvgl_read)

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
