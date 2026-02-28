# import streamlit as st
# import whisper
# import spacy
# import os
# import tempfile
# from python_files.clean_text import clean_text
# from python_files.gen_meet_summ import gen_meet_summe
# from python_files.extract_items import extr_items
# from python_files.gen_mom_pdf import create_pdf
#
#
#
#
# # Load models (cached to avoid reloading)
# @st.cache_resource
# def load_whisper():
#     return whisper.load_model("base")
#
# @st.cache_resource
# def load_nlp():
#     return spacy.load("en_core_web_sm")
#
#
#
# # Initialize models
# whisper_model = load_whisper()
# nlp = load_nlp()
#
#
#
#
# # Streamlit UI
# st.title("🤖 AI MOM Generator")
# st.markdown("---")
#
# input_type = st.radio(
#     "Select input type",
#     ["Upload Audio File", "Paste Transcript"],
#     horizontal= True
# )
#
# st.markdown("---")
#
#
#
# # Audio Upload
# if input_type == "Upload Audio File":
#     audio_file = st.file_uploader("Upload meeting audio", type=["mp3", "wav", "m4a"])
#
#     if audio_file:
#         with tempfile.NamedTemporaryFile(delete=False) as tmp:
#             tmp.write(audio_file.read())
#             tmp_path = tmp.name
#
#         with st.spinner("Transcribing audio..."):
#             result = whisper_model.transcribe(tmp_path)
#             transcript = result["text"]
#
#         st.subheader("Transcript")
#         st.write(transcript)
#
#
#
#
# # Text Input
# if input_type == "Paste Transcript":
#     transcript = st.text_area("Paste meeting transcript")
#
# st.markdown("---")
#
#
# # Generate MoM
# if st.button("🚀 Generate Minutes of Meeting", type="primary", use_container_width=True):
#     if not transcript.strip():
#         st.error("Please provide audio or transcript")
#     else:
#         with st.spinner("Generating AI summary..."):
#             cleaned_text = clean_text(transcript)
#             summary = gen_meet_summe(cleaned_text)
#             action_items = extr_items(cleaned_text)
#
#         st.subheader("📄 Meeting Summary")
#         st.write(summary)
#
#         st.subheader("✅ Action Items")
#         for a in action_items:
#             st.write("•", a)
#
#         pdf_path = create_pdf(summary, action_items)
#
#         with open(pdf_path, "rb") as f:
#             st.download_button(
#                 "⬇ Download MoM PDF",
#                 f,
#                 file_name="meeting_minutes.pdf"
#             )
#
#
# # Add footer
# st.markdown("---")
# st.markdown(
#     "<div style='text-align: center; color: gray; padding: 10px;'>"
#     "Powered by Whisper, spaCy, and Transformers"
#     "</div>",
#     unsafe_allow_html=True
# )


import streamlit as st
import whisper
import spacy
import os
import tempfile
from datetime import datetime
from python_files.clean_text import clean_text
from python_files.gen_meet_summ import gen_meet_summe
from python_files.extract_items import extr_items
from python_files.gen_mom_pdf import create_pdf
import pandas as pd
import re

# Page configuration
st.set_page_config(
    page_title="AI MOM Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .mom-section {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .action-item {
        background-color: #e8f4fd;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 30px;
        border-radius: 25px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)


# Load models (cached to avoid reloading)
@st.cache_resource
def load_whisper():
    return whisper.load_model("base")


@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")


# Initialize models
whisper_model = load_whisper()
nlp = load_nlp()

