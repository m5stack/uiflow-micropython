# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# StampS3 startup script
import M5
import time
import network
import machine
import binascii
from . import Startup


# StampS3 startup menu
class XIAOS3_Startup(Startup):
    COLOR_RED = 0xFF0000  # WiFi not connected
    COLOR_BLUE = 0x0000FF  # WiFi connected, server not connected
    COLOR_GREEN = 0x00FF00  # WiFi connected, server connected

    def __init__(self) -> None:
        super().__init__()
        self.led = machine.Pin(21, machine.Pin.OUT)

    def show_hits(self, hits: str) -> None:
        pass

    def show_msg(self, msg: str) -> None:
        pass

    def show_ssid(self, ssid: str) -> None:
        pass

    def show_mac(self) -> None:
        mac = binascii.hexlify(machine.unique_id()).decode("utf-8").upper()
        print("Mac: " + mac[0:6] + "_" + mac[6:])

    def show_error(self, ssid: str, error: str) -> None:
        print("SSID: " + ssid + "\r\nNotice: " + error)

    def led_blink(self, delay: int) -> None:
        self.led.value(1)
        time.sleep_ms(delay)
        self.led.value(0)
        time.sleep_ms(delay)

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self.show_mac()

        if super().connect_network(ssid=ssid, pswd=pswd):
            print("Connecting to " + ssid + " ", end="")
            status = super().connect_status()
            start = time.time()
            while status is not network.STAT_GOT_IP:
                time.sleep_ms(300)
                self.led_blink(100)
                if status is network.STAT_NO_AP_FOUND:
                    self.show_error(ssid, "NO AP FOUND")
                    break
                elif status is network.STAT_WRONG_PASSWORD:
                    self.show_error(ssid, "WRONG PASSWORD")
                    break
                elif status is network.STAT_HANDSHAKE_TIMEOUT:
                    self.show_error(ssid, "HANDSHAKE ERR")
                    break
                elif status is network.STAT_CONNECTING:
                    print(".", end="")
                status = super().connect_status()
                # connect to network timeout
                if (time.time() - start) > timeout:
                    self.show_error(ssid, "TIMEOUT")
                    break

            print(" ")
            if status is network.STAT_GOT_IP:
                print("Local IP: " + super().local_ip())
                self.led.value(1)
            else:
                self.led.value(0)
        else:
            self.led.value(0)
            self.show_error("Not Found", "Please use M5Burner setup :)")
