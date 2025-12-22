from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

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
while True:
    #take the input
    user_input = input("You : ")
    if user_input =="exit":
        break

    #append user message in conversation 
    conversation.append({"role":"user","content":user_input})

    #invoke the agent 
    result =agent.invoke({"messages":conversation})
    #print the only last message
    ai_msg=result["messages"][-1]
    print("AI",ai_msg.content)
    #lets use conversation history returned by agent 
    conversation=result["messages"]
