from gtts import gTTS
import os
import uuid

def text_to_speech(text , emotion="neutral" , language="english"):

    filename = f"audio_{uuid.uuid4().hex}.mp3"
    file_path = f"app/audio_output/{filename}"

    os.makedirs("app/audio_output", exist_ok=True)

    # language mapping
    lang_code = "hi" if language == "hindi" else "en"

    # emotion-based speed
    slow = True if emotion == "sad" else False

    
    tts = gTTS(text=text, lang=lang_code, slow=slow)
    tts.save(file_path)

    return file_path