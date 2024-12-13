import streamlit as st
import pandas as pd

from src.utils import df, get_artists

st.title('Songs filter')


options = st.multiselect("Select Artist", get_artists())
st.write("You selected:", options)


if options:
    filtered_df = df[df['artists'].fillna('Unknown').str.contains('|'.join(options))]
    filtered_df = filtered_df.drop_duplicates(subset=['spotify_id'])
    st.dataframe(data=filtered_df[['name', 'artists', 'spotify_id']])
                 