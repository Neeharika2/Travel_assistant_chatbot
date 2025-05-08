import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API settings
API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Using the existing env var but for OpenRouter
MODEL = os.getenv("DEEPSEEK_MODEL")       # Model name to use with OpenRouter
API_URL = "https://openrouter.ai/api/v1/chat/completions"  # OpenRouter endpoint

# Configure page settings
st.set_page_config(
    page_title="OpenRouter AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# App title and description
st.title("AI Chatbot")
st.caption("✈️ Try asking me things like 'Plan a 3-day trip to Tokyo under $500', or 'Suggest food spots in Paris for vegetarians'.")
st.write("🌍 Paris in Spring is amazing! Here's your 5-day itinerary:")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a smart and friendly travel assistant. "
                "You help users plan trips, suggest destinations, find hotels and flights, "
                "recommend food, activities, local tips, and answer travel-related questions. "
                "Always ask for the destination, dates, budget, and preferences if not provided."
            )
        },
        {
            "role": "assistant",
            "content": "Hello! I'm your travel assistant. Where are you planning to go?"
        }
    ]

# Function to call OpenRouter API
def get_ai_response(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",  # OpenRouter requires this header
        "X-Title": "Streamlit AI Chatbot"         # Optional for analytics
    }
    
    payload = {
        "model": MODEL,
        "messages": messages
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return "I'm sorry, I encountered an error while processing your request."

# Display chat history
for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get API messages format (excluding system messages for display)
    api_messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.messages
        if msg["role"] in ["user", "assistant"]
    ]
    
    # Display thinking message
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(api_messages)
            st.write(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add some styling
st.markdown("""
    <style>
        .stChatMessage {
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .stChatMessage[data-test="user"] {
            background-color: #e6f7ff;
        }
        .stChatMessage[data-test="assistant"] {
            background-color: #f0f2f5;
        }
    </style>
""", unsafe_allow_html=True)
