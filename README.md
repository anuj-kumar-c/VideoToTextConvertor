# Video to English Transcript App

This guide explains how to set up and run a **Streamlit app** that converts video files into English transcripts using **OpenAI Whisper** and **Hugging Face translation models**.

---

## ✅ Features
- Upload a video file (`.mp4`, `.mov`, `.avi`)
- Extract audio using FFmpeg
- Transcribe audio using Whisper (supports multiple languages)
- Translate transcript to English if needed
- Display transcript in the app

---

## ✅ Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- FFmpeg installed and added to PATH

---

## ✅ Installation Steps (Windows)

### 1. Install Python and pip
Check your Python version:
```bash
python --version
```

### 2. Install Required Python Libraries
Run these commands in **Command Prompt** or **PowerShell**:
```bash
pip install streamlit
pip install openai-whisper
pip install transformers
pip install ffmpeg-python
```

### 3. Install FFmpeg on Windows
Whisper requires FFmpeg to process audio/video.

#### Steps:
1. Go to [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
2. Download **ffmpeg-release-full.7z** (precompiled build)
3. Extract the archive to `C:\ffmpeg`
4. Locate the `bin` folder inside the extracted directory (e.g., `C:\ffmpeg\bin`)
5. Add `C:\ffmpeg\bin` to your **PATH**:
   - Search **Environment Variables** → Edit PATH → Add `C:\ffmpeg\bin`
6. Verify installation:
```bash
ffmpeg -version
```

---

## ✅ Running the App
1. Save the Streamlit app code as `app.py`
2. Run the app:
```bash
streamlit run app.py
```
3. Upload your video file in the UI and wait for processing.

---

## ✅ Optional Enhancements
- **Download transcript as .txt file**
- **Generate subtitles (.srt)**
- **Enable GPU acceleration for Whisper** (requires CUDA and PyTorch with GPU support)

To enable GPU for Whisper:
```python
model = whisper.load_model("medium", device="cuda")
```

---

## ✅ Troubleshooting
- If `ffmpeg` is not recognized, ensure the `bin` folder is correctly added to PATH.
- If Whisper runs slowly, consider using a smaller model (`tiny`, `base`, `small`).

---

## ✅ Requirements File
Create a `requirements.txt` for easy installation:
```
streamlit
openai-whisper
transformers
ffmpeg-python
```
Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## ✅ Links
- [FFmpeg Builds for Windows](https://www.gyan.dev/ffmpeg/builds/)
- [OpenAI Whisper GitHub](https://github.com/openai/whisper)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)

---

## ✅ Performance Improvements & Future Options
Whisper transcription can be slow on CPU and large models. Here are ways to improve performance:

### 1. Choose Smaller Models
- **tiny (~75 MB)**: Fastest, lowest accuracy
- **base (~140 MB)**: Faster, decent accuracy
- **small (~500 MB)**: Good balance
- **medium (~1.4 GB)**: High accuracy, slower
- **large (~3 GB)**: Best accuracy, very slow on CPU

Update in code:
```python
model = whisper.load_model("small")  # or "base", "tiny"
```

### 2. Enable GPU Acceleration
If you have an NVIDIA GPU, install PyTorch with CUDA:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
Then load Whisper on GPU:
```python
model = whisper.load_model("medium", device="cuda")
```

### 3. Pre-download Models
Avoid downloading models every time:
```bash
whisper --model small
```
This caches the model locally.

### 4. Split Long Videos
For very long videos, split into smaller chunks (e.g., 10 minutes each) and process in parallel for faster results.

---

## ✅ Future Enhancements
- Add option in the script to select model size interactively.
- Auto-detect GPU and use it if available.
- Implement video chunking for large files.
- Add progress indicators for transcription.
