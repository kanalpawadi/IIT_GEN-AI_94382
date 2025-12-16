import os
import requests
import json

api_key=os.getenv("GROQ_API_KEY")
print(GROQ_API_KEY)
url="https://api.groq.com/openai/v1/chat/completions"

headers={
    "authorization ":f"Bearer{GROQ_API_KEY}",
    "content-Type":"application/json"
}

user_prompt=input("ask anything :")
req_data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        { "role": "user", "content": user_prompt }
    ],
}


response=requests.post(url,data=json.dumps(req_data),headers=headers)
print("status:",response.status_code)
print(response.json())