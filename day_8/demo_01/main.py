from langchain.embeddings import init_embeddings 
embed_model=init_embeddings(
    model="text-embedding-all-minilm-l6-v2-embedding",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy_key",
    check_embedding_ctx_length=False
)

sentence=[
    "I like Artificial Intelligence",
    "Generative AI is magnificant",
    "World is amazing"
]

embeddings=embed_model.embed_documents(sentence)
for embedding in embeddings:
   print(f"Len={len(embedding)}-->{embedding[:4]}")