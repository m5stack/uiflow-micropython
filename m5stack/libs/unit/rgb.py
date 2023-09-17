from driver.neopixel.sk6812 import SK6812


class RGB(SK6812):
    def __init__(self, port, number):
        super().__init__(port[1], number)
