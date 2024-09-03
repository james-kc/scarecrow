import pandas as pd
import folium
from matplotlib import pyplot as plt

import scarecrow_tools as st

DATA_DIR = 'post_flight/data/barometer.csv'

def altitude_plot(df):
    st.plotter(df, 'timestamp', 'relative_altitude')

def altitude_velocity_plot(df):
    # Ensure the timestamp column is correctly converted to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y %H:%M:%S.%f')

    # Remove sequential duplicate altitude values
    df = df[df['relative_altitude'].shift() != df['relative_altitude']]

    # Calculate time differences in seconds
    df['time_diff'] = df['timestamp'].diff().dt.total_seconds()

    # Calculate altitude differences
    df['altitude_diff'] = df['relative_altitude'].diff()

    # Compute vertical velocity
    df['vertical_velocity'] = df['altitude_diff'] / df['time_diff']

    # Calculate velocity differences
    df['velocity_diff'] = df['vertical_velocity'].diff()

    # Compute vertical acceleration
    df['vertical_acceleration'] = df['velocity_diff'] / df['time_diff']

    st.multi_ax_plotter(
        df, 'timestamp', 'vertical_acceleration', 'vertical_velocity'
    )


def main():
    df = pd.read_csv(DATA_DIR)
    # altitude_plot(df)
    altitude_velocity_plot(df)
    plt.show()

    
if __name__ == '__main__':
    main()
