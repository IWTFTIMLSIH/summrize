import streamlit as st
import fitz  # PyMuPDF
import openai
import os

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["general"]["OPENAI_API_KEY"]

st.set_page_config(page_title="Summrize", layout="centered")
st.title("📄 Summrize – Alberta Condo Doc Review")
st.write("Upload your condo documents (PDF only) and get a smart AI-powered summary.")

uploaded_file = st.file_uploader("📂 Upload condo document", type=["pdf"])

def extract_text_from_pdf(file) -> str:
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def summarize_document(text: str) -> str:
    prompt = f"""
You are an Alberta-based condominium document reviewer. The following text is extracted from a condominium document.

Your task:
- Summarize the contents in plain English.
- Highlight any red flags (lawsuits, low reserves, special assessments, restrictive rules).
- Mention any important bylaws, financial or legal issues.

Document:
{text}

Provide the summary below:
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=700
    )
    return response["choices"][0]["message"]["content"]

if uploaded_file:
    st.info(f"📄 File uploaded: {uploaded_file.name}")
    with st.spinner("🔍 Reviewing your document..."):
        try:
            text = extract_text_from_pdf(uploaded_file)
            summary = summarize_document(text)
            st.success("✅ Review complete!")
            st.subheader("🧾 Document Summary")
            st.write(summary)
        except Exception as e:
            st.error(f"Something went wrong: {e}")