import os
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

class LanguageModel:
    def __init__(self, vector_store, openai_client):
        if vector_store.vector_store is None:
            raise ValueError("Vector store is not initialized. Please ensure documents are added before creating the LanguageModel.")
        self.retriever = vector_store.vector_store.as_retriever()
        self.chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_client.api_key)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.chain = ConversationalRetrievalChain.from_llm(
            self.chat_model,
            retriever=self.retriever,
            memory=self.memory
        )

    def generate_response(self, user_input):
        response = self.chain({"question": user_input})
        return response['answer']