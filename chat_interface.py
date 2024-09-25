import streamlit as st

class ChatInterface:
    def __init__(self):
        st.title("AI Innovation Consultant Assistant")
        self.user_input = st.text_input("You:", key="user_input")
        self.chat_history = []

    def get_user_input(self):
        return self.user_input

    def display_response(self, response):
        self.chat_history.append(("You", self.user_input))
        self.chat_history.append(("Assistant", response))
        
        for role, message in self.chat_history:
            st.write(f"{role}: {message}")

    def clear_input(self):
        st.session_state.user_input = ""