from matplotlib import pyplot as plt
import pandas as pd

def data_trimmer(df: pd.DataFrame, datetime: str, trim: str):

    if trim not in ['flight', 'ascent', 'all']:
        raise ValueError("Argument trim must be one of ['flight', 'ascent', 'all']")

    if trim == 'flight':
        # Define the time range
        start_time = pd.to_datetime('12/07/2024 19:44:00', format='%d/%m/%Y %H:%M:%S')
        end_time = pd.to_datetime('12/07/2024 19:46:42', format='%d/%m/%Y %H:%M:%S')

        # Filter the DataFrame to only include rows within the time range
        return df[(df[datetime] >= start_time) & (df[datetime] <= end_time)]

    elif trim == 'ascent':
        # Define the time range
        start_time = pd.to_datetime('12/07/2024 19:44:00', format='%d/%m/%Y %H:%M:%S')
        end_time = pd.to_datetime('12/07/2024 19:44:20', format='%d/%m/%Y %H:%M:%S')

        # Filter the DataFrame to only include rows within the time range
        return df[(df[datetime] >= start_time) & (df[datetime] <= end_time)]

    elif trim == 'all':
        return df

def plotter(
        df: pd.DataFrame,
        datetime: str,
        y: str,
        trim: str = 'flight'
    ):
    # Convert 'thread_datetime' to datetime
    df[datetime] = pd.to_datetime(df[datetime], format='%d/%m/%Y %H:%M:%S.%f')

    df_filtered = data_trimmer(df, datetime, trim)

    plt.plot(df_filtered[datetime], df_filtered[y], 'k')
    plt.xlabel(datetime)
    plt.ylabel(y)

def multi_ax_plotter(
        df: pd.DataFrame,
        datetime: str,
        y1: str,
        y2: str,
        trim: bool = 'flight'
    ):
    # Convert 'thread_datetime' to datetime
    df[datetime] = pd.to_datetime(df[datetime], format='%d/%m/%Y %H:%M:%S.%f')

    df_filtered = data_trimmer(df, datetime, trim)

    fig, ax1 = plt.subplots()

    ax1.plot(df_filtered[datetime], df_filtered[y1], 'g')
    ax1.set_ylabel(y1, color='g')

    ax2 = ax1.twinx()
    ax2.plot(df_filtered[datetime], df_filtered[y2], 'k')
    ax2.set_ylabel(y2, color='k')


def multi_line_plotter(
        df: pd.DataFrame,
        datetime: str,
        y: [str],
        trim: str = 'flight'
    ):
    # Convert 'thread_datetime' to datetime
    df[datetime] = pd.to_datetime(df[datetime], format='%d/%m/%Y %H:%M:%S.%f')

    df_filtered = data_trimmer(df, datetime, trim)

    for line in y:
        plt.plot(df_filtered[datetime], df_filtered[line], label=line)
    
    plt.legend()