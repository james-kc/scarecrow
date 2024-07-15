import serial
import time

# Setup serial connection
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

while True:
    if ser.in_waiting > 0:
        # Read data from serial
        sensor_data = ser.readline().decode('utf-8').strip()
        if sensor_data:
            print(f"Received: {sensor_data}")
        else:
            print("Got no milk")
    time.sleep(0.1)  # Adjust the delay as needed
