# Library found here https://github.com/pimoroni/bme280-python

import time
from smbus2 import SMBus
from bme280 import BME280


def initialise_bme280():
    # Initialise the BME280
    bus = SMBus(1)
    bme280 = BME280(i2c_dev=bus)

    baseline_values = []
    baseline_size = 100

    print(f"Collecting baseline values for {baseline_size:d} seconds. Do not move the sensor!\n")

    # Collect some values to calculate a baseline pressure
    for i in range(baseline_size):
        pressure = bme280.get_pressure()
        baseline_values.append(pressure)
        time.sleep(1)

    # Calculate average baseline
    # baseline = sum(baseline_values[:-25]) / len(baseline_values[:-25])
    baseline = sum(baseline_values) / len(baseline_values)

    return bme280, baseline

def get_temperature(bme280):
    return bme280.get_temperature()

def get_pressure(bme280):
    return bme280.get_pressure()

def get_humidity(bme280):
    return bme280.get_humidity()

def get_relative_altitude(bme280, baseline):
    return bme280.get_altitude(qnh=baseline)

def main():
    bme280, baseline = initialise_bme280()

    while True:
        altitude = get_relative_altitude(bme280, baseline)
        temperature = get_temperature(bme280)
        pressure = get_pressure(bme280)
        humidity = get_humidity(bme280)

        # print(f"Relative altitude: {altitude:05.2f} metres")
        print(
            f"Relative altitude: {altitude:05.2f} m\n"
            f"Temperature: {temperature:05.2f}°C\n"
            f"Pressure: {pressure:05.2f}hPa\n"
            f"Humidity: {humidity:05.2f}%\n"
        )
        time.sleep(1)

if __name__ == "__main__":
    main()
