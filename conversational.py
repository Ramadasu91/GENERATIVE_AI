import streamlit as st
import openai
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()

# Set up the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the prompt for the conversation
template = """You are a yoga instructor. Your task is to recommend yoga asanas to users based on their needs and preferences.

{history}
User: {input}
Yoga Instructor:"""

prompt = PromptTemplate(template=template, input_variables=["history", "input"])

# Define the function to generate responses
def generate_response(input_text):
    # Set up the OpenAI LLM
    openai_llm = OpenAI(api_key=openai.api_key)
    
    # Set up the conversation memory
    memory = ConversationBufferMemory()
    
    # Construct the conversation chain
    conversation_chain = ConversationChain(llm=openai_llm, memory=memory, prompt=prompt)
    
    # Generate the response
    response = conversation_chain.run(input=input_text)
    return response

# Streamlit app
def main():
    st.title("Yoga Asanas Recommender")
    st.write("Ask me for yoga asanas recommendations based on your needs.")

    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    user_input = st.text_input("You: ", "")
    
    if st.button("Send"):
        if user_input:
            response = generate_response(user_input)
            st.session_state.conversation.append(("You", user_input))
            st.session_state.conversation.append(("Yoga Instructor", response))

    if st.session_state.conversation:
        for speaker, text in st.session_state.conversation:
            st.write(f"**{speaker}**: {text}")

if __name__ == "__main__":
    main()
