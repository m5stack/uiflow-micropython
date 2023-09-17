import _thread
import time

PERIODIC = 0x00
ONE_SHOT = 0x01


class Timer:
    PERIODIC = 0x00
    ONE_SHOT = 0x01

    def __init__(self, period, mode, callback):
        self.callback = callback
        self.nextTime = time.ticks_ms() + period
        self.period = period
        self.mode = mode
        self.dead = False

    def update(self):
        if time.ticks_ms() > self.nextTime:
            self.nextTime = time.ticks_ms() + self.period
            try:
                self.callback()
            except:
                pass
            if self.mode == Timer.ONE_SHOT:
                self.dead = True

    def deinit(self):
        self.dead = True


delete_num = []


class TimerThread:
    PERIODIC = 0x00
    ONE_SHOT = 0x01

    def __init__(self):
        self.timerList = []
        self._thread_run = False

    def checkInit(self):
        if not self._thread_run:
            self._thread_run = True
            _thread.start_new_thread(self.timeCb, ())

    def addTimer(self, period, mode, callback):
        self.checkInit()
        timer = Timer(period, mode, callback)
        self.timerList.append(timer)
        return timer

    def timeCb(self):
        global delete_num
        while True:
            for i in self.timerList:
                if i.dead:
                    delete_num.append(i)
                else:
                    i.update()
            if delete_num:
                for i in delete_num:
                    self.timerList.remove(i)
                delete_num = []
            time.sleep_ms(10)

    def deinit(self):
        pass
