# app.py
import streamlit as st
import os
from config import get_chroma
from models.shortlist import shortlist_resumes
from models.upload_resumes import upload_resume
from models.list_resumes import list_resumes
from models.delete_resume import delete_resume

os.makedirs("resumes", exist_ok=True)
if "resume_to_update" not in st.session_state:
    st.session_state.resume_to_update=None

chroma = get_chroma()

st.header("AI-Powered Resume Shortlisting System")

menu = st.sidebar.selectbox(
    "Select Option",
    ["home page","Upload Resume", "Shortlist Resumes","List Resumes", "Delete Resume"] 
)

# Upload Resume 
if menu =="home page":
    st.header("HOME PAGE ",text_alignment="center")
    st.snow()
    st.balloons()
elif menu == "Upload Resume":
    st.header("Upload Resume (PDF)")
    file = st.file_uploader("Upload PDF", type=["pdf"])

    if file:
        save_path = os.path.join("resumes", file.name)

        with open(save_path, "wb") as f:
            f.write(file.getbuffer())

        msg = upload_resume(save_path)
        st.success(msg)
     
    st.subheader("view all resumes in database")
    if st.button("View Resumes",type="primary"):
        all_docs =chroma.get()
        st.table(all_docs['ids'])


#  Shortlist Resumes  
elif menu == "Shortlist Resumes":
    st.header("Shortlist Candidates")

    job_desc = st.text_area("Enter Job Description")
    top_k = st.number_input("Number of resumes to shortlist", 1, 10, 3)

    if st.button("Shortlist Resumes",type="primary"):
        results = shortlist_resumes(job_desc, top_k)

        if not results:
            st.warning("No resumes found in database")
        else:
            for r in results:
                st.subheader(r["file"])
                st.write("Pages:", r["pages"])
                st.write("Preview:", r["content"])
                st.divider()


# Delete Resume  
elif menu == "Delete Resume":
    st.header("Delete Resume")

    name = st.text_input("Enter resume file name (example: resume.pdf)")

    if st.button("Delete Resume",type="primary"):
        msg = delete_resume(name)
        st.success(msg)

    st.subheader("view all resumes in database")
    if st.button("View Resumes",type="primary"):
        all_docs =chroma.get()
        st.table(all_docs['ids'])
    
elif menu=="List Resumes":
    st.header("Available Resumes")
    resumes=list_resumes()
    
    # if update mode active
    if st.session_state.resume_to_update:
       st.subheader(f"update resume:{st.session_state.resume_to_update}")
       new_file=st.file_uploader("upload updated resume(pdf)",type=["pdf"])
       col1,col2=st.columns(2)
       if col1.button("Save Updated Resume " ,type="primary"):
            if not new_file:
                st.error("please upload a file before saving .")
            else:
                #delate old resume
                delete_resume(st.session_state.resume_to_update)
                #save new resume
                save_path=os.path.join("resumes",new_file.name)
                with open(save_path,"wb")as f:
                    f.write(new_file.getbuffer())
                #insert +embed
                msg=upload_resume(save_path)
                st.success(f"Resume updated Successfully !  {msg}")
                #exit update mode
                st.session_state.resume_to_update=None
                st.rerun()
            
            #cancel
            if col2.button("cancel",type="primary"):
                st.session_state.resume_to_update=None
                st.rerun()

    # if normal mode is active 
    else:
        if not resumes:
            st.warning("NO resumes found ! ")
        else:
            for file_name in resumes:
                st.subheader(file_name)
                col1,col2=st.columns(2)

                #delate button 
                if col1.button("Delete",key="del_"+file_name,type="primary"):
                    msg=delete_resume(file_name)
                    st.success(msg)
                    st.rerun()

                #update button
                if col2.button("Update (Replace)",key="upd_"+file_name,type="primary"):
                    st.session_state.resume_to_update=file_name
                    st.rerun()


         
         

       
