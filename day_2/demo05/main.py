import streamlit as st
st.title("Prashant's Institute Info Page ")
def show_about_uspage():
    st.header("About us" )
    st.write("DKTE’s Textile & Engineering Institute, with its exquisite and iconic historic mansion and sprawling campus is situated in the heart of Ichalkaranji city, the city which is known as the Manchester of Maharashtra. The institute was established in 1981 under the guidance of a visionary and a philanthropist leader Mr.K.B. Awade (Ex. M.P). To support the phenomenal growth of the textile industry that was taking place at Ichalkaranji and to overcome the dearth of technically qualified professionals, the founding of the institute has significantly contributed in enhancing the technological, industrial and economic development of the region and the country for last four decades.")
    st.balloons()
def show_courses_page():
    st.header("Courses")
    st.write("1. Textile Engineering 2. Computer Science and Engineering 3. Mechanical Engineering 4. Civil Engineering 5. Electrical Engineering 6. Electronics and Telecommunication Engineering 7. Information Technology 8. Artificial Intelligence and Data Science")
    st.balloons()
    

def show_contactpage():
    st.header("contact us :")
    st.write("D.K.T.E. SOCIETY'S TEXTILE & ENGINEERING INSTITUTE PO BOX130 RAJWADA ICHALKARANJI MAHARASHTRA 416115 India.Phone: 7385666811 (0230) 2421300 (0230) 2439557 / 58 / 59 (0230) 2432340   Email: director@dkte.ac.in dktestextile@gmail.com Fax: (0230) 2432329 Toll Free No:  1800 843 1300")
    st.balloons()
if "page" not in st.session_state :
    st.session_state.page="About us"

with st.sidebar:
    if st.button("About us",width="stretch"):
        st.session_state.page="About us"
    if st.button("courses",width="stretch"):
        st.session_state.page="courses"
    if st.button("contact us",width="stretch"):
        st.session_state.page="contact us"
    
if st.session_state.page=="About us":
    show_about_uspage()
elif st.session_state.page=="courses":
    show_courses_page()
else:
    show_contactpage()
