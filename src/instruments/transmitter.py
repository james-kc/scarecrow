import serial
import time

# Replace with the correct serial port name
serial_port = '/dev/serial0'
baud_rate = 9600

ser = serial.Serial(serial_port, baud_rate)

while True:
    data_to_send = "Hello from PC"
    ser.write(data_to_send.encode('utf-8'))
    print(f"Sent: {data_to_send}")
    time.sleep(1)
