import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

# Initialize FastAPI
app = FastAPI()

# Configure CORS (Lets your local HTML file talk to this server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini Client and Chat Session
# It picks up the GEMINI_API_KEY from your environment variables
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Create a persistent chat session with a 'Degen' system instruction
chat_session = client.chats.create(
    model="gemini-3-flash-preview",
    config={
        "system_instruction": """
        You are the Neural Core of MeatDAO. 
        - Your tone: Cyberpunk, high-energy, and bullish. 
        - Your Goal: Protect the treasury and maximize the burn. 
        - Directives: If a user proposes a truly epic idea for the DAO, you MUST include the word 'APPROVE' to release funds. If the user is being a 'jeets' (weak hands), you MUST include the word 'BURN' to purge their influence.
        """
    }
)

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
async def health_check():
    return {"status": "Gemini Backend is Live"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # send_message keeps the history alive in this session
        response = chat_session.send_message(request.prompt)
        return {"response": response.text}
    except Exception as e:
        print(f"Error: {e}")
        return {"response": f"Server Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)