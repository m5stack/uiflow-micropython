# Fingerprint2 Unit

This library is the driver for Unit Fingerprint2.

Support the following products:

    Unit Fingerprint2

## MicroPython Example

#### Enroll and recognize

This example demonstrates how to use a fingerprint recognition module to perform
the complete process of fingerprint enrollment, identification, and deletion.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from unit import Fingerprint2Unit

page0 = None
btn_enroll = None
btn_recognize = None
btn_delete = None
label0 = None
label_tip = None
label_res = None
fingerprint2_0 = None
id2 = None
count = None
operation = None
i = None
g_id = None
res = None

def wait_for_finger_press():
    global \
        id2, \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_tip.set_text(str("Please place your finger"))
    while not (fingerprint2_0.get_enroll_image()):
        time.sleep_ms(100)
    Speaker.tone(888, 100)

def wait_for_finger_left():
    global \
        id2, \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_tip.set_text(str("Please remove your finger"))
    while fingerprint2_0.get_enroll_image():
        time.sleep_ms(100)

def enroll(id2, count):
    global \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_res.set_text(str(""))
    i = 0
    while i < count:
        wait_for_finger_press()
        if fingerprint2_0.gen_feature():
            i = (i if isinstance(i, (int, float)) else 0) + 1
            print(i)
        wait_for_finger_left()
    if fingerprint2_0.gen_template():
        if fingerprint2_0.store_template(g_id):
            label_res.set_text(str((str((str("Enroll ID: ") + str(g_id))) + str(" success!"))))
            operation = 0
            label_tip.set_text(str(""))
            if g_id < 98:
                g_id = (g_id if isinstance(g_id, (int, float)) else 0) + 1
            Speaker.tone(666, 100)

def recognize():
    global \
        id2, \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_res.set_text(str(""))
    label_tip.set_text(str("Please place your finger"))
    while not (fingerprint2_0.get_verify_image()):
        time.sleep_ms(100)
    label_tip.set_text(str(""))
    if fingerprint2_0.gen_feature():
        res = fingerprint2_0.find_match()
        if res:
            id2 = res[0]
            label_res.set_text(str((str("Recognize ID: ") + str(id2))))
            Speaker.tone(666, 100)
            operation = 0
    if operation != 0:
        operation = 0
        label_res.set_text(str("Recognize failed! "))
        Speaker.tone(999, 200)

def delete(id2):
    global \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_res.set_text(str(""))
    if g_id > 0:
        g_id = (g_id if isinstance(g_id, (int, float)) else 0) + -1
    if fingerprint2_0.delete_template(g_id):
        label_res.set_text(str((str("Delete ID: ") + str(g_id))))
    else:
        label_res.set_text(str("Delete failed!"))
        Speaker.tone(999, 200)
    operation = 0

