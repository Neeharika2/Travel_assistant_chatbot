# DeepSeek AI Chatbot

A simple chatbot built with DeepSeek AI and LangChain, wrapped in a Streamlit interface.

## Setup

1. Run the setup script to create a virtual environment and install dependencies:
   ```
   setup.bat
   ```

2. Activate the virtual environment (if not already activated):
   ```
   venv\Scripts\activate
   ```

3. Run the chatbot:
   ```
   streamlit run app.py
   ```

## Features

- Simple chat interface
- Powered by DeepSeek AI language model
- Chat history maintained during the session
- Clean and responsive UI with Streamlit
- Easy setup with included batch script

## Configuration

API keys are stored in the `.env` file. Make sure this file is included in your `.gitignore` if you're using version control.

## How it works

The application uses:
- **Streamlit**: For the web interface
- **DeepSeek API**: To generate responses from the AI model
- **python-dotenv**: To securely load API keys from the environment

The chat history is maintained during your session, allowing for contextual conversations.
