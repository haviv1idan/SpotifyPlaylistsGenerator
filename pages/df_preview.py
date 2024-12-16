import streamlit as st

from src.utils import df

st.title("df_preview")

st.dataframe(df[:100])
