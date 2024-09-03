import pandas as pd
from pandas import DataFrame
import folium
from matplotlib import pyplot as plt

import scarecrow_tools as st

DATA_DIR = 'post_flight/data/gps.csv'

def make_map(df):

    # Convert 'thread_datetime' to datetime
    df['thread_datetime'] = pd.to_datetime(df['thread_datetime'], format='%d/%m/%Y %H:%M:%S.%f')

    # Filter the DataFrame to only include rows within the time range
    df_filtered = st.data_trimmer(df, 'thread_datetime', 'all')

    # Extract the relevant latitude and longitude columns, filtering out rows with NaN values
    coordinates = df_filtered[['latitude', 'longitude']].dropna().values

    # Create a map centered at the first coordinate with a satellite tile layer
    map = folium.Map(location=[coordinates[0][0], coordinates[0][1]], zoom_start=10)

    # Add a satellite tile layer with the necessary attribution
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri, Maxar, Earthstar Geographics, and the GIS User Community',
        name='Esri Satellite',
        overlay=False,
        control=True
    ).add_to(map)

    # Add a PolyLine to connect the coordinates
    folium.PolyLine(coordinates, color="blue", weight=2.5, opacity=1).add_to(map)

    # Save the map as an HTML file
    map.save("map.html")

    # Display the map
    map

def altitude_plot(df):
    st.plotter(df, 'thread_datetime', 'altitude_m', 'all')

def speed_plot(df):
    df['speed_m/s'] = df['speed_knots'] * 1.94384
    st.plotter(df, 'thread_datetime', 'speed_m/s')

def speed_altitude_plot(df):
    df['speed_m/s'] = df['speed_knots'] * 1.94384
    st.multi_ax_plotter(df, 'thread_datetime', 'altitude_m', 'speed_m/s', 'flight')

def main():
    # Read the data into a pandas DataFrame
    df = pd.read_csv(DATA_DIR)

    make_map(df)
    # altitude_plot(df)
    # speed_plot(df)
    # speed_altitude_plot(df)
    # plt.show()
    


if __name__ == '__main__':
    main()