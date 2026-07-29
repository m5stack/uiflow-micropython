# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import uwb
from stamp import StampUWB
import time
import struct


stamp_uwb = None
poll_frame = None
sequence = None
status = None
response = None
expected_response = None
poll_tx = None
response_rx = None
delayed_time = None
delayed_time_even = None
final_tx = None
final_frame = None


def setup():
    global \
        stamp_uwb, \
        poll_frame, \
        sequence, \
        status, \
        response, \
        expected_response, \
        poll_tx, \
        response_rx, \
        delayed_time, \
        delayed_time_even, \
        final_tx, \
        final_frame

    M5.begin()
    stamp_uwb = StampUWB()
    stamp_uwb.configure(
        preamble_length=128,
        pac=8,
        tx_code=9,
        rx_code=9,
        sfd_type=uwb.SFD_DW_8,
        data_rate=uwb.BR_6M8,
        phr_mode=uwb.PHR_STD,
        phr_rate=uwb.PHR_RATE_STD,
        sfd_timeout=129,
    )
    stamp_uwb.configure_tx_rf(pg_delay=0x34, tx_power=0xFEFEFEFE, pg_count=0)
    stamp_uwb.set_antenna_delay(tx=16385, rx=16385)
    stamp_uwb.set_lna_pa(lna=True, pa=True)
    stamp_uwb.set_rx_after_tx_delay(0)
    stamp_uwb.set_rx_timeout(30000)
    sequence = 0


def loop():
    global \
        stamp_uwb, \
        poll_frame, \
        sequence, \
        status, \
        response, \
        expected_response, \
        poll_tx, \
        response_rx, \
        delayed_time, \
        delayed_time_even, \
        final_tx, \
        final_frame
    M5.update()
    try:
        stamp_uwb.force_trx_off()
        stamp_uwb.clear_status(uwb.STATUS_TX_DONE | uwb.STATUS_RX_ALL)
        poll_frame = bytearray(2)
        poll_frame[0] = 1
        poll_frame[1] = sequence
        stamp_uwb.write_tx_frame(poll_frame, True)
        stamp_uwb.start_tx(uwb.TX_IMMEDIATE | uwb.RESPONSE_EXPECTED)
        status = stamp_uwb.wait_status(uwb.STATUS_RX_ALL, 50)
        if not (status & uwb.STATUS_RX_GOOD):
            print("response timeout")
            time.sleep_ms(200)
        else:
            response = stamp_uwb.read_rx_frame()
            expected_response = bytearray(2)
            expected_response[0] = 2
            expected_response[1] = sequence
            if response != expected_response:
                print("invalid response")
                time.sleep_ms(200)
            else:
                poll_tx = stamp_uwb.tx_timestamp()
                response_rx = stamp_uwb.rx_timestamp()
                delayed_time = response_rx + 10000 * 63898 >> 8
                delayed_time_even = delayed_time & 0xFFFFFFFE
                final_tx = (delayed_time_even << 8) + 16385
                final_frame = struct.pack(
                    "<BBIII",
                    3,
                    sequence,
                    poll_tx & 0xFFFFFFFF,
                    response_rx & 0xFFFFFFFF,
                    final_tx & 0xFFFFFFFF,
                )
                stamp_uwb.clear_status(uwb.STATUS_TX_DONE | uwb.STATUS_RX_ALL)
                stamp_uwb.set_delayed_trx_time(delayed_time)
                stamp_uwb.write_tx_frame(final_frame, True)
                stamp_uwb.start_tx(uwb.TX_DELAYED)
                status = stamp_uwb.wait_status(uwb.STATUS_TX_DONE, 30)
                stamp_uwb.clear_status(uwb.STATUS_TX_DONE)
                print((str("final sent, sequence=") + str(sequence)))
                sequence = sequence + 1 & 0xFF
    except:
        print("ranging retry")
        stamp_uwb.force_trx_off()
        stamp_uwb.clear_status(uwb.STATUS_TX_DONE | uwb.STATUS_RX_ALL)

    time.sleep_ms(200)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
