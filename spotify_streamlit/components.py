import streamlit as st
import pandas as pd
import constants
import utils

# Streamlit input for a selection box containing milliseconds, seconds, minutes, hours, and days
def select_time_unit():
    return st.selectbox(
        'Time units',
        constants.CONVERSION_FACTORS.keys(),
        help='Time unit to convert display time to')

def header(df, songs, time_unit):
    # Get dates of first and last listens in the history
    df['endTime'] = pd.to_datetime(df['endTime'])  # convert endTime to datetime
    start_date = df['endTime'].min()
    end_date = df['endTime'].max()
    time_duration = (end_date - start_date).total_seconds()*1e3 / constants.CONVERSION_FACTORS[time_unit]
    listening_sum = df[time_unit].sum()

    st.title(f'You listened to {round(songs[time_unit].sum(), 1):,.1f} {time_unit.lower()} of Spotify!', anchor=None, help=None)
    st.write(f'That equates to {100*(listening_sum/time_duration):.2f}% of the time between {utils.pretty_date(start_date)} and {utils.pretty_date(end_date)}.')


def ignore_artists_selector(df):
    # Ignore certain artists   
    return st.multiselect(
        'Select artists to ignore',
        df['artistName'],
        placeholder='Select artists',
        #on_change=st.rerun(),
        help='Artists to ignore in the analysis; may be helpful if you listened to podcasts, white noise, etc',
        )

def write_and_make_downloadable(df, name):
    st.subheader(name)
    st.write(df)
    st.download_button(
        "Download CSV",
        utils.convert_df(df),
        f'{name}.csv',
        "text/csv",
        key=f'download-{name}-csv'
    )
