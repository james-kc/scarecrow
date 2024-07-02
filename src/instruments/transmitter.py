#!/usr/bin/python
# -*- coding: UTF-8 -*-

#
#    this is an UART-LoRa device and thers is an firmware on Module
#    users can transfer or receive the data directly by UART and dont
#    need to set parameters like coderate,spread factor,etc.
#    |============================================ |
#    |   It does not suport LoRaWAN protocol !!!   |
#    | ============================================|
#   
#    This script is mainly for Raspberry Pi 3B+, 4B, and Zero series
#    Since PC/Laptop does not have GPIO to control HAT, it should be configured by
#    GUI and while setting the jumpers, 
#    Please refer to another script pc_main.py
#

import sys
import sx126x
import threading
import time
import select
import termios
import tty
from threading import Timer


#
#    Need to disable the serial login shell and have to enable serial interface 
#    command `sudo raspi-config`
#    More details: see https://github.com/MithunHub/LoRa/blob/main/Basic%20Instruction.md
#
#    When the LoRaHAT is attached to RPi, the M0 and M1 jumpers of HAT should be removed.
#


#   serial_num
#       PiZero, Pi3B+, and Pi4B use "/dev/ttyS0"
#
#    Frequency is [850 to 930], or [410 to 493] MHz
#
#    address is 0 to 65535
#        under the same frequence,if set 65535,the node can receive 
#        messages from another node of address is 0 to 65534 and similarly,
#        the address 0 to 65534 of node can receive messages while 
#        the another note of address is 65535 sends.
#        otherwise two node must be same the address and frequence
#
#    The tramsmit power is {10, 13, 17, and 22} dBm
#
#    RSSI (receive signal strength indicator) is {True or False}
#        It will print the RSSI value when it receives each message
#

node = sx126x.sx126x(
    serial_num="/dev/ttyS0",
    freq=868,
    addr=0,
    power=22,
    rssi=True,
    air_speed=2400,
    relay=False
)

def send_deal():
    get_rec = ""
    print("")
    print("input a string such as \033[1;32m0,868,Hello World\033[0m,it will send `Hello World` to lora node device of address 0 with 868M ")
    print("please input and press Enter key:",end='',flush=True)

    while True:
        rec = sys.stdin.read(1)
        if rec != None:
            if rec == '\x0a': break
            get_rec += rec
            sys.stdout.write(rec)
            sys.stdout.flush()

    get_t = get_rec.split(",")

    offset_frequence = int(get_t[1])-(850 if int(get_t[1])>850 else 410)
    #
    # the sending message format
    #
    #         receiving node              receiving node                   receiving node           own high 8bit           own low 8bit                 own 
    #         high 8bit address           low 8bit address                    frequency                address                 address                  frequency             message payload
    data = bytes([int(get_t[0])>>8]) + bytes([int(get_t[0])&0xff]) + bytes([offset_frequence]) + bytes([node.addr>>8]) + bytes([node.addr&0xff]) + bytes([node.offset_freq]) + get_t[2].encode()

    node.send(data)
    print('\x1b[2A',end='\r')
    print(" "*200)
    print(" "*200)
    print(" "*200)
    print('\x1b[3A',end='\r')

def send_message(message):
    data = bytes([0>>8]) + bytes([0&0xff]) + bytes([18]) + bytes([0>>8]) + bytes([0&0xff]) + bytes([node.offset_freq]) + message.encode()
    # data = bytes([255]) + bytes([255]) + bytes([18]) + bytes([255]) + bytes([255]) + bytes([12]) + str(message).encode()
    node.send(data)

def main():
    for i in range(15):
        message = f"Message {i}"
        print(f"Sending: {message}")
        send_message(message)

if __name__ == '__main__':
    main()
