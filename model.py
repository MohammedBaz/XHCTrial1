import openai
import streamlit as st

# Initialize the OpenAI client with API key from secrets
openai.api_key = st.secrets["OpenAIKey"]
ASSISTANT_ID=st.secrets["AssistantID"]
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
        assistant_id=ASSISTANT_ID,
    )

    # 4. Wait for the run to complete (you might want to add more robust polling/waiting logic)
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(2)

    # 5. Get the assistant's response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_response = messages.data[0].content[0].text.value  # Get the last message (assistant's response)

    return assistant_response
