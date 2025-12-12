import requests
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get API key from .env
api_key = os.getenv("API_KEY")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error: Cannot fetch weather. Check city name or API key.")
        print("API Response:", response.text)
        return
    
    data = response.json()
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    print(f"\nWeather in {city.title()}:")
    print(f"Temperature : {temp}°C")
    print(f"Condition   : {desc}\n")

# Main Program
if __name__ == "__main__":
    city = input("Enter city: ")
    get_weather(city)
