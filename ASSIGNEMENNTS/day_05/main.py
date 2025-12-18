"""Q1: Design a Streamlit-based application with a sidebar to switch between Groq and LM Studio.
The app should accept a user question and display responses using Groq’s cloud LLM and a
locally running LM Studio model.Also maintain and display the complete chat history of user 
questions and model responses."""

import os
import requests
from dotenv import load_dotenv
import streamlit as st
import json

load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

api_key="Dummy"
if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
def ask_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model":"openai/gpt-oss-120b",
        "messages": [{"role": "user", "content": prompt}]
    }
    response=requests.post(GROQ_URL,json=data,headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def ask_lm_studio(prompt):
    data = {
        "model": "microsoft/phi-4-mini-reasoning",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(LM_STUDIO_URL, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

st.set_page_config(page_title="Groq vs LM studio chat ", layout="wide")
st.title("🤖 Groq & LM Studio Chat App")
st.caption("Groq (Cloud) + LM Studio (Local)")

#sidebar
with st.sidebar:
    st.sidebar.header("select machines ")
    model_choice=st.selectbox(
            "Choose LLM",
            ["Groq (Cloud)","LM Studio (Local)"]
        )
    

prompt=st.chat_input("💬 Ask a question:")

for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["question"])
    with st.chat_message("assistant"):
        st.markdown(chat["answer"])
    

if prompt:   # ✅ THIS LINE FIXES THE ERROR
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.spinner("Thinking ..."):
        if model_choice == "Groq (Cloud)":
            answer=ask_groq(prompt)
            with st.chat_message("assistant"):
                st.markdown(answer)
        else:
            answer=ask_lm_studio(prompt )
            with st.chat_message("assistant"):
                st.markdown(answer)
        
        #save chat histrory 
        st.session_state.chat_history.append({
            "model" : model_choice,
            "question":prompt,
            "answer":answer
        
        })
