import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

# Allow your website to talk to the bot
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
chat_session = client.chats.create(model="gemini-2.0-flash-exp")

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = chat_session.send_message(request.prompt)
        return {"response": response.text}
    except Exception as e:
        return {"response": f"AI_ERROR: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    # MUST use 0.0.0.0 and 7860
    uvicorn.run(app, host="0.0.0.0", port=7860)
