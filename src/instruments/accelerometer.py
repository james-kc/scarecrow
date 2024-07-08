# Functions relating to the use of the accelerometer/gyroscope module LGA-14L
#
# Datasheet:
# https://www.mouser.co.uk/datasheet/2/744/en_DM00133076-2488588.pdf

import time
import board
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3

def initilise_accelerometer():
    """Function used to initialise the accelerometer module."""

    i2c = board.I2C()
    sensor = LSM6DS3(i2c)
    return sensor

def get_acceleration(sensor):
    return sensor.acceleration

def get_gyro(sensor):
    return sensor.gyro

def main():
    sensor = initilise_accelerometer()

    while True:
        # print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
        # print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (sensor.gyro))
        print(get_acceleration(sensor))
        print(get_gyro(sensor))
        print("")
        time.sleep(0.5)

if __name__ == '__main__':
    main()