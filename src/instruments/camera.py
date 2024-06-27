from picamera2 import Picamera2
import time
from datetime import datetime

IMG_DIR = 'images'

def initialise_camera():
    """Function used to initialise the Mini Camera Module."""
    picam2 = Picamera2()
    config = picam2.create_still_configuration(main={"size": (2592, 1944)})
    picam2.configure(config)
    picam2.start()
    return picam2

def capture_image(picam2):
    """Capture an image and save it with a timestamp."""
    filename = f"{IMG_DIR}/{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}.png"
    picam2.capture_file(filename)
    print(f"Image captured: {filename}")

def power_down_camera(picam2):
    """Power down the camera."""
    picam2.stop()
    picam2.close()
    print("Camera powered down.")

def main():
    picam2 = initialise_camera()
    capture_image(picam2)


if __name__ == '__main__':
    main()
