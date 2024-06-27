import random
from datetime import datetime

def read_gps():
    """Simulate reading from a GPS."""
    # Replace with actual code to read from the GPS
    gps_data = {
        "datetime": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),
        "latitude": random.uniform(-90, 90),
        "longitude": random.uniform(-180, 180),
        "altitude": random.uniform(0, 10000)
    }
    print(f"GPS data: {gps_data}")
    return gps_data
