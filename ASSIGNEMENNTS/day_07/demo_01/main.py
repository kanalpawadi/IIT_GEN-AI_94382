"""Q1
• Create tools: calculator, file reader, current weather, and knowledge lookup
using @tool decorator.
• Build an agent with all three tools and test with prompts requiring tool usage.
• Inspect message history to understand tool-calling flow.
• Implement a logging middleware and observe its output during agent
execution."""

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os
import json
import requests
load_dotenv()
import streamlit as s

s.title("Web pages of multiple tools : ")
 
@tool
def calculator(expression):
    """
    This calculator function solves any arithmetic expression containing all constant values.
    It supports basic arithmetic operators +, -, *, /, and parenthesis. 
    
    :param expression: str input arithmetic expression
    :returns expression result as str
    """
    try:
        result=eval(expression)
        return str(result)
    except:
        return "Error : Cannot solve expression "
    
@tool
def get_weather(city):
    """
    this get_weather() function gets the current weather of given city .
    if weather cannot be found ,it returns "Error".
    this function doesn't return historic or general weather of the city ,
    :param city :str input -city name 
    :returns current weather in json format or "error"
    """
    try:
        api_key=os.getenv("weather_api")
        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}"
        response=requests.get(url)
        weather =response.json()
        return json.dumps(weather)
    except:
        return "Error"

@tool
def read_file(filepath):
    """
    Docstring for read_file
    read the uploaded file 
    :param filepath: Description
    """
    try:
        with open(filepath, 'r') as file:
            text = file.read()
            return text
    except:
        return "Error"

    
#create model 
llm=init_chat_model(
    model = "google/gemma-3-4b",
    model_provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "non-needed"
)

#cereate agent 
agent=create_agent(
    model=llm,
    tools=[calculator,get_weather,read_file],
    system_prompt="You are a helpful assistent . Answer in short ."

)
if "chat" not in s.session_state:
    s.session_state.chat = []

user_input=s.chat_input("You: ")
if user_input:
    s.session_state.chat.append({"role":"user","content":user_input})
    #invoke the agent with user input 
    result=agent.invoke({
        "messages":s.session_state.chat
        
    })
    llm_output=result["messages"][-1].content
    #s.write("AI: ",llm_output.content)
    s.session_state.chat.append({"role":"assistant","content":llm_output})
    # s.write("\n\n", result["messages"])

    for msg in s.session_state.chat:
        if msg["role"]=="user":
            s.write(f"You: {msg['content']}")
        else:
            s.write(f"AI: {msg['content']}")
            