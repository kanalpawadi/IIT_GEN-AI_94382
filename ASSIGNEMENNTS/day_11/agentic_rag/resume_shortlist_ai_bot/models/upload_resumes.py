# modules/upload_resume.py
import os
from langchain_community.document_loaders import PyPDFLoader
from config import get_chroma, EMBED_MODEL

RESUME_DIR = "resumes"
os.makedirs(RESUME_DIR, exist_ok=True)


def upload_resume(file_path):

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    text = ""
    for page in docs:
        text += page.page_content

    chroma = get_chroma()

    resume_id = os.path.basename(file_path)

    # If exists, delete old embedding (update support)
    chroma.delete(ids=[resume_id])
    chroma.add_texts(
        texts=[text],
        metadatas=[{
            "file_name": resume_id,
            "pages": len(docs)
        }],
        ids=[resume_id]
    )
    chroma.persist()
    return f"Resume '{resume_id}' uploaded & indexed(with embeddings) successfully!"
   
