import openai
import streamlit as st

# Initialize the OpenAI client with API key from secrets
openai.api_key = st.secrets["OpenAIKey"]

# Function to get OpenAI response
def get_openai_response(messages, model="gpt-4"):
    try:
        # Send request to the OpenAI API with the required arguments: model, messages
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,  # Messages should be passed as a list of dictionaries
            max_tokens=150,  # Optional: Set max tokens for the response
        )

        # Return the assistant's message from the response
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        st.error(f"Error with OpenAI Assistant API: {e}")
        return None
