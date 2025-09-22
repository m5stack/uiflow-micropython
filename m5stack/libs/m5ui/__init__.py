# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "init": "port",
    "deinit": "port",
    "event_loop": "port",
    "M5Arc": "arc",
    "M5Bar": "bar",
    "M5Button": "button",
    "M5ButtonMatrix": "buttonmatrix",
    "M5Calendar": "calendar",
    "M5Canvas": "canvas",
    "M5Checkbox": "checkbox",
    "M5Dropdown": "dropdown",
    "M5Image": "image",
    "M5Keyboard": "keyboard",
    "M5Label": "label",
    "M5LED": "led",
    "M5Line": "line",
    "M5List": "list",
    "M5Msgbox": "msgbox",
    "M5Page": "page",
    "M5Roller": "roller",
    "M5Scale": "scale",
    "M5Slider": "slider",
    "M5Spinbox": "spinbox",
    "M5Spinner": "spinner",
    "M5Switch": "switch",
    "M5TextArea": "textarea",
    "M5Win": "win",
}


def __getattr__(attr):
    mod = _attrs.get(attr, None)
    if mod is None:
        raise AttributeError(attr)
    value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
