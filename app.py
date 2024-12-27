import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import whisper
import os
import io

# ------------------------------
# Load Whisper Model
# ------------------------------
@st.cache_resource
def load_whisper_model():
    """
    Load the Whisper model for audio transcription.
    Returns:
        whisper model
    """
    return whisper.load_model("tiny")


# ------------------------------
# Load NER Model
# ------------------------------
@st.cache_resource
def load_ner_model():
    """
    Load the Named Entity Recognition (NER) model pipeline.
    Returns:
        NER pipeline
    """
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    return pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


# ------------------------------
# Transcription Logic
# ------------------------------
def transcribe_audio(uploaded_file, whisper_model):
    """
    Transcribe audio into text using the Whisper model.
    Args:
        uploaded_file: Audio file uploaded by the user.
        whisper_model: Loaded Whisper model.
    Returns:
        str: Transcribed text from the audio file.
    """
    # Add ffmpeg to PATH
    ffmpeg_path = os.path.abspath('ffmpeg_bin')
    os.environ['PATH'] = ffmpeg_path + os.pathsep + os.environ['PATH']
    
    with open("temp.wav", "wb") as f:
        f.write(uploaded_file.read())

    result = whisper_model.transcribe("temp.wav")
    os.remove("temp.wav")  # Clean up temporary file
    return result["text"]


# ------------------------------
# Entity Extraction
# ------------------------------
def extract_entities(text, ner_pipeline):
    """
    Extract entities from transcribed text using the NER model.
    Args:
        text (str): Transcribed text.
        ner_pipeline: NER pipeline loaded from Hugging Face.
    Returns:
        dict: Grouped entities (ORGs, LOCs, PERs).
    """
    entities = ner_pipeline(text)
    grouped_entities = {
        "PER": set(entity["word"] for entity in entities if entity["entity_group"] == "PER"),
        "ORG": set(entity["word"] for entity in entities if entity["entity_group"] == "ORG"),
        "LOC": set(entity["word"] for entity in entities if entity["entity_group"] == "LOC"),
    }
    return grouped_entities


# ------------------------------
# Main Streamlit Application
# ------------------------------
def main():
    st.title("Meeting Transcription and Entity Extraction")

    # Student details
    STUDENT_NAME = "Your Name"
    STUDENT_ID = "Your Student ID"
    st.write(f"**{STUDENT_ID} - {STUDENT_NAME}**")

    # Load models
    st.write("Modeller yükleniyor...")
    whisper_model = load_whisper_model()
    ner_pipeline = load_ner_model()
    st.success("Modeller yüklendi!")

    # File upload
    uploaded_file = st.file_uploader("Ses dosyasını yükleyin (WAV formatında)", type=["wav"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")  # Play uploaded audio
        st.write("Ses dosyası işleniyor...")

        # Transcription
        transcription = transcribe_audio(uploaded_file, whisper_model)
        st.subheader("Transkripsiyon")
        st.write(transcription)

        # Entity Extraction
        st.write("Varlıklar çıkarılıyor...")
        entities = extract_entities(transcription, ner_pipeline)
        
        st.subheader("Varlıklar")
        st.write("**Kişiler (PER):**", ", ".join(entities["PER"]) if entities["PER"] else "Yok")
        st.write("**Organizasyonlar (ORG):**", ", ".join(entities["ORG"]) if entities["ORG"] else "Yok")
        st.write("**Lokasyonlar (LOC):**", ", ".join(entities["LOC"]) if entities["LOC"] else "Yok")


if __name__ == "__main__":
    main()
