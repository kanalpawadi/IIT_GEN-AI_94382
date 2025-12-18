"""Create a Streamlit application that allows users to upload a CSV file
 and view its schema.Use an LLM to convert user questions into SQL queries, 
 execute them on the CSV data using pandasql, and explain the 
 results in simple English.
"""

import streamlit as st 
import pandas as pd 
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

st.set_page_config("csv sql chatbot :")
st.title("Sql chatbot  ")

file_upload=st.file_uploader("upload the csv file " ,type=['csv'])
if file_upload:
    df=pd.read_csv(file_upload)
    st.subheader("csv preview ")
    st.dataframe(df.head())

    st.subheader("csv schema ")
    st.write(df.dtypes)

    st.subheader("ask anything from table : ")
    prompt=st.text_input("ex:display anything :")

    if prompt:
        sql_prompt=f"""
        you are the sql expert generator 
        table name :data 
        table schema {df.dtypes}
        user_question:{prompt}
        instruction :
        generate only valid sqlite sql query 
        with explaination if not possible to show the direct error 
        explain the results in simple English.
        """
sql_response=llm.invoke(sql_prompt) 
st.subheader("generated subquery : ")

st.write(sql_response.content)