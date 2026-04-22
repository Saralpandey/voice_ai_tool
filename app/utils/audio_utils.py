import noisereduce as nr
import numpy as np
from scipy.io import wavfile
import tempfile

def reduce_noise(audio_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(audio_bytes)
        temp_path = temp.name

    rate, data = wavfile.read(temp_path)

    # apply noise reduction
    reduced = nr.reduce_noise(y=data, sr=rate)

    wavfile.write(temp_path, rate, reduced)

    with open(temp_path, "rb") as f:
        cleaned_audio = f.read()

    return cleaned_audio