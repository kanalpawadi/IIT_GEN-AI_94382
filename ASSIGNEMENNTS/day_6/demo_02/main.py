""" Input city name from user. Get current weather from weather API.
Ask LLM to explain the weather in English."""

from langchain.chat_models import init_chat_model
import os 
import requests
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
st.title("weather chatbot:" )
llm=init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY") 
)

 

weather_api=os.getenv("weather_api")
city =st.text_input("Enter the city :")

# Call Weather API
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric"
response = requests.get(url)

if response.status_code!=200:
    st.write("error in fetching weather data ")
    exit()

weather =response.json()

llm_prompt=f"""
current wether details :
city :{city}
 {weather}
explain the current weather in simple english words .
"""

result=llm.invoke(llm_prompt)
st.write(result.content)
 