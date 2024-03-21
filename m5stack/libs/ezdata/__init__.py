# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

try:
    import urequests as requests
except ImportError:
    import requests
import json

_server = "https://ezdata2.m5stack.com/api/v2"

DEBUG = False

_data_types = {
    list: "array",
    dict: "dict",
    str: "string",
    int: "int",
    float: "double",
}


def _get_token():
    try:
        import M5Things

        return M5Things.info()[5]
    except ImportError:
        # import esp32

        # nvs = esp32.NVS("ezdata")
        # return nvs.get_str("device_token")
        return ""


class EzData:
    def __init__(self, token, key, public=False) -> None:
        self._device_token = token if token else _get_token()
        self._key = key
        self._value = None
        self._data_token = None
        self._date_type = None
        self._public = public
        self._data_status = False
        self._update_time = 0

    def set(self, value, is_file=False):
        if self._public:
            return
        if is_file:
            return self._set_file(value)
        else:
            return self._set(value)

    def _set(self, value):
        self._date_type = _data_types.get(type(value), "")
        if self._device_token is None:
            return

        payload = {}
        payload["dataType"] = self._date_type
        payload["name"] = self._key
        payload["permissions"] = "1"
        payload["value"] = value
        DEBUG and print("payload:", payload)
        url = "{0}/{1}/add".format(_server, self._device_token)
        try:
            rsp = requests.post(url, json=payload, headers={})
            if rsp.status_code == 200:
                rsp_data = json.loads(rsp.text)
                rsp.close()
                if rsp_data["code"] == 200:
                    self._value = value
                    return self._value
                return None
            else:
                return None
        except:
            return None
        finally:
            del url, payload

    def _set_file(self, path: str):
        self._date_type = "file"
        try:
            import os

            os.stat(path)
        except OSError:
            return
        from .multi import MultiPartForm

        form = MultiPartForm()
        form.add_field("dataType", "file")
        form.add_field("name", self._key)
        form.add_field("permissions", "1")
        form.add_field("value", path.split("/")[-1])
        form.add_field("deviceToken", self._device_token)
        form.add_file("file", path)
        headers = {}
        headers["Content-Type"] = str(form.content_type())
        url = "{0}/{1}/uploadFile".format(_server, self._device_token)
        try:
            rsp = requests.post(url, headers=headers, data=form.content())
            if rsp.status_code == 200:
                rsp_data = json.loads(rsp.text)
                rsp.close()
                if rsp_data["code"] == 200:
                    self._value = path.split("/")[-1]
                    return self._value
                return None
            else:
                return None
        except:
            return None
        finally:
            del url

    def get_update_time(self):
        if self._update_time == 0:
            self.get()
        return self._update_time

    def has_new_data(self):
        last_time = self._update_time
        self.get()
        self._data_status = True if self._update_time > last_time else False
        return self._data_status

    def get(self):
        if self._data_status:
            return self._value
        url = None
        if self._public:
            url = "{0}/{1}/data".format(_server, self._device_token)
        else:
            url = "{0}/{1}/dataByKey/{2}".format(_server, self._device_token, self._key)
        DEBUG and print("'getDeviceEzData' url:", url)
        try:
            rsp = requests.get(url, headers={})
            if rsp.status_code == 200:
                rsp_data = json.loads(rsp.text)
                rsp.close()
                if rsp_data["code"] == 200:
                    self._value = rsp_data["data"]["value"]
                    self._date_type = rsp_data["data"]["dataType"]
                    self._update_time = int(rsp_data["data"]["updateTime"])
                    return self._value
                return None
            else:
                return None
        except:
            return None
        finally:
            del url

    def get_file(self, path):
        self.get()
        if self._date_type == "file":
            try:
                rsp = requests.get(self._value)
                f = open(path, "wb")
                f.write(rsp.content)
                f.close()
            except:
                return None
            finally:
                pass

    def history(self) -> list:
        url = None
        res = []
        if self._public:
            url = "{0}/{1}/history".format(_server, self._device_token)
        else:
            url = "{0}/{1}/historyByKey/{2}".format(_server, self._device_token, self._key)
        DEBUG and print("'history' url:", url)
        try:
            rsp = requests.get(url, headers={})
            if rsp.status_code == 200:
                rsp_data = json.loads(rsp.text)
                rsp.close()
                if rsp_data["code"] == 200:
                    for i in rsp_data["data"]["rows"]:
                        res.append(i["value"])
            return res
        except:
            return None
        finally:
            del url, res

    def delete(self):
        if self._public:
            return
        url = "{0}/{1}/delete/{2}".format(_server, self._device_token, self._key)
        DEBUG and print("'delete' url:", url)
        try:
            rsp = requests.delete(
                url, headers={"deviceToken": self._device_token, "key": self._key}
            )
            if rsp.status_code == 200:
                rsp_data = json.loads(rsp.text)
                rsp.close()
                return True if rsp_data["code"] == 200 else False
        except:
            return False
        finally:
            del url


def get_key_list(device_token=None):
    data_maps = {}
    device_token = device_token if device_token else _get_token()

    url = "{0}/{1}/list".format(_server, device_token)
    DEBUG and print("'list' url:", url)
    try:
        rsp = requests.get(url, headers={})
        if rsp.status_code == 200:
            rsp_data = json.loads(rsp.text)
            rsp.close()
            if rsp_data["code"] == 200:
                for iterm in rsp_data["data"]["rows"]:
                    DEBUG and print("key:", iterm["name"])
                    DEBUG and print("value:", iterm["value"])
                    data_maps[iterm["name"]] = iterm["value"]
                return data_maps
            return None
        else:
            return None
    except:
        return None
    finally:
        del url
