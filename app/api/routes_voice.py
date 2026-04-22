from fastapi import APIRouter, UploadFile, File
from app.services.asr_service import speech_to_text
from app.services.llm_service import generate_response
from app.services.tts_service import text_to_speech
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/voice")
async def voice_chat(file: UploadFile = File(...)):
    
    audio_bytes = await file.read()

    # Step 1: Speech → Text
    text = speech_to_text(audio_bytes)

    session_id = "user_1"
    # Step 2: Text → Response + Emotion
    response, emotion , language = generate_response(text,session_id)

    # Step 3: Text → Speech
    audio_output = text_to_speech(response, emotion , language)

    return FileResponse(audio_output, media_type="audio/mpeg")