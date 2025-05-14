import os
import streamlit as st
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY") 
MODEL = os.getenv("DEEPSEEK_MODEL")       
API_URL = "https://openrouter.ai/api/v1/chat/completions"  


st.set_page_config(
    page_title="OpenRouter AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("AI Chatbot")
st.caption("✈️ Try asking me things like 'Plan a 3-day trip to Tokyo under $500', or 'Suggest food spots in Paris for vegetarians'.")

TRAVEL_KEYWORDS = [
    'travel', 'trip', 'vacation', 'holiday', 'tour', 'journey', 'excursion',
    'destination', 'itinerary', 'flight', 'hotel', 'resort', 'hostel', 'airbnb', "go", "go to", "going to",
    'booking', 'reservation', 'airport', 'airplane', 'train', 'bus', 'car rental',
    'sightseeing', 'tourist', 'tourism', 'backpacking', 'cruise', 'beach', 'mountain','hiking',
    'camping', 'passport', 'visa', 'currency','exchange rate', 'budget','cost', 'expense', 'landmark',
    'attraction', 'museum', 'restaurant', 'cafe','food', 'cuisine', 'local', 'guide', 'map', 
    'direction', 'transportation','luggage',
    'packing', 'weather', 'season', 'place', 'world',
    'adventure', 'explore', 'discover','city', 'country', 'continent', 'international', 'domestic', 
    'roadtrip','culture', 'language', 'translate', 'souvenir', 'photo', 'memory', 'experience'
]


def is_travel_related(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in TRAVEL_KEYWORDS)


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


def get_ai_response(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",  
    }
    
    payload = {
        "model": MODEL,
        "messages": messages
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  
        
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return "I'm sorry, I encountered an error while processing your request."

for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    if is_travel_related(prompt):
        api_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages
            if msg["role"] in ["user", "assistant"]
        ]
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_ai_response(api_messages)
                st.write(response)
    else:
        response = "I'm your travel assistant, designed to help with travel-related questions and planning. Could you please ask me something about travel, destinations, flights, accommodations, or activities? I'd be happy to assist you with your travel needs!"
        
        with st.chat_message("assistant"):
            st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})


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
