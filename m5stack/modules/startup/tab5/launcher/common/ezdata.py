# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MI

from ..hal import *
import asyncio
import requests
import json
from umqtt import MQTTClient


class Ezdata:
    class State:
        INIT = 0
        WAIT_USER_TOKEN = 1
        NORMAL = 2

    _state: State = State.INIT
    _device_token: str | None = None
    _user_token: str | None = None
    _mqtt_client: MQTTClient | None = None
    _task = None

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
    async def _ezdata_task():
        try:
            Ezdata._set_state(Ezdata.State.INIT)
            await Ezdata._wait_network_connected()
            await Ezdata._get_device_token()
            await Ezdata._connect_mqtt()
            Ezdata._get_user_token_from_storage()

            # Keep mqtt update
            while True:
                Ezdata._mqtt_client.check_msg()
                await asyncio.sleep(0.2)

        except Exception as e:
            print("ezdata task failed:", e)
            await asyncio.sleep(2)
            asyncio.create_task(Ezdata._ezdata_task())

    @staticmethod
    async def _wait_network_connected():
        while get_hal().get_network_status() in {NetworkStatus.DISCONNECTED, NetworkStatus.INIT}:
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
    async def _connect_mqtt():
        client_id = "".join(f"{byte:02x}" for byte in get_hal().get_mac())
        client_id = f"m5{client_id}m5"

        Ezdata._mqtt_client = MQTTClient(
            client_id,
            "uiflow2.m5stack.com",
            port=1883,
            user=Ezdata._device_token,
            password="",
            keepalive=60,
        )

        # Try connect and subscribe
        while True:
            try:
                Ezdata._mqtt_client.connect(clean_session=True)
                Ezdata._mqtt_client.subscribe(
                    f"$ezdata/{Ezdata._device_token}/down", Ezdata._on_ezdata_down_message
                )
                break
            except Exception as e:
                print("connect mqtt failed:", e)

            await asyncio.sleep(2)

    @staticmethod
    def _on_ezdata_down_message(data: tuple[bytes, bytes]):
        try:
            topic = data[0].decode("utf-8")
            payload = data[1].decode("utf-8")
            print("mqtt >>", topic, ":", payload)

            msg = json.loads(payload)
            if msg.get("userToken"):
                Ezdata._user_token = msg.get("userToken")
                if Ezdata._check_token_valid(Ezdata._user_token):
                    get_hal().store_ezdata_user_token(Ezdata._user_token)
                    Ezdata._set_state(Ezdata.State.NORMAL)
                else:
                    Ezdata._user_token = None
                    raise Exception("invalid user token")

        except Exception as e:
            print("on ezdata down message failed:", e)

    @staticmethod
    def _get_user_token_from_storage():
        Ezdata._user_token = get_hal().get_ezdata_user_token()
        if Ezdata._check_token_valid(Ezdata._user_token):
            Ezdata._set_state(Ezdata.State.NORMAL)
        else:
            Ezdata._user_token = ""
            Ezdata._set_state(Ezdata.State.WAIT_USER_TOKEN)

    @staticmethod
    def get_add_user_qr_code():
        data = {"deviceToken": Ezdata._device_token, "deviceType": "tab5", "type": "device"}
        return json.dumps(data)

    @staticmethod
    def _simplify_user_group_list_response_json(data: dict):
        return [{k: item.get(k) for k in ["id", "domainName"]} for item in data.get("data", [])]

    @staticmethod
    def get_user_group_list():
        result = []

        try:
            if not Ezdata._check_token_valid(Ezdata._user_token):
                raise Exception("user token not valid")

            url = f"https://ezdata2.m5stack.com/api/v2/device/userGroupList/{Ezdata._user_token}"

            response = requests.get(url)
            if response.status_code == 200:
                result = Ezdata._simplify_user_group_list_response_json(response.json())

                # Filter out invalid items
                result = [item for item in result if "id" in item and "domainName" in item]

            else:
                raise Exception(
                    f"get user group list failed, status code: {response.status_code} , text: {response.text}"
                )

        except Exception as e:
            print("get user group list failed:", e)

        return result

    @staticmethod
    def _simplify_user_data_list_response_json(data: dict):
        return [
            {k: item.get(k) for k in ["alias", "value", "updateTime", "valueType"]}
            for item in data.get("data", [])
        ]

    @staticmethod
    def get_user_data_list(group_id: str):
        result = []

        try:
            if not group_id:
                raise Exception("group id not valid")

            if not Ezdata._check_token_valid(Ezdata._user_token):
                raise Exception("user token not valid")

            url = f"https://ezdata2.m5stack.com/api/v2/device/userDataList/{Ezdata._user_token}/{group_id}"

            response = requests.get(url)
            if response.status_code == 200:
                result = Ezdata._simplify_user_data_list_response_json(response.json())
            else:
                raise Exception(
                    f"get user data list failed, status code: {response.status_code} , text: {response.text}"
                )

        except Exception as e:
            print("get user data list failed:", e)

        return result

    @staticmethod
    def reset_user_token():
        get_hal().reset_ezdata_user_token()
        Ezdata._user_token = None
        Ezdata._set_state(Ezdata.State.WAIT_USER_TOKEN)


class EzdataAppState:
    _current_group_id: str = ""
    _needs_refresh: bool = True

    @staticmethod
    def set_new_group_id(group_id: str):
        EzdataAppState._current_group_id = group_id
        EzdataAppState._needs_refresh = True

    @staticmethod
    def get_current_group_id():
        return EzdataAppState._current_group_id

    @staticmethod
    def needs_refresh():
        return EzdataAppState._needs_refresh

    @staticmethod
    def clear_needs_refresh():
        EzdataAppState._needs_refresh = False
