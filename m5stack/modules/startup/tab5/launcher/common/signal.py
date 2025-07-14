# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


class Signal:
    def __init__(self):
        self._slots = []

    def connect(self, func):
        if callable(func) and func not in self._slots:
            self._slots.append(func)

    def disconnect(self, func):
        if func in self._slots:
            self._slots.remove(func)

    def clear(self):
        self._slots.clear()

    def emit(self, *args, **kwargs):
        for func in self._slots:
            func(*args, **kwargs)

    def __len__(self):
        return len(self._slots)

    def __contains__(self, func):
        return func in self._slots
