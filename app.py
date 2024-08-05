import streamlit as st
from langchain.llms import GoogleGenerativeAI  # Replace with desired LLM (e.g., Gemini API)
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")  # Replace with "GOOGLE_GENERATIVE_API_KEY" if using Gemini API

# Initialize Langchain LLM model (replace with desired model)
llm = GoogleGenerativeAI(model_name="your_gemini_model_name", api_key=api_key)  # Replace with actual model name

# Streamlit UI Configuration (Enhanced Styling & Responsiveness)
st.set_page_config(
    page_title="Medical Chatbot 🩺",
    page_icon="🩺",
    layout="wide",
)

st.title("Your AI Healthcare Assistant 🩺")

st.markdown(
    """
    <style>
        body {
            background-color: #f0f2f6;
            margin: 0;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            height: 100vh;
            justify-content: center;
            align-items: center;
        }
        .container {
            max-width: 800px;
            padding: 20px;
            border-radius: 10px;
            background-color: #fff;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
            display: flex;
            flex-direction: column;
            align-items: stretch;
        }
        .chat-history {
            list-style: none;
            padding: 0;
            margin: 0;
            flex-grow: 1;
            overflow-y: scroll;
        }
        .chat-message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            white-space: pre-wrap;
            word-wrap: break-word;  /* Ensure text wraps to container width */
        }
        .user-message {
            background-color: #d1e7dd;
            justify-content: flex-start;
        }
        .bot-message {
            background-color: #fff3cd;
            justify-content: flex-end;
        }
        .user-message p, .bot-message p {
            margin: 0;
        }
        .user-name, .bot-name {
            font-weight: bold;
            margin-right: 10px;
        }
        .input-container {
            display: flex;
            align-items: center;
            margin-top: 20px;
        }
        .input-field {
            flex: 1;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .send-button {
            background-color: #6c63ff;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        @media only screen and (max-width: 768px) {
            .container {
                max-width: 100%;
            }
            .chat-message {
                font-size: 14px;  /* Adjust font size for smaller screens */
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.write(
    "What medical questions do you have today? (Disclaimer: I am not a medical professional. Please consult a doctor for any medical advice.)"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Function to generate response using LLM
def get_response(question):
    # Replace with your actual Gemini API interaction logic
    # (consider confidentiality of API keys)
    gemini_api_url = "https://api.gemini.org/vX/interpret"  # Replace with actual API URL
    headers = {"Authorization": f"Bearer {api_key}"}  # Set authorization header with API key
    data = {"text": question}  # Create payload for API request

    try:
        response = requests.post(gemini_api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        # Parse JSON response and extract relevant information
        response_data = response.json()
        interpretation = response_data.get("interpretation", {})
        possible_diagnoses = interpretation.get("possible_diagnoses", [])
        treatment_suggestions = interpretation.get("treatment_suggestions", [])

        # Craft a response combining Gemini API data and a disclaimer
        response_text = (
            f"Here's what I found based on the Gemini API:\n\n"
            f"**Possible Diagnoses:**\n"
        )
        for diagnosis in possible_diagnoses:
            response_text += f"- {diagnosis}\n"

        if treatment_suggestions:
            response_text += (
                "\n**Treatment Suggestions (Disclaimer: Please consult a doctor for any medical advice):**\n"
            )
            for suggestion in treatment_suggestions:
                response_text += f"- {suggestion}\n"

        response_text += "\n**Disclaimer:** I am not a medical professional and this information should not be used as a substitute for medical advice. Please consult a doctor for any medical concerns."

        return response_text

    except requests.exceptions.RequestException as e:
        # Handle API request errors gracefully
        return f"An error occurred while communicating with the Gemini API: {e}"

