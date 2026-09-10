import io
import speech_recognition as sr

def transcribe_audio(audio_bytes: bytes) -> str:
    """Takes audio bytes from audio_recorder and transcribes to text."""
    if not audio_bytes:
        return ""
    
    recognizer = sr.Recognizer()
    try:
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="en-US")
            except Exception:
                text = recognizer.recognize_google(audio_data, language="ar-EG")
            return text
    except sr.UnknownValueError:
        return "Error: Could not understand audio"
    except sr.RequestError as e:
        return f"Error: Speech service request failed ({e})"
    except Exception as e:
        return f"Error: {str(e)}"