import m5
from m5 import lcd
import random

WIDTH = 320
HEIGHT = 240

m5.begin()
canvas = m5.lcd.newCanvas(WIDTH, HEIGHT, 1, 1)


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
for i in range(0, 100):
    r = random.randint(10, 25) + 3
    balls.append(
        Ball(
            int(random.randint(r, r + (WIDTH - 2 * r))),
            int(random.randint(r, r + (HEIGHT - 2 * r))),
            r,
            int((10 - r) / 2),
            int((10 - r) / 2),
            # int(random.randint(0x0, 0x01)),
            1,
            i,
        )
    )


def run():
    while True:
        for ball in balls:
            ball.x += ball.dx
            ball.y += ball.dy

            xmax = WIDTH - ball.r
            xmin = ball.r
            ymax = HEIGHT - ball.r
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
            canvas.drawCircle(ball.x, ball.y, ball.r, lcd.BLACK)
            canvas.setCursor(ball.x - 4, ball.y - 4)
            canvas.print(str(ball.index), lcd.BLACK)
