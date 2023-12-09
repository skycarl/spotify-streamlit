import json
import pandas as pd
import streamlit as st



@st.cache_data
def read_history(path):
    with open(path, 'r') as f:
        return json.load(f)

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def pretty_date(date):
    day = date.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    return date.strftime(f'%B {day}{suffix}, %Y')