import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Initialize Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. CREATE SESSION HERE (After client, before routes)
# This creates a persistent conversation that stays alive as long as the server is running
chat_session = client.chats.create(model="gemini-3-flash-preview")

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"status": "Gemini Backend is Live"}

# New route for persistent chat
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Use send_message instead of generate_content to use the history
        response = chat_session.send_message(request.prompt)
        return {"response": response.text}
    except Exception as e:
        print(f"Chat Error: {e}")
        return {"response": f"Chat Error: {str(e)}"}

# Original route for one-off generations
@app.post("/generate")
async def generate_response(request: ChatRequest):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=request.prompt
        )
        return {"response": response.text}
    except Exception as e:
        return {"response": f"AI Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)