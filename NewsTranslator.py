import streamlit as st
import whisper
import tempfile
import requests
from gtts import gTTS
import os

# Set page info
st.set_page_config(page_title="Multilingual Speech-to-Speech Translator")
st.title("🎙️ Multilingual Speech-to-Speech Translator")
st.write("Upload your voice file, and we'll transcribe, translate, and speak it back!")

# Load Whisper model (cached)
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# Translation function
def translate_text(text, source="en", target="fr"):
    response = requests.post(
        "https://libretranslate.de/translate",
        data={"q": text, "source": source, "target": target, "format": "text"},
    )
    return response.json()["translatedText"]

# File uploader UI
audio_file = st.file_uploader("📁 Upload a .wav or .mp3 file", type=["wav", "mp3"])

if audio_file is not None:
    # Save uploaded audio to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        temp_path = tmp.name

    st.audio(temp_path, format="audio/wav")

    # Transcribe
    result = model.transcribe(temp_path)
    transcribed = result["text"]
    st.subheader("📝 Transcribed Text")
    st.write(transcribed)

    # Language selector
    target_lang = st.selectbox("🌍 Translate to:", ["fr", "es", "de", "hi", "zh"])

    # Translate
    translated = translate_text(transcribed, source="en", target=target_lang)
    st.subheader("🌐 Translated Text")
    st.write(translated)

    # Text-to-Speech
    tts = gTTS(translated, lang=target_lang)
    tts.save("output.mp3")
    st.subheader("🔊 Translated Speech")
    audio_out = open("output.mp3", "rb")
    st.audio(audio_out.read(), format="audio/mp3")
