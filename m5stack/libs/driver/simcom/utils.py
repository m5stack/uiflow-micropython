# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import re
import time


def extract_text(text, start_str, end_str) -> str:
    # print("text:", repr(text))
    # print("start_str:", repr(start_str))
    # print("end_str:", repr(start_str))
    pattern = re.compile(f"{start_str}(.*?){end_str}")
    match = re.search(pattern, text)
    return match.group(1) if match else None


def extract_int(text, start_str, end_str) -> int:
    pattern = re.compile(f"{start_str}(.*?){end_str}")
    match = re.search(pattern, text)
    return int(match.group(1)) if match else None


def extract_number(text) -> list:
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    pattern = r"\d+(?:,\d+)*"
    match = re.search(pattern, text)
    if match:
        return [int(x) for x in match.group(0).split(",")]
    return []


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.ticks_ms()
        result = func(*args, **kwargs)  # 执行原函数
        end_time = time.ticks_ms()  # 记录结束时间
        execution_time = end_time - start_time  # 计算执行时间
        print(f"total time consumed to execute {func}: {execution_time}ms")
        return result

    return wrapper
