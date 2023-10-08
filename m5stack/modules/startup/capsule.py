from .stamps3 import StampS3_Startup
import network
import time
import M5


class Capsule_Startup(StampS3_Startup):
    """AtomS3U startup menu"""

    def __init__(self) -> None:
        super().__init__()

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self.show_mac()
        M5.Speaker.setVolumePercentage(1.0)

        if super().connect_network(ssid=ssid, pswd=pswd):
            print("Connecting to " + ssid + " ", end="")
            status = super().connect_status()
            self.rgb.set_brightness(60)
            start = time.time()
            while True:
                t = super().connect_status()
                if t != network.STAT_GOT_IP:
                    status = t
                    M5.Speaker.tone(5000, 50)
                    if t is network.STAT_NO_AP_FOUND:
                        self.show_error(ssid, "NO AP FOUND")
                        break
                    elif t is network.STAT_WRONG_PASSWORD:
                        self.show_error(ssid, "WRONG PASSWORD")
                        break
                    elif t is network.STAT_HANDSHAKE_TIMEOUT:
                        self.show_error(ssid, "HANDSHAKE ERR")
                        break
                    elif t is network.STAT_CONNECTING:
                        print(".", end="")
                if t != status and t == network.STAT_GOT_IP:
                    status = t
                    print(" ")
                    print("Local IP: " + super().local_ip())
                    self.rgb.set_color(0, self.COLOR_GREEN)
                    self.rgb.set_brightness(100)
                    break
                # connect to network timeout
                if (time.time() - start) > timeout:
                    self.show_error(ssid, "TIMEOUT")
                    break
                time.sleep_ms(300)
            if status == network.STAT_GOT_IP:
                M5.Speaker.tone(4500, 50)
                time.sleep(0.1)
                M5.Speaker.tone(4500, 50)
        else:
            self.rgb.set_color(0, self.COLOR_RED)
            self.rgb.set_brightness(100)
            self.show_error("Not Found", "Please use M5Burner setup :)")
