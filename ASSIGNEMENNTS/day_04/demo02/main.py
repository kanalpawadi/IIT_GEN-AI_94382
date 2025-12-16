#2. ⁠Connect to Groq and  I using REST api. Send same prompt and compare results. Also compare the speed.
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

user_prompt = input("Ask anything: ")
req_data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        { "role": "user", "content": user_prompt }
    ],
}

response = requests.post(url, data=json.dumps(req_data), headers=headers)
print("Status:", response.status_code)
print(response.json())