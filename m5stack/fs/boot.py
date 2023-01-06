# -*- encoding: utf-8 -*-
# boot.py
import time
import esp32
import network
import M5

M5.begin()
time.sleep(1)
# Read saved Wi-Fi information from NVS
nvs = esp32.NVS("uiflow")
ssid = nvs.get_str("ssid0")
pswd = nvs.get_str("pswd0")

if (len(ssid) > 0) and (len(pswd) > 0):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    wlan.connect(ssid, pswd)
    start = time.time()
    while wlan.isconnected() is False:
        time.sleep_ms(200)
        if (time.time() - start) > 10:
            break
    M5.Lcd.print("Local IP: " + str(wlan.ifconfig()[0]))
else:
    M5.Lcd.print("No Wi-Fi information found, please consider using M5Burner setting.")
