# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import network


sta_record = None


def setup():
    M5.begin()
    wlan = network.WLAN(network.STA_IF)
    wlan.config(reconnects=3)
    wlan.config(txpower=20)
    wlan.config(dhcp_hostname="m5stack")
    wlan.active(False)
    wlan.active(True)
    print("scan result:")
    for sta_record in wlan.scan():
        print((str("  ") + str(((sta_record[0]).decode()))))
        print((str("    mac: ") + str((str((sta_record[1]))))))
        print((str("    channel: ") + str((sta_record[2]))))
        print((str("    rssi: ") + str((sta_record[3]))))
        print((str("    auth: ") + str((sta_record[4]))))
    wlan.connect("M5-R&D", 'echo"password">/dev/null')
    while not (wlan.isconnected()):
        pass
    print((str("local ip: ") + str((wlan.ifconfig()[0]))))
    print((str("subnet: ") + str((wlan.ifconfig()[1]))))
    print((str("gateway: ") + str((wlan.ifconfig()[2]))))
    print((str("dns: ") + str((wlan.ifconfig()[3]))))
    print((str("rssi: ") + str((wlan.status("rssi")))))
    print((str("mac: ") + str((wlan.config("mac")))))
    print((str("dhcp: ") + str((wlan.config("dhcp_hostname")))))
    print((str("reconnects: ") + str((wlan.config("reconnects")))))
    print((str("tx power: ") + str((wlan.config("txpower")))))


def loop():
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
