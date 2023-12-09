import streamlit as st
import pandas as pd
import utils
import plots
import components
import constants


path = '/Users/skylercarlson/Library/CloudStorage/OneDrive-Personal/Data/Spotify/Spotify Account Data/StreamingHistory0.json'

st.set_page_config(page_title='Spotify Unwrapped',
                   page_icon='media/favicon.png',
                   layout='centered',
                   initial_sidebar_state='expanded')

# Define sidebar
with st.sidebar:
    st.write('Upload your Spotify streaming history (`StreamingHistory*.json`)')
    st.write('How to download your Spotify streaming history (link)')
    file = st.file_uploader('Select a file', type='json')
    time_unit = components.select_time_unit()

    st.divider()
    st.write('**Filter by date**')
    date_help_str = 'Select a date range to filter your streaming history'
    st.date_input('Start date', value=None, help=date_help_str)
    st.date_input('End date', value=None, help=date_help_str)
    st.divider()

    #st.write('You selected:', options)


    # Radio button to filter for music or podcasts
    media_type_filter = st.radio('Filter for music or podcasts', ['Both', 'Music', 'Podcasts'])

#if uploaded_file is not None:
@st.cache_data
def preprocess_history(path, time_unit):
    # Read the json file into a DataFrame   
    history = utils.read_history(path)
    
    # Determine file type: abridged history or full
    df = pd.DataFrame(history)

    # TODO filter by date filter in sidebar

    # Convert msPlayed to the selected time unit
    df[time_unit] = df['msPlayed'] / constants.CONVERSION_FACTORS[time_unit]
    df = df.drop(columns='msPlayed')
    return df

@st.cache_data
def get_artists(df, time_unit):
    # Determine unique artists and sum the time_unit for each artist
    df_artists = df[['artistName', time_unit]].groupby('artistName').sum().reset_index()
    df_artists.columns = ['artistName', time_unit]
    df_artists = df_artists.sort_values(time_unit, ascending=False)
    return df_artists.reset_index(drop=True)
    

@st.cache_data
def get_songs(df, time_unit):
    # Group df by songs, summing time_unit column for each song and counting the number of times each song was played
    df_songs = df[['artistName', 'trackName', time_unit]].groupby(['artistName', 'trackName']).agg({time_unit: ['sum', 'count']}).reset_index()
    df_songs.columns = ['artistName', 'trackName', time_unit, 'count']
    df_songs = df_songs.sort_values(time_unit, ascending=False)
    return df_songs.reset_index(drop=True)


df = preprocess_history(path, time_unit)
artists = get_artists(df, time_unit)
songs = get_songs(df, time_unit)

# Write the stats header
components.header(df, songs, time_unit)

# Plots
plots.time_of_day_distribution(df)
plots.top_artists_with_multiselect(artists, time_unit)
plots.top_songs_with_multiselect(songs, time_unit)
plots.weekly_listening_time(df, time_unit)
plots.daily_listening_time_heatmap(df, time_unit)


# DataFrames at the end
st.title('View and download processed data')
components.write_and_make_downloadable(songs, 'Songs')
components.write_and_make_downloadable(artists, 'Artists')
components.write_and_make_downloadable(df, 'Full history')


