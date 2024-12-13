import streamlit as st
import pandas as pd

def page_1():
    st.title("Page 1")

def page_2():
    st.title("Page 2")


pages = {
    "Main Page": [
        st.Page("pages/main_page.py", title="Main Page"),
        st.Page("pages/df_preview.py", title="df_preview")
    ],
    "Other Pages": [
        st.Page(page_1),
        st.Page(page_2)
    ]
}

pg = st.navigation(pages)
pg.run()