def btn_enroll_clicked_event(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    operation = 1
    Speaker.tone(888, 100)

def btn_recognize_clicked_event(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    operation = 2
    Speaker.tone(888, 100)

def btn_delete_clicked_event(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    Speaker.tone(888, 100)
    operation = 3

def btn_enroll_event_handler(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_enroll_clicked_event(event_struct)
    return

def btn_recognize_event_handler(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_recognize_clicked_event(event_struct)
    return

def btn_delete_event_handler(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_delete_clicked_event(event_struct)
    return

def setup():
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    btn_enroll = m5ui.M5Button(
        text="enroll",
        x=14,
        y=165,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    btn_recognize = m5ui.M5Button(
        text="recognize",
        x=109,
        y=165,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    btn_delete = m5ui.M5Button(
        text="delete",
        x=229,
        y=165,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "Fingerprint enroll, recognize, delete",
        x=14,
        y=9,
        text_c=0x0F6DD1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_tip = m5ui.M5Label(
        "Tip:",
        x=46,
        y=61,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_res = m5ui.M5Label(
        "Result:",
        x=20,
        y=95,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    btn_enroll.add_event_cb(btn_enroll_event_handler, lv.EVENT.ALL, None)
    btn_recognize.add_event_cb(btn_recognize_event_handler, lv.EVENT.ALL, None)
    btn_delete.add_event_cb(btn_delete_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)
    fingerprint2_0 = Fingerprint2Unit(2, port=(1, 2))
    fingerprint2_0.activate_module()
    fingerprint2_0.set_work_mode(1, save=False)
    btn_enroll.set_size(80, 60)
    btn_enroll.align_to(page0, lv.ALIGN.CENTER, -105, 60)
    btn_recognize.set_size(100, 60)
    btn_recognize.align_to(page0, lv.ALIGN.CENTER, 0, 60)
    btn_delete.set_size(80, 60)
    btn_delete.align_to(page0, lv.ALIGN.CENTER, 105, 60)
    operation = 0
    g_id = 0

def loop():
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    M5.update()
    if operation == 1:
        enroll(1, 5)
    elif operation == 2:
        recognize()
    elif operation == 3:
        delete(1)
    else:
        pass

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

#### Upload and download template

This example demonstrates how to use a fingerprint recognition module to perform the complete process of fingerprint enrollment, identification, deletion,
and template upload/download.(The upload and download functions enable cross-device fingerprint recognition — a fingerprint enrolled on one module can be verified on another.
The fingerprint template transfer method can be customized according to user requirements, such as via serial communication, network, or cloud synchronization.)

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from unit import Fingerprint2Unit

page0 = None
btn_enroll = None
btn_upload = None
btn_recognize = None
btn_download = None
btn_delete = None
label0 = None
label_tip = None
label_res = None
fingerprint2_0 = None
id2 = None
count = None
operation = None
i = None
g_id = None
res = None

def wait_for_finger_press():
    global \
        id2, \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_tip.set_text(str("Please place your finger"))
    while not (fingerprint2_0.get_enroll_image()):
        time.sleep_ms(100)
    Speaker.tone(888, 100)

def wait_for_finger_left():
    global \
        id2, \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_tip.set_text(str("Please remove your finger"))
    while fingerprint2_0.get_enroll_image():
        time.sleep_ms(100)

def enroll(id2, count):
    global \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_res.set_text(str(""))
    i = 0
    while i < count:
        wait_for_finger_press()
        if fingerprint2_0.gen_feature():
            i = (i if isinstance(i, (int, float)) else 0) + 1
            print(i)
        wait_for_finger_left()
    if fingerprint2_0.gen_template():
        if fingerprint2_0.store_template(g_id):
            label_res.set_text(str((str((str("Enroll ID: ") + str(g_id))) + str(" success!"))))
            operation = 0
            label_tip.set_text(str(""))
            if g_id < 98:
                g_id = (g_id if isinstance(g_id, (int, float)) else 0) + 1
            Speaker.tone(666, 100)

def upload():
    global \
        id2, \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_res.set_text(str(""))
    if fingerprint2_0.load_template(0):
        label_tip.set_text(str("template uploading..."))
        if fingerprint2_0.upload_template("/flash/res/tp1.tzh"):
            label_tip.set_text(str(""))
            label_res.set_text(str((str((str("Upload ID: ") + str(0))) + str(" success!"))))
            Speaker.tone(666, 100)
        else:
            label_res.set_text(str((str((str("Upload ID: ") + str(0))) + str("failed!"))))
            Speaker.tone(999, 200)
    else:
        label_res.set_text(str("load template failed!"))
        Speaker.tone(999, 200)
    operation = 0

def recognize():
    global \
        id2, \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_res.set_text(str(""))
    label_tip.set_text(str("Please place your finger"))
    while not (fingerprint2_0.get_verify_image()):
        time.sleep_ms(100)
    label_tip.set_text(str(""))
    if fingerprint2_0.gen_feature():
        res = fingerprint2_0.find_match()
        if res:
            id2 = res[0]
            label_res.set_text(str((str("Recognize ID: ") + str(id2))))
            Speaker.tone(666, 100)
            operation = 0
    if operation != 0:
        operation = 0
        label_res.set_text(str("Recognize failed! "))
        Speaker.tone(999, 200)

def download():
    global \
        id2, \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_res.set_text(str(""))
    label_tip.set_text(str("download template"))
    if fingerprint2_0.download_template("/flash/res/tp1.tzh"):
        label_res.set_text(str("Download template success!"))
        if fingerprint2_0.store_template(66):
            operation = 0
            label_tip.set_text(str("store template"))
            label_res.set_text(str("Store template success!"))
            Speaker.tone(666, 100)
        else:
            label_res.set_text(str("Store template failed!"))
            Speaker.tone(999, 200)
    else:
        label_res.set_text(str("download template failed!"))
        Speaker.tone(999, 200)
    operation = 0

def delete(id2):
    global \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_res.set_text(str(""))
    if g_id > 0:
        g_id = (g_id if isinstance(g_id, (int, float)) else 0) + -1
    if fingerprint2_0.delete_template(g_id):
        label_res.set_text(str((str("Delete ID: ") + str(g_id))))
    else:
        label_res.set_text(str("Delete failed!"))
        Speaker.tone(999, 200)
    operation = 0

def btn_enroll_clicked_event(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    operation = 1
    Speaker.tone(888, 100)

def btn_recognize_clicked_event(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    operation = 2
    Speaker.tone(888, 100)

def btn_delete_clicked_event(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    Speaker.tone(888, 100)
    operation = 3

def btn_upload_clicked_event(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    operation = 4
    Speaker.tone(888, 100)

def btn_download_clicked_event(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    operation = 5
    Speaker.tone(888, 100)

def btn_enroll_event_handler(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_enroll_clicked_event(event_struct)
    return

def btn_recognize_event_handler(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_recognize_clicked_event(event_struct)
    return

def btn_delete_event_handler(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_delete_clicked_event(event_struct)
    return

def btn_upload_event_handler(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_upload_clicked_event(event_struct)
    return

def btn_download_event_handler(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_download_clicked_event(event_struct)
    return

def setup():
    global \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    btn_enroll = m5ui.M5Button(
        text="enroll",
        x=14,
        y=165,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    btn_upload = m5ui.M5Button(
        text="upload",
        x=45,
        y=106,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    btn_recognize = m5ui.M5Button(
        text="recognize",
        x=109,
        y=165,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    btn_download = m5ui.M5Button(
        text="download",
        x=186,
        y=108,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    btn_delete = m5ui.M5Button(
        text="delete",
        x=229,
        y=165,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "Fingerprint enroll, recognize, delete",
        x=14,
        y=9,
        text_c=0x0F6DD1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_tip = m5ui.M5Label(
        "Tip:",
        x=38,
        y=35,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_res = m5ui.M5Label(
        "Result:",
        x=12,
        y=56,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    btn_enroll.add_event_cb(btn_enroll_event_handler, lv.EVENT.ALL, None)
    btn_recognize.add_event_cb(btn_recognize_event_handler, lv.EVENT.ALL, None)
    btn_delete.add_event_cb(btn_delete_event_handler, lv.EVENT.ALL, None)
    btn_upload.add_event_cb(btn_upload_event_handler, lv.EVENT.ALL, None)
    btn_download.add_event_cb(btn_download_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)
    fingerprint2_0 = Fingerprint2Unit(2, port=(1, 2))
    while not (fingerprint2_0.is_connected()):
        time.sleep_ms(500)
        print(".")
    fingerprint2_0.activate_module()
    fingerprint2_0.set_work_mode(1, save=False)
    print(fingerprint2_0.get_firmware_version())
    btn_upload.set_size(80, 60)
    btn_upload.align_to(page0, lv.ALIGN.CENTER, -60, 0)
    btn_download.set_size(80, 60)
    btn_download.align_to(page0, lv.ALIGN.CENTER, 60, 0)
    btn_enroll.set_size(80, 60)
    btn_enroll.align_to(page0, lv.ALIGN.CENTER, -105, 70)
    btn_recognize.set_size(100, 60)
    btn_recognize.align_to(page0, lv.ALIGN.CENTER, 0, 70)
    btn_delete.set_size(80, 60)
    btn_delete.align_to(page0, lv.ALIGN.CENTER, 105, 70)
    operation = 0
    g_id = 0

def loop():
    global \
        page0, \
        btn_enroll, \
        btn_upload, \
        btn_recognize, \
        btn_download, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    M5.update()
    if operation == 1:
        enroll(1, 5)
    elif operation == 2:
        recognize()
    elif operation == 3:
        delete(1)
    elif operation == 4:
        upload()
    elif operation == 5:
        download()
    else:
        pass

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

#### Upload adn display fingerprint image

This example demonstrates how to upload and display the fingerprint image.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import Fingerprint2Unit
import time

page0 = None
canvas0 = None
btn_upload = None
label0 = None
fingerprint2_0 = None
upload = None
fpimg = None

# Describe this function...
def upload_image():
    global upload, fpimg, page0, canvas0, btn_upload, label0, fingerprint2_0
    Speaker.tone(666, 100)
    label0.set_text(str("Please press finger"))
    while not (fingerprint2_0.get_enroll_image()):
        print(".")
        time.sleep_ms(1000)
    label0.set_text(str("Uploading..."))
    fpimg = fingerprint2_0.upload_image(to_rgb565=True, byte_order=True)
    if fpimg:
        Speaker.tone(666, 100)
        label0.set_text(str("Upload image finished!"))
        canvas0.set_buffer(fpimg, 80, 208, lv.COLOR_FORMAT.RGB565)
        upload = False
    else:
        Speaker.tone(888, 200)
        label0.set_text(str("Upload image failed!"))
    upload = False

def btn_upload_clicked_event(event_struct):
    global page0, canvas0, btn_upload, label0, fingerprint2_0, upload, fpimg
    upload = True

def btn_upload_event_handler(event_struct):
    global page0, canvas0, btn_upload, label0, fingerprint2_0, upload, fpimg
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_upload_clicked_event(event_struct)
    return

def setup():
    global page0, canvas0, btn_upload, label0, fingerprint2_0, upload, fpimg
    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    canvas0 = m5ui.M5Canvas(
        x=115,
        y=25,
        w=80,
        h=208,
        color_format=lv.COLOR_FORMAT.ARGB8888,
        bg_c=0xC9C9C9,
        bg_opa=255,
        parent=page0,
    )
    btn_upload = m5ui.M5Button(
        text="upload",
        x=216,
        y=144,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "tip",
        x=6,
        y=3,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    btn_upload.add_event_cb(btn_upload_event_handler, lv.EVENT.ALL, None)
    fingerprint2_0 = Fingerprint2Unit(2, port=(1, 2))
    page0.screen_load()
    Speaker.begin()
    Speaker.setVolumePercentage(0.8)
    btn_upload.set_size(80, 60)
    upload = True
    upload_image()

def loop():
    global page0, canvas0, btn_upload, label0, fingerprint2_0, upload, fpimg
    M5.update()
    if upload:
        upload_image()

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

#### Fingerprint2Unit

## `Fingerprint2Unit`
### `send_cmd`

### `get_verify_image`
Capture fingerprint image for verification.

- Returns: True if the fingerprint image was successfully captured, False otherwise.
- Return type: bool

```python
unit_fp2_0.get_verify_image()
```

### `get_enroll_image`
Capture fingerprint image for enrollment.

- Returns: True if the fingerprint image was successfully captured, False otherwise.
- Return type: bool

```python
unit_fp2_0.get_enroll_image()
```

### `gen_feature`
Generate fingerprint feature.

Converts the original fingerprint image stored in the image buffer into a feature file,
which is then stored in the template buffer.

- Returns: True if the fingerprint feature was successfully generate, False otherwise.
- Return type: bool

```python
unit_fp2_0.gen_feature()
```

### `gen_template`
Merge fingerprint features to generate a template.

Combines two fingerprint feature files into one fingerprint template.

- Returns: True if the fingerprint template was successfully generate, False otherwise.
- Return type: bool

```python
unit_fp2_0.gen_template()
```

### `store_template`
Store fingerprint template into flash memory.

Stores the generated fingerprint template into flash memory at the specified ID.

- Parameter `id` (`int`): Storage location ID (range: 0 ~ 99)
- Returns: True if storage successful False otherwise.
- Return type: bool

```python
unit_fp2_0.store_template(id)
```

### `load_template`
Load fingerprint template from flash memory.

Loads the fingerprint template with the specified ID from flash memory
into the template buffer.

- Parameter `id` (`int`): ID of the fingerprint template to load

- Returns: True if load template succcessful.
- Return type: bool

```python
unit_fp2_0.load_template(id)
```

### `delete_template`
Delete fingerprint template from flash memory.

Deletes the fingerprint template with the specified ID from the flash storage.

- Parameter `id` (`int`): ID of the fingerprint template to delete
- Returns: True if deletion successful, False otherwise
- Return type: bool

```python
unit_fp2_0.delete_template(id)
```

### `delete_all_template`
Clear the fingerprint database.

Deletes all fingerprint templates stored in the fingerprint database.

- Returns: True if deletion successful, False otherwise
- Return type: bool

```python
unit_fp2_0.delete_all_template()
```

### `upload_template`
Upload fingerprint template and save to specified path

Uploads the template stored in the template buffer to the host controller.

- Parameter `path` (`str`): File path to save the uploaded template
- Returns: True if upload template successful.
- Return type: bool

```python
unit_fp2_0.upload_template(path)
```

### `download_template`
Download template.

Reads the fingerprint template from the file system and downloads it to the fingerprint module.

- Parameter `path` (`str`): Path to the fingerprint template file
- Returns: True if download template successful.
- Return type: bool

```python
unit_fp2_0.download_template(path)
```

### `upload_image`
Upload fingerprint image from module.

Uploads the 4-bit grayscale fingerprint image from the module (size: 80x208).
Optionally, converts the raw image to RGB565 format suitable for display.

- Parameter `to_rgb565` (`bool`): Whether to convert raw image to RGB565 (default True)
- Parameter `byte_order` (`bool`): If converting to RGB565, set True for little-endian byte order, or False for big-endian. Default is True.
- Returns: Fingerprint image data as bytearray. Returns None on failure.
- Return type: bytearray | None

```python
img_buf = unit_fp2_0.upload_image(to_rgb565=True, byte_order=True)
```

### `get_valid_template_num`
Get the number of valid fingerprint templates.

Returns the count of fingerprint templates currently stored in the fingerprint database.

- Returns: Number of valid fingerprint templates
- Return type: int

```python
unit_fp2_0.get_valid_template_num()
```

### `get_stored_template_id`
Get the list of stored fingerprint template IDs from the fingerprint sensor.

This function queries the fingerprint sensor for its template index map,
which represents the occupied (used) template slots in the database,
and returns the list of those occupied IDs.

- Returns: A list of occupied fingerprint template IDs, or None if retrieval fails.
- Return type: list[int] | None

```python
stored_ids = get_stored_template_id(sensor)
```

### `find_match`
Search for a matching fingerprint in the database.

Compares the fingerprint features stored in the template buffer
with the stored templates in the database.

- Returns:
    - (id, score): A tuple of the matched fingerprint ID and match score.
    - None: If no matching fingerprint is found.

```python
unit_fp2_0.find_match()
```

### `match`
Precisely match two fingerprint features.

Compares two fingerprint feature files and returns the result and score.

- Returns: Similarity score of the match
- Return type: int

```python
unit_fp2_0.match()
```

### `is_connected`
Check whether the fingerprint module is connected.

- Returns: True if the module is connected, False otherwise.
- Return type: bool

```python
unit_fp2_0.is_connected()
```

### `activate_module`
Activate the module.

```python
unit_fp2_0.activate_module()
```

### `set_work_mode`
Set the working mode.

- Parameter `mode` (`int`): Working mode (0: Auto sleep, 1: Always-on).
- Parameter `save` (`bool`): Whether to save the setting to the device. Default is False.

```python
unit_fp2_0.set_work_mode(mode, save)
```

### `get_work_mode`
Get the current working mode.

Returns the module's current working mode:
    - 0: Auto sleep mode
    - 1: Always-on mode

- Returns: Current working mode
- Return type: int

```python
mode = unit_fp2_0.get_work_mode()
```

### `set_auto_sleep_time`
Set the sleep timeout.

This parameter is only effective in "Auto Sleep Mode".
It determines how long the fingerprint module waits without receiving any command
before it enters sleep mode and starts monitoring for fingerprint press.

- Parameter `time_s` (`int`): Auto sleep timeout in seconds. Range: 10~254.
- Parameter `save` (`bool`): Whether to save this configuration to flash.

```python
unit_fp2_0.set_auto_sleep_time(30, save=True)
```

### `get_auto_sleep_time`
Get auto sleep time.

This value is only valid in "Timed Sleep Mode". It indicates how long the module will wait
without receiving commands before entering sleep state.

- Returns: Auto sleep time in seconds
- Return type: int

```python
sleep_time = unit_fp2_0.get_auto_sleep_time()
```

### `get_work_status`
Get fingerprint module work status.

- Returns: True if active, False otherwise
- Return type: bool

```python
status = unit_fp2_0.get_work_status()
```

### `get_firmware_version`
Get firmware version.

- Returns: Firmware version number
- Return type: int

```python
version = unit_fp2_0.get_firmware_version()
```

### `set_led_breath`
Set LED breathing mode.

- Parameter `start_color` (`int`): Start color (bit0: blue, bit1: green, bit2: red)
- Parameter `end_color` (`int`): End color (bit0: blue, bit1: green, bit2: red)
- Parameter `repeat` (`int`): Number of cycles (0=infinite)
- Returns: True if command successful, False otherwise
- Return type: bool

Color codes:
    - 0x00: All off
    - 0x01: Blue
    - 0x02: Green
    - 0x03: Cyan (blue + green)
    - 0x04: Red
    - 0x05: Magenta (red + blue)
    - 0x06: Yellow (red + green)
    - 0x07: White (red + green + blue)

```python
# Blue breathing light, 5 cycles
unit_fp2_0.set_led_breath(0x01, 0x01, 5)

# Red to white breathing light, infinite cycles
unit_fp2_0.set_led_breath(0x04, 0x07, 0)
```

### `set_led_color`
Set LED color.

- Parameter `color` (`int`): LED color (0: always off, other values: always on with specified color)
- Returns: True if command successful, False otherwise
- Return type: bool

Color codes:
    - 0x00: Always off
    - 0x01: Blue
    - 0x02: Green
    - 0x03: Cyan (blue + green)
    - 0x04: Red
    - 0x05: Magenta (red + blue)
    - 0x06: Yellow (red + green)
    - 0x07: White (red + green + blue)

```python
# Always on white light
unit_fp2_0.set_led_color(0x07)

# Always off (turn off all LEDs)
unit_fp2_0.set_led_color(0x00)

# Always on red light
unit_fp2_0.set_led_color(0x04)
```
