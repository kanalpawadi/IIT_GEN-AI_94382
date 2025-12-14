import pandas as pd 
import streamlit as st
st.title(":::welcome to ALL IN ONE AI TOOL:::")

#upload the file
data_file=st.file_uploader("upload your csv file  here ",type=['csv'])

#load it as dataframe
if data_file :
    df=pd.read_csv(data_file)
    #display the dataframe 
    st.dataframe(df)
    st.bar_chart(df)
    st.balloons()