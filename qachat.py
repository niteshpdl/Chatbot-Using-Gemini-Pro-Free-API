import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the API key
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("No API key found. Please check your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=API_KEY)

## function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

## initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    full_response = ""
    for chunk in response:
        text = chunk.text
        full_response += text
        st.write(text)
    
    st.session_state['chat_history'].append(("Bot", full_response))

st.subheader("The Chat History is")
    
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")