from openai import OpenAI
import streamlit as st

# Initialize the OpenAI client with API key from secrets
client = OpenAI(api_key=st.secrets["OpenAIKey"])

# Function to generate a response from a pre-configured Assistant
from openai import OpenAI
import streamlit as st

# Initialize the OpenAI client with API key from secrets
client = OpenAI(api_key=st.secrets["OpenAIKey"])

# Function to generate a response from the OpenAI Assistant
def get_openai_response(messages, assistant_id):
    try:
        # Call the assistant's chat endpoint
        response = client.assistants.chat.create(
            assistant_id=assistant_id,  # Assistant ID from secrets
            messages=messages           # Messages from the user and assistant
        )
        return response.choices[0].message  # Return the assistant's response
    except Exception as e:
        st.error(f"Error with OpenAI Assistant API: {e}")
        return None

