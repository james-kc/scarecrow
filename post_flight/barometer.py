import pandas as pd
import folium
from matplotlib import pyplot as plt

import scarecrow_tools as st

DATA_DIR = 'post_flight/data/barometer.csv'

def altitude_plot(df):
    st.plotter(df, 'timestamp', 'relative_altitude')

def main():
    df = pd.read_csv(DATA_DIR)
    altitude_plot(df)
    plt.show()

    
if __name__ == '__main__':
    main()