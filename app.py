import streamlit as st
import pandas as pd
import re
from model import get_openai_response

# Load the healthcare dataset
@st.cache_data
def load_data():
    return pd.read_csv("healthcare_data.csv")

data = load_data()

# Filter the data based on the "District" column (for Taif only)
taif_data = data[data["District"] == "Taif"]

# Streamlit app layout
st.title("Healthcare Facility Data for Taif")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages in the chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input for a new message
if user_input := st.chat_input("Ask a question about the healthcare data:"):
    # Append user's message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Function to identify the intent based on keywords
    def identify_intent(query):
        if re.search(r'\b(hospital|clinic|polyclinic)\b', query, re.IGNORECASE):
            return "facility_names"
        elif re.search(r'\b(doctors|nurses)\b', query, re.IGNORECASE):
            return "staff_count"
        elif re.search(r'\b(satisfaction|patient satisfaction)\b', query, re.IGNORECASE):
            return "avg_satisfaction"
        elif re.search(r'\b(waiting time)\b', query, re.IGNORECASE):
            return "avg_waiting_time"
        elif re.search(r'\b(beds|occupancy)\b', query, re.IGNORECASE):
            return "total_beds"
        else:
            return "openai_query"

    # Determine the intent based on user input
    intent = identify_intent(user_input)

    # Handle different intents
    if intent == "facility_names":
        # Query for the names of all facilities in Taif
        hospital_data = taif_data[taif_data['Type'] == 'Hospital']
        facility_names = hospital_data["Facility Name"].tolist()
        assistant_response = f"The hospitals in Taif are: {', '.join(facility_names)}."

    elif intent == "staff_count":
        # Query the total number of doctors or nurses in Taif
        if "doctor" in user_input.lower():
            doctor_count = taif_data["Doctors"].sum()
            assistant_response = f"The total number of doctors in Taif is {doctor_count}."
        elif "nurse" in user_input.lower():
            nurse_count = taif_data["Nurses"].sum()
            assistant_response = f"The total number of nurses in Taif is {nurse_count}."
        else:
            assistant_response = "Please specify whether you're asking for the number of doctors or nurses."

    elif intent == "avg_satisfaction":
        # Query the average patient satisfaction in Taif
        avg_satisfaction = taif_data["PatientSatisfaction"].mean()
        assistant_response = f"The average patient satisfaction in Taif is {avg_satisfaction:.2f}."

    elif intent == "avg_waiting_time":
        # Query the average waiting time in Taif
        avg_waiting_time = taif_data["WaitingTime"].mean()
        assistant_response = f"The average waiting time in Taif is {avg_waiting_time:.2f}."

    elif intent == "total_beds":
        # Query the total number of beds in Taif
        total_beds = taif_data["Beds"].sum()
        assistant_response = f"The total number of beds in Taif is {total_beds}."

    else:
        # For complex or general queries, use OpenAI to get an answer
        assistant_message = get_openai_response(st.session_state.messages)
        if assistant_message:
            assistant_response = assistant_message.content
        else:
            assistant_response = "Sorry, I could not understand your question."

    # Append assistant's response to session state and display it
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
