# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import uos
from flashbdev import vfs_bdev


def check_bootsec():
    buf = bytearray(vfs_bdev.ioctl(5, 0))  # 5 is SEC_SIZE
    vfs_bdev.readblocks(0, buf)
    empty = True
    for b in buf:
        if b != 0xFF:
            empty = False
            break
    if empty:
        return True
    fs_corrupted()


def fs_corrupted():
    import time

    while 1:
        print(
            """\
FAT filesystem appears to be corrupted. If you had important data there, you
may want to make a flash snapshot to try to recover it. Otherwise, perform
factory reprogramming of MicroPython firmware (completely erase flash, followed
by firmware programming).
"""
        )
        time.sleep(3)


def setup():
    # check_bootsec()
    print("Performing initial setup")
    uos.VfsLfs2.mkfs(vfs_bdev)
    vfs = uos.VfsLfs2(vfs_bdev, progsize=32, readsize=128, lookahead=128)
    uos.mount(vfs, "/flash")
    with open("/flash/boot.py", "w") as f:
        f.write(
            """\
# -*- encoding: utf-8 -*-
# boot.py
import M5
import esp32
import time

\"\"\"
boot_option:
    0 -> Run main.py directly
    1 -> Show startup menu and network setup
    2 -> Only network setup

Quick reference:
    when use uiflow2.m5stack.com website, click RUN button to run workspace
    code, boot_option won't change, if you click DOWNLOAD button to download
    workspace code to device, boot_option will change to 2, it means after
    download code done, device will auto reboot and won't show startup menu, 
    only do the network connect, but after network connect success, you can
    still download or run workspace code. If you don't want do anything after
    boot, you can delete this whole file. Cardputer Adv, StickS3, and StackChan
    provide a one-shot startup override. During the 200ms detection window,
    hold the Cardputer Adv top-left ESC-labeled key, StickS3 BtnA, or touch the
    StackChan screen for at least 30ms. The device enters the startup menu
    without deleting main.py or changing the saved boot_option; the next boot
    runs normally.

    BTW, the network connection time has a default timeout (60s), you can modify
    the following definition to change this default value.
\"\"\"

NETWORK_TIMEOUT = 60
_uiflow_run_main = True

# Execute startup script, if not needed, delete the code below
if __name__ == "__main__":
    M5.begin()
    from startup import BOOT_OPT_MENU_NET, startup

    nvs = esp32.NVS("uiflow")
    try:
        tz = nvs.get_str("tz")
        time.timezone(tz)
    except:
        pass

    try:
        boot_option = nvs.get_u8("boot_option")
    except:
        boot_option = 1  # default
    boot_option = startup(boot_option, NETWORK_TIMEOUT)
    _uiflow_run_main = boot_option != BOOT_OPT_MENU_NET

"""
        )
    uos.mkdir("/flash/apps")
    uos.mkdir("/flash/libs")
    uos.mkdir("/flash/res")
    uos.mkdir("/flash/res/font")
    uos.mkdir("/flash/res/img")
    return vfs
