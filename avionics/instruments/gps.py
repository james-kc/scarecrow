# Library found here: https://github.com/adafruit/Adafruit_CircuitPython_GPS/tree/main

import time
import board
import busio
from datetime import datetime

import adafruit_gps

from pprint import pprint

def initialise_gps():
    i2c = board.I2C()  # uses board.SCL and board.SDA

    # Create a GPS module instance.
    gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

    # Turn on the basic GGA and RMC info (what you typically want)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

    # Set update rate to once a second (1hz) which is what you typically want.
    gps.send_command(b"PMTK220,1000")

    return gps

def get_position(gps):
    gps.update()

    if not gps.has_fix:
        # Try again if we don't have a fix yet.
        datetime_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    else:
        datetime_str = "{}/{}/{} {:02}:{:02}:{:02}".format(
            gps.timestamp_utc.tm_mday,  # struct_time object that holds
            gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
            gps.timestamp_utc.tm_year,  # the fix time.  Note you might
            gps.timestamp_utc.tm_hour,  # not get all data like year, day,
            gps.timestamp_utc.tm_min,  # month!
            gps.timestamp_utc.tm_sec,
        )

    gps_data = {
        'datetime': datetime_str,
        'fix': gps.fix_quality,
        'latitude': gps.latitude,
        'longitude': gps.longitude,
        'latitude_degrees': gps.latitude_degrees,
        'latitude_minutes': gps.latitude_minutes,
        'longitude_degrees': gps.longitude_degrees,
        'longitude_minutes': gps.longitude_minutes,
        'satellites': gps.satellites,
        'altitude_m': gps.altitude_m,
        'speed_knots': gps.speed_knots,
        'track_angle_deg': gps.track_angle_deg,
        'horizontal_dilution': gps.horizontal_dilution,
        'height_geoid': gps.height_geoid
    }

    return gps_data, gps.has_fix

def main():
    gps = initialise_gps()
    while True:
        gps_data = get_position(gps)
        pprint(gps_data)

if __name__ == '__main__':
    main()
