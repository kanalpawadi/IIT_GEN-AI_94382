import streamlit as st
import pandas as pd
from datetime import datetime
import os

 
st.set_page_config(page_title="CSV Management App", layout="wide")

USERS_FILE = "users.csv"
USERFILES_FILE = "userfiles.csv"
 
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(USERFILES_FILE):
    pd.DataFrame(columns=["username", "filename", "upload_datetime"]).to_csv(USERFILES_FILE, index=False)
 
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None
 
def home():
    st.title("🏠 Home")
    st.info("Welcome to the CSV Management App")
    st.write("Please login or register to continue.")

def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users_df = pd.read_csv(USERS_FILE)
        valid = users_df[
            (users_df["username"] == username) &
            (users_df["password"] == password)
        ]

        if not valid.empty:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Logged in as {username}")
            st.rerun()
        else:
            st.error("Invalid username or password")

def register():
    st.title("📝 Register")
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")

    if st.button("Register"):
        users_df = pd.read_csv(USERS_FILE)

        if username in users_df["username"].values:
            st.error("User already exists")
        elif username == "" or password == "":
            st.warning("Fields cannot be empty")
        else:
            new_user = pd.DataFrame([[username, password]],
                                    columns=["username", "password"])
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            users_df.to_csv(USERS_FILE, index=False)
            st.success("Registration successful! Please login.")

def explore_csv():
    st.title("📊 Explore CSV")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)

        history_df = pd.read_csv(USERFILES_FILE)
        new_entry = pd.DataFrame([[
            st.session_state.username,
            uploaded_file.name,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]], columns=["username", "filename", "upload_datetime"])

        history_df = pd.concat([history_df, new_entry], ignore_index=True)
        history_df.to_csv(USERFILES_FILE, index=False)

        st.success("CSV uploaded & history saved")

def see_history():
    st.title("📜 Upload History")
    history_df = pd.read_csv(USERFILES_FILE)
    user_history = history_df[
        history_df["username"] == st.session_state.username
    ]

    if user_history.empty:
        st.info("No uploads found")
    else:
        st.dataframe(user_history, use_container_width=True)

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.success("Logged out successfully")
    st.rerun()
 
st.sidebar.title("📌 Menu")

if not st.session_state.logged_in:
    menu = st.sidebar.selectbox("Select Menu", ["Home", "Login", "Register"])

    if menu == "Home":
        home()
    elif menu == "Login":
        login()
    elif menu == "Register":
        register()

else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    menu = st.sidebar.selectbox(
        "Select Menu",
        ["Explore CSV", "See History", "Logout"]
    )

    if menu == "Explore CSV":
        explore_csv()
    elif menu == "See History":
        see_history()
    elif menu == "Logout":
        logout()
