import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

# 1️⃣ Embedding Model
embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 2️⃣ Text to index
raw_text = """
Soccer players train daily to build stamina, improve ball control,
practice tactical strategies, and enhance teamwork.
Training also includes strength conditioning and mental focus exercises.
"""

# 3️⃣ Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_text(raw_text)

# 4️⃣ Initialize Persistent Chroma DB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="demo"
)

# 5️⃣ Create embeddings
embeddings = embed_model.embed_documents(chunks)

# 6️⃣ Prepare metadata & ids
ids = [f"doc_{i}" for i in range(len(chunks))]
metadatas = [{"source": "example.txt", "chunk_id": i} for i in range(len(chunks))]

# 7️⃣ Add to DB
collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadatas
)

# 8️⃣ Query (Similarity Search)
query = "How do soccer players train?"
query_embedding = embed_model.embed_query(query)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print("Top Results:\n")
for doc, meta, dist in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
):
    print("Document:", doc)
    print("Metadata:", meta)
    print("Distance:", dist)
    print("-" * 50)

# 9️⃣ Update (delete + reinsert)
collection.delete(ids=["doc_1"])

updated_text = "Professional soccer players train every day with expert coaches."
updated_embedding = embed_model.embed_documents([updated_text])

collection.add(
    ids=["doc_1"],
    documents=[updated_text],
    embeddings=updated_embedding,
    metadatas=[{"source": "example.txt", "chunk_id": 1}]
)

#client.persist()
