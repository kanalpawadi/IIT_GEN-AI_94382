# modules/delete_resume.py
import os
from config import get_chroma

RESUME_DIR = "resumes"


def delete_resume(file_name):
    chroma = get_chroma()
   #delete from chroma 
    try:

        chroma.delete(ids=[file_name])
        chroma.persist()
    except:
        pass #in case id is not exist 

    #delete from  local storage
    resume_path = os.path.join(RESUME_DIR, file_name)
    if os.path.exists(resume_path):
        os.remove(resume_path)
        return f"Resume '{file_name}' deleted successfully!"
    else:
        return f"Resume not found  ."
