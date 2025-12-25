import streamlit as st 
import mysql.connector
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
load_dotenv()

st.set_page_config(page_title="MySQL Connector ",layout="centered")
st.title("🔌 MySQL Database Connector")

host=os.getenv("HOST")
user=os.getenv("USER")
password=os.getenv("PASSWORD")
database="Sunbeam_test_mysql_connector"


# Session State
if "conn" not in st.session_state:
    st.session_state.conn = None
if "tables" not in st.session_state:
    st.session_state.tables=None

 
def connect_database():
    try:
        st.session_state.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        st.success("✅ Connected Successfully!")

        cursor = st.session_state.conn.cursor()
        cursor.execute("SHOW TABLES")
        st.session_state.tables = cursor.fetchall()

    except mysql.connector.Error as e:
        st.error(f"❌ MySQL Error: {e}")


def disconnect_database():
    if st.session_state.conn:
        st.session_state.conn.close()
        st.session_state.conn = None
        st.warning("🔌 Disconnected!")
    else:
        st.info("ℹ️ No active database connection.")



def get_schema_context():
    if not st.session_state.conn:
        return ""

    cursor = st.session_state.conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]

    schema = ""
    for table in tables:
        cursor.execute(f"DESCRIBE {table}")
        cols = cursor.fetchall()
        schema += f"\nTable: {table}\n"
        for c in cols:
            schema += f"- {c[0]} ({c[1]})\n"

    return schema


#buttons 
col1,col2 = st.columns(2)

with col1:
    if st.button("Connect Database", type="primary"):
        connect_database()

with col2:
    if st.button("Disconnect Database", type="primary"):
        disconnect_database()


 #session states
if st.session_state.conn:
    st.success("🟢 Status: Connected")
else:
    st.error("🔴 Status: Disconnected")

 
if st.session_state.tables:
    tables = [t[0] for t in st.session_state.tables]

    st.subheader("📂 Tables in Database:")
    selected_table = st.selectbox("Select a table", tables)

    if st.button("Show Table Schema"):
        cursor = st.session_state.conn.cursor()
        cursor.execute(f"DESCRIBE {selected_table}")
        schema = cursor.fetchall()

        st.subheader(f"🧾 Schema of `{selected_table}`")
        st.table({
            "Field":[r[0] for r in schema],
            "Type":[r[1] for r in schema],
            "Null":[r[2] for r in schema],
            "Key":[r[3] for r in schema],
            "Default":[r[4] for r in schema],
            "Extra":[r[5] for r in schema]
        })


 
st.header("🤖 AI SQL Assistant")

user_prompt = st.text_area("Ask anything about the database:")

if st.button("Generate SQL Query"):
    if not st.session_state.conn:
        st.error("⚠️ Connect to DB first!")
    elif not user_prompt.strip():
        st.warning("✏️ Enter a question")
    else:
        with st.spinner("🤖 Thinking..."):

            schema_context = get_schema_context()

            system_prompt = f"""
You are a MySQL expert with 10 years experience.
Convert the user question into VALID MySQL SELECT query ONLY.

Database: {database}

Schema:
{schema_context}

Rules:
- First output SQL query in code block
- Then explanation in very simple English
- ONLY SELECT queries allowed
- Do NOT hallucinate columns
- Do NOT modify database
"""

            llm = init_chat_model(
                model="google/gemma-3-4b",
                model_provider="openai",
                base_url="http://127.0.0.1:1234/v1",
                api_key="dummy"
            )

            result = llm.invoke(
    [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_prompt}
    ]
)


            st.subheader("🧠 AI Generated Result")
            st.write(result.content)
