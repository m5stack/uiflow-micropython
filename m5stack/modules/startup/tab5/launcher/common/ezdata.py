# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..hal import get_hal, NetworkStatus
from .uwebsockets import connect as ws_connect
from .uwebsockets import WebsocketClient
from .debug import debug_print
from .signal import Signal
import asyncio
import requests
import json
import time


class _EzdataClientWebsocket:
    """
    Ezdata client via websocket
    """

    # Response type
    DEVICE_ADD_DATA = 100
    DEVICE_UPDATE_DATA = 101
    DEVICE_DELETE_DATA = 102
    DEVICE_DATA_LIST = 103
    DEVICE_DATA = 104
    DEVICE_DATA_FILE = 105
    DEVICE_REQUEST_ERROR = 500

    def __init__(self, device_token: str, on_data_changed: Signal):
        self._device_token = device_token
        self._on_data_changed = on_data_changed
        self._ws: WebsocketClient | None = None
        self._ws_last_heartbeat_time = 0
        self._data = {}

    async def init(self):
        await self._connect()
        await self.fetch_all_data()  # Fetch actively to create initial data

    def get_all_data(self):
        return self._data

    def get_data(self, data_id: str):
        for data in self._data:
            if data.get("id") == data_id:
                return data
        return None

    async def _connect(self):
        try:
            # Close if already connected
            if self._ws:
                self._ws.close()
                self._ws = None

            # Connect and login
            uri = "wss://ezdata2.m5stack.com/ws"
            msg = f'{{"deviceToken": "{self._device_token}"}}'

            self._ws = ws_connect(uri)

            # Wait login
            for i in range(10):
                debug_print("ws send:", msg)
                self._ws.send(msg)

                await asyncio.sleep(1)
                resp = self._ws.recv(blocking=False)
                debug_print("ws recv:", resp)

                if "Login successful" in resp:
                    self._ws_last_heartbeat_time = time.time()
                    debug_print("ws login successful")
                    return

            raise Exception("max login retry")

        except Exception as e:
            raise Exception("connect ws failed:", e)

    async def fetch_all_data(self):
        if self._ws is None:
            return

        self._data.clear()

        for i in range(10):
            try:
                msg = json.dumps(
                    {
                        "deviceToken": self._device_token,
                        "body": {"requestType": "DEVICE_DATA_LIST"},
                    }
                )
                debug_print("ws send:", msg)
                self._ws.send(msg)

                await asyncio.sleep(1)
                resp = self._ws.recv(blocking=False)

                response = json.loads(resp)
                if response.get("code") == 200:
                    self._data = response.get("body")
                    # debug_print("fetch first data success:", self._data)
                    return

            except Exception as e:
                debug_print("fetch first data failed:", e)
                await asyncio.sleep(1)
                continue

        self._data.clear()
        raise Exception("max fetch data retry")

    def update(self):
        self._receive()
        self._heartbeat()

    def _receive(self):
        if self._ws is None:
            return

        try:
            msg = self._ws.recv(blocking=False)
            if not msg:
                return

            # debug_print("ws recv:", msg)

            # Skip heartbeat
            if msg == "pong":
                return

            # Handle data update msg
            response = json.loads(msg)
            if response.get("code") == 200:
                cmd = response.get("cmd")
                if cmd in [
                    self.DEVICE_ADD_DATA,
                    self.DEVICE_UPDATE_DATA,
                    self.DEVICE_DELETE_DATA,
                    self.DEVICE_DATA_LIST,
                ]:
                    self.fetch_all_data()
                    self._on_data_changed.emit()
            else:
                print("ws recv error msg:", msg)

        except Exception as e:
            debug_print("ws recv failed:", e)

    def _heartbeat(self):
        if self._ws is None:
            return

        if time.time() - self._ws_last_heartbeat_time > 25:
            msg = f'{{"deviceToken": "{self._device_token}", "body": "ping"}}'
            debug_print("ws send:", msg)
            self._ws.send(msg)
            self._ws_last_heartbeat_time = time.time()


class Ezdata:
    class State:
        INIT = 0
        NORMAL = 1

    _state: State = State.INIT
    _device_token: str | None = None
    _client: _EzdataClientWebsocket | None = None
    _task = None

    on_data_list_changed: Signal = Signal()
    on_selected_data_changed: Signal = Signal()
    _selected_data_id: str

    @staticmethod
    def start():
        Ezdata._task = asyncio.create_task(Ezdata._ezdata_task())

    @staticmethod
    def get_state() -> State:
        return Ezdata._state

    @staticmethod
    def _set_state(state: State):
        Ezdata._state = state

    @staticmethod
    def get_all_data():
        if Ezdata._client is None:
            return {}
        return Ezdata._client.get_all_data()

    @staticmethod
    def get_data(data_id: str):
        if Ezdata._client is None:
            return None
        return Ezdata._client.get_data(data_id)

    @staticmethod
    def get_selected_data():
        return Ezdata.get_data(Ezdata._selected_data_id)

    @staticmethod
    def set_selected_data_id(data_id: str):
        Ezdata._selected_data_id = data_id
        Ezdata.on_selected_data_changed.emit()

    @staticmethod
    async def _ezdata_task():
        try:
            Ezdata._set_state(Ezdata.State.INIT)

            # Wait network and get device token
            await Ezdata._wait_network_connected()
            await Ezdata._get_device_token()

            # Create ezdata websocket client and init
            Ezdata._client = _EzdataClientWebsocket(
                Ezdata._device_token, Ezdata.on_selected_data_changed
            )
            await Ezdata._client.init()
            Ezdata._set_state(Ezdata.State.NORMAL)

            # Keep ezdata websocket client running
            while True:
                Ezdata._client.update()
                await asyncio.sleep(0.2)

        except Exception as e:
            print("ezdata task failed:", e)
            await asyncio.sleep(2)
            asyncio.create_task(Ezdata._ezdata_task())

    @staticmethod
    async def _wait_network_connected():
        while get_hal().get_network_status() in {
            NetworkStatus.DISCONNECTED,
            NetworkStatus.INIT,
        }:
            await asyncio.sleep(1)

    @staticmethod
    def _check_token_valid(token: str | None) -> bool:
        if token is None:
            return False
        if token == "":
            return False
        if len(token) != 32:
            return False
        return True

    @staticmethod
    async def _get_device_token():
        url = "https://ezdata2.m5stack.com/api/v2/device/registerMac"
        headers = {"Content-Type": "application/json"}
        data = {
            "deviceType": "tab5",
            "mac": "".join(f"{byte:02x}" for byte in get_hal().get_mac()),
        }
        json_data = json.dumps(data)

        # Fetch device token
        while True:
            try:
                response = requests.post(url, data=json_data, headers=headers)
                if response.status_code == 200:
                    # Parse and check
                    response_data = response.json()
                    Ezdata._device_token = response_data.get("data")
                    if Ezdata._check_token_valid(Ezdata._device_token):
                        # print("get device token:", Ezdata._device_token)
                        break
                    print("invalid device token:", Ezdata._device_token)
                else:
                    print(
                        f"get device token failed, status code: {response.status_code} , text: {response.text}"
                    )
            except Exception as e:
                print("get device token failed:", e)

            Ezdata._device_token = None
            await asyncio.sleep(2)

    @staticmethod
    def get_add_user_qr_code():
        data = {
            "deviceToken": Ezdata._device_token,
            "deviceType": "tab5",
            "type": "device",
        }
        return json.dumps(data)
