import threading
import time
from instruments import camera, gps, barometer, accelerometer, gps


def image_capture_thread(start_event, stop_event):
    picam2 = None
    while not stop_event.is_set():
        if start_event.is_set():
            if picam2 is None:
                picam2 = camera.initialise_camera()
            camera.capture_image(picam2)
            time.sleep(1)  # Capture image every 1 second
        else:
            if picam2 is not None:
                camera.power_down_camera(picam2)
                picam2 = None

def barometer_thread(start_event, stop_event):
    barometer_obj = None

    while not stop_event.is_set():
        if start_event.is_set():

            if not barometer_obj:
                barometer_obj, baseline = barometer.initialise_bme280()

            relative_altitude = barometer.get_relative_altitude(
                barometer_obj,
                baseline
            )

            print(f"Relative Altitude: {relative_altitude:05.2f}")
            time.sleep(0.5)  # Read sensors and transmit data every 0.5 seconds

def accel_thread(start_event, stop_event):
    accel_obj = None

    while not stop_event.is_set():
        if start_event.is_set():

            if not accel:
                accel_obj = accelerometer.initialise_accelerometer()

            print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (accelerometer.get_acceleration(accel_obj)))
            print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (accelerometer.get_gyro(accel_obj)))
            time.sleep(0.5)  # Read sensors and transmit data every 0.5 seconds

def gps_thread(start_event, stop_event):
    gps_obj = None

    while not stop_event.is_set():
        if start_event.is_set():

            if not gps_obj:
                sensor = gps_obj.initialise_gps()

            pprint(gps.get_position(gps_obj))
            time.sleep(0.5)  # Read sensors and transmit data every 0.5 seconds

def main():

    # Events to control the threads
    start_event = threading.Event()
    stop_event = threading.Event()

    # Create and start threads for image capture and sensor reading
    threads = [
        threading.Thread(
            target=image_capture_thread, args=(start_event, stop_event)
        ),
        threading.Thread(
            target=barometer_thread, args=(start_event, stop_event)
        ),
        threading.Thread(
            target=accel_thread, args=(start_event, stop_event)
        ),
        threading.Thread(
            target=gps_thread, args=(start_event, stop_event)
        )
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
