
import streamlit as st
import subprocess
import whisper
from transformers import pipeline
import os

# Functions without logging
def detect_ffmpeg_path():
    try:
        result = subprocess.run(["where", "ffmpeg"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except Exception:
        pass
    return "ffmpeg"  # fallback

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False

def extract_audio(video_path, audio_path="audio.wav", ffmpeg_cmd="ffmpeg"):
    command = [ffmpeg_cmd, "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path]
    subprocess.run(command, check=True)
    return audio_path

def transcribe_audio(audio_path, model_name="medium"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result["text"], result["language"]

def translate_to_english(text):
    translator = pipeline("translation", model="Helsinki-NLP/opus-mt-mul-en")
    translation = translator(text, max_length=512)
    return translation[0]['translation_text']

def video_to_english_transcript(video_path, ffmpeg_cmd):
    audio_path = extract_audio(video_path, ffmpeg_cmd=ffmpeg_cmd)
    transcript, detected_lang = transcribe_audio(audio_path)
    if detected_lang != "en":
        transcript = translate_to_english(transcript)
    return transcript

# Streamlit UI
st.title("🎥 Video to English Transcript")
st.write("Upload a video file to extract and translate its audio into English.")

uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mkv", "avi"])

if uploaded_file:
    temp_video_path = os.path.join("temp_video.mp4")
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.read())

    ffmpeg_cmd = "ffmpeg"
    if not check_ffmpeg():
        ffmpeg_cmd = detect_ffmpeg_path()
        if ffmpeg_cmd == "ffmpeg":
            st.error("FFmpeg not found. Please install FFmpeg and add it to PATH.")
            st.stop()

    st.info("Processing video... This may take a few minutes.")
    try:
        transcript = video_to_english_transcript(temp_video_path, ffmpeg_cmd)
        st.success("Transcript generated successfully!")
        st.text_area("English Transcript", transcript, height=300)

        # Download option
        st.download_button(
            label="Download Transcript",
            data=transcript,
            file_name="transcript.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
