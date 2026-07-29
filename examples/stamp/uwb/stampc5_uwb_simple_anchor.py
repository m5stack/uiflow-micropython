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
import math


stamp_uwb = None
status = None
sequence = None
poll = None
poll_rx = None
response_frame = None
final_frame = None
response_tx = None
final_rx = None
round_a = None
round_b = None
delay_a = None
response_rx = None
poll_tx = None
delay_b = None
denominator = None
final_tx = None
tof_dtu = None
distance = None
display_distance = None


def setup():
    global \
        stamp_uwb, \
        status, \
        sequence, \
        poll, \
        poll_rx, \
        response_frame, \
        final_frame, \
        response_tx, \
        final_rx, \
        round_a, \
        round_b, \
        delay_a, \
        response_rx, \
        poll_tx, \
        delay_b, \
        denominator, \
        final_tx, \
        tof_dtu, \
        distance, \
        display_distance

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
    stamp_uwb.set_rx_timeout(30000)
    sequence = 0


def loop():
    global \
        stamp_uwb, \
        status, \
        sequence, \
        poll, \
        poll_rx, \
        response_frame, \
        final_frame, \
        response_tx, \
        final_rx, \
        round_a, \
        round_b, \
        delay_a, \
        response_rx, \
        poll_tx, \
        delay_b, \
        denominator, \
        final_tx, \
        tof_dtu, \
        distance, \
        display_distance
    M5.update()
    try:
        stamp_uwb.force_trx_off()
        stamp_uwb.clear_status(uwb.STATUS_TX_DONE | uwb.STATUS_RX_ALL)
        stamp_uwb.rx_enable(uwb.RX_IMMEDIATE)
        status = stamp_uwb.wait_status(uwb.STATUS_RX_ALL, 50)
        if status & uwb.STATUS_RX_GOOD:
            poll = stamp_uwb.read_rx_frame()
            if len(poll) == 2 and poll[0] == 1:
                sequence = poll[1]
                poll_rx = stamp_uwb.rx_timestamp() & 0xFFFFFFFF
                stamp_uwb.clear_status(uwb.STATUS_TX_DONE | uwb.STATUS_RX_ALL)
                stamp_uwb.set_rx_after_tx_delay(0)
                response_frame = bytearray(2)
                response_frame[0] = 2
                response_frame[1] = sequence
                stamp_uwb.write_tx_frame(response_frame, True)
                stamp_uwb.start_tx(uwb.TX_IMMEDIATE | uwb.RESPONSE_EXPECTED)
                status = stamp_uwb.wait_status(uwb.STATUS_RX_ALL, 50)
                if status & uwb.STATUS_RX_GOOD:
                    final_frame = stamp_uwb.read_rx_frame()
                    if (
                        len(final_frame) == 14
                        and final_frame[0] == 3
                        and final_frame[1] == sequence
                    ):
                        response_tx = stamp_uwb.tx_timestamp() & 0xFFFFFFFF
                        final_rx = stamp_uwb.rx_timestamp() & 0xFFFFFFFF
                        poll_tx, response_rx, final_tx = struct.unpack_from("<III", final_frame, 2)
                        round_a = response_rx - poll_tx & 0xFFFFFFFF
                        round_b = final_rx - response_tx & 0xFFFFFFFF
                        delay_a = final_tx - response_rx & 0xFFFFFFFF
                        delay_b = response_tx - poll_rx & 0xFFFFFFFF
                        denominator = (round_a + round_b) + (delay_a + delay_b)
                        if denominator != 0:
                            tof_dtu = (round_a * round_b - delay_a * delay_b) / denominator
                            distance = math.fabs((tof_dtu * (1 / (499200000 * 128))) * 299702547)
                            display_distance = round(distance * 100) / 100
                            if distance >= 0 and distance <= 100:
                                print(
                                    (
                                        str(
                                            (
                                                str(
                                                    (
                                                        str((str("sequence=") + str(sequence)))
                                                        + str(" distance=")
                                                    )
                                                )
                                                + str(display_distance)
                                            )
                                        )
                                        + str(" m")
                                    )
                                )
                            else:
                                print((str("invalid distance: ") + str(distance)))
                    else:
                        print("invalid final")
                else:
                    print("final timeout")
    except:
        print("ranging retry")
        stamp_uwb.force_trx_off()
        stamp_uwb.clear_status(uwb.STATUS_TX_DONE | uwb.STATUS_RX_ALL)

    time.sleep_ms(10)


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
