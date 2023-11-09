from hardware import Button


def DualButtonUnit(port):
    return Button(port[0]), Button(port[1])