# Header
st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Meeting Minutes Generator</h1>
        <p>Transform your meetings into comprehensive, professional documentation</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    st.subheader("Meeting Details")
    meeting_title = st.text_input("Meeting Title", value="Weekly Team Sync")
    meeting_date = st.date_input("Meeting Date", value=datetime.now())
    meeting_time = st.time_input("Meeting Time", value=datetime.now().time())
    meeting_duration = st.number_input("Duration (minutes)", min_value=15, max_value=240, value=60)

    st.markdown("---")

    st.subheader("Participants")
    num_participants = st.number_input("Number of Participants", min_value=1, max_value=50, value=5)
    participants = []
    for i in range(num_participants):
        participant = st.text_input(f"Participant {i + 1} Name", key=f"participant_{i}")
        if participant:
            participants.append(participant)

    st.markdown("---")

    st.subheader("Output Options")
    include_timestamps = st.checkbox("Include timestamps in transcript", value=True)
    include_speakers = st.checkbox("Attempt speaker diarization", value=True)
    summary_length = st.select_slider(
        "Summary Length",
        options=["Brief", "Standard", "Detailed"],
        value="Standard"
    )

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📤 Input")
    input_type = st.radio(
        "Select input type",
        ["Upload Audio File", "Paste Transcript", "Record Audio"],
        horizontal=True
    )

    transcript = ""

    if input_type == "Upload Audio File":
        audio_file = st.file_uploader(
            "Upload meeting audio",
            type=["mp3", "wav", "m4a", "mp4"],
            help="Supported formats: MP3, WAV, M4A, MP4"
        )

        if audio_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name

            if st.button("🎤 Transcribe Audio", use_container_width=True):
                with st.spinner("Transcribing audio... This may take a moment."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        # Simulate progress (in real app, you'd get actual progress from whisper)
                        progress_bar.progress(i + 1)

                    result = whisper_model.transcribe(
                        tmp_path,
                        word_timestamps=include_timestamps,
                        verbose=False
                    )
                    transcript = result["text"]

                    if include_timestamps and "segments" in result:
                        st.session_state['segments'] = result['segments']

                    progress_bar.empty()
                    st.success("✅ Transcription complete!")

                    # Clean up temp file
                    os.unlink(tmp_path)

    elif input_type == "Paste Transcript":
        transcript = st.text_area(
            "Paste meeting transcript",
            height=200,
            placeholder="Paste your meeting transcript here..."
        )

    else:  # Record Audio
        st.info("🎙️ Audio recording feature requires additional setup. Please use file upload for now.")
        # In production, you'd implement audio recording here

with col2:
    if transcript:
        st.markdown("### 📝 Transcript Preview")
        with st.expander("View Full Transcript", expanded=False):
            st.write(transcript)

        # Quick stats
        word_count = len(transcript.split())
        st.markdown(f"**Word Count:** {word_count} words")
        st.markdown(f"**Estimated Duration:** {word_count // 150} minutes (at 150 words/min)")

st.markdown("---")

# Generate MoM button
if st.button("🚀 Generate Detailed Minutes of Meeting", use_container_width=True):
    if not transcript.strip():
        st.error("⚠️ Please provide audio or transcript first!")
    else:
        with st.spinner("🤖 AI is analyzing your meeting and generating comprehensive minutes..."):
            progress_bar = st.progress(0)

            # Step 1: Clean text (20%)
            progress_bar.progress(20, text="Cleaning and preprocessing text...")
            cleaned_text = clean_text(transcript)

            # Step 2: Generate summary based on length preference (40%)
            progress_bar.progress(40, text="Generating meeting summary...")
            summary_params = {
                "Brief": "Create a concise summary in 3-4 sentences",
                "Standard": "Create a balanced summary covering key points",
                "Detailed": "Create a comprehensive summary with all important details"
            }
            summary = gen_meet_summe(cleaned_text)

            # Step 3: Extract action items (60%)
            progress_bar.progress(60, text="Identifying action items and tasks...")
            action_items = extr_items(cleaned_text)

            # Step 4: Extract additional insights (80%)
            progress_bar.progress(80, text="Extracting decisions, questions, and key points...")

            # Enhanced NLP processing
            doc = nlp(cleaned_text)

            # Extract named entities (people, organizations, etc.)
            entities = {
                "PERSON": [],
                "ORG": [],
                "DATE": [],
                "GPE": []  # Geo-political entities (locations)
            }
            for ent in doc.ents:
                if ent.label_ in entities:
                    entities[ent.label_].append(ent.text)

            # Remove duplicates while preserving order
            for key in entities:
                entities[key] = list(dict.fromkeys(entities[key]))

            # Extract decisions (sentences with decision-related keywords)
            decision_keywords = ['decided', 'agreed', 'consensus', 'approved', 'confirmed', 'finalized']
            decisions = []
            for sent in doc.sents:
                if any(keyword in sent.text.lower() for keyword in decision_keywords):
                    decisions.append(sent.text)

            # Extract questions raised
            questions = []
            for sent in doc.sents:
                if '?' in sent.text:
                    questions.append(sent.text)

            # Identify key discussion points
            key_points = []
            for sent in list(doc.sents)[:5]:  # First 5 sentences as key points
                if len(sent.text.split()) > 10:  # Only substantive sentences
                    key_points.append(sent.text)

            # Extract deadlines if any
            deadline_pattern = r'\b(by|due|deadline|before)\s+(\w+\s+\d{1,2}(?:st|nd|rd|th)?(?:\s*,?\s*\d{4})?)'
            deadlines = re.findall(deadline_pattern, cleaned_text.lower())

            progress_bar.progress(100, text="Finalizing minutes...")
            progress_bar.empty()

        # Display results in organized sections
        st.success("✅ Meeting minutes generated successfully!")

        # Meeting header
        st.markdown(f"""
            <div class="mom-section" style="color: black;">
                <h2 style="color: black;">📋 {meeting_title}</h2>
                <p style="color: black;"><strong>Date:</strong> {meeting_date.strftime('%B %d, %Y')}</p>
                <p style="color: black;"><strong>Time:</strong> {meeting_time.strftime('%I:%M %p')}</p>
                <p style="color: black;"><strong>Duration:</strong> {meeting_duration} minutes</p>
            </div>
        """, unsafe_allow_html=True)

        # Participants
        if participants:
            st.markdown("### 👥 Participants")
            cols = st.columns(4)
            for idx, participant in enumerate(participants):
                cols[idx % 4].markdown(f"- {participant}")

        # Key Information in columns
        col1, col2, col3 = st.columns(3)

        with col1:
            if entities["PERSON"]:
                st.markdown("**👤 People Mentioned:**")
                for person in entities["PERSON"][:5]:
                    st.markdown(f"- {person}")

        with col2:
            if entities["ORG"]:
                st.markdown("**🏢 Organizations:**")
                for org in entities["ORG"][:5]:
                    st.markdown(f"- {org}")

        with col3:
            if entities["DATE"]:
                st.markdown("**📅 Dates Mentioned:**")
                for date in entities["DATE"][:5]:
                    st.markdown(f"- {date}")

        st.markdown("---")

        # Main summary
        st.markdown("### 📄 Executive Summary")
        st.markdown(f'<div class="mom-section" style="color: black;">{summary}</div>', unsafe_allow_html=True)

        # Key decisions
        if decisions:
            st.markdown("### ⚖️ Key Decisions")
            for i, decision in enumerate(decisions[:5], 1):
                st.markdown(f'<div class="action-item">{i}. {decision}</div>', unsafe_allow_html=True)

        # Action Items with priority
        if action_items:
            st.markdown("### ✅ Action Items")
            for i, item in enumerate(action_items, 1):
                priority = "🔴" if i <= len(action_items) // 3 else "🟡" if i <= 2 * len(action_items) // 3 else "🟢"
                st.markdown(f'<div class="action-item" style="color: black;">{priority} Task {i}: {item}</div>',
                            unsafe_allow_html=True)

        # Questions raised
        if questions:
            st.markdown("### ❓ Questions Raised")
            for i, question in enumerate(questions[:3], 1):
                st.markdown(f"{i}. {question}")

        # Deadlines
        if deadlines:
            st.markdown("### ⏰ Deadlines")
            for deadline in deadlines:
                st.markdown(f"- {deadline[0]} {deadline[1]}")

        # Timestamps if available
        if 'segments' in st.session_state:
            st.markdown("### ⏱️ Timeline")
            timeline_df = pd.DataFrame([
                {
                    "Time": f"{seg['start']:.1f}s - {seg['end']:.1f}s",
                    "Content": seg['text'][:100] + "..."
                }
                for seg in st.session_state['segments'][:5]
            ])
            st.dataframe(timeline_df, use_container_width=True)

        # Generate PDF with all information
        st.markdown("---")

        # Create comprehensive PDF
        pdf_path = create_pdf(
            summary=summary,
            action_items=action_items,
            meeting_title=meeting_title,
            meeting_date=meeting_date,
            participants=participants,
            decisions=decisions,
            questions=questions,
            entities=entities
        )

        # Download options
        col1, col2, col3 = st.columns(3)

        with open(pdf_path, "rb") as f:
            pdf_data = f.read()

            with col1:
                st.download_button(
                    "📥 Download PDF Minutes",
                    pdf_data,
                    file_name=f"meeting_minutes_{meeting_date.strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            with col2:
                # Text version
                text_content = f"""
                MEETING MINUTES
                Title: {meeting_title}
                Date: {meeting_date}

                SUMMARY:
                {summary}

                ACTION ITEMS:
                {chr(10).join([f'- {item}' for item in action_items])}
                """
                st.download_button(
                    "📄 Download Text Version",
                    text_content,
                    file_name=f"meeting_minutes_{meeting_date.strftime('%Y%m%d')}.txt",
                    use_container_width=True
                )

            with col3:
                if st.button("📧 Email Minutes", use_container_width=True):
                    st.info("Email functionality would be implemented here")

        # Clean up
        os.unlink(pdf_path)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; padding: 10px;'>
        <p>🚀 Powered by Whisper, spaCy, and Transformers | Version 2.0</p>
        <p style='font-size: 0.8em;'>© 2024 AI Meeting Minutes Generator. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)

# Session state initialization
if 'segments' not in st.session_state:
    st.session_state['segments'] = []