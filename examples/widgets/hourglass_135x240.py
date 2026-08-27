# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""Widgets hourglass example for a 135 x 240 display.

Flip the device to change the direction of gravity. Button A refills the
upstream chamber and Button B pauses or resumes the simulation.
"""

import gc
import time

import M5
from M5 import BtnA, BtnB, Imu, Widgets


# User settings.
# Milliseconds between simulation steps. Increase this value for slower sand.
FRAME_INTERVAL_MS = 40
# Number of grains loaded by Button A. One chamber holds at most 275 grains.
INITIAL_GRAINS = 190


SCREEN_WIDTH = 135
SCREEN_HEIGHT = 240

# Required behavior: IMU X > 0 moves sand left; IMU Y > 0 moves sand down.
IMU_X_AXIS = 0
IMU_Y_AXIS = 1
# The sand grid grows rightward and downward, so the screen-space signs are -X/+Y.
IMU_X_SIGN = -1.0
IMU_Y_SIGN = 1.0
IMU_FILTER_ALPHA = 0.18
IMU_DEAD_ZONE = 0.08

CELL_SIZE = 4
GRAIN_SIZE = 3
GRID_LEFT = 23
GRID_TOP = 28
GRID_COLUMNS = 23
GRID_ROWS = 47
GRID_CENTER_COLUMN = GRID_COLUMNS // 2
GRID_NECK_ROW = GRID_ROWS // 2

CENTER_X = 67
TOP_Y = 26
NECK_Y = 120
BOTTOM_Y = 214
CHAMBER_HALF_WIDTH = 45
NECK_HALF_WIDTH = 4

COLOR_BACKGROUND = 0x071018
COLOR_FRAME = 0xB96E28
COLOR_FRAME_LIGHT = 0xF0A24A
COLOR_GLASS = 0x668899
COLOR_SAND = 0xF6C445
COLOR_SAND_LIGHT = 0xFFE08A
COLOR_PAUSED = 0x0000FF

canvas = None
cells = None
valid_cells = None
paused = False
reset_requested = False
gravity_x = 0.0
gravity_y = 1.0
frame_number = 0
last_frame_ms = 0


def grid_x(column):
    return GRID_LEFT + column * CELL_SIZE


def grid_y(row):
    return GRID_TOP + row * CELL_SIZE


def chamber_half_width(y):
    distance = abs(y - NECK_Y)
    span = NECK_Y - TOP_Y
    return NECK_HALF_WIDTH + distance * (CHAMBER_HALF_WIDTH - NECK_HALF_WIDTH) // span


def build_valid_cells():
    mask = []
    for row in range(GRID_ROWS):
        y = grid_y(row)
        half_width = chamber_half_width(y) - 1
        line = bytearray(GRID_COLUMNS)
        for column in range(GRID_COLUMNS):
            if abs(grid_x(column) - CENTER_X) <= half_width:
                line[column] = 1
        mask.append(line)
    return mask


def clear_sand():
    for row in cells:
        for column in range(GRID_COLUMNS):
            row[column] = 0


def reset_sand():
    clear_sand()
    remaining = INITIAL_GRAINS

    # Fill the chamber opposite the current vertical gravity direction.
    if gravity_y >= 0:
        rows = range(GRID_NECK_ROW - 1, -1, -1)
    else:
        rows = range(GRID_ROWS - 1, GRID_NECK_ROW, -1)

    for row in rows:
        columns = range(GRID_COLUMNS) if row & 1 else range(GRID_COLUMNS - 1, -1, -1)
        for column in columns:
            if valid_cells[row][column]:
                cells[row][column] = 1
                remaining -= 1
                if remaining <= 0:
                    return


def button_a_clicked(_state):
    global reset_requested
    reset_requested = True


def button_b_clicked(_state):
    global paused
    paused = not paused


def update_gravity(initialize=False):
    global gravity_x, gravity_y
    try:
        acceleration = Imu.getAccel()
    except Exception as error:
        print("IMU_READ_ERROR", error)
        return
    raw_x = acceleration[IMU_X_AXIS] * IMU_X_SIGN
    raw_y = acceleration[IMU_Y_AXIS] * IMU_Y_SIGN
    if initialize:
        gravity_x = raw_x
        gravity_y = raw_y
    else:
        gravity_x += (raw_x - gravity_x) * IMU_FILTER_ALPHA
        gravity_y += (raw_y - gravity_y) * IMU_FILTER_ALPHA


def gravity_step():
    x = gravity_x
    y = gravity_y
    if abs(x) < IMU_DEAD_ZONE:
        x = 0.0
    if abs(y) < IMU_DEAD_ZONE:
        y = 0.0
    if x == 0.0 and y == 0.0:
        return 0, 0

    abs_x = abs(x)
    abs_y = abs(y)
    dx = 1 if x > 0 else -1
    dy = 1 if y > 0 else -1
    if abs_x > abs_y * 1.8:
        dy = 0
    elif abs_y > abs_x * 1.8:
        dx = 0
    return dx, dy


def can_move(row, column):
    return (
        0 <= row < GRID_ROWS
        and 0 <= column < GRID_COLUMNS
        and valid_cells[row][column]
        and not cells[row][column]
    )


def move_grain(row, column, target_row, target_column):
    if not can_move(target_row, target_column):
        return False
    cells[row][column] = 0
    cells[target_row][target_column] = 1
    return True


def update_sand():
    global frame_number
    dx, dy = gravity_step()
    if dx == 0 and dy == 0:
        return

    row_range = range(GRID_ROWS - 1, -1, -1) if dy > 0 else range(GRID_ROWS)
    column_range_forward = range(GRID_COLUMNS - 1, -1, -1) if dx > 0 else range(GRID_COLUMNS)

    for row in row_range:
        for column in column_range_forward:
            if not cells[row][column]:
                continue
            if move_grain(row, column, row + dy, column + dx):
                continue

            alternate = 1 if (row + column + frame_number) & 1 else -1
            if dy:
                if move_grain(row, column, row + dy, column + alternate):
                    continue
                move_grain(row, column, row + dy, column - alternate)
            elif dx:
                if move_grain(row, column, row + alternate, column + dx):
                    continue
                move_grain(row, column, row - alternate, column + dx)
    frame_number += 1


def draw_hourglass():
    canvas.fillScreen(COLOR_BACKGROUND)

    left_top = CENTER_X - CHAMBER_HALF_WIDTH - 4
    right_top = CENTER_X + CHAMBER_HALF_WIDTH + 4
    left_neck = CENTER_X - NECK_HALF_WIDTH - 2
    right_neck = CENTER_X + NECK_HALF_WIDTH + 2

    # Glass outline.
    canvas.drawLine(left_top, TOP_Y, left_neck, NECK_Y - 5, COLOR_GLASS)
    canvas.drawLine(left_neck, NECK_Y - 5, left_neck, NECK_Y + 5, COLOR_GLASS)
    canvas.drawLine(left_neck, NECK_Y + 5, left_top, BOTTOM_Y, COLOR_GLASS)
    canvas.drawLine(right_top, TOP_Y, right_neck, NECK_Y - 5, COLOR_GLASS)
    canvas.drawLine(right_neck, NECK_Y - 5, right_neck, NECK_Y + 5, COLOR_GLASS)
    canvas.drawLine(right_neck, NECK_Y + 5, right_top, BOTTOM_Y, COLOR_GLASS)

    # Wooden top, bottom, and side supports.
    canvas.fillRoundRect(12, 16, 111, 11, 4, COLOR_FRAME)
    canvas.fillRect(17, 18, 101, 3, COLOR_FRAME_LIGHT)
    canvas.fillRoundRect(12, 213, 111, 11, 4, COLOR_FRAME)
    canvas.fillRect(17, 215, 101, 3, COLOR_FRAME_LIGHT)
    canvas.drawLine(17, 27, 17, 212, COLOR_FRAME)
    canvas.drawLine(18, 27, 18, 212, COLOR_FRAME_LIGHT)
    canvas.drawLine(117, 27, 117, 212, COLOR_FRAME)
    canvas.drawLine(116, 27, 116, 212, COLOR_FRAME_LIGHT)

    for row in range(GRID_ROWS):
        for column in range(GRID_COLUMNS):
            if cells[row][column]:
                color = COLOR_SAND_LIGHT if (row + column) % 5 == 0 else COLOR_SAND
                canvas.fillRect(
                    grid_x(column) - GRAIN_SIZE // 2,
                    grid_y(row) - GRAIN_SIZE // 2,
                    GRAIN_SIZE,
                    GRAIN_SIZE,
                    color,
                )

    if paused:
        canvas.fillRoundRect(105, 30, 20, 20, 4, COLOR_PAUSED)
        canvas.fillRect(111, 35, 3, 10, 0xFFFFFF)
        canvas.fillRect(117, 35, 3, 10, 0xFFFFFF)

    canvas.push(0, 0)


def setup():
    global canvas, cells, valid_cells, last_frame_ms
    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(COLOR_BACKGROUND)

    # Replace callbacks from an earlier run before reclaiming its canvas.
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=button_a_clicked)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=button_b_clicked)
    gc.collect()

    canvas = M5.Lcd.newCanvas(SCREEN_WIDTH, SCREEN_HEIGHT, 8, True)
    cells = [bytearray(GRID_COLUMNS) for _ in range(GRID_ROWS)]
    valid_cells = build_valid_cells()

    M5.update()
    time.sleep_ms(50)
    update_gravity(initialize=True)
    reset_sand()
    draw_hourglass()
    last_frame_ms = time.ticks_ms()


def loop():
    global last_frame_ms, reset_requested
    M5.update()
    now = time.ticks_ms()
    if time.ticks_diff(now, last_frame_ms) < FRAME_INTERVAL_MS:
        time.sleep_ms(2)
        return
    last_frame_ms = now

    update_gravity()
    if reset_requested:
        reset_requested = False
        reset_sand()
    if not paused:
        update_sand()
    draw_hourglass()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as error:
        try:
            from utility import print_error_msg

            print_error_msg(error)
        except ImportError:
            print(error)
    finally:
        if canvas is not None:
            try:
                canvas.delete()
            except Exception:
                pass
            canvas = None
        cells = None
        valid_cells = None
        gc.collect()
