from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)

def create_documents(data_list):
    from langchain_core.documents import Document
    
    documents = []
    for item in data_list:
        content = item.get('content', '')
        metadata = {k: v for k, v in item.items() if k != 'content'}
        
        if content:
            documents.append(Document(page_content=content, metadata=metadata))
            
    return documents
