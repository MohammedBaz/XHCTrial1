from openai import OpenAI
import streamlit as st

# Initialize the OpenAI client with API key from secrets
client = OpenAI(api_key=st.secrets["OpenAIKey"]["api_key"])

# Function to generate a response from the OpenAI API
def get_openai_response(messages, model="gpt-4o-mini"):
    try:
        # OpenAI chat completions API call
        completion = client.chat.completions.create(
            model=model,
            store=True,
            messages=messages
        )
        return completion.choices[0].message  # Returning the assistant's message object
    except Exception as e:
        st.error(f"Error with OpenAI API: {e}")
        return None
