import streamlit as st
import os
import fitz  # PyMuPDF
from tempfile import NamedTemporaryFile
import pyttsx3

st.set_page_config(page_title="Research Paper Audiobook Reader", layout="wide")

# Setup directories
UPLOAD_DIR = "data/uploads"
AUDIO_DIR = "data/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# Initialize TTS engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 160)

# ---- Functions ---- #
def extract_text_from_pdf(pdf_path):
    text_by_page = []
    doc = fitz.open(pdf_path)
    for page in doc:
        text_by_page.append(page.get_text())
    return text_by_page

def generate_audio_from_text(text, output_path):
    tts_engine.save_to_file(text, output_path)
    tts_engine.runAndWait()

# ---- Streamlit UI ---- #
st.title("📖 Research Paper Audiobook Reader")

uploaded_file = st.file_uploader("Upload a research paper (PDF)", type="pdf")

if uploaded_file:
    with NamedTemporaryFile(delete=False, dir=UPLOAD_DIR, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.success("PDF uploaded successfully!")

    st.subheader("Extracted Sections")
    pages = extract_text_from_pdf(tmp_path)
    selected_page = st.selectbox("Select a page to listen to", range(1, len(pages) + 1))

    page_text = pages[selected_page - 1]
    st.text_area("Page Text", page_text, height=300)

    audio_file_path = os.path.join(AUDIO_DIR, f"audio_page_{selected_page}.mp3")

    if st.button("🔊 Generate Audio"):
        generate_audio_from_text(page_text, audio_file_path)
        st.audio(audio_file_path)

    if os.path.exists(audio_file_path):
        st.audio(audio_file_path, format="audio/mp3")