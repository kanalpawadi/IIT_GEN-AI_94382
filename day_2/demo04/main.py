import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []
st.title(":: Prashant's CHAT-BOT :: ")
with st.sidebar:
    st.header(" settings  ")
    choices=['Upper Case ','Lower Case ','Toggle '] 
    mode =st.selectbox(" select the mode ",choices)
    count=st.slider(" select the count ",1,10,6,1)

    st.subheader("config ")
    st.json({"mode":mode,
             "count":count  })
    
msg=st.chat_input("What you want today ....")  
if msg:
        if mode=='Upper Case ':
            outmsg=msg.upper()
        elif mode=='Lower Case ':
            outmsg=msg.lower()
        else:
            outmsg=msg.swapcase()
         
        
        st.session_state.messages.append({msg})
        st.session_state.messages.append({outmsg})
        st.balloons()

        msglist=st.session_state.messages
        for idx,mssage in enumerate(msglist):
             role='human' if idx%2==0 else "assistent"
             with st.chat_message(role):
                    st.write(mssage)