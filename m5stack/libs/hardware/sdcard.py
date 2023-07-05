import machine, os

sd = None


def SDCard(
    slot=1, width=1, cd=None, wp=None, sck=None, miso=None, mosi=None, cs=None, freq=20000000
):
    global sd
    try:
        os.umount("/sd")
        sd.deinit()
    except Exception as e:
        print(e)
    finally:
        sd = machine.SDCard(
            slot=slot, width=width, cd=cd, wp=wp, sck=sck, miso=miso, mosi=mosi, cs=cs, freq=freq
        )
        sd.info()
        os.mount(sd, "/sd")
