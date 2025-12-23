# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .launcher import *
from machine import Pin, I2C, UART, reset, unique_id, SoftI2C, ADC
import network
import esp32
import time
import sys
import os
import M5

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


class HALTab5(HALBase):
    def __init__(self, wifi):
        super().__init__()

        self._wifi = wifi

        # Default values
        self.set_volume(self._volume)
        self.set_backlight(self._backlight)
        self.set_charge_mode(self._charge_mode)

        self._load_network_config_from_nvs()

        self._pin_485_de = None
        self._pin_obj_map = {}
        self._adc_obj_map = {}

    def _load_network_config_from_nvs(self) -> NetworkConfig:
        nvs = esp32.NVS("uiflow")
        self._network_config = NetworkConfig(
            nvs.get_str("ssid0"), nvs.get_str("pswd0"), nvs.get_str("server")
        )

    def _save_network_config_to_nvs(self):
        nvs = esp32.NVS("uiflow")
        nvs.set_str("ssid0", self._network_config.ssid)
        nvs.set_str("pswd0", self._network_config.password)
        nvs.set_str("server", self._network_config.server)
        nvs.commit()

    def get_asset_path(self, asset_path: str) -> str:
        return "S:/system/tab5/" + asset_path

    def create_temp_dir(self):
        try:
            os.stat("tmp")
        except OSError:
            os.mkdir("tmp")

    def get_lvgl_temp_file_path(self, file_name: str) -> str:
        return "S:/flash/tmp/" + file_name

    def get_os_temp_file_path(self, file_name: str) -> str:
        return "tmp/" + file_name

    def play_click_sfx(self):
        M5.Speaker.playWavFile("/system/common/wav/click.wav")

    def power_off(self):
        M5.Power.powerOff()

    def sleep(self):
        M5.Power.deepSleep()

    def set_volume(self, volume: int):
        self._volume = volume
        # 0~100 to 0~255
        M5.Speaker.setVolume(int(volume * 255 / 100))

    def set_backlight(self, backlight: int):
        self._backlight = backlight
        # 0~100 to 0~255
        M5.Lcd.setBrightness(int(backlight * 255 / 100))

    def set_charge_mode(self, mode: ChargeMode):
        self._charge_mode = mode

        if mode == ChargeMode.DISABLE:
            M5.Power.setBatteryCharge(False)
            return

        M5.Power.setBatteryCharge(True)
        if mode == ChargeMode.NORMAL:
            M5.Power.setChargeCurrent(500)
        elif mode == ChargeMode.QC:
            M5.Power.setChargeCurrent(1000)

    def get_battery_level(self) -> int:
        return M5.Power.getBatteryLevel()

    def get_output_current(self) -> float:
        return M5.Power.getBatteryCurrent() / 1000.0

    def is_charging(self) -> bool:
        return M5.Power.isCharging()

    def get_network_status(self) -> NetworkStatus:
        status = self._wifi.connect_status()
        if status is network.STAT_GOT_IP:
            rssi = self._wifi.get_rssi()
            if rssi <= -80:
                return NetworkStatus.RSSI_WORSE
            elif rssi <= -60:
                return NetworkStatus.RSSI_MID
            else:
                return NetworkStatus.RSSI_GOOD
        else:
            return NetworkStatus.DISCONNECTED

    def get_cloud_status(self) -> CloudStatus:
        if _HAS_SERVER is True:
            status = M5Things.status()
            return {
                -2: CloudStatus.DISCONNECTED,
                -1: CloudStatus.DISCONNECTED,
                0: CloudStatus.INIT,
                1: CloudStatus.INIT,
                2: CloudStatus.CONNECTED,
                3: CloudStatus.DISCONNECTED,
            }[status]
        else:
            return CloudStatus.DISCONNECTED

    def get_network_config(self) -> NetworkConfig:
        self._load_network_config_from_nvs()
        return NetworkConfig(
            ssid=self._network_config.ssid,
            password=self._network_config.password,
            server=self._network_config.server,
        )

    def set_network_config(self, config: NetworkConfig):
        is_changed = False
        if self._network_config.ssid != config.ssid:
            self._network_config.ssid = config.ssid
            is_changed = True
        if self._network_config.password != config.password:
            self._network_config.password = config.password
            is_changed = True
        if self._network_config.server != config.server:
            self._network_config.server = config.server
            is_changed = True

        if is_changed:
            self._save_network_config_to_nvs()

            # Reconnect
            self._wifi.network.disconnect()
            self._wifi.network.active(False)
            self._wifi.network.active(True)
            self._wifi.connect_network(self._network_config.ssid, self._network_config.password)

    def get_py_app_list(self) -> list[str]:
        py_apps = []
        for file in os.listdir("apps"):
            if file.endswith(".py"):
                py_apps.append(file)
        return py_apps

    def run_py_app(self, app_name: str, once: bool):
        if not app_name:
            print("invalid py app name")

        if once:
            execfile("/".join(["apps", app_name]), {"__name__": "__main__"})  # noqa: F821
            raise KeyboardInterrupt
        else:
            nvs = esp32.NVS("uiflow")
            nvs.set_u8("boot_option", 2)
            nvs.commit()
            with open("apps/" + app_name, "rb") as f_src, open("main.py", "wb") as f_dst:
                while True:
                    chunk = f_src.read(1024)
                    if not chunk:
                        break
                    f_dst.write(chunk)
            time.sleep(1)
            reset()

    async def scan_wifi(self):
        return self._wifi.network.scan()

    def i2c_init(self):
        # self._i2c_0 = I2C(0, scl=Pin(32), sda=Pin(31),
        #                   freq=400000, timeout=100)
        # self._i2c_1 = I2C(1, scl=Pin(54), sda=Pin(53),
        #                   freq=400000, timeout=100)
        self._i2c_0 = SoftI2C(scl=Pin(32), sda=Pin(31), freq=400000, timeout=100)
        self._i2c_1 = SoftI2C(scl=Pin(54), sda=Pin(53), freq=400000, timeout=100)

    def i2c_deinit(self):
        self._i2c_0 = None
        self._i2c_1 = None

    def i2c_scan(self, port: int) -> list[int]:
        if port == 0:
            return self._i2c_0.scan()
        return self._i2c_1.scan()

    def get_mac(self) -> bytes:
        return unique_id()

    def uart_init(self, baudrate: int, tx_pin: int, rx_pin: int):
        self._uart = UART(1, baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin))

        # RS485
        if tx_pin == 20:
            self._pin_485_de = Pin(34, Pin.OUT)
            self._pin_485_de.off()

    def uart_deinit(self):
        self._uart = None
        self._pin_485_de = None

    def uart_write(self, msg: str):
        if self._pin_485_de:
            self._pin_485_de.on()

        self._uart.write(msg + "\n")

        if self._pin_485_de:
            time.sleep_ms(1)
            self._pin_485_de.off()

    def uart_read(self) -> bytes | None:
        return self._uart.read()

    def store_ezdata_user_token(self, user_token: str):
        nvs = esp32.NVS("uiflow")
        nvs.set_str("ustoken", user_token)

    def get_ezdata_user_token(self) -> str:
        nvs = esp32.NVS("uiflow")
        try:
            token = nvs.get_str("ustoken")
            return token
        except:
            return ""

    def reset_ezdata_user_token(self):
        nvs = esp32.NVS("uiflow")
        nvs.set_str("ustoken", "")

    def gpio_init(self, pin: int, mode: int):
        """
        mode:
            0: input
            1: output
        """
        self._pin_obj_map[pin] = Pin(pin, Pin.OUT if mode == 1 else Pin.IN)

    def gpio_set_level(self, pin: int, level: bool):
        """
        level:
            False: low
            True: high
        """
        if pin not in self._pin_obj_map:
            return
        self._pin_obj_map[pin].value(level)

    def gpio_deinit(self, pin: int):
        if pin not in self._pin_obj_map:
            return
        del self._pin_obj_map[pin]

    def adc_init(self, pin: int):
        self._adc_obj_map[pin] = ADC(Pin(pin))

    def adc_deinit(self, pin: int):
        if pin not in self._adc_obj_map:
            return
        del self._adc_obj_map[pin]

    def adc_read(self, pin: int) -> int:
        if pin not in self._adc_obj_map:
            return 0
        return self._adc_obj_map[pin].read()
