import streamlit as st


pages = {
    "Your Account": [
        st.Page("pages/create_account.py", title="Create your account"),
        st.Page("pages/manage_account.py", title="Manage your account"),    
    ],
    "Main Page": [
        st.Page("pages/main_page.py", title="Main Page"),
        st.Page("pages/df_preview.py", title="df_preview"),
    ]
}

pg = st.navigation(pages)
pg.run()