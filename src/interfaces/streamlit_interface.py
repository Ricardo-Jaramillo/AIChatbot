from interfaces.base_interface import BaseInterface
import streamlit as st

class StreamlitInterface(BaseInterface):
    def __init__(self, model):
        self.model = model

    def display(self):
        st.title("Chatbot Interface")
        user_input = st.text_input("You: ", "")
        
        if st.button("Send"):
            response = self.model.generate_response(user_input)
            st.text_area("Bot:", response, height=200)

    def get_user_input(self):
        user_input = st.text_input("You: ", "")
        return user_input

    def run(self):
        st.title("Chatbot Interface")
        user_input = self.get_user_input()

        if st.button("Send"):
            response = self.model.generate_response(user_input)
            st.text_area("Bot:", response, height=200)

    def prompt_for_parameters(self):
        st.title("Chatbot con LLM")
        prompt = st.text_input("Escribe tu mensaje:")
        return prompt

    def show_response(self, response):
        st.write("Respuesta del modelo:")
        st.write(response)