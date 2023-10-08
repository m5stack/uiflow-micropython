from collections import namedtuple
import _thread
import time

# Queue = namedtuple("Queue", ["task", "period", "enable"])

thread_id = 0
thread_status = False


class Task:
    def __init__(self, fn, period, enable) -> None:
        self.fn = fn
        self.period = period
        self.enable = enable
        self.last_time = time.ticks_ms()


tasks = []


def register_queue(task: Task):
    if len(tasks) < 3:
        tasks.append(task)


def loop():
    while True:
        for task in tasks:
            if task.enable is not True:
                continue
            if time.ticks_ms() - task.last_time >= task.period:
                task.fn and task.fn()
                task.last_time = time.ticks_ms()
        time.sleep_ms(100)
    _thread.exit()
