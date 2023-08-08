try:
    import urequests
except ImportError:
    import requests as urequests
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
    def __init__(self, token, key) -> None:
        self._device_token = token if token else _get_token()
        self._key = key
        self._value = None
        self._data_token = None
        self._date_type = None

    def set(self, value, is_file=False):
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
            rsp = urequests.post(url, json=payload, headers={})
            if rsp.status_code == 200:
                rsp_data = json.loads(rsp.text)
                if rsp_data["code"] == 200:
                    self._value = value
                    return self._value
                return None
            else:
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
            rsp = urequests.post(url, headers=headers, data=form.content())
            if rsp.status_code == 200:
                rsp_data = json.loads(rsp.text)
                if rsp_data["code"] == 200:
                    self._value = path.split("/")[-1]
                    return self._value
                return None
            else:
                return None
        finally:
            del url

    def get(self):
        url = "{0}/{1}/dataByKey/{2}".format(_server, self._device_token, self._key)
        DEBUG and print("'getDeviceEzData' url:", url)
        try:
            rsp = urequests.get(url, headers={})
            if rsp.status_code == 200:
                rsp_data = json.loads(rsp.text)
                if rsp_data["code"] == 200:
                    self._value = rsp_data["data"]["value"]
                    self._date_type = rsp_data["data"]["dataType"]
                    return self._value
                return None
            else:
                return None
        finally:
            del url

    def get_file(self, path):
        self.get()
        if self._date_type == "file":
            try:
                rsp = urequests.get(self._value)
                f = open(path, "wb")
                f.write(rsp.content)
                f.close()
            finally:
                pass

    def history(self) -> list:
        res = []
        url = "{0}/{1}/historyByKey/{2}".format(_server, self._device_token, self._key)
        DEBUG and print("'history' url:", url)
        try:
            rsp = urequests.get(url, headers={})
            if rsp.status_code == 200:
                rsp_data = json.loads(rsp.text)
                if rsp_data["code"] == 200:
                    for i in rsp_data["data"]["rows"]:
                        res.append(i["value"])
                    rsp.close()
            return res
        finally:
            del url, res

    def delete(self):
        url = "{0}/{1}/delete/{2}".format(_server, self._device_token, self._key)
        DEBUG and print("'delete' url:", url)
        try:
            rsp = urequests.delete(
                url, headers={"deviceToken": self._device_token, "key": self._key}
            )
            if rsp.status_code == 200:
                rsp_data = json.loads(rsp.text)
                if rsp_data["code"] == 200:
                    rsp.close()
        finally:
            del url


def get_key_list(device_token=None):
    data_maps = {}
    device_token = device_token if device_token else _get_token()

    url = "{0}/{1}/list".format(_server, device_token)
    DEBUG and print("'list' url:", url)
    try:
        rsp = urequests.get(url, headers={})
        if rsp.status_code == 200:
            rsp_data = json.loads(rsp.text)
            if rsp_data["code"] == 200:
                for iterm in rsp_data["data"]["rows"]:
                    DEBUG and print("key:", iterm["name"])
                    DEBUG and print("value:", iterm["value"])
                    data_maps[iterm["name"]] = iterm["value"]
                return data_maps
            return None
        else:
            return None
    finally:
        del url
