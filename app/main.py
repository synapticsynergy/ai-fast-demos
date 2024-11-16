from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers import chat, image_classify


load_dotenv()
app = FastAPI()

app.include_router(chat.router)
app.include_router(image_classify.router)

@app.get("/")
def read_root():
    return {"New Phone": "Who Dis?"}
