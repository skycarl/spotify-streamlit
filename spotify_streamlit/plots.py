import streamlit as st
import pandas as pd
import plotly.express as px


def top_artists(df, time_unit):
    """Bar chart of top artists"""

    fig = px.bar(df[:10], x='artistName', y=time_unit, labels={'artistName': 'Artist', time_unit: time_unit})
    fig.update_layout(
        title='Top artists',
        xaxis_title='Artist',
        yaxis_title=time_unit,
        showlegend=False
    )

    # Plot!
    st.subheader('Who did you listen to the most?')
    st.plotly_chart(fig, use_container_width=True)
    st.write('The simple history doesn\'t delineate between music and other types of content (like podcasts, audiobooks, or white noise). Want to ignore any artists to get a clearer picture? Use the dropdown in the sidebar to filter out artists by name.')

def top_artists_with_multiselect(artists, time_unit):
    """Bar chart of top artists with a multiselect widget to ignore artists"""
    # Create a placeholder for the plot
    plot_placeholder = st.empty()

    options = st.multiselect(
        'Select artists to ignore',
        artists['artistName'],
        placeholder='Select artists',
        help='Artists to ignore in the analysis; may be helpful if you listened to podcasts, white noise, etc',
    )

    # Check if options are selected and filter the DataFrame
    if options:
        artists_filtered = artists[~artists['artistName'].isin(options)]
        # Display the plot with filtered data
        with plot_placeholder.container():
            top_artists(artists_filtered, time_unit)
    else:
        # Display the initial plot if no options are selected
        with plot_placeholder.container():
            top_artists(artists, time_unit)


@st.cache_data
def time_of_day_distribution(df):
    """Histogram of time of day distribution"""

    end_times = df['endTime'].dt.hour
    fig = px.histogram(end_times, nbins=24, labels={'value': 'Hour (UTC)'})
    fig.update_layout(
        title='Listens by hour of day',
        xaxis_title='Hour (UTC)',
        yaxis_title='Number of listens',
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=2
        ),
        showlegend=False
    )

    # Plot!
    st.subheader('When were you listening?')
    st.plotly_chart(fig, use_container_width=True)
    st.write('Spotify records when each stream ends in [Coordinated Universal Time (UTC)](https://support.spotify.com/us/article/understanding-my-data/). Adjust the time zone in the sidebar to see when you were listening in your local time zone.')


def top_songs(df, time_unit):
    """Bar chart of top songs"""

    fig = px.bar(df[:10], x='trackName', y=time_unit, labels={'trackName': 'Song', time_unit: time_unit})
    fig.update_layout(
        title='Top songs',
        xaxis_title='Song',
        yaxis_title=time_unit,
        showlegend=False
    )

    # Plot!
    st.subheader('What did you listen to the most?')
    st.plotly_chart(fig, use_container_width=True)
    st.write('If you listened to white noise or similar, you might have some tracks that you want to ignore.')


def top_songs_with_multiselect(songs, time_unit):
    """Bar chart of top songs with a multiselect widget to ignore specific songs"""
    # Create a placeholder for the plot
    plot_placeholder = st.empty()

    options = st.multiselect(
        'Select tracks to ignore',
        songs['trackName'],
        placeholder='Select songs',
        help='Songs to ignore in the analysis; may be helpful if you listened to white noise, etc.',
    )

    # Check if options are selected and filter the DataFrame
    if options:
        songs_filtered = songs[~songs['trackName'].isin(options)]
        # Display the plot with filtered data
        with plot_placeholder.container():
            top_songs(songs_filtered, time_unit)

    else:
        # Display the initial plot if no options are selected
        with plot_placeholder.container():
            top_songs(songs, time_unit)


# Weekly listening time
def weekly_listening_time(df, time_unit):
    """Line chart of weekly listening time"""

    # Set 'endTime' as the index and resample to weekly frequency
    df = df.set_index('endTime')
    df_weekly = df.resample('W-MON')[time_unit].sum().reset_index()
    df_weekly.columns = ['week', time_unit]

    # Convert 'week' to string format
    df_weekly['week'] = df_weekly['week'].dt.strftime('%Y-%m-%d')

    fig = px.line(df_weekly, x='week', y=time_unit, labels={'week': 'Week', time_unit: time_unit})
    fig.update_layout(
        title='Weekly listening time',
        xaxis_title='Week',
        yaxis_title=time_unit,
        showlegend=False
    )

    # Plot!
    st.subheader('How did your listening change over time?')
    st.plotly_chart(fig, use_container_width=True)

# Daily listening time heatmap
import plotly.graph_objects as go

def daily_listening_time_heatmap(df, time_unit):
    """Heatmap of daily listening time"""

    # Convert 'endTime' to datetime if it's not already
    df['endTime'] = pd.to_datetime(df['endTime'])

    # Extract day of week and week of year
    df['day_of_week'] = df['endTime'].dt.day_name()
    df['week_of_year'] = df['endTime'].dt.to_period('W').apply(lambda r: r.start_time)

    # Specify the correct order of days
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=days, ordered=True)

    # Pivot to get matrix for heatmap
    df_pivot = df.pivot_table(index='day_of_week', columns='week_of_year', values=time_unit, aggfunc='sum')

    # Create heatmap with square boxes
    fig = go.Figure(data=go.Heatmap(
        z=df_pivot.values,
        x=df_pivot.columns,
        y=df_pivot.index,
        colorscale='Viridis',
        xgap=1, # this
        ygap=1, # and this is used to make the grid squares
    ))

    fig.update_layout(
        title='Daily listening time',
        xaxis_title='Week of Year',
        yaxis_title='Day of Week',
        showlegend=False
    )

    # Plot!
    st.plotly_chart(fig, use_container_width=True)
    
    # Categorical histogram for day of week
