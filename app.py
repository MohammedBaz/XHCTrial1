import streamlit as st
from model import get_openai_response

# Streamlit app layout
st.title("ChatGPT-like Assistant")

# Initialize session state to keep track of the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores the chat history

# Display previous messages (user and assistant)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input for a new message
if user_input := st.chat_input("Ask me something:"):
    # Append the user's message to the session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Fetch the response from OpenAI
    assistant_message = interact_with_assistant(st.session_state.messages)
    
    if assistant_message:  # Check if a response is received
        # Append the assistant's response to the chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        # Display the assistant's response
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
    else:
        st.error("Failed to fetch response from OpenAI.")
