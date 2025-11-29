# =====================================================================
# SkillGapAI – Milestone 1: Premium Enhanced UI | Data Ingestion & Parsing
# =====================================================================

import streamlit as st
import docx2txt
import PyPDF2
import re

# ---------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="SkillGapAI – Milestone 1",
    layout="wide"
)

# ---------------------------------------------------------------------
# CUSTOM CSS FOR MODERN UI
# ---------------------------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #F4F7FB;
}

/* Gradient Header */
.header {
    background: linear-gradient(90deg, #102A43, #243B53, #486581);
    padding: 25px;
    border-radius: 16px;
    color: white;
    margin-bottom: 32px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

/* Glassmorphism Card */
.section-card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(8px);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0 8px 18px rgba(0,0,0,0.06);
    margin-bottom: 25px;
    transition: transform .2s ease-in-out;
}

.section-card:hover {
    transform: scale(1.01);
}

/* Text Area */
textarea {
    border-radius: 14px !important;
    padding: 12px !important;
}

/* Footer */
.footer {
    text-align:center; 
    color: #6B7280; 
    margin-top: 30px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# HEADER UI
# ---------------------------------------------------------------------
st.markdown("""
<div class='header'>
    <h2 style='margin-bottom:4px;'>🧠 SkillGapAI – Milestone 1</h2>
    <p style='font-size:17px;'>Data Ingestion & Parsing • Extract • Clean • Download</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# TEXT CLEANER
# ---------------------------------------------------------------------
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.replace("\r", " ").replace("\n", " ").strip()

# ---------------------------------------------------------------------
# FILE PARSER
# ---------------------------------------------------------------------
def extract_text(uploaded_file):
    text = ""

    try:
        name = uploaded_file.name.lower()

        # PDF extraction
        if name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content + " "

        # DOCX extraction
        elif name.endswith(".docx"):
            text = docx2txt.process(uploaded_file)

        # TXT extraction
        elif name.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8")

        else:
            st.error("❌ Unsupported file format.")
            return ""

        return clean_text(text)

    except Exception as e:
        st.error(f"⚠️ Error extracting text: {e}")
        return ""

# ---------------------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------------------
col1, col2 = st.columns([1.1, 2])

# ---------------- LEFT PANEL ----------------
with col1:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    
    st.markdown("### 📤 Upload Resume or Job Description")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "txt"]
    )
    
    st.info("Supported: **PDF • DOCX • TXT**")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- RIGHT PANEL ----------------
with col2:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    
    st.markdown("### 🧾 Extracted & Cleaned Text Preview")

    if uploaded_file:
        with st.spinner("🔍 Extracting and cleaning text..."):
            extracted = extract_text(uploaded_file)

        st.success(f"✔ File Parsed Successfully: {uploaded_file.name}")

        st.text_area(
            "Cleaned Extracted Text",
            extracted[:6000],
            height=350,
            key="parsed_text"
        )

        st.caption(
            f"Characters: {len(extracted)} • Words: {len(extracted.split())}"
        )

        st.download_button(
            label="💾 Download Cleaned Text",
            data=extracted,
            file_name=f"parsed_{uploaded_file.name.split('.')[0]}.txt",
            mime="text/plain"
        )

    else:
        st.warning("📌 Upload a file to view extracted content here.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# OPTIONAL MANUAL JD INPUT
# ---------------------------------------------------------------------
st.markdown("<div class='section-card'>", unsafe_allow_html=True)

st.subheader("📋 Optional: Paste Job Description")

jd_text = st.text_area(
    "Paste job description below:",
    height=180
)

if jd_text.strip():
    cleaned_jd = clean_text(jd_text)

    st.text_area(
        "Cleaned Job Description Output",
        cleaned_jd,
        height=180
    )

    st.caption(
        f"Characters: {len(cleaned_jd)} • Words: {len(cleaned_jd.split())}"
    )

    st.download_button(
        label="💾 Download Cleaned JD",
        data=cleaned_jd,
        file_name="cleaned_job_description.txt"
    )

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------
st.markdown("""
<div class='footer'>
    Milestone 1 • Enhanced Premium UI • SkillGapAI Project
</div>
""", unsafe_allow_html=True)
