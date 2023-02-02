# -*- encoding: utf-8 -*-
# boot.py
import M5
import esp32

# Execute startup script, if not needed, delete the code below
if __name__ == '__main__':
    M5.begin()
    from startup import startup
    nvs = esp32.NVS("uiflow")
    startup(nvs.get_u8("boot_option"))
