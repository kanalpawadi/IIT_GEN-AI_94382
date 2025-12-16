#2. ⁠Connect to  Gemini AI using REST api. Send same prompt and compare results. Also compare the speed.
import os
import time
import requests
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()
 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(GEMINI_API_KEY)
 

from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)
while True:
    prompt=input("ask anything :")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    print(response.text)
