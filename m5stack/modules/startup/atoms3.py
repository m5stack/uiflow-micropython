# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
# AtomS3 startup script
import M5
import time
import network
import machine
import binascii
from . import Startup

# AtomS3 startup menu


class AtomS3_Startup(Startup):
    WIFI_OK = "/system/atoms3/wifi_ok.png"
    WIFI_ERR = "/system/atoms3/wifi_err.png"
    MODE_DEV = "/system/atoms3/mode_dev.png"

    def __init__(self) -> None:
        super().__init__()

    def show_hits(self, hits: str) -> None:
        M5.Lcd.fillRect(24, 70, 95, 11, M5.Lcd.COLOR.BLACK)
        M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu9)
        M5.Lcd.drawCenterString(hits, 73, 70)

    def show_msg(self, msg: str) -> None:
        M5.Lcd.fillRect(36, 49, 82, 17, M5.Lcd.COLOR.BLACK)
        M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu12)
        M5.Lcd.drawCenterString(msg, 71, 51)

    def show_ssid(self, ssid: str) -> None:
        if len(ssid) > 9:
            self.show_msg(ssid[:7] + "...")
        else:
            self.show_msg(ssid)

    def show_mac(self) -> None:
        mac = binascii.hexlify(machine.unique_id()).decode("utf-8").upper()
        M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu9)
        M5.Lcd.drawCenterString(mac[0:6] + "_" + mac[6:], 65, 85)

    def show_error(self, ssid: str, error: str) -> None:
        M5.Lcd.clear()
        M5.Lcd.drawImage(self.WIFI_ERR, 0, 0)
        M5.Lcd.drawImage(self.MODE_DEV, 0, 98)
        self.show_ssid(ssid)
        self.show_hits(error)
        self.show_mac()
        print("SSID: " + ssid + "\r\nNotice: " + error)

    def startup(
        self,
        ssid: str,
        pswd: str,
        protocol: str = "",
        ip: str = "",
        netmask: str = "",
        gateway: str = "",
        dns: str = "",
        timeout: int = 60,
    ) -> None:
        M5.Lcd.drawImage(self.WIFI_OK, 0, 0)
        M5.Lcd.drawImage(self.MODE_DEV, 0, 98)
        self.show_mac()

        if super().connect_network(
            ssid=ssid,
            pswd=pswd,
            protocol=protocol,
            ip=ip,
            netmask=netmask,
            gateway=gateway,
            dns=dns,
        ):
            self.show_ssid(ssid)
            count = 1
            status = super().connect_status()
            start = time.time()
            while status is not network.STAT_GOT_IP:
                time.sleep_ms(300)
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
                    self.show_hits("." * count)
                    count = count + 1
                    if count > 5:
                        count = 1
                status = super().connect_status()
                # connect to network timeout
                if (time.time() - start) > timeout:
                    self.show_error(ssid, "TIMEOUT")
                    break

            if status is network.STAT_GOT_IP:
                self.show_hits(super().local_ip())
                print("Local IP: " + super().local_ip())
        else:
            self.show_error("Not Found", "Use Burner setup")
            M5.Lcd.drawImage(self.MODE_DEV, 0, 98)
