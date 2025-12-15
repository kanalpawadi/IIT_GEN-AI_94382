"""
1. Make a chat bot like UI. Input a message from user and reply it back, but
display the reply using st.write_stream(). Use delay to show chatlike effect.
"""
import streamlit as st 
import time

if "messages" not in st.session_state:
    st.session_state.messages = []
st.title(":: CHAT-BOT  ")

with st.sidebar:
    st.header(" settings  ")
    choices=['Upper Case ','Lower Case ','Toggle ' ] 
    mode =st.selectbox(" select the mode ",choices)
    count=st.slider(" select the count ",1,10,6,1)

    st.subheader("config ")
    st.json({"mode":mode,
             "count":count  })

def stream_text(text, delay=0.05):
    for char in text:
        yield char
        time.sleep(delay)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
user_msg = st.chat_input("What you want today ....")

if user_msg:
    st.session_state.messages.append({
        "role": "human",
        "content": user_msg
    })

    with st.chat_message("human"):
        st.write(user_msg)

   
    if mode == 'Upper Case':
        bot_reply = user_msg.upper()
    elif mode == 'Lower Case':
        bot_reply = user_msg.lower()
    else:
        bot_reply = user_msg.swapcase()
 
    with st.chat_message("assistant"):
        st.write_stream(stream_text(bot_reply))

     
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    st.balloons()
    st.snow()