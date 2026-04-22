import whisper
import tempfile
import os
from app.utils.audio_utils import reduce_noise
from pydub import AudioSegment


model = whisper.load_model("medium")  # fast + decent accuracy
def speech_to_text(audio_bytes):


    # save incoming (webm)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_in:
        temp_in.write(audio_bytes)
        webm_path = temp_in.name

    # convert to wav
    wav_path = webm_path.replace(".webm", ".wav")

    audio = AudioSegment.from_file(webm_path, format="webm")
    audio.export(wav_path, format="wav")

    # transcribe
    result = model.transcribe(wav_path)

    # cleanup
    os.remove(webm_path)
    os.remove(wav_path)

    return result["text"]