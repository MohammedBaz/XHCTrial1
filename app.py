# app.py
import streamlit as st
from model import Assistant

# Initialize the assistant
API_KEY = st.secrets["OpenAIKey"]
ASSISTANT_ID = st.secrets["AssistantID"]
assistant = Assistant(api_key=API_KEY, assistant_id=ASSISTANT_ID)

st.title("AI-Powered CV Assistant")

# Session state management
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# File uploader
uploaded_file = st.file_uploader("Upload your CV (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])
if uploaded_file and "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = uploaded_file.name
    st.success(f"File '{uploaded_file.name}' uploaded successfully.")

# Display previous messages
if st.session_state.messages:
    for message in st.session_state.messages:
        role, content = message
        with st.chat_message(role):
            st.markdown(content)

# Chat input
user_query = st.chat_input("What would you like to ask about the CV?")

if user_query:
    # Add user message
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append(("user", user_query))

    # Interact with assistant
    with st.spinner("Processing your query..."):
        responses = assistant.interact_with_assistant(
            user_query, thread_id=st.session_state.thread_id
        )

    # Display assistant responses
    for response in responses:
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append(("assistant", response))
