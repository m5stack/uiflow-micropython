# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# draw moving circle with circle id
import M5
import random

scr_width = 0
scr_height = 0
canvas = None


class Ball:
    def __init__(self, x, y, r, dx, dy, color, index):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.color = color
        self.index = index


# initialise shapes
balls = []


def setup():
    global canvas, balls, scr_width, scr_height
    M5.begin()
    scr_width = M5.Display.width()
    scr_height = M5.Display.height()
    canvas = M5.Display.newCanvas(scr_width, scr_height, 1, 1)

    for i in range(0, 100):
        r = random.randint(10, 25) + 3
        x = int(random.randint(r, r + (scr_width - (2 * r))))
        y = int(random.randint(r, r + (scr_height - (2 * r))))
        balls.append(Ball(x, y, r, int((10 - r) / 2), int((10 - r) / 2), 1, i))


def loop():
    global canvas, balls, scr_width, scr_height
    for ball in balls:
        ball.x += ball.dx
        ball.y += ball.dy

        xmax = scr_width - ball.r
        xmin = ball.r
        ymax = scr_height - ball.r
        ymin = ball.r

        if ball.x <= xmin or ball.x >= xmax:
            ball.dx *= -1

        if ball.y <= ymin or ball.y >= ymax:
            ball.dy *= -1

        canvas.drawCircle(ball.x, ball.y, ball.r, ball.color)
        canvas.setCursor(ball.x - 4, ball.y - 4)
        canvas.print(str(ball.index), ball.color)

    canvas.push(0, 0)

    for ball in balls:
        canvas.drawCircle(ball.x, ball.y, ball.r, M5.Display.BLACK)
        canvas.setCursor(ball.x - 4, ball.y - 4)
        canvas.print(str(ball.index), M5.Display.BLACK)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except:
        # error handler
        # if use canvas, need manual delete it to free allocated memory for now
        if canvas:
            canvas.delete()
