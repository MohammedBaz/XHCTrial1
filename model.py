from openai import OpenAI
import streamlit as st

# Initialize the OpenAI client with API key from secrets
client = OpenAI(api_key=st.secrets["OpenAIKey"])

# Function to generate a response from a pre-configured Assistant
def get_openai_response(messages, assistant_id):
    """
    Fetch a response from the specified OpenAI Assistant.
    
    :param messages: List of messages (user and assistant chat history).
    :param assistant_id: ID of the pre-configured Assistant.
    :return: Assistant's response message object or None if an error occurs.
    """
    try:
        # OpenAI chat completion call for the specific Assistant
        completion = client.chat.completions.create(
            assistant=assistant_id,
            messages=messages
        )
        return completion.choices[0].message  # Returning the assistant's message object
    except Exception as e:
        st.error(f"Error with OpenAI Assistant API: {e}")
        return None
