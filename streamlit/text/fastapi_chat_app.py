# app.py
import os
import streamlit as st
import requests
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
FASTAPI_URL = "http://localhost:8000/stream_chat"  # TODO: pass dynamically

st.title("🦜🔗 Chat Demos")

# Hide deploy button
st.markdown(
    r"""
    <style>
    .stAppDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)

if not OPENAI_API_KEY:
    OPENAI_API_KEY = st.sidebar.text_input("OpenAI API Key", type="password")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def stream_from_fastapi(url, data):
    """Stream response from FastAPI server"""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
    }

    with requests.post(url, json=data, headers=headers, stream=True) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    content = line[6:]  # Remove 'data: ' prefix
                    yield content

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        data = {
            "messages": [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            "model": st.session_state["openai_model"]
        }
        stream = stream_from_fastapi(FASTAPI_URL, data)
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})