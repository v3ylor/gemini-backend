from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # New Import
from pydantic import BaseModel
from google import genai
import os

app = FastAPI()

# --- CORS SETUP ---
# This allows your local website to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, "*" allows any site to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key="YOUR_API_KEY_HERE")

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"status": "Gemini Backend is Live"}

@app.post("/generate")
async def generate_response(request: ChatRequest):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=request.prompt
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) # Changed 0.0.0.0 to 127.0.0.1