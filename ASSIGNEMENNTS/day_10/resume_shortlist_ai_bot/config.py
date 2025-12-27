# config.py
import os
from langchain.embeddings import init_embeddings
from langchain_community.vectorstores import Chroma

#  Embedding Model  
EMBED_MODEL = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)

CHROMA_DIR = "chroma_store"
COLLECTION_NAME = "resume_vectors"


def get_chroma():
    os.makedirs(CHROMA_DIR, exist_ok=True)

    chroma = Chroma(
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=EMBED_MODEL
    )

    chroma.persist()
    return chroma
