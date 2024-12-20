import streamlit as st
from openai import OpenAI
import time

# Initialize the OpenAI client
client = OpenAI(api_key=st.secrets["OpenAIKey"])

# Function to interact with the OpenAI Assistant
def interact_with_assistant(user_query):
    # 1. Create a thread (or retrieve an existing thread ID from session state)
    if "thread_id" not in st.session_state:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    # Get the thread ID (either newly created or from session state)
    thread_id = st.session_state.thread_id

    # 2. Add a message to the thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_query,
        # Add file IDs if needed (after file upload): file_ids=[st.session_state.file_id]
    )

    # 3. Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=st.secrets["AssistantID"],
    )

    # 4. Periodically check for the run to complete and display messages
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        time.sleep(1)

        # Retrieve and display messages so far
        messages = client.beta.threads.messages.list(thread_id=thread_id, order="asc")
        for msg in messages:
            if msg.run_id == run.id or msg.created_at > run.created_at:  # Only show new messages
                with st.chat_message(msg.role):
                    st.markdown(msg.content[0].text.value)

    return run

# Streamlit UI components

st.title("CV Analysis Assistant")

# Initialize session state variables if they don't exist
if "file_id" not in st.session_state:
    st.session_state.file_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# File uploader
uploaded_file = st.file_uploader("Upload your CV", type=["pdf", "txt", "docx"])  # Add other supported formats
if uploaded_file is not None and st.session_state.file_id is None:
    # Upload the file to OpenAI and store the file ID in session state
    with st.spinner("Uploading file..."):
        file = client.files.create(file=uploaded_file, purpose="assistants")
        st.session_state.file_id = file.id

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_query = st.chat_input("What do you want to ask about the CV?")

# Handle user input
if user_query:
    # Add user message to the chat and session state
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Interact with the assistant
    with st.spinner("Thinking..."):
        run = interact_with_assistant(user_query)

    # (Optional) Store the run ID for later retrieval, if needed
    # st.session_state.run_id = run.id
