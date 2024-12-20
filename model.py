import openai
import streamlit as st

# Initialize the OpenAI client with API key from secrets
openai.api_key = st.secrets["OpenAIKey"]

# Function to create a thread and send a message
def create_thread_with_message(messages):
    try:
        # Create a new thread with an initial message
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Specify the model you'd like to use
            messages=messages,  # List of messages to start the thread with
            max_tokens=150,  # Optional: Control the maximum response length
        )

        # The response will contain the assistant's response
        return response.choices[0].message["content"]
    
    except Exception as e:
        st.error(f"Error with OpenAI Assistant API: {e}")
        return None
