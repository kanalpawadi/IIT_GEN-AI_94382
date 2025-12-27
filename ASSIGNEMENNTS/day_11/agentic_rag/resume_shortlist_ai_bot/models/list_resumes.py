#modules/list_resumes.py

import os 
Resume_dir="resumes"

def list_resumes():
    if not os.path.exists(Resume_dir):
        return[]
    return [f for f in os.listdir(Resume_dir) if f.lower().endswith(".pdf")]