# -*- encoding: utf-8 -*-
# boot.py
import M5
import esp32
import time

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
    boot, you can delete this whole file. If you want show startup menu again,
    you can hold BtnA(most device) and click reset button or repower device
    until show the startup menu(for those devices with screens, and this is a
    temporary method and may change in the future), after that the boot_option
    will change to 1, so next time still will show the startup menu.

    BTW, the network connection time has a default timeout (60s), you can modify
    the following definition to change this default value.
"""

NETWORK_TIMEOUT = 60

# Execute startup script, if not needed, delete the code below
if __name__ == "__main__":
    M5.begin()
    from startup import startup

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
    startup(boot_option, NETWORK_TIMEOUT)
