"""Two Intelligent Agents - CSV QA + Sunbeam Web Scraper"""

from langchain_groq import ChatGroq
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from pandasql import sqldf
import pandas as pd
import os
import streamlit as s

load_dotenv()

s.set_page_config(page_title="Two Intelligent Agents", layout="wide")
s.title("🧠 Multi Agent Streamlit Application")

#  MODEL 
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# CHAT HISTORY  
if "chat_history" not in s.session_state:
    s.session_state.chat_history = []

#   SIDEBAR  
with s.sidebar:
    s.sidebar.header("Select Machine")
    model_choice = s.selectbox(
        "Choose CHATBOT ",
        ["📂 CSV SQL Chatbot", "🌐 Web Scraping Bot"])
 
def csv_agent():
    s.header("📂 CSV SQL Chatbot")

    file_upload = s.file_uploader("Upload CSV File", type=['csv'])

    if not file_upload:
        return "Please upload a CSV file to continue."

    df = pd.read_csv(file_upload)

    s.subheader("CSV Preview")
    s.dataframe(df.head())

    s.subheader("CSV Schema")
    s.write(df.dtypes)

    question = s.chat_input("Ask anything about this CSV...")

    if not question:
        return "Waiting for your CSV question…"

    s.chat_message("user").write(question)

    sql_prompt = f"""
    You are an SQL expert.
    Convert this question to a valid SQLite SQL query.
    Table name = df
    Question = {question}
    """

    sql_query = llm.invoke(sql_prompt).content

    s.write("### Generated SQL Query")
    s.code(sql_query)

    try:
        result = sqldf(sql_query, {"df": df})
        s.write("### Query Result")
        s.dataframe(result)

        explanation = (
            "I understood your question, converted it into an SQL query, "
            "executed it on your uploaded CSV using pandasql, and displayed "
            "the result in a very simple and clear way."
        )

        s.chat_message("assistant").success(explanation)

        return explanation

    except Exception as e:
        error_msg = f"SQL Execution Failed: {str(e)}"
        s.chat_message("assistant").error(error_msg)
        return error_msg

 
def web_srapping_agent():
    s.header("🌐 Sunbeam Internship Web Scraper")

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.sunbeaminfo.in/internship")

    s.write("Page Title: " + driver.title)
    driver.implicitly_wait(5)

    table_body = driver.find_element(By.CLASS_NAME, "table")
    table_rows = table_body.find_elements(By.TAG_NAME, "tr")

    data_list = []

    for row in table_rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) == 8:
            data_list.append({
                "Sr_No": cols[0].text,
                "Batch": cols[1].text,
                "Batch Duration": cols[2].text,
                "Start Date": cols[3].text,
                "End Date": cols[4].text,
                "Time": cols[5].text,
                "Fees (Rs.)": cols[6].text,
                "Download Brochure": cols[7].text
            })

    driver.quit()

    if not data_list:
        return "No internship details found."

    s.subheader("Sunbeam Internship Batches")
    s.table(pd.DataFrame(data_list))

    explanation = (
        "I opened the Sunbeam Internship website, read the internship "
        "table, and displayed all batch details in an easy-to-understand "
        "format."
    )

    s.success(explanation)
    return explanation
# MAIN CONTROLLER
if model_choice == "📂 CSV SQL Chatbot":
    answer = csv_agent()
else:
    answer = web_srapping_agent()
