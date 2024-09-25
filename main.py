import os
from dotenv import load_dotenv
import streamlit as st
from data_processor import process_documents
from vector_store import VectorStore
from language_model import LanguageModel
from chat_interface import ChatInterface
from memory_manager import MemoryManager
import logging
from openai import OpenAI

# Load environment variables
load_dotenv()

# Ensure OpenAI API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
print(f"API key loaded: {api_key[:5]}...{api_key[-5:]}")  # Print first and last 5 characters

logging.basicConfig(level=logging.INFO)

def main():
    st.title("AI Innovation Consultant")

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf"])

    if uploaded_file is not None:
        documents = process_documents(uploaded_file)
        
        if documents:
            vector_store = VectorStore()
            vector_store.add_documents(documents)
            
            if vector_store.vector_store is not None:
                try:
                    language_model = LanguageModel(vector_store, client)
                    chat_interface = ChatInterface()
                    
                    user_input = chat_interface.get_user_input()
                    if user_input:
                        response = language_model.generate_response(user_input)
                        chat_interface.display_response(response)
                        chat_interface.clear_input()
                except ValueError as e:
                    st.error(f"Error initializing language model: {str(e)}")
            else:
                st.error("Failed to initialize vector store. Please try again.")
        else:
            st.warning("No content could be extracted from the uploaded file. Please try a different file.")
    else:
        st.info("Please upload a document to get started.")

if __name__ == "__main__":
    main()
