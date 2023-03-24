# -*- encoding: utf-8 -*-
import sys, io, M5


def print_error_msg(e: Exception, lcd=M5.Lcd) -> None:
    e_msg = io.StringIO()
    sys.print_exception(e, e_msg)
    e_msg.seek(0)
    error_str = e_msg.read()
    # print error message to lcd
    lcd.setCursor(0, 0)
    lcd.clear()
    lcd.print(error_str)
    # print error message to repl
    print(error_str)
    e_msg.close()
    # deinit
    M5.end()
