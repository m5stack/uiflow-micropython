# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
# boot.py
import esp32

"""
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
"""

NETWORK_TIMEOUT = 60
_uiflow_run_main = True

# Execute startup script, if not needed, delete the code below
if __name__ == "__main__":
    from startup import BOOT_OPT_MENU_NET, startup

    nvs = esp32.NVS("uiflow")
    try:
        boot_option = nvs.get_u8("boot_option")
    except:
        boot_option = 1  # default

    boot_option = startup(boot_option, NETWORK_TIMEOUT)
    _uiflow_run_main = boot_option != BOOT_OPT_MENU_NET
