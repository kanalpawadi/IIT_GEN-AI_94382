import streamlit as st 

#registation page 

with st.form(key='registration_form'):
    st.header("User Registration")
    first_name=st.text_input("first name ")
    last_name=st.text_input("last name ")
    age =st.slider("age",1,100,25,1)
    address=st.text_area("address")
    submit_button=st.form_submit_button("submit" , type="primary")

    # form submit handling must be done outside form `with` block
if submit_button:
    #validate form data 
    err_message =""
    is_error=False
    if not first_name:
        is_error=True
        err_message +="first name cannot be empty \n  "
    if not last_name:
        is_error=True
        err_message +="last name cannot be empty \n  "
    if not address:
        is_error=True
        err_message +="address cannot be empty \n  "    
    if is_error:
        st.error(err_message)
    else:
        message = f"Successfully registered: {first_name} {last_name}.\nAge: {age}. Living at {address}"
        st.success(message)