import tempfile
import os
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_documents(uploaded_file):
    documents = []
    
    # Create a temporary file to save the uploaded content
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name

    try:
        loader = UnstructuredFileLoader(temp_file_path)
        documents.extend(loader.load())
    except Exception as e:
        print(f"Error processing uploaded file: {e}")
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_documents = text_splitter.split_documents(documents)
    
    return split_documents