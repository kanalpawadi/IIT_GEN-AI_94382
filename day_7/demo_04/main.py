from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter=RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap=200,separators=["\n\n"," ",""])
with open("dummy_data.txt","r")as file:
    raw_text=file.read()

docs =text_splitter.create_documents([raw_text])

for doc in docs:
    print(doc.page_content)
    print("\n")