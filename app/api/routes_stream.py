from fastapi import APIRouter, WebSocket
from app.services.asr_service import speech_to_text
from app.services.llm_service import generate_response
from app.services.tts_service import text_to_speech
from app.services.memory_service import set_speaking, is_speaking

router = APIRouter()

@router.websocket("/ws/voice")
async def voice_stream(websocket: WebSocket):
    await websocket.accept()

    try:
        session_id = "user_1"

        while True:
            audio_bytes = await websocket.receive_bytes()

            # 🔥 INTERRUPT LOGIC
            if is_speaking(session_id):
                print("User interrupted → stopping current speech")
                set_speaking(session_id, False)

            text = speech_to_text(audio_bytes)

            response, emotion, language = generate_response(text, session_id)

            audio_path = text_to_speech(response, emotion, language)

            set_speaking(session_id, True)

            with open(audio_path, "rb") as f:
                audio_data = f.read()

            await websocket.send_bytes(audio_data)

            set_speaking(session_id, False)

    except Exception as e:
        print("WebSocket Error:", e)
        await websocket.close()
    