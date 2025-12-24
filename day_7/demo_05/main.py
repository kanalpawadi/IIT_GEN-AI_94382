# 5 . code aware chunking 
from langchain_text_splitters import RecursiveCharacterTextSplitter
code_splitter=RecursiveCharacterTextSplitter.from_language(language="java",chunk_size=1000,chunk_overlap=100)
with open("dummy_code.java","r") as file:
    code_text=file.read()

docs=code_splitter.create_documents([code_text])

for doc in docs:
    print(doc.page_content)
    print("\n\n")