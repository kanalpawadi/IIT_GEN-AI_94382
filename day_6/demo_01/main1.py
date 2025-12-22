from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
import streamlit as st 

st.title("dummy agent: ")

#create model 
llm=init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy"
)
conversation=[]
#create agent 
agent =create_agent(
    model=llm,
    tools=[],
    system_prompt="you are a helpful assistent.answer in short ."

)
prompt=st.chat_input("You : ")
if prompt:
    #append user message in conversation 
    conversation.append({"role":"user","content":prompt})
    #invoke the agent 
    result =agent.invoke({"messages":conversation})
    #print the only last message
    ai_msg=result["messages"][-1]
    st.write("AI",ai_msg.content)
    #lets use conversation history returned by agent 
    conversation=result["messages"]
