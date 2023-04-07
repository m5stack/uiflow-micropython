from hardware import RGB as RGBBase

class RGB(RGBBase):

    def __int__(self, port, number):
        super().__init__(io=port[1], n=number, type="SK6812")
