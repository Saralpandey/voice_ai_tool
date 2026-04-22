import os
from groq import Groq
from dotenv import load_dotenv
from app.services.memory_service import get_memory, add_to_memory


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(user_text, session_id="default"):
    try:
        emotion = detect_emotion(user_text)
        language = detect_language(user_text)

        system_prompt = f"""
        You are a high-quality AI voice assistant for Indian users.

        Rules:
        - Always give clear, correct, and useful answers
        - If question is technical → explain simply with examples
        - If question is general → answer naturally like a human
        - Keep response short but meaningful (not 1 line useless answer)
        - Respond in {language}
        - Match emotion: {emotion}

        If you don't know something, say it honestly.
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant"
        )

        response = chat_completion.choices[0].message.content

        return response, emotion, language

    except Exception as e:
        print("LLM ERROR:", e)
        return "Sorry, something went wrong.", "neutral", "english"

def detect_emotion(text):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Detect the emotion of the user's sentence. Reply with only one word from: happy, sad, angry, neutral."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            model="llama-3.1-8b-instant"
        )

        return response.choices[0].message.content.strip().lower()

    except:
        return "neutral"

def detect_language(text):
    try:
        result = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Detect the language of the user input. Reply with only one word: english or hindi."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            model="llama-3.1-8b-instant"
        )

        return result.choices[0].message.content.strip().lower()

    except:
        return "english"