import streamlit as st
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import Anthropic
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()

# Set up Anthropic API key
import os
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Initialize Streamlit app
st.title("AI Innovation Consultant Assistant")

# File uploader
uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf", "docx", "xlsx", "pptx"])

# Initialize or load vector store
persist_directory = 'db'
embedding = HuggingFaceEmbeddings()  # Using HuggingFace embeddings as an alternative to OpenAI
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

if uploaded_file is not None:
    # Process and add new document to vector store
    loader = UnstructuredFileLoader(uploaded_file)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    vectordb.add_documents(texts)
    vectordb.persist()

# Set up retrieval chain
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = Anthropic(model="claude-2", temperature=0)  # Using Claude-2 model
qa_chain = ConversationalRetrievalChain.from_llm(
    llm,
    vectordb.as_retriever(),
    memory=memory
)

# Chat interface
user_input = st.text_input("Ask a question:")
if user_input:
    response = qa_chain({"question": user_input})
    st.write(response['answer'])