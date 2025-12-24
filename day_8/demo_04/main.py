#connect with chroma db 
import chromadb

db = chromadb.PersistentClient(path="./knowledge_base")

collection = db.get_or_create_collection("resumes")

collection.add(
    ids=["resume_1"],
    documents=["This is my resume text"],
    embeddings=[[0.1, 0.2, 0.3, 0.4]],   # Example dummy vector
    metadatas=[{"name": "Nilesh"}]
)

print("Added successfully")
