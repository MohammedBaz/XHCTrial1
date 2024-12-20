import streamlit as st
from model import get_openai_response

# Streamlit app layout
st.title("ChatGPT-like Clone")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores the chat history

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input for a new message
if user_input := st.chat_input("Ask me something:"):
    # Append user's message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Fetch the response from OpenAI
    assistant_message = get_openai_response(st.session_state.messages)
    if assistant_message:  # Check if a response is received
        # Access the assistant's message attributes directly
        st.session_state.messages.append({"role": "assistant", "content": assistant_message.content})

        # Display the assistant's response
        with st.chat_message("assistant"):
            st.markdown(assistant_message.content)
    else:
        st.error("Failed to fetch response from OpenAI.")
