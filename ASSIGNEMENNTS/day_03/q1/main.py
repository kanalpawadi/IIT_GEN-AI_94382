import sqlite3
import pandas as pd
import streamlit as st

st.title("CSV to SQL Query Tool")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Data Preview")
    st.dataframe(df)
    
    # Register dataframe as SQL table
    conn = sqlite3.connect(":memory:")
    df.to_sql("data", conn, index=False, if_exists="replace")
    
    # Get SQL query from user
    query = st.text_area("Enter your SQL query:")
    
    if st.button("Execute Query"):
        try:
            result = pd.read_sql_query(query, conn)
            st.subheader("Query Result")
            st.dataframe(result)
        except Exception as e:
            st.error(f"Error executing query: {e}")
    
    conn.close()

    
 