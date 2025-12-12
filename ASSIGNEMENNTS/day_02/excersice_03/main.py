import requests 
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY") 
city = input("Enter city: ")
url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"   

try:
   response=requests.get(url)
   print("response status code : ",response.status_code)
   print(response.text)
   weather_data=response.json()
   print(f"Current temperature in {city} is {weather_data['main']['temp']} Kelvin") 
except:
   print("Error occurred:")
   