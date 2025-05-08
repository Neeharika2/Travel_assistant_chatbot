@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing required packages...
pip install streamlit python-dotenv langchain requests

echo Setup completed! Run the chatbot with: streamlit run app.py
