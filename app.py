import streamlit as st
from model import get_openai_response

# Streamlit app layout
st.title("Healthcare Chat Assistant")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores the chat history

# Display previous messages in chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input for a new message
if user_input := st.chat_input("Ask me something about healthcare:"):
    # Append user's message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Fetch the response from OpenAI Assistant
    assistant_message = get_openai_response(
        messages=st.session_state.messages,
        assistant_id=st.secrets["AssistantID"]  # Read assistant_id from secrets
    )

    if assistant_message:  # Check if a response is received
        # Append assistant's response to session state
        st.session_state.messages.append({"role": "assistant", "content": assistant_message.content})

        # Display the assistant's response
        with st.chat_message("assistant"):
            st.markdown(assistant_message.content)
    else:
        st.error("Failed to fetch response from OpenAI Assistant.")
