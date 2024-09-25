from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
import chromadb
import os

class VectorStore:
    def __init__(self):
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None
        self.persist_directory = "chroma_db"
        
        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)
        
        self.chroma_client = chromadb.PersistentClient(path=self.persist_directory)

    def add_documents(self, documents):
        self.vector_store = Chroma.from_documents(
            documents,
            self.embeddings,
            client=self.chroma_client,
            collection_name="document_collection"
        )

    def search(self, query, k=5):
        if not self.vector_store:
            return []
        return self.vector_store.similarity_search(query, k=k)