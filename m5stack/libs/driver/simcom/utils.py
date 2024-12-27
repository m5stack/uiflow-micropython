# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time


def converter(data, type):
    if isinstance(data, type):
        return data

    if isinstance(data, str):
        if type == bytes:
            return data.encode("utf-8")
        if type == bytearray:
            return bytearray(data, "utf-8")

    if isinstance(data, bytes):
        if type == str:
            return data.decode("utf-8")
        if type == bytearray:
            return bytearray(data)

    if isinstance(data, bytearray):
        if type == str:
            return str(data, "utf-8")
        if type == bytes:
            return bytes(data)


def extract_text(text, beg, end) -> str | bytes | bytearray:
    # print("text:", repr(text), "start:", repr(beg), "end:", repr(end))
    beg = converter(beg, type(text))
    end = converter(end, type(text))
    start_pos = text.find(beg)
    if start_pos == -1:
        return type(text)()
    start_pos += len(beg)
    end_pos = text.find(end, start_pos)
    if end_pos == -1:
        return type(text)()
    return text[start_pos:end_pos]


def extract_int(text, start_str, end_str) -> int | None:
    text = extract_text(text, start_str, end_str)
    return int(text) if text else None


def extract_list(text, start_str, end_str) -> list:
    o = extract_text(text, start_str, end_str)
    o = converter(o, str)
    return o.split(",") if o else []


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.ticks_ms()
        result = func(*args, **kwargs)
        end_time = time.ticks_ms()
        execution_time = end_time - start_time
        print(f"total time consumed to execute {func}: {execution_time}ms")
        return result

    return wrapper
