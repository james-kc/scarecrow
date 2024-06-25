from picamera2 import Picamera2
import time
from datetime import datetime

IMG_DIR = 'images'

def initialise_camera():
    """Function used to initialise the Mini Camera Module.
    """

    picam2 = Picamera2()

    # Ensuring highest jpeg quality with no compression (fastest)
    picam2.options["quality"] = 95
    picam2.options["compress_level"] = 0

    # Setting resolution for output images
    config = picam2.create_still_configuration(
        main={"size": (2592, 1944)}
    )
    picam2.configure(config)
    picam2.start()

    return picam2

def capture_image():
    picam2.capture_file(
        f"{IMG_DIR}/{(dt_filename := datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))}.png"
    )

def main():
    picam2 = Picamera2()

    config = picam2.create_still_configuration(
        main={"size": (2592, 1944)}
    )

    # Capture 3 images. Use a 0.5 second delay after the first image.
    picam2.start_and_capture_files(
        IMG_DIR + "/test{:d}.jpg",
        num_files=1,
        delay=0.5,
        show_preview=False,
        preview_mode=config
    )


if __name__ == '__main__':
    main()
