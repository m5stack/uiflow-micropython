import bleuart
import time


def server_demo():
    uart = bleuart.BLEUARTServer(verbose=False)

    def on_rx():
        print("rx: ", uart.read().decode().strip())

    # uart.irq(handler=on_rx)

    try:
        while True:
            l = uart.any()
            if l > 0:
                uart.write(uart.read())
            else:
                time.sleep_ms(1000)
    except KeyboardInterrupt:
        pass

    uart.close()

def client_demo():
    uart = bleuart.BLEUARTClient(verbose=False)

    not_found = False
    def on_scan(addr_type, addr, name):
        if addr_type is not None:
            print("Found sensor:", addr_type, addr, name)
            uart.connect()
        else:
            nonlocal not_found
            not_found = True
            print("No sensor found.")

    uart.scan(callback=on_scan)

    # Wait for connection...
    while not uart.is_connected():
        time.sleep_ms(100)
        if not_found:
            return

    print("Connected")

    nums = [4, 8, 15, 16, 23, 42]
    i = 0

    try:
        while True:
            uart.write(str(nums[i]))
            i = (i + 1) % len(nums)
            time.sleep_ms(1000)
            print("rx: ", uart.read().decode().strip())
    except KeyboardInterrupt:
        pass

    uart.close()

client_demo()
