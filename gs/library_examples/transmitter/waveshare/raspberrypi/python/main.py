#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import sx126x
import threading
import time
import select
import termios
import tty
from threading import Timer

old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())

def get_cpu_temp():
    with open("/sys/class/thermal/thermal_zone0/temp") as tempFile:
        cpu_temp = tempFile.read()
    return float(cpu_temp) / 1000

node = sx126x.sx126x(serial_num="/dev/ttyAMA0", freq=868, addr=0, power=22, rssi=True, air_speed=2400, relay=False)

def send_deal():
    get_rec = ""
    print("\nInput a string such as \033[1;32m0,868,Hello World\033[0m, it will send `Hello World` to LoRa node device of address 0 with 868 MHz")
    print("Please input and press Enter key:", end='', flush=True)

    while True:
        rec = sys.stdin.read(1)
        if rec:
            if rec == '\n': break
            get_rec += rec
            sys.stdout.write(rec)
            sys.stdout.flush()

    get_t = get_rec.split(",")

    try:
        address = int(get_t[0])
        frequency = int(get_t[1])
        message = get_t[2]
    except ValueError:
        print("Invalid input. Please use the format address,frequency,message.")
        return

    if 850 <= frequency <= 930:
        offset_frequency = frequency - 850
    elif 410 <= frequency <= 493:
        offset_frequency = frequency - 410
    else:
        print("Invalid frequency. Please use a frequency between 850-930 MHz or 410-493 MHz.")
        return

    print(f"Sending to address: {address}, frequency: {frequency} MHz (offset: {offset_frequency})")
    
    data = (
        bytes([address >> 8]) +
        bytes([address & 0xff]) +
        bytes([offset_frequency]) +
        bytes([node.addr >> 8]) +
        bytes([node.addr & 0xff]) +
        bytes([node.offset_freq]) +
        message.encode('utf-8')
    )

    node.send(data)
    print('\x1b[2A', end='\r')
    print(" " * 200)
    print(" " * 200)
    print(" " * 200)
    print('\x1b[3A', end='\r')

def send_cpu_continue(continue_or_not=True):
    if continue_or_not:
        global timer_task
        global seconds
        data = (
            bytes([255]) +
            bytes([255]) +
            bytes([18]) +
            bytes([255]) +
            bytes([255]) +
            bytes([12]) +
            "CPU Temperature:".encode() +
            str(get_cpu_temp()).encode() +
            " C".encode()
        )
        node.send(data)
        time.sleep(0.2)
        timer_task = Timer(seconds, send_cpu_continue)
        timer_task.start()
    else:
        data = (
            bytes([255]) +
            bytes([255]) +
            bytes([18]) +
            bytes([255]) +
            bytes([255]) +
            bytes([12]) +
            "CPU Temperature:".encode() +
            str(get_cpu_temp()).encode() +
            " C".encode()
        )
        node.send(data)
        time.sleep(0.2)
        timer_task.cancel()

try:
    time.sleep(1)
    print("Press \033[1;32mEsc\033[0m to exit")
    print("Press \033[1;32mi\033[0m to send")
    print("Press \033[1;32ms\033[0m to send CPU temperature every 10 seconds")
    
    seconds = 10
    
    while True:
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            c = sys.stdin.read(1)
            if c == '\x1b': break
            if c == '\x69':
                send_deal()
            if c == '\x73':
                print("Press \033[1;32mc\033[0m to exit the send task")
                timer_task = Timer(seconds, send_cpu_continue)
                timer_task.start()
                while True:
                    if sys.stdin.read(1) == '\x63':
                        timer_task.cancel()
                        print('\x1b[1A', end='\r')
                        print(" " * 100)
                        print('\x1b[1A', end='\r')
                        break
            sys.stdout.flush()
        node.receive()
except Exception as e:
    print(f"An error occurred: {e}")
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
