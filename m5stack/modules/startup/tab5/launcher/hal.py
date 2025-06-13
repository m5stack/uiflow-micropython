# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


class ChargeMode:
    NORMAL = 0
    QC = 1
    DISABLE = 2


class NetworkStatus:
    INIT = 0
    RSSI_GOOD = 1
    RSSI_MID = 2
    RSSI_WORSE = 3
    DISCONNECTED = 4


class CloudStatus:
    INIT = 0
    CONNECTED = 1
    DISCONNECTED = 2


class NetworkConfig:
    def __init__(self, ssid: str, password: str, server: str):
        self.ssid = ssid
        self.password = password
        self.server = server


class HALBase:
    def __init__(self):
        self._volume = 100
        self._backlight = 100
        self._charge_mode = ChargeMode.NORMAL

    def power_off(self):
        ...

    def sleep(self):
        ...

    def get_battery_level(self) -> int:
        return 66

    def get_output_current(self) -> float:
        return 0.23

    def is_charging(self) -> bool:
        return False

    def set_charge_mode(self, mode: ChargeMode):
        self._charge_mode = mode

    def get_charge_mode(self) -> ChargeMode:
        return self._charge_mode

    def get_asset_path(self, asset_path: str) -> str:
        raise NotImplementedError()

    def get_volume(self) -> int:
        return self._volume

    def set_volume(self, volume: int):
        self._volume = volume

    def play_click_sfx(self):
        ...

    def get_backlight(self) -> int:
        return self._backlight

    def set_backlight(self, backlight: int):
        self._backlight = backlight

    def get_network_status(self) -> NetworkStatus:
        return NetworkStatus.RSSI_GOOD

    def get_cloud_status(self) -> CloudStatus:
        return CloudStatus.CONNECTED

    def get_network_config(self) -> NetworkConfig:
        ...

    def set_network_config(self, config: NetworkConfig):
        ...

    def get_py_app_list(self) -> list[str]:
        ...

    def run_py_app(self, app_name: str, once: bool):
        ...

    async def scan_wifi(self):
        ...

    def i2c_init(self):
        ...

    def i2c_deinit(self):
        ...

    def i2c_scan(self, port: int) -> list[int]:
        ...

    def uart_init(self, baudrate: int, tx_pin: int, rx_pin: int):
        ...

    def uart_deinit(self):
        ...

    def uart_write(self, msg: str):
        ...

    def uart_read(self) -> bytes | None:
        ...

    def get_mac(self) -> bytes:
        ...

    def store_ezdata_user_token(self, user_token: str):
        ...

    def get_ezdata_user_token(self) -> str:
        ...

    def reset_ezdata_user_token(self):
        ...


_instance: HALBase = None


def set_hal(hal: HALBase):
    global _instance
    _instance = hal


def get_hal():
    global _instance
    return _instance
