from langchain.chat_models import init_chat_model
import os 
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

llm=init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY") 
)

conversation = [
    {"role": "system", "content": "You are SQLite expert developer with 10 years of experience."}
]

csv_file=input("Ask anything about this csv?")
df=pd.read_csv(csv_file)
print("CSV schema: ")
print (df.dtypes)

while True:
    user_input=input("ask anything about this csv ? ")
    if user_input == "exit":
        break
    llm_input=f"""
     table Name:data
     table Schema:{df.dtypes}
     question:{user_input}
     Instruction : 
      write a sql query for the above question.
      generate sql query only in plain text format and nothing alse.
      if you cannot generate the query , then output "error".
    
      """
    
    result=llm.invoke(llm_input)
    print(result.content)