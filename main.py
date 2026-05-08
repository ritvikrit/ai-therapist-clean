from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import tempfile
import os
import io

# -----------------------------
# LOAD ENV VARIABLES
# -----------------------------
load_dotenv()

# -----------------------------
# OPENAI CLIENT
# -----------------------------
client = OpenAI() # Ensure OPENAI_API_KEY is in your .env

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# MEMORY (Simplified for demo)
# NOTE: In production, use a Session ID or Database
# -----------------------------
conversation_history = []

# -----------------------------
# SYSTEM PROMPT
# -----------------------------
SYSTEM_PROMPT = """
You are a calm and emotionally supportive AI therapist.
Speak warmly and naturally. Keep responses concise.
Ask thoughtful follow-up questions.
Do not use markdown. Do not use emojis.
Your responses will be spoken aloud.
"""

# -----------------------------
# VOICE ENDPOINT
# -----------------------------
@app.post("/voice")
async def voice_chat(audio: UploadFile = File(...)):
    temp_audio_path = None
    try:
        # 1. SAVE TEMP AUDIO FILE
        # Using a context manager for safety
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            content = await audio.read()
            temp_audio.write(content)
            temp_audio_path = temp_audio.name

        # 2. SPEECH TO TEXT (Whisper)
        with open(temp_audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )
        
        user_text = transcript.text
        if not user_text:
            raise HTTPException(status_code=400, detail="No speech detected")

        # 3. UPDATE MEMORY
        conversation_history.append({"role": "user", "content": user_text})

        # 4. GPT RESPONSE (LLM)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *conversation_history[-10:] # Keep context window manageable
            ]
        )
        ai_text = response.choices[0].message.content

        # 5. SAVE AI MEMORY
        conversation_history.append({"role": "assistant", "content": ai_text})

        # 6. TEXT TO SPEECH (TTS)
        # Fix: Using the correct model "tts-1"
        speech_response = client.audio.speech.create(
            model="tts-1", 
            voice="alloy",
            input=ai_text,
        )

        # 7. STREAM RESPONSE
        # We use a BytesIO stream to return the audio without saving to disk
        return StreamingResponse(
            io.BytesIO(speech_response.content),
            media_type="audio/mpeg"
        )

    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}

    finally:
        # CLEANUP: Ensure the temp file is deleted even if an error occurs
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

# -----------------------------
# ROOT ENDPOINT
# -----------------------------
@app.get("/")
async def root():
    return {"status": "online", "agent": "AI Therapist"}