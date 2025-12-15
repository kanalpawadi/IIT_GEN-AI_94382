"""
Show Login Form. If login is successful (fake auth if username & passwd is
same, consider valid user), show weather page. There input a city name
from text box and display current weather information. Provide a logout
button and on its click, display thanks message.
"""
 
import streamlit as st
import requests
from dotenv import load_dotenv
load_dotenv()
import os
 
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "logged_out" not in st.session_state:
    st.session_state.logged_out = False


 
def login_page():
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == password and username != "":
            st.session_state.logged_in = True
            st.session_state.logged_out = False
            st.session_state.username = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials (Username and Password must be same)")


 
def weather_page():
    st.title("🌤️ Weather Page")

    city = st.text_input("Enter City Name")

    if st.button("Get Weather"):
        if city:
            api_key = os.getenv("weather_api")  # Your API key           
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                weather = data['weather'][0]['description']
                temp = data['main']['temp']
                st.success(f"📍 {city}")
                st.write(f"🌡️ Temperature: {temp} °C")
                st.write(f"🌥️ Weather: {weather}")
            else:
                st.error("City not found!")
        else:
            st.warning("Please enter a city name")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.logged_out = True
        st.rerun()


 
def thanks_page():
    st.title("🙏 Thank You")
    st.success("Thanks for using the Weather App!")


 
def main():
    if st.session_state.logged_in:
        weather_page()
    elif st.session_state.logged_out:
        thanks_page()
    else:
        login_page()


if __name__ == "__main__":
    main()
