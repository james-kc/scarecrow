import serial

# Replace with the correct serial port name
serial_port = '/dev/ttyS0'
baud_rate = 9600

ser = serial.Serial(serial_port, baud_rate)

while True:
    if ser.in_waiting > 0:
        received_data = ser.read(ser.in_waiting).decode('utf-8')
        print(f"Received: {received_data}")
