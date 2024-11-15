from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict
import json

load_dotenv()
app = FastAPI()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.get("/")
def read_root():
    return {"New Phone": "Who Dis?"}

@app.post("/stream_chat")
async def stream_chat(request: Request):

    data = await request.json()
    messages: List[Dict] = data.get("messages", [])
    model: str = data.get("model", "gpt-3.5-turbo")

    async def generate():
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                # Yield in the format Streamlit expects
                yield f"data: {chunk.choices[0].delta.content}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
