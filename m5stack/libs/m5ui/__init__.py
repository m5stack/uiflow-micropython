# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "init": "port",
    "deinit": "port",
    "M5Arc": "arc",
    "M5Bar": "bar",
    "M5Button": "button",
    "M5Calendar": "calendar",
    "M5Checkbox": "checkbox",
    "M5Image": "image",
    "M5Label": "label",
    "M5Line": "line",
    "M5Page": "page",
    "M5Slider": "slider",
    "M5Switch": "switch",
    "M5TextArea": "textarea",
}


def __getattr__(attr):
    mod = _attrs.get(attr, None)
    if mod is None:
        raise AttributeError(attr)
    value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
