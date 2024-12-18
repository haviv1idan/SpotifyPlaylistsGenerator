import streamlit as st
from db_api import UsersAPI

users_api = UsersAPI()


def create_account():
    st.title("Create Account")
    st.text("Please fill in your details to create an account.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if username in users_api.get_all_user_names():
            st.error("Username already exists. Please choose another one.")
        elif password != confirm_password:
            st.error("Passwords do not match. Try again.")
        elif len(username) == 0 or len(password) == 0:
            st.error("Username and Password cannot be empty.")
        elif not isinstance(username, str) or not isinstance(password, str):
            st.error("Username and Password must be strings.")
        else:
            users_api.create_user(username, password)
            st.success("Account created successfully! You can now log in.")
            st.info("Go to the Login page from the sidebar.")
            st.switch_page(login)


def login():
    st.session_state['user'] = None
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users_api.get_all_user_names() and users_api.get_user_by_name(username)['password'] == password:
            st.success(f"Welcome, {username}!")
            st.write("You are logged in.")
            st.session_state['user'] = username
            st.write("session_state:", st.session_state)
            st.switch_page(st.Page(main))
        else:
            st.error("Invalid username or password. Please try again.")


def main():
    st.write("session_state:", st.session_state)
    if not st.session_state['user']:
        st.warning("Please login")
        st.switch_page(st.Page(login))
    st.title("main page")
    st.write("Welcome to the main page!")


pages = {
    "Go to": [
        st.Page(login, title="Login"),
        st.Page(create_account, title="Create Account")
    ],
    "overview": [
        st.Page(main, title="Main Page")
    ]
}


pg = st.navigation(pages=pages, position="sidebar")
pg.run()
