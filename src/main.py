import threading
from datetime import datetime
import time
import os
import csv
from instruments import camera, gps, barometer, accelerometer, gps

DATA_PATH = 'data'
# Begin by creating session folder in /data
current_datetime = datetime.now().strftime('%Y%m%dT%H%M%S')
SESSION_DATA_PATH = f"{DATA_PATH}/{current_datetime}"
os.makedirs(SESSION_DATA_PATH, exist_ok=True)

def image_capture_thread(start_event, stop_event):
    picam2 = None
    with open(f"{SESSION_DATA_PATH}/image_capture.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'image_path'])
        
        while not stop_event.is_set():
            if start_event.is_set():
                if picam2 is None:
                    picam2 = camera.initialise_camera()
                image_path = camera.capture_image(picam2)
                writer.writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"), image_path])
                file.flush()
                time.sleep(1)  # Capture image every 1 second
            else:
                if picam2 is not None:
                    camera.power_down_camera(picam2)
                    picam2 = None

def barometer_thread(start_event, stop_event):
    barometer_obj = None
    with open(f"{SESSION_DATA_PATH}/barometer.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'relative_altitude'])

        while not stop_event.is_set():
            if start_event.is_set():
                if not barometer_obj:
                    barometer_obj, baseline = barometer.initialise_bme280()
                relative_altitude = barometer.get_relative_altitude(barometer_obj, baseline)
                writer.writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"), relative_altitude])
                file.flush()
                time.sleep(0.05)  # Read sensors and transmit data every 0.5 seconds

def accel_thread(start_event, stop_event):
    accel_obj = None
    with open(f"{SESSION_DATA_PATH}/accelerometer.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z'])

        while not stop_event.is_set():
            if start_event.is_set():
                if not accel_obj:
                    accel_obj = accelerometer.initialise_accelerometer()
                accel_data = accelerometer.get_acceleration(accel_obj)
                gyro_data = accelerometer.get_gyro(accel_obj)
                writer.writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"), *accel_data, *gyro_data])
                file.flush()
                time.sleep(0.05)  # Read sensors and transmit data every 0.5 seconds

def gps_thread(start_event, stop_event):
    gps_obj = None
    with open(f"{SESSION_DATA_PATH}/gps.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'thread_datetime',
            'datetime',
            'fix',
            'latitude',
            'longitude',
            'latitude_degrees',
            'latitude_minutes',
            'longitude_degrees',
            'longitude_minutes',
            'satellites',
            'altitude_m',
            'speed_knots',
            'track_angle_deg',
            'horizontal_dilution',
            'height_geoid',
        ])

        while not stop_event.is_set():
            if start_event.is_set():
                if not gps_obj:
                    gps_obj = gps.initialise_gps()
                position = gps.get_position(gps_obj)
                writer.writerow([
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"),
                    position['datetime'],
                    position['fix'],
                    position['latitude'],
                    position['longitude'],
                    position['latitude_degrees'],
                    position['latitude_minutes'],
                    position['longitude_degrees'],
                    position['longitude_minutes'],
                    position['satellites'],
                    position['altitude_m'],
                    position['speed_knots'],
                    position['track_angle_deg'],
                    position['horizontal_dilution'],
                    position['height_geoid'],
                ])
                file.flush()
                time.sleep(0.05)  # Read sensors and transmit data every 0.5 seconds

def main():
    # Events to control the threads
    start_event = threading.Event()
    stop_event = threading.Event()
    thread_args = (start_event, stop_event)

    # Create and start threads for image capture and sensor reading
    threads = [
        threading.Thread(target=image_capture_thread, args=thread_args),
        threading.Thread(target=barometer_thread, args=thread_args),
        threading.Thread(target=accel_thread, args=thread_args),
        threading.Thread(target=gps_thread, args=thread_args)
    ]

    for thread in threads:
        thread.start()

    try:
        while True:
            # Simulate starting and stopping the threads
            command = input("Enter 'start' to start capturing, 'stop' to stop capturing, 'exit' to exit: ").strip().lower()
            if command == 'start':
                start_event.set()
                print("Capture started.")
            elif command == 'stop':
                start_event.clear()
                print("Capture stopped.")
            elif command == 'exit':
                stop_event.set()
                break
    finally:
        for thread in threads:
            thread.join()

if __name__ == '__main__':
    main()
