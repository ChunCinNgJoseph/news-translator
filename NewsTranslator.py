import streamlit as st
st.title("🚀 Hello from Streamlit!")
from streamlit_audiorecorder import audiorecorder
import whisper
import tempfile
import requests
from gtts import gTTS
import os

# Load Whisper model once
@st.cache_resource
def load_model():
    return whisper.load_model("base")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# LibreTranslate API call
def translate_text(text, source="en", target="fr"):
    response = requests.post(
        "https://libretranslate.de/translate",
        data={
            "q": text,
            "source": source,
            "target": target,
            "format": "text"
        }
    )
    return response.json()["translatedText"]

# Streamlit app UI
st.title("🎙️ Multilingual Speech-to-Speech Translator")
st.write("Record your voice, we'll transcribe it, translate it, and speak it back!")

# Record from mic
audio = audiorecorder("Click to record", "Recording...")

if len(audio) > 0:
    # Save audio input to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio)
        temp_audio_path = f.name

    # Playback original
    st.subheader("🎧 Your Recording")
    st.audio(temp_audio_path, format="audio/wav")

    # Transcribe with Whisper
    result = model.transcribe(temp_audio_path)
    transcribed = result["text"]
    st.subheader("📝 Transcribed Text")
    st.write(transcribed)

    # Target language selection
    target_lang = st.selectbox("🌍 Select target language", ["fr", "es", "de", "hi", "zh"])

    # Translate
    translated = translate_text(transcribed, source="en", target=target_lang)
    st.subheader("🌐 Translated Text")
    st.write(translated)

    # Text-to-Speech
    tts = gTTS(translated, lang=target_lang)
    tts.save("output.mp3")
    st.subheader("🔊 Translated Speech")
    audio_file = open("output.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")
