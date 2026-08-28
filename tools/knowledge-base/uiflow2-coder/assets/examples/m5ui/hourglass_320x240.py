# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""M5UI/LVGL hourglass example for a 320 x 240 display.

Touch REFILL to reload the upstream chamber. Touch PAUSE/RESUME to stop or
continue the simulation.
"""

import gc
import time

import M5
import lvgl as lv
import m5ui
from M5 import Imu, Widgets


# User settings.
# Milliseconds between display updates.
FRAME_INTERVAL_MS = 40
# Two physics steps per display update makes the default sand speed 2x faster
# without forcing LVGL to redraw at 50 FPS.
SIMULATION_STEPS_PER_FRAME = 2
# Number of grains loaded by REFILL. One chamber holds about 300 grains.
INITIAL_GRAINS = 260


SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
CANVAS_X = 80
CANVAS_WIDTH = 160
CANVAS_HEIGHT = 240

# Required screen behavior:
#   IMU X > 0 points to screen right, so sand moves left.
#   IMU Y > 0 points to screen top, so sand moves down.
# LVGL/canvas coordinates grow rightward and downward, hence -X/+Y.
IMU_X_AXIS = 0
IMU_Y_AXIS = 1
IMU_X_SIGN = -1.0
IMU_Y_SIGN = 1.0
IMU_FILTER_ALPHA = 0.18
IMU_DEAD_ZONE = 0.08

CELL_SIZE = 4
GRAIN_SIZE = 3
SAND_GLASS_MARGIN = 7
GRID_LEFT = 12
GRID_TOP = 20
GRID_COLUMNS = 35
GRID_ROWS = 51
GRID_NECK_ROW = 25

CENTER_X = 80
TOP_Y = 12
NECK_Y = 120
BOTTOM_Y = 228
CHAMBER_HALF_WIDTH = 65
NECK_HALF_WIDTH = 5

COLOR_BACKGROUND = 0x081118
COLOR_SURFACE = 0x152129
COLOR_FRAME = 0xA96028
COLOR_FRAME_LIGHT = 0xE99A48
COLOR_GLASS = 0x7DA4B8
COLOR_SAND = 0xF4C542
COLOR_SAND_LIGHT = 0xFFE59A
COLOR_ACCENT = 0x2BAAC0
COLOR_TEXT = 0xF3F7F8

page = None
canvas_front = None
canvas_back = None
canvas_front_buffer = None
canvas_back_buffer = None
canvas_front_layer = None
canvas_back_layer = None
line_descriptor = None
rect_descriptor = None
grain_descriptor = None
draw_area = None
lv_colors = None
refill_button = None
pause_button = None
cells = None
valid_cells = None
paused = False
refill_requested = False
gravity_x = 0.0
gravity_y = 1.0
frame_number = 0
last_frame_ms = 0


def grid_x(column):
    return GRID_LEFT + column * CELL_SIZE


def grid_y(row):
    return GRID_TOP + row * CELL_SIZE


def glass_outline_half_width(y):
    neck_top = NECK_Y - 5
    neck_bottom = NECK_Y + 5
    outer_half_width = CHAMBER_HALF_WIDTH + 5
    neck_outline_half_width = NECK_HALF_WIDTH + 2

    if y < neck_top:
        return neck_outline_half_width + (
            (neck_top - y) * (outer_half_width - neck_outline_half_width) // (neck_top - TOP_Y)
        )
    if y <= neck_bottom:
        return neck_outline_half_width
    return neck_outline_half_width + (
        (y - neck_bottom)
        * (outer_half_width - neck_outline_half_width)
        // (BOTTOM_Y - neck_bottom)
    )


def build_valid_cells():
    mask = []
    for row in range(GRID_ROWS):
        y = grid_y(row)
        # Derive the mask from the actual six glass lines, then keep the full
        # 4 x 4 clearing cell away from their 2px strokes.
        half_width = max(0, glass_outline_half_width(y) - SAND_GLASS_MARGIN)
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


def reset_sand(force_top=False):
    clear_sand()
    remaining = INITIAL_GRAINS

    # Startup always begins in the top chamber. Later refills load the chamber
    # opposite the current vertical gravity direction.
    if force_top or gravity_y >= 0:
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


def refill_clicked(_event):
    global refill_requested
    refill_requested = True


def pause_clicked(_event):
    global paused
    paused = not paused
    pause_button.set_btn_text("RESUME" if paused else "PAUSE")


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
    column_range = range(GRID_COLUMNS - 1, -1, -1) if dx > 0 else range(GRID_COLUMNS)

    for row in row_range:
        for column in column_range:
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


def draw_line(layer, x1, y1, x2, y2, color, width=1):
    line_descriptor.init()
    line_descriptor.color = lv_colors[color]
    line_descriptor.opa = lv.OPA.COVER
    line_descriptor.width = width
    line_descriptor.p1.x = x1
    line_descriptor.p1.y = y1
    line_descriptor.p2.x = x2
    line_descriptor.p2.y = y2
    line_descriptor.round_start = 1
    line_descriptor.round_end = 1
    lv.draw_line(layer, line_descriptor)


def draw_rect(layer, x, y, width, height, color, radius=0):
    rect_descriptor.init()
    rect_descriptor.radius = radius
    rect_descriptor.bg_color = lv_colors[color]
    rect_descriptor.bg_opa = lv.OPA.COVER
    rect_descriptor.border_width = 0
    draw_area.x1 = x
    draw_area.y1 = y
    draw_area.x2 = x + width - 1
    draw_area.y2 = y + height - 1
    lv.draw_rect(layer, rect_descriptor, draw_area)


def draw_grain(layer, x, y, color):
    grain_descriptor.bg_color = lv_colors[color]
    draw_area.x1 = x
    draw_area.y1 = y
    draw_area.x2 = x + GRAIN_SIZE - 1
    draw_area.y2 = y + GRAIN_SIZE - 1
    lv.draw_rect(layer, grain_descriptor, draw_area)


def draw_hourglass(target, layer):
    left_top = CENTER_X - CHAMBER_HALF_WIDTH - 5
    right_top = CENTER_X + CHAMBER_HALF_WIDTH + 5
    left_neck = CENTER_X - NECK_HALF_WIDTH - 2
    right_neck = CENTER_X + NECK_HALF_WIDTH + 2

    target.fill_bg(lv_colors[COLOR_BACKGROUND], lv.OPA.COVER)
    target.init_layer(layer)

    # Glass outline.
    draw_line(layer, left_top, TOP_Y, left_neck, NECK_Y - 5, COLOR_GLASS, 2)
    draw_line(layer, left_neck, NECK_Y - 5, left_neck, NECK_Y + 5, COLOR_GLASS, 2)
    draw_line(layer, left_neck, NECK_Y + 5, left_top, BOTTOM_Y, COLOR_GLASS, 2)
    draw_line(layer, right_top, TOP_Y, right_neck, NECK_Y - 5, COLOR_GLASS, 2)
    draw_line(layer, right_neck, NECK_Y - 5, right_neck, NECK_Y + 5, COLOR_GLASS, 2)
    draw_line(layer, right_neck, NECK_Y + 5, right_top, BOTTOM_Y, COLOR_GLASS, 2)

    # Wooden rails and side supports.
    draw_rect(layer, 2, 4, 156, 12, COLOR_FRAME, 4)
    draw_rect(layer, 10, 6, 140, 3, COLOR_FRAME_LIGHT, 1)
    draw_rect(layer, 2, 224, 156, 12, COLOR_FRAME, 4)
    draw_rect(layer, 10, 226, 140, 3, COLOR_FRAME_LIGHT, 1)
    draw_line(layer, 8, 16, 8, 223, COLOR_FRAME, 3)
    draw_line(layer, 152, 16, 152, 223, COLOR_FRAME, 3)

    # Keep the same independent 3 x 3 grains as the Widgets reference.
    for row in range(GRID_ROWS):
        for column in range(GRID_COLUMNS):
            if cells[row][column]:
                color = COLOR_SAND_LIGHT if (row + column) % 5 == 0 else COLOR_SAND
                draw_grain(
                    layer,
                    grid_x(column) - GRAIN_SIZE // 2,
                    grid_y(row) - GRAIN_SIZE // 2,
                    color,
                )

    target.finish_layer(layer)


def render_next_frame():
    global canvas_front, canvas_back, canvas_front_layer, canvas_back_layer
    draw_hourglass(canvas_back, canvas_back_layer)
    # Show the completed frame before hiding the old one, so no blank frame is
    # ever exposed. This is the LVGL equivalent of the Widgets canvas.push().
    canvas_back.remove_flag(lv.obj.FLAG.HIDDEN)
    canvas_front.add_flag(lv.obj.FLAG.HIDDEN)
    canvas_front, canvas_back = canvas_back, canvas_front
    canvas_front_layer, canvas_back_layer = canvas_back_layer, canvas_front_layer


def create_lvgl_canvas():
    target = lv.canvas(page)
    buffer = lv.draw_buf_create(CANVAS_WIDTH, CANVAS_HEIGHT, lv.COLOR_FORMAT.RGB565, 0)
    target.set_draw_buf(buffer)
    target.set_pos(CANVAS_X, 0)
    target.fill_bg(lv_colors[COLOR_BACKGROUND], lv.OPA.COVER)
    layer = lv.layer_t()
    return target, buffer, layer


def setup():
    global page, canvas_front, canvas_back, refill_button, pause_button
    global canvas_front_buffer, canvas_back_buffer
    global canvas_front_layer, canvas_back_layer
    global line_descriptor, rect_descriptor, grain_descriptor, draw_area, lv_colors
    global cells, valid_cells, last_frame_ms

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page = m5ui.M5Page(bg_c=COLOR_SURFACE)
    # Replace LVGL's default white screen immediately. Widgets and the initial
    # sand are then built on this already-visible dark page.
    page.screen_load()

    lv_colors = {
        COLOR_BACKGROUND: lv.color_hex(COLOR_BACKGROUND),
        COLOR_FRAME: lv.color_hex(COLOR_FRAME),
        COLOR_FRAME_LIGHT: lv.color_hex(COLOR_FRAME_LIGHT),
        COLOR_GLASS: lv.color_hex(COLOR_GLASS),
        COLOR_SAND: lv.color_hex(COLOR_SAND),
        COLOR_SAND_LIGHT: lv.color_hex(COLOR_SAND_LIGHT),
    }
    line_descriptor = lv.draw_line_dsc_t()
    rect_descriptor = lv.draw_rect_dsc_t()
    grain_descriptor = lv.draw_rect_dsc_t()
    grain_descriptor.init()
    grain_descriptor.radius = 0
    grain_descriptor.bg_opa = lv.OPA.COVER
    grain_descriptor.border_width = 0
    draw_area = lv.area_t()

    canvas_front, canvas_front_buffer, canvas_front_layer = create_lvgl_canvas()
    canvas_back, canvas_back_buffer, canvas_back_layer = create_lvgl_canvas()
    canvas_front.add_flag(lv.obj.FLAG.HIDDEN)
    canvas_back.add_flag(lv.obj.FLAG.HIDDEN)
    refill_button = m5ui.M5Button(
        text="REFILL",
        x=4,
        y=94,
        w=68,
        h=52,
        bg_c=COLOR_ACCENT,
        text_c=COLOR_TEXT,
        font=lv.font_montserrat_14,
        parent=page,
    )
    pause_button = m5ui.M5Button(
        text="PAUSE",
        x=248,
        y=94,
        w=68,
        h=52,
        bg_c=COLOR_FRAME,
        text_c=COLOR_TEXT,
        font=lv.font_montserrat_14,
        parent=page,
    )
    refill_button.set_style_radius(6, lv.PART.MAIN)
    pause_button.set_style_radius(6, lv.PART.MAIN)
    refill_button.add_event_cb(refill_clicked, lv.EVENT.CLICKED, None)
    pause_button.add_event_cb(pause_clicked, lv.EVENT.CLICKED, None)

    cells = [bytearray(GRID_COLUMNS) for _ in range(GRID_ROWS)]
    valid_cells = build_valid_cells()

    # The first IMU sample directly establishes gravity before sand is loaded.
    M5.update()
    time.sleep_ms(50)
    update_gravity(initialize=True)
    reset_sand(force_top=True)
    draw_hourglass(canvas_front, canvas_front_layer)
    canvas_front.remove_flag(lv.obj.FLAG.HIDDEN)
    last_frame_ms = time.ticks_ms()


def loop():
    global last_frame_ms, refill_requested
    M5.update()
    now = time.ticks_ms()
    if time.ticks_diff(now, last_frame_ms) < FRAME_INTERVAL_MS:
        time.sleep_ms(2)
        return
    last_frame_ms = now

    update_gravity()
    render_requested = False
    if refill_requested:
        refill_requested = False
        reset_sand()
        render_requested = True
    elif not paused:
        for _step in range(SIMULATION_STEPS_PER_FRAME):
            update_sand()
        render_requested = True
    if render_requested:
        render_next_frame()


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
        try:
            m5ui.deinit()
        except Exception:
            pass
        page = None
        canvas_front = None
        canvas_back = None
        canvas_front_buffer = None
        canvas_back_buffer = None
        canvas_front_layer = None
        canvas_back_layer = None
        line_descriptor = None
        rect_descriptor = None
        grain_descriptor = None
        draw_area = None
        lv_colors = None
        cells = None
        valid_cells = None
        gc.collect()
