#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import sx126x
import time

# Initialize the node
node = sx126x.sx126x(
    serial_num="/dev/ttyAMA0",
    freq=868,
    addr=0,
    power=22,
    rssi=True,
    air_speed=2400,
    relay=False
)

def main():
    try:
        while True:
            received_data = node.receive()
            if received_data:
                # Assuming the data format: [receiving address (2 bytes), offset frequency (1 byte), own address (2 bytes), own offset frequency (1 byte), message (remaining bytes)]
                if len(received_data) < 6:
                    print("Received data is too short, ignoring.")
                    continue

                receiving_address = (received_data[0] << 8) + received_data[1]
                offset_frequency = received_data[2]
                own_address = (received_data[3] << 8) + received_data[4]
                own_offset_frequency = received_data[5]
                message = received_data[6:]

                # Calculate the frequency
                frequency = 850 + offset_frequency if offset_frequency < 80 else 410 + offset_frequency

                # Decode the message
                try:
                    message_decoded = message.decode('utf-8')
                except UnicodeDecodeError:
                    print("Error decoding message. Invalid byte sequence.")
                    message_decoded = str(message)

                print(f"Received from address {receiving_address}, frequency {frequency} MHz:")
                print(f"Message: {message_decoded}")
                if node.rssi:
                    print(f"RSSI: {node.last_rssi} dBm")

    except Exception as e:
        print(f"Exception: {e}")
        node.close_serial()

if __name__ == '__main__':
    main()
