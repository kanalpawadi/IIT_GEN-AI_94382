from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# api_key=os.getenv("GROQ_API_KEY")
# llm=ChatGroq(
#     model="openai/gpt-oss-120b",
#     api_key=api_key
# )
# usesr_input=input("You: ")
# # result=llm.invoke(usesr_input)
# # print("AI: " ,result.content)


# api_key=os.getenv("GEMINI_API_KEY")
# llm=ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     api_key=api_key
# )'
url="http://127.0.0.1:1234/v1"
llm=ChatOpenAI(
    base_url=url,
    model="google/gemma-3-4b",
    api_key="dummy"
)
usesr_input=input("You: ")
result=llm.stream(usesr_input)
for chunk in result:
    print(chunk.content, end="")