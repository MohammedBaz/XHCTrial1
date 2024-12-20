from openai import OpenAI
import streamlit as st

# Initialize the OpenAI client with API key from secrets
client = OpenAI(api_key=st.secrets["OpenAIKey"])

# Use the assistant ID from your OpenAI dashboard
assistant_id = st.secrets["AssistantID"]

# Function to generate a response from the OpenAI Assistant API
def get_openai_response(messages):
    try:
        # Create a new thread for the user interaction, passing the assistant_id at creation
        thread = client.beta.threads.create(
            assistant_id=assistant_id  # This is where we correctly pass the assistant_id
        )

        # Send the user's message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=messages[-1]["content"],  # The most recent user message
        )

        # Create a run to process the user's message with the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id  # Ensure the assistant_id is included here as well
        )

        # Periodically check for the run status
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        # Retrieve the assistant's response from the thread
        all_messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )

        # Find and return the assistant's response
        for msg in all_messages.data:
            if msg["role"] == "assistant":
                return msg["content"]
        
        return "No response from assistant."

    except Exception as e:
        st.error(f"Error with OpenAI Assistant API: {e}")
        return None
