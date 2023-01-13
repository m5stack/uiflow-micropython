# -*- encoding: utf-8 -*-
# boot.py
import time
import binascii
import esp32
import network
import machine
import M5


def show_hits(hits):
    M5.Lcd.fillRect(24, 70, 95, 11, M5.Lcd.COLOR.BLACK)
    M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu9)
    M5.Lcd.drawCenterString(hits, 73, 70)


def show_msg(msg):
    M5.Lcd.fillRect(36, 49, 82, 17, M5.Lcd.COLOR.BLACK)
    M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu12)
    M5.Lcd.drawCenterString(msg, 71, 51)


def show_ssid(ssid):
    if len(ssid) > 9:
        show_msg(ssid[:7] + "...")
    else:
        show_msg(ssid)


def show_mac():
    mac = binascii.hexlify(machine.unique_id()).decode('utf-8').upper()
    M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu9)
    M5.Lcd.drawCenterString(mac[0:6] + '_' + mac[6:], 65, 85)


def show_error(ssid, error):
    M5.Lcd.clear()
    M5.Lcd.drawImage("res/img/sys/wifi_err.png", 0, 0)
    M5.Lcd.drawImage("res/img/sys/mode_dev.png", 0, 98)
    show_ssid(ssid)
    show_hits(error)
    show_mac()


M5.begin()
M5.Lcd.drawImage("res/img/sys/wifi_ok.png", 0, 0)
M5.Lcd.drawImage("res/img/sys/mode_dev.png", 0, 98)
show_mac()

# Read saved Wi-Fi information from NVS
nvs = esp32.NVS("uiflow")
ssid = nvs.get_str("ssid0")
pswd = nvs.get_str("pswd0")

if (len(ssid) > 0) and (len(pswd) > 0):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    wlan.connect(ssid, pswd)

    # show Wi-Fi information
    show_ssid(ssid)

    # check Wi-Fi connection
    count = 1
    while wlan.status() is not network.STAT_GOT_IP:
        time.sleep_ms(300)
        if wlan.status() is network.STAT_NO_AP_FOUND:
            show_error(ssid, "NO AP FOUND")
            break
        elif wlan.status() is network.STAT_WRONG_PASSWORD:
            show_error(ssid, "WRONG PASSWORD")
            break
        elif wlan.status() is network.STAT_BEACON_TIMEOUT:
            show_error(ssid, "BEACON TIMEOUT")
            break
        elif wlan.status() is network.STAT_ASSOC_FAIL:
            show_error(ssid, "ASSOC FAIL")
            break
        elif wlan.status() is network.STAT_HANDSHAKE_TIMEOUT:
            show_error(ssid, "HANDSHAKE ERR")
            break
        elif wlan.status() is network.STAT_CONNECTING:
            show_hits('.' * count)
            count = count + 1
            if count > 5:
                count = 1

    if wlan.status() is network.STAT_GOT_IP:
        show_hits(str(wlan.ifconfig()[0]))
else:
    show_error("Not Found", "Use Burner setup")
    M5.Lcd.drawImage("res/img/sys/mode_dev.png", 0, 98)
