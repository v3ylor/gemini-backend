import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
chat_session = client.chats.create(model="gemini-2.0-flash-exp")

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(request: ChatRequest):
    response = chat_session.send_message(request.prompt)
    return {"response": response.text}

if __name__ == "__main__":
    import uvicorn
    # Critical: Use port 7860 for Hugging Face
    uvicorn.run(app, host="0.0.0.0", port=7860)
