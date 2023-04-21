from hardware import Button


def DualButton(port):
    return Button(port[0]), Button(port[1])
