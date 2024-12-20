from openai import OpenAI
import streamlit as st
import time
# Initialize the OpenAI client with API key from secrets

client = OpenAI(api_key=st.secrets["OpenAIKey"])
def interact_with_assistant(user_query):
    # 1. Create a thread
    thread = client.beta.threads.create()

    # 2. Add a message to the thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_query,
    )

    # 3. Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=st.secrets["AssistantID"]
    )

    # 4. Wait for the run to complete (you might want to add more robust polling/waiting logic)
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
