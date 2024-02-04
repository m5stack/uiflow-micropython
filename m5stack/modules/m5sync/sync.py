# -*- encoding: utf-8 -*-
"""
@File    :   sync.py
@Time    :   2024/1/22
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

"""
HOW TO USE:

import sync
sync.run()

This module will download files from res.json and save them to /flash/res.
It will also create a record.json to record the files it has downloaded.
Included a simple GUI to show the progress.

If a file in record.json is not in res.json, it will be deleted.
If a file in res.json is not in record.json, it will be downloaded.
If a file in res.json is in record.json, it will be skipped.
"""

import json
import M5
import os
import hashlib
try:
    import urequests as requests
except ImportError:
    import requests
import network
from hardware import RGB
import time

# Log control
WARN = True
INFO = True
DEBUG = False

config = {
    "path_prefix": "/flash/res",
    "sync_file": "/flash/res/res.json",
}

lcd_param = {
    "mode": "",
    "w": "",
    "h": "",
    "cx": "",
    "cy": "",
    "bar_width": "",
    "bar_start": "",
}

rgb = None

RECORD_JSON_PATH = f"{config['path_prefix']}/{'record.json'}"
SYNC_JSON_PATH = f"{config['path_prefix']}/{'res.json'}"
COLOR_RED = 0xFF0000
COLOR_YELLOW = 0xFFFF00
COLOR_BLUE = 0x0000FF
COLOR_GREEN = 0x00FF00


def file_exists(file_path):
    try:
        with open(file_path, "r"):
            return True
    except OSError:
        return False


def file_copy(source_path, destination_path):
    try:
        # 打开源文件和目标文件
        with open(source_path, "rb") as source_file, open(destination_path, "wb") as dest_file:
            # 逐块读取源文件并写入目标文件
            chunk_size = 1024  # 1KB
            while True:
                chunk = source_file.read(chunk_size)
                if not chunk:
                    break
                dest_file.write(chunk)

        DEBUG and print("Debug: File copied successfully.")
    except Exception as e:
        WARN and print("WARN: File copied error:", e)


def downloadFile(url, save_path, retry=3):
    update_info(f"fetching {save_path}")

    def _downloadFile(url, save_path):
        # 发送GET请求
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            length = int(response.headers["Content-Length"])
            BLOCKLEN = 4096
            source = response.raw
            read = 0
            with open(save_path, "wb") as file:
                # 逐块读取数据
                while read < length:
                    to_read = BLOCKLEN if (length - read) >= BLOCKLEN else length - read
                    buf = source.read(to_read)
                    read += len(buf)
                    DEBUG and print(f"Debug: {read}/{length}; LEN = {len(buf)}", end="\r")
                    file.write(buf)
                    update_progress(0, read / length)
                    update_info(f"{read}/{length}")
                    # time.sleep(0.1) #emulate slow connection
                INFO and print(f"Info: File {url} downloaded successfully.")
            response.close()
            return True
        else:
            WARN and print("Warn: Failed to download file. code = %d" % response.status_code)
            response.close()
            return False

    for i in range(retry):
        if _downloadFile(url, save_path):
            return True
        WARN and print(f"Warn: Retry {i+1}...")


def calculateMD5(file_path):
    md5_hash = hashlib.md5()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            md5_hash.update(data)
    return md5_hash.digest().hex()


def sync_available():
    return file_exists(SYNC_JSON_PATH)


def open_or_create_chche(file_path):
    DEBUG and print("Debug: record.json path:", file_path)
    INFO and print("Info: Opening record.json...")
    if file_exists(file_path):
        root = None
        with open(file_path, "r") as f:
            root = json.load(f)
            return root["fileList"]
    return []


def open_or_create_json(file_path):
    DEBUG and print("Debug: open record.json path:", file_path)
    INFO and print("Info: Opening record.json...")
    if file_exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    else:
        return {"time": time.mktime(time.localtime()), "fileList": []}


def save_json(file_path, data):
    DEBUG and print("Debug: save record.json path:", file_path)
    with open(file_path, "w") as f:
        json.dump({"time": time.mktime(time.localtime()), "fileList": data}, f)


def process_files(record, sync):
    # TODO
    err = ""

    # 检查sync文件中的记录在不在record中，不在就删除
    for old_file in record:
        no_exist = True
        for file in sync:
            if file["devicePath"] == old_file["devicePath"]:
                no_exist = False
                break
        if no_exist:
            try:
                os.remove(old_file["devicePath"])
                INFO and print("Info: Deleted file:", old_file["devicePath"])
            except OSError as e:
                WARN and print(f"Warn: Error deleting file {old_file['devicePath']}: {e}")
            record.remove(old_file)
            continue  # 继续下一个循环，不增加索引

    # 检查record文件中的记录在不在sync中，不在就下载
    i = 0
    file_num = len(sync)
    for file in sync:
        update_info(f"{i+1}/{file_num}")
        if file_exists(file["devicePath"]):
            # 如果文件存在，检查md5
            if calculateMD5(file["devicePath"]) == file["md5"]:
                INFO and print(f"Info: File {file['devicePath']} already downloaded.")
                i += 1
                update_progress(i / file_num, 1.0)
                for index in range(len(record)):
                    if record[index]["devicePath"] == file["devicePath"]:
                        record.pop(index)
                        break
                record.append(file)
                continue

        # 如果文件不存在，或者md5不匹配，下载文件
        INFO and print(f"Info: MD5 mismatch for file: {file['name']}")
        for _ in range(3):
            if downloadFile(file["url"], file["devicePath"]) is False:
                INFO and print(f"Info: Failed to download file: {file['devicePath']}")
                continue
            if calculateMD5(file["devicePath"]) == file["md5"]:
                INFO and print(f"Info: Downloaded and verified file: {file['devicePath']}")
                for index in range(len(record)):
                    if record[index]["devicePath"] == file["devicePath"]:
                        record.pop(index)
                        break
                record.append(file)
                break
        i += 1
        update_progress(i / file_num, 1.0)
    return err


def draw_status(status):
    if lcd_param["mode"] == "led":
        rgb.set_color(0, COLOR_YELLOW)
        return
    cx = lcd_param["cx"]
    cy = lcd_param["cy"]
    M5.Lcd.setTextColor(0, 0xFFFFFF)
    if lcd_param["w"] > 120:
        M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu40)
        M5.Lcd.fillRect(lcd_param["bar_start"], cy - 40, lcd_param["w"], 40, 0xFFFFFF)
        M5.Lcd.drawCenterString(status, cx, cy - 40)
    else:
        M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu24)
        M5.Lcd.fillRect(lcd_param["bar_start"], cy - 24, lcd_param["w"], 24, 0xFFFFFF)
        M5.Lcd.drawCenterString(status, cx, cy - 24)


last_progress_led_c = 0


def update_progress(total_progress, progress):
    if lcd_param["mode"] == "led":
        if last_progress_led_c == 0:
            last_progress_led_c = COLOR_YELLOW
        else:
            last_progress_led_c = 0
        rgb.set_color(0, last_progress_led_c)  # blink led when downloading
        return
    cx = lcd_param["cx"]
    cy = lcd_param["cy"]
    y1 = cy + 10
    y2 = cy + 35
    bar_width = lcd_param["bar_width"]
    bar_start = lcd_param["bar_start"]
    total_progress_w = int(bar_width * total_progress)
    progress_w = int(bar_width * progress)
    M5.Lcd.drawRect(bar_start, y1, bar_width, 15, 0)
    M5.Lcd.fillRect(bar_start + total_progress_w, y2, bar_width - total_progress_w, 15, 0xFFFFFF)
    M5.Lcd.drawRect(bar_start, y2, bar_width, 15, 0)
    M5.Lcd.fillRect(bar_start, y1, total_progress_w, 15, 0)
    M5.Lcd.fillRect(bar_start, y2, progress_w, 15, 0)


def update_info(info):
    if lcd_param["mode"] == "led":
        rgb.set_color(0, COLOR_YELLOW)
        return
    cx = lcd_param["cx"]
    cy = lcd_param["cy"]
    M5.Lcd.setTextColor(0, 0xFFFFFF)
    M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu12)
    M5.Lcd.fillRect(lcd_param["bar_start"], cy + 55, lcd_param["w"], 15, 0xFFFFFF)
    M5.Lcd.drawString(info, lcd_param["bar_start"], cy + 55)


def wait_key(timeout=5000):
    start = time.time()
    while time.time() - start < timeout:
        M5.update()
        if M5.Touch.getCount() > 0:
            return
        if M5.BtnA.wasClicked() or M5.BtnB.wasClicked() or M5.BtnC.wasClicked():
            return
        if M5.BtnPWR.wasPressed():
            return
    return


def run():
    INFO and print("Info: Syncing resources...")

    wlan = network.WLAN(network.STA_IF)
    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    if not wlan.isconnected():
        WARN and print("Warn: WiFi not connected.")
        WARN and print("Warn: quit sync.")
        return

    INFO and print("Info: WiFi connected!")

    # STEP1: create or open record.json
    cache_records = open_or_create_chche(RECORD_JSON_PATH)
    # record = open_or_create_json(RECORD_JSON_PATH)
    DEBUG and print("Debug: record.json:", cache_records)

    # STEP2: open res.json
    file_records = []
    if not file_exists(SYNC_JSON_PATH):
        return
    else:
        with open(SYNC_JSON_PATH, "r") as f:
            sync = json.load(f)
        DEBUG and print("Debug: res.json:", sync)
        file_records = sync["fileList"]

    if len(cache_records) == 0 and len(file_records) == 0:
        INFO and print("Info: No files to sync.")
        return # no files to sync

    # STEP3: init lcd or led
    if M5.Lcd.width() != 0:
        lcd_param["mode"] = "lcd"
        lcd_param["w"] = M5.Lcd.width()
        lcd_param["h"] = M5.Lcd.height()
        lcd_param["cx"] = lcd_param["w"] // 2
        lcd_param["cy"] = lcd_param["h"] // 2
        lcd_param["bar_width"] = lcd_param["w"] - 40
        lcd_param["bar_start"] = 20
        M5.Lcd.clear(0xFFFFFF)
    else:
        lcd_param["mode"] = "led"
        rgb = RGB()
        rgb.set_color(0, COLOR_RED)
        rgb.set_brightness(30)

    draw_status(f"Sync...")
    update_progress(0, 0)
    update_info("pending")

    # STEP4: process files
    err = process_files(cache_records, file_records)

    if len(err) > 0:
        update_info(err)
        draw_status("Failed")
        if lcd_param["mode"] == "led":
            rgb.set_color(0, COLOR_RED)
    else:
        update_info(f"downloaded {len(sync['fileList'])} file(s)")
        draw_status("Done")
        if lcd_param["mode"] == "led":
            rgb.set_color(0, COLOR_GREEN)

    # STEP5: save record, remove res.json
    save_json(RECORD_JSON_PATH, cache_records)
    if len(err) > 0:
        wait_key()

    if lcd_param["mode"] == "led":
        rgb.set_color(0, 0)
    else:
        print("Press any key to continue...")
        M5.Lcd.clear(0x000000)
        M5.Lcd.setTextColor(0xFFFFFF, 0)
