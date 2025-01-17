import M5
import machine


class SpeakerHat:
    _en_pin = {
        M5.BOARD.M5StickC: 0,
        M5.BOARD.M5StickCPlus: 0,
        M5.BOARD.M5StickCPlus2: 0,
        M5.BOARD.M5StackCoreInk: 25,
    }

    def __new__(cls, *args, **kwargs):
        spk = M5.createSpeaker()
        pin_en = machine.Pin(cls._en_pin.get(M5.getBoard()), machine.Pin.OUT)
        pin_en(1)
        spk.config(pin_data_out=26, use_dac=True, buzzer=False, magnification=32)
        spk.begin()
        spk.setVolume(80)
        return spk